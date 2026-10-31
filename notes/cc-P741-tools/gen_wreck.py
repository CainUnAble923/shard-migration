"""cc-P741: the whole wreck (both halves) from OSI's own composition on Malas (1688-1712, 1630-1645, the only place
OSI lays the ShipwreckBow art: survey_wrecks.py), moved to the isle's west tip: ORIGIN on Malas lands on SPOT.
Keeps the 60 hull pieces, the driftwood (0x0C2D-0x0C30), the waves and the swirl in the break (0x1FBC, 0x1FC5,
0x3492); drops OSI's shore water (the isle's own shore is there) and the lobster buoy; keeps the morning glories
(seaweed on the sand) only where they land on the isle's land. Prints the C# table and the tiles it covers.
    python -P gen_wreck.py <map folder>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import uofiles
C = 'D:/UO/UltimaOnlineVanilla'
ORIGIN = (1700, 1637)
SPOT = (6624, 3995)
SEA = {0xA8, 0xA9, 0xAA, 0xAB}
folder = sys.argv[1]
st = [s for s in uofiles.statics_in(C, 3, 1686, 1628, 1714, 1647) if s[3] != 0x2198]
mf = uofiles.MapFile(folder, 1)
land = mf.region(SPOT[0] - 16, SPOT[1] - 10, SPOT[0] + 16, SPOT[1] + 10)
keep = []
hull_tiles = {(x, y) for (x, y, z, t) in st if 0x479A <= t <= 0x490F}
for (x, y, z, t) in sorted(st, key=lambda s: (s[3] not in range(0x479A, 0x4910), s[0], s[1], s[3])):
    dx, dy = x - ORIGIN[0], y - ORIGIN[1]
    ix, iy = SPOT[0] + dx, SPOT[1] + dy
    on_sea = land[(ix, iy)][0] in SEA
    hull = 0x479A <= t <= 0x490F
    if 0x1796 <= t <= 0x17B2 or t == 0x44CC:
        continue
    if t == 0x0D34 and on_sea:
        continue
    if t in (0x0C2D, 0x0C2E, 0x0C2F, 0x0C30) and abs(dx) > 9:
        continue                                    # the far driftwood would lie on the road's side of the tip
    if t in (0x0C2D, 0x0C2E, 0x0C2F, 0x0C30) and on_sea and not any(
            abs(x - h[0]) <= 1 and abs(y - h[1]) <= 1 for h in hull_tiles):
        continue                                    # no driftwood out in open water, only against the hull
    keep.append((t, dx, dy, 0, 'sea' if on_sea else 'land', hull))
print('pieces', len(keep), 'hull', sum(1 for k in keep if k[5]))
rows = ['(%d, %d, %d, %d)' % (t, dx, dy, z) for (t, dx, dy, z, w, h) in keep]
for i in range(0, len(rows), 6):
    print('        ' + ', '.join(rows[i:i + 6]) + ',')
xs = [SPOT[0] + k[1] for k in keep]; ys = [SPOT[1] + k[2] for k in keep]
print('covers x', min(xs), max(xs), 'y', min(ys), max(ys))
