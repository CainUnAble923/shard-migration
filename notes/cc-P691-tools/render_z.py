"""isorender of a map rect with statics capped at a Z (to see a floor under the roofs).
    python -P render_z.py <folder> x1 y1 x2 y2 zmax out.(png|jpg) [maxside]"""
import os, sys
sys.path.insert(0, r"D:/UO/golems/Iron/shard-migration/scripts")
from mapbuild import isorender
from PIL import Image
folder, x1, y1, x2, y2, zmax, out = sys.argv[1], *map(int, sys.argv[2:7]), sys.argv[7]
side = int(sys.argv[8]) if len(sys.argv) > 8 else 1600
sc = isorender.Scene.from_map(folder, 1, x1, y1, x2, y2)
sc.statics = [s for s in sc.statics if s[2] <= zmax]
img = isorender.render(sc, x1, y1, x2, y2)
img.thumbnail((side, side))
img.convert('RGB').save(out, quality=85)
print(out, img.size)
