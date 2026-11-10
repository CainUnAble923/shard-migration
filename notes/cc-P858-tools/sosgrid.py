# cc-P858: stallgrid.py's character map, but on the Siege of Sosaria map main's Trammel uses (P481's islands loader).
import os, sys
NOTES = r"D:\UO\golems\Iron\shard-migration\notes"
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
import islands
from mapbuild import uofiles
LAND, ITEMS = uofiles.read_tiledata(islands.VANILLA)
x1, y1, x2, y2 = (int(v) for v in sys.argv[1:5])
ids, zs = islands.load_land('sos')
sx, sy, sz, sid = islands.load_statics('sos')
st = {}
import numpy as np
m = (sx >= x1) & (sx <= x2) & (sy >= y1) & (sy <= y2)
for x, y, z, t in zip(sx[m], sy[m], sz[m], sid[m]):
    st.setdefault((int(x), int(y)), []).append((int(z), int(t)))
print("     " + "".join(str(x % 10) for x in range(x1, x2 + 1)))
for y in range(y1, y2 + 1):
    row = ""
    for x in range(x1, x2 + 1):
        if (x, y) == (3636, 2627):
            row += "P"; continue
        s = st.get((x, y), [])
        if any(ITEMS[t]["flags"] & 0x40 for z, t in s): row += "#"
        elif s: row += "s"
        else:
            z = int(zs[x, y]); row += "." if z == 0 else ("~" if z < 0 else str(min(9, z // 5)))
    print(y, row)
