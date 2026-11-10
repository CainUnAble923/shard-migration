"""cc-P858: renders main's New Haven ground (the Siege of Sosaria land and statics, P481's islands loader) round the
Festival stall, with the stall's pieces and the fortune teller's wagon added at a given origin, through isorender.py.

    python -P render858.py <out.jpg> <x1> <y1> <x2> <y2> [wagon_x,wagon_y,wagon_z] [vanilla] [cutaway=<z>]

"vanilla" draws the release's map (D:/UO/UltimaOnlineVanilla) instead. Hues are not drawn (isorender draws no hues).
"""
import os
import re
import sys

NOTES = r"D:\UO\golems\Iron\shard-migration\notes"
os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\scripts")
import islands  # noqa: E402
from mapbuild import isorender as iso  # noqa: E402
from mapbuild import uofiles as U  # noqa: E402
from PIL import Image  # noqa: E402

DESIGN = r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations\FestivalWagon\FortuneTellerWagonDesign.cs"
STALL_AT = (3636, 2627, 0)
STALL = [(0, 1, 0x0B7C), (1, 1, 0x0B7D), (-1, 0, 0x0E3D), (1, 0, 0x0E77), (-2, -1, 0xA854)]


def wagon_parts():
    text = open(DESIGN, encoding="utf-8").read()
    return [(int(i, 16), int(x), int(y), int(z)) for i, x, y, z in
            re.findall(r"new\(0x([0-9A-F]+), (-?\d+), (-?\d+), (-?\d+),", text)]


def main():
    out = sys.argv[1]
    x1, y1, x2, y2 = (int(v) for v in sys.argv[2:6])
    wagon = None
    vanilla = "vanilla" in sys.argv[6:]
    for a in sys.argv[6:]:
        if a.count(",") == 2:
            wagon = tuple(int(v) for v in a.split(","))
    land, statics = {}, []
    if vanilla:
        folder = r"D:\UO\UltimaOnlineVanilla"
        land = U.MapFile(folder, 1).region(x1, y1, x2, y2)
        statics = U.statics_in(folder, 1, x1, y1, x2, y2)
    else:
        ids, zs = islands.load_land('sos')
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                land[(x, y)] = (int(ids[x, y]), int(zs[x, y]))
        sx, sy, sz, sid = islands.load_statics('sos')
        m = (sx >= x1) & (sx <= x2) & (sy >= y1) & (sy <= y2)
        statics = [(int(a), int(b), int(c), int(d)) for a, b, c, d in zip(sx[m], sy[m], sz[m], sid[m])]
    ax, ay, az = STALL_AT
    statics += [(ax + dx, ay + dy, az, t) for dx, dy, t in STALL]
    if wagon:
        wx, wy, wz = wagon
        zmax = 999
        for a in sys.argv[6:]:
            if a.startswith("cutaway="):
                zmax = int(a.split("=")[1])   # parts at or above this z left out (the roof, for a look inside)
        statics += [(wx + x, wy + y, wz + z, t) for t, x, y, z in wagon_parts() if z < zmax]
    im = iso.render(iso.Scene(land, statics), x1, y1, x2, y2, art=iso.Art())
    im = im.convert("RGB")
    im.thumbnail((1400, 1400))
    im.save(out, quality=82)
    print(out, im.size)


if __name__ == "__main__":
    main()
