"""cc-P687: put the dressed patch in the code copy and add P687's line to the map's SOURCE.txt (once).
Usage: python -I install_patch.py <dressed trammel.mapops> <code copy>"""
import os, shutil, sys

src, code = sys.argv[1], sys.argv[2]
d = os.path.join(code, "player-package", "vendor", "shattered-legacy-map")
shutil.copyfile(src, os.path.join(d, "trammel.mapops"))
p = os.path.join(d, "SOURCE.txt")
s = open(p, encoding="utf-8", newline="").read()
I = " " * 17
anchor = I + "(palms, banana, o'hii, OSI's jungle trees whole, ferns, pampas). Same 875 blocks; 4,618 S+ lines.\n"
assert s.count(anchor) == 1
if "cc-P687" not in s:
    s = s.replace(anchor, anchor
                  + I + "cc-P687, 2026-10-29 (SoS swap S14): the author's cliff seams dressed near where players go: on\n"
                  + I + "every bare grass, dirt, sand, forest, jungle or snow tile within 40 of a town, road or moongate\n"
                  + I + "that stands 20 or more above its south or east neighbour (a new seam: not the same one on stock),\n"
                  + I + "OSI's tall grey boulders (0x1357-0x135C) at the low side's Z, one more each 20 Z, each under the\n"
                  + I + "tile's walking Z (notes/cc-P687-tools/dress.py). S14's five closure boxes are fenced instead.\n"
                  + I + "8,389 S+ lines on 6,143 faces.\n")
open(p, "w", encoding="utf-8", newline="").write(s)
print("installed", os.path.getsize(os.path.join(d, "trammel.mapops")), "bytes")
