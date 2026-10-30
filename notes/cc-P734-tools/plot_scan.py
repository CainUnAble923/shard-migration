"""cc-P734: find an empty, flat test plot for the practice builds. Renders a top-down picture of a region (land by kind,
statics on top) and lists the empty flat rectangles of a given size (one land Z, no statics, no water), with how far
the nearest water is (the dock needs a shore).
Usage: python -P plot_scan.py <map folder> <facet> x1 y1 x2 y2 <out.png> [w h]"""
import os
import sys

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from mapbuild import uofiles  # noqa: E402
from PIL import Image  # noqa: E402

folder, fi = sys.argv[1], int(sys.argv[2])
x1, y1, x2, y2 = (int(v) for v in sys.argv[3:7])
out = sys.argv[7]
W, H = (int(sys.argv[8]), int(sys.argv[9])) if len(sys.argv) > 9 else (40, 30)
land_td, items = uofiles.read_tiledata()
mf = uofiles.MapFile(folder, fi)
land = mf.region(x1, y1, x2, y2)
statics = uofiles.statics_in(folder, fi, x1, y1, x2, y2)
occupied = {(s[0], s[1]) for s in statics}


def lname(t):
    return land_td[t][2].lower() if t < len(land_td) else ''


def colour(t):
    n = lname(t)
    if 'water' in n:
        return (40, 70, 160)
    if 'sand' in n:
        return (214, 196, 140)
    if 'grass' in n or 'forest' in n or 'jungle' in n:
        return (80, 140, 60)
    if 'dirt' in n or 'cobble' in n or 'road' in n or 'path' in n:
        return (140, 105, 70)
    if 'rock' in n or 'mountain' in n or 'cave' in n:
        return (110, 110, 110)
    return (30, 30, 30)


img = Image.new('RGB', (x2 - x1 + 1, y2 - y1 + 1))
water = set()
for (x, y), (t, z) in land.items():
    if x1 <= x <= x2 and y1 <= y <= y2:
        img.putpixel((x - x1, y - y1), colour(t))
        if 'water' in lname(t):
            water.add((x, y))
for x, y, z, t in statics:
    if x1 <= x <= x2 and y1 <= y <= y2:
        n = items[t]['name'].lower()
        if 'water' in n:
            water.add((x, y))
            img.putpixel((x - x1, y - y1), (40, 70, 160))
        else:
            img.putpixel((x - x1, y - y1), (20, 60, 20) if 'tree' in n or 'leaves' in n else (230, 230, 230))
img.resize((img.width * 3, img.height * 3), Image.NEAREST).save(out)

found = 0
for py in range(y1, y2 - H + 1, 5):
    for px in range(x1, x2 - W + 1, 5):
        zs = set()
        ok = True
        for y in range(py, py + H):
            for x in range(px, px + W):
                t, z = land.get((x, y), (0, 0))
                if (x, y) in occupied or (x, y) in water or 'grass' not in lname(t):
                    ok = False
                    break
                zs.add(z)
            if not ok:
                break
        if ok and max(zs) - min(zs) <= 1:
            dist = min((abs(wx - px - W // 2) + abs(wy - py - H // 2) for wx, wy in water), default=-1)
            print('plot %d,%d %dx%d land z %d..%d, water %s tiles from its centre' % (px, py, W, H, min(zs), max(zs), dist))
            found += 1
print('%d plots; picture %s' % (found, out))
