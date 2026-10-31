import sys, collections
sys.path.insert(0, r"D:/UO/golems/Iron/shard-migration/scripts")
from mapbuild import uofiles
import numpy as np

STOCK = r"D:/UO/UltimaOnlineVanilla"
x1, y1, x2, y2 = 6151, 2301, 6563, 2839
ids, zs = uofiles.load_land(STOCK, 1)
sub = ids[x1:x2 + 1, y1:y2 + 1]
c = collections.Counter(sub.flatten().tolist())
print("land ids top:", [(hex(k), v) for k, v in c.most_common(12)])
nonvoid = sub != uofiles.VOID
xs, ys = np.nonzero(nonvoid)
print("nonvoid land cells", nonvoid.sum(), "bbox", x1 + xs.min(), y1 + ys.min(), x1 + xs.max(), y1 + ys.max())
st = uofiles.statics_in(STOCK, 1, x1 - 40, y1 - 40, x2 + 40, y2 + 40)
inbox = [s for s in st if x1 <= s[0] <= x2 and y1 <= s[1] <= y2]
out = [s for s in st if not (x1 <= s[0] <= x2 and y1 <= s[1] <= y2)]
print("statics in box", len(inbox), "in 40 margin outside", len(out))
sx = [s[0] for s in inbox]; sy = [s[1] for s in inbox]
print("statics bbox", min(sx), min(sy), max(sx), max(sy))
# nonvoid in margin around
M = 40
big = ids[x1 - M:x2 + M + 1, y1 - M:y2 + M + 1] != uofiles.VOID
print("nonvoid in margin ring", big.sum() - nonvoid.sum())
# rows/cols occupancy profile
occ = nonvoid.copy()
for s in inbox:
    occ[s[0] - x1, s[1] - y1] = True
rows = occ.any(axis=0)
cols = occ.any(axis=1)
def runs(a, base):
    out, start = [], None
    for i, v in enumerate(a):
        if v and start is None: start = i
        if not v and start is not None: out.append((base + start, base + i - 1)); start = None
    if start is not None: out.append((base + start, base + len(a) - 1))
    return out
print("y runs", runs(rows, y1))
print("x runs", runs(cols, x1))
