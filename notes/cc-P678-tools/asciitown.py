r"""cc-P678: the town as characters: 'R' covered floor (inside a building), '.' open, '#' blocked, '~' water,
'S' a stock spawner or decoration tile, digits for given points.
    python -P asciitown.py x1 y1 x2 y2 [x,y ...]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import buildings, townmap, placer
a = [int(v) for v in sys.argv[1:5]]
pts = [tuple(int(v) for v in p.split(",")[:2]) for p in sys.argv[5:]]
cov, _ = buildings.find(*a)
stock = placer.stock_tiles()
print("     " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(a[0], a[2] + 1)))
for y in range(a[1], a[3] + 1):
    row = []
    for x in range(a[0], a[2] + 1):
        if (x, y) in pts:
            row.append(str(pts.index((x, y)) % 10)); continue
        k, _ = townmap.tile(x, y)
        c = {"open": ".", "blocked": "#", "water": "~", "void": " "}[k]
        if (x, y) in cov: c = "R"
        if (x, y) in stock and c != "#": c = "S"
        row.append(c)
    print("%4d " % y + "".join(row))
