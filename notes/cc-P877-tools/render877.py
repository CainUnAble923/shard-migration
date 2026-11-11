"""cc-P877 (P858's render858.py, cut down): renders main's New Haven square (the Siege of Sosaria land and statics, P481's
islands loader) with the two test fountains the proof walk staged on the private proof shard's world copy: the Fountain of
Youth at 3651,2600,0 (refused by [VBuild statify) and the stone fountain at 3655,2605,0 (frozen, then undone). Both
use pinned's StoneFountainAddon pieces and offsets. Nothing here is placed in a shipped world, seeder or map file.

    python -P render877.py <out.jpg> [x1 y1 x2 y2]

Hues are not drawn (isorender draws no hues), so the Fountain of Youth's hue does not show.
"""
import os
import sys

NOTES = r"D:\UO\golems\Iron\shard-migration\notes"
os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\scripts")
import islands  # noqa: E402
from mapbuild import isorender as iso  # noqa: E402

OFFSETS = [(-2, 1), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (1, -2), (0, -2), (0, -1), (0, 0), (-1, 0), (-2, 0),
           (-2, -1), (-1, -1), (-1, -2)]
YOUTH = (3651, 2600, 0)
STONE = (3655, 2605, 0)


def fountain(origin):
    ox, oy, oz = origin
    parts = [(ox + dx, oy + dy, oz, 0x1731 + i) for i, (dx, dy) in enumerate(OFFSETS)]
    parts.append((ox - 2, oy - 2, oz, 0x1741))
    return parts


def main():
    out = sys.argv[1]
    x1, y1, x2, y2 = (int(v) for v in sys.argv[2:6]) if len(sys.argv) >= 6 else (3640, 2588, 3668, 2614)
    land = {}
    ids, zs = islands.load_land('sos')
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            land[(x, y)] = (int(ids[x, y]), int(zs[x, y]))
    sx, sy, sz, sid = islands.load_statics('sos')
    m = (sx >= x1) & (sx <= x2) & (sy >= y1) & (sy <= y2)
    statics = [(int(a), int(b), int(c), int(d)) for a, b, c, d in zip(sx[m], sy[m], sz[m], sid[m])]
    for x, y, z, t in fountain(YOUTH) + fountain(STONE):
        print("placed %04X at %d,%d,%d (land z %d)" % (t, x, y, z, land[(x, y)][1]))
    statics += fountain(YOUTH) + fountain(STONE)
    im = iso.render(iso.Scene(land, statics), x1, y1, x2, y2, art=iso.Art())
    im = im.convert("RGB")
    im.thumbnail((1400, 1400))
    im.save(out, quality=82)
    print(out, im.size)


if __name__ == "__main__":
    main()
