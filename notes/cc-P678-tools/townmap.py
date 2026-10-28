r"""cc-P678: a character map of SoS Haven for picking spots: '.' open ground, '#' under an impassable static,
'~' water, ' ' void, '+' a door or other static that is passable, digits mark a given list of points.
    python -P townmap.py x1 y1 x2 y2 [x,y ...]   (inclusive)  -> stdout
Each open tile's Z is the land's, or the lowest walkable static on it at or above the land (its floor, not the roof); the legend prints Z of marked points.
Read only, SoS 3.0 through P481's loaders.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cc-P481-tools"))
import islands  # noqa: E402

WATER = set(range(0x00A8, 0x00AC)) | set(range(0x0136, 0x0138))
VOID = {0x0244, 0x0002, 0x01DB}

_cache = {}


def load():
    if not _cache:
        ids, zs = islands.load_land("sos")
        sx, sy, sz, sid = islands.load_statics("sos")
        lf, itf = islands.flags()
        _cache.update(ids=ids, zs=zs, sx=sx, sy=sy, sz=sz, sid=sid, itf=itf, lf=lf)
    return _cache


def tile(x, y):
    """-> (kind, z): kind 'open', 'blocked', 'water', 'void'; z the land's, or the highest surface static's."""
    c = load()
    lid, lz = int(c["ids"][x, y]), int(c["zs"][x, y])
    m = (c["sx"] == x) & (c["sy"] == y)
    sids, szs = c["sid"][m], c["sz"][m]
    f = c["itf"][np.minimum(sids, len(c["itf"]) - 1)]
    imp = ((f & np.uint64(0x40)) != 0) & ((f & np.uint64(0x200)) == 0)
    surf = (f & np.uint64(0x200)) != 0
    if lid in VOID:
        return "void", lz
    if imp.any():
        return "blocked", lz
    if lid in WATER and not surf.any():
        return "water", lz
    # the floor: the lowest walkable surface at or above the land (a roof is a surface too, higher up)
    floors = [int(v) for v in szs[surf] if int(v) >= lz - 2]
    if not (int(c["lf"][lid]) & 0x40):   # passable land is a floor too (an earth or stone floor is land)
        floors.append(lz)
    z = min(floors) if floors else lz
    return "open", z


def draw(x1, y1, x2, y2, marks=()):
    load()
    mk = {(x, y): str(i % 10) for i, (x, y) in enumerate(marks)}
    print("     " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x1, x2 + 1)))
    for y in range(y1, y2 + 1):
        row = []
        for x in range(x1, x2 + 1):
            if (x, y) in mk:
                row.append(mk[(x, y)])
                continue
            k, _ = tile(x, y)
            row.append({"open": ".", "blocked": "#", "water": "~", "void": " "}[k])
        print("%4d " % y + "".join(row))
    for i, (x, y) in enumerate(marks):
        print(i % 10, x, y, *tile(x, y))


if __name__ == "__main__":
    a = [int(v) for v in sys.argv[1:5]]
    pts = [tuple(int(v) for v in p.split(",")) for p in sys.argv[5:]]
    draw(*a, pts)
