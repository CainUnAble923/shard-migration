r"""cc-P678 office/alembic: list the statics of a box of SoS, per tile: id, z, height, flags (I impassable,
S surface, D door, W wall, B background) and tiledata name.
    python -P statics.py x1 y1 x2 y2
Read only.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "cc-P481-tools"))
import townmap, islands  # noqa: E402
from islands import uofiles  # noqa: E402

items = uofiles.read_tiledata(islands.VANILLA)[1]
x1, y1, x2, y2 = [int(v) for v in sys.argv[1:5]]
c = townmap.load()
m = (c["sx"] >= x1) & (c["sx"] <= x2) & (c["sy"] >= y1) & (c["sy"] <= y2)
rows = sorted(zip(c["sy"][m].tolist(), c["sx"][m].tolist(), c["sz"][m].tolist(), c["sid"][m].tolist()))
for y, x, z, i in rows:
    it = items[i] if i < len(items) else {"name": "?", "flags": 0, "height": 0}
    f = it["flags"]
    fl = "".join(ch for b, ch in ((0x40, "I"), (0x200, "S"), (0x20000000, "D"), (0x10, "W"), (0x1, "B")) if f & b)
    print(x, y, z, "0x%04X" % i, "h%d" % it.get("height", 0), fl, it["name"])
