"""cc-P720 item 3: where each lesson's signpost stands. The standing signpost (0xA854) is impassable, so it cannot stand
on the lesson's stop (P663's marker tile, which the road runs through and NPCs share). For each core lesson this picks
the first tile, nearest the stop, that is: within 2 tiles of the stop; off every walked leg of the route (build_isle's
gate paths) and off the road; not a server item's tile or spot, nor beside one; fits a 16-high person on the built
files (Walker.can_fit, pinned's CanFit); and leaves the stop reachable from both of its neighbours.

    python -P sign_spots.py <work folder>     prints the spots and the C# switch
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, os.path.join(REPO, 'notes', 'cc-P662-tools'))
import build_isle as B  # noqa: E402

# the stop each lesson's marker stood on (TutorialCorePlacement.MarkerSpot), isle coordinates
STOPS = {
    'core.movement': (6646, 3993), 'core.backpack': (6656, 3990), 'core.paperdoll': (6665, 3992),
    'core.chat': (6692, 3990), 'core.farm': (6714, 3979), 'core.death': (6736, 3995),
    'core.banking': (6762, 3981), 'core.league': (6782, 3994), 'core.loop': (6794, 3982),
    'core.travel': (6831, 3991)}
SIGN = 0xA854


def B_off(t, sx, sy, road):
    return (sx + t[3], sy + t[2]) not in road


def main():
    work = sys.argv[1]
    edited = os.path.join(work, 'edited')
    farm, props, pts, farm_door = B.server_items()
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
    # doors and gates are walked open by the gate, so their tiles look free: the bank's, the lodge's, the farmhouse's,
    # the field gate and the fence piece above it (TutorialFarm), the yard's 3-tile gate; and every spot itself
    taken |= {farm_door, (6713, 3979), (6713, 3978)} | {B.shifted(*c) for c in B.YARD_GATE} | set(pts.values())
    # inside a building (floor or wall ring) is never a sign's place: the lesson's sign stands outside its door
    for r in info['rooms'].values():
        taken |= {B.shifted(*c) for c in r['floor'] | r['ring']}
    near_spot = {(p[0] + a, p[1] + b) for p in pts.values() for a in (-1, 0, 1) for b in (-1, 0, 1)}
    chosen = {}
    for key, (sx, sy) in STOPS.items():
        cands = sorted(((abs(dx) + abs(dy), max(abs(dx), abs(dy)), dy, dx) for dx in range(-2, 3) for dy in range(-2, 3)
                        if (dx or dy)), key=lambda t: (t[1], t[0], -t[2], t[3]))
        # off the road first; a road-edge tile (off the walked route) only when nothing else is free
        for (_, _, dy, dx) in [t for t in cands if B_off(t, sx, sy, road)] + [t for t in cands if not B_off(t, sx, sy, road)]:
            c = (sx + dx, sy + dy)
            if c in route or c in taken or c in chosen.values():
                continue
            if c in near_spot and c not in {(sx + a, sy + b) for a in (-1, 0, 1) for b in (-1, 0, 1)}:
                continue
            z = w0.ground(*c)
            if not w.can_fit(c[0], c[1], z):
                continue
            # the sign in place: the stop must still be reached from the stops either side
            w2 = B.Walker(edited, rect, extra + [(c[0], c[1], z, SIGN)])
            i = [k for k, s in enumerate(stops) if abs(s[0] - sx) <= 2 and abs(s[1] - sy) <= 2]
            ok = True
            for k in i:
                for n in (k - 1, k + 1):
                    if 0 <= n < len(stops) and not w2.path(stops[k], stops[n]):
                        ok = False
            if ok and w2.path((sx, sy), stops[0] if key != 'core.movement' else stops[-1]) is None:
                ok = False
            if ok:
                chosen[key] = c
                break
        print('%-14s stop %s  sign %s' % (key, (sx, sy), chosen.get(key)))
    print()
    for key, c in chosen.items():
        print('        "%s" => new Point2D(%d, %d),' % (key, c[0], c[1]))


if __name__ == '__main__':
    main()
