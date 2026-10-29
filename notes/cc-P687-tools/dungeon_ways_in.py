"""cc-P687 (SoS swap S14) part 4: which of the author's dungeons can be WALKED into.

S6 (cc-P683) left out every teleporter from the surface into his dungeons, so a dungeon reached only by teleporter is
sealed already. This looks for the other way in: a standable tile inside one of his dungeon regions next to a standable
tile outside every one of his dungeons, a step apart (P681's walk grid: pinned's movement reduced to the files, the
author's land). Each such pair is a walk-in seam; the tiles on the inside, grouped, are the entrances to fence.

    python -P dungeon_ways_in.py <code copy>     -> out/dungeon-ways-in.csv, out/dungeon-entrances.json

The author's dungeons are the DungeonRegions S3 (cc-P676) added from his Regions.xml (decision 'added' in
notes/cc-P676-tools/out-decisions.csv), less two that are not his dungeons but the way into a stock one: Sanctuary
Entrance (the stock Sanctuary's surface cave) and Paroxysmus Exit (the stock Palace's way out).
A step is 4-neighbour or diagonal, with the two Z within STEP of each other (generous on purpose: stairs and slopes
climb more than pinned's 2 per step over a run, so every real seam is caught; each one found is then looked at).
"""
import csv, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P681-tools"))
import sosgrid  # noqa: E402

NOT_HIS = {"Sanctuary Entrance", "Paroxysmus Exit"}
STEP = 10
NONE = sosgrid.NONE


def his_dungeons(code):
    dec = {r["region"]: r["decision"] for r in csv.DictReader(open(os.path.join(NOTES, "cc-P676-tools", "out-decisions.csv")))}
    t = json.load(open(os.path.join(code, "server", "data", "regions-trammel.json"), encoding="utf-8"))
    out = []
    for r in t:
        n = r.get("Name")
        if r.get("$type") == "DungeonRegion" and dec.get(n) == "added" and n not in NOT_HIS:
            out.append((n, [(a["x1"], a["y1"], a["x2"], a["y2"]) for a in r["Area"]]))
    return out


def main():
    code = sys.argv[1]
    g = sosgrid.load()
    stand = g["stand"].astype(np.int32)
    W, H = stand.shape
    dungeons = his_dungeons(code)
    owner = np.full((W, H), -1, dtype=np.int32)
    for i, (_, rects) in enumerate(dungeons):
        for x1, y1, x2, y2 in rects:
            owner[x1:x2, y1:y2] = np.where(owner[x1:x2, y1:y2] < 0, i, owner[x1:x2, y1:y2])
    ok = stand != NONE
    rows, ent = [], {}
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        a = (slice(max(0, -dx), W - max(0, dx)), slice(max(0, -dy), H - max(0, dy)))
        b = (slice(max(0, dx), W - max(0, -dx)), slice(max(0, dy), H - max(0, -dy)))
        inside = (owner[a] >= 0) & ok[a]
        outside = (owner[b] < 0) & ok[b]
        near = np.abs(stand[a] - stand[b]) <= STEP
        xs, ys = np.nonzero(inside & outside & near)
        for x, y in zip(xs.tolist(), ys.tolist()):
            ix, iy = x + a[0].start, y + a[1].start
            ox, oy = ix + dx, iy + dy
            n = dungeons[int(owner[ix, iy])][0]
            rows.append((n, ix, iy, int(stand[ix, iy]), ox, oy, int(stand[ox, oy])))
            ent.setdefault(n, set()).add((ix, iy))
    rows.sort()
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "dungeon-ways-in.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dungeon", "insideX", "insideY", "insideZ", "outsideX", "outsideY", "outsideZ"])
        w.writerows(rows)
    summary = {}
    for n, rects in dungeons:
        tiles = sorted(ent.get(n, ()))
        summary[n] = {"rects": rects, "seamTiles": len(tiles),
                      "box": [min(t[0] for t in tiles), min(t[1] for t in tiles), max(t[0] for t in tiles), max(t[1] for t in tiles)] if tiles else None}
        print("%-28s seam tiles %5d  %s" % (n, len(tiles), summary[n]["box"]))
    json.dump(summary, open(os.path.join(HERE, "out", "dungeon-entrances.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
