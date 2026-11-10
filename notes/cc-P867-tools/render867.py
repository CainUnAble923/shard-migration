"""cc-P867: isorender of each round of plan867.py: the staged house (OSI's large brick house, multi 0x74, below its roof,
so every wall corner shows) with the round's pieces at the floor tiles the trainee targets.
Client-correct statics (scripts/mapbuild/isorender.py), flat grass for the land (the plot is grass, Z 20-21).

  python -P render867.py <out folder>     writes house-<round>.jpg and placed-rows.txt
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
from mapbuild import isorender as iso  # noqa: E402
import decorcfg as D  # noqa: E402
import plan867 as P  # noqa: E402

HOUSE_Z = P.HOUSE_Z


def house_statics():
    sc = iso.Scene.from_multi(P.MULTI, 26)   # floor and walls at multi Z 7, none of the roof
    return [(P.CX + x, P.CY + y, HOUSE_Z + z, t) for x, y, z, t in sc.statics]


def main(out):
    os.makedirs(out, exist_ok=True)
    art = iso.Art()
    plan, missing = P.main()
    house = house_statics()
    rows = []
    x1, y1, x2, y2 = P.CX - 8, P.CY - 8, P.CX + 7, P.CY + 7   # the whole house
    for name, row, stand in plan:
        statics = list(house)
        for design, wall, ox, oy, oz, who in row:
            head, parts = D.read(design)
            for tid, dx, dy, dz in parts:
                statics.append((ox + dx, oy + dy, oz + dz, tid))
                rows.append("%s|%s|%s|0x%04X|%d,%d,%d|%s" % (name, design, wall, tid, ox + dx, oy + dy, oz + dz, who))
        land = {(x, y): (0x0003, 0) for x in range(x1 - 3, x2 + 4) for y in range(y1 - 3, y2 + 4)}
        for (x, y) in land:
            land[(x, y)] = (0x0003, HOUSE_Z)
        im = iso.render(iso.Scene(land, statics), x1, y1, x2, y2, art=art).convert("RGB")
        path = os.path.join(out, "house-%s.jpg" % name)
        im.save(path, quality=85)
        print(path, im.size, os.path.getsize(path))
    with open(os.path.join(HERE, "placed-rows.txt"), "w") as f:
        f.write("\n".join(rows) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
