# cc-P858: where the fortune teller's wagon (footprint x -2..3, y -6..9 with its new stair, the stair's foot at y 10)
# can stand near the Festival stall: every footprint tile flat land at z 0 with no static, the tile in front of the stair
# clear too, at least 2 tiles from the stall's pieces and the peddler. Prints the nearest candidates. Read only.
import os, sys
sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\scripts")
from mapbuild import uofiles as U
folder = sys.argv[1] if len(sys.argv) > 1 else r"D:\UO\tool-trials\client-data-copy"
AX, AY = 3636, 2627
STALL = [(0, 0), (0, 1), (1, 1), (-1, 0), (1, 0), (-2, -1)]
x1, y1, x2, y2 = AX - 30, AY - 30, AX + 30, AY + 30
land = U.MapFile(folder, 1).region(x1, y1, x2, y2)
st = {}
for (x, y, z, t) in U.statics_in(folder, 1, x1, y1, x2, y2):
    st.setdefault((x, y), []).append(t)
def free(x, y):
    return (x, y) in land and land[(x, y)][1] == 0 and (x, y) not in st
res = []
for ox in range(x1 + 3, x2 - 4):
    for oy in range(y1 + 7, y2 - 11):
        tiles = [(ox + dx, oy + dy) for dx in range(-2, 4) for dy in range(-6, 11)]
        if not all(free(*t) for t in tiles):
            continue
        near = min(max(abs(tx - (AX + sx)), abs(ty - (AY + sy))) for tx, ty in tiles for sx, sy in STALL)
        if near < 2:
            continue
        d = max(abs(ox - AX), abs(oy - AY))
        res.append((near, d, ox, oy))
res.sort()
for r in res[:25]:
    print("gap %d  origin %d,%d  (chebyshev %d from the peddler)" % (r[0], r[2], r[3], r[1]))
