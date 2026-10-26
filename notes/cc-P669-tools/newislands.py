r"""cc-P669: islands of SoS 3.0 that are new (under 20 percent of their box's SoS-dry tiles were dry in stock Trammel).
Reads P481's island surveys (cc-P481-tools\scratch\{sos,trammel}-islands.csv, islands.py survey --min 400).
    python -P newislands.py -> out\new-islands.csv"""
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cc-P481-tools"))
import islands, sosdiff
_, ks, _, _, _, _ = islands.build("trammel")
_, ko, _, _, _, _ = islands.build("sos")
spots = sosdiff.parse_spots()
rows = []
for r in csv.DictReader(open(os.path.join(os.path.dirname(HERE), "cc-P481-tools", "scratch", "sos-islands.csv"))):
    if r["kind"] != "island":
        continue
    x1, y1, x2, y2 = (int(r[k]) for k in ("x1", "y1", "x2", "y2"))
    dry = ko[x1:x2 + 1, y1:y2 + 1] == 0
    was = (ks[x1:x2 + 1, y1:y2 + 1] == 0) & dry
    share = was.sum() / max(1, dry.sum())
    names = sorted({s[0].split(" / ")[-1] + ": " + s[1] for s in spots if x1 <= s[2] <= x2 and y1 <= s[3] <= y2})
    rows.append([r["id"], x1, y1, x2, y2, int(r["dry_tiles"]), int(r["statics"]), round(float(share), 2),
                 "new" if share < 0.2 else "existing (changed or not)", "; ".join(names)[:300]])
with open(os.path.join(sosdiff.OUT, "new-islands.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "x1", "y1", "x2", "y2", "dryTiles", "statics", "shareDryInStock", "verdict", "authorSpots"])
    w.writerows(sorted(rows, key=lambda r: -r[5]))
new = [r for r in rows if r[8] == "new"]
print(len(rows), "SoS islands (400+ tiles);", len(new), "new;", sum(r[5] for r in new), "dry tiles in the new ones")
for r in sorted(new, key=lambda r: -r[5])[:40]:
    print(r[1:7], r[9][:110])
