"""cc-P803 renders: python -P rend.py <folder> x1 y1 x2 y2 cutz out.png [extras.json]
cutz: drop statics with z >= cutz (0 = keep all). extras: [[id,x,y,z],...] server items drawn in."""
import os, sys, json
sys.path.insert(0, r"D:/UO/golems/Iron/shard-migration/scripts")
os.environ.setdefault("MAPBUILD_CLIENT", r"D:/UO/tool-trials/client-data-copy")
from mapbuild import isorender as R
folder = sys.argv[1]; x1, y1, x2, y2, cutz = map(int, sys.argv[2:7]); out = sys.argv[7]
ex = json.load(open(sys.argv[8])) if len(sys.argv) > 8 else []
sc = R.Scene.from_map(folder, 1, x1, y1, x2, y2)
if cutz:
    sc.statics = [s for s in sc.statics if s[2] < cutz]
for e in ex:
    i, x, y, z = [int(v, 16) if isinstance(v, str) else v for v in e[:4]]
    sc.statics.append((x, y, z, i))
im = R.render(sc, x1, y1, x2, y2)
im = im.convert("RGB")
if out.endswith(".jpg"):
    im.save(out, quality=88)
else:
    im.save(out)
print(out, im.size)
