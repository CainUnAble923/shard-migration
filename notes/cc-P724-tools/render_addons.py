"""cc-P724: renders addon scripts (their component tables) on sand with scripts/mapbuild/isorender.py, the overseer's
render_addons.py made general. Usage: python -P render_addons.py <out.jpg> <title=path.cs> ... ; a path may also be
"ids:0xA62B" for single items."""
import os
import re
import sys

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from mapbuild import isorender as iso  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402


def components(path):
    if path.startswith("ids:"):
        return [(int(v, 0), i * 2, 0, 0) for i, v in enumerate(path[4:].split(","))]
    txt = open(path, encoding="utf-8", errors="ignore").read()
    comps = [tuple(int(v) for v in m) for m in
             re.findall(r"\{\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\}", txt)]
    for m in re.findall(r"AddComponent\(\s*new\s+AddonComponent\(\s*(0x[0-9A-Fa-f]+|\d+)\s*\)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)", txt):
        comps.append((int(m[0], 0), int(m[1]), int(m[2]), int(m[3])))
    for m in re.findall(r"AddComplexComponent\(\s*\(BaseAddon\)\s*this\s*,\s*(0x[0-9A-Fa-f]+|\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)", txt):
        comps.append((int(m[0], 0), int(m[1]), int(m[2]), int(m[3])))
    return [c for c in comps if c[0] > 100]


def main():
    out = sys.argv[1]
    art = iso.Art()
    tiles = []
    for arg in sys.argv[2:]:
        title, path = arg.split("=", 1)
        comps = components(path)
        statics = [(x, y, z, tid) for tid, x, y, z in comps]
        xs = [s[0] for s in statics]
        ys = [s[1] for s in statics]
        pad = 2
        land = {(x, y): (0x0016, 0) for x in range(min(xs) - pad, max(xs) + pad + 2) for y in range(min(ys) - pad, max(ys) + pad + 2)}
        im = iso.render(iso.Scene(land, statics), min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad, art=art)
        print(title, len(comps), im.size)
        tiles.append((title, im))
    w = sum(min(im.width, 500) for _, im in tiles) + 20 * (len(tiles) + 1)
    h = max(min(im.height, 500) for _, im in tiles) + 50
    sheet = Image.new("RGB", (w, h), (27, 27, 27))
    d = ImageDraw.Draw(sheet)
    x = 20
    for title, im in tiles:
        im = im.copy()
        im.thumbnail((500, 500))
        d.text((x, 10), title, fill=(240, 198, 116))
        sheet.paste(im.convert("RGB"), (x, 35))
        x += im.width + 20
    sheet.save(out, quality=85)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
