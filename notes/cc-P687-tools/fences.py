"""cc-P687 (SoS swap S14) parts 2 and 4: the fence regions, where each turns a player back to, and what each covers.

The fences (x1, y1, x2, y2 inclusive):
  - S14's five closure boxes (P673 section 2; the same five as ClusterFSosTreasureLand.Closures, cc-P684): the four
    unfinished areas and Glimmerwood's seam cells, which part 3 fences instead of dressing;
  - the author's one dungeon with a walk-in way (dungeon_ways_in.py): the Swamp of Desolation, a walled surface valley,
    fenced over its own rects (S3's DungeonRegion), so its three gaps (west x 1805, south y 1214, north y 913) refuse a
    walker and no spell lands inside. His other 33 are reached only by the teleporters S6 (cc-P683) left out.

The turn-back spot ("the last shore") is where a player who is somehow inside, not on a boat, is put: the nearest
standable tile outside every fence (P681's walk grid, the author's land; Chebyshev rings out from the box) that belongs
to a walkable area of at least BIG tiles (the mainland or a big island, not a rock in the sea). Walkers are simply
refused at the edge, so they stay on their own last shore.

    python -P fences.py <code copy>   -> out/fences.json (and a report: what each fence overlaps)
"""
import collections, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P681-tools"))
import sosgrid  # noqa: E402

BIG = 20000
STEP = 10
UNFINISHED = [
    ("Unfinished land: the rooster island", [(2840, 1324, 3039, 1523)]),
    ("Unfinished land: the north-east snow isles", [(4224, 256, 4479, 767)]),
    ("Unfinished land: the bare land east of Haven", [(3072, 2304, 3199, 2559)]),
    ("Unfinished land: the cells round Echoback and Darkfathom", [(4096, 2560, 4223, 2815)]),
    ("Unfinished land: Glimmerwood's broken cliffs", [(2688, 2688, 2943, 3071)]),
]
SEALED = ["Swamp of Desolation"]


SMALL = set()   # tiles of components already found smaller than BIG


def component_size(stand, x, y, cap=BIG):
    if (x, y) in SMALL:
        return 0
    seen = {(x, y)}
    q = collections.deque([(x, y)])
    W, H = stand.shape
    while q and len(seen) < cap:
        a, b = q.popleft()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                c, d = a + dx, b + dy
                if (c, d) in seen or not (0 <= c < W and 0 <= d < H) or stand[c, d] == sosgrid.NONE:
                    continue
                if abs(int(stand[c, d]) - int(stand[a, b])) > STEP:
                    continue
                seen.add((c, d))
                q.append((c, d))
    if len(seen) < cap:
        SMALL.update(seen)
    return len(seen)


def inside(rects, x, y):
    return any(x1 <= x <= x2 and y1 <= y <= y2 for x1, y1, x2, y2 in rects)


def turn_back(stand, rects, all_rects):
    x1 = min(r[0] for r in rects); y1 = min(r[1] for r in rects)
    x2 = max(r[2] for r in rects); y2 = max(r[3] for r in rects)
    tried = set()
    for ring in range(1, 400):
        best = []
        for x in range(x1 - ring, x2 + ring + 1):
            for y in (y1 - ring, y2 + ring):
                best.append((x, y))
        for y in range(y1 - ring, y2 + ring + 1):
            for x in (x1 - ring, x2 + ring):
                best.append((x, y))
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        best.sort(key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2)
        for x, y in best:
            if (x, y) in tried or not (0 <= x < 5120 and 0 <= y < 4096):
                continue
            tried.add((x, y))
            if stand[x, y] == sosgrid.NONE or inside(all_rects, x, y):
                continue
            if component_size(stand, x, y) >= BIG:
                return (x, y, int(stand[x, y]))
    return None


def main():
    code = sys.argv[1]
    g = sosgrid.load()
    stand = g["stand"]
    tram = json.load(open(os.path.join(code, "server", "data", "regions-trammel.json"), encoding="utf-8"))
    by = {r.get("Name"): r for r in tram if r.get("Name")}
    fences = [(n, r, "unfinished") for n, r in UNFINISHED]
    for n in SEALED:
        fences.append((n, [(a["x1"], a["y1"], a["x2"] - 1, a["y2"] - 1) for a in by[n]["Area"]], "sealed dungeon"))
    all_rects = [q for _, rs, _ in fences for q in rs]
    out = []
    for n, rects, kind in fences:
        tb = turn_back(stand, rects, all_rects)
        over = sorted({r.get("Name") or "(unnamed)" for r in tram if r.get("Name") != n and any(
            a["x1"] <= q[2] and q[0] < a["x2"] and a["y1"] <= q[3] and q[1] < a["y2"] for q in rects for a in r["Area"])})
        guarded = sorted({r.get("Name") for r in tram if r.get("$type") in ("TownRegion", "GuardedRegion") and any(
            a["x1"] <= q[2] and q[0] < a["x2"] and a["y1"] <= q[3] and q[1] < a["y2"] for q in rects for a in r["Area"])})
        walk = sum(int((stand[q[0]:q[2] + 1, q[1]:q[3] + 1] != sosgrid.NONE).sum()) for q in rects)
        out.append(dict(name=n, kind=kind, rects=rects, turnBack=tb, standable=walk, overlaps=over, guarded=guarded))
        print(n, kind, "turn back", tb, "standable", walk, "guarded", guarded, "overlaps", over)
    json.dump(out, open(os.path.join(HERE, "out", "fences.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
