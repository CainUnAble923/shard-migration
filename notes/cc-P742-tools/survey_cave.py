"""cc-P742: where OSI's stock dungeons (Trammel, x 5120+) use the cave wall statics 0x025C-0x0280 and the cave floor
statics 0x053B-0x0553: per 64x64 area, a count, so a small room can be rendered and copied in spirit.
Usage: python -P survey_cave.py [client folder]"""
import collections
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from mapbuild import uofiles  # noqa: E402

folder = sys.argv[1] if len(sys.argv) > 1 else r"D:\UO\tool-trials\client-data-copy"
walls = set(range(0x025C, 0x0281))
floors = set(range(0x053B, 0x0554))
st = uofiles.statics_in(folder, 1, 5120, 0, 6143, 2559)
area = collections.Counter()
ids = collections.Counter()
for s in st:
    x, y, z, tid = s[0], s[1], s[2], s[3]
    if tid in walls or tid in floors:
        area[(x // 64 * 64, y // 64 * 64, "wall" if tid in walls else "floor")] += 1
        ids[tid] += 1
print("statics read:", len(st))
for k, v in area.most_common(15):
    print(k, v)
print("ids:", sorted((hex(k), v) for k, v in ids.items()))
