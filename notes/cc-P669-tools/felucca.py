r"""cc-P669 part 3: Felucca, if it were built from the same SoS land.

    python -P felucca.py   -> out\felucca-summary.csv (printed)

1. How far stock Felucca already differs from stock Trammel (8 x 8 blocks, as sosdiff): EA's own Felucca-only
   geography (Haven's ruins, Magincia, Bucs' Den, the Lost Lands' champion areas...).
2. Felucca's stock content graded on SoS land with geo.Grader: spawners, decoration, teleporters, moongates, regions,
   and the champion spawns of pinned GenChamps.cs (Felucca only; stock Trammel has none).
3. Our code's Felucca-only points (files naming Felucca and not Trammel) on SoS land.
"""
import collections
import csv
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cc-P481-tools"))
import islands  # noqa: E402
import sosdiff  # noqa: E402
import geo  # noqa: E402

BW, BH = sosdiff.BW, sosdiff.BH


def block_diff(a, b):
    la, za = islands.load_land(a)
    lb, zb = islands.load_land(b)
    land = ((la != lb) | (za != zb)).reshape(BW, 8, BH, 8).any(axis=(1, 3))
    ka, kb = sosdiff.static_keys(a), sosdiff.static_keys(b)
    d = np.concatenate([np.setdiff1d(ka, kb, assume_unique=True), np.setdiff1d(kb, ka, assume_unique=True)])
    st = np.zeros(BW * BH, bool)
    st[np.unique(d >> 30)] = True
    st = st.reshape(BW, BH)
    either = land | st
    return int(either.sum()), int(either[:640].sum())


def main():
    rows = []
    for a, b in (("trammel", "felucca"), ("felucca", "sos"), ("trammel", "sos")):
        n, surf = block_diff(a, b)
        rows.append(["blocks differing", a + " vs " + b, n, surf, "", "", ""])
        print(a, "vs", b, "blocks differing", n, "of which surface (x<5120)", surf, flush=True)
    g = geo.Grader("felucca")
    pts = geo.stock_points("felucca")
    src = open(os.path.join(geo.PIN, "Projects", "UOContent", "Engines", "CannedEvil", "GenChamps.cs")).read()
    for m in re.finditer(r"new\(typeof\((\w+)\),[^P]*new Point3D\((\d+), (\d+), -?\d+\), Map\.Felucca", src):
        pts.append(("stock champion spawn", "GenChamps.cs", m.group(1), int(m.group(2)), int(m.group(3))))
    ours, _ = geo.our_points()
    for cat, s, maps, x, y in ours:
        if maps == "Felucca":
            pts.append(("ours (Felucca only)", s, "", x, y))
    summ = collections.defaultdict(collections.Counter)
    for cat, s, name, x, y in pts:
        summ[cat][g.grade(x, y)] += 1
    for k, c in summ.items():
        rows.append([k, "felucca on SoS land", sum(c.values()), "", c["unchanged"], c["moves"], c["rework"]])
        print(k, sum(c.values()), dict(c))
    with open(os.path.join(sosdiff.OUT, "felucca-summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["what", "compared", "count", "surfaceBlocks", "unchanged", "moves", "rework"])
        w.writerows(rows)


if __name__ == "__main__":
    main()
