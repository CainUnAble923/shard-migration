"""cc-P724: renders an isle area from the built map files (isometric, scripts/mapbuild/isorender.py) with addons placed
on it, to choose spots and variants before any server work. Usage:
    python -P plan_render.py <map folder> <out.png> x1 y1 x2 y2 [<path.cs or ids:..>@x,y,z ...]
Each addon is put with its centre at x,y and its components' z offsets added to z. Prints, per addon, the land under
every component (name, z) so a piece over water or a cliff shows."""
import os
import sys

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
sys.path.insert(0, HERE)
from mapbuild import isorender as iso  # noqa: E402
from mapbuild import uofiles  # noqa: E402
from render_addons import components  # noqa: E402


def main():
    folder, out = sys.argv[1], sys.argv[2]
    x1, y1, x2, y2 = (int(v) for v in sys.argv[3:7])
    scene = iso.Scene.from_map(folder, 1, x1, y1, x2, y2)
    land_td = uofiles.read_tiledata()[0]
    mf = uofiles.MapFile(folder, 1)
    for arg in sys.argv[7:]:
        path, at = arg.rsplit("@", 1)
        cx, cy, cz = (int(v) for v in at.split(","))
        kinds = {}
        for tid, dx, dy, dz in components(path):
            scene.statics.append((cx + dx, cy + dy, cz + dz, tid))
            t, z = mf.get(cx + dx, cy + dy)
            k = "%s z%d" % (land_td[t][2], z)
            kinds[k] = kinds.get(k, 0) + 1
        print(os.path.basename(path), "at", (cx, cy, cz), "land under components:", kinds)
    im = iso.render(scene, x1, y1, x2, y2, art=iso.Art())
    im.save(out)
    print("saved", out, im.size)


if __name__ == "__main__":
    main()
