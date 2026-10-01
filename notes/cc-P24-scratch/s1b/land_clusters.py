# Cluster land-diff blocks; summarise per cluster: cells changed, z deltas, top land id transitions.
import json, os
from collections import Counter
import numpy as np
from uodata import *

here = os.path.dirname(os.path.abspath(__file__))
cl = json.load(open(os.path.join(here, "changed_land.json")))
st = json.load(open(os.path.join(here, "changed_statics.json")))
landtd, items = read_tiledata(NEW)
out = {}
for fi in ("0", "1"):
    name, w, h = FACETS[int(fi)]
    bh = h >> 3
    a = load_land(OLD, int(fi)); b = load_land(NEW, int(fi))
    blocks = set(cl[fi]["blocks"])
    sblocks = set(st[fi]["blocks"])
    seen = set(); clusters = []
    for blk in sorted(blocks):
        if blk in seen: continue
        stack = [blk]; seen.add(blk); comp = []
        while stack:
            c = stack.pop(); comp.append(c)
            cx, cy = c // bh, c % bh
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    nb = (cx + dx) * bh + (cy + dy)
                    if nb in blocks and nb not in seen:
                        seen.add(nb); stack.append(nb)
        xs = [c // bh for c in comp]; ys = [c % bh for c in comp]
        x0, y0, x1, y1 = min(xs)*8, min(ys)*8, max(xs)*8+8, max(ys)*8+8
        ai, bi = a["ids"][x0:x1, y0:y1], b["ids"][x0:x1, y0:y1]
        az, bz = a["z"][x0:x1, y0:y1].astype(int), b["z"][x0:x1, y0:y1].astype(int)
        m = (ai != bi) | (az != bz)
        dz = (bz - az)[m]
        trans = Counter(zip([landtd[i][2] for i in ai[m]], [landtd[i][2] for i in bi[m]]))
        clusters.append(dict(nblocks=len(comp), bbox=[x0, y0, x1-1, y1-1], cells=int(m.sum()),
                             statics_blocks_overlap=len(set(comp) & sblocks),
                             dz_min=int(dz.min()), dz_max=int(dz.max()), dz_abs_mean=float(np.abs(dz).mean()),
                             top=trans.most_common(4)))
    clusters.sort(key=lambda c: -c["cells"])
    out[fi] = clusters
    print("==", name, len(clusters), "clusters; land blocks", len(blocks), "statics blocks", len(sblocks),
          "overlap", len(blocks & sblocks), "statics-only", len(sblocks - blocks))
    for c in clusters[:40]:
        print(c["nblocks"], c["bbox"], c["cells"], "ovl", c["statics_blocks_overlap"], "dz", c["dz_min"], c["dz_max"], round(c["dz_abs_mean"], 1), c["top"][:3])
json.dump(out, open(os.path.join(here, "land_clusters.json"), "w"), indent=1)
