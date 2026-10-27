"""cc-P662 (P481 F2): builds the Wakening Isle into a SCRATCH copy of the Trammel files and makes the map patch.

The plan is P481 section 11.2's (notes/cc-P481-tools/newisle.py: the route, the stops, the zones and the island's
shape, all in void C's coordinates); this driver adds one constant shift (P673 section 1.4, site A: +424, +1992), so
the plan and the build cannot drift apart. The look is isle-sets.json beside this file (seeds, weights, every id
measured on stock Trammel by the survey scripts here); nothing about the look is in this code.

    python -P build_isle.py <work folder> [--plan-only] [--fresh] [--base <pristine folder>] [--ship]

  <work folder>  holds ORIGINAL-SHA256.txt (the pristine base's hashes), edited/ (the scratch build) and the patch
  --plan-only    writes the CSVs and plan-cells.json, touches no map file
  --fresh        rebuilds edited/ from the pristine base plus the shipped trammel.mapops with every line inside the
                 isle's drawn area dropped, so a rebuild never stacks on an old one (P413's review)
  --base         the pristine Trammel folder: stock now (MAPBUILD_CLIENT, D:/UO/UltimaOnlineVanilla), the SoS file
                 after P675 (S2); only the fingerprints of the isle's lines change, the island does not (site A is
                 void in both)
  --ship         writes the patch into the code copy (SL_CODE, default ../ShatteredLegacy beside this repo):
                 player-package/vendor/shattered-legacy-map/trammel.mapops

The farm addon, every NPC, door, lesson prop and the moongate are server items (P663, TutorialCorePlacement and
TutorialIsleFarmLayout); this build keeps their tiles clear and the gate walks with them in place.
"""
import collections, csv, hashlib, json, math, os, random, re, shutil, subprocess, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, os.path.join(REPO, 'notes', 'cc-P481-tools'))
from mapbuild import uofiles, walls as W, scatter as S, audit, mapops  # noqa: E402
import newisle as P  # noqa: E402  (the plan: STOPS, ROAD, FARM_LOOP, MEADOW, YARD, SQUARE, BANK, LODGE, KNOLL, DOCK)

RULES = json.load(open(os.path.join(HERE, 'isle-sets.json'), encoding='utf-8'))
CELLS = os.path.join(HERE, 'plan-cells.json')
CLIENT = uofiles.CLIENT
FACET = 1
DX, DY = RULES['shift']
AREA = (6170, 1913, 6441, 2057)                          # the drawn area with its sea (P481 11.2, void C)
SL_CODE = os.environ.get('SL_CODE', os.path.join(os.path.dirname(REPO), 'ShatteredLegacy'))
PATCH_REL = os.path.join('player-package', 'vendor', 'shattered-legacy-map', 'trammel.mapops')

# The buildings (P481 11.2): floor rects from the plan, one door each, at P663's door spots (TutorialWorld.BankDoor
# 6762,3980 and LodgeDoor 6782,3995, less the shift).
BANK_DOOR = (6338, 1988)
LODGE_DOOR = (6358, 2003)
YARD_GATE = [(6311, 2002), (6312, 2002), (6313, 2002)]
# The dock's end: a stone landing at the deck's height holds the moongate and the dock-end stop, so P663's spots
# (TutorialWorld.DockEnd 6831,3991 and Moongate 6832,3991) stand on land: its seeder's CanFit reads the land's
# average Z, which over the open sea is -5, under the planks.
LANDING = (6405, 1997, 6409, 2001)
LANDING_Z = -2

IMP, WET, SURF, BRIDGE, WALL = 0x40, 0x80, 0x200, 0x400, 0x10


def shifted(x, y):
    return x + DX, y + DY


def cells(r):
    return [(x, y) for x in range(r[0], r[2] + 1) for y in range(r[1], r[3] + 1)]


def stream(stage):
    """One random stream per stage (playbook section 5)."""
    return random.Random(RULES['seed'] ^ zlib.crc32(stage.encode()))


def hx(v):
    return int(v, 16) if isinstance(v, str) else int(v)


def table(t):
    return {hx(k): v for k, v in t.items() if not k.startswith('_')}


def code_file(rel, must):
    """A file of the code copy holding `must` (a regex), else main's, else (P663 not merged yet) the branch's that
    added it."""
    p = os.path.join(SL_CODE, rel)
    if os.path.exists(p):
        text = open(p, encoding='utf-8').read()
        if re.search(must, text):
            return text
    for ref in ('origin/main', 'golem/Iron/P663', 'origin/golem/Iron/P663'):
        r = subprocess.run(['git', '-C', SL_CODE, 'show', '%s:%s' % (ref, rel.replace(os.sep, '/'))],
                           capture_output=True, text=True, encoding='utf-8')
        if r.returncode == 0 and re.search(must, r.stdout):
            return r.stdout
    raise FileNotFoundError(rel)


def server_items():
    """P663's server items on the isle, in the isle's (shifted) coordinates: [(x, y, z, id, what)] and the spots its
    seeder fit-checks {name: (x, y)}. Read from TutorialWorld.cs, TutorialCorePlacement.cs, TutorialFarm.cs and
    TutorialIsleFarmLayout.cs, so the gate walks the isle as the server will hold it."""
    tw = code_file(os.path.join('server', 'customizations', 'Tutorial', 'TutorialWorld.cs'), r'DockEnd')
    pts = {m.group(1): (int(m.group(2)), int(m.group(3)))
           for m in re.finditer(r'public static readonly Point2D (\w+) = new\((\d+), (\d+)\)', tw)}
    lay = code_file(os.path.join('server', 'customizations', 'Tutorial', 'TutorialIsleFarmLayout.cs'), r'Pieces')
    farm = [(int(x), int(y), int(z), int(t, 16), 'farm') for t, x, y, z in
            re.findall(r'\((0x[0-9A-Fa-f]+), (\d+), (\d+), (-?\d+)\), //', lay)]
    fs = code_file(os.path.join('server', 'customizations', 'Tutorial', 'TutorialFarm.cs'), r'FarmhandSpot = OnIsle')
    shift = tuple(int(v) for v in re.search(r'Shift = new\((\d+), (\d+)\)', lay).groups())
    for name in ('FarmhandSpot', 'FarmVetSpot', 'PestSpot'):
        m = re.search(name + r' = OnIsle\(new Point2D\((\d+), (\d+)\)\)', fs)
        pts[name] = (int(m.group(1)) + shift[0], int(m.group(2)) + shift[1])
    cp = code_file(os.path.join('server', 'customizations', 'Tutorial', 'TutorialCorePlacement.cs'), r'TutorialWorld\.Camp')
    props = []
    for m in re.finditer(r'\((0x[0-9A-Fa-f]+), new Point2D\(TutorialWorld\.(\w+)\.X( [+-] \d+)?, TutorialWorld\.\w+\.Y( [+-] \d+)?\), "([^"]+)"\)', cp):
        bx, by = pts[m.group(2)]
        ox = int(m.group(3).replace(' ', '')) if m.group(3) else 0
        oy = int(m.group(4).replace(' ', '')) if m.group(4) else 0
        props.append((bx + ox, by + oy, None, int(m.group(1), 16), m.group(5)))
    for m in re.finditer(r'\((0x[0-9A-Fa-f]+), TutorialWorld\.(\w+), "([^"]+)"\)', cp):
        bx, by = pts[m.group(2)]
        props.append((bx, by, None, int(m.group(1), 16), m.group(3)))
    door = re.search(r'DoorSpot = new\((\d+), (\d+), (-?\d+)\)', lay)
    return farm, props, pts, (int(door.group(1)), int(door.group(2)))


# ------------------------------------------------------------------------------------------------ the plan

DOCK_SHORE_X = 6384      # the route's points east of this do not shape the land: the sea reaches the dock


def shape():
    """newisle.build()'s island shape: land within a wobbling distance of the route and eight lobes. One change: the
    route's points east of DOCK_SHORE_X are left out, because round the road's last point (6398, 1999) they made dry
    land out to x 6409, so the sketch's dock stood on land; without them the east shore falls near x 6390."""
    keep = []
    for (a, b) in zip(P.ROAD, P.ROAD[1:]):
        n = max(abs(a[0] - b[0]), abs(a[1] - b[1]))
        keep += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1)]
    blobs = [(6272, 1980, 26), (6313, 2010, 16), (6340, 1988, 17), (6300, 1962, 22), (6330, 1965, 18),
             (6358, 2006, 12), (6370, 1986, 13), (6240, 2010, 14)]
    d = {}
    for (x, y) in cells(AREA):
        v = min(math.hypot(x - px, y - py) - 11 for (px, py) in keep[::3] if px <= DOCK_SHORE_X)
        for (bx, by, br) in blobs:
            v = min(v, math.hypot(x - bx, y - by) - br)
        v -= 2.2 * math.sin(x / 7.0) + 1.8 * math.cos(y / 5.0 + x / 13.0)
        # the yard, the square, the bank and the lodge stand on dry ground with a 4-tile margin before the sand
        # starts (junction sheet round 1: the yard's south-east fence corner stood in the sea)
        for r in (P.YARD, P.SQUARE, P.BANK, P.LODGE):
            if r[0] - 4 <= x <= r[2] + 4 and r[1] - 4 <= y <= r[3] + 4:
                v = min(v, -8)
        d[(x, y)] = v
    return d, blobs


def chebyshev(sources, within):
    """Chebyshev distance from a set of tiles over `within` (multi-source BFS, 8 neighbours)."""
    dist = {c: 0 for c in sources}
    q = collections.deque(sources)
    while q:
        c = q.popleft()
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                n = (c[0] + a, c[1] + b)
                if n in within and n not in dist:
                    dist[n] = dist[c] + 1
                    q.append(n)
    return dist


def road_tiles(dry, brush=((-1, 0, 1), lambda ox, oy: True)):
    """newisle's road: a brush along the route's line over dry land (3 x 3 by default, the walked road)."""
    offs, keep = brush
    road = set()
    for (a, b) in zip(P.ROAD, P.ROAD[1:]):
        n = max(abs(a[0] - b[0]), abs(a[1] - b[1]))
        for i in range(n + 1):
            px = round(a[0] + (b[0] - a[0]) * i / n)
            py = round(a[1] + (b[1] - a[1]) * i / n)
            for ox in offs:
                for oy in offs:
                    if keep(ox, oy) and (px + ox, py + oy) in dry:
                        road.add((px + ox, py + oy))
    return road


# the road's dirt: the walked road's 3 x 3 brush; the transition pass grows it where the route jogs (render round 1:
# without the growth the corner rule left a broken line of blotches; a radius 2.2 brush made it 5 wide, round 2)
DIRT_BRUSH = ((-1, 0, 1), lambda ox, oy: True)


def corners_of(cls, x, y, mine, mates):
    """The tile's corner pattern (top, right, bottom, left): a corner is this tile's class letter when every tile round
    that vertex is in `mates`, else 'g' (grass)."""
    around = {'t': [(-1, -1), (0, -1), (-1, 0), (0, 0)], 'r': [(0, -1), (1, -1), (1, 0), (0, 0)],
              'b': [(1, 0), (1, 1), (0, 1), (0, 0)], 'l': [(-1, 0), (-1, 1), (0, 1), (0, 0)]}
    out = ''
    for k in 'trbl':
        out += mine if all(cls.get((x + a, y + b), 'w') in mates for a, b in around[k]) else 'g'
    return out


def plan(farm, props, pts, quiet=False):
    """Returns land {(x, y): (id, z)} and statics [(x, y, z, id, why)] in the plan's (void C) coordinates, plus the
    report: zones, rooms, corner log, wall tiles, keep-clear tiles."""
    L = RULES['land']
    items = uofiles.read_tiledata(CLIENT)[1]
    report = collections.OrderedDict()
    d, blobs = shape()
    water = {c for c, v in d.items() if v > 0}
    dry = set(d) - water
    dw = chebyshev(water, set(d))
    # 1. classes: sand rim (P481: 4 tiles, and never less than 3 from the sea so a transition never touches water),
    #    grass inside, the road dirt where it is 2+ from the sand (on the beach the path stays sand), the square paved
    cls = {}
    for c in d:
        if c in water:
            cls[c] = 'w'
        elif d[c] > -4 or dw[c] <= 2:
            cls[c] = 's'
        else:
            cls[c] = 'g'
    road = road_tiles(dry)
    ds = chebyshev({c for c in cls if cls[c] == 's'}, set(d))
    laid = set()
    for c in road_tiles(dry, DIRT_BRUSH):
        if cls[c] == 'g' and ds[c] >= 2:
            cls[c] = 'd'
            laid.add(c)
    # the transition pass may grow the road only this far (render round 3: unbounded, it wandered into the meadow)
    may_grow = {(c[0] + a, c[1] + b) for c in laid for a in (-1, 0, 1) for b in (-1, 0, 1)}
    for c in cells(P.SQUARE):
        cls[c] = 'p'
    bank_floor = set(cells(P.BANK))
    lodge_floor = set(cells(P.LODGE))
    bank_ring = W.ring_of(bank_floor)
    lodge_ring = W.ring_of(lodge_floor)
    for c in lodge_floor | lodge_ring:
        cls[c] = 'd'
    yard = set(cells(P.YARD))
    for c in yard:
        cls[c] = 'd'
    landing = set(cells(LANDING))
    for c in landing:
        cls[c] = 'p'
    for c in bank_floor | bank_ring:
        assert cls[c] == 'p', ('the bank stands on the square', c)
    # 2. transitions: sand and dirt tiles take the stock tile for their corner pattern; a pattern with no stock tile
    #    (the two diagonal saddles, and dirt's three-dirt-one-grass-at-the-bottom) turns the tile to grass, until none
    sg = {k: [hx(v) for v in vs] for k, vs in L['sandGrass'].items()}
    dg = {k: [hx(v) for v in vs] for k, vs in L['dirtGrass'].items()}
    changed = True
    rounds = 0
    pat = {}
    never_dirt = set()
    while changed:
        changed = False
        rounds += 1
        for c in sorted(cls):
            k = cls[c]
            if k == 's':
                p = corners_of(cls, c[0], c[1], 's', ('s', 'w'))
                if 'g' in p and p not in sg:
                    cls[c] = 'g'; changed = True
                else:
                    pat[c] = p
            elif k == 'd':
                p = corners_of(cls, c[0], c[1], 'a', ('d', 'p')).replace('g', 'b')
                if 'b' in p and p not in dg:
                    # grow the road over the grass corner (turning the tile to grass instead ate the road from one
                    # side, round after round: render round 1); away from the sand only
                    grown = False
                    for i, k2 in enumerate('trbl'):
                        if p[i] != 'b':
                            continue
                        for (a, b) in {'t': [(-1, -1), (0, -1), (-1, 0)], 'r': [(0, -1), (1, -1), (1, 0)],
                                       'b': [(1, 0), (1, 1), (0, 1)], 'l': [(-1, 0), (-1, 1), (0, 1)]}[k2]:
                            n = (c[0] + a, c[1] + b)
                            if cls.get(n) == 'g' and ds.get(n, 0) >= 2 and n not in never_dirt and n in may_grow:
                                cls[n] = 'd'; grown = True
                    if not grown:
                        cls[c] = 'g'
                        never_dirt.add(c)       # monotone: dirt only grows, and a tile turned to grass stays grass
                    changed = True
                else:
                    pat[c] = p
    report['transition rounds'] = rounds
    rng = stream('land')
    land = {}
    tcount = collections.Counter()
    for c in sorted(cls):
        k = cls[c]
        if k == 'w':
            land[c] = (S.weighted(rng, table(L['water'])), L['seaZ'])
        elif k == 's':
            p = pat[c]
            tid = rng.choice(sg[p]) if 'g' in p else S.weighted(rng, table(L['sand']))
            tcount['sand-grass' if 'g' in p else 'sand'] += 1
            land[c] = (tid, L['beachZ'].get(str(dw[c]), 0))
        elif k == 'd':
            p = pat[c]
            tid = rng.choice(dg[p]) if 'b' in p else S.weighted(rng, table(L['dirt']))
            tcount['dirt-grass' if 'b' in p else 'dirt'] += 1
            land[c] = (tid, 0)
        elif k == 'p':
            land[c] = (S.weighted(rng, table(L['stone'])), LANDING_Z if c in landing else 0)
            tcount['paving'] += 1
        else:
            land[c] = (S.weighted(rng, table(L['grass'])), 0)
            tcount['grass'] += 1
    report['land'] = dict(tcount)
    # 3. the knoll: a rise to Z 8 round the stone ring (newisle's profile), on dry land only
    kx, ky, kr = P.KNOLL
    for c in cells((kx - kr - 5, ky - kr - 5, kx + kr + 5, ky + kr + 5)):
        dd = math.hypot(c[0] - kx, c[1] - ky)
        if c in dry and cls[c] in ('g', 'd') and dd < kr + 5:
            # tapered to 0 two tiles from the sand (render round 3: the rise met the beach's dip under the shore
            # water and left a black wedge at the knoll's north shore)
            land[c] = (land[c][0], int(max(0, min(8, (kr + 5 - dd) * 2, 2 * (ds[c] - 2)))))

    statics = []
    by_tile = collections.defaultdict(list)

    def put(x, y, z, tid, why):
        statics.append((x, y, z, tid, why))
        by_tile[(x, y)].append(tid)

    # the tiles P663's server items stand on, and their neighbours: no static of ours goes there
    def unshift(c):
        return c[0] - DX, c[1] - DY
    spots = {k: unshift(v) for k, v in pts.items()}
    server_tiles = {unshift((s[0], s[1])) for s in farm} | {unshift((s[0], s[1])) for s in props}
    spot_tiles = set(spots.values()) | server_tiles     # nothing impassable of ours on these (the assertion below)
    keep_clear = set(server_tiles)                        # no decor of ours on these or beside a spot
    for c in spots.values():
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                keep_clear.add((c[0] + a, c[1] + b))

    # 4. the bank and the lodge: stone walls by the run rule, the door tile an opening (OSI's stone town doors: floor
    #    static on the door tile, run pieces either side, the door a server item), floors, the slate roof over the
    #    visible room, every inner corner dressed
    stone = RULES['walls']['stone']
    rooms = {}
    corner_log = {}
    wall_tiles = {}
    rngc = stream('corners')
    C = RULES['corners']
    for name, floor, door, ftable in (('bank', bank_floor, BANK_DOOR, RULES['floors']['bank']),
                                      ('lodge', lodge_floor, LODGE_DOOR, RULES['floors']['lodge'])):
        ring = W.ring_of(floor) - {door}
        Wt = lambda c, ring=ring: c in ring
        for (x, y) in sorted(ring):
            for tid, role in W.wall_pieces(Wt, x, y, stone):
                put(x, y, 0, tid, '%s wall %s' % (name, role))
            wall_tiles[(x, y)] = 'stone'
        rf = stream('floor ' + name)
        for (x, y) in sorted(floor | {door}):
            put(x, y, 0, S.pick_unlike(rf, table(ftable), (x, y), by_tile), '%s floor' % name)
        xs = [c[0] for c in floor]; ys = [c[1] for c in floor]
        x1, x2, y1, y2 = min(xs), max(xs), min(ys), max(ys)
        for (x, y) in cells((x1, y1, x2 + 1, y2 + 1)):
            put(x, y, RULES['roof']['z'], hx(RULES['roof']['id']), '%s roof' % name)
        # corners: NW torch on the north wall and a seat; NE a piece on the east strip; SW a torch on the west wall
        # and a piece on the south strip; SE two pieces, one on each strip
        log = collections.Counter()
        dressing = {
            'NW': [((x1, y1), 13, rngc.choice([hx(v) for v in C['torchNorth']]), 'torch north wall'),
                   ((x1, y1), 0, None, 'seat')],
            'NE': [((x2 + 1, y1), 0, 'strip', 'strip')],
            'SW': [((x1, y2), 13, rngc.choice([hx(v) for v in C['torchWest']]), 'torch west wall'),
                   ((x1, y2 + 1), 0, 'strip', 'strip')],
            'SE': [((x2 + 1, y2), 0, 'strip', 'strip'), ((x2, y2 + 1), 0, 'strip', 'strip')],
        }
        for corner, pieces in dressing.items():
            log['concave'] += 1
            placed = 0
            for (c, z, tid, what) in pieces:
                if c in keep_clear or c == door:
                    continue
                if tid is None:
                    tid = S.pick_unlike(rngc, table(C['floorPieces']), c, by_tile)
                elif tid == 'strip':
                    tid = S.pick_unlike(rngc, table(C['stripPieces']), c, by_tile)
                put(c[0], c[1], z, tid, '%s corner %s %s' % (name, corner, what))
                placed += 1
            if placed:
                log['concave dressed'] += 1
        corner_log[name] = log
        rooms[name] = dict(floor=floor, ring=ring, door=door)
    report['corners'] = corner_log

    # 5. fences: the training yard (gate on the north side, by the road) and the meadow (open where the road runs
    #    along it and at the farm's gate; the farm's own fence is the farm addon's)
    fence = RULES['walls']['fence']
    fence_lines = {}
    yard_line = {c for c in cells(P.YARD) if c[0] in (P.YARD[0], P.YARD[2]) or c[1] in (P.YARD[1], P.YARD[3])}
    yard_line -= set(YARD_GATE)
    fence_lines['yard'] = yard_line
    near_road = {(c[0] + a, c[1] + b) for c in road for a in (-1, 0, 1) for b in (-1, 0, 1)}
    mx1, my1, mx2, my2 = P.MEADOW
    meadow_line = {c for c in cells(P.MEADOW) if c[0] in (mx1, mx2) or c[1] in (my1, my2)}
    meadow_line = {c for c in meadow_line if c not in near_road and c not in server_tiles and cls[c] != 'w'
                   and not any((c[0] + a, c[1] + b) in server_tiles for a in (-1, 0, 1) for b in (-1, 0, 1))}
    # drop the runs the road's gaps cut to fewer than 3 tiles (render round 3: lone posts beside the road)
    left = set(meadow_line)
    while left:
        comp, q = set(), [left.pop()]
        while q:
            c = q.pop()
            comp.add(c)
            for n in ((c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)):
                if n in left:
                    left.discard(n); q.append(n)
        if len(comp) < 3:
            meadow_line -= comp
    fence_lines['meadow'] = meadow_line
    for name, line in fence_lines.items():
        Wt = lambda c, line=line: c in line
        for (x, y) in sorted(line):
            for tid, role in W.wall_pieces(Wt, x, y, fence):
                put(x, y, land[(x, y)][1], tid, '%s fence %s' % (name, role))
            wall_tiles[(x, y)] = 'fence'
    # the yard's pieces and the square's (room for later tasters; P481 11.2)
    for (tid, x, y) in RULES['yard']['dummies'] + RULES['yard']['butte'] + RULES['yard']['ankh']:
        put(x, y, 0, hx(tid), 'yard')
    for (tid, x, y) in RULES['square']['pieces']:
        put(x, y, 0, hx(tid), 'square')

    # 6. the knoll's standing stones: newisle's ring, the gap south toward the road
    rs = stream('stones')
    for a in range(0, 360, 30):
        if 60 <= a <= 120:
            continue
        x = round(kx + kr * math.cos(math.radians(a)))
        y = round(ky + kr * math.sin(math.radians(a)))
        put(x, y, land[(x, y)][1], S.pick_unlike(rs, table(RULES['stones']['ids']), (x, y), by_tile), 'stones')

    # 7. the dock: planks over the sea from the shore to the landing, rope rails on the outer rows, posts at the ends
    D = RULES['dock']
    rd = stream('dock')
    dz = D['deckZ']
    deck = [c for c in cells(P.DOCK) if (cls[c] == 'w' or (cls[c] == 's' and dw[c] == 1)) and c not in landing]
    deck_set = set(deck)
    y1, y2 = P.DOCK[1], P.DOCK[3]
    for c in sorted(deck):
        put(c[0], c[1], dz, S.pick_unlike(rd, table(D['planks']), c, by_tile), 'dock plank')
    ends = []
    for y in (y1, y2):
        row = sorted(c[0] for c in deck if c[1] == y)
        if row:
            ends.append((row[0], y))       # the shore end; the landing's corner posts stand at the other
    for c in sorted(deck):
        if c in ends:
            for (tid, off) in D['post']:
                put(c[0], c[1], dz + off, hx(tid), 'dock post')
        elif c[1] in (y1, y2):
            put(c[0], c[1], dz + D['railDz'], hx(D['railX']), 'dock rail')
    # the landing: rails along its north and south rows and its east end, posts at its four corners; the moongate
    # (a server item) and the dock-end stop on the middle row
    lx1, ly1, lx2, ly2 = LANDING
    for c in sorted(landing):
        corner = c[0] in (lx1, lx2) and c[1] in (ly1, ly2)
        if corner:
            for (tid, off) in D['post']:
                if off >= 0:
                    put(c[0], c[1], LANDING_Z + off, hx(tid), 'landing post')
        elif c[1] in (ly1, ly2):
            put(c[0], c[1], LANDING_Z + D['railDz'], hx(D['railX']), 'landing rail')
        elif c[0] == lx2:
            put(c[0], c[1], LANDING_Z + D['railDz'], hx(D['railY']), 'landing rail')

    # 8. decor: woods on the two north hills, a light scatter elsewhere, the beach, the shore's static water
    De = RULES['decor']
    keepout = set(keep_clear) | road | yard | set(cells(P.SQUARE)) | landing | deck_set
    for r in (P.YARD, P.SQUARE, P.LODGE, P.BANK):
        keepout |= set(cells((r[0] - 3, r[1] - 3, r[2] + 3, r[3] + 3)))
    keepout |= set(cells((kx - kr - 3, ky - kr - 3, kx + kr + 3, ky + kr + 3)))
    keepout |= set(cells(P.MEADOW))
    keepout |= {(c[0] + a, c[1] + b) for c in road for a in (-2, -1, 0, 1, 2) for b in (-2, -1, 0, 1, 2)}
    keepout |= {c for c in fence_lines['meadow'] | fence_lines['yard']}
    woods = [(6300, 1962, 22), (6330, 1965, 18)]
    in_woods = lambda c: any(math.hypot(c[0] - bx, c[1] - by) <= br for (bx, by, br) in woods)
    zones = collections.defaultdict(set)
    for c, k in cls.items():
        if k == 'w':
            continue
        if in_woods(c) and k == 'g':
            zones['woods'].add(c)
        elif c in set(cells(P.MEADOW)):
            zones['meadow'].add(c)
        elif k == 's':
            zones['beach'].add(c)
        elif k == 'g':
            zones['grass'].add(c)
    trees = [(hx(a), hx(b), w) for a, b, w in De['woods']['trees']]
    under = table(De['woods']['under'])

    def tree_ok(c):
        return all((c[0] + a, c[1] + b) not in keepout and not by_tile.get((c[0] + a, c[1] + b))
                   for a in (-1, 0, 1) for b in (-1, 0, 1)) and cls.get(c) == 'g'

    def plant(rng, c, why):
        t = trees[S.weighted(rng, {i: w for i, (_, _, w) in enumerate(trees)})]
        if any(t[0] in by_tile.get((c[0] + a, c[1] + b), []) for a in (-1, 0, 1) for b in (-1, 0, 1)):
            t = trees[(trees.index(t) + 1) % len(trees)]
        z = land[c][1]
        put(c[0], c[1], z, t[0], why + ' tree')
        put(c[0], c[1], z, t[1], why + ' leaves')

    rw = stream('woods')
    for zone, tshare, ushare in (('woods', De['woods']['treeShare'], De['woods']['underShare']),
                                 ('grass', De['grass']['trees'], De['grass']['under'])):
        tiles = sorted(zones[zone])
        rw.shuffle(tiles)
        for c in tiles:
            k = rw.random()
            if k < tshare and tree_ok(c):
                plant(rw, c, zone)
            elif k < tshare + ushare and c not in keepout and not by_tile.get(c) and cls.get(c) == 'g':
                put(c[0], c[1], land[c][1], S.pick_unlike(rw, under, c, by_tile), zone + ' undergrowth')
    rf = stream('flowers')
    for zone, share, tab in (('meadow', De['meadow']['share'], De['meadow']['flowers']),
                             ('grass', De['grass']['flowers'], De['meadow']['flowers'])):
        for c in sorted(zones[zone]):
            if rf.random() < share and c not in keep_clear and not by_tile.get(c) and cls.get(c) == 'g' \
                    and c not in road and c not in server_tiles:
                put(c[0], c[1], land[c][1], S.pick_unlike(rf, table(tab), c, by_tile), zone + ' flowers')
    rb = stream('beach')
    for c in sorted(zones['beach']):
        if rb.random() < De['beach']['share'] and c not in keepout and not by_tile.get(c) and c not in road:
            put(c[0], c[1], land[c][1], S.pick_unlike(rb, table(De['beach']['pieces']), c, by_tile), 'beach')
    for c in sorted(dry):
        if cls.get(c) == 's' and dw[c] == 1 and c not in deck_set and c not in landing:
            put(c[0], c[1], De['shoreWater']['z'], hx(De['shoreWater']['id']), 'shore water')

    # 9. checks of the plan: nothing outside the area, nothing impassable on a kept-clear tile, one wall piece a tile
    for (x, y, z, tid, why) in statics:
        assert AREA[0] <= x <= AREA[2] and AREA[1] <= y <= AREA[3], (x, y, why)
        if (x, y) in spot_tiles and (items[tid]['flags'] & IMP):
            raise AssertionError(('impassable static on a server item spot', x, y, why))
    # the fence set has no corner piece: its south-east corners carry both runs (walls.wall_pieces), as allowed
    fence_corners = {c for c, st in wall_tiles.items() if st == 'fence'}
    report['doubled wall tiles'] = [t for t in W.check_wall_tiles(statics, items) if t[0] not in fence_corners]
    report['slope audit'] = audit.slope_audit(land, limit=12)
    densities = {}
    piece_count = collections.Counter()
    for (x, y, z, tid, why) in statics:
        for zone, tiles in zones.items():
            if (x, y) in tiles and not any(w in why for w in ('fence', 'wall', 'roof', 'floor', 'shore water')):
                piece_count[zone] += 1
    for zone, tiles in zones.items():
        densities[zone] = (piece_count[zone], len(tiles), round(100.0 * piece_count[zone] / max(1, len(tiles)), 1))
    report['densities'] = densities
    report['zones'] = {k: len(v) for k, v in zones.items()}
    return land, statics, report, dict(cls=cls, road=road, rooms=rooms, wall_tiles=wall_tiles, keep_clear=keep_clear,
                                       landing=landing, deck=deck_set, fence_lines=fence_lines, zones=zones)


# ------------------------------------------------------------------------------------------------ the walk (pinned)

class Walker:
    """Pinned Movement.cs (CheckMovement, Check, GetStartZ, IsOk) and Map.GetAverageZ / CanFit, reduced to the map
    files plus a list of server items: a player (cannot swim), 8 directions, a diagonal only when both orthogonal
    steps are also open (the player rule), doors open (the gate walks with doors as passages)."""

    def __init__(self, folder, rect, items_extra=()):
        self.m = uofiles.MapFile(folder, FACET)
        self.landtd, self.td = uofiles.read_tiledata(CLIENT)
        x1, y1, x2, y2 = rect
        self.tiles = collections.defaultdict(list)
        for s in uofiles.statics_in(folder, FACET, x1, y1, x2, y2):
            self.tiles[(s[0], s[1])].append((s[2], s[3]))
        for (x, y, z, tid) in items_extra:
            self.tiles[(x, y)].append((z, tid))
        self.rect = rect

    def land(self, x, y):
        return self.m.get(x, y)

    @staticmethod
    def ignored(tid):
        return tid == 2 or tid == 0x1DB or 0x1AE <= tid <= 0x1B5

    def avg(self, x, y):
        zt = self.land(x, y)[1]; zl = self.land(x, y + 1)[1]; zr = self.land(x + 1, y)[1]; zb = self.land(x + 1, y + 1)[1]
        low, top = min(zt, zl, zr, zb), max(zt, zl, zr, zb)
        a, b = (zl, zr) if abs(zt - zb) > abs(zl - zr) else (zt, zb)
        return low, (a + b) // 2, top

    def calc(self, tid):
        d = self.td[tid]
        return d['height'] // 2 if d['flags'] & BRIDGE else d['height']

    def is_ok(self, ourZ, ourTop, x, y):
        for (z, tid) in self.tiles.get((x, y), []):
            if self.td[tid]['flags'] & (IMP | SURF):
                if z + self.calc(tid) > ourZ and ourTop > z:
                    return False
        return True

    def start_z(self, x, y, locZ):
        tid = self.land(x, y)[0]
        blocks = bool(self.landtd[tid][0] & IMP)
        landZ, center, landTop = self.avg(x, y)
        zLow = zTop = zCenter = 0
        is_set = False
        if not self.ignored(tid) and not blocks and locZ >= center:
            zLow, zCenter, zTop = landZ, center, landTop
            is_set = True
        for (z, t) in self.tiles.get((x, y), []):
            d = self.td[t]
            calc_top = z + self.calc(t)
            if (is_set and calc_top < zCenter) or locZ < calc_top or not (d['flags'] & SURF):
                continue
            zLow, zCenter = z, calc_top
            top = z + d['height']
            if not is_set or top > zTop:
                zTop = top
            is_set = True
        if not is_set:
            zLow = zTop = locZ
        elif locZ > zTop:
            zTop = locZ
        return zLow, zTop

    def check(self, x, y, startTop, startZ, mZ):
        tid = self.land(x, y)[0]
        lf = self.landtd[tid][0]
        land_blocks = bool(lf & IMP)
        consider = not self.ignored(tid)
        landZ, center, _ = self.avg(x, y)
        ok, newZ = False, 0
        stepTop = startTop + 2
        checkTop = startZ + 16
        for (z, t) in self.tiles.get((x, y), []):
            d = self.td[t]
            if not (d['flags'] & SURF) or (d['flags'] & IMP):
                continue
            ourZ = z + self.calc(t)
            itemTop = z
            testTop = checkTop
            if ok:
                cmp = abs(ourZ - mZ) - abs(newZ - mZ)
                if cmp > 0 or (cmp == 0 and ourZ > newZ):
                    continue
            if ourZ + 16 > testTop:
                testTop = ourZ + 16
            if not d['flags'] & BRIDGE:
                itemTop += d['height']
            if stepTop < itemTop:
                continue
            landCheck = z + min(d['height'], 2)
            if consider and landCheck < center and center > ourZ and testTop > landZ:
                continue
            if self.is_ok(ourZ, testTop, x, y):
                newZ, ok = ourZ, True
        if not consider or land_blocks or stepTop < landZ:
            return ok, newZ
        testTop = max(checkTop, center + 16)
        should = True
        if ok:
            cmp = abs(center - mZ) - abs(newZ - mZ)
            if cmp > 0 or (cmp == 0 and center > newZ):
                should = False
        if should and self.is_ok(center, testTop, x, y):
            newZ, ok = center, True
        return ok, newZ

    def moves(self, x, y, z):
        startZ, startTop = self.start_z(x, y, z)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not (dx or dy):
                    continue
                nx, ny = x + dx, y + dy
                if not (self.rect[0] <= nx <= self.rect[2] and self.rect[1] <= ny <= self.rect[3]):
                    continue
                ok, nz = self.check(nx, ny, startTop, startZ, z)
                if ok and dx and dy:
                    if not self.check(x + dx, y, startTop, startZ, z)[0] or not self.check(x, y + dy, startTop, startZ, z)[0]:
                        ok = False
                if ok:
                    yield nx, ny, nz

    def ground(self, x, y):
        return self.avg(x, y)[1]

    def path(self, a, b):
        """Fewest steps from tile a (standing at the land's average Z, as TutorialWorld.Ground) to tile b."""
        start = (a[0], a[1], self.ground(*a))
        prev = {start: None}
        q = collections.deque([start])
        end = None
        while q:
            s = q.popleft()
            if (s[0], s[1]) == tuple(b):
                end = s
                break
            for n in self.moves(*s):
                if n not in prev:
                    prev[n] = s
                    q.append(n)
        if end is None:
            return None
        out = []
        while end is not None:
            out.append(end)
            end = prev[end]
        return out[::-1]

    def flood(self, a):
        start = (a[0], a[1], self.ground(*a))
        seen = {start}
        q = collections.deque([start])
        while q:
            s = q.popleft()
            for n in self.moves(*s):
                if n not in seen:
                    seen.add(n)
                    q.append(n)
        return seen

    def can_fit(self, x, y, z, height=16):
        """Map.CanFit(p, height, checkBlocksFit: false, checkMobiles: false, requireSurface: true), map tiles and the
        listed items (as statics; none of P663's is movable)."""
        tid = self.land(x, y)[0]
        lf = self.landtd[tid][0]
        low, avgz, _ = self.avg(x, y)
        if lf & IMP and avgz > z and z + height > low:
            return False
        surface = not (lf & IMP) and z == avgz and not self.ignored(tid)
        for (tz, t) in self.tiles.get((x, y), []):
            f = self.td[t]['flags']
            if (f & (SURF | IMP)) and tz + self.calc(t) > z and z + height > tz:
                return False
            if f & SURF and not f & IMP and z == tz + self.calc(t):
                surface = True
        return surface


# ------------------------------------------------------------------------------------------------ files

def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def strip_area(text):
    """The shipped patch without any line inside the isle's drawn area (shifted), and without the B lines of blocks
    the area alone touched."""
    x1, y1 = shifted(AREA[0], AREA[1])
    x2, y2 = shifted(AREA[2], AREA[3])
    bh = 4096 >> 3
    inside = lambda x, y: x1 <= x <= x2 and y1 <= y <= y2
    keep, kept_blocks, b_lines = [], set(), []
    for line in text.splitlines():
        f = line.split()
        if f and f[0] in ('L', 'S+', 'S-'):
            x, y = int(f[1]), int(f[2])
            if inside(x, y):
                continue
            kept_blocks.add((x >> 3) * bh + (y >> 3))
        if f and f[0] == 'B':
            b_lines.append(line)
            continue
        keep.append(line)
    out = []
    for line in keep:
        out.append(line)
        if line.startswith('F '):
            out += [b for b in b_lines if int(b.split()[1]) in kept_blocks]
    return '\n'.join(out) + '\n'


def fresh(work, base):
    """edited/ = the pristine base (hashes as ORIGINAL-SHA256.txt) plus the shipped patch less the isle's lines."""
    want = {}
    for line in open(os.path.join(work, 'ORIGINAL-SHA256.txt')):
        h, _, name = line.strip().partition(' *')
        if name:
            want[name.split('/')[-1]] = h
    for name in ('map1LegacyMUL.uop', 'statics1.mul', 'staidx1.mul'):
        h = sha(os.path.join(base, name))
        assert h == want[name], ('the base is not the pristine copy', name, h, want[name])
    shipped = open(os.path.join(SL_CODE, PATCH_REL), encoding='utf-8').read()
    others = strip_area(shipped)
    open(os.path.join(work, 'others.mapops'), 'w', newline='\n').write(others)
    edited = os.path.join(work, 'edited')
    os.makedirs(edited, exist_ok=True)
    drifted, missing = mapops.apply(others, base, edited, FACET)
    print('fresh: edited/ = base + the shipped patch less the isle (%d lines); drifted %s, missing %s' % (
        len(others.splitlines()), len(drifted), len(missing)))
    return edited


def shift_land(land):
    return {shifted(*c): v for c, v in land.items()}


def shift_statics(statics):
    return [(x + DX, y + DY, z, tid, why) for (x, y, z, tid, why) in statics]


# ------------------------------------------------------------------------------------------------ the gate

def gate(edited, farm, props, pts, farm_door):
    """Walk the built files from the beach to the dock with the server items in place; every leg, every lesson
    detour, and P663's every fit-checked spot. Returns (rows, fits, walkable set)."""
    td = uofiles.read_tiledata(CLIENT)[1]
    extra = []
    for (x, y, z, tid, what) in farm:
        if (x, y) == farm_door:
            continue                         # the farmhouse door: walked open
        extra.append((x, y, z, tid))
    rect = (shifted(*AREA[:2]) + shifted(*AREA[2:]))
    w0 = Walker(edited, rect)
    for (x, y, z, tid, what) in props:
        extra.append((x, y, w0.ground(x, y), tid))
    w = Walker(edited, rect, extra)
    rows = []
    stops = [(n, label, shifted(x, y)) for (n, label, x, y) in P.STOPS]
    sketch = dict((n, None) for n, _, _ in stops)
    for line in open(os.path.join(REPO, 'notes', 'cc-P481-tools', 'new-isle', 'legs.txt')):
        m = re.match(r'\s*(\d+) .*?(\d+)\s*$', line)
        if m and not line.startswith('road') and not line.startswith('walkable') and not line.startswith('land'):
            sketch[int(m.group(1))] = int(m.group(2))
    for (a, b) in zip(stops, stops[1:]):
        p = w.path(a[2], b[2])
        rows.append(('%d to %d' % (a[0], b[0]), b[1], len(p) - 1 if p else None, sketch.get(b[0])))
    # the lessons inside: the bank to Merrin, the lodge to Elara, the yard to the echo, the farm to Wren
    for name, frm, to in (('bank: stop 7 to Merrin', pts['BankStop'], pts['Banker']),
                          ('lodge: stop 8 to Elara', pts['LodgeStop'], pts['Elara']),
                          ('yard: stop 6 to the echo', pts['Yard'], pts['Echo']),
                          ('yard: the echo to Sera', pts['Echo'], pts['Healer']),
                          ('farm: stop 5 to Wren', pts['FarmGate'], pts['FarmhandSpot']),
                          ('farm: Wren to the pests', pts['FarmhandSpot'], pts['PestSpot']),
                          ('dock end to the moongate', pts['DockEnd'], pts['Moongate'])):
        p = w.path(frm, to)
        rows.append((name, '', len(p) - 1 if p else None, None))
    fits = {}
    for name, (x, y) in sorted(pts.items()):
        if name in ('SiteShift',):
            continue
        z = w.ground(x, y)
        fits[name] = (x, y, z, w0.can_fit(x, y, z))
    flood = w.flood(shifted(*P.STOPS[0][2:]))
    return rows, fits, {(s[0], s[1]) for s in flood}


# ------------------------------------------------------------------------------------------------ main

def main():
    args = sys.argv[1:]
    work = args[0]
    plan_only = '--plan-only' in args
    base = args[args.index('--base') + 1] if '--base' in args else CLIENT
    farm, props, pts, farm_door = server_items()
    land, statics, report, info = plan(farm, props, pts)
    print('land:', report['land'], 'transition rounds', report['transition rounds'])
    print('zones (tiles):', report['zones'])
    print('densities (pieces, tiles, per 100):', report['densities'])
    print('corners:', {k: dict(v) for k, v in report['corners'].items()})
    print('doubled wall tiles:', report['doubled wall tiles'])
    print(audit.summary(report['slope audit']))
    counts = collections.Counter(s[4].split(' ')[0] + ' ' + s[4].split(' ')[1] if ' ' in s[4] else s[4] for s in statics)
    print('statics', len(statics), dict(sorted(counts.items())))
    L = shift_land(land)
    St = shift_statics(statics)
    with open(os.path.join(HERE, 'statics-placed.csv'), 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['x', 'y', 'z', 'id_hex', 'why'])
        for (x, y, z, tid, why) in sorted(St):
            wr.writerow([x, y, z, '0x%04X' % tid, why])
    byid = collections.Counter((tid, z) for (tid, z) in L.values())
    with open(os.path.join(HERE, 'land-summary.csv'), 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['land_id_hex', 'z', 'tiles'])
        for (tid, z), n in sorted(byid.items()):
            wr.writerow(['0x%04X' % tid, z, n])
    json.dump({'report': {k: v for k, v in report.items() if k not in ('slope audit',)},
               'slope': report['slope audit']}, open(os.path.join(HERE, 'build-report.json'), 'w'), indent=1,
              default=lambda o: dict(o) if isinstance(o, collections.Counter) else list(o))
    if plan_only:
        return
    if '--fresh' in args or not os.path.exists(os.path.join(work, 'edited', 'map1LegacyMUL.uop')):
        edited = fresh(work, base)
    else:
        edited = os.path.join(work, 'edited')
        x1, y1 = shifted(*AREA[:2]); x2, y2 = shifted(*AREA[2:])
        assert not uofiles.statics_in(edited, FACET, x1, y1, x2, y2), 'edited/ already holds the isle: use --fresh'
    changed = uofiles.write_land(edited, FACET, L)
    print('land tiles written', len(changed), 'their old values', dict(collections.Counter(changed.values()).most_common(3)))
    nblocks, kept = uofiles.write_statics(edited, FACET, St)
    print('statics written', len(St), 'in', nblocks, 'blocks; blocks that already held statics:', kept)
    bad, same, n = uofiles.verify(edited, FACET, L, St)
    print('verify (a second read of the files): land mismatches', bad, '; statics round-trip', same, '(%d read back)' % n)
    assert bad == 0 and same
    rows, fits, walkable = gate(edited, farm, props, pts, farm_door)
    print('the walk (pinned movement, server items in place):')
    for r in rows:
        print('  %-28s %-30s walked %-5s sketch %s' % r)
    bad_fit = {k: v for k, v in fits.items() if not v[3]}
    print('P663 spots that CanFit at their ground:', sum(1 for v in fits.values() if v[3]), 'of', len(fits),
          '; refused:', bad_fit)
    rec = {'walkable': sorted(walkable), 'walls': sorted(info['wall_tiles'])}
    if os.path.exists(CELLS):
        prev = json.load(open(CELLS))
        same_cells = prev == json.loads(json.dumps(rec))
        print('walkable set and wall tiles unchanged from plan-cells.json:', same_cells)
    else:
        same_cells = None
        json.dump(rec, open(CELLS, 'w'))
        print('plan-cells.json written (the first build of this layout)')
    json.dump({'legs': rows, 'fits': fits, 'walkable_tiles': len(walkable), 'same_cells': same_cells},
              open(os.path.join(HERE, 'walk-report.json'), 'w'), indent=1)
    assert all(r[2] is not None for r in rows), 'a leg cannot be walked'
    assert not bad_fit, 'a P663 spot does not fit'
    patch = mapops.diff(base, edited, FACET)
    out = os.path.join(work, 'trammel.mapops')
    open(out, 'w', newline='\n').write(patch)
    drifted, missing, land_equal, nbad = mapops.check(patch, base, edited, FACET)
    kinds = collections.Counter(l.split()[0] for l in patch.splitlines() if l and not l.startswith('#'))
    print('patch', out, os.path.getsize(out), 'bytes', dict(kinds), '; check: drifted', len(drifted), 'missing',
          len(missing), 'land identical', land_equal, 'blocks differing', nbad)
    if '--ship' in args:
        dst = os.path.join(SL_CODE, PATCH_REL)
        shutil.copyfile(out, dst)
        print('shipped to', dst)


if __name__ == '__main__':
    main()
