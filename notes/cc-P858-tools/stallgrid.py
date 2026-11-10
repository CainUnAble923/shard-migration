# cc-P858: a character map of the ground round the Festival stall on one map folder: '.' flat land at z 0, a digit the
# land z / 5 when not 0, '#' an impassable static, 's' any other static, 'P' the peddler's anchor. Read only.
import os, sys
sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\scripts")
folder = sys.argv[1]
os.environ["MAPBUILD_CLIENT"] = r"D:\UO\tool-trials\client-data-copy"
from mapbuild import uofiles as U
_, items = U.read_tiledata(r"D:\UO\tool-trials\client-data-copy")
x1, y1, x2, y2 = (int(v) for v in sys.argv[2:6]) if len(sys.argv) > 5 else (3618, 2606, 3656, 2650)
land = U.MapFile(folder, 1).region(x1, y1, x2, y2)
st = {}
for (x, y, z, t) in U.statics_in(folder, 1, x1, y1, x2, y2):
    st.setdefault((x, y), []).append((z, t))
print("     " + "".join(str(x % 10) for x in range(x1, x2 + 1)))
for y in range(y1, y2 + 1):
    row = ""
    for x in range(x1, x2 + 1):
        if (x, y) == (3636, 2627):
            row += "P"; continue
        s = st.get((x, y), [])
        if any(items[t]["flags"] & 0x40 for z, t in s):
            row += "#"
        elif s:
            row += "s"
        else:
            lid, lz = land[(x, y)]
            row += "." if lz == 0 else ("~" if lz < 0 else str(min(9, lz // 5)))
    print(y, row)
