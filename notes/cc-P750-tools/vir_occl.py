# cc-P750 scratch: cover model probe (see the notes). Reads this task's SoS client folder, never the default.
import os
os.environ.setdefault('MAPBUILD_CLIENT', 'D:/UO/golems/Iron/p708-work/sosclient')
os.environ.setdefault('MAPBUILD_ART', 'D:/UO/golems/Iron/p708-work/sosclient')
"""Per open tile: fraction of a standing figure's screen box (20x60 px above the tile centre) covered by art drawn after
it (tiles with a larger x+y), from the real art alpha. Read only."""
import sys
import numpy as np
sys.path.insert(0, 'D:/UO/golems/Iron/shard-migration/scripts')
from mapbuild import isorender as iso
SOS = 'D:/UO/golems/Iron/p708-work/sosclient'
x1, y1, x2, y2 = (int(v) for v in sys.argv[1:5])
sc = iso.Scene.from_map(SOS, 1, x1 - 2, y1 - 2, x2 + 14, y2 + 14)
art = iso.Art()
alpha = {}
def a(tid):
    if tid not in alpha:
        im = art.static(tid)
        alpha[tid] = None if im is None else (np.array(im)[:, :, 3] > 0)
    return alpha[tid]
occ = set((s[0], s[1]) for s in sc.statics)
items = []
for (x, y, z, tid) in sc.statics:
    m = a(tid)
    if m is None:
        continue
    h, w = m.shape
    left = (x - y) * 22 + 22 - w // 2
    top = (x + y) * 22 + 44 - h - z * 4
    items.append((x + y, left, top, m))
res = {}
for y in range(y1, y2 + 1):
    for x in range(x1, x2 + 1):
        if (x, y) in occ:
            continue
        cx = (x - y) * 22 + 22
        feet = (x + y) * 22 + 22
        L, T, W, H = cx - 10, feet - 60, 20, 60
        cov = np.zeros((H, W), bool)
        for (d, left, top, m) in items:
            if d <= x + y:
                continue
            hh, ww = m.shape
            ox0, oy0 = max(L, left), max(T, top)
            ox1, oy1 = min(L + W, left + ww), min(T + H, top + hh)
            if ox0 >= ox1 or oy0 >= oy1:
                continue
            cov[oy0 - T:oy1 - T, ox0 - L:ox1 - L] |= m[oy0 - top:oy1 - top, ox0 - left:ox1 - left]
        res[(x, y)] = cov.mean()
print('covered fraction per open tile, 0-9 (tenths), # = has statics')
print('      ' + ''.join(str(x % 10) for x in range(x1, x2 + 1)))
for y in range(y1, y2 + 1):
    print('%5d ' % y + ''.join('#' if (x, y) not in res else str(min(9, int(res[(x, y)] * 10))) for x in range(x1, x2 + 1)))
for k in [(1003, 1004), (1000, 1006), (1001, 980), (1002, 985), (1000, 990)]:
    print(k, None if k not in res else round(res[k], 2))
