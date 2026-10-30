r"""cc-P688 (SoS swap S15) part 1, step 2: the whole-map survey's groups (walkgrid.py, one level a tile) checked with
the exact walk (exact.py, every level, pinned's Check step by step).

The one-level survey can split a place off where a walker climbs one stack of floors and comes down another (Fort
Yondall's gatehouse stairs) or steps from a floor onto lower logs (Papua's bank door). So every pair of places in
different groups that stand within REACH tiles of each other is walked exactly, both ways, over the rectangle around
the two plus MARGIN. Groups joined both ways are merged; a pair joined one way only is listed.

    python -P verify.py <code copy>     -> out/table.csv (the reachability table), out/table-groups.csv, out/exact.csv
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import exact  # noqa: E402
import walkgrid  # noqa: E402
import numpy as np  # noqa: E402

REACH, MARGIN = 150, 60


def table(code, say=print):
    """(rows, final groups as lists of row indexes, the exact walks tried)."""
    res = walkgrid.survey(code)
    rows, reach = res["rows"], res["reach"]
    groups = walkgrid.groups(rows, reach)
    gid = {}
    for k, g in enumerate(groups):
        for j in g:
            gid[j] = k
    parent = list(range(len(groups)))

    def find(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k

    # For each place: the exact walk over the square REACH around it. A tile it reaches in another group's walk area
    # (the survey's own area of the tile names the group) is walked back to the place, exactly. Both ways: one group.
    lab = res["lab"]
    area_group = {}
    for k, g in enumerate(groups):
        for j in g:
            area_group[rows[j]["area"]] = k
    tried = []
    for a, g in enumerate(groups):
        for i in g:
            r = rows[i]
            rect = (max(0, r["sx"] - REACH), max(0, r["sy"] - REACH),
                    min(walkgrid.W - 2, r["sx"] + REACH), min(walkgrid.H - 2, r["sy"] + REACH))
            e = exact.Exact(rect)
            prev, _ = e.flood(r["sx"], r["sy"], r["z"])
            hits = {}
            for x, y, z in prev:
                b = area_group.get(int(lab[x, y]))
                if b is not None and find(b) != find(a):
                    d = max(abs(x - r["sx"]), abs(y - r["sy"]))
                    if b not in hits or d < hits[b][0]:
                        hits[b] = (d, x, y, z)
            for b, (d, x, y, z) in sorted(hits.items()):
                if find(a) == find(b):
                    continue
                back, _ = e.flood(x, y, z, goal=(r["sx"], r["sy"]))
                ok_back = any((p[0], p[1]) == (r["sx"], r["sy"]) for p in back)
                s = dict(name="%s's area at %d,%d" % (rows[groups[b][0]]["name"], x, y), sx=x, sy=y, z=z)
                tried.append((r, s, rect, (True, None, (x, y), len(prev)), (ok_back, None, (r["sx"], r["sy"]), len(back))))
                say("%-34s -> %-44s True / back %s" % (r["name"], s["name"], ok_back))
                if ok_back:
                    parent[find(a)] = find(b)
    merged = {}
    for k in range(len(groups)):
        merged.setdefault(find(k), []).extend(groups[k])
    final = sorted(merged.values(), key=lambda g: (-len(g), rows[g[0]]["name"]))
    return rows, final, tried


def main():
    rows, final, tried = table(sys.argv[1])
    os.makedirs(walkgrid.OUT, exist_ok=True)
    with open(os.path.join(walkgrid.OUT, "exact.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["from", "to", "rect", "there", "there_steps", "back", "back_steps", "nearest_there", "nearest_back"])
        for r, s, rect, there, back in tried:
            w.writerow([r["name"], s["name"], "%d,%d-%d,%d" % rect, there[0], there[1], back[0], back[1],
                        "%d,%d" % there[2], "%d,%d" % back[2]])
    with open(os.path.join(walkgrid.OUT, "table-groups.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["group", "kind", "name", "x", "y", "z"])
        for k, g in enumerate(final):
            for j in g:
                w.writerow([k + 1, rows[j]["kind"], rows[j]["name"], rows[j]["x"], rows[j]["y"], rows[j]["z"]])
    for k, g in enumerate(final):
        print("\ngroup %d: %s" % (k + 1, "; ".join("%s %s" % (rows[j]["kind"], rows[j]["name"]) for j in g)))


if __name__ == "__main__":
    main()
