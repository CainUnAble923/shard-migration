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

  Fix 3 (enum members, D24). ServUO files use enum members (`Alignment.Good`) that pinned lacks.
    Legacy mode indexed no enum member, so such a name fell into `unknown`. Fixed mode owns each
    member by the file declaring its enum, but only where the referencing file writes the
    member qualified by that enum (`Alignment.Good`), which is the only way C# names it outside
    the enum. That qualifier is also the tie-break against a type or member of the same name:
    see Index.enum_owners.
  Fix 4 (generated names, D24). `[SerializableField] private int _recipeID;` in pinned or ours
    emits a `RecipeID` property that no source file spells. Fixed mode adds the generated name to
    the resolving side, derived by `generated_name`, which matches ModernUO.Serialization.Generator
    2.14.3's own SourceGeneration.GetPropertyName on every field name pinned declares.
  Fix 5 (preprocessor lines, P2 2026-09-28). `#region Mondain's Legacy` put `Mondain` in the file's
    names, and nothing declares it, so ten cc7 addons were `unknown` on a region label. Fixed mode
    reads names from code only, on both sides; legacy keeps S9's reading.

  Also fixed, because it is the label that cost time: legacy `upstream` mixed "a member of a
  class ModernUO ships" (a patch) with "a type that lives in a discarded file" (an extract,
  ordinary content work). They are separate buckets here: `upstream` and `extract`.

Usage:
  python tools/content_index.py row artifacts [--legacy] [--ours PATH] [--json OUT]
  python tools/content_index.py hidden [--row artifacts]     # every secondary type, classified
  python tools/content_index.py compare-s9 artifacts --ours PATH   # the three deltas
  python tools/content_index.py reach [--ours PATH] [--sources] [--twins] [--json OUT]
      # D33: what, other than itself, puts each of our types in the world. --sources adds what does it
      # in ServUO, ranked by files it would reach; --twins sweeps for pinned types under another name.
      # Reads pinned with our patches applied, as docker/uo/apply-patches.sh applies them (cc-P27), so an
      # export for --ours must carry that script: `git archive HEAD server docker/uo/apply-patches.sh`.
  python -m unittest tools/test_content_index.py

Regression checks live in test_content_index.py. The one S9 set: legacy step 1 returns
3,134 of 6,144 against the S9-era tree.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
from collections import defaultdict

SERVUO = r'D:\UO\ServUO-pub57'
S = os.path.join(SERVUO, 'Scripts')
M = r'D:\UO\ModernUO-pinned\Projects'
# CONTENT_INDEX_OURS points the default at an export (`git archive HEAD server | tar -x`) when the live
# shard tree must not be read, e.g. while it is being deployed.
C = os.environ.get('CONTENT_INDEX_OURS', r'D:\ShatteredLegacy\server\customizations')

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
# A whole preprocessor line: `#region Bizaar Authority Storage`, `#pragma warning disable CS0618`.
RE_PREPROC = re.compile(r'^[ \t]*#[^\n]*', re.M)
RE_TYPE = re.compile(r'\b(class|struct|interface|enum|record)\s+(\w+)(?:\s*<[^>{]*>)?\s*(?::\s*([\w.]+))?')
# Delimiters are lookarounds: consuming the `;` that ends one member hides the next one.
RE_MEMBER = re.compile(r'(?:^|(?<=[;{}\]]))\s*(?:' + MODIFIERS + r'\s+)+[\w<>\[\],.?\s]*?\b(\w+)\s*(?:<[^>(]*>)?\s*(?=\(|\{|=>|=|;)', re.M)
RE_IDENT = re.compile(r'\b[A-Z_]\w*\b')
# The first `: base(...)` argument when it is an integer literal. Decimal (P2, 2026-09-28) only when the
# argument is the literal alone, `base(40681)`, at least two digits (an amount `base(1)` is not read) and within the
# art range (a cliloc `base(1094954)` is not read).
# A later argument (`base(bonus, 0x030C)`) and an inherited graphic are still not read: see index-blindspots.
RE_GRAPHIC = re.compile(r':\s*base\s*\(\s*(0x[0-9A-Fa-f]+|[1-9]\d+(?=\s*[,)]))')
# The field a [SerializableField(...)] (plus any further attributes) stands on: its last identifier
# before `;` or `=`. Pinned writes `Dictionary<Mobile, int>_damageEntries;` once, so no space is required.
RE_SERFIELD = re.compile(r'\[SerializableField\b[^\]]*\](?:\s*\[[^\]]*\])*\s*[^;=\[]*?\b(\w+)\s*(?:=[^;]*)?;')
# The identifier directly before a `.` that ends the searched span: the qualifier of what follows it.
RE_QUALIFIER = re.compile(r'(\w+)\s*\.\s*$')


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


def generated_name(field):
    """The property ModernUO.Serialization.Generator emits for a [SerializableField] field.

    Checked against the generator itself (SourceGeneration.GetPropertyName, 2.14.3, invoked on all
    of pinned's field names; notes/index-blindspots.md "D24"): drop `m_` or leading underscores,
    capitalise each underscore-separated part's first letter, touch nothing else. So `_recipeID`
    is `RecipeID`, `_bardingHP` is `BardingHP`, `_line1` is `Line1`. Pinned's attribute arguments
    are order, getter, setter and isVirtual; none of them renames the property.
    """
    n = field[2:] if field.startswith('m_') else field.lstrip('_')
    return ''.join(p[:1].upper() + p[1:] for p in n.split('_') if p)


def enum_members(body):
    """Member names of one enum body. Values may be expressions; attributes are dropped."""
    out = []
    for part in re.sub(r'\[[^\]]*\]', '', body).split(','):
        m = re.match(r'\s*([A-Za-z_]\w*)', part)
        if m:
            out.append(m.group(1))
    return out


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
    __slots__ = ('rel', 'types', 'members', 'idents', 'idents_code', 'aliases', 'primary', 'lines',
                 'graphics', 'enums', 'generated', 'quals')

    def __init__(self, rel, raw, quals=False):
        t, self.aliases = clean(raw)
        self.rel = rel
        self.lines = raw.count('\n') + 1
        self.types = type_spans(t)
        tnames = {x['name'] for x in self.types}
        # Enum members are deliberately not members: S9 did not index them (its appendix prints
        # `unknown: Good`). They are kept apart in `enums` and only fixed mode reads them (fix 3).
        self.members = {n for n in RE_MEMBER.findall(t) if n not in tnames}
        self.idents = set(RE_IDENT.findall(RE_DIRECTIVE.sub('', t)))
        # Fix 5: the same without preprocessor lines. Legacy reads `idents`, fixed reads this.
        self.idents_code = set(RE_IDENT.findall(RE_PREPROC.sub('', RE_DIRECTIVE.sub('', t))))
        enums = [x for x in self.types if x['kind'] == 'enum']
        self.enums = {x['name']: enum_members(t[x['start'] + 1:x['end']]) for x in enums}
        self.generated = {generated_name(n) for n in RE_SERFIELD.findall(t)}
        # Every *use* of a name -> the qualifiers it is written with, None for an unqualified use.
        # Enum bodies are blanked first, because a member's declaration is not a use of it, and
        # using/namespace lines are dropped, because `using X.SkillMasteries;` is not one either.
        # ServUO side only.
        self.quals = None
        if quals:
            q_text = t
            for x in enums:
                q_text = q_text[:x['start'] + 1] + ' ' * (x['end'] - x['start'] - 1) + q_text[x['end']:]
            q_text = RE_PREPROC.sub('', RE_DIRECTIVE.sub('', q_text))
            self.quals = defaultdict(set)
            for m in RE_IDENT.finditer(q_text):
                q = RE_QUALIFIER.search(q_text, max(0, m.start() - 80), m.start())
                self.quals[m.group()].add(q.group(1) if q else None)
        stem = os.path.basename(rel)[:-3]
        names = [x['name'] for x in self.types]
        self.primary = stem if stem in names else (names[0] if names else None)
        self.graphics = {}
        for x in self.types:
            g = RE_GRAPHIC.search(t, x['start'], x['end'])
            # A decimal above the art range is a cliloc (`base(1094954)`), not a graphic.
            if g and (g.group(1).startswith('0x') or int(g.group(1)) <= 0xFFFF):
                self.graphics[x['name']] = int(g.group(1), 0)


def load(root, quals=False):
    files = {}
    for p in walk(root):
        with open(p, encoding='utf-8', errors='ignore') as fh:
            rel = os.path.relpath(p, root).replace('\\', '/')
            files[rel] = FileInfo(rel, fh.read(), quals)
    return files


class Tree:
    """Declarations and identifiers of pinned + ours, the side a name must resolve against."""

    def __init__(self, files_list, use_aliases, use_generated=False, use_code_idents=False):
        self.types, self.idents, self.alias_only, self.graphic = set(), set(), {}, defaultdict(set)
        self.generated_only = {}
        declared = set()
        for files in files_list:
            for f in files.values():
                for x in f.types:
                    declared.add(x['name'])
                for n, g in f.graphics.items():
                    self.graphic[g].add(n)
                self.idents |= f.idents_code if use_code_idents else f.idents
        self.types = set(declared)
        if use_aliases:
            for files in files_list:
                for f in files.values():
                    for a in f.aliases:
                        if a not in declared:
                            self.alias_only.setdefault(a, f.rel)
            self.types |= set(self.alias_only)
            self.idents |= set(self.alias_only)
        if use_generated:
            # Fix 4: a generated property is a member, so it resolves a name but declares no type.
            for files in files_list:
                for f in files.values():
                    for g in f.generated:
                        if g not in self.idents:
                            self.generated_only.setdefault(g, f.rel)
            self.idents |= set(self.generated_only)


class Index:
    def __init__(self, ours=C, legacy=False, _cache={}):
        self.legacy = legacy
        key = ('S',)
        if key not in _cache:
            _cache[key] = load(S, quals=True)
            _cache[('SRV',)] = load(os.path.join(SERVUO, 'Server'))
        if ('M',) not in _cache:
            _cache[('M',)] = load(M)
        if ('C', ours) not in _cache:
            _cache[('C', ours)] = load(ours)
        self.sv, self.muo, self.ours = _cache[('S',)], _cache[('M',)], _cache[('C', ours)]
        self.sv_core = _cache[('SRV',)]
        self.tree = Tree([self.muo, self.ours], use_aliases=not legacy, use_generated=not legacy,
                         use_code_idents=not legacy)

        # ServUO ownership: which files declare a name as a type, which as a member.
        self.type_owner, self.member_owner = defaultdict(set), defaultdict(set)
        self.enum_owner = defaultdict(set)   # (enum, member) -> ServUO Scripts files declaring it
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
                    for e, ms in f.enums.items():
                        for n in ms:
                            self.enum_owner[(e, n)].add(f.rel)

        # Step 1: a file is discarded when pinned or ours declares (fixed: or aliases) its primary type.
        self.discarded, self.discard_reason = set(), {}
        for rel, f in self.sv.items():
            if f.primary and f.primary in self.tree.types:
                self.discarded.add(rel)
                self.discard_reason[rel] = 'aliased' if f.primary in self.tree.alias_only else 'declared'

    # ---- step 2 ------------------------------------------------------------------------------
    def missing(self, f):
        own = {x['name'] for x in f.types} | f.members
        if not self.legacy:
            # Fix 3: the file's own enum members, under the same qualifier rule as everyone else's.
            # One whose every use is qualified by the file's own enum (or that is never used outside
            # the enum) is the file's own. One also used another way, as `typeof(Cannonball)` beside
            # `AmmunitionType.Cannonball`, goes on to resolve_name with the file itself excluded.
            for ms in f.enums.values():
                for n in ms:
                    if n not in f.quals or f.quals[n] <= set(f.enums):
                        own.add(n)
        return sorted(n for n in (f.idents if self.legacy else f.idents_code)
                      if n not in self.tree.idents and n not in own
                      and n not in EQUIV and n not in CONVERT and n not in DELETABLE
                      and n not in BLACKLIST and not n.startswith('Internal'))

    def enum_owners(self, n, f):
        """Fix 3. (files, enums, exclusive) for the enums `f` qualifies `n` with that declare it.

        The tie-break against a type or member of the same name is the qualifier. `Alignment.Good`
        can only mean the member, so when every use of `n` in `f` is qualified by an enum that
        declares it, the enum's file is the only owner (`exclusive`). When `f` also uses `n` another
        way (bare, or behind a qualifier that is not such an enum), the type and member owners
        stay as well, because the ident set cannot say which use is the missing one.
        """
        if self.legacy or f is None or not f.quals or n not in f.quals:
            return set(), set(), False
        qs = f.quals[n]
        declaring = {q for q in qs if q and (q, n) in self.enum_owner}
        # The file's own enum is never a dependency of itself (missing() has already decided it).
        enums = {q for q in declaring if self.enum_owner[(q, n)] - {f.rel}}
        files = set().union(*(self.enum_owner[(q, n)] for q in enums)) - {f.rel} if enums else set()
        return files, enums, bool(files) and not (qs - declaring)

    def resolve_name(self, n, row_cands, f=None):
        efiles, enums, exclusive = self.enum_owners(n, f)
        if exclusive:
            owners, members = set(efiles), set()
        else:
            owners = self.type_owner.get(n, set()) | self.member_owner.get(n, set()) | efiles
            members = self.member_owner.get(n, set())
        if owners & row_cands:
            return 'in-row', None
        outside = sorted(o for o in owners if o not in self.discarded and o not in row_cands)
        if outside:
            return 'elsewhere', outside[0]
        if owners:
            if self.legacy or members:
                return 'upstream', None
            # Every owner is discarded. A member of an enum pinned or ours ships is a patch to that
            # enum (or a rename); a member of an enum only the discarded file has comes with the extract.
            if efiles and (exclusive or not self.type_owner.get(n)):
                if any(e in self.tree.types for e in enums):
                    return 'upstream', None
                return 'extract', sorted(efiles)[0]
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
                kind, owner = self.resolve_name(n, cands, self.sv[r])
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
                # The check reads only a literal first argument of `: base(...)`. `not run` is not `none found`.
                check = 'not run' if g is None else ('twin' if same else 'none found')
                rows.append({'file': rel, 'primary': f.primary, 'type': n, 'class': cls,
                             'graphic': hex(g) if g is not None else None, 'pinned_same_graphic': same,
                             'graphic_check': check})
        return rows


# ---- reach: what names each of our types, and is the namer itself reached -----------------------
# The rest of this file answers "what does a ServUO file need". This answers the reverse, for our
# tree: "what, other than itself, puts this type in the world". notes/reachability-audit.md.
#
# A name is not a reach. `item is BestialArms` checks, `class X : BestialArms` inherits, a comment
# mentions; none of them creates one. Only these do, and only from a context that is itself reached:
#   new     `new X(`                                   construction
#   typeof  `typeof(X)`, with the call it sits in       craft (`AddCraft`), vendor (`GenericBuyInfo`),
#                                                       loot and reward lists, spawner code
#   string  "X" in code, or ".X" at the end of one      FindTypeByName, TypeAlias
#   spawn   an entry name in Distribution/Data/Spawns   BaseSpawner resolves it case-insensitively
#   data    a word in any other Data file                MLQuests.cfg, Decoration, containers ...
# Roots, reached by definition: pinned code with server/patches applied as the build applies them (cc-P27; for
# names pinned does not declare itself), the spawn and data files, and any of our types with a static Configure
# or Initialize (invoked by name for every type, pinned Server/Main.cs:441,448) or in one of the five replacement files.
# A reached type also reaches its own base classes in our tree, whose code it runs.
PINNED_DATA = r'D:\UO\ModernUO-pinned\Distribution\Data'
# The build's own list of what it does to pinned, relative to the shard repo root (cc-P27).
APPLY_PATCHES = os.path.join('docker', 'uo', 'apply-patches.sh')
SERVUO_SPAWN_DIRS = ('Spawns', 'RevampedSpawns')
# `typeof` sites that read a type rather than create one, read at a use 2026-09-29 (FindItemByType on its
# name alone): imbuing
# property and ingredient tables, the slayer and Shadowguard protection tables, craft's markable/colour
# tables, a craft recipe's consumed resources, `if (x.GetType() == typeof(X))`, and backpack lookups
# (`GetAmount`, `ConsumeTotal`, `FindItemByType`, `Find`, our satchels' `_acceptedTypes`). Both sides.
READER_SITES = {'ItemPropertyInfo', '_SpecialImbuable', 'm_IngredTypes', 'IngredTypes', 'SlayerEntry', 'SetProtection',
                'm_MarkableTable', 'm_ColoredItemTable', 'm_NeverColorTable', 'AddRes', 'if', 'GetAmount',
                'ConsumeTotal', 'FindItemByType', 'Find', '_acceptedTypes',
                # ServUO CleanUpBritanniaData.Entries[typeof(X)] = points: what a player turns IN (:47-49).
                # The rewards Clean Up hands OUT are CleanUpBritanniaRewards, a different table.
                'Entries'}
SERVUO_READER_SITES = READER_SITES
REPLACEMENTS = {'CharacterCreation', 'CraftItem', 'HammerOfHephaestus', 'Meditation', 'RegenRates'}  # AGENTS.md
# Data that puts a named type in the world: spawner entries, decoration, ML quest registration
# (MLQuests.cfg, read by MLQuestSystem through FindTypeByName) and profession kits. Every other Data
# file (bodyTable.cfg, npc-speeds.json, regions.json, the [add gump's categorization.json ...) names
# types without creating one, and is recorded as `data-mention`, which does not reach.
DATA_REACH = ('Spawns/', 'Decoration/', 'MLQuests.cfg', 'Professions/')
REACHING = ('new', 'typeof', 'string', 'spawn', 'data')
# Hooks whose every command is GameMaster or above and hands things to someone (read 2026-09-29). What
# only these reach is `staff-only`. World seeders ([SetupDespise, the ClusterF seeders) are not here:
# they place content where players walk, the same as [GenerateSpawners does for the spawn data.
STAFF_ROOTS = {'ClusterFCompactAdminTools', 'ClusterFDevTools', 'DevTestingCrystal', 'ClusterFAreaScan',
               'AddCloneCommands', 'SmithCommissionCommands'}
RE_HOOK = re.compile(r'\bstatic\s+(?:\w+\s+)*void\s+(Configure|Initialize)\s*\(\s*\)')
RE_WORD = re.compile(r'[A-Za-z_]\w*')


def blank(raw, comments=None):
    """Comments and string contents to spaces, positions and newlines kept. Also the strings, and
    the comments into `comments` when a list is passed."""
    out, strings = list(raw), []
    pat = re.compile(r'//[^\n]*|/\*.*?\*/|@"(?:""|[^"])*"|\$@"(?:""|[^"])*"|\$?"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])\'', re.S)
    for m in pat.finditer(raw):
        s, e, tok = m.start(), m.end(), m.group()
        if tok.startswith('"') or tok.startswith(('@"', '$"', '$@"')):
            q = tok.index('"')
            strings.append((s, tok[q + 1:-1]))
            s, e = s + q + 1, e - 1
        elif comments is not None:
            comments.append((s, tok))
        for k in range(s, e):
            if out[k] != '\n':
                out[k] = ' '
    return ''.join(out), strings


def ref_kind(code, s, e):
    """How the name at code[s:e] is used, and for typeof the call or list it sits in."""
    before = code[max(0, s - 200):s]
    # `Server.Items.X` is X written qualified: step over the qualifier.
    before = re.sub(r'(?:global::)?(?:[A-Za-z_]\w*\s*\.\s*)+$', '', before) if re.search(r'\.\s*$', before) else before
    after = code[e:e + 40]
    if re.search(r'\bnew\s*$', before):
        return ('other', 'array') if re.match(r'\s*\[', after) else ('new', None)
    if re.search(r'\btypeof\s*\(\s*$', before):
        site = typeof_site(code, s)
        if site == 'AddCraft' and not first_typeof_in_call(code, s):
            # AddCraft(typeof(Product), group, name, min, max, typeof(FirstResource), ...): only the first typeof is
            # what the entry makes. Every later one is a resource it consumes, a read like AddRes
            # (craft-registrations 4.1.1, cc-P27). Before, ServUO's tinkering read as a source of CrystalShards.
            return 'check', 'AddCraft'
        return 'typeof', site
    if re.search(r'\b(?:class|struct|record|interface)\s+\w+(?:\s*<[^>{;]*>)?\s*:[^{;}()]*$', before):
        return 'inherit', None
    if re.search(r'\b(?:is|as)\s*(?:not\s*)?$', before) or (re.search(r'\(\s*$', before) and re.match(r'\s*\)\s*[\w(]', after)):
        return 'check', None
    if re.search(r'<\s*$', before) or re.search(r'<[\w\s,.]*,\s*$', before):
        m = re.search(r'(\w+)\s*<[\w\s,.]*$', before)
        return 'generic', m.group(1) if m else None
    if re.match(r'\s*\.\s*[A-Za-z_]', after):
        # `ShameSpawns.Definitions`: runs the type's static code, creates no instance of it.
        return 'static', None
    return 'other', None


def enclosing_open(code, s):
    """Index of the nearest unclosed ( { or [ before the typeof whose type name starts at s, or None."""
    depth, i = 0, code.rfind('(', 0, s)  # typeof's own paren
    i -= 1
    while i >= 0 and s - i < 4000:
        c = code[i]
        if c in ')}]':
            depth += 1
        elif c in '({[':
            if depth == 0:
                return i
            depth -= 1
        elif c == ';' and depth == 0:
            return None
        i -= 1
    return None


def typeof_site(code, s):
    """For a typeof: the identifier that owns the nearest unclosed ( or { before it (`AddCraft`,
    `GenericBuyInfo`, a field name for an array initializer)."""
    i = enclosing_open(code, s)
    if i is None:
        return None
    m = re.search(r'([A-Za-z_]\w*)\s*(?:\[\s*\])?\s*(?:=\s*(?:new\s*[\w.]*\s*\[\s*\]\s*)?)?$', code[max(0, i - 120):i])
    return m.group(1) if m else code[i]


def first_typeof_in_call(code, s):
    """Whether the typeof at s is the first typeof among its call's own arguments (none earlier at depth 0)."""
    i = enclosing_open(code, s)
    own = code.rfind('typeof', 0, s)
    depth = 0
    for m in re.finditer(r'[(){}\[\]]|\btypeof\b', code[i + 1:own]):
        t = m.group()
        if t in '({[':
            depth += 1
        elif t in ')}]':
            depth -= 1
        elif depth == 0:
            return False
    return True


def apply_steps(script_text):
    """apply-patches.sh's steps on pinned, in its order: ('patch', name) for `apply_patch "$PATCHES/name"`, and
    ('replace', 'PATCHES' or 'CUSTOMIZATIONS', name, dest) for `replace_file "$ROOT/name" "dest"`. Its additive copies
    are not steps on pinned: those files are ours, read as ours."""
    text = re.sub(r'\\\n\s*', ' ', script_text.replace('\r\n', '\n'))
    steps = []
    for line in text.split('\n'):
        if line.lstrip().startswith('#'):
            continue
        m = re.match(r'\s*apply_patch\s+"\$PATCHES/([^"]+)"', line)
        if m:
            steps.append(('patch', m.group(1)))
            continue
        m = re.match(r'\s*replace_file\s+"\$(PATCHES|CUSTOMIZATIONS)/([^"]+)"\s+"([^"]+)"', line)
        if m:
            steps.append(('replace',) + m.groups())
    return steps


def pinned_as_built(pinned, patches, script):
    """Every pinned file apply-patches.sh changes from server/patches, changed the way it changes it: a scratch copy,
    the server/patches replacements copied over and the .patch files applied, in its order, with its own flags (GNU
    patch, -p1, --fuzz=0). Replacements from server/customizations are left to the ours side (see below). Returns
    ({normcase pinned path: patched copy}, scratch dir). A patch that does not apply stops the tool, as it stops the
    build. The export must hold docker/uo/apply-patches.sh beside server/ (`git archive HEAD server
    docker/uo/apply-patches.sh`): without it the tool cannot know what the build applies, and says so."""
    if not os.path.isfile(script):
        raise SystemExit(f'reach: {script} not found. It lists what the build applies to pinned; export it with '
                         f'the tree (git archive HEAD server {APPLY_PATCHES.replace(os.sep, "/")}).')
    tool = shutil.which('patch')
    if not tool:
        raise SystemExit('reach: GNU patch is not on PATH (Git for Windows ships it in usr/bin).')
    repo = os.path.dirname(os.path.normpath(pinned))
    scratch = tempfile.mkdtemp(prefix='content_index_pinned_')
    staged = {}

    def stage(rel):
        if rel not in staged:
            src = os.path.join(repo, rel)
            if not os.path.isfile(src):
                shutil.rmtree(scratch, ignore_errors=True)
                raise SystemExit(f'reach: {rel} is not in pinned; apply-patches.sh would fail here too')
            dst = os.path.join(scratch, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            # LF, as the build's Linux checkout has it.
            with open(src, encoding='utf-8', errors='ignore', newline='') as a, open(dst, 'w', encoding='utf-8', newline='\n') as b:
                b.write(a.read().replace('\r\n', '\n'))
            staged[rel] = dst
        return staged[rel]

    with open(script, encoding='utf-8', errors='ignore') as fh:
        steps = apply_steps(fh.read())
    for step in steps:
        if step[0] == 'replace':
            _, root, name, dest = step
            if root == 'CUSTOMIZATIONS':
                # Ours (CraftItem, HammerOfHephaestus ...): read as ours, a root through REPLACEMENTS or as a shadow
                # of pinned's name. Copied over pinned here, its extra types (ReinforcedHammerOfHephaestus) would read
                # as pinned's and drop out of our content. The stock file it replaces stays read, as before cc-P27.
                continue
            shutil.copyfile(os.path.join(patches, name), stage(dest))
            continue
        with open(os.path.join(patches, step[1]), encoding='utf-8', errors='ignore', newline='') as fh:
            diff = fh.read().replace('\r\n', '\n')
        for m in re.finditer(r'^\+\+\+ (?:"b/([^"]+)"|b/(\S+))', diff, re.M):
            stage(m.group(1) or m.group(2))
        run = subprocess.run([tool, '-p1', '--forward', '--ignore-whitespace', '--fuzz=0', '--batch', '-d', scratch],
                             input=diff.encode('utf-8'), capture_output=True)
        if run.returncode:
            shutil.rmtree(scratch, ignore_errors=True)
            raise SystemExit(f'reach: {step[1]} does not apply to pinned:\n{run.stdout.decode(errors="ignore")}')
    return {os.path.normcase(os.path.normpath(os.path.join(repo, rel))): p for rel, p in staged.items()}, scratch


class Reach:
    """Every reference to one of our types, and the closure from the roots."""

    def __init__(self, ours=C, patches=None, pinned=M, data=PINNED_DATA, script=None):
        self.ours_root = ours
        patches = patches or os.path.join(os.path.dirname(os.path.normpath(ours)), 'patches')
        script = script or os.path.join(os.path.dirname(os.path.dirname(os.path.normpath(ours))), APPLY_PATCHES)
        # Pinned as the build compiles it (cc-P27): every file server/patches touches is read from a scratch copy
        # with apply-patches.sh's own steps applied, so an uncomment patch's context lines are code.
        built, scratch = pinned_as_built(pinned, patches, script)
        try:
            self._index(ours, pinned, data, built)
        finally:
            shutil.rmtree(scratch, ignore_errors=True)

    def _index(self, ours, pinned, data, built):
        self.types = {}          # name -> {file, line, kind, base, abstract, nested}
        self.dupes = defaultdict(list)
        self.refs = []           # (target, kind, site, context, file, line)
        self.hooks, self.pinned_names, self.shadow = set(), set(), {}
        ours_files = {}
        for p in walk(ours):
            rel = os.path.relpath(p, ours).replace('\\', '/')
            with open(p, encoding='utf-8', errors='ignore') as fh:
                ours_files[rel] = fh.read()
        self.parents = {}
        for p in walk(pinned):
            with open(built.get(os.path.normcase(os.path.normpath(p)), p), encoding='utf-8', errors='ignore') as fh:
                code, _ = blank(fh.read())
            for x in type_spans(code):
                self.pinned_names.add(x['name'])
                if x['base']:
                    self.parents.setdefault(x['name'], x['base'])
        spans = {}
        for rel, raw in ours_files.items():
            code, strings = blank(raw)
            ts = type_spans(code)
            spans[rel] = (code, strings, ts)
            for x in ts:
                if x['base']:
                    self.parents[x['name']] = x['base']
                if x['nested']:
                    continue
                head = code[code.rfind('\n', 0, x['start']) + 1:x['start']]
                decl = re.search(r'\b(class|struct|interface|enum|record)\s+' + x['name'] + r'\b[^{]*$', code[:x['start']])
                line_start = code.rfind('\n', 0, decl.start()) + 1 if decl else 0
                abstract = bool(decl) and 'abstract' in code[line_start:decl.start()]
                if x['name'] in self.pinned_names:
                    # Not our content: a partial of a pinned type, one of the five replacements, or a clash.
                    # Its code runs as pinned's type, so it is a root.
                    partial = bool(decl) and 'partial' in code[line_start:decl.start()]
                    self.shadow[x['name']] = ('partial' if partial else 'replacement'
                                              if os.path.basename(rel)[:-3] in REPLACEMENTS else 'same name', rel)
                    self.hooks.add(x['name'])
                    continue
                rec = {'file': rel, 'line': code.count('\n', 0, decl.start() if decl else x['start']) + 1,
                       'kind': x['kind'], 'base': x['base'], 'abstract': abstract,
                       # An item in its own right: someone can construct it by its own name.
                       'constructible': bool(re.search(r'\[\s*Constructible\b', code[x['start']:x['end']]))}
                if x['name'] in self.types:
                    self.dupes[x['name']].append(rel)
                else:
                    self.types[x['name']] = rec
                if RE_HOOK.search(code, x['start'], x['end']):
                    self.hooks.add(x['name'])
                if os.path.basename(rel)[:-3] in REPLACEMENTS:
                    self.hooks.add(x['name'])
        self.pinned_lower = {n.lower() for n in self.pinned_names}
        self.lower = defaultdict(set)
        for n in self.types:
            self.lower[n.lower()].add(n)
        # Our [TypeAlias("Server.Mobiles.Old")] makes "Old" resolve to the aliased type too.
        self.alias = {}
        for rel, (code, strings, ts) in spans.items():
            for m in re.finditer(r'\[\s*TypeAlias\s*\(', code):
                owner = self.outer(ts, m.start()) or self.next_type(ts, m.start())
                for s, v in strings:
                    if m.start() < s < code.find(')', m.end()) + 1 and owner:
                        self.alias[v.split('.')[-1].lower()] = owner
        # References from our tree, then pinned with server/patches applied. Before cc-P27 a patch's
        # added lines were read as a root of their own and pinned was read unpatched, so the lines an uncomment patch
        # makes live (context lines, the comment markers being all that changes) still read as a comment (cc-P7 2.7).
        for rel, (code, strings, ts) in spans.items():
            self.scan(code, strings, ts, rel, lambda pos, ts=ts: self.outer(ts, pos) or self.next_type(ts, pos) or 'file:' + rel)
        for p in walk(pinned):
            rel = 'pinned/' + os.path.relpath(p, pinned).replace('\\', '/')
            comments = []
            with open(built.get(os.path.normcase(os.path.normpath(p)), p), encoding='utf-8', errors='ignore') as fh:
                code, strings = blank(fh.read(), comments)
            self.scan(code, strings, None, rel, lambda pos: 'root:pinned', pinned_side=True)
            # Pinned code left commented out, `// TODO: uncomment once added` over `new GreymistChest()`:
            # not a reach, but a hook pinned already wrote and is waiting on the type for.
            for pos, text in comments:
                for m in RE_WORD.finditer(text):
                    if m.group() in self.types:
                        kind, _ = ref_kind(text, m.start(), m.end())
                        self.refs.append((m.group(), 'pinned-comment:' + kind, None, 'root:pinned', rel,
                                          code.count('\n', 0, pos) + text.count('\n', 0, m.start()) + 1))
        self.scan_data(data)
        self.close()

    @staticmethod
    def outer(ts, pos):
        for x in ts:
            if not x['nested'] and x['start'] <= pos <= x['end']:
                return x['name']
        return None

    @staticmethod
    def next_type(ts, pos):
        after = [x for x in ts if not x['nested'] and x['start'] > pos]
        return min(after, key=lambda x: x['start'])['name'] if after else None

    def scan(self, code, strings, ts, rel, ctx_of, pinned_side=False):
        for m in RE_WORD.finditer(code):
            n = m.group()
            if n not in self.types:
                continue
            # Pinned naming a name it declares itself means its own type, not ours (twin sweep reports it).
            if pinned_side and n in self.pinned_names:
                continue
            ctx = ctx_of(m.start())
            if ctx == n:
                continue
            kind, site = ref_kind(code, m.start(), m.end())
            if kind == 'typeof' and site in READER_SITES:
                kind = 'check'
            # A name in a type's own declaration line is not a use (`class X`, `enum X`).
            if re.search(r'\b(?:class|struct|interface|enum|record)\s+$', code[max(0, m.start() - 12):m.start()]):
                continue
            self.refs.append((n, kind, site, ctx, rel, code.count('\n', 0, m.start()) + 1))
        for s, v in strings:
            last = v.split('.')[-1].strip()
            for n in self.lower.get(last.lower(), ()) if re.fullmatch(r'[\w.]+', v or '-') else ():
                if pinned_side and n in self.pinned_names:
                    continue
                ctx = ctx_of(s)
                if ctx != n:
                    # A pinned string naming one of ours is an alias or a word ("Fur"), not a lookup of our type.
                    kind = 'string-pinned' if pinned_side else 'string'
                    self.refs.append((n, kind, None, ctx, rel, code.count('\n', 0, s) + 1))

    def scan_data(self, data):
        for d, _, fs in os.walk(data):
            for f in fs:
                p = os.path.join(d, f)
                rel = 'data/' + os.path.relpath(p, data).replace('\\', '/')
                with open(p, encoding='utf-8', errors='ignore') as fh:
                    text = fh.read()
                if rel.startswith('data/Spawns/') and f.endswith('.json'):
                    for n, line in spawn_entry_names(text):
                        for t in self.resolve_ci(n):
                            self.refs.append((t, 'spawn', None, 'root:' + rel, rel, line))
                    continue
                kind = 'data' if rel[5:].startswith(DATA_REACH) else 'data-mention'
                for i, line in enumerate(text.split('\n'), 1):
                    if line.lstrip().startswith('#'):
                        continue
                    words = set(RE_WORD.findall(line))
                    if kind == 'data' and '/Decoration/' in rel:
                        # `Type (props)` heads a block; the rest are coordinates. Only the type places anything.
                        words = set(RE_WORD.findall(line)[:1])
                    for w in words:
                        for t in self.resolve_ci(w):
                            self.refs.append((t, kind, None, 'root:' + rel, rel, i))

    def resolve_ci(self, n):
        """AssemblyHandler.FindTypeByName: case-insensitive, and alias strings count (Q-048). A name
        pinned also declares, in any case, is pinned's here; the twin sweep reports the clash."""
        if n.lower() in self.pinned_lower:
            return set()
        out = set(self.lower.get(n.lower(), ()))
        if n.lower() in self.alias:
            out.add(self.alias[n.lower()])
        return out

    def close(self):
        self.by_target = defaultdict(list)
        out = defaultdict(list)
        for r in self.refs:
            self.by_target[r[0]].append(r)
            if r[1] in REACHING or r[1] == 'static':
                out[r[3]].append(r)
        self.out = out
        self.roots = {r[3] for r in self.refs if r[3].startswith('root:')} | self.hooks
        # Player reach leaves out the staff hand-out commands; staff reach is everything.
        self.reached, self.live = self._closure(out, self.roots - STAFF_ROOTS)
        self.reached_staff, _ = self._closure(out, self.roots)

    def _closure(self, out, roots):
        """(created, live). `live`: types whose code runs, each with the edge that first made it so.
        `created`: types an instance of which is made by live code (new, typeof, string, spawn, data),
        or roots. A static access (`ShameSpawns.Definitions`) makes code live and creates nothing."""
        # A context acts (its references count) once it can run: a root; a created type; a base of an
        # acting type, whose code runs as part of it; or a live helper that is not itself an item or a
        # mobile. An item or mobile only reached statically (`FountainOfFortune.UnderProtection`) does
        # not act: its instance code, `new GemologistsSatchel()` in the fountain's reward, never runs.
        live = {c: None for c in roots}
        created = {c: None for c in roots}
        acting, frontier = set(roots), sorted(roots)
        while frontier:
            nxt = []
            for c in frontier:
                steps = list(out.get(c, ()))
                b = self.parents.get(c)
                seen = set()
                while b in self.types and b not in seen:
                    seen.add(b)
                    steps.append((b, 'base', None, c, self.types[c]['file'] if c in self.types else '', 0))
                    b = self.parents.get(b)
                for r in steps:
                    t = r[0]
                    live.setdefault(t, r)
                    if r[1] in REACHING:
                        created.setdefault(t, r)
                    if t not in acting and (r[1] in REACHING or r[1] == 'base' or not self.is_content(t)):
                        acting.add(t)
                        nxt.append(t)
            frontier = nxt
        # A base class of a created type exists in the world as that type (`ShameGuardian` as its three
        # guardians), so it is not an orphan even when nothing constructs it by its own name. Unless it is
        # an item in its own right: `AloronsBustier` existing does not put a `TigerPeltBustier` in anyone's hands.
        for c in list(created):
            b, seen = self.parents.get(c), set()
            while b in self.types and b not in seen:
                seen.add(b)
                if not self.types[b]['constructible']:
                    created.setdefault(b, (b, 'base', None, c, self.types[c]['file'] if c in self.types else '', 0))
                b = self.parents.get(b)
        return created, live

    def what_if(self, extra):
        """Created set if `extra` types were also created by something outside the tree (a gate)."""
        created, _ = self._closure(self.out, (self.roots - STAFF_ROOTS) | set(extra))
        return created

    def is_content(self, n):
        """Something a player can hold or meet: an item or a mobile of ours."""
        return n in self.types and self.types[n]['kind'] == 'class' and self.category(n) in ('item', 'creature', 'mobile')

    def standing(self, name):
        """Where a type named in ServUO stands in our world."""
        if name in self.types:
            return 'ours' if name in self.reached else 'ours-unreached'
        if name in self.pinned_names or name in self.shadow:
            return 'pinned'
        return 'absent'

    def chain(self, n):
        seen, out = set(), []
        while n in self.parents and n not in seen:
            seen.add(n)
            n = self.parents[n]
            out.append(n)
        return out

    def category(self, n):
        ch = self.chain(n)
        for base, label in (('BaseCreature', 'creature'), ('Mobile', 'mobile'), ('Item', 'item'), ('Gump', 'gump'),
                            ('BaseGump', 'gump'), ('Timer', 'timer'), ('Target', 'target'), ('MLQuest', 'quest'),
                            ('ContextMenuEntry', 'support'), ('Spell', 'spell'), ('Region', 'region')):
            if base in ch:
                return label
        return 'other'

    def path(self, n, limit=12):
        """The creating edge, then the edges that made each context's code live, back to a root."""
        out, d = [], self.reached
        while n in d and d[n] is not None and len(out) < limit:
            r = d[n]
            out.append(r)
            n, d = r[3], self.live
        return out, n

    def report(self):
        """Per type: reached or not, how, and for the unreached every naming reference."""
        rows = {}
        for n, t in self.types.items():
            refs = [r for r in self.by_target.get(n, ()) if r[3] != n]
            rows[n] = {'type': n, 'file': t['file'], 'line': t['line'], 'kind': t['kind'], 'abstract': t['abstract'],
                       'category': self.category(n) if t['kind'] == 'class' else t['kind'],
                       'reached': n in self.reached, 'refs': refs}
        return rows


RE_LABEL = re.compile(r'\bLabelNumber\s*(?:=>\s*|\{\s*get\s*(?:=>\s*|\{\s*return\s+))(\d{6,7})\b')


def type_facts(root):
    """name -> (file, graphic, cliloc) for every non-nested class under root. Graphic is the literal first
    `: base(...)` argument (hex, or decimal in art range); cliloc is a literal LabelNumber override."""
    out = {}
    for p in walk(root):
        rel = os.path.relpath(p, root).replace('\\', '/')
        with open(p, encoding='utf-8', errors='ignore') as fh:
            code, _ = blank(fh.read())
        for x in type_spans(code):
            if x['nested'] or x['kind'] != 'class':
                continue
            g = RE_GRAPHIC.search(code, x['start'], x['end'])
            gv = int(g.group(1), 0) if g and (g.group(1).startswith('0x') or int(g.group(1)) <= 0xFFFF) else None
            lab = RE_LABEL.search(code, x['start'], x['end'])
            out.setdefault(x['name'], (rel, gv, int(lab.group(1)) if lab else None))
    return out


def twins(reach, ours=C, pinned=M):
    """Our types that may be pinned types under another spelling. Three independent tests, each reported:
    `case` a pinned type with the same name in another case (AssemblyHandler resolves case-insensitively,
    AssemblyHandler.cs:189), `alias` a pinned [TypeAlias] string naming it, `art+cliloc` a pinned class
    with the same literal graphic and the same literal LabelNumber. For judgment, never for deletion."""
    o, p = type_facts(ours), type_facts(pinned)
    plower = defaultdict(list)
    for n in p:
        plower[n.lower()].append(n)
    by_art, by_label = defaultdict(list), defaultdict(list)
    for n, (f, g, lab) in p.items():
        if g is not None and lab is not None:
            by_art[(g, lab)].append(n)
        if lab is not None:
            by_label[lab].append(n)
    palias = {}
    for q in walk(pinned):
        with open(q, encoding='utf-8', errors='ignore') as fh:
            raw = fh.read()
        for a in RE_ALIAS.findall(RE_LINE_COMMENT.sub('', raw)):
            for s in re.findall(r'"([^"]+)"', a):
                palias.setdefault(s.split('.')[-1].lower(), os.path.relpath(q, pinned).replace('\\', '/'))
    hits = []
    for n, (f, g, lab) in sorted(o.items()):
        if n not in reach.types:
            continue   # a partial or replacement of a pinned type: not ours to twin
        for m in plower.get(n.lower(), ()):
            if m != n:
                hits.append((n, f, 'case', m, p[m][0]))
        if n.lower() in palias:
            hits.append((n, f, 'alias', n, palias[n.lower()]))
        for m in by_art.get((g, lab), ()) if g is not None and lab is not None else ():
            hits.append((n, f, 'art+cliloc', m, p[m][0] + f' (0x{g:X}, {lab})'))
        if lab is not None and not by_art.get((g, lab)):
            # Weaker: the same cliloc alone. A named item's cliloc is close to unique, so this is how a
            # MysticBook/MysticSpellbook shape shows up when the art is inherited or set another way.
            for m in by_label.get(lab, ()):
                hits.append((n, f, 'cliloc', m, p[m][0] + f' ({lab}; art ours {hex(g) if g is not None else "?"}, '
                                                        f'pinned {hex(p[m][1]) if p[m][1] is not None else "?"})'))
    return hits


def servuo_sources(reach, names, servuo=SERVUO):
    """For each of `names`, every ServUO reference that would put it in the world there: code that
    constructs or lists it, and ServUO's own spawn and data files. Each code source carries where its
    enclosing type stands for us: `pinned` (pinned has it, so the fix is a hook or a patch into pinned's
    version), `ours` or `ours-unreached`, or `absent` (it would have to be ported first)."""
    names = set(names)
    lower = {n.lower(): n for n in names}
    out = defaultdict(list)
    for p in walk(os.path.join(servuo, 'Scripts')):
        rel = os.path.relpath(p, os.path.join(servuo, 'Scripts')).replace('\\', '/')
        with open(p, encoding='utf-8', errors='ignore') as fh:
            code, strings = blank(fh.read())
        ts = None
        for m in RE_WORD.finditer(code):
            n = m.group()
            if n not in names:
                continue
            ts = ts if ts is not None else type_spans(code)
            ctx = Reach.outer(ts, m.start()) or Reach.next_type(ts, m.start()) or 'file:' + rel
            if ctx == n or re.search(r'\b(?:class|struct|interface|enum|record)\s+$', code[max(0, m.start() - 12):m.start()]):
                continue
            kind, site = ref_kind(code, m.start(), m.end())
            if kind == 'typeof' and site in SERVUO_READER_SITES:
                continue
            if kind in ('new', 'typeof'):
                out[n].append((kind, site, ctx, reach.standing(ctx), 'Scripts/' + rel, code.count('\n', 0, m.start()) + 1))
    for d in SERVUO_SPAWN_DIRS:
        root = os.path.join(servuo, d)
        for p in walk_any(root, ('.xml',)):
            rel = d + '/' + os.path.relpath(p, root).replace('\\', '/')
            with open(p, encoding='utf-8', errors='ignore') as fh:
                for i, line in enumerate(fh, 1):
                    # XmlSpawner: <Objects2>Silenii,{RND,1,5}:MX=2:...:OBJ=ForestNymph,...</Objects2>. Each entry's
                    # leading word is the type; the rest is spawner options and property settings.
                    m = re.search(r'<Objects2>(.*)</Objects2>', line)
                    for entry in m.group(1).split(':OBJ=') if m else ():
                        w = re.match(r'\s*([A-Za-z_]\w*)', entry)
                        if w and w.group(1).lower() in lower:
                            out[lower[w.group(1).lower()]].append(('spawn', None, 'root', 'data', rel, i))
    return out


def walk_any(root, exts):
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(exts):
                yield os.path.join(d, f)


def spawn_entry_names(text):
    """(entry name, line) for every spawner entry in one Spawns JSON file, one per occurrence."""
    try:
        objs = json.loads(text.lstrip('\ufeff'))
    except ValueError:
        return []
    names = {(e.get('name') or '').strip() for o in (objs if isinstance(objs, list) else [])
             for e in (o.get('entries') or ())}
    out = []
    for i, l in enumerate(text.split('\n'), 1):
        for m in re.finditer(r'"name"\s*:\s*"([^"]+)"', l):
            if m.group(1).strip() in names:
                out.append((m.group(1).split()[0], i))
    return out


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
    checks = defaultdict(int)
    for x in by['item']:
        checks[x['graphic_check']] += 1
    print(f'same-graphic check on the {len(by["item"])} item types: twin {checks["twin"]} . '
          f'none found {checks["none found"]} . not run {checks["not run"]}')
    print('  It reads only an integer literal as the first argument of `: base(...)`, hex or decimal, on both sides.')
    print('  "none found" means not found BY THIS CHECK, not that no twin exists. "not run" means the graphic is set')
    print('  another way (a later argument, a cast, inherited from a base class) and nothing was compared at all.')
    for k in order:
        print(f'\n## {k} ({len(by[k])})')
        for x in by[k]:
            if x['graphic_check'] == 'twin':
                same = f'  [pinned or ours has same graphic {x["graphic"]}: {", ".join(x["pinned_same_graphic"])}]'
            elif k != 'item':
                same = ''
            elif x['graphic_check'] == 'none found':
                same = f'  [graphic {x["graphic"]}: no same-graphic type found by the base() literal check]'
            else:
                same = '  [graphic not read: same-graphic check not run]'
            print(f'  {x["file"]} | primary {x["primary"]} | {x["type"]}{same}')
    return rows


def reach_files(r, rows):
    """file -> (status, content types). Content: a concrete item or mobile. A file is `reached` when
    every content type in it is, `partial` when some are, `staff-only` when only a staff hand-out
    command makes one, `unreached` otherwise. Ported content lives in a subdirectory (AGENTS.md)."""
    by = defaultdict(list)
    for n, v in rows.items():
        if r.is_content(n) and not v['abstract']:
            by[v['file']].append(n)
    out = {}
    for f, ns in by.items():
        k = sum(n in r.reached for n in ns)
        st = ('reached' if k == len(ns) else 'partial' if k else
              'staff-only' if any(n in r.reached_staff for n in ns) else 'unreached')
        out[f] = (st, sorted(ns))
    return out


def print_reach(r, sources=False, show_twins=False):
    rows = r.report()
    files = reach_files(r, rows)
    content = {n for fs in files.values() for n in fs[1]}
    un = sorted(n for n in content if n not in r.reached)
    print('# reach: what puts each of our types in a player\'s world (notes/reachability-audit.md)')
    print(f'types {len(rows)}; content (concrete item or mobile) {len(content)}: reached {len(content) - len(un)}, '
          f'unreached {len(un)} (staff-only {sum(n in r.reached_staff for n in un)})')
    for label, keep in (('content files', lambda f: True), ('ported (subdirectory) content files', lambda f: '/' in f)):
        c = defaultdict(int)
        for f, (st, _) in files.items():
            if keep(f):
                c[st] += 1
        print(f'{label} {sum(c.values())}: ' + ', '.join(f'{k} {c[k]}' for k in ('reached', 'partial', 'unreached', 'staff-only')))
    print('\n## reached content by the root that reaches it (a type can have several)')
    fam = defaultdict(set)
    for root in r.roots - STAFF_ROOTS:
        fam[root].add(root)
    counts = []
    for root, rs in fam.items():
        created, _ = r._closure(r.out, rs)
        k = sum(1 for n in content if n in created)
        if k:
            counts.append((k, root))
    for k, root in sorted(counts, reverse=True):
        print(f'  {k:4}  {root}')
    print(f'\n## unreached content, by file ({sum(1 for s, _ in files.values() if s != "reached")} files)')
    for f in sorted(files):
        st, ns = files[f]
        if st == 'reached':
            continue
        print(f'  {f}  [{st}]')
        for n in ns:
            if n in r.reached:
                continue
            refs = [x for x in rows[n]['refs'] if not x[1].startswith('data-mention')]
            print(f'    {n}' + ('' if refs else '  (named by nothing)'))
            for x in refs[:6]:
                live = 'live' if x[3] in r.live else 'not live'
                print(f'      {x[1]:<22} by {x[3]} ({live})  {x[4]}:{x[5]}')
            if len(refs) > 6:
                print(f'      ... {len(refs) - 6} more')
    res = {'files': files, 'unreached': un}
    if sources:
        src = servuo_sources(r, un)
        res['sources'] = src
        byfile = {f: ns for f, (st, ns) in files.items()}
        base = {f for f, (st, _) in files.items() if st == 'reached'}
        groups = defaultdict(set)
        for n in un:
            for s in src.get(n, ()):
                groups[(s[4], s[3])].add(n)
            for x in r.by_target.get(n, ()):
                if x[1] in ('pinned-comment:new', 'pinned-comment:typeof'):
                    groups[(x[4] + ' (commented out)', 'pinned-comment')].add(n)
        ranked = []
        for k, ns in groups.items():
            created = r.what_if(ns)
            newf = {f for f, fns in byfile.items() if f not in base and all(n in created for n in fns)}
            ranked.append((len(newf), len(ns), k))
        print(f'\n## ServUO sources of the {len(un)} unreached types, by the files each would reach alone')
        print('  standing: pinned = pinned has that type (hook or patch into it); absent = port it first;')
        print('  ours-unreached = our copy is itself unreached (a chain); data = ServUO spawn XML only.')
        for nf, nt, (path, standing) in sorted(ranked, reverse=True):
            print(f'  {nf:4} files {nt:4} types  {standing:15} {path}')
        # Only commented-out construction counts as a source, as in the grouping above. Since cc-P27 pinned is read
        # patched, so the prose comments our patches add (BaseWeapon's naming PetMimic) are pinned comments too.
        nos = [n for n in un if not src.get(n) and not any(
            x[1] in ('pinned-comment:new', 'pinned-comment:typeof') for x in r.by_target.get(n, ()))]
        print(f'\n## no source in ServUO code, ServUO spawns, or pinned\'s commented-out code ({len(nos)})')
        for n in nos:
            print(f'  {n}  {rows[n]["file"]}')
    if show_twins:
        hits = twins(r, r.ours_root)
        res['twins'] = hits
        print(f'\n## twin sweep: {len(hits)} hits, for judgment')
        for n, f, test, m, where in hits:
            print(f'  {n} ({f})  {test}  pinned {m}  {where}  [{"reached" if n in r.reached else "unreached"}]')
    return res


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
    ap.add_argument('cmd', choices=['row', 'hidden', 'compare-s9', 'filter', 'reach'])
    ap.add_argument('row', nargs='?', default='artifacts', choices=sorted(ROWS))
    ap.add_argument('--legacy', action='store_true', help='S9 method: no alias names, no extract bucket')
    ap.add_argument('--ours', default=C, help='customizations tree (an older export reproduces an old survey)')
    ap.add_argument('--all', action='store_true', help='hidden: whole tree, not one row')
    ap.add_argument('--s9', default=os.path.join(os.path.dirname(__file__), '..', 'notes', 's9-backlog-remeasure.md'))
    ap.add_argument('--s9-title', default='Artifacts + equipment')
    ap.add_argument('--json', help='also write the result as JSON')
    ap.add_argument('--sources', action='store_true', help='reach: ServUO sources of every unreached type')
    ap.add_argument('--twins', action='store_true', help='reach: pinned types ours may duplicate')
    a = ap.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    if a.cmd == 'reach':
        res = print_reach(Reach(a.ours), a.sources, a.twins)
        if a.json:
            with open(a.json, 'w', encoding='utf-8') as fh:
                json.dump(res, fh, indent=1, default=list)
        return
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
