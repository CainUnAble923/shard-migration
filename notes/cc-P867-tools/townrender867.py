"""cc-P867: isorender of each town spot (town867.py) on main's SoS map with the design in place: land and statics from
P678's SoS facet reader, statics more than 15 over the floor left out so the room shows, the pieces at their rows.

  python -P townrender867.py <out folder>     writes town-<design>.jpg and town-rows.txt
"""
import ast
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, os.path.join(HERE, "..", "cc-P678-tools", "winter"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
sys.path.insert(0, HERE)
import sosbase as B  # noqa: E402
from mapbuild import isorender as iso  # noqa: E402
import decorcfg as D  # noqa: E402


def town_rows():
    text = open(os.path.join(HERE, "town-out.txt")).read()
    return ast.literal_eval(text.split("TOWN = ", 1)[1].split("\n]", 1)[0] + "\n]")


def main(out):
    F = B.facet()
    art = iso.Art()
    rows = []
    for design, facing, ox, oy, oz, stand in town_rows():
        _, parts = D.read(design)
        x1, y1, x2, y2 = ox - 6, oy - 6, ox + 7, oy + 7
        land = {(x, y): F.land(x, y) for x in range(x1 - 2, x2 + 4) for y in range(y1 - 2, y2 + 4)}
        statics = [(x, y, z, i) for (x, y) in land for i, z in F.statics(x, y) if z <= oz + 15]
        for tid, dx, dy, dz in parts:
            statics.append((ox + dx, oy + dy, oz + dz, tid))
            rows.append("%s|%s|0x%04X|%d,%d,%d" % (design, facing, tid, ox + dx, oy + dy, oz + dz))
        im = iso.render(iso.Scene(land, statics), x1, y1, x2, y2, art=art).convert("RGB")
        im.thumbnail((700, 700))
        p = os.path.join(out, "town-%s.jpg" % design)
        im.save(p, quality=85)
        print(p, im.size)
    open(os.path.join(HERE, "town-rows.txt"), "w").write("\n".join(rows) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
