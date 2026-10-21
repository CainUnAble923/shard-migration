# cc-P267 read only: one client-view preview per bank from placement.json, with the decor drawn in (stock art, so the
# client's own art file supplies every piece) and each row ringed. Roofs and upper walls are left out so the inside
# shows ("open"); -roof draws the building as a player outside sees it.
#     python render_previews.py [out-folder] [bank-key ...]
import json, os, sys
import bankbase as B

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'placement.json')))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'previews')
only = sys.argv[2:]
os.makedirs(out, exist_ok=True)
banks = {}
for r in rows: banks.setdefault(r['bank'], []).append(r)
FS = {}
for key, rs in banks.items():
    if only and key not in only: continue
    F = FS.setdefault(rs[0]['facet'], B.Facet(B.FACET[rs[0]['facet']]))
    xs = [r['x'] for r in rs]; ys = [r['y'] for r in rs]
    x0, y0, x1, y1 = min(xs) - 4, min(ys) - 4, max(xs) + 4, max(ys) + 4
    fz = min(r['z'] for r in rs if r['mode'] in ('corner', 'indoor')) if any(r['mode'] in ('corner', 'indoor') for r in rs) else min(r['z'] for r in rs)
    extra = [(r['itemId'], r['x'], r['y'], r['z']) for r in rs]
    marks = [('', r['x'], r['y'], r['z'], (255, 60, 60) if r['mode'] == 'outside' else (80, 200, 255)) for r in rs]
    label = '%s (%s): %d pieces' % (rs[0]['bankName'], rs[0]['facet'], len(rs))
    p = os.path.join(out, key + '.jpg')
    size = B.render(F, x0, y0, x1, y1, extra=extra, marks=marks, grid=5, out=p, scale=0.6, hide_roofs_above=fz + 12, label=label)
    print(key, size, os.path.getsize(p) // 1024, 'KB')
