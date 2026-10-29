"""cc-P687 part 3: OSI's own rock statics on stock Trammel's surface, and how steep the ground under them is.

For every static named rock, rocks, boulder or cave wall (stock tiledata): its count on stock Trammel's surface, the
share standing on a tile whose land Z jumps 20 or more to a 4-neighbour (a cliff), its flags and height. The dressing
pass takes OSI's commonest cliff rocks: those it lays on cliffs most.

    python -P rock_palette.py   -> out/rock-palette.csv
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
import seams  # noqa: E402

WORDS = ("rock", "rocks", "boulder", "cave wall")


def main():
    _, items = uofiles.read_tiledata()
    want = {i for i, it in enumerate(items) if it["name"].strip().lower() in WORDS}
    _, zs = islands.load_land("trammel")
    j = seams.jump(zs[:seams.SURFACE])
    sx, sy, sz, sid = islands.load_statics("trammel")
    on = (sx < seams.SURFACE) & np.isin(sid, list(want))
    cnt, cliff = collections.Counter(sid[on].tolist()), collections.Counter(sid[on][j[sx[on], sy[on]] >= 20].tolist())
    rows = []
    for i in sorted(cnt, key=lambda k: -cliff[k]):
        it = items[i]
        rows.append(["0x%04X" % i, it["name"].strip(), cnt[i], cliff[i], round(cliff[i] / cnt[i], 3),
                     uofiles.flagstr(it["flags"]), it["height"]])
    with open(os.path.join(HERE, "out", "rock-palette.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "onSurface", "onCliffs", "cliffShare", "flags", "height"])
        w.writerows(rows)
    for r in rows[:30]:
        print(r)


if __name__ == "__main__":
    main()
