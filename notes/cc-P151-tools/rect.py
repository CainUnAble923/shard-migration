"""Check a rectangle: blocked tiles, z range, pinned spawners and signs inside (and within 3 tiles)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import uomap, survey
def check(f, x1, y1, x2, y2):
    fac = uomap.Facet(f)
    bad = 0; zs = []
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            z = survey.tile_ok(fac, x, y)
            if z is None: bad += 1
            else: zs.append(z)
    n = (x2 - x1 + 1) * (y2 - y1 + 1)
    sp = [s[:4] for s in survey.SPAWNERS[survey.MAPNAME[f]] if x1 - 3 <= s[0] <= x2 + 3 and y1 - 3 <= s[1] <= y2 + 3]
    sg = [s for s in survey.SIGNS[f] if x1 - 3 <= s[0] <= x2 + 3 and y1 - 3 <= s[1] <= y2 + 3]
    print(f"{survey.MAPNAME[f]} {x1},{y1}-{x2},{y2} ({x2-x1+1}x{y2-y1+1}): blocked {bad}/{n}, z {min(zs) if zs else None}..{max(zs) if zs else None}; spawners {sp}; signs {[s[3] for s in sg]}")
for a in sys.argv[1:]:
    f, r = a.split(":"); check(int(f), *map(int, r.split(",")))
