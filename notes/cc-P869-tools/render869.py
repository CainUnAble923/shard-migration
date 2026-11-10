"""cc-P869: renders New Haven ground with New Haven's winter set pieces (WinterSetDesigns.cs) placed at given origins,
through isorender.py. Main is the Siege of Sosaria land (P481's islands loader); "vanilla" draws the release's map.

    python -P render869.py <out.jpg> <x1> <y1> <x2> <y2> design@x,y,z [design@x,y,z ...] [vanilla] [rows]

"rows" also draws P678's winter rows of main (cc-P678-tools/winter/placement.json) that fall in the box.
Hues are not drawn (isorender draws no hues).
"""
import json
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

DESIGNS = r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations\WinterSet\WinterSetDesigns.cs"


def parts(design):
    text = open(DESIGNS, encoding="utf-8").read()
    block = text.split('["%s"]' % design, 1)[1].split("]),", 1)[0]
    return [(int(i, 16), int(x), int(y), int(z)) for i, x, y, z in
            re.findall(r"new\(0x([0-9A-F]+), (-?\d+), (-?\d+), (-?\d+),", block)]


def main():
    out = sys.argv[1]
    x1, y1, x2, y2 = (int(v) for v in sys.argv[2:6])
    rest = sys.argv[6:]
    vanilla = "vanilla" in rest
    if vanilla:
        folder = r"D:\UO\UltimaOnlineVanilla"
        land = U.MapFile(folder, 1).region(x1, y1, x2, y2)
        statics = U.statics_in(folder, 1, x1, y1, x2, y2)
    else:
        land = {}
        ids, zs = islands.load_land('sos')
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                land[(x, y)] = (int(ids[x, y]), int(zs[x, y]))
        sx, sy, sz, sid = islands.load_statics('sos')
        m = (sx >= x1) & (sx <= x2) & (sy >= y1) & (sy <= y2)
        statics = [(int(a), int(b), int(c), int(d)) for a, b, c, d in zip(sx[m], sy[m], sz[m], sid[m])]
    if "rows" in rest:
        rows = json.load(open(os.path.join(NOTES, "cc-P678-tools", "winter", "placement.json")))
        for r in rows:
            item = r.get("itemId") or r.get("item") or r.get("ItemId")
            if isinstance(item, str):
                item = int(item, 16)
            if item and x1 <= r["x"] <= x2 and y1 <= r["y"] <= y2:
                statics.append((r["x"], r["y"], r.get("z", 0), item))
    for a in rest:
        if "@" in a:
            design, at = a.split("@")
            ox, oy, oz = (int(v) for v in at.split(","))
            statics += [(ox + x, oy + y, oz + z, t) for t, x, y, z in parts(design)]
    im = iso.render(iso.Scene(land, statics), x1, y1, x2, y2, art=iso.Art())
    im = im.convert("RGB")
    im.thumbnail((1400, 1400))
    im.save(out, quality=82)
    print(out, im.size)


if __name__ == "__main__":
    main()
