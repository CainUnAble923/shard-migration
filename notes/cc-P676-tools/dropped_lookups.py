"""cc-P676: for each stock Trammel region the generator drops that our code looks up by name, each rect's change share
(P669's measure) and its dry share on the SoS land. python -P dropped_lookups.py <SoS map folder>"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gen_regions as g  # noqa: E402

NAMES = ['Avatar Isle Cave', 'Ice Isle Cave 2', 'Mt Kendall', 'North Territory Mine 2', 'Wrong Entrance',
         'Covetous Entrance', 'Despise Entrance', 'Despise Passage']
folder = sys.argv[1]
pinned = [r for r in json.load(open(g.PINNED, encoding='utf-8')) if r['Map'] == 'Trammel']
land = g.Land(folder)
cmp = g.Stock(folder)
for n in NAMES:
    r = next(s for s in pinned if s.get('Name') == n)
    print(n, r.get('$type', 'Region'), 'parent', (r.get('Parent') or {}).get('Name'))
    for q in g.rects_of(r):
        print('   rect %s changed %.0f%% dry %.0f%% water %.0f%% void %.0f%%' % (
            q, cmp.changed_share(q), 100 * land.share([q], 0), 100 * land.share([q], 1), 100 * land.share([q], 2)))
