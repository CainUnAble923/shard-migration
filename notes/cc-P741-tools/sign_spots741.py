"""cc-P741 item 3 (Chase 10-30: "lesson 1 sign needs to go to north side of path", "all signs should be north of
path"): where each lesson's signpost stands. P720's sign_spots.py with one more rule: the sign stands NORTH of its path,
beside it: on a tile whose column has road within 3 tiles south of it and none north of it within 3, so the path runs
south of the sign, and the signpost's board (0xA854, the face that reads from the south) faces the path. Everything
else as P720: off every walked leg of the route and the road; not a server item's tile or spot, nor beside one; outside
every building; fits a 16-high person on the built files; and leaves the stop reachable from both neighbours.

The travel lesson's sign (Chase: "sign next to moongate at end is hard to see") stands where the road meets the dock,
north of it, clear of the moongate frame's glow and the lighthouse, so it is seen before the dock (its "stop" here is the
road's last tile, ROAD_END). The chat lesson's second sign (the farm signpost, TutorialCorePlacement.ChatSignpost) is
checked by the same rule.

    python -P sign_spots741.py <work folder>     prints the spots and the C# switch
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, os.path.join(REPO, 'notes', 'cc-P662-tools'))
import build_isle as B  # noqa: E402

# each lesson's stop (TutorialCorePlacement.MarkerSpot), isle coordinates; cc-P741: the farm's and healing's moved
STOPS = {
    'core.movement': (6646, 3993), 'core.backpack': (6656, 3990), 'core.paperdoll': (6665, 3992),
    'core.chat': (6692, 3990), 'core.farm': (6696, 3979), 'core.healing': (6702, 3979), 'core.death': (6736, 3995),
    'core.banking': (6762, 3981), 'core.league': (6782, 3994), 'core.loop': (6794, 3982),
    'core.travel': (6811, 3991)}
SIGN = 0xA854
REACH = 3


def main():
    work = sys.argv[1]
    edited = os.path.join(work, 'edited')
    farm, props, pts, farm_door = B.server_items()
    # the lesson signs themselves are what is being placed: leave them out of the items the walker sees
    props = [p for p in props if not p[4].startswith('sign core.')]
    land, statics, report, info = B.plan(farm, props, pts)
    road = {B.shifted(*c) for c in info['road']}
    rect = B.shifted(*B.AREA[:2]) + B.shifted(*B.AREA[2:])
    w0 = B.Walker(edited, rect)
    extra = [(x, y, z, t) for (x, y, z, t, _) in farm if (x, y) != farm_door]
    extra += [(x, y, w0.ground(x, y), t) for (x, y, z, t, _) in props]
    w = B.Walker(edited, rect, extra)
    stops = [B.shifted(x, y) for (_, _, x, y) in B.P.STOPS]
    route = set()
    for a, b in zip(stops, stops[1:]):
        route |= {(s[0], s[1]) for s in w.path(a, b)}
    taken = {(x, y) for (x, y, *_r) in farm} | {(x, y) for (x, y, *_r) in props}
    gate = (6695, 3979)
    taken |= {farm_door, gate, (6695, 3978)} | {B.shifted(*c) for c in B.YARD_GATE} | set(pts.values())
    for r in info['rooms'].values():
        taken |= {B.shifted(*c) for c in r['floor'] | r['ring']}
    # the moongate frame and its glow: the landing and 4 tiles round the gate
    gx, gy = pts['Moongate']
    taken |= {(gx + a, gy + b) for a in range(-4, 5) for b in range(-4, 5)}
    # a door's approach line stays clear for two tiles (guide 2.4)
    for (dx_, dy_) in [B.shifted(*B.BANK_DOOR), (farm_door[0], farm_door[1])]:
        taken |= {(dx_, dy_ + k) for k in range(1, 3)}
    taken |= {(B.shifted(*B.LODGE_DOOR)[0], B.shifted(*B.LODGE_DOOR)[1] - k) for k in range(1, 3)}
    near_spot = {(p[0] + a, p[1] + b) for p in pts.values() for a in (-1, 0, 1) for b in (-1, 0, 1)}

    def north_of_path(c):
        south = any((c[0], c[1] + k) in road for k in range(1, REACH + 1))
        # the whole band: no road north of it in its own column or either side, nor beside it (a hole in the road
        # passed the column test alone: the yard's first pick)
        north = any((c[0] + a, c[1] - k) in road for a in (-1, 0, 1) for k in range(0 if a else 1, REACH + 1))
        return south and not north and c not in road

    chosen = {}
    for key, (sx, sy) in STOPS.items():
        cands = sorted(((max(abs(dx), abs(dy)), abs(dx) + abs(dy), dx, dy) for dx in range(-5, 6) for dy in range(-10, 3)
                        if (dx or dy)))
        for (_, _, dx, dy) in cands:
            c = (sx + dx, sy + dy)
            if not north_of_path(c) or c in route or c in taken or c in chosen.values():
                continue
            if c in near_spot and max(abs(dx), abs(dy)) > 1:
                continue
            z = w0.ground(*c)
            if not w.can_fit(c[0], c[1], z):
                continue
            w2 = B.Walker(edited, rect, extra + [(c[0], c[1], z, SIGN)] +
                          [(v[0], v[1], w0.ground(*v), SIGN) for v in chosen.values()])
            ok = all(w2.path(a, b) for a, b in zip(stops, stops[1:]))
            if ok:
                chosen[key] = c
                break
        print('%-14s stop %s  sign %s' % (key, (sx, sy), chosen.get(key)))
    chat_post = (6690, 3987)
    print('chat farm signpost', chat_post, 'north of path:', north_of_path(chat_post))
    print()
    for key, c in chosen.items():
        print('        "%s" => new Point2D(%d, %d),' % (key, c[0], c[1]))


if __name__ == '__main__':
    main()
