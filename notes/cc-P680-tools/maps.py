"""cc-P680 (SoS swap S5): the three maps the decoration is graded on, with fast per-tile reads.

  sos    the server's overlay (Build-MapOverlay.ps1's output: the SoS base with our trammel.mapops), file index 1. Trammel
         and Felucca both read it (server/customizations/Maps/SosMaps.cs).
  tram   EA's own Trammel: D:\\UO\\UltimaOnlineVanilla, file index 1 (P669's stock).
  fel    EA's own Felucca: the same folder, file index 0. It differs from Trammel on about 1.07 million tiles, so a
         Felucca-only cfg is graded against it.

tiledata comes from MAPBUILD_CLIENT. Each Map reads land once (numpy) and statics per 8 x 8 block, cached.
"""
import functools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(DOCS, 'scripts'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P481-tools'))
from mapbuild import uofiles  # noqa: E402
import islands  # noqa: E402

VANILLA = r'D:\UO\UltimaOnlineVanilla'
IMP, WET, WALL, WINDOW, SURF, BRIDGE, ROOF, DOOR = 0x40, 0x80, 0x10, 0x1000, 0x200, 0x400, 1 << 28, 1 << 29
VOID_IDS = set(int(i) for i in islands.VOID_IDS)
IGNORED_LAND = {2, 0x1DB} | set(range(0x1AE, 0x1B6))  # pinned LandTile.Ignored (cc-P679)
STRUCT = IMP | WALL | WINDOW | SURF | ROOF | DOOR

_TILEDATA = None


def tiledata():
    global _TILEDATA
    if _TILEDATA is None:
        _TILEDATA = uofiles.read_tiledata(uofiles.CLIENT)
    return _TILEDATA


class Map:
    def __init__(self, folder, fi):
        self.folder, self.fi = folder, fi
        self.ids, self.zs = uofiles.load_land(folder, fi)
        self.idx, self.sta = uofiles.load_statics_index(folder, fi)
        self.land, self.items = tiledata()
        self.bh = uofiles.FACETS[fi][2] >> 3
        self._block = functools.lru_cache(maxsize=400000)(self._read_block)

    def _read_block(self, b):
        out = {}
        for (tid, cx, cy, z, hue) in uofiles.block_statics(self.idx, self.sta, b):
            out.setdefault((cx, cy), []).append((z, tid))
        return out

    def statics(self, x, y):
        """[(z, id)] on the tile."""
        if not (0 <= x < 7168 and 0 <= y < 4096):
            return []
        return self._block((x >> 3) * self.bh + (y >> 3)).get((x & 7, y & 7), [])

    def flags(self, tid):
        return self.items[tid]['flags']

    def height(self, tid):
        it = self.items[tid]
        return it['height'] // 2 if it['flags'] & BRIDGE else it['height']

    def name(self, tid):
        return self.items[tid]['name']

    def land_kind(self, x, y):
        lid = int(self.ids[x, y])
        if lid in VOID_IDS:
            return 'void'
        if lid in IGNORED_LAND:
            return 'ignored'
        if self.land[lid][0] & WET:
            return 'water'
        if self.land[lid][0] & IMP:
            return 'rock'
        return 'ground'

    def avgz(self, x, y):
        """pinned Map.GetAverageZ (FloorAverage rounds down; cc-P679)."""
        zs = self.zs
        t, l = int(zs[x, y]), int(zs[x, min(4095, y + 1)])
        r, b = int(zs[min(7167, x + 1), y]), int(zs[min(7167, x + 1), min(4095, y + 1)])
        return (l + r) // 2 if abs(t - b) > abs(l - r) else (t + b) // 2

    def same_tile(self, other, x, y):
        """The same for anything placed there: the land's height and kind (ground, rock, water, void, cave mouth) and
        the same statics. A re-textured floor (the author re-tiled Destard's caves, same heights) counts as the same."""
        return (int(self.zs[x, y]) == int(other.zs[x, y]) and self.land_kind(x, y) == other.land_kind(x, y)
                and sorted(self.statics(x, y)) == sorted(other.statics(x, y)))


def sos(folder):
    return Map(folder, 1)


def stock(facet):
    return Map(VANILLA, 0 if facet == 'Felucca' else 1)
