# cc-P678 read only: cc-P237's nhbase.Facet rules (pinned Map.GetAverageZ, GetTopSurfaceZ, CanFit's blocked test,
# wall_at, P34's walkway test, pinned DoorGenerator's scan) on the Siege of Sosaria Trammel map (SoS 3.0, through
# P481's islands loader) instead of the classic client's. Tiledata is the vanilla client's (islands.flags reads the
# same file): SoS uses stock art. Only the Haven box is loaded. ASCII only.
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(NOTES, 'cc-P481-tools'))
import islands  # noqa: E402
from mapbuild import uofiles  # noqa: E402  (islands put the docs copy's scripts folder on the path)

LAND, ITEMS = uofiles.read_tiledata(islands.VANILLA)
IMP, WET, SURF, BRIDGE, WALL, DOOR, ROOF = 0x40, 0x80, 0x200, 0x400, 0x10, 1 << 29, 1 << 28
BOX = (3540, 2440, 3790, 2730)   # the town box 3568-3761, 2460-2712 and a margin


def iflags(i): return ITEMS[i]['flags']
def iheight(i): return ITEMS[i]['height']
def iname(i): return ITEMS[i]['name'].strip()
def lname(i): return LAND[i][2].strip()
def calch(i): return iheight(i) // 2 if iflags(i) & BRIDGE else iheight(i)


class Facet:
    fi = 1

    def __init__(self):
        ids, zs = islands.load_land('sos')
        x0, y0, x1, y1 = BOX
        self.ids = ids[x0:x1 + 2, y0:y1 + 2].astype(int)
        self.zs = zs[x0:x1 + 2, y0:y1 + 2].astype(int)
        sx, sy, sz, sid = islands.load_statics('sos')
        m = (sx >= x0) & (sx <= x1 + 1) & (sy >= y0) & (sy <= y1 + 1)
        self.st = {}
        for x, y, z, i in zip(sx[m].tolist(), sy[m].tolist(), sz[m].tolist(), sid[m].tolist()):
            self.st.setdefault((x, y), []).append((i, z))

    def land(self, x, y):
        x0, y0, x1, y1 = BOX
        if not (x0 <= x <= x1 + 1 and y0 <= y <= y1 + 1): return (0, 0)
        return int(self.ids[x - x0, y - y0]), int(self.zs[x - x0, y - y0])

    def landz(self, x, y): return self.land(x, y)[1]

    def statics(self, x, y): return list(self.st.get((x, y), ()))

    def avgz(self, x, y):
        t, l, r, b = self.landz(x, y), self.landz(x, y + 1), self.landz(x + 1, y), self.landz(x + 1, y + 1)
        def fa(a, c):
            v = a + c
            if v < 0: v -= 1
            return int(v / 2)
        return fa(l, r) if abs(t - b) > abs(l - r) else fa(t, b)

    @staticmethod
    def ignored_land(i): return i == 2 or i == 0x1DB or 0x1AE <= i <= 0x1B5

    def top_surface(self, x, y, pz=127):
        s = None
        lid, _ = self.land(x, y)
        if not self.ignored_land(lid):
            a = self.avgz(x, y)
            if a <= pz: s = a
        for sid, sz in self.statics(x, y):
            f = iflags(sid)
            if f & SURF or f & WET:
                tz = sz + calch(sid)
                if (s is None or tz > s) and tz <= pz: s = tz
        return s

    def blocked(self, x, y, z):
        for sid, sz in self.statics(x, y):
            f = iflags(sid)
            if f & IMP and sz < z + 16 and sz + calch(sid) > z: return '0x%04X(%s)' % (sid, iname(sid))
        if LAND[self.land(x, y)[0]][0] & IMP and self.landz(x, y) >= z - 2: return 'impassable land'
        return ''

    def wall_at(self, x, y, z):
        return any(iflags(s) & WALL and z - 3 <= sz <= z + 3 for s, sz in self.statics(x, y))

    def roof_over(self, x, y, z):
        return any(sz >= z + 10 for s, sz in self.statics(x, y))

    def describe(self, x, y):
        return ' '.join('0x%04X@%d+%d(%s)' % (s, sz, iheight(s), iname(s)) for s, sz in self.statics(x, y)) or 'none'


WALK_LAND = ('dirt', 'cobblestone', 'flagstone', 'road', 'sand stone', 'marble', 'brick', 'stone', 'paving')
WALK_STATIC = ('road', 'path', 'planks', 'dock', 'pier', 'boards', 'cobblestone', 'flagstone', 'paving', 'tile', 'floor', 'marble', 'brick')


def walkway(F, x, y, z):
    """P34's rule: road-like land at z, or a floor/path static top at z."""
    ln = lname(F.land(x, y)[0]).lower()
    if F.top_surface(x, y, z + 2) is not None and any(w in ln for w in WALK_LAND) and abs(F.avgz(x, y) - z) <= 2: return 'land:' + ln
    for sid, sz in F.statics(x, y):
        n = iname(sid).lower()
        if abs(sz + calch(sid) - z) <= 2 and any(w in n for w in WALK_STATIC): return 'static:' + n
    return ''


# pinned DoorGenerator's frame lists and scan (cc-P237 nhbase.py, copied as is)
_SOUTH = [0x0006, 0x0008, 0x000B, 0x001A, 0x001B, 0x001F, 0x0038, 0x0057, 0x0059, 0x005B, 0x005D, 0x0080, 0x0081, 0x0082, 0x0084, 0x0090, 0x0091, 0x0094, 0x0096, 0x0099, 0x00A6, 0x00A7, 0x00AA, 0x00AE, 0x00B0, 0x00B3, 0x00C7, 0x00C9, 0x00F8, 0x00FA, 0x00FD, 0x00FE, 0x0100, 0x0103, 0x0104, 0x0106, 0x0109, 0x0127, 0x0129, 0x012B, 0x012D, 0x012F, 0x0131, 0x0132, 0x0134, 0x0135, 0x0137, 0x0139, 0x013B, 0x014C, 0x014E, 0x014F, 0x0151, 0x0153, 0x0155, 0x0157, 0x0158, 0x015A, 0x015D, 0x015E, 0x015F, 0x0162, 0x01CF, 0x01D1, 0x01D4, 0x01FF, 0x0204, 0x0206, 0x0208, 0x020A]
_NORTH = [0x0006, 0x0008, 0x000D, 0x001A, 0x001B, 0x0020, 0x003A, 0x0057, 0x0059, 0x005B, 0x005D, 0x0080, 0x0081, 0x0082, 0x0084, 0x0090, 0x0091, 0x0094, 0x0096, 0x0099, 0x00A6, 0x00A7, 0x00AC, 0x00AE, 0x00B0, 0x00C7, 0x00C9, 0x00F8, 0x00FA, 0x00FD, 0x00FE, 0x0100, 0x0103, 0x0104, 0x0106, 0x0109, 0x0127, 0x0129, 0x012B, 0x012D, 0x012F, 0x0131, 0x0132, 0x0134, 0x0135, 0x0137, 0x0139, 0x013B, 0x014C, 0x014E, 0x014F, 0x0151, 0x0153, 0x0155, 0x0157, 0x0158, 0x015A, 0x015D, 0x015E, 0x015F, 0x0162, 0x01CF, 0x01D1, 0x01D4, 0x01FF, 0x0201, 0x0204, 0x0208, 0x020A]
_EAST = [0x0007, 0x000A, 0x001A, 0x001C, 0x001E, 0x0037, 0x0058, 0x0059, 0x005C, 0x005E, 0x0080, 0x0081, 0x0082, 0x0084, 0x0090, 0x0092, 0x0095, 0x0097, 0x0098, 0x00A6, 0x00A8, 0x00AB, 0x00AE, 0x00AF, 0x00B2, 0x00C7, 0x00C8, 0x00EA, 0x00F8, 0x00F9, 0x00FC, 0x00FE, 0x00FF, 0x0102, 0x0104, 0x0105, 0x0108, 0x0127, 0x0128, 0x012B, 0x012C, 0x012E, 0x0130, 0x0132, 0x0133, 0x0135, 0x0136, 0x0138, 0x013A, 0x014C, 0x014D, 0x014F, 0x0150, 0x0152, 0x0154, 0x0156, 0x0158, 0x0159, 0x015C, 0x015E, 0x0160, 0x0163, 0x01CF, 0x01D0, 0x01D3, 0x01FF, 0x0203, 0x0205, 0x0207, 0x0209]
_WEST = [0x0007, 0x000C, 0x001A, 0x001C, 0x0021, 0x0039, 0x0058, 0x0059, 0x005C, 0x005E, 0x0080, 0x0081, 0x0082, 0x0084, 0x0090, 0x0092, 0x0095, 0x0097, 0x0098, 0x00A6, 0x00A8, 0x00AD, 0x00AE, 0x00AF, 0x00B5, 0x00C7, 0x00C8, 0x00EA, 0x00F8, 0x00F9, 0x00FC, 0x00FE, 0x00FF, 0x0102, 0x0104, 0x0105, 0x0108, 0x0127, 0x0128, 0x012C, 0x012E, 0x0130, 0x0132, 0x0133, 0x0135, 0x0136, 0x0138, 0x013A, 0x014C, 0x014D, 0x014F, 0x0150, 0x0152, 0x0154, 0x0156, 0x0158, 0x0159, 0x015C, 0x015E, 0x0160, 0x0163, 0x01CF, 0x01D0, 0x01D3, 0x01FF, 0x0200, 0x0203, 0x0207, 0x0209]
_SOUTH, _NORTH, _EAST, _WEST = set(_SOUTH), set(_NORTH), set(_EAST), set(_WEST)
SWING = {'WestCW': (-1, 1), 'EastCCW': (1, 1), 'WestCCW': (-1, 0), 'EastCW': (1, -1), 'SouthCW': (1, 1),
         'NorthCCW': (1, -1), 'SouthCCW': (0, 0), 'NorthCW': (0, -1)}


def _frame_at(F, x, y, z, frames):
    for sid, sz in F.statics(x, y):
        if sid in frames and -1 <= sz - z <= 1: return True, sz
    return False, None


def _can_fit(F, x, y, z):
    lid, lz = F.land(x, y)
    if LAND[lid][0] & IMP: return False
    for sid, sz in F.statics(x, y):
        f = iflags(sid)
        if (f & IMP or f & SURF) and sz < z + 16 and sz + calch(sid) > z: return False
    return True


def generated_doors(F, x0, y0, x1, y1):
    out = []
    def add(x, y, z, facing):
        if _can_fit(F, x, y, z): out.append((x, y, z, facing))
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for sid, z in F.statics(x, y):
                if sid in _WEST:
                    ok, nz = _frame_at(F, x + 2, y, z, _EAST)
                    if ok: add(x + 1, y, min(z, nz), 'WestCW'); continue
                    ok, nz = _frame_at(F, x + 3, y, z, _EAST)
                    if ok: add(x + 1, y, min(z, nz), 'WestCW'); add(x + 2, y, min(z, nz), 'EastCCW')
                elif sid in _NORTH:
                    ok, nz = _frame_at(F, x, y + 2, z, _SOUTH)
                    if ok: add(x, y + 1, min(z, nz), 'SouthCW'); continue
                    ok, nz = _frame_at(F, x, y + 3, z, _SOUTH)
                    if ok: add(x, y + 1, min(z, nz), 'NorthCCW'); add(x, y + 2, min(z, nz), 'SouthCW')
    return sorted(set(out))


_F = None
def facet():
    global _F
    if _F is None: _F = Facet()
    return _F
