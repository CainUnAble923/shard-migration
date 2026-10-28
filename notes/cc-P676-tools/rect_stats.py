"""cc-P676: per rect of each region this prompt drew or changed (every decision but kept and kept for S7), its dry,
water and void shares; prints the rects with the least dry land. python -P rect_stats.py <SoS map folder> <json>"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_regions as g  # noqa: E402

folder, path = sys.argv[1], sys.argv[2]
land = g.Land(folder)
regions = json.load(open(path, encoding='utf-8'))
decided = {r['region']: r['decision'] for r in csv.DictReader(open(os.path.join(HERE, 'out-decisions.csv')))}
rows = []
for r in regions:
    name = r.get('Name') or '(unnamed)'
    if decided.get(name) in ('kept', 'kept for S7'):
        continue
    for a in r['Area']:
        q = (a['x1'], a['y1'], a['x2'], a['y2'])
        rows.append((land.share([q], 0), land.share([q], 1), land.share([q], 2), name, r.get('$type', 'Region'), q))
rows.sort()
print('rects', len(rows))
for d, w, v, n, t, q in rows[:30]:
    print('dry %.2f water %.2f void %.2f  %-40s %-16s %s' % (d, w, v, n, t, q))
