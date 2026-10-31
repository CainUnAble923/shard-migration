"""Where the north block (invasion rooms) meets the dungeon proper on stock Trammel, and what the south-west block is."""
import sys, collections
sys.path.insert(0, r"D:/UO/golems/Iron/shard-migration/scripts")
from mapbuild import uofiles
import numpy as np

STOCK = r"D:/UO/UltimaOnlineVanilla"
ids, zs = uofiles.load_land(STOCK, 1)
st = uofiles.statics_in(STOCK, 1, 6150, 2300, 6500, 2860)
occ = np.zeros((7168, 4096), bool)
occ[6150:6501, 2300:2861] = ids[6150:6501, 2300:2861] != uofiles.VOID
for s in st:
    occ[s[0], s[1]] = True

# rows: how many cells occupied per row in the north block's x span
for y in range(2575, 2600):
    row = "".join("#" if occ[x, y] else "." for x in range(6240, 6500))
    print(y, row)

for name, (x1, y1, x2, y2) in {"north": (6240, 2310, 6495, 2590), "sw": (6176, 2752, 6303, 2847)}.items():
    sub = ids[x1:x2 + 1, y1:y2 + 1]
    c = collections.Counter(sub.flatten().tolist())
    print(name, "land", [(hex(k), v) for k, v in c.most_common(8)])
    ss = [s for s in st if x1 <= s[0] <= x2 and y1 <= s[1] <= y2]
    c2 = collections.Counter(s[2] for s in ss)
    print(name, "statics", len(ss), [(hex(k), v) for k, v in c2.most_common(10)])
print("static tuple sample", st[0])
