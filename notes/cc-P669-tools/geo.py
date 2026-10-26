r"""cc-P669 part 2: every place our server, package and bot assume stock Trammel geography, graded against SoS 3.0.

Read only. Sources (counted from the files, never from a description):
  stock   pinned ModernUO Data: Spawns/{post-uoml,shared}/trammel/*.json, Decoration/{Britannia,Trammel}/*.cfg,
          teleporters.json (Trammel ends), treasure.cfg, regions.json (Trammel), PublicMoongate.cs PMList.Trammel
  ours    every coordinate literal in ShatteredLegacy server/customizations and server/patches (*.cs, *.patch) and the
          play-test bot (tools/playtest-bot/uobot/*.py): new Point3D/Point2D(x, y[, z]), new Rectangle2D/3D, bare
          (x, y, z) tuples, "go x y" strings; the file decides the map (it names Trammel, Felucca, both, or neither)
  patch   player-package/vendor/shattered-legacy-map/trammel.mapops: the blocks it writes

Each point is graded on its own tile and the 8 tiles round it:
  unchanged   land id and Z and the statics on the point's 3 x 3 are the same in both maps
  moves       something within that 3 x 3 changed but the point is still dry, not void and not under an impassable
              static, within 5 Z of stock: the content may stay, but must be looked at in game
  rework      the point is now water or void, or under an impassable static, or its land Z moved more than 5
    python -P geo.py collect   -> out\geo-points.csv, out\geo-summary.csv, out\geo-files.csv
"""
import collections
import csv
import glob
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cc-P481-tools"))
import islands  # noqa: E402
import sosdiff  # noqa: E402

PIN = r"D:\UO\ModernUO-pinned"
SL = r"D:\UO\golems\Iron\ShatteredLegacy"
OUT = sosdiff.OUT
W, H = sosdiff.W, sosdiff.H


class Grader:
    def __init__(self, base="trammel"):
        print("loading both maps", flush=True)
        self.ls, self.zs = islands.load_land(base)
        self.lo, self.zo = islands.load_land("sos")
        _, self.ks, _, _, _, _ = islands.build(base)
        _, self.ko, _, _, _, _ = islands.build("sos")
        ks, ko = sosdiff.static_keys(base), sosdiff.static_keys("sos")
        diff = np.concatenate([np.setdiff1d(ks, ko, assume_unique=True), np.setdiff1d(ko, ks, assume_unique=True)])
        self.tile_static = np.zeros((W, H), dtype=bool)
        blk, cell = diff >> 30, (diff >> 24) & 63
        self.tile_static[(blk // sosdiff.BH) * 8 + cell // 8, (blk % sosdiff.BH) * 8 + cell % 8] = True
        lf, itf = islands.flags()
        sx, sy, sz, sid = islands.load_statics("sos")
        f = itf[np.minimum(sid, len(itf) - 1)]
        imp = ((f & np.uint64(0x40)) != 0) & ((f & np.uint64(0x200)) == 0)
        self.blocked = np.zeros((W, H), dtype=bool)
        self.blocked[sx[imp], sy[imp]] = True
        self.changed = (self.ls != self.lo) | (self.zs != self.zo) | self.tile_static

    def grade(self, x, y):
        if not (0 <= x < W and 0 <= y < H):
            return "off map"
        x1, x2, y1, y2 = max(0, x - 1), min(W, x + 2), max(0, y - 1), min(H, y + 2)
        if not self.changed[x1:x2, y1:y2].any():
            return "unchanged"
        if self.ko[x, y] != 0 or self.blocked[x, y] or abs(int(self.zo[x, y]) - int(self.zs[x, y])) > 5:
            return "rework"
        return "moves"


def stock_points(facet="trammel"):
    Facet = facet.capitalize()
    pts = []
    D = os.path.join(PIN, "Distribution", "Data")
    for f in sorted(glob.glob(os.path.join(D, "Spawns", "*", facet, "*.json"))):
        rel = os.path.relpath(f, D).replace("\\", "/")
        for s in json.load(open(f, encoding="utf-8")):
            loc = s.get("location")
            if loc and s.get("map", Facet) == Facet:
                pts.append(("stock spawner", rel, s.get("name", ""), loc[0], loc[1]))
    for f in sorted(glob.glob(os.path.join(D, "Decoration", "Britannia", "*.cfg")) + glob.glob(os.path.join(D, "Decoration", Facet, "*.cfg"))):
        rel = os.path.relpath(f, D).replace("\\", "/")
        item = ""
        for line in open(f, encoding="utf-8", errors="replace"):
            line = line.strip()
            m = re.match(r"^(-?\d+) (-?\d+) (-?\d+)", line)
            if m:
                pts.append(("stock decoration", rel, item, int(m.group(1)), int(m.group(2))))
            elif line and not line.startswith("#"):
                item = line.split(" ")[0] + " " + (line.split(" ")[1] if len(line.split(" ")) > 1 else "")
    for t in json.load(open(os.path.join(D, "teleporters.json"))):
        for end in ("src", "dst"):
            if t[end]["map"] == Facet:
                pts.append(("stock teleporter", "teleporters.json", end, t[end]["loc"][0], t[end]["loc"][1]))
    for line in open(os.path.join(D, "treasure.cfg")):
        m = re.match(r"^(\d+) (\d+)\s*$", line.strip())
        if m:
            pts.append(("stock treasure map spot", "treasure.cfg", "", int(m.group(1)), int(m.group(2))))
    src = open(os.path.join(PIN, "Projects", "UOContent", "Items", "Misc", "PublicMoongate.cs")).read()
    nxt = {"Trammel": "PMList Felucca", "Felucca": "PMList Ilshenar"}[Facet]
    tram = src[src.index("PMList " + Facet):src.index(nxt)]
    for m in re.finditer(r"new Point3D\((\d+), (\d+),.*?// (.*)", tram):
        pts.append(("stock moongate", "PublicMoongate.cs PMList." + Facet, m.group(3).strip(), int(m.group(1)), int(m.group(2))))
    for r in json.load(open(os.path.join(D, "regions.json"))):
        if r.get("Map") == Facet:
            for a in r.get("Area", []):
                pts.append(("stock region (centre)", r.get("$type", ""), r.get("Name", ""), (a["x1"] + a["x2"]) // 2, (a["y1"] + a["y2"]) // 2))
    return pts


PAT = [
    re.compile(r"new Point3D\(\s*(\d{1,4})\s*,\s*(\d{1,4})\s*,"),
    re.compile(r"new Point2D\(\s*(\d{1,4})\s*,\s*(\d{1,4})\s*\)"),
    re.compile(r"new Rectangle[23]D\(\s*(\d{1,4})\s*,\s*(\d{1,4})\s*,"),
    re.compile(r"\(\s*(\d{3,4})\s*,\s*(\d{3,4})\s*,\s*-?\d{1,3}\s*\)"),
    re.compile(r"\bgo (\d{3,4}) (\d{3,4})"),
]
OTHER = re.compile(r"Map\.(Ilshenar|Malas|Tokuno|TerMur)|\b(Ilshenar|Malas|Tokuno|TerMur)\b")


def our_points():
    files = (glob.glob(os.path.join(SL, "server", "customizations", "**", "*.cs"), recursive=True)
             + glob.glob(os.path.join(SL, "server", "patches", "**", "*.patch"), recursive=True)
             + glob.glob(os.path.join(SL, "server", "patches", "**", "*.cs"), recursive=True)
             + glob.glob(os.path.join(SL, "tools", "playtest-bot", "uobot", "*.py")))
    pts, per_file = [], {}
    for f in files:
        text = open(f, encoding="utf-8", errors="replace").read()
        rel = os.path.relpath(f, SL).replace("\\", "/")
        t, fe, other = "Trammel" in text, "Felucca" in text, bool(OTHER.search(text))
        maps = "both" if t and fe else "Trammel" if t else "Felucca" if fe else "other facet" if other else "unnamed"
        n = 0
        for i, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith(("//", "///", "#")) and "go " not in line:
                continue
            for p in PAT:
                for m in p.finditer(line):
                    x, y = int(m.group(1)), int(m.group(2))
                    if x < 8 and y < 8:
                        continue
                    pts.append(("ours", rel + ":" + str(i), maps, x, y))
                    n += 1
        if n:
            per_file[rel] = (maps, n)
    return pts, per_file


def mapops_blocks():
    """The (bx, by) blocks trammel.mapops writes. Format per scripts/mapbuild/mapops.py."""
    p = os.path.join(SL, "player-package", "vendor", "shattered-legacy-map", "trammel.mapops")
    return p, os.path.getsize(p)


def collect():
    g = Grader()
    rows = []
    for cat, src, name, x, y in stock_points():
        rows.append([cat, src, name, x, y, g.grade(x, y)])
    ours, per_file = our_points()
    for cat, src, maps, x, y in ours:
        # A literal on another facet's file, or past Trammel's surface on a file that names no facet, is not Trammel's.
        if maps in ("other facet",):
            continue
        rows.append(["ours (" + maps + ")", src, "", x, y, g.grade(x, y)])
    with open(os.path.join(OUT, "geo-points.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "source", "name", "x", "y", "grade"])
        w.writerows(rows)
    summ = collections.defaultdict(collections.Counter)
    for r in rows:
        key = r[0] if not r[0].startswith("ours") else r[0]
        summ[key][r[5]] += 1
    with open(os.path.join(OUT, "geo-summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "points", "unchanged", "moves", "rework", "off map"])
        for k, c in summ.items():
            w.writerow([k, sum(c.values()), c["unchanged"], c["moves"], c["rework"], c["off map"]])
            print(k, sum(c.values()), dict(c))
    # Per source file (ours) and per stock file: how many points, and the worst grade.
    byfile = collections.defaultdict(collections.Counter)
    for r in rows:
        src = r[1].split(":")[0]
        byfile[(r[0], src)][r[5]] += 1
    with open(os.path.join(OUT, "geo-files.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "file", "points", "unchanged", "moves", "rework", "verdict"])
        for (cat, src), c in sorted(byfile.items()):
            verdict = "needs rework" if c["rework"] else "moves" if c["moves"] else "unchanged"
            w.writerow([cat, src, sum(c.values()), c["unchanged"], c["moves"], c["rework"], verdict])
    print("files:", collections.Counter(("needs rework" if c["rework"] else "moves" if c["moves"] else "unchanged", cat.split(" (")[0]) for (cat, _), c in byfile.items()))
    p, size = mapops_blocks()
    print("mapops", p, size, "bytes")


if __name__ == "__main__":
    if sys.argv[1] == "collect":
        collect()
