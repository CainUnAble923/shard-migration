# Scan every .cs under server/customizations for literal coordinates and test them against changed blocks.
# Candidate = two consecutive decimal int literals (a, b) inside one argument list / initializer with
# 0<=a<7168 and 0<=b<4096 (Point3D/Point2D/new(...)/tuples/Rectangle2D/X=..,Y=..). Conservative on purpose:
# false candidates only add rows; a real coordinate cannot be missed unless it is computed or hex.
import os, re, json, csv
import numpy as np

ROOT = r"D:\ShatteredLegacy\server\customizations"
here = os.path.dirname(os.path.abspath(__file__))
st = json.load(open(os.path.join(here, "changed_statics.json")))
ld = json.load(open(os.path.join(here, "changed_land.json")))
BH = 4096 >> 3
changed = {f: set(st[f]["blocks"]) | set(ld[f]["blocks"]) for f in ("0", "1")}
# per-facet arrays of changed block centres for distance
cent = {f: np.array([((b // BH) * 8 + 3.5, (b % BH) * 8 + 3.5) for b in changed[f]]) for f in changed}

def blk(x, y): return (x >> 3) * BH + (y >> 3)

def dist(f, x, y):
    c = cent[f]
    return float(np.min(np.maximum(np.abs(c[:, 0] - x), np.abs(c[:, 1] - y))) - 3.5)

INT = r"-?\d+"
argre = re.compile(r"\(([^()]*)\)|\{([^{}]*)\}")
xyre = re.compile(r"\bX\s*=\s*(\d+)\s*,\s*Y\s*=\s*(\d+)")
rectre = re.compile(r"new\s+Rectangle2D\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")
rows = []
for dp, dn, fn in os.walk(ROOT):
    if "\\bin" in dp or "\\obj" in dp: continue
    for f in fn:
        if not f.endswith(".cs"): continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT)
        for ln, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
            s = line.split("//")[0]
            for m in rectre.finditer(s):
                x, y, w, h = map(int, m.groups())
                hit = {fa: any(blk(xx, yy) in changed[fa] for xx in range(x, x + w, 4) for yy in range(y, y + h, 4))
                       for fa in ("0", "1")}
                rows.append(dict(file=rel, line=ln, kind="Rectangle2D", x=x, y=y, extra=f"w{w} h{h}",
                                 hit0=hit["0"], hit1=hit["1"], d0=dist("0", x, y), d1=dist("1", x, y), text=line.strip()[:140]))
            for m in xyre.finditer(s):
                x, y = map(int, m.groups())
                if x < 7168 and y < 4096:
                    rows.append(dict(file=rel, line=ln, kind="X=,Y=", x=x, y=y, extra="",
                                     hit0=blk(x, y) in changed["0"], hit1=blk(x, y) in changed["1"],
                                     d0=dist("0", x, y), d1=dist("1", x, y), text=line.strip()[:140]))
            for m in re.finditer(r"(?<![\w.])(\d+)\s*,\s*(?:[xy]:\s*)?(\d+)(?![\w.])|x:\s*(\d+)\s*,\s*y:\s*(\d+)", s):
                g = m.groups()
                x, y = (int(g[0]), int(g[1])) if g[0] is not None else (int(g[2]), int(g[3]))
                if 16 <= x < 7168 and 16 <= y < 4096:
                    pre = s[:m.start()].rstrip()
                    if "Rectangle2D(" in pre[-14:]: continue
                    kind = "Point3D" if "Point3D(" in pre[-9:] else ("Point2D" if "Point2D(" in pre[-9:] else "pair")
                    rows.append(dict(file=rel, line=ln, kind=kind, x=x, y=y, extra="",
                                     hit0=blk(x, y) in changed["0"], hit1=blk(x, y) in changed["1"],
                                     d0=dist("0", x, y), d1=dist("1", x, y), text=line.strip()[:140]))
with open(os.path.join(here, "coords_all.csv"), "w", newline="", encoding="ascii", errors="replace") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("candidates", len(rows), "files", len(set(r["file"] for r in rows)))
print("hits Fel", sum(r["hit0"] for r in rows), "hits Tram", sum(r["hit1"] for r in rows))
for r in rows:
    if r["hit0"] or r["hit1"] or min(r["d0"], r["d1"]) < 64:
        print("NEAR/HIT", r)
from collections import defaultdict
byf = defaultdict(list)
for r in rows: byf[r["file"]].append(r)
for f, rs in sorted(byf.items()):
    print(f"{f}: n={len(rs)} x[{min(r['x'] for r in rs)}-{max(r['x'] for r in rs)}] y[{min(r['y'] for r in rs)}-{max(r['y'] for r in rs)}] "
          f"minDistFel={min(r['d0'] for r in rs):.0f} minDistTram={min(r['d1'] for r in rs):.0f}")
