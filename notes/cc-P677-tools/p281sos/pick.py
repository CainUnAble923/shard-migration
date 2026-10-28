# cc-P281: proposes, per hall, the main door, a travel stop outside it and guildmaster tiles inside, by the rules in the
# notes (read only). The picks in design/guild-halls/halls.json were chosen from this output and its maps, then checked
# by check.py.     python -P pick.py [key ...]   -> pick-<key>.txt (scratch, git-ignored)
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hallbase as H  # noqa: E402
import survey_halls as S  # noqa: E402
from walk import Walk  # noqa: E402


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def interior(W, rect, z, roofed=True):
    x1, y1, x2, y2 = rect
    out = set()
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for h in W.heights(x, y):
                if abs(h - z) <= 3 and (W.F.roof_over(x, y, h) or not roofed):
                    out.add((x, y, h))
    return out


def main_floor(W, rect):
    x1, y1, x2, y2 = rect
    c = collections.Counter()
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for h in W.heights(x, y):
                if W.F.roof_over(x, y, h):
                    c[h] += 1
    if not c:
        # no roof over the building (Castle British's keep, the open courts): the commonest standable height inside
        for x in range(x1 + 1, x2):
            for y in range(y1 + 1, y2):
                for h in W.heights(x, y):
                    c[h] += 1
        return c.most_common(1)[0][0], False
    return c.most_common(1)[0][0], True


def propose(key, fi, rect, kind, z=None, door=None):
    W = Walk(fi, rect)
    F = W.F
    out = ['%s (%s) %s rect %s' % (key, kind, H.FNAME[fi], rect)]
    mz, roofed = main_floor(W, rect)
    z = z if z is not None else mz
    out.append('main floor z %s' % z)
    signs = S.signs_in(fi, *W.box)
    doors = sorted(W.door_tiles())
    out.append('door tiles: %s' % doors)
    if door is None and doors:
        ref = (signs[0][1], signs[0][2]) if signs else ((rect[0] + rect[2]) // 2, rect[3])
        door = min(doors, key=lambda d: cheb(d, ref))
    out.append('main door %s (nearest the stock sign %s)' % (door, signs[0][1:4] if signs else None))
    inside = interior(W, rect, z, roofed)
    # outside: a tile 2 out from the door, on the side without a roof
    stop = None
    if door:
        for dx, dy in ((0, 2), (2, 0), (0, -2), (-2, 0), (2, 2), (-2, 2), (2, -2), (-2, -2)):
            t = (door[0] + dx, door[1] + dy)
            hs = W.heights(*t)
            if hs and not any(F.roof_over(t[0], t[1], h) for h in hs):
                stop = (t[0], t[1], min(hs, key=lambda h: abs(h - z)))
                break
    out.append('travel stop proposal %s' % (stop,))
    reach = W.flood(stop) if stop else set()
    inside_r = {t for t in inside if t in reach}
    out.append('interior tiles at the floor: %d, reachable from the stop: %d' % (len(inside), len(inside_r)))
    sp = H.spawns_in(H.FNAME[fi], *W.box)
    deco = [(d[0], d[1]) for d in H.decoration_in(fi, *W.box)]
    cands = []
    xy = {(t[0], t[1]) for t in inside_r}
    for (x, y, h) in inside_r:
        if any(cheb((x, y), d) < 3 for d in doors):
            continue
        if any(cheb((x, y), (s[1], s[2])) < 3 for s in sp):
            continue
        if any(cheb((x, y), d) < 2 for d in deco):
            continue
        free = sum(1 for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx or dy) and (x + dx, y + dy) in xy)
        dd = cheb((x, y), door) if door else 0
        cands.append((free * 10 - abs(dd - 5), x, y, h, free, dd))
    cands.sort(reverse=True)
    for c in cands[:8]:
        out.append('gm candidate %d,%d,%d free %d door dist %d score %d' % (c[1], c[2], c[3], c[4], c[5], c[0]))
    marks = {}
    for d in doors:
        marks[d] = 'D'
    for s in sp:
        marks[(s[1], s[2])] = 'S'
    for i, c in enumerate(cands[:5]):
        marks[(c[1], c[2])] = str(i + 1)
    if stop:
        marks[(stop[0], stop[1])] = 'T'
    for sg in signs:
        marks.setdefault((sg[1], sg[2]), 's')
    out.append(H.floormap(F, *W.box, z, marks=marks))
    return '\n'.join(out)


if __name__ == '__main__':
    want = set(sys.argv[1:])
    for key, fi, rect, kind in S.HALLS:
        if want and key not in want:
            continue
        t = propose(key, fi, rect, kind)
        open('pick-%s.txt' % key, 'w').write(t + '\n')
        print('\n'.join(t.split('\n')[:6] + [l for l in t.split('\n') if l.startswith('gm candidate')][:3]))
        print()
