"""cc-P871 (P866 review, item 2): renders each of the variable carpet's six styles laid NON-square, 5 by 3 and 3 by 5,
through isorender.py, with the art each tile gets chosen exactly as VariableCarpetStyle.ArtAt chooses it (the style
table and ArtAt are read from the code copy, not retyped). Writes one image per style and a sheet of all six, and
prints the placed.md lines.

    python -P render871.py <out folder>
"""
import os
import re
import sys

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
os.environ.setdefault("MAPBUILD_ART", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\scripts")
from mapbuild import isorender as iso  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

CODE = r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations\Items\Addons\VariableCarpet.cs"
FLOOR = 0x0519   # grey paver static under the carpet, as a house floor (P857 laid its proofs on a stone floor)
GRASS = 0x0003


def styles():
    text = open(CODE, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'new\("([^"]+)", ((?:0x[0-9A-F]+, ){8}0x[0-9A-F]+)\)', text):
        out.append((m.group(1), [int(v, 16) for v in m.group(2).split(", ")]))
    assert len(out) == 6, out
    return out


def art_at(s, x, y, last_x, last_y):
    # VariableCarpetStyle.ArtAt, same order: (west, east, north, south)
    north_c, east_c, south_c, west_c, nw_e, ne_e, se_e, sw_e, mid = s
    west, east, north, south = x == 0, x == last_x, y == 0, y == last_y
    if west and north: return north_c
    if east and north: return east_c
    if east and south: return south_c
    if west and south: return west_c
    if west: return nw_e
    if north: return ne_e
    if east: return se_e
    if south: return sw_e
    return mid


def lay(s, ox, oy, w, h):
    return [(ox + x, oy + y, 0, art_at(s, x, y, w - 1, h - 1)) for x in range(w) for y in range(h)]


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    x1, y1, x2, y2 = 0, 0, 13, 9
    land = {(x, y): (GRASS, 0) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}
    art = iso.Art()
    tiles, lines = [], []
    for i, (name, s) in enumerate(styles()):
        statics = [(x, y, -1, FLOOR) for x in range(1, 13) for y in range(1, 9)]
        statics += lay(s, 1, 2, 5, 3)    # 5 wide (x), 3 deep (y)
        statics += lay(s, 8, 1, 3, 5)    # 3 wide, 5 deep
        im = iso.render(iso.Scene(land, statics), x1, y1, x2, y2, art=art).convert("RGB")
        d = ImageDraw.Draw(im)
        d.text((8, 8), "%d %s: left 5 by 3 (x by y), right 3 by 5" % (i, name), fill=(255, 220, 120))
        slug = re.sub(r"[^a-z]+", "-", name.lower()).strip("-")
        path = os.path.join(out, "carpet-%d-%s.jpg" % (i, slug))
        im.save(path, quality=85)
        tiles.append(im)
        n = ["NW corner (ArtAt north)", "NE corner (east)", "SE corner (south)", "SW corner (west)",
             "W edge (north-west)", "N edge (north-east)", "E edge (south-east)", "S edge (south-west)", "middle"]
        lines.append("- style %d, %s: " % (i, name) + "; ".join("%s 0x%04X" % (a, b) for a, b in zip(n, s)))
        print(path)
    w, h = tiles[0].size
    sheet = Image.new("RGB", (w * 3, h * 2))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % 3) * w, (i // 3) * h))
    sheet.thumbnail((2400, 2400))
    sheet.save(os.path.join(out, "carpets-all-six.jpg"), quality=82)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
