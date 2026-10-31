"""cc-P741: a text map round a stop: R road, r road on the walked route, w walked route off road, T taken (items,
spots, rooms, door lines), . free; S the stop. python -P debug_signs.py <work> x y"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts')); sys.path.insert(0, os.path.join(REPO, 'notes', 'cc-P662-tools'))
import build_isle as B
work, sx, sy = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
farm, props, pts, farm_door = B.server_items()
props = [p for p in props if not p[4].startswith('sign core.')]
land, statics, report, info = B.plan(farm, props, pts, quiet=True)
road = {B.shifted(*c) for c in info['road']}
edited = os.path.join(work, 'edited'); rect = B.shifted(*B.AREA[:2]) + B.shifted(*B.AREA[2:])
w0 = B.Walker(edited, rect)
extra = [(x, y, z, t) for (x, y, z, t, _) in farm if (x, y) != farm_door] + [(x, y, w0.ground(x, y), t) for (x, y, z, t, _) in props]
w = B.Walker(edited, rect, extra)
stops = [B.shifted(x, y) for (_, _, x, y) in B.P.STOPS]
route = set()
for a, b in zip(stops, stops[1:]):
    route |= {(s[0], s[1]) for s in w.path(a, b)}
taken = {(x, y) for (x, y, *_r) in farm} | {(x, y) for (x, y, *_r) in props} | set(pts.values())
for r in info['rooms'].values():
    taken |= {B.shifted(*c) for c in r['floor'] | r['ring']}
for y in range(sy - 7, sy + 6):
    row = ''
    for x in range(sx - 8, sx + 9):
        c = (x, y)
        ch = 'S' if c == (sx, sy) else ('r' if c in route else 'R') if c in road else 'w' if c in route else 'T' if c in taken else ('~' if info['cls'].get((x - B.DX, y - B.DY)) == 'w' else '.')
        row += ch
    print(y, row)
