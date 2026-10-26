r"""cc-P669: where SoS 3.0 looks unfinished, measured two ways on the surface (x < 5120).

  sparse  128 x 128 cells with 2,000+ new dry tiles (water or void in stock) and few statics on them: land laid,
          not yet dressed. Statics per new dry tile; stock Trammel's whole surface is the yardstick.
  seams   dry tiles with no static where land Z jumps 20 or more to a neighbour: the black cuts in the renders
          (a cliff or step with nothing covering it). Counted for both maps, so EA's own count is the baseline.
    python -P unfinished.py   -> out\unfinished.csv (printed)
"""
import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cc-P481-tools"))
import islands  # noqa: E402
import sosdiff  # noqa: E402

C = 128


def seams(z, kind, cnt):
    z = z.astype(np.int16)
    s = np.zeros(z.shape, bool)
    d = np.abs(z[1:, :] - z[:-1, :]) >= 20
    s[1:, :] |= d
    s[:-1, :] |= d
    d = np.abs(z[:, 1:] - z[:, :-1]) >= 20
    s[:, 1:] |= d
    s[:, :-1] |= d
    return s & (kind == 0) & (cnt == 0)


def main():
    _, zs = islands.load_land("trammel")
    _, zo = islands.load_land("sos")
    _, ks, cs, _, _, _ = islands.build("trammel")
    _, ko, co, _, _, _ = islands.build("sos")
    new = (ks != 0) & (ko == 0)
    so, ss = seams(zo, ko, co), seams(zs, ks, cs)
    stock_density = float(cs[:5120][ks[:5120] == 0].mean())
    rows = []
    for x in range(0, 5120, C):
        for y in range(0, 4096, C):
            n = int(new[x:x + C, y:y + C].sum())
            dens = float(co[x:x + C, y:y + C][new[x:x + C, y:y + C]].mean()) if n else 0.0
            rows.append([x, y, x + C - 1, y + C - 1, n, round(dens, 3), int(so[x:x + C, y:y + C].sum()), int(ss[x:x + C, y:y + C].sum())])
    with open(os.path.join(sosdiff.OUT, "unfinished.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x1", "y1", "x2", "y2", "newDryTiles", "staticsPerNewDryTile", "bareSeamTilesSos", "bareSeamTilesStock"])
        w.writerows(rows)
    print("stock surface statics per dry tile", round(stock_density, 3))
    print("bare seam tiles on the surface: SoS", int(so[:5120].sum()), "stock", int(ss[:5120].sum()))
    big = [r for r in rows if r[4] >= 2000]
    print(len(big), "cells with 2000+ new dry tiles; sparsest:")
    for r in sorted(big, key=lambda r: r[5])[:12]:
        print("  ", r)
    print("most bare seams (SoS minus stock):")
    for r in sorted(rows, key=lambda r: -(r[6] - r[7]))[:12]:
        print("  ", r)


if __name__ == "__main__":
    main()
