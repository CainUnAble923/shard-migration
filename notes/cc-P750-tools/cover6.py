# cc-P750 scratch: cover model probe (see the notes). Reads this task's SoS client folder, never the default.
import os
os.environ.setdefault('MAPBUILD_CLIENT', 'D:/UO/golems/Iron/p708-work/sosclient')
os.environ.setdefault('MAPBUILD_ART', 'D:/UO/golems/Iron/p708-work/sosclient')
import sys, json
import numpy as np
sys.path.insert(0, 'D:/UO/golems/Iron/shard-migration/scripts')
from mapbuild import isorender as iso
SOS = 'D:/UO/golems/Iron/p708-work/sosclient'
art = iso.Art()
def cover(x, y, z):
    sc = iso.Scene.from_map(SOS, 1, x - 1, y - 1, x + 16, y + 16)
    cx = (x - y) * 22 + 22; feet = (x + y) * 22 + 22 - z * 4
    L, T, W, H = cx - 10, feet - 60, 20, 60
    cov = np.zeros((H, W), bool)
    over = [s[2] for s in sc.statics if (s[0], s[1]) == (x, y) and s[2] > z + 10]
    maxz = min(over) if over else None
    for (sx, sy, sz, tid) in sc.statics:
        if sx + sy <= x + y or (maxz is not None and sz >= maxz):
            continue
        im = art.static(tid)
        if im is None:
            continue
        m = np.array(im)[:, :, 3] > 0
        hh, ww = m.shape
        left = (sx - sy) * 22 + 22 - ww // 2; top = (sx + sy) * 22 + 44 - hh - sz * 4
        ox0, oy0 = max(L, left), max(T, top); ox1, oy1 = min(L + W, left + ww), min(T + H, top + hh)
        if ox0 < ox1 and oy0 < oy1:
            cov[oy0 - T:oy1 - T, ox0 - L:ox1 - L] |= m[oy0 - top:oy1 - top, ox0 - left:ox1 - left]
    return cov.mean() if maxz is None else (cov.mean(), maxz)
d = json.load(open(sys.argv[1]))
hs = d['halls'] if isinstance(d, dict) else d
for h in hs:
    if h['key'] in ('league', 'merchants', 'healers', 'rangers', 'tinkers', 'custodians'):
        n, t = h['npc'], h['travel']
        print('%-11s npc %s %s   stop %s %s' % (h['key'], (n['x'], n['y'], n['z']), cover(n['x'], n['y'], n['z']), (t['x'], t['y'], t['z']), cover(t['x'], t['y'], t['z'])))
print('P708 rangers post (1003,1004,0) %s' % cover(1003, 1004, 0))
