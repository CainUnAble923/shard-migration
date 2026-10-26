r"""cc-P669 option (c): what lifting one SoS piece into stock Trammel costs, as mapops lines (changed land tiles + statics
added + statics removed) and bytes at the current patch's measured 19 bytes a line (trammel.mapops: 253,167 bytes,
13,186 lines). Boxes are the author's region boxes (sos-map-author-spots.md) or a box round his go-menu spot.
    python -P pieces.py -> out\pieces.csv"""
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cc-P481-tools"))
import islands, sosdiff, places
PIECES = [
    ("Valunstead (walled town, moated keep)", 419, 328, 539, 448, "box of 120 round the go-menu spot 479,388"),
    ("Fort Whitestone", 850, 1015, 930, 1095, "box of 80 round 890,1055"),
    ("Elandrim Nur Shaz", 860, 987, 920, 1052, "author region"),
    ("Castle Dunbain", 1293, 1337, 1373, 1417, "box of 80 round 1333,1377"),
    ("Fort Stormhammer", 1450, 1283, 1530, 1363, "box of 80 round 1490,1323"),
    ("Hammerhill", 1481, 959, 1622, 1068, "author region"),
    ("Kameron Kove", 1200, 2391, 1341, 2558, "author region"),
    ("Tigerclaw Fortress", 2555, 1045, 2635, 1125, "box of 80 round 2595,1085"),
    ("Khalahandra Keep (island)", 2456, 1648, 2543, 1707, "island box"),
    ("Fort Yondall", 3366, 308, 3413, 406, "author region"),
    ("Elmhaven", 1891, 3135, 2049, 3263, "author region"),
    ("Kettleburg", 427, 2316, 733, 2618, "author region"),
    ("Nujelm desert landmass (whole)", 3500, 1000, 5100, 2150, "change map"),
]
ls, zs = islands.load_land("trammel"); lo, zo = islands.load_land("sos")
_, ks, _, _, _, _ = islands.build("trammel"); _, ko, _, _, _, _ = islands.build("sos")
k1, k2 = sosdiff.static_keys("trammel"), sosdiff.static_keys("sos")
rows = []
for name, x1, y1, x2, y2, src in PIECES:
    d = places.stats(ls, zs, lo, zo, k1, k2, ks, ko, x1, y1, x2, y2)
    lines = d["landChanged"] + d["onlySos"] + d["onlyStock"]
    rows.append([name, "%d,%d-%d,%d" % (x1, y1, x2, y2), src, d["landChanged"], d["onlySos"], d["onlyStock"], lines, round(lines * 19.2 / 1e6, 2)])
    print(rows[-1])
with open(os.path.join(sosdiff.OUT, "pieces.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["piece", "box", "boxFrom", "landTiles", "staticsAdded", "staticsRemoved", "mapopsLines", "mapopsMB"]); w.writerows(rows)
