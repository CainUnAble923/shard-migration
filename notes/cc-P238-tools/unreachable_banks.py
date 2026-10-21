"""cc-P238 Part 1: count the 8x8 ore banks on Felucca and Trammel that no walkable tile within 2 can reach.

Reads the client map files through cc-P151-tools/uomap.py (read-only). A bank is an ORE bank when at least one of its 64
tiles is mineable by our Mining.cs (server/patches/Mining.cs:24-55: land ranges _mountainCaveTiles, statics
_mountainCaveStaticTiles; RangedTiles = true, so each pair is an inclusive range). A bank is REACHABLE when some mineable
tile in it is within 2 (Chebyshev, Mining MaxRange 2, InRange is a square) of a walkable tile.

Walkable, approximately (the same reading as P151's ascii.py): the land is not impassable or wet (tiledata) and not a void
tile, or a surface static (a floor) covers it; and no static on it is impassable, a wall or wet unless it is a surface.
Heights are ignored: a ledge more than a step high still counts as walkable here, so the unreachable count is a FLOOR,
not a ceiling.

Usage: python -I unreachable_banks.py [facet ...]   (0 Felucca, 1 Trammel; default both)
"""
import os
import struct
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cc-P151-tools"))
import uomap  # noqa: E402

LAND_RANGES = [
    (220, 231), (236, 247), (252, 236), (268, 279), (286, 297), (321, 324), (467, 474), (476, 487), (492, 495),
    (543, 579), (581, 621), (1741, 1757), (1771, 1790), (1801, 1824), (1831, 1854), (1861, 1884), (1981, 2004),
    (2028, 2033), (2100, 2105), (0x3F39, 0x3F74), (0x3F82, 0x3F8F), (0x3F91, 0x3FCF),
]
STATIC_RANGES = [(0x053B, 0x054F)]
VOID_LAND = {0x2, 0x1DB, 0x244}


def in_ranges(i, ranges):
    return any(lo <= i <= hi for lo, hi in ranges)


def main(facets):
    land_td, stat_td = uomap.tiledata()
    land_mine = [in_ranges(i, LAND_RANGES) for i in range(0x4000)]
    land_pass = [not (f & (uomap.F_IMPASSABLE | uomap.F_WET)) and i not in VOID_LAND for i, (f, _) in enumerate(land_td)]
    stat_mine = [in_ranges(i, STATIC_RANGES) for i in range(len(stat_td))]
    stat_surface = [bool(f & uomap.F_SURFACE) for f, _, _ in stat_td]
    stat_block = [bool(f & (uomap.F_IMPASSABLE | uomap.F_WALL | uomap.F_WET)) and not (f & uomap.F_SURFACE)
                  for f, _, _ in stat_td]

    for n in facets:
        t0 = time.time()
        fac = uomap.Facet(n)
        bw, bh = fac.w // 8, fac.h // 8
        walk = bytearray(fac.w * fac.h)   # 1 = walkable
        mine_banks = {}                   # (bx, by) -> list of mineable (x, y)

        for bx in range(bw):
            for by in range(bh):
                b = bx * bh + by
                off = b * 196 + 4
                cells = list(struct.iter_unpack("<Hb", fac._map[off:off + 192]))
                stats = fac.statics_block(bx, by)
                fac._stat_cache.clear()
                mined = None
                for k, (tid, _z) in enumerate(cells):
                    x, y = bx * 8 + (k & 7), by * 8 + (k >> 3)
                    tid &= 0x3FFF
                    st = stats.get((x, y), ())
                    surface = blocked = smine = False
                    for sid, _sz in st:
                        if sid >= len(stat_td):
                            continue
                        surface |= stat_surface[sid]
                        blocked |= stat_block[sid]
                        smine |= stat_mine[sid]
                    if (land_pass[tid] or surface) and not blocked:
                        walk[y * fac.w + x] = 1
                    if land_mine[tid] or smine:
                        if mined is None:
                            mined = mine_banks.setdefault((bx, by), [])
                        mined.append((x, y))

        def reachable(tiles):
            for (x, y) in tiles:
                for yy in range(max(0, y - 2), min(fac.h, y + 3)):
                    row = yy * fac.w
                    for xx in range(max(0, x - 2), min(fac.w, x + 3)):
                        if walk[row + xx]:
                            return True
            return False

        split = 5120  # the mainland ends here on both facets; east of it are the dungeons and Green Acres
        totals = {"main": [0, 0], "east": [0, 0]}
        unreachable_examples = []
        for (bx, by), tiles in mine_banks.items():
            part = "main" if bx * 8 < split else "east"
            totals[part][0] += 1
            if not reachable(tiles):
                totals[part][1] += 1
                if len(unreachable_examples) < 8 and part == "main":
                    unreachable_examples.append((bx * 8, by * 8))

        name = {0: "Felucca", 1: "Trammel"}.get(n, str(n))
        all_banks = totals["main"][0] + totals["east"][0]
        all_un = totals["main"][1] + totals["east"][1]
        print(f"{name}: {all_banks} ore banks, {all_un} unreachable ({100.0 * all_un / max(1, all_banks):.1f}%); "
              f"mainland (x < {split}) {totals['main'][1]} of {totals['main'][0]}, "
              f"east (x >= {split}) {totals['east'][1]} of {totals['east'][0]}; {time.time() - t0:.0f} s")
        print(f"  first unreachable mainland banks (x, y of the corner): {unreachable_examples}")


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]] or [0, 1])
