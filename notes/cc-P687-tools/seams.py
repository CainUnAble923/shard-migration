"""cc-P687 (SoS swap S14) part 3: the uncovered cliff seams near where players go, and what stock lays on its own.

A seam tile is P669's (notes/cc-P669-tools/unfinished.py seams): a dry surface tile with no static where the land Z
jumps 20 or more to a 4-neighbour. "Near" is within NEAR tiles (Chebyshev) of
  - a town: every TownRegion or GuardedRegion rect of S3's regions-trammel.json (Felucca's towns are the same, P686);
  - a road: a land tile in pinned's TreasureMap RoadIDs (the list cc-P684 treasure.py copies);
  - a public moongate: PMList on the SoS land (server/patches/PublicMoongate-sos-gates.patch, Felucca's Bucs' Den too).
Seams inside S14's five closure boxes are left: those boxes are fenced.

The stock palette: on stock Trammel's surface, every seam-shaped tile (dry, a 20+ Z jump) that DOES carry a static,
with the static ids counted. What OSI laid on its own cliffs is what the dressing lays.

    python -P seams.py <code copy>   -> out/seams-near.csv (x, y, z, jump, why), out/stock-seam-statics.csv
"""
import collections, csv, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
import islands  # noqa: E402

NEAR = 40
SURFACE = 5120
CLOSURES = [(2840, 1324, 3039, 1523), (4224, 256, 4479, 767), (3072, 2304, 3199, 2559), (4096, 2560, 4223, 2815),
            (2688, 2688, 2943, 3071)]
ROADS = [(0x0071, 0x0078), (0x00E8, 0x00EB), (0x07AE, 0x07B1), (0x3FF4, 0x3FF4), (0x3FF8, 0x3FFB), (0x0442, 0x0479),
         (0x0501, 0x0510), (0x0009, 0x0015), (0x0150, 0x015C)]
MOONGATES = [(4467, 1283), (1336, 1997), (1499, 3771), (771, 752), (2701, 692), (1828, 2948), (643, 2067), (3563, 2139),
             (3696, 2570), (2711, 2234)]


def jump(z):
    z = z.astype(np.int16)
    j = np.zeros(z.shape, np.int16)
    d = np.abs(z[1:, :] - z[:-1, :])
    j[1:, :] = np.maximum(j[1:, :], d)
    j[:-1, :] = np.maximum(j[:-1, :], d)
    d = np.abs(z[:, 1:] - z[:, :-1])
    j[:, 1:] = np.maximum(j[:, 1:], d)
    j[:, :-1] = np.maximum(j[:, :-1], d)
    return j


def grow(mask, r):
    """Every tile within r (Chebyshev) of a True tile, by a running max over rows then columns."""
    c = np.cumsum(np.pad(mask, ((r + 1, r), (0, 0))).astype(np.int32), axis=0)
    m = (c[2 * r + 1:, :] - c[:-2 * r - 1, :]) > 0
    c = np.cumsum(np.pad(m, ((0, 0), (r + 1, r))).astype(np.int32), axis=1)
    return (c[:, 2 * r + 1:] - c[:, :-2 * r - 1]) > 0


def towns(code):
    t = json.load(open(os.path.join(code, "server", "data", "regions-trammel.json"), encoding="utf-8"))
    return [(r.get("Name"), (a["x1"], a["y1"], a["x2"], a["y2"])) for r in t
            if r.get("$type") in ("TownRegion", "GuardedRegion") for a in r["Area"]]


def main():
    code = sys.argv[1]
    ids, zs = islands.load_land("sos")
    _, kind, cnt, _, _, _ = islands.build("sos")
    ids, zs, kind, cnt = ids[:SURFACE], zs[:SURFACE], kind[:SURFACE], cnt[:SURFACE]
    j = jump(zs)
    seam = (j >= 20) & (kind == 0) & (cnt == 0)
    closed = np.zeros(seam.shape, bool)
    for x1, y1, x2, y2 in CLOSURES:
        closed[x1:x2 + 1, y1:y2 + 1] = True
    town = np.zeros(seam.shape, bool)
    for _, (x1, y1, x2, y2) in towns(code):
        town[max(0, x1):min(SURFACE, x2), y1:y2] = True
    road = np.zeros(seam.shape, bool)
    for a, b in ROADS:
        road |= (ids >= a) & (ids <= b)
    gate = np.zeros(seam.shape, bool)
    for x, y in MOONGATES:
        gate[x, y] = True
    near_t, near_r, near_g = grow(town, NEAR), grow(road, NEAR), grow(gate, NEAR)
    pick = seam & ~closed & (near_t | near_r | near_g)
    xs, ys = np.nonzero(pick)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "seams-near.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "z", "jump", "nearTown", "nearRoad", "nearMoongate"])
        for x, y in zip(xs.tolist(), ys.tolist()):
            w.writerow([x, y, int(zs[x, y]), int(j[x, y]), int(near_t[x, y]), int(near_r[x, y]), int(near_g[x, y])])
    print("seams on the surface", int(seam.sum()), "in the closure boxes", int((seam & closed).sum()))
    print("near a town", int((seam & ~closed & near_t).sum()), "a road", int((seam & ~closed & near_r).sum()),
          "a moongate", int((seam & ~closed & near_g).sum()), "-> to dress", len(xs))
    print("road tiles on the surface", int(road.sum()))

    # the stock palette
    sids, szs = islands.load_land("trammel")
    _, sk, sc, _, _, _ = islands.build("trammel")
    sj = jump(szs[:SURFACE])
    shaped = (sj >= 20) & (sk[:SURFACE] == 0) & (sc[:SURFACE] > 0)
    sx, sy, sz, sid = islands.load_statics("trammel")
    on = (sx < SURFACE)
    on[on] = shaped[sx[on], sy[on]]
    c = collections.Counter(sid[on].tolist())
    with open(os.path.join(HERE, "out", "stock-seam-statics.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "count"])
        for k, v in c.most_common():
            w.writerow(["0x%04X" % k, v])
    print("stock seam-shaped tiles with a static", int(shaped.sum()), "; top ids:",
          ", ".join("0x%04X %d" % (k, v) for k, v in c.most_common(25)))


if __name__ == "__main__":
    main()
