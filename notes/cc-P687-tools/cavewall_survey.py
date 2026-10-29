"""cc-P687 part 3: where OSI stands its cave-wall pieces on stock Trammel's surface, relative to the slope.

For every static named "cave wall" on the surface (x < 5120): the land Z rise to its north (z(x, y-1) - z) and to its
west (z(x-1, y) - z), the walkable land Z under it against the piece's own Z, and its flags and height. A piece used
where the ground rises to the north covers a south-facing slope; to the west, an east-facing one. The camera looks from
the south-east, so those are the faces a player sees.

    python -P cavewall_survey.py   -> out/cavewall-survey.csv
"""
import collections, csv, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(NOTES), "scripts"))
import islands  # noqa: E402
from mapbuild import uofiles  # noqa: E402

S = 5120


def main():
    _, items = uofiles.read_tiledata()
    want = sorted(i for i, it in enumerate(items) if it["name"].strip().lower() == "cave wall")
    _, zs = islands.load_land("trammel")
    z = zs.astype(np.int32)
    sx, sy, sz, sid = islands.load_statics("trammel")
    on = (sx < S) & (sx > 0) & (sy > 0) & np.isin(sid, want)
    rows = []
    for i in want:
        m = on & (sid == i)
        if not m.any():
            continue
        x, y = sx[m], sy[m]
        rn = z[x, y - 1] - z[x, y]
        rw = z[x - 1, y] - z[x, y]
        dz = sz[m].astype(np.int32) - z[x, y]
        it = items[i]
        rows.append(["0x%04X" % i, int(m.sum()), int((rn >= 10).sum()), int((rw >= 10).sum()), int(np.median(rn)),
                     int(np.median(rw)), int(np.median(dz)), uofiles.flagstr(it["flags"]), it["height"]])
    with open(os.path.join(HERE, "out", "cavewall-survey.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "onSurface", "riseNorth10", "riseWest10", "medRiseNorth", "medRiseWest", "medZoverLand", "flags",
                    "height"])
        w.writerows(rows)
    for r in sorted(rows, key=lambda r: -r[1]):
        print(r)


if __name__ == "__main__":
    main()
