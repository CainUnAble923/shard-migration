r"""cc-P678: door statics (tiledata Door flag 0x20000000) in a box of SoS, with their ids and Z.
    python -P doors.py x1 y1 x2 y2
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import townmap
x1, y1, x2, y2 = [int(v) for v in sys.argv[1:5]]
c = townmap.load()
m = (c["sx"] >= x1) & (c["sx"] <= x2) & (c["sy"] >= y1) & (c["sy"] <= y2)
f = c["itf"][np.minimum(c["sid"][m], len(c["itf"]) - 1)]
d = (f & np.uint64(0x20000000)) != 0
for x, y, z, i in zip(c["sx"][m][d], c["sy"][m][d], c["sz"][m][d], c["sid"][m][d]):
    print(int(x), int(y), int(z), hex(int(i)))
