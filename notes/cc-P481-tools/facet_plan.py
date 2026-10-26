"""cc-P481: the recommended direction's plan pictures. A design sketch, not a build: nothing here writes a map file.

  1. fold-zones.png   the whole void rectangle C of the Trammel map file (x 6160-6639, y 1832-2279; P24 2.1 found it
                      empty: void land 0x0244, 0 statics; recounted by P481) with the zones of "the Fold".
  2. fold-isle.png    the Wakening Isle, top-down: sand, grass, the dirt road, the farm, the stops and the walk,
                      each leg's length counted on foot over the sketch (8 directions, a diagonal is one tile).
  3. fold-isle-iso.png an in-client style mock of the arrival camp (stops 0 to 4), drawn by scripts/mapbuild/isorender
                      from the same sketch with a few stock statics. Hues are not applied (the tiles show untinted).

  python -P facet_plan.py <out folder>        (MAPBUILD_CLIENT and MAPBUILD_ART as for isorender)
"""
import collections, math, os, random, sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
sys.path.insert(0, HERE)
from mapbuild import isorender  # noqa: E402
from mapbuild.isorender import Scene, render  # noqa: E402
import topdown  # noqa: E402

VOID_C = (6160, 1832, 6639, 2279)
CX, CY = 6300, 2000          # isle centre
A_LEN, A_WID = 98, 44        # half length along the SW-NE axis, half width across it
GRASS, SAND, WATER, DIRT = (0x0003, 0x0004, 0x0005, 0x0006), (0x0016, 0x0017, 0x0018, 0x0019), \
    (0x00A8, 0x00A9, 0x00AA, 0x00AB), (0x0071, 0x0072, 0x0073, 0x0074)
R2 = math.sqrt(2)


def uv(x, y):
    """u runs south-west to north-east along the isle, v across it (south-east positive)."""
    dx, dy = x - CX, y - CY
    return (dx - dy) / R2, (dx + dy) / R2


def xy(u, v):
    return round(CX + (u + v) / R2), round(CY + (v - u) / R2)


STOPS = [  # (num, label, u, v)
    (0, 'wake on the shore, greeter', -90, 2),
    (1, 'walking tiles', -80, 0),
    (2, 'backpack', -71, 5),
    (3, 'paperdoll', -63, -4),
    (4, 'chat', -54, 2),
    (5, 'farm gate: pet, pests, vet', -32, 2),
    (6, 'shrine: echo and Sera', -6, -6),
    (7, 'practice bank', 16, 4),
    (8, 'League lodge (Elara)', 36, -4),
    (9, 'standing stones: vision', 58, 2),
    (10, 'pier moongate to New Haven', 90, 0),
]
FARM_W, FARM_H = 24, 27      # P276's farm footprint (x 3388-3411, y 2600-2626), axis-aligned like the addon


def farm_rect():
    gx, gy = xy(-32, 2)
    return gx - 2, gy + 2, gx - 2 + FARM_W - 1, gy + 2 + FARM_H - 1


def isle():
    """{(x, y): land id} for the sketch, plus the road tiles and blocked tiles."""
    rng = random.Random(481)
    land, road, blocked = {}, set(), set()
    x1, y1, x2, y2 = CX - 110, CY - 110, CX + 110, CY + 110
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            u, v = uv(x, y)
            wob = 0.06 * math.sin(u / 9.0) + 0.05 * math.cos(v / 7.0 + u / 23.0)
            r = (u / A_LEN) ** 2 + (v / A_WID) ** 2 - wob
            if r > 1.0:
                land[(x, y)] = rng.choice(WATER)
            elif r > 0.80:
                land[(x, y)] = rng.choice(SAND)
            else:
                land[(x, y)] = rng.choice(GRASS)
    pts = [xy(u, v) for (_, _, u, v) in STOPS]
    for (a, b) in zip(pts, pts[1:]):
        n = max(abs(a[0] - b[0]), abs(a[1] - b[1]))
        for i in range(n + 1):
            px = round(a[0] + (b[0] - a[0]) * i / max(n, 1))
            py = round(a[1] + (b[1] - a[1]) * i / max(n, 1))
            for ox in (-1, 0, 1):
                for oy in (-1, 0, 1):
                    t = (px + ox, py + oy)
                    if land.get(t) not in WATER:
                        road.add(t)
                        land[t] = rng.choice(DIRT)
    # the pier: dirt over the water from the last stop to the gate's dock end is drawn as road on sand
    fx1, fy1, fx2, fy2 = farm_rect()
    for x in range(fx1, fx2 + 1):
        for y in range(fy1, fy2 + 1):
            if (x, y) not in road:
                land[(x, y)] = rng.choice(DIRT)
            if (x in (fx1, fx2) or y in (fy1, fy2)) and not (y == fy1 and x <= fx1 + 4):
                blocked.add((x, y))   # the fence, with its gate at the north-west corner by the road
    return land, road, blocked


def walk(land, blocked, a, b):
    ok = lambda t: t in land and land[t] not in WATER and t not in blocked
    prev = {a: None}
    q = collections.deque([a])
    while q:
        c = q.popleft()
        if c == b:
            break
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (c[0] + dx, c[1] + dy)
                if (dx or dy) and n not in prev and ok(n):
                    prev[n] = c
                    q.append(n)
    if b not in prev:
        return None
    out, c = [], b
    while c:
        out.append(c)
        c = prev[c]
    return out[::-1]


def colour(tid):
    if tid in WATER:
        return (20, 60, 110)
    if tid in SAND:
        return (214, 196, 140)
    if tid in DIRT:
        return (120, 92, 60)
    if tid in GRASS:
        return (64, 112, 48)
    return (0, 0, 0)


def zones_picture(out):
    x1, y1, x2, y2 = VOID_C
    s = 2
    im = Image.new('RGB', ((x2 - x1 + 1) * s, (y2 - y1 + 1) * s), (8, 8, 8))
    land, _, _ = isle()
    px = im.load()
    for (x, y), t in land.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            for a in range(s):
                for b in range(s):
                    px[(x - x1) * s + a, (y - y1) * s + b] = colour(t)
    plan = {'rect': [x1, y1, x2, y2], 'scale': s,
            'title': 'The Fold: server map 32 on the Trammel map file, void rectangle C (480 x 448)',
            'zones': [
                {'name': '1 Wakening Isle (tutorial), 220 x 220 with its sea', 'x1': CX - 110, 'y1': CY - 110,
                 'x2': CX + 110, 'y2': CY + 110, 'colour': [255, 220, 80], 'alpha': 0},
                {'name': '2 Vision chamber 24 x 24', 'x1': 6440, 'y1': 1850, 'x2': 6463, 'y2': 1873,
                 'colour': [200, 140, 255], 'alpha': 60},
                {'name': '3 League private spaces (ch. 6, the Setting)', 'x1': 6480, 'y1': 1850, 'x2': 6630,
                 'y2': 2040, 'colour': [120, 200, 255], 'alpha': 30},
                {'name': '4 Events', 'x1': 6170, 'y1': 2125, 'x2': 6400, 'y2': 2270, 'colour': [255, 140, 100],
                 'alpha': 30},
                {'name': '5 Custom dungeons', 'x1': 6420, 'y1': 2060, 'x2': 6630, 'y2': 2270,
                 'colour': [140, 255, 160], 'alpha': 30},
            ], 'stops': []}
    im2, _, _ = topdown.draw_plan(im, plan)
    im2.save(os.path.join(out, 'fold-zones.png'), optimize=True)


def isle_picture(out):
    land, road, blocked = isle()
    x1, y1, x2, y2 = CX - 110, CY - 100, CX + 110, CY + 100
    s = 4
    im = Image.new('RGB', ((x2 - x1 + 1) * s, (y2 - y1 + 1) * s))
    d = ImageDraw.Draw(im)
    for (x, y), t in land.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            c = (150, 110, 70) if (x, y) in blocked else colour(t)
            d.rectangle([(x - x1) * s, (y - y1) * s, (x - x1) * s + s - 1, (y - y1) * s + s - 1], fill=c)
    stops = []
    legs = []
    pts = [xy(u, v) for (_, _, u, v) in STOPS]
    for i, (num, label, u, v) in enumerate(STOPS):
        stops.append({'num': num, 'label': label, 'at': list(pts[i]), 'straight': True})
    for a, b, st in zip(pts, pts[1:], STOPS[1:]):
        p = walk(land, blocked, a, b)
        legs.append((st[1], len(p) - 1 if p else None))
    fx1, fy1, fx2, fy2 = farm_rect()
    plan = {'rect': [x1, y1, x2, y2], 'scale': s,
            'title': 'Wakening Isle (the Fold, map 32): one road, south-west to north-east',
            'zones': [{'name': 'farm (P276 layout, moved)', 'x1': fx1, 'y1': fy1, 'x2': fx2,
                       'y2': fy2, 'colour': [120, 255, 120], 'alpha': 0}],
            'stops': stops}
    im2, _, _ = topdown.draw_plan(im, plan)
    total = sum(l[1] for l in legs[:-1] if l[1]) + (legs[-1][1] or 0)
    dd = ImageDraw.Draw(im2)
    f = topdown.font(14)
    dd.rectangle([0, 0, im2.size[0], 24], fill=(0, 0, 0))
    dd.text((6, 4), plan['title'] + '   walk: %d tiles, arrival to moongate (counted on the sketch)' % total,
            fill=(255, 255, 255), font=f)
    im2.save(os.path.join(out, 'fold-isle.png'), optimize=True)
    return legs, total


def iso_mock(out):
    land, road, blocked = isle()
    a, b = xy(-94, 0), xy(-52, 0)
    x1, y1 = min(a[0], b[0]) - 3, min(a[1], b[1]) - 3
    x2, y2 = max(a[0], b[0]) + 3, max(a[1], b[1]) + 3
    sc_land = {}
    for x in range(x1 - 1, x2 + 2):
        for y in range(y1 - 1, y2 + 2):
            t = land.get((x, y), WATER[0])
            sc_land[(x, y)] = (t, -5 if t in WATER else 0)
    st = []
    rng = random.Random(4811)

    def put(u, v, tid, z=0):
        st.append((*xy(u, v), z, tid))
    m1, m2 = xy(-80, 0), xy(-80, 2)
    st += [(m1[0], m1[1], 0, 0x050E), (m2[0], m2[1], 0, 0x050E)]           # the two walking tiles
    put(-90, 4, 0x0B97)                                                       # signpost where the greeter stands
    put(-71, 8, 0x0DE3)                                                       # campfire, the backpack camp
    put(-73, 10, 0x0A55)
    put(-69, 10, 0x0A56)
    put(-63, -8, 0x0B98)                                                      # paperdoll: a sign by the road
    put(-54, 6, 0x0B9B)                                                       # chat: the metal signpost
    for _ in range(140):
        u, v = rng.uniform(-100, -40), rng.uniform(-40, 40)
        x, y = xy(u, v)
        if not (x1 <= x <= x2 and y1 <= y <= y2):
            continue
        near_road = any((x + dx, y + dy) in road for dx in (-1, 0, 1) for dy in (-1, 0, 1))
        if land.get((x, y)) in GRASS and not near_road and (u / A_LEN) ** 2 + (v / A_WID) ** 2 < 0.7:
            k = rng.random()
            if k < 0.35:   # an oak is a trunk and its leaves on the same tile
                t = rng.choice([(0x0CDA, 0x0CDB), (0x0CDD, 0x0CDE)])
                st += [(x, y, 0, t[0]), (x, y, 0, t[1])]
            else:
                st.append((x, y, 0, rng.choice([0x0C9F, 0x0CA1, 0x0CA2, 0x0CA3])))
    sc = Scene(sc_land, st)
    im = render(sc, x1, y1, x2, y2)
    isorender.save(im, os.path.join(out, 'fold-isle-iso.png'))


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    zones_picture(out)
    legs, total = isle_picture(out)
    for l in legs:
        print('%-32s %s' % l)
    print('total', total)
    iso_mock(out)


if __name__ == '__main__':
    main()
