"""Secondary types hidden by the S3/S9 step-1 filter.

For every ServUO file whose primary type (filename stem, else first declared type) pinned
ModernUO declares, list the other types in that file that neither pinned nor our tree
declares or aliases. Those are the types the filter threw away with the file.
"""
import os, re, sys, json

S = r'D:\UO\ServUO-pub57\Scripts'
M = r'D:\UO\ModernUO-pinned\Projects'
C = r'D:\ShatteredLegacy\server\customizations'

DECL = re.compile(r'\b(?:class|struct|interface|enum)\s+(\w+)')
ALIAS = re.compile(r'TypeAlias\s*\(([^)]*)\)')
STR = re.compile(r'"(?:\\.|[^"\\])*"')
PARENT = re.compile(r'\bclass\s+(\w+)\s*:\s*([\w.]+)')


def strip(t):
    t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
    return re.sub(r'//[^\n]*', '', t)


def read(p):
    with open(p, encoding='utf-8', errors='ignore') as fh:
        return strip(fh.read())


def walk(root):
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.cs'):
                yield os.path.join(d, f)


def index(root):
    names, al = set(), set()
    for p in walk(root):
        t = read(p)
        for a in ALIAS.findall(t):
            for s in re.findall(r'"([^"]+)"', a):
                al.add(s.split('.')[-1])
        names.update(DECL.findall(STR.sub('""', t)))
    return names, al


def main():
    Mn, Ma = index(M)
    Cn, Ca = index(C)
    known = Mn | Ma | Cn | Ca

    out, nfilt = [], 0
    parents = {}
    for p in walk(S):
        t = STR.sub('""', read(p))
        for c, b in PARENT.findall(t):
            parents.setdefault(c, (b.split('.')[-1], os.path.relpath(p, S)))
        ts = DECL.findall(t)
        if not ts:
            continue
        stem = os.path.basename(p)[:-3]
        prim = stem if stem in ts else ts[0]
        if prim in Mn:
            nfilt += 1
            sec = [x for x in dict.fromkeys(ts) if x != prim and x not in known and not x.startswith('Internal')]
            if sec:
                out.append((os.path.relpath(p, S), prim, sec))

    print('files filtered at step 1 (primary type pinned):', nfilt)
    print('of those, files with secondary types nobody declares or aliases:', len(out),
          ' types:', sum(len(s) for _, _, s in out))

    mode = sys.argv[1] if len(sys.argv) > 1 else 'garg'
    if mode == 'garg':
        g = [(p, pr, [x for x in s if re.match(r'(Female)?Garg', x)]) for p, pr, s in out]
        g = [x for x in g if x[2]]
        print('Gargish*/Gargoyle* among them:', sum(len(x[2]) for x in g), 'in', len(g), 'files')
        for p, pr, s in sorted(g):
            print('  ', p, '| primary', pr, '|', ', '.join(s))
    elif mode == 'items':
        it = [x for x in out if x[0].startswith('Items')]
        print('under Items/:', len(it), 'files,', sum(len(s) for _, _, s in it), 'types')
        for p, pr, s in sorted(it):
            print('  ', p, '| primary', pr, '|', ', '.join(s))
    elif mode == 'desc':
        # ServUO classes whose parent chain reaches a hidden secondary type, and whether we have them
        hidden = {x for _, _, s in out for x in s}
        rows = []
        for c, (b, f) in parents.items():
            chain, cur = [], b
            while cur in parents and cur not in hidden and len(chain) < 12:
                chain.append(cur); cur = parents[cur][0]
            if cur in hidden and c not in known:
                rows.append((f, c, cur))
        print('ServUO classes absent from both trees whose parent chain reaches a hidden type:', len(rows))
        for f, c, h in sorted(rows):
            print('  ', f, '|', c, '<-', h)


if __name__ == '__main__':
    main()
