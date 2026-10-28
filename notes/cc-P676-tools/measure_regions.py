"""cc-P676: each generated Trammel region on the SoS land: its dry, water and void shares, and for a guarded region the
share of its 8 x 8 blocks that are open wild (all dry, no statics). Writes out-measure.csv.
python -P measure_regions.py <SoS map folder> <regions-trammel.json>"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_regions as g  # noqa: E402

GUARDED = {'TownRegion', 'GuardedRegion'}
folder, path = sys.argv[1], sys.argv[2]
regions = json.load(open(path, encoding='utf-8'))
land = g.Land(folder)


def rects(r):
    return [(a['x1'], a['y1'], a['x2'], a['y2']) for a in r.get('Area', [])]


def wild_share(rs):
    blocks = set()
    for (x1, y1, x2, y2) in rs:
        for bx in range(max(0, x1) // 8, (min(g.W, x2) - 1) // 8 + 1):
            for by in range(max(0, y1) // 8, (min(g.H, y2) - 1) // 8 + 1):
                blocks.add((bx, by))
    if not blocks:
        return 0.0, 0
    wild = sum(1 for (bx, by) in blocks if land.blk_dry[bx, by] == 64 and land.blk_statics[bx, by] == 0)
    return wild / len(blocks), len(blocks)


rows = []
for i, r in enumerate(regions):
    rs = rects(r)
    t = r.get('$type', 'Region')
    parent = (r.get('Parent') or {}).get('Name', '')
    row = {'i': i, 'name': r.get('Name') or '(unnamed)', 'type': t, 'parent': parent, 'rects': len(rs),
           'dry': round(land.share(rs, 0), 3), 'water': round(land.share(rs, 1), 3), 'void': round(land.share(rs, 2), 3)}
    if t in GUARDED and not parent:
        w, n = wild_share(rs)
        row['guardedWild'], row['guardedBlocks'] = round(w, 3), n
    rows.append(row)
keys = ['i', 'name', 'type', 'parent', 'rects', 'dry', 'water', 'void', 'guardedWild', 'guardedBlocks']
with open(os.path.join(HERE, 'out-measure.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, keys)
    w.writeheader()
    w.writerows(rows)
print('regions', len(rows))
