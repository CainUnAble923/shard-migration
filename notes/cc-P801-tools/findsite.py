"""cc-P801: find a flat, empty plot for the New Haven jail on either land.
    python -u -P -W ignore notes/cc-P801-tools/findsite.py sos|stock W H x0 y0 x1 y1 rookx rooky
A plot is W x H tiles plus a 1-tile margin: no statics at all, land height spread at most 2, no water or rock,
with a road or dirt tile within 4 tiles south of its south wall. Read only."""
import os, sys
DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P708-tools', 'p281sos'))
import hallbase as H
which = sys.argv[1]
if which == 'stock':
    H.CLIENT = H.uofiles.CLIENT = 'D:/UO/tool-trials/client-data-copy'
W, Hh, x0, y0, x1, y1, rx, ry = [int(a) for a in sys.argv[2:10]]
F = H.Facet(1)
BAD = ('water', 'rock', 'mountain', 'cave', 'void', 'lava', 'nodraw') + (('cobblestone', 'flagstone', 'road', 'paving') if os.environ.get('NOROAD') else ())
ROAD = ('cobblestone', 'dirt', 'flagstone', 'road', 'paving')
def clear(x, y):
    n = H.lname(F.land(x, y)[0]).lower()
    return not [q for q in F.statics(x, y) if not (H.iflags(q[0]) == 0 or 'grass' in H.iname(q[0]).lower() or 'flower' in H.iname(q[0]).lower())] and not any(b in n for b in BAD)
out = []
for x in range(x0, x1 - W):
    for y in range(y0, y1 - Hh):
        zs = []
        ok = True
        for i in range(-1, W + 1):
            for j in range(-1, Hh + 1):
                if not clear(x + i, y + j):
                    ok = False
                    break
                zs.append(F.landz(x + i, y + j))
            if not ok:
                break
        if not ok or max(zs) - min(zs) > int(os.environ.get("SPREAD","2")):
            continue
        road = 99
        for i in range(W):
            for d in range(1, 8):
                n = H.lname(F.land(x + i, y + Hh + d)[0]).lower()
                st = ' '.join(H.iname(s) for s, _ in F.statics(x + i, y + Hh + d)).lower()
                if any(r in n for r in ROAD) or any(r in st for r in ('road', 'cobble', 'paving')):
                    road = min(road, d)
                    break
        dist = max(abs(x + W // 2 - rx), abs(y + Hh // 2 - ry))
        out.append((dist, x, y, min(zs), max(zs), road))
out.sort()
print(which, 'plots', len(out))
seen = []
for o in out:
    if any(abs(o[1] - s[1]) < 8 and abs(o[2] - s[2]) < 8 for s in seen):
        continue
    seen.append(o)
    print('dist %3d plot %d,%d z %d-%d road-south %s' % o)
    if len(seen) >= 14:
        break
