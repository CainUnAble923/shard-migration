"""cc-P741: windows of stock Trammel where a sandy coast runs on the map's diagonal (a stair of single steps), the
coasts that look level or upright on screen, so the isle's can copy what OSI lays there.
    python -P find_diag_coast.py"""
import collections, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import uofiles
C = 'D:/UO/UltimaOnlineVanilla'
mf = uofiles.MapFile(C, 1)
W, H = 5120, 4096
ids = np.zeros((W, H), dtype=np.int32)
reg = mf.region(0, 0, W - 1, H - 1)
for (x, y), (t, z) in reg.items():
    ids[x, y] = t
sea = np.isin(ids, [0xA8, 0xA9, 0xAA, 0xAB])
sand = ((ids >= 0x16) & (ids <= 0x19)) | ((ids >= 0x33) & (ids <= 0x3E))
land = ~sea
# a stair step of a coast running x+ / y- (land to the south-west): sea cell, land S and W, sea N and E
def sh(a, dx, dy):
    return np.roll(np.roll(a, -dx, 0), -dy, 1)
kinds = {
    'NE-facing (land SW)': sea & sh(land, 0, 1) & sh(land, -1, 0) & sh(sea, 0, -1) & sh(sea, 1, 0),
    'SW-facing (land NE)': sea & sh(land, 0, -1) & sh(land, 1, 0) & sh(sea, 0, 1) & sh(sea, -1, 0),
    'NW-facing (land SE)': sea & sh(land, 0, 1) & sh(land, 1, 0) & sh(sea, 0, -1) & sh(sea, -1, 0),
    'SE-facing (land NW)': sea & sh(land, 0, -1) & sh(land, -1, 0) & sh(sea, 0, 1) & sh(sea, 1, 0),
}
nearsand = sh(sand, 0, 1) | sh(sand, 0, -1) | sh(sand, 1, 0) | sh(sand, -1, 0)
for k, m in kinds.items():
    m = m & nearsand
    c = collections.Counter()
    for x, y in zip(*np.nonzero(m)):
        c[(x // 24 * 24, y // 24 * 24)] += 1
    print(k, int(m.sum()), c.most_common(6))
