"""cc-P691: the review renders, from the scratch build (SoS + the new patch): a top-down overview of site A and
isometric close-ups. python -P renders.py <edited folder> <out folder>"""
import os, sys
sys.path.insert(0, r"D:/UO/golems/Iron/shard-migration/scripts")
from mapbuild import uofiles, isorender
import numpy as np
from PIL import Image, ImageDraw

F, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# 1. overview: site A, land kind and statics, one pixel a tile, x2
x1, y1, x2, y2 = 6160, 3744, 7167, 4095
ids, zs = uofiles.load_land(F, 1)
sub = ids[x1:x2 + 1, y1:y2 + 1].T
img = np.zeros(sub.shape + (3,), np.uint8)
img[(sub >= 0x1fa) & (sub <= 0x1ff)] = (60, 40, 30)
water = (sub >= 0xa8) & (sub <= 0xab)
img[water] = (30, 60, 120)
other = ~((sub >= 0x1fa) & (sub <= 0x1ff)) & (sub != 0x244) & (sub != 0x245) & ~water
img[other] = (150, 150, 120)
for x, y, z, t in uofiles.statics_in(F, 1, x1, y1, x2, y2):
    img[y - y1, x - x1] = (200, 60, 60)
im = Image.fromarray(img).resize(((x2 - x1 + 1) * 2, (y2 - y1 + 1) * 2), Image.NEAREST)
d = ImageDraw.Draw(im)
for (a, b, c, e, col) in [(6216, 3804, 6512, 4052, (255, 255, 0)), (6904, 3795, 7146, 4067, (255, 255, 0)), (6594, 3905, 6865, 4049, (0, 255, 255))]:
    d.rectangle([(a - x1) * 2, (b - y1) * 2, (c - x1) * 2 + 1, (e - y1) * 2 + 1], outline=col)
d.text((10, 10), "site A (x 6160-7167, y 3744-4095): yellow = Blackthorn's two pieces, cyan = the isle's box", fill=(255, 255, 255))
im.convert('RGB').save(os.path.join(OUT, 'overview-site-a.jpg'), quality=85)


def iso(name, a, b, c, e, zmax=None, extra=(), side=1600):
    sc = isorender.Scene.from_map(F, 1, a, b, c, e)
    if zmax is not None:
        sc.statics = [s for s in sc.statics if s[2] <= zmax]
    sc.statics = list(sc.statics) + list(extra)
    im = isorender.render(sc, a, b, c, e)
    im.thumbnail((side, side))
    im.convert('RGB').save(os.path.join(OUT, name + '.jpg'), quality=85)
    print(name, im.size)


iso('castle-storeroom-hatch', 1508, 1426, 1526, 1442, zmax=34, extra=[(1519, 1437, 14, 0x3E65)])
iso('landing-hall', 6428, 3905, 6488, 3950)
iso('join-dungeon-side', 6385, 3826, 6420, 3852)
iso('join-invasion-side', 6995, 4045, 7040, 4068)
iso('invasion-room-north', 6985, 3810, 7040, 3860)
iso('dungeon-south', 6400, 3990, 6510, 4052, side=1800)
