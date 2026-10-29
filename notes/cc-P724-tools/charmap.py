"""cc-P724: a character map of land kinds and statics (# impassable, capital: passable static) with land z for a
rect. Usage: python -P charmap.py x1 y1 x2 y2 [z]"""
import os, sys
os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from mapbuild import uofiles
M = r"D:\UO\golems\Iron\p731-proof\tazuo\uo-override"
x1, y1, x2, y2 = (int(v) for v in sys.argv[1:5])
showz = len(sys.argv) > 5
mf = uofiles.MapFile(M, 1); land, items = uofiles.read_tiledata()
st = {}
for x, y, z, t in uofiles.statics_in(M, 1, x1, y1, x2, y2): st.setdefault((x, y), []).append((z, t))
print("      " + "".join(("%4d" if showz else "%d") % (x % (100 if showz else 10)) for x in range(x1, x2 + 1)))
for y in range(y1, y2 + 1):
    r = ""
    for x in range(x1, x2 + 1):
        t, z = mf.get(x, y); n = land[t][2]
        c = {'stone': 's', 'grass': '.', 'water': '~', 'sand': ':', 'dirt': 'd'}.get(n.split()[0] if n else '', '?')
        if (x, y) in st:
            c = '#' if any(items[i]['flags'] & uofiles.IMPASSABLE for _, i in st[(x, y)]) else c.upper()
            z = max(zz for zz, _ in st[(x, y)])
        r += ("%s%3d" % (c, z)) if showz else c
    print(y, r)
