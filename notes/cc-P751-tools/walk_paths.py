"""cc-P751: the route a real character walks in TazUO for the P748 review's item 6, as tile paths. The builder's own
walker (build_isle.Walker: pinned's movement rules, the server items in place) finds each leg's path on the built map
files; IsleWalk751.py then steps the client along it one tile at a time and logs every step's Z.

The route: the west beach past the wreck (P741's walk), then every lesson leg from the wake spot (stop 0) to the dock
end (stop 10), with each door walked in and out: the farmhouse step and door, the bank door, the lodge door, and the
dock back to the landing.

    python -P walk_paths.py <map folder> <out.json>     (SL_CODE = the code copy)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'cc-P662-tools'))
import build_isle as B  # noqa: E402

folder, out = sys.argv[1], sys.argv[2]
farm, props, pts, farm_door = B.server_items()
rect = B.shifted(*B.AREA[:2]) + B.shifted(*B.AREA[2:])
w0 = B.Walker(folder, rect)
# every farm piece, the door tile's floor too (the gate drops the whole door tile, so its walker sees bare ground there and
# cannot climb to the floor; the door itself is a server item, not in the layout, and TazUO opens it when walked into)
extra = [(x, y, z, tid) for (x, y, z, tid, what) in farm]
extra += [(x, y, w0.ground(x, y), tid) for (x, y, z, tid, what) in props]
w = B.Walker(folder, rect, extra)
stops = [(n, label, B.shifted(x, y)) for (n, label, x, y) in B.P.STOPS]
S = {n: (label, xy) for n, label, xy in stops}

# (name, waypoints): each waypoint after the first is reached by the walker's shortest path from the one before
route = [('beach: west sand north past the wreck', [(6629, 4003), (6629, 3986)]),
         ('beach: to the wake spot (stop 0)', [(6629, 3986), S[0][1]])]
for (a, b) in zip(stops, stops[1:]):
    if b[0] == 10:
        break
    route.append(('stop %d to %d: %s' % (a[0], b[0], b[1]), [a[2], b[2]]))
    if b[0] == 5:   # the farm gate: then the farmhouse, up its step and in at its door, and out again
        route.append(('farmhouse: up the step and in at the door', [b[2], (6702, 3981), (6701, 3977)]))
        route.append(('farmhouse: out at the door and down the step', [(6701, 3977), (6702, 3981), b[2]]))
    if b[0] == 7:   # the bank: in at its south door to the counter's queue side, and out
        route.append(('bank: in at the south door', [b[2], (6762, 3978)]))
        route.append(('bank: out at the south door', [(6762, 3978), b[2]]))
    if b[0] == 8:   # the lodge: in at its north door to Elara's desk side, and out
        route.append(('lodge: in at the north door', [b[2], (6782, 3997)]))
        route.append(('lodge: out at the north door', [(6782, 3997), b[2]]))
dock_end = S[10][1]
dock_end = (dock_end[0] - 1, dock_end[1])          # the dock end beside the moongate, not the gate itself
route.append(('stop 9 to the dock end (stop 10, beside the moongate)', [S[9][1], dock_end]))
route.append(('dock: back to the landing road', [dock_end, (6800, 3991)]))

def path3(start, b):
    """Walker.path from a standing spot with its Z (Walker.path starts at the land's Z, which inside a house is the
    ground under the floor)."""
    prev = {start: None}
    q = [start]
    end = None
    while q:
        s = q.pop(0)
        if (s[0], s[1]) == tuple(b):
            end = s
            break
        for nb in w.moves(*s):
            if nb not in prev:
                prev[nb] = s
                q.append(nb)
    out = []
    while end is not None:
        out.append(end)
        end = prev[end]
    return out[::-1] or None


legs = []
here = None
for name, wps in route:
    path = []
    for a, b in zip(wps, wps[1:]):
        start = tuple(path[-1]) if path else (here if here and (here[0], here[1]) == tuple(a) else (a[0], a[1], w.ground(*a)))
        p = path3(start, b)
        assert p, ('no path', name, a, b)
        path += p if not path else p[1:]
    here = tuple(path[-1])
    legs.append({'name': name, 'path': [list(s) for s in path]})
    print('%-58s %3d steps, from %s to %s' % (name, len(path) - 1, tuple(path[0]), tuple(path[-1])))
json.dump(legs, open(out, 'w'), indent=0)
print(out, sum(len(l['path']) - 1 for l in legs), 'steps in', len(legs), 'legs')
