r"""cc-P678 (SoS swap S7): every coordinate on the Haven island in our code, graded against Siege of Sosaria 3.0.

P669's geo.py counted points only in Point3D/Point2D/Rectangle calls, tuples and "go" strings; it missed most of our layout
tables (ClusterFNewHavenServicesSeeder.cs holds 131 Haven literals, P669 counted 1). This reads every "x, y" pair of
integers in the Haven island's box (pinned regions.json "Haven Island": x 3314-3813, y 2345-3094) in our server code,
patches and bot, outside comments, and grades each with P669's Grader (its own tile and the 8 round it):
    unchanged   land, Z and statics the same on both maps
    moves       something near changed, the tile itself still dry, open and within 5 Z
    rework      water or void, under an impassable static, or Z moved more than 5
    python -P havenpoints.py   -> out\haven-points.csv (file, line, x, y, grade, the line), out\haven-files.csv
Read only.
"""
import collections
import csv
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(os.path.dirname(HERE), "cc-P669-tools")
sys.path.insert(0, TOOLS)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cc-P481-tools"))
import geo  # noqa: E402

SL = r"D:\UO\golems\Iron\ShatteredLegacy"
OUT = os.path.join(HERE, "out")
BOX = (3314, 2345, 3813, 3094)
PAIR = re.compile(r"(?<![\d.])(3\d{3})\s*,\s*(2\d{3})(?![\d.])")


def files():
    return sorted(glob.glob(os.path.join(SL, "server", "customizations", "**", "*.cs"), recursive=True)
                  + glob.glob(os.path.join(SL, "server", "patches", "**", "*.patch"), recursive=True)
                  + glob.glob(os.path.join(SL, "server", "patches", "**", "*.cs"), recursive=True)
                  + glob.glob(os.path.join(SL, "server", "tests", "**", "*.cs"), recursive=True)
                  + glob.glob(os.path.join(SL, "tools", "playtest-bot", "uobot", "*.py")))


def points():
    out = []
    for f in files():
        rel = os.path.relpath(f, SL).replace("\\", "/")
        for i, line in enumerate(open(f, encoding="utf-8", errors="replace").read().splitlines(), 1):
            code = line.split("//")[0] if not rel.endswith(".py") else line.split("#")[0]
            for m in PAIR.finditer(code):
                x, y = int(m.group(1)), int(m.group(2))
                if BOX[0] <= x <= BOX[2] and BOX[1] <= y <= BOX[3]:
                    out.append((rel, i, x, y, line.strip()[:160]))
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    pts = points()
    g = geo.Grader()
    rows, per = [], collections.defaultdict(collections.Counter)
    for rel, i, x, y, line in pts:
        k = g.grade(x, y)
        rows.append((rel, i, x, y, k, line))
        per[rel][k] += 1
    with open(os.path.join(OUT, "haven-points.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "line", "x", "y", "grade", "text"])
        w.writerows(rows)
    with open(os.path.join(OUT, "haven-files.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "points", "unchanged", "moves", "rework"])
        for rel in sorted(per, key=lambda r: -sum(per[r].values())):
            c = per[rel]
            w.writerow([rel, sum(c.values()), c["unchanged"], c["moves"], c["rework"]])
    tot = collections.Counter(r[4] for r in rows)
    print(len(rows), "points in", len(per), "files:", dict(tot))


if __name__ == "__main__":
    main()
