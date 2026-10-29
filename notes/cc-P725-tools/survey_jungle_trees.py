"""cc-P725: OSI's jungle trees are several tiles each: trunk pieces along the north-east diagonal with leaf layers.
For each family's first trunk piece (0x0D41, 0x0D57, 0x0D6E, 0x0D84) on stock Trammel (Buccaneer's Den's island and
the rect given), the pieces of the 0x0D41-0x0D93 range within 4 tiles are collected as (dx, dy, dz, id) and the most
common whole compositions are written, so the isle lays each tree exactly as OSI does.
    python -P survey_jungle_trees.py <client folder> <out json> x1,y1,x2,y2"""
import collections, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
from mapbuild import uofiles as U

folder, out, r = sys.argv[1:4]
x1, y1, x2, y2 = (int(v) for v in r.split(','))
st = U.statics_in(folder, 1, x1, y1, x2, y2)
JUNGLE = set(range(0x0D41, 0x0D94))
by = collections.defaultdict(list)
for x, y, z, t in st:
    if t in JUNGLE:
        by[(x, y)].append((t, z))
rep = {}
for anchor in (0x0D41, 0x0D57, 0x0D6E, 0x0D84):
    comps = collections.Counter()
    for x, y, z, t in st:
        if t != anchor:
            continue
        comp = []
        for a in range(-4, 5):
            for b in range(-4, 5):
                for (u, zz) in by.get((x + a, y + b), []):
                    # this tree's pieces lie on its own diagonal (dx = -dy) and at its height
                    if a == -b and zz == z:
                        comp.append((a, b, zz - z, '0x%04X' % u))
        comps[tuple(sorted(comp))] += 1
    rep['0x%04X' % anchor] = [[list(map(list, c)), n] for c, n in comps.most_common(4)]
    print('0x%04X' % anchor, sum(comps.values()))
    for c, n in comps.most_common(4):
        print('   %4d %s' % (n, ' '.join('%+d%+d:%s' % (a, b, u) for a, b, dz, u in c)))
json.dump(rep, open(out, 'w'), indent=1)
