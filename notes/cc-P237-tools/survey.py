# cc-P237 read only: where things are in New Haven (farm land, crops, market stalls, the pier) by static and land name.
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nhbase as B
F = B.Facet(1)
KEYS = sys.argv[1].split(',')
x0, y0, x1, y1 = 3380, 2440, 3680, 2680
hits = collections.defaultdict(list)
for x in range(x0, x1 + 1):
    for y in range(y0, y1 + 1):
        for sid, z in F.statics(x, y):
            n = B.iname(sid).lower()
            for k in KEYS:
                if k in n: hits[k].append((x, y, z, sid))
        ln = B.lname(F.land(x, y)[0]).lower()
        for k in KEYS:
            if 'land:' + k == 'land:' + ln and k.startswith('furrow'): hits['land ' + k].append((x, y))
for k, v in hits.items():
    xs = [p[0] for p in v]; ys = [p[1] for p in v]
    # cluster by 16x16 cells
    cells = collections.Counter((p[0] // 16 * 16, p[1] // 16 * 16) for p in v)
    print(k, len(v), 'cells:', sorted(cells.items(), key=lambda c: -c[1])[:12])
