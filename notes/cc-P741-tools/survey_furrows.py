"""cc-P741: OSI's furrowed field land on stock Trammel: how often each furrow tile is used, and the densest field.
    python -P survey_furrows.py"""
import collections, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import uofiles
C = 'D:/UO/UltimaOnlineVanilla'
W, H = 5120, 4096
reg = uofiles.MapFile(C, 1).region(0, 0, W - 1, H - 1)
F = set(range(0x9, 0x16)) | set(range(0x150, 0x15D))
cnt = collections.Counter(); win = collections.Counter(); z = collections.Counter()
for (x, y), (t, zz) in reg.items():
    if t in F:
        cnt[t] += 1; win[(x // 16 * 16, y // 16 * 16)] += 1; z[zz] += 1
print('furrow tiles', sum(cnt.values()), [(hex(t), n) for t, n in cnt.most_common()])
print('windows', win.most_common(5)); print('z', z.most_common(5))
