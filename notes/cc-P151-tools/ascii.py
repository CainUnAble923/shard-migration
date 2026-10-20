"""Top-down tile map: one char per tile.
 ~ water   ^ impassable land (rock/mountain)   T tree/foliage blocker   # wall or other blocker
 = covered (roof or static floor)   . clear land   , clear land with flat decor   + z step (land differs >4 from west neighbour)
 S spawner  s sign"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import uomap, survey
from uomap import *

land_td, stat_td = uomap.tiledata()


def char(fac, x, y):
    tid, z = fac.land(x, y)
    lf = land_td[tid & 0x3FFF][0]
    st = fac.statics(x, y)
    block = None
    covered = False
    flat = False
    for sid, sz in st:
        f, h, name = stat_td[sid]
        if f & F_ROOF or (f & F_SURFACE and h <= 1):
            covered = True
        elif f & F_WET:
            block = block or "~"
        elif f & (F_IMPASSABLE | F_WALL):
            block = "T" if f & F_FOLIAGE or "tree" in name or "trunk" in name else "#"
        else:
            flat = True
    if block == "#" or block == "T":
        return block
    if covered:
        return "="
    if lf & F_WET or block == "~":
        return "~"
    if lf & F_IMPASSABLE or tid in (0x2, 0x1DB):
        return "^"
    return "," if flat else "."


def draw(facet, x1, y1, x2, y2):
    fac = uomap.Facet(facet)
    sp = {(s[0], s[1]) for s in survey.SPAWNERS[survey.MAPNAME[facet]]}
    sg = {(s[0], s[1]) for s in survey.SIGNS[facet]}
    print("      " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x1, x2 + 1)))
    for y in range(y1, y2 + 1):
        row = []
        for x in range(x1, x2 + 1):
            if (x, y) in sp:
                row.append("S")
            elif (x, y) in sg:
                row.append("s")
            else:
                row.append(char(fac, x, y))
        print(f"{y:5d} " + "".join(row))


if __name__ == "__main__":
    f = int(sys.argv[1]); x1, y1, x2, y2 = map(int, sys.argv[2].split(","))
    draw(f, x1, y1, x2, y2)
