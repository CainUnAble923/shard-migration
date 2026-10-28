r"""cc-P678: SoS Haven's buildings, and which are not a stock pre-UOML shop.
A building is a 4-connected group of covered open tiles (an open tile with a static 10 or more above its floor:
a roof or an upper floor). Each is listed with its box, its tile count, its floor Z range and the stock "Haven"
shop region (pinned regions.json) that covers most of it, or "-" when none does.
    python -P buildings.py [x1 y1 x2 y2]   (default: the town box 3568-3761, 2460-2712)
Read only, SoS 3.0 through P481's loaders.
"""
import json
import os
import sys
from collections import deque

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import townmap  # noqa: E402

REGIONS = "D:/UO/ModernUO-pinned/Distribution/Data/regions.json"


def shops():
    out = []
    for r in json.load(open(REGIONS)):
        p = r.get("Parent") or {}
        if r.get("Map") == "Trammel" and p.get("Name") == "Haven" and r.get("Name"):
            out.append((r["Name"], [(a["x1"], a["y1"], a["x2"], a["y2"]) for a in r["Area"]]))
    return out


def narrow(x1, y1, x2, y2):
    """Cut the statics in townmap's cache down to the box, so tile() scans a few thousand, not millions."""
    c = townmap.load()
    if "all" not in c:
        c["all"] = {k: c[k] for k in ("sx", "sy", "sz", "sid")}
    c.update(c["all"])
    x1, y1, x2, y2 = x1 - 2, y1 - 2, x2 + 2, y2 + 2
    m = (c["sx"] >= x1) & (c["sx"] <= x2) & (c["sy"] >= y1) & (c["sy"] <= y2)
    for k in ("sx", "sy", "sz", "sid"):
        c[k] = c[k][m]


def covered(x, y):
    kind, z = townmap.tile(x, y)
    if kind != "open":
        return None
    c = townmap._cache
    m = (c["sx"] == x) & (c["sy"] == y)
    return z if any(int(v) >= z + 10 for v in c["sz"][m]) else None


def find(x1, y1, x2, y2):
    narrow(x1, y1, x2, y2)
    cov = {}
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            z = covered(x, y)
            if z is not None:
                cov[(x, y)] = z
    seen, groups = set(), []
    for p in cov:
        if p in seen:
            continue
        q, g = deque([p]), []
        seen.add(p)
        while q:
            x, y = q.popleft()
            g.append((x, y))
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n in cov and n not in seen:
                    seen.add(n)
                    q.append(n)
        groups.append(g)
    return cov, groups


def main():
    a = [int(v) for v in sys.argv[1:5]] or [3568, 2460, 3761, 2712]
    cov, groups = find(*a)
    sh = shops()
    for g in sorted(groups, key=lambda g: (min(p[1] for p in g), min(p[0] for p in g))):
        if len(g) < 12:
            continue
        xs, ys = [p[0] for p in g], [p[1] for p in g]
        zs = [cov[p] for p in g]
        best, n = "-", 0
        for name, rects in sh:
            k = sum(1 for (x, y) in g if any(r[0] <= x <= r[2] and r[1] <= y <= r[3] for r in rects))
            if k > n:
                best, n = name, k
        print("%4d-%4d %4d-%4d tiles %3d z %d..%d  %s%s" % (min(xs), max(xs), min(ys), max(ys), len(g), min(zs), max(zs),
                                                       best, "" if best == "-" else " (%d)" % n))


if __name__ == "__main__":
    main()
