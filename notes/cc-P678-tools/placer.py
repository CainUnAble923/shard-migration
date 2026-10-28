r"""cc-P678: pick standing tiles for our NPCs inside a SoS Haven building.
    python -P placer.py x1 y1 x2 y2 count [near_x near_y]
Picks covered, open tiles of the building in the box (buildings.py's groups) that are not on its edge (all four
neighbours open or blocked inside the box), not a stock spawner's tile (pinned uoml/post-uoml/shared Trammel), not a
stock Haven decoration tile (pinned Decoration/Trammel *.cfg), not a HavenSpots spot, and at least 2 tiles from each
other. Nearest to (near_x, near_y) first (default: the building's north-west corner, the back wall in the client).
Prints x y z per pick. Read only.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import buildings  # noqa: E402
import townmap  # noqa: E402

PINNED = "D:/UO/ModernUO-pinned/Distribution/Data"
SPOTS = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/HavenSpots.cs"


def stock_tiles():
    out = set()
    for f in glob.glob(PINNED + "/Spawns/*/trammel/*.json"):
        for s in json.load(open(f)):
            loc = s["location"]
            out.add((loc[0], loc[1]))
    for f in glob.glob(PINNED + "/Decoration/Trammel/*.cfg"):
        for line in open(f, errors="replace"):
            m = re.match(r"^\s*(\d+)\s+(\d+)\s+(-?\d+)", line)
            if m:
                out.add((int(m.group(1)), int(m.group(2))))
    for m in re.finditer(r"new\((\d{4}), (\d{4}), (-?\d+)\)", open(SPOTS).read()):
        out.add((int(m.group(1)), int(m.group(2))))
    return out


def pick(x1, y1, x2, y2, count, near=None, avoid=(), yard=False):
    """yard: an open-air yard, so any open tile in the box counts, covered or not."""
    cov, groups = buildings.find(x1, y1, x2, y2)
    if yard:
        cov = {(x, y): townmap.tile(x, y)[1] for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)
               if townmap.tile(x, y)[0] == "open"}
    stock = stock_tiles() | set(avoid)
    inside = [p for p in cov
              if all(((n in cov) or townmap.tile(*n)[0] == "blocked") for n in
                     ((p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)))]
    near = near or (x1, y1)
    inside.sort(key=lambda p: ((p[0] - near[0]) ** 2 + (p[1] - near[1]) ** 2, p))
    got = []
    for p in inside:
        if p in stock or any(abs(p[0] - q[0]) < 2 and abs(p[1] - q[1]) < 2 for q in got):
            continue
        got.append(p)
        if len(got) == count:
            break
    return [(x, y, cov[(x, y)]) for x, y in got]


if __name__ == "__main__":
    a = [int(v) for v in sys.argv[1:]]
    near = (a[5], a[6]) if len(a) > 6 else None
    for p in pick(*a[:4], a[4], near):
        print(*p)
