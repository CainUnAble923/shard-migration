"""cc-P481 (Chase 10-26: "make a new one"): the Wakening Isle as a new island painted in void C, built for the
tutorial. A design sketch, not a build: nothing here writes a map file.

The route is laid out first (stops 0 to 10, west to east, one way), then the land is shaped round it: a flat farm
meadow, a training yard, a trades square with the practice bank, the League lodge, a low knoll for the standing
stones and a dock with the moongate. The sea reaches at least SEA_MARGIN tiles past every walkable tile, so no player
on the isle ever sees the void's black edge or another zone.

Legs are walked on the sketch: 8 directions, a diagonal is one tile, no diagonal past a blocked corner (P605 found
the first sketch's walk allowed that), fences, walls, trees and stones block, doors and gates are open tiles.

  python -P newisle.py <out folder>     (MAPBUILD_CLIENT and MAPBUILD_ART as for isorender; the farm's pieces are read
                                         from the code work copy's TutorialFarmLayout.cs, SL_CODE or ../ShatteredLegacy)

Outputs: plan.png (top-down), where.png (void C and the Fold's zones), iso-farm.png and iso-east.png (in-client
style mocks; no shore transitions or hues yet), legs.txt.
"""
import collections, math, os, random, re, sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, HERE)
from mapbuild import isorender, uofiles, walls  # noqa: E402
import topdown  # noqa: E402

VOID_C = (6160, 1832, 6639, 2279)
SEA_MARGIN = 24              # more than the client's view range (18 to 24 tiles), so the void is never seen
GRASS = (0x0003, 0x0004, 0x0005, 0x0006)
SAND = (0x0016, 0x0017, 0x0018, 0x0019)
WATER = (0x00A8, 0x00A9, 0x00AA, 0x00AB)
DIRT = (0x0071, 0x0072, 0x0073, 0x0074)
FURROW = (0x0009, 0x000A, 0x000B)
COBBLE = (0x0442, 0x0443, 0x0444, 0x0445)  # cobblestones: the trades square
FLOOR = 0x04A9                              # wooden boards: bank and lodge floors
PLANK = 0x04A1                              # the dock deck
STONE_WALLS = {'ew': '0x001A', 'ns': '0x001B', 'corner': '0x001C', 'post': '0x001D'}  # checked on a 5 x 5 test room

# The farm (P276's approved layout) moves whole: every piece shifts by FARM_D, its height above the old ground kept.
FARM_D = (2890, -628)

# ---------------------------------------------------------------------------------------------- the route, first
STOPS = [  # num, label, x, y
    (0, 'wake on the beach; Tamsin', 6214, 2001),
    (1, 'walking tiles', 6222, 2000),
    (2, 'camp: backpack', 6232, 1998),
    (3, 'rack: paperdoll', 6241, 2000),
    (4, 'signpost: chat', 6268, 1998),
    (5, 'farm gate: Wren, Tobin', 6272, 1987),     # cc-P741: the field moved west (was 6290, 1987)
    (6, 'yard: echo, Sera', 6312, 2003),
    (7, 'bank: Merrin', 6338, 1989),
    (8, 'lodge: Elara', 6358, 2002),
    (9, 'stones: the vision', 6370, 1990),
    (10, 'moongate to New Haven', 6407, 1999),
]
# The road's own line (the stops sit on it or at a door beside it); the dock is planks after the last point.
# cc-P741: the jog north leads to the field's gate (moved west) and runs on past the farmhouse's steps (it went to
# the old gate at 6292, 1990, by way of 6286, 1995)
ROAD = [(6211, 2001), (6222, 2000), (6232, 1998), (6241, 1999), (6250, 1998), (6270, 1997), (6273, 1990),
        (6283, 1992), (6299, 1995), (6312, 2000), (6326, 1996), (6338, 1991), (6350, 1996), (6358, 2001),
        (6364, 1996), (6370, 1991), (6378, 1997), (6398, 1999)]
# Inside the farm, the lesson loop from the gate and back to it (pen, crop rows, the vet).
FARM_LOOP = [(6291, 1986), (6286, 1982), (6278, 1985), (6286, 1988), (6291, 1986)]

MEADOW = (6252, 1966, 6292, 1995)       # flat, Z 0, the farm inside it
YARD = (6302, 2002, 6324, 2018)          # training yard, low fence, gate on its north side
SQUARE = (6330, 1979, 6350, 1996)        # trades square, cobbles
BANK = (6334, 1981, 6342, 1987)          # floor tiles of the practice bank (walls ring them), door south
LODGE = (6354, 2004, 6362, 2010)         # floor tiles of the League lodge, door north
KNOLL = (6370, 1984, 4)                  # centre x, y, radius of the stone ring
DOCK = (6390, 1997, 6409, 2001)          # deck tiles over the water


def farm_pieces():
    code = os.environ.get('SL_CODE', os.path.join(os.path.dirname(REPO), 'ShatteredLegacy'))
    src = open(os.path.join(code, 'server', 'customizations', 'Tutorial', 'TutorialFarmLayout.cs')).read()
    rows = re.findall(r'\((0x[0-9A-Fa-f]+), (\d+), (\d+), (-?\d+)\), //', src)
    mf = uofiles.MapFile(uofiles.CLIENT, 1)
    out = []
    for tid, x, y, z in rows:
        x, y, z = int(x), int(y), int(z)
        ground = mf.get(x, y)[1]
        out.append((x + FARM_D[0], y + FARM_D[1], max(0, z - ground), int(tid, 16)))
    door = re.search(r'DoorSpot = new\((\d+), (\d+), (-?\d+)\)', src)
    dx, dy, dz = (int(v) for v in door.groups())
    out.append((dx + FARM_D[0], dy + FARM_D[1], max(0, dz - mf.get(dx, dy)[1]), 0x06AD))
    return out


def inside(r, x, y):
    return r[0] <= x <= r[2] and r[1] <= y <= r[3]


def build():
    """land {(x, y): (id, z)}, statics [(x, y, z, id)], blocked set, open set (doors and gates)."""
    rng = random.Random(4812)
    pts = [(x, y) for (_, _, x, y) in STOPS]
    # The island: every tile within a wobbling distance of the route, the meadow, the yards and a north wood.
    keep = []
    for (a, b) in zip(ROAD, ROAD[1:]):
        n = max(abs(a[0] - b[0]), abs(a[1] - b[1]))
        keep += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1)]
    blobs = [(6272, 1980, 26), (6313, 2010, 16), (6340, 1988, 17), (6300, 1962, 22), (6330, 1965, 18),
             (6358, 2006, 12), (6370, 1986, 13), (6240, 2010, 14)]
    land = {}
    walkable_box = [10 ** 6, 10 ** 6, -1, -1]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x1, y1 = min(xs) - 20 - SEA_MARGIN, min(ys) - 50 - SEA_MARGIN
    x2, y2 = max(xs) + 10 + SEA_MARGIN, max(ys) + 30 + SEA_MARGIN
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            d = min(math.hypot(x - px, y - py) - 11 for (px, py) in keep[::3])
            for (bx, by, br) in blobs:
                d = min(d, math.hypot(x - bx, y - by) - br)
            d -= 2.2 * math.sin(x / 7.0) + 1.8 * math.cos(y / 5.0 + x / 13.0)
            if d > 0:
                land[(x, y)] = (rng.choice(WATER), -5)
            elif d > -4:
                land[(x, y)] = (rng.choice(SAND), 0)
            else:
                land[(x, y)] = (rng.choice(GRASS), 0)
    statics, blocked, opened = [], set(), set()

    def dry(x, y):
        return land.get((x, y), (WATER[0],))[0] not in WATER

    # the road, three wide, over the stop points (the dock is planks)
    road = set()
    for (a, b) in zip(ROAD, ROAD[1:]):
        n = max(abs(a[0] - b[0]), abs(a[1] - b[1]))
        for i in range(n + 1):
            px = round(a[0] + (b[0] - a[0]) * i / n)
            py = round(a[1] + (b[1] - a[1]) * i / n)
            for ox in (-1, 0, 1):
                for oy in (-1, 0, 1):
                    if dry(px + ox, py + oy):
                        road.add((px + ox, py + oy))
    for t in road:
        land[t] = (rng.choice(DIRT), 0)
    # the meadow stays grass (the farm brings its own crop rows); the square is cobbles
    for x in range(SQUARE[0], SQUARE[2] + 1):
        for y in range(SQUARE[1], SQUARE[3] + 1):
            land[(x, y)] = (rng.choice(COBBLE), 0)
    # buildings: stone walls round a board floor, one door
    for rect, door in ((BANK, (6338, 1988)), (LODGE, (6358, 2003))):
        floor = {(x, y) for x in range(rect[0], rect[2] + 1) for y in range(rect[1], rect[3] + 1)}
        for t in floor:
            land[t] = (FLOOR, 0)
        st, ring = walls.walls_for(floor, set(), STONE_WALLS)
        for (x, y, z, tid, role) in st:
            if (x, y) == door:
                continue
            statics.append((x, y, 0, tid))
            blocked.add((x, y))
        land[door] = (FLOOR, 0)
        opened.add(door)
    # the training yard: low fence (the farm's fence art), gate on the north side by the road
    fence = []
    for x in range(YARD[0], YARD[2] + 1):
        fence += [(x, YARD[1], 0x0836), (x, YARD[3], 0x0836)]
    for y in range(YARD[1] + 1, YARD[3]):
        fence += [(YARD[0], y, 0x0837), (YARD[2], y, 0x0837)]
    for (x, y, tid) in fence:
        if y == YARD[1] and 6311 <= x <= 6313:
            opened.add((x, y))
            continue
        statics.append((x, y, 0, tid))
        blocked.add((x, y))
    for i, (x, y) in enumerate([(6306, 2007), (6309, 2007), (6306, 2011), (6309, 2011)]):
        statics.append((x, y, 0, 0x1070 + (i % 2) * 4))
        blocked.add((x, y))
    for (x, y) in ((6320, 2015), (6321, 2015)):
        statics.append((x, y, 0, 0x100A))
        blocked.add((x, y))
    statics += [(6317, 2008, 0, 0x0003)]          # the ankh by Sera (pinned's ankh art 0x0002-0x0005)
    blocked.add((6317, 2008))
    # the trades square: forge, anvil, loom, stalls (room for later trade tasters)
    for (x, y, tid) in ((6345, 1983, 0x0FB1), (6345, 1985, 0x0FAF), (6347, 1990, 0x1049), (6348, 1990, 0x104A)):
        statics.append((x, y, 0, tid))
        blocked.add((x, y))
    # the knoll and its standing stones: a rise to Z 8, a ring of rocks with a gap facing the road
    kx, ky, kr = KNOLL
    for x in range(kx - kr - 5, kx + kr + 6):
        for y in range(ky - kr - 5, ky + kr + 6):
            dd = math.hypot(x - kx, y - ky)
            if dry(x, y) and dd < kr + 5:
                land[(x, y)] = (land[(x, y)][0], int(max(0, min(8, (kr + 5 - dd) * 2))))
    for a in range(0, 360, 30):
        if 60 <= a <= 120:
            continue                                  # the gap, south, towards the road
        x = round(kx + kr * math.cos(math.radians(a)))
        y = round(ky + kr * math.sin(math.radians(a)))
        statics.append((x, y, land[(x, y)][1], 0x1772))
        blocked.add((x, y))
    # the dock: planks over the water, poles at the corners
    for x in range(DOCK[0], DOCK[2] + 1):
        for y in range(DOCK[1], DOCK[3] + 1):
            if not dry(x, y):
                statics.append((x, y, 0, PLANK))
                opened.add((x, y))
    for (x, y) in ((DOCK[2], DOCK[1]), (DOCK[2], DOCK[3])):
        statics.append((x, y, 0, 0x01CD))
        blocked.add((x, y))
    statics.append((6408, 1999, 0, 0x0F6C))      # the moongate (a server item in the build; drawn here for the mock)
    # the farm, moved whole
    for (x, y, z, tid) in farm_pieces():
        statics.append((x, y, z, tid))
    td = uofiles.read_tiledata(uofiles.CLIENT)[1]
    for (x, y, z, tid) in farm_pieces():
        if td[tid]['flags'] & 0x40 and tid != 0x06AD:
            blocked.add((x, y))
    gate = [(6289, 1986), (6289, 1987)]
    for t in gate:
        blocked.discard(t)
        opened.add(t)
    # woods: trees on the grass away from everything built
    keepout = set(road) | opened
    for r in (MEADOW, YARD, SQUARE, LODGE, DOCK):
        for x in range(r[0] - 3, r[2] + 4):
            for y in range(r[1] - 3, r[3] + 4):
                keepout.add((x, y))
    for x in range(kx - kr - 3, kx + kr + 4):
        for y in range(ky - kr - 3, ky + kr + 4):
            keepout.add((x, y))
    for (x, y), (tid, z) in list(land.items()):
        if tid in GRASS and (x, y) not in keepout and \
                not any((x + a, y + b) in keepout for a in (-2, 0, 2) for b in (-2, 0, 2)):
            k = rng.random()
            dens = 0.16 if y < 1975 else 0.05
            if k < dens:
                t = rng.choice([(0x0CDA, 0x0CDB), (0x0CDD, 0x0CDE), (0x0CE0, 0x0CE1), (0x0CD6, 0x0CD7)])
                statics += [(x, y, 0, t[0]), (x, y, 0, t[1])]
                blocked.add((x, y))
            elif k < dens + 0.05:
                statics.append((x, y, 0, rng.choice([0x0C9F, 0x0CA1, 0x0CA2, 0x0CA3])))
    walk_ok = {t for t, (tid, z) in land.items() if tid not in WATER} | opened
    walk_ok -= blocked
    xs = [t[0] for t in walk_ok]
    ys = [t[1] for t in walk_ok]
    box = (min(xs), min(ys), max(xs), max(ys))
    return land, statics, walk_ok, box, (x1, y1, x2, y2), road


def walk(ok, a, b, road=frozenset()):
    """Fewest steps (8 directions, no diagonal past a blocked corner); among equal walks, the one on the road."""
    import heapq
    best = {a: (0, 0)}
    prev = {a: None}
    q = [(0, 0, a)]
    while q:
        st, off, c = heapq.heappop(q)
        if c == b:
            break
        if (st, off) > best[c]:
            continue
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not (dx or dy):
                    continue
                n = (c[0] + dx, c[1] + dy)
                if n not in ok:
                    continue
                if dx and dy and ((c[0] + dx, c[1]) not in ok or (c[0], c[1] + dy) not in ok):
                    continue
                k = (st + 1, off + (n not in road))
                if n not in best or k < best[n]:
                    best[n] = k
                    prev[n] = c
                    heapq.heappush(q, (k[0], k[1], n))
    if b not in prev:
        return None
    out, c = [], b
    while c:
        out.append(c)
        c = prev[c]
    return out[::-1]


def colour(tid, z):
    if tid in WATER:
        return (20, 60, 110)
    if tid in SAND:
        return (214, 196, 140)
    if tid in DIRT:
        return (120, 92, 60)
    if tid in COBBLE:
        return (150, 150, 150)
    if tid == FLOOR:
        return (170, 130, 80)
    g = 112 + z * 6
    return (64, min(255, g), 48)


def plan_picture(out, land, statics, ok, box, area, road):
    td = uofiles.read_tiledata(uofiles.CLIENT)[1]
    x1, y1, x2, y2 = box[0] - 8, box[1] - 8, box[2] + 28, box[3] + 8
    s = 7
    im = Image.new('RGB', ((x2 - x1 + 1) * s, (y2 - y1 + 1) * s), (20, 60, 110))
    d = ImageDraw.Draw(im)
    for (x, y), (tid, z) in land.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            d.rectangle([(x - x1) * s, (y - y1) * s, (x - x1) * s + s - 1, (y - y1) * s + s - 1], fill=colour(tid, z))
    for (x, y, z, tid) in statics:
        if not (x1 <= x <= x2 and y1 <= y <= y2):
            continue
        nm = td[tid]['name']
        c = (30, 80, 30) if 'tree' in nm or 'leaves' in nm or 'needles' in nm else \
            (90, 90, 90) if 'stone' in nm or 'rock' in nm else (140, 100, 60)
        if tid == PLANK:
            c = (150, 115, 70)
        if tid == 0x0F6C:
            c = (90, 200, 255)
        d.rectangle([(x - x1) * s + 1, (y - y1) * s + 1, (x - x1) * s + s - 2, (y - y1) * s + s - 2], fill=c)
    zones = [
        ('flat farm meadow (P276 farm moved whole)', MEADOW, (140, 255, 120)),
        ('training yard', YARD, (255, 170, 90)),
        ('trades square', SQUARE, (220, 220, 220)),
        ('lodge', LODGE, (120, 200, 255)),
        ('dock', DOCK, (90, 220, 255)),
    ]
    plan = {'rect': [x1, y1, x2, y2], 'scale': s,
            'title': 'Wakening Isle, new island (the Fold, map 32, void C): one road west to east',
            'zones': [{'name': n, 'x1': r[0], 'y1': r[1], 'x2': r[2], 'y2': r[3], 'colour': list(c), 'alpha': 0}
                      for n, r, c in zones],
            'stops': []}
    im2, _, _ = topdown.draw_plan(im, plan)
    # redraw the walked route over the straight lines
    dd = ImageDraw.Draw(im2)
    legs = []
    pts = [(x, y) for (_, _, x, y) in STOPS]
    for (a, b, st) in zip(pts, pts[1:], STOPS[1:]):
        p = walk(ok, a, b, road)
        legs.append((st[0], st[1], len(p) - 1 if p else None))
        if p:
            dd.line([((x - x1) * s + s // 2, (y - y1) * s + s // 2) for (x, y) in p], fill=(255, 255, 255), width=2)
    loop = 0
    for a, b in zip(FARM_LOOP, FARM_LOOP[1:]):
        p = walk(ok, a, b, road)
        loop += len(p) - 1 if p else 0
        if p:
            dd.line([((x - x1) * s + s // 2, (y - y1) * s + s // 2) for (x, y) in p], fill=(255, 255, 120), width=1)
    total = sum(l[2] for l in legs if l[2])
    f = topdown.font(18)
    fl = topdown.font(16)
    for i, (n, label, x, y) in enumerate(STOPS):
        cx, cy = (x - x1) * s + s // 2, (y - y1) * s + s // 2
        r = 11
        dd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 30, 30), outline=(255, 255, 255), width=2)
        tw = dd.textlength(str(n), font=fl)
        dd.text((cx - tw / 2, cy - 10), str(n), fill=(255, 255, 255), font=fl)
        ty = cy - 34 if i % 2 == 0 else cy + 14
        dd.text((cx - 20, ty), label, fill=(255, 255, 255), font=fl, stroke_width=3, stroke_fill=(0, 0, 0))
    dd.rectangle([0, 0, im2.size[0], 30], fill=(0, 0, 0))
    dd.text((6, 5), plan['title'] + '   walked: %d tiles' % total, fill=(255, 255, 255), font=f)
    dd.rectangle([0, im2.size[1] - 52, im2.size[0], im2.size[1]], fill=(0, 0, 0))
    w, h = box[2] - box[0] + 1, box[3] - box[1] + 1
    dd.text((6, im2.size[1] - 48), 'Road walked: %d tiles, beach to moongate (white), plus %d inside the farm (yellow loop). '
            'Dry land and dock %d x %d tiles; sea %d+ tiles beyond every walkable tile.' % (total, loop, w, h, SEA_MARGIN),
            fill=(255, 255, 255), font=f)
    dd.text((6, im2.size[1] - 22), 'Sketch for the plan, not the build: tiles, shore transitions and decor come in F2 '
            'through the playbook. North is up.', fill=(200, 200, 200), font=f)
    im2.save(os.path.join(out, 'plan.png'), optimize=True)
    return legs, loop, total


def where_picture(out, land, box, area):
    x1, y1, x2, y2 = VOID_C
    s = 2
    im = Image.new('RGB', ((x2 - x1 + 1) * s, (y2 - y1 + 1) * s), (8, 8, 8))
    px = im.load()
    for (x, y), (tid, z) in land.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            for a in range(s):
                for b in range(s):
                    px[(x - x1) * s + a, (y - y1) * s + b] = colour(tid, z)
    plan = {'rect': [x1, y1, x2, y2], 'scale': s,
            'title': 'The Fold: void rectangle C of the Trammel map file (x 6160-6639, y 1832-2279)',
            'zones': [
                {'name': '1 Wakening Isle with its sea', 'x1': area[0], 'y1': area[1], 'x2': area[2], 'y2': area[3],
                 'colour': [255, 220, 80], 'alpha': 0},
                {'name': '2 Vision chamber', 'x1': 6440, 'y1': 1850, 'x2': 6463, 'y2': 1873,
                 'colour': [200, 140, 255], 'alpha': 60},
                {'name': '3 League private spaces', 'x1': 6480, 'y1': 1850, 'x2': 6630, 'y2': 2040,
                 'colour': [120, 200, 255], 'alpha': 30},
                {'name': '4 Events', 'x1': 6170, 'y1': 2125, 'x2': 6400, 'y2': 2270, 'colour': [255, 140, 100],
                 'alpha': 30},
                {'name': '5 Custom dungeons', 'x1': 6420, 'y1': 2060, 'x2': 6630, 'y2': 2270,
                 'colour': [140, 255, 160], 'alpha': 30},
            ], 'stops': []}
    im2, _, _ = topdown.draw_plan(im, plan)
    im2.save(os.path.join(out, 'where.png'), optimize=True)


def iso(out, name, land, statics, x1, y1, x2, y2, maxw=1500):
    sc_land = {(x, y): land.get((x, y), (WATER[0], -5)) for x in range(x1 - 1, x2 + 2) for y in range(y1 - 1, y2 + 2)}
    st = [s for s in statics if x1 <= s[0] <= x2 and y1 <= s[1] <= y2]
    im = isorender.render(isorender.Scene(sc_land, st), x1, y1, x2, y2)
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    isorender.save(im.convert('RGB'), os.path.join(out, name))


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    land, statics, ok, box, area, road = build()
    legs, loop, total = plan_picture(out, land, statics, ok, box, area, road)
    where_picture(out, land, box, area)
    lines = ['%2d %-42s %s' % l for l in legs]
    lines.append('road total %d, farm loop %d' % (total, loop))
    lines.append('walkable box %s (%d x %d); drawn area with sea %s (%d x %d)' % (
        box, box[2] - box[0] + 1, box[3] - box[1] + 1, area, area[2] - area[0] + 1, area[3] - area[1] + 1))
    lines.append('land tiles %d (dry %d), statics %d' % (len(land), sum(1 for v in land.values() if v[0] not in WATER),
                                                         len(statics)))
    open(os.path.join(out, 'legs.txt'), 'w', newline='\n').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    iso(out, 'iso-farm.png', land, statics, 6244, 1968, 6296, 2004)
    iso(out, 'iso-east.png', land, statics, 6328, 1978, 6412, 2012)


if __name__ == '__main__':
    main()
