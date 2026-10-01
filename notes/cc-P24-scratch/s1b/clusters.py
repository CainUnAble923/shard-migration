# Group changed statics blocks into connected clusters (8-neighbour, gap<=2 blocks) and summarise adds/removes.
import json, os
from collections import Counter
from uodata import *

here = os.path.dirname(os.path.abspath(__file__))
ch = json.load(open(os.path.join(here, "changed_statics.json")))
land, items = read_tiledata(NEW)
out = {}
for fi in ("0", "1"):
    name, w, h = FACETS[int(fi)]
    bh = h >> 3
    blocks = set(ch[fi]["blocks"])
    io, so = load_statics_index(OLD, int(fi))
    inn, sn = load_statics_index(NEW, int(fi))
    seen = set()
    clusters = []
    for b in sorted(blocks):
        if b in seen:
            continue
        stack = [b]; seen.add(b); comp = []
        while stack:
            c = stack.pop(); comp.append(c)
            cx, cy = c // bh, c % bh
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    nb = (cx + dx) * bh + (cy + dy)
                    if nb in blocks and nb not in seen:
                        seen.add(nb); stack.append(nb)
        xs = [c // bh for c in comp]; ys = [c % bh for c in comp]
        add = Counter(); rem = Counter()
        for c in comp:
            a = Counter(block_statics(io, so, c)); n = Counter(block_statics(inn, sn, c))
            for k, v in (n - a).items(): add[k[0]] += v
            for k, v in (a - n).items(): rem[k[0]] += v
        clusters.append(dict(n=len(comp), bbox=[min(xs)*8, min(ys)*8, max(xs)*8+7, max(ys)*8+7],
                             added=sum(add.values()), removed=sum(rem.values()),
                             top_add=[(hex(t), items[t]["name"], v) for t, v in add.most_common(6)],
                             top_rem=[(hex(t), items[t]["name"], v) for t, v in rem.most_common(6)]))
    clusters.sort(key=lambda c: -c["n"])
    out[fi] = clusters
    print("==", name, len(clusters), "clusters")
    for c in clusters:
        print(c["n"], c["bbox"], "+%d -%d" % (c["added"], c["removed"]), "ADD", c["top_add"][:4], "REM", c["top_rem"][:4])
json.dump(out, open(os.path.join(here, "clusters.json"), "w"), indent=1)
