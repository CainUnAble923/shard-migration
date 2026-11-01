"""cc-P742: renders the vision chamber's piece table (TutorialVisionChamberLayout.cs) full size with isorender, on the void
land (0x0244 at Z 0) it stands on in site A, as the client draws it from the default camera. Optional extra statics
show a scene beat (the Gem on the pedestal, or the shards).
Usage: python -P render_chamber.py <TutorialVisionChamberLayout.cs> <out.png> [gem|shards]"""
import os
import re
import sys

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from mapbuild import isorender as iso  # noqa: E402

src, out = sys.argv[1], sys.argv[2]
beat = sys.argv[3] if len(sys.argv) > 3 else ""
rows = re.findall(r"\[\s*(0x[0-9A-Fa-f]+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*\]", open(src, encoding="utf-8").read())
statics = [(int(x), int(y), int(z), int(t, 16)) for t, x, y, z in rows]
pedestal_top = 0 + 6  # 0x1223's height is read by the server from tiledata; 6 is close enough for a picture
if beat == "gem":
    statics.append((4, 4, pedestal_top, 0x1EA7))
elif beat == "shards":
    statics += [(4, 4, pedestal_top, 0x5738), (3, 5, 0, 0x5738), (5, 3, 0, 0x5738), (5, 5, 0, 0x5738), (3, 4, 0, 0x0F61)]
land = {(x, y): (0x0244, 0) for x in range(-4, 14) for y in range(-4, 14)}
im = iso.render(iso.Scene(land, statics), -3, -3, 11, 11, art=iso.Art())
im.save(out)
print(out, len(statics), "statics", im.size)
