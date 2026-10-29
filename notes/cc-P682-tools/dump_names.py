"""cc-P682 exploration: the static names inside each new town's region, most common first (to choose fitting rules)."""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

regs = common.regions()
names = common.item_names()
for town in sys.argv[1:] or common.TOWNS:
    rects = regs[town]
    x1, y1 = min(r[0] for r in rects), min(r[1] for r in rects)
    x2, y2 = max(r[2] for r in rects), max(r[3] for r in rects)
    sx, sy, sz, sid = common.statics_in_box(x1, y1, x2, y2)
    c = collections.Counter()
    for x, y, i in zip(sx, sy, sid):
        if common.in_rects(int(x), int(y), rects):
            c[names[int(i)]] += 1
    print("==", town, sum(c.values()))
    print(", ".join(f"{n}:{k}" for n, k in c.most_common(160)))
