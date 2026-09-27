"""The S3/S9 content index, as a kept tool instead of a throwaway script.

S3 and S9 each rebuilt this index from a written method and discarded the script. This is
that method (notes/s9-backlog-remeasure.md sections 2 and 11) with the two D20 blind spots
fixed. `--legacy` switches both fixes off, so the published S9 numbers can be reproduced
and every delta is measured on one instrument, not two.

  Fix 1 (alias names). Pinned declares some ServUO type names only as strings inside
    [TypeAlias("Server.Items.GargishClothKilt", ...)]. AssemblyHandler resolves those in the
    same lookup as real type names (AssemblyHandler.cs:251-263), so they are indexed here as
    declarations of the type they name. Legacy mode stripped them with every other string.
  Fix 2 (secondary types). A file is discarded when pinned declares its primary type. Legacy
    mode only ever saw the file's other types if a candidate referenced them. The fixed
    index reports every one, classified mechanically where it can be and marked
    `unresolved` where it cannot. It is not a backlog and is never summed as one.

  Also fixed, because it is the label that cost time: legacy `upstream` mixed "a member of a
  class ModernUO ships" (a patch) with "a type that lives in a discarded file" (an extract,
  ordinary content work). They are separate buckets here: `upstream` and `extract`.

Usage:
  python tools/content_index.py row artifacts [--legacy] [--ours PATH] [--json OUT]
  python tools/content_index.py hidden [--row artifacts]     # every secondary type, classified
  python tools/content_index.py compare-s9 artifacts --ours PATH   # the three deltas
  python -m unittest tools/test_content_index.py

Regression checks live in test_content_index.py. The one S9 set: legacy step 1 returns
3,134 of 6,144 against the S9-era tree.
"""
import argparse, json, os, re, sys
from collections import defaultdict

SERVUO = r'D:\UO\ServUO-pub57'
S = os.path.join(SERVUO, 'Scripts')
M = r'D:\UO\ModernUO-pinned\Projects'
C = r'D:\ShatteredLegacy\server\customizations'

# Row definitions, S9 section 11. Prefixes relative to ServUO Scripts, forward slashes.
ROWS = {
    'cc4': ['Services/Revamped Dungeons'],
    'artifacts': ['Items/Artifacts', 'Items/Equipment'],
    'cc7': ['Items/Addons', 'Items/Decorative', 'Services/New Magincia'],
    'cc7extra': ['Items/Resource', 'Services/BulkOrders'],
    'cc5': ['Services/Expansions/High Seas/Items', 'Services/Expansions/High Seas/Mobiles'],
}

# S9 section 2. Each was verified there by reading both implementations; not re-derived here.
EQUIV = {'FlipableAttribute', 'Flipable', 'ITool', 'IFlipable', 'ItemQuality', 'IRepairable',
         'IChopable', 'IQuality', 'IResource', 'TalismanSkill', 'SimpleContextMenuEntry'}
# GenericWriter and TimerCallback are not in S9's printed list; they are the same conversions as
# GenericReader and TimerStateCallback, and S9's appendix buckets their files as if applied.
CONVERT = {'GenericReader', 'GenericWriter', 'TimerCallback', 'Constructable', 'ReadItem', 'ReadMobile', 'IsPlayer',
           'UpdateProperties', 'GetEnumeratedMobiles', 'TimerStateCallback'}
DELETABLE = {'IsArtifact', 'CanBeWornByGargoyles', 'Alterable', 'ExcludeDeedHue', 'SetWearable'}
# S3 section 2 names these and ends the list with an ellipsis. The rest are not recoverable,
# so the `Internal` prefix rule stands in for them. A reproduction gap, stated in the note.
BLACKLIST = {'InternalTarget', 'InternalTimer', 'InternalBuyInfo', 'InternalSellInfo', 'Misc',
             'City', 'Filter', 'Form'}

MODIFIERS = r'(?:public|private|protected|internal|static|virtual|override|abstract|readonly|const|sealed|new|extern|volatile|async|unsafe|partial|event)'

RE_BLOCK_COMMENT = re.compile(r'/\*.*?\*/', re.S)
RE_LINE_COMMENT = re.compile(r'//[^\n]*')
RE_STRING = re.compile(r'@"(?:""|[^"])*"|\$?"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])\'')
RE_ALIAS = re.compile(r'TypeAlias\s*\(([^)]*)\)')
RE_DIRECTIVE = re.compile(r'^\s*(?:using\s+[^;(]*;|namespace\s+[\w.]+\s*;?)', re.M)
RE_TYPE = re.compile(r'\b(class|struct|interface|enum|record)\s+(\w+)(?:\s*<[^>{]*>)?\s*(?::\s*([\w.]+))?')
# Delimiters are lookarounds: consuming the `;` that ends one member hides the next one.
RE_MEMBER = re.compile(r'(?:^|(?<=[;{}\]]))\s*(?:' + MODIFIERS + r'\s+)+[\w<>\[\],.?\s]*?\b(\w+)\s*(?:<[^>(]*>)?\s*(?=\(|\{|=>|=|;)', re.M)
RE_IDENT = re.compile(r'\b[A-Z_]\w*\b')
RE_GRAPHIC = re.compile(r':\s*base\s*\(\s*(0x[0-9A-Fa-f]+)')


def walk(root):
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.cs'):
                yield os.path.join(d, f)


def clean(raw):
    """Comments out, strings emptied. Alias strings are collected first, from the raw text."""
    t = RE_LINE_COMMENT.sub('', RE_BLOCK_COMMENT.sub('', raw))
    aliases = [s.split('.')[-1] for a in RE_ALIAS.findall(t) for s in re.findall(r'"([^"]+)"', a)]
    return RE_STRING.sub('""', t), aliases


def type_spans(t):
    """Each declared type with its kind, base, body span and whether it is nested in another type."""
    out, stack, pending = [], [], None
    marks = [(m.start(), 'type', m) for m in RE_TYPE.finditer(t)]
    marks += [(m.start(), ch, None) for m in re.finditer(r'[{};]', t) for ch in [m.group()]]
    marks.sort(key=lambda x: x[0])
    for pos, what, m in marks:
        if what == 'type':
            pending = m
        elif what == '{':
            if pending is not None:
                rec = {'name': pending.group(2), 'kind': pending.group(1),
                       'base': (pending.group(3) or '').split('.')[-1] or None,
                       'nested': any(s is not None for s in stack), 'start': pos, 'end': len(t)}
                out.append(rec)
                stack.append(rec)
                pending = None
            else:
                stack.append(None)
        elif what == '}':
            if stack:
                rec = stack.pop()
                if rec is not None:
                    rec['end'] = pos
        elif what == ';':
            pending = None
    return out


class FileInfo:
    __slots__ = ('rel', 'types', 'members', 'idents', 'aliases', 'primary', 'lines', 'graphics')

    def __init__(self, rel, raw):
        t, self.aliases = clean(raw)
        self.rel = rel
        self.lines = raw.count('\n') + 1
        self.types = type_spans(t)
        tnames = {x['name'] for x in self.types}
        # Enum members are deliberately not members: S9 did not index them (its appendix prints
        # `unknown: Good`), and changing that here would confound the D20 delta. See the note.
        self.members = {n for n in RE_MEMBER.findall(t) if n not in tnames}
        self.idents = set(RE_IDENT.findall(RE_DIRECTIVE.sub('', t)))
        stem = os.path.basename(rel)[:-3]
        names = [x['name'] for x in self.types]
        self.primary = stem if stem in names else (names[0] if names else None)
        self.graphics = {}
        for x in self.types:
            g = RE_GRAPHIC.search(t, x['start'], x['end'])
            if g:
                self.graphics[x['name']] = int(g.group(1), 16)


def load(root):
    files = {}
    for p in walk(root):
        with open(p, encoding='utf-8', errors='ignore') as fh:
            rel = os.path.relpath(p, root).replace('\\', '/')
            files[rel] = FileInfo(rel, fh.read())
    return files


class Tree:
    """Declarations and identifiers of pinned + ours, the side a name must resolve against."""

    def __init__(self, files_list, use_aliases):
        self.types, self.idents, self.alias_only, self.graphic = set(), set(), {}, defaultdict(set)
        declared = set()
        for files in files_list:
            for f in files.values():
                for x in f.types:
                    declared.add(x['name'])
                for n, g in f.graphics.items():
                    self.graphic[g].add(n)
                self.idents |= f.idents
        self.types = set(declared)
        if use_aliases:
            for files in files_list:
                for f in files.values():
                    for a in f.aliases:
                        if a not in declared:
                            self.alias_only.setdefault(a, f.rel)
            self.types |= set(self.alias_only)
            self.idents |= set(self.alias_only)


class Index:
    def __init__(self, ours=C, legacy=False, _cache={}):
        self.legacy = legacy
        key = ('S',)
        if key not in _cache:
            _cache[key] = load(S)
            _cache[('SRV',)] = load(os.path.join(SERVUO, 'Server'))
        if ('M',) not in _cache:
            _cache[('M',)] = load(M)
        if ('C', ours) not in _cache:
            _cache[('C', ours)] = load(ours)
        self.sv, self.muo, self.ours = _cache[('S',)], _cache[('M',)], _cache[('C', ours)]
        self.sv_core = _cache[('SRV',)]
        self.tree = Tree([self.muo, self.ours], use_aliases=not legacy)

        # ServUO ownership: which files declare a name as a type, which as a member.
        self.type_owner, self.member_owner = defaultdict(set), defaultdict(set)
        self.parent = {}
        for files in (self.sv_core, self.sv):
            for f in files.values():
                for x in f.types:
                    if files is self.sv:
                        self.type_owner[x['name']].add(f.rel)
                    if x['base']:
                        self.parent.setdefault(x['name'], x['base'])
                if files is self.sv:
                    for n in f.members:
                        self.member_owner[n].add(f.rel)

        # Step 1: a file is discarded when pinned or ours declares (fixed: or aliases) its primary type.
        self.discarded, self.discard_reason = set(), {}
        for rel, f in self.sv.items():
            if f.primary and f.primary in self.tree.types:
                self.discarded.add(rel)
                self.discard_reason[rel] = 'aliased' if f.primary in self.tree.alias_only else 'declared'

    # ---- step 2 ------------------------------------------------------------------------------
    def missing(self, f):
        own = {x['name'] for x in f.types} | f.members
        return sorted(n for n in f.idents
                      if n not in self.tree.idents and n not in own
                      and n not in EQUIV and n not in CONVERT and n not in DELETABLE
                      and n not in BLACKLIST and not n.startswith('Internal'))

    def resolve_name(self, n, row_cands):
        owners = self.type_owner.get(n, set()) | self.member_owner.get(n, set())
        if owners & row_cands:
            return 'in-row', None
        outside = sorted(o for o in owners if o not in self.discarded and o not in row_cands)
        if outside:
            return 'elsewhere', outside[0]
        if owners:
            if self.legacy or self.member_owner.get(n):
                return 'upstream', None
            return 'extract', sorted(self.type_owner[n])[0]
        return 'unknown', None

    def row(self, name):
        prefixes = ROWS[name]
        raw = sorted(r for r in self.sv if any(r.startswith(p + '/') for p in prefixes))
        cands = {r for r in raw if r not in self.discarded and self.sv[r].types}
        out = {'raw': raw, 'discarded': sorted(r for r in raw if r in self.discarded),
               'aliased': sorted(r for r in raw if self.discard_reason.get(r) == 'aliased'),
               'no_types': sorted(r for r in raw if not self.sv[r].types), 'files': {}, 'extra': set()}
        for r in sorted(cands):
            by = defaultdict(list)
            for n in self.missing(self.sv[r]):
                kind, owner = self.resolve_name(n, cands)
                by[kind].append(n)
                if kind in ('elsewhere', 'extract') and owner:
                    out['extra'].add(owner)
            # Legacy merges unknown into upstream, as S9 did. Fixed keeps them apart: an unknown
            # name means read the file, which is not the same job as patching a base class.
            if by['upstream'] or (self.legacy and by['unknown']):
                bucket = 'upstream'
            elif by['unknown']:
                bucket = 'unknown'
            elif by['extract']:
                bucket = 'extract'
            elif by['elsewhere']:
                bucket = 'elsewhere'
            elif by['in-row']:
                bucket = 'in-row'
            else:
                bucket = 'drops'
            out['files'][r] = {'bucket': bucket, 'names': {k: v for k, v in by.items() if v}}
        out['extra'] = sorted(out['extra'])
        return out

    # ---- fix 2: every secondary type of a discarded file --------------------------------------
    def chain(self, n):
        seen = []
        while n in self.parent and n not in seen and len(seen) < 20:
            seen.append(n)
            n = self.parent[n]
        return seen + [n]

    def classify(self, f, x):
        n = x['name']
        if n in EQUIV:
            return 'equivalent'
        if x['nested']:
            return 'nested helper'
        if x['kind'] in ('enum', 'interface', 'struct'):
            return 'support: ' + x['kind']
        ch = self.chain(n)
        for base, label in (('Gump', 'gump'), ('ContextMenuEntry', 'context menu entry'),
                            ('Timer', 'timer'), ('Target', 'target'), ('Prompt', 'prompt'),
                            ('Hair', 'hair/beard'), ('Beard', 'hair/beard'), ('BaseHair', 'hair/beard'),
                            ('Spell', 'spell'), ('BaseAI', 'ai'), ('Region', 'region'),
                            ('QuestSystem', 'quest'), ('BaseQuest', 'quest'), ('QuestObjective', 'quest'),
                            ('Mobile', 'mobile'), ('Item', 'item')):
            if base in ch[1:]:
                return label
        return 'unresolved'

    def hidden(self, prefixes=None):
        rows = []
        for rel in sorted(self.discarded):
            if prefixes and not any(rel.startswith(p + '/') for p in prefixes):
                continue
            f = self.sv[rel]
            for x in f.types:
                n = x['name']
                if n == f.primary or n in self.tree.types or n.startswith('Internal'):
                    continue
                cls = self.classify(f, x)
                g = f.graphics.get(n)
                same = sorted(self.tree.graphic.get(g, ())) if g is not None else []
                rows.append({'file': rel, 'primary': f.primary, 'type': n, 'class': cls,
                             'graphic': hex(g) if g is not None else None, 'pinned_same_graphic': same})
        return rows


# ---- output --------------------------------------------------------------------------------------
BUCKETS = [('drops', 'drops straight in'), ('in-row', 'needs another file of this row'),
           ('elsewhere', 'co-port: needs a ServUO file outside the row'),
           ('extract', 'extract: needs a type that lives inside a discarded file (content work, read it)'),
           ('unknown', 'unknown: uses a name nothing in ServUO Scripts declares (read it)'),
           ('upstream', 'upstream: needs a member of a class ModernUO ships (patch or carrier; legacy: or unknown)')]


def fmt_names(names):
    parts = []
    for k in ('in-row', 'elsewhere', 'extract', 'upstream', 'unknown'):
        if names.get(k):
            parts.append(('' if k == 'in-row' else k + ': ') + ', '.join(names[k]))
    return ' | '.join(parts)


def print_row(idx, name):
    r = idx.row(name)
    files = r['files']
    count = defaultdict(int)
    for v in files.values():
        count[v['bucket']] += 1
    mode = 'legacy (S9 method)' if idx.legacy else 'fixed (D20)'
    print(f'# {name}: {mode}')
    print(f'raw {len(r["raw"])} -> discarded {len(r["discarded"])} (of which aliased {len(r["aliased"])}) '
          f'-> no types {len(r["no_types"])} -> candidates {len(files)}')
    print(' . '.join(f'{lab.split(":")[0]} {count[k]}' for k, lab in BUCKETS))
    for k, lab in BUCKETS:
        print(f'\n## {lab} ({count[k]})')
        for rel, v in files.items():
            if v['bucket'] == k:
                print(f'  {rel}' + (f'  <- {fmt_names(v["names"])}' if v['names'] else ''))
    print(f'\n## extra ServUO files co-port and extract pull in ({len(r["extra"])})')
    for e in r['extra']:
        print('  ' + e)
    print(f'\n## discarded because pinned only aliases the primary type ({len(r["aliased"])})')
    for a in r['aliased']:
        print(f'  {a}  = {idx.sv[a].primary} -> alias in {idx.tree.alias_only[idx.sv[a].primary]}')
    return r


def print_hidden(idx, prefixes):
    rows = idx.hidden(prefixes)
    by = defaultdict(list)
    for x in rows:
        by[x['class']].append(x)
    files = {x['file'] for x in rows}
    print(f'# secondary types of discarded files that neither pinned nor ours declares or aliases')
    print(f'{len(rows)} types in {len(files)} files. NOT a backlog: classified below, unresolved means read it.')
    order = sorted(by, key=lambda k: (k == 'unresolved', -len(by[k])))
    for k in order:
        print(f'  {k:22} {len(by[k])}')
    for k in order:
        print(f'\n## {k} ({len(by[k])})')
        for x in by[k]:
            same = f'  [pinned or ours has same graphic {x["graphic"]}: {", ".join(x["pinned_same_graphic"])}]' \
                if x['pinned_same_graphic'] else ''
            print(f'  {x["file"]} | primary {x["primary"]} | {x["type"]}{same}')
    return rows


def parse_s9(path, row_title):
    """S9's published appendix for one row: file -> bucket."""
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    heads = {'drops straight in': 'drops', 'portable once other files': 'in-row',
             'needs ServUO files from outside': 'elsewhere', 'needs an upstream member': 'upstream',
             'filtered out at step 1': 'discarded'}
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith('#### '):
            cur = None
            if line.startswith('#### ' + row_title + ' '):
                for k, v in heads.items():
                    if k in line:
                        cur = v
        elif cur and line.startswith(('Items/', 'Services/', 'Mobiles/', 'Misc/')):
            out[line[:line.index('.cs') + 3]] = cur
    return out


def compare_s9(ours, rowname, s9_note, row_title):
    s9 = parse_s9(s9_note, row_title)
    legacy = Index(ours, legacy=True)
    fixed = Index(ours, legacy=False)
    lr, fr = legacy.row(rowname), fixed.row(rowname)

    def state(r, rel):
        if rel in r['files']:
            return r['files'][rel]['bucket']
        return 'discarded' if rel in r['discarded'] else 'no types'

    allf = sorted(set(s9) | set(lr['raw']))
    agree = sum(1 for f in allf if s9.get(f) == state(lr, f))
    print(f'# reproduction: legacy mode vs S9 appendix, row {rowname}')
    print(f'{agree} of {len(allf)} files in the same bucket')
    for f in allf:
        if s9.get(f) != state(lr, f):
            print(f'  differs: {f}  S9 {s9.get(f)}  legacy {state(lr, f)}')

    print(f'\n# transitions S9 published -> fixed')
    trans = defaultdict(list)
    for f in allf:
        trans[(s9.get(f), state(fr, f))].append(f)
    for (a, b), fs in sorted(trans.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        if a != b:
            print(f'\n## {a} -> {b} ({len(fs)})')
            for f in fs:
                names = fr['files'].get(f, {}).get('names')
                print(f'  {f}' + (f'  <- {fmt_names(names)}' if names else ''))
    return s9, lr, fr


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=['row', 'hidden', 'compare-s9', 'filter'])
    ap.add_argument('row', nargs='?', default='artifacts', choices=sorted(ROWS))
    ap.add_argument('--legacy', action='store_true', help='S9 method: no alias names, no extract bucket')
    ap.add_argument('--ours', default=C, help='customizations tree (an older export reproduces an old survey)')
    ap.add_argument('--all', action='store_true', help='hidden: whole tree, not one row')
    ap.add_argument('--s9', default=os.path.join(os.path.dirname(__file__), '..', 'notes', 's9-backlog-remeasure.md'))
    ap.add_argument('--s9-title', default='Artifacts + equipment')
    ap.add_argument('--json', help='also write the result as JSON')
    a = ap.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    if a.cmd == 'compare-s9':
        compare_s9(a.ours, a.row, a.s9, a.s9_title)
        return
    idx = Index(a.ours, legacy=a.legacy)
    if a.cmd == 'filter':
        print(f'step 1 discards {len(idx.discarded)} of {len(idx.sv)} ServUO files '
              f'({sum(1 for v in idx.discard_reason.values() if v == "aliased")} of them aliased)')
        return
    res = print_row(idx, a.row) if a.cmd == 'row' else print_hidden(idx, None if a.all else ROWS[a.row])
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(res, fh, indent=1, default=list)


if __name__ == '__main__':
    main()
