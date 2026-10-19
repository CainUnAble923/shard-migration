"""cc-P167 / cc-P180 / cc-P181: builds the Rootdeep Burrows (P141's approved layout, notes/art/rootdeep-mockup/layout.json)
into a SCRATCH copy of Trammel (map1LegacyMUL.uop in place, statics1.mul/staidx1.mul rewritten per block). Never run
against the client-data folder either repo or the shard reads: pass the scratch folder (D:/UO/cc-p167-work/scratch-client).

    python -P build_burrows.py <scratch folder> [--plan-only] [--fresh]

  --plan-only   writes the CSVs and plan-cells.json, touches no map file
  --fresh       first restores the scratch map, statics and index from the shard's client-data copy (read only; the
                copies must hash as ORIGINAL-SHA256.txt beside them), so a rebuild never stacks on an old build

The general machinery (file readers and writers, the wall rule, corners, doorway frames, scatter, the slope audit)
lives in scripts/mapbuild/ since P181; this file is the Rootdeep-specific driver. The look comes from plan-sets.json
beside this file (one seed per zone, tile weights, decor and corner rules, frames); nothing about the look is in
this code. P141's layout fixes the walkable floor; this builder never changes it (it checks its walkable set against
the previous build's plan-cells.json and refuses to write if they differ).

Walls: notes/uo-wall-orientation.md (measured on OSI buildings). Corners and frames: notes/cc-P181-cont-rootdeep-round3.md
and notes/map-building-playbook.md. Cave zones (Warren, Brood Pit, Tangle, Dawnseam) use raised cave-rock land, as
OSI's caves do: ring at floor level, then +12, then void at +20. Every floor is Z 0.
"""
import collections, csv, json, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import uofiles, walls as W, scatter as S, audit  # noqa: E402
from mapbuild.walls import hx  # noqa: E402

LAYOUT = r'D:\UO\shard-migration\notes\art\rootdeep-mockup\layout.json'
RULES = os.path.join(HERE, 'plan-sets.json')
CELLS = os.path.join(HERE, 'plan-cells.json')
SEEDER = r'D:\ShatteredLegacy\server\customizations\ClusterFRootdeepSeeder.cs'
VAULT = r'D:\ShatteredLegacy\server\customizations\Regions\RootdeepVault.cs'
CLIENT = uofiles.CLIENT
FACET = 1
VOID = uofiles.VOID
FLOOR_Z = 0
RAMP_Z, TOP_Z = 12, 20
ITEM_ZONE_PRIORITY = ['Vault', 'Landing', 'Gloom lair', 'Gloom']

# the cave edge tiles (cave floor with a black wedge toward the rock), by which orthogonal sides are rock; measured
# on Khaldun (Trammel 5376-5567 x 1280-1407, 2,058 tiles): side tiles when one side is rock, corner tiles when two
EDGE_TILES = {'N': ['0x0257', '0x0258', '0x0259'], 'S': ['0x024E', '0x024F', '0x0253'],
              'E': ['0x0254', '0x0255', '0x0256'], 'W': ['0x0250', '0x0251', '0x0252'],
              'ES': ['0x024A'], 'SW': ['0x024B'], 'NE': ['0x024C'], 'NW': ['0x024D']}


def weighted(rng, table):
    return S.weighted(rng, table)


def cells(rect):
    x1, y1, x2, y2 = rect
    return [(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]


def read_points():
    src = open(SEEDER, encoding='utf-8').read()
    vault = open(VAULT, encoding='utf-8').read()
    pt = lambda name, text: tuple(int(v) for v in re.search(name + r' = new\((\d+), (\d+)', text).groups())
    pat = re.compile(r'new\("([^"]+)", "([^"]+)", (\d+), (\d+), (\d+), (\d+), (true|false), (\d+), (\d+), ')
    spawners = [(int(m.group(3)), int(m.group(4))) for m in pat.finditer(src)]
    pts = {'arrival': pt('Arrival', src), 'ankh': pt('AnkhAt', src), 'doorway': pt('Doorway', vault),
           'landingSpot': pt('LandingSpot', vault), 'mouth': pt('CrawlwayMouth', vault), 'exit': pt('CrawlwayExit', vault)}
    return spawners, pts


# ------------------------------------------------------------------------------------------------ the plan

def plan(layout, rules, spawners, pts, quiet=False):
    """Returns land {(x,y): (id, z)}, statics [(x,y,z,id,why)], stats, counts, floor, opening, walls, report."""
    items = uofiles.read_tiledata(CLIENT)[1]
    land_flags = uofiles.read_tiledata(CLIENT)[0]
    impassable = lambda tid: bool(items[tid]['flags'] & uofiles.IMPASSABLE)
    zones = rules['zones']
    rngs = {z: random.Random(zones[z]['seed']) for z in zones}
    report = collections.OrderedDict()
    floor = {}        # (x,y) -> zone key, walkable floors incl. openings
    opening = set()   # floor tiles that cut through a wall line
    rect_of = {}
    for f in layout['floors']:
        for c in cells(f['rect']):
            floor[c] = f['zone']
            rect_of[c] = tuple(f['rect'])
            if f['name'].startswith('gap ') or f['name'].startswith('lair mouth'):
                opening.add(c)
    dx, dy = pts['doorway']
    for c in ((dx, dy), (dx, dy + 1)):
        floor[c] = 'Vault'; opening.add(c); rect_of[c] = (dx, dy, dx, dy + 1)
    crawl = [(pts['mouth'][0], y) for y in range(pts['mouth'][1] + 1, pts['exit'][1] - 1)]  # 5160,1160 and 5160,1161
    assert len(crawl) == 2, crawl
    for c in crawl:
        floor[c] = 'Warren'; opening.add(c); rect_of[c] = (c[0], crawl[0][1], c[0], crawl[-1][1])

    obstacles = {}    # (x,y) -> (zone, name, rect)
    for o in layout['obstacles']:
        for c in cells(o['rect']):
            obstacles[c] = (o['zone'], o['name'], tuple(o['rect']))
    for c in obstacles:
        floor.pop(c, None); opening.discard(c)
    anyfloor = lambda c: c in floor

    # wall tiles: every non-floor tile touching a floor (8 neighbours). The mockup counts these (1,618).
    walls = W.ring_of(floor)

    def zone_of_wall(c):
        x, y = c
        near = collections.Counter()
        for ddx in (-1, 0, 1):
            for ddy in (-1, 0, 1):
                n = (x + ddx, y + ddy)
                if n in floor:
                    near[floor[n]] += 1
        for z in ITEM_ZONE_PRIORITY:
            if near[z]:
                return z
        return near.most_common(1)[0][0]

    land = {}
    statics = []
    counts = collections.Counter()
    by_tile = collections.defaultdict(list)

    def put(x, y, tid, why, z=FLOOR_Z):
        statics.append((x, y, z, tid, why))
        by_tile[(x, y)].append(tid)
        counts[why] += 1

    def unput(x, y, pred):
        """Remove statics at (x, y) whose why matches pred (a wall piece a frame replaces)."""
        gone = [s for s in statics if s[0] == x and s[1] == y and pred(s[4])]
        for s in gone:
            statics.remove(s)
            by_tile[(x, y)].remove(s[3])
            counts[s[4]] -= 1
        return gone

    def obstacle_rule(name):
        for key, rule in rules['obstacles'].items():
            if name.startswith(key):
                return key, rule
        raise KeyError(name)

    # 1. floors: weighted draw per tile from the zone's table, one rng per zone
    for c, zone in sorted(floor.items()):
        land[c] = (weighted(rngs[zone], zones[zone]['floor']), FLOOR_Z)
    for c in crawl:
        land[c] = (hx(next(iter(zones['Warren']['floor']))), FLOOR_Z)
        put(c[0], c[1], weighted(rngs['Warren'], rules['crawlway']['rocks']), 'crawlway rocks')

    # 2. obstacles (solid blocks inside a floor), by the rule named after the block
    wall_blocks = set()
    item_blocks = set()
    for c, (zone, name, rect) in sorted(obstacles.items()):
        x, y = c
        key, rule = obstacle_rule(name)
        rng = rngs[zone]
        if rule['kind'] == 'walls':
            land[c] = (weighted(rng, zones[zone]['floor']), FLOOR_Z)
            wall_blocks.add(c)
        elif rule['kind'] == 'items':
            land[c] = (weighted(rng, zones[zone]['floor']), FLOOR_Z)
            item_blocks.add(c)
            x1, y1, x2, y2 = rect
            at_end = (y1 == y2 and x in (x1, x2)) or (x1 == x2 and y in (y1, y2))
            if rule.get('ends') and at_end:
                put(x, y, S.pick_unlike(rng, rule['ends'], c, by_tile), rule['why'] + ' end piece', z=0)
            else:
                tid = S.pick_unlike(rng, rule['ids'], c, by_tile)
                put(x, y, tid, rule['why'], z=rng.choice(rule.get('z', [0])))
            for extra in rule.get('extra', []):
                if rng.random() < extra['p']:
                    put(x, y, S.pick_unlike(rng, extra['ids'], c, by_tile), extra['why'], z=rng.choice(extra['z']))
        elif rule['kind'] == 'mound':
            item_blocks.add(c)
            x1, y1, x2, y2 = rect
            rim = x in (x1, x2) or y in (y1, y2)
            land[c] = (weighted(rng, rule['rim']), FLOOR_Z) if rim else (weighted(rng, rule['inside']), rule['insideZ'])
            dec = rule['rimDecor'] if rim else rule['insideDecor']
            if rng.random() < dec['p']:
                put(x, y, S.pick_unlike(rng, dec['ids'], c, by_tile), dec['why'], z=rng.choice(dec['z']))
        else:
            raise ValueError(rule['kind'])

    # 3. walls (item zones) and cave rings (land zones)
    wall_zone = {c: zone_of_wall(c) for c in walls}
    F = lambda c: c in floor and c not in opening
    ring = {}
    for c in sorted(walls):
        if c in obstacles and c not in wall_blocks:
            continue   # the obstacle fill above stands
        x, y = c
        zone = wall_zone[c] if c in wall_zone else obstacles[c][0]
        look = zones[zone]
        if look['kind'] == 'land':
            ring[c] = zone
            continue
        land[c] = (weighted(rngs[zone], look['floor']), FLOOR_Z)
        for tid, role in W.wall_pieces(F, x, y, rules['wallSets'][look['wallSet']]):
            put(x, y, tid, '%s wall %s' % (zone, role))

    # 4. cave rings: ring tile at floor level, the next ring +12, the one beyond +20 (void), unless near an item zone
    def dist_to(targets, cmax):
        d = {t: 0 for t in targets}
        frontier = list(targets)
        k = 0
        while frontier and k < cmax:
            k += 1
            nxt = []
            for (x, y) in frontier:
                for ddx in (-1, 0, 1):
                    for ddy in (-1, 0, 1):
                        n = (x + ddx, y + ddy)
                        if n not in d:
                            d[n] = k
                            nxt.append(n)
            frontier = nxt
        return d
    land_floors = [c for c, z in floor.items() if zones[z]['kind'] == 'land']
    item_floors = [c for c, z in floor.items() if zones[z]['kind'] == 'item']
    dl = dist_to(land_floors, 3)
    di = dist_to(item_floors, 3)
    rock_beyond = lambda c: c not in floor and c not in ring and c not in opening and (c not in land or land[c][0] not in range(0x0486, 0x048A))
    for c, zone in sorted(ring.items()):
        x, y = c
        look = zones[zone]
        if look.get('ringEdge'):
            # the Khaldun foot: a cave edge tile whose black wedge faces the rock behind the ring
            sides = ''.join(k for k, n in (('N', (x, y - 1)), ('E', (x + 1, y)), ('S', (x, y + 1)), ('W', (x - 1, y))) if rock_beyond(n) and n not in ring)
            key = {'NE': 'NE', 'ES': 'ES', 'SW': 'SW', 'NW': 'NW', 'N': 'N', 'E': 'E', 'S': 'S', 'W': 'W'}.get(sides)
            if key is None and len(sides) > 2:
                key = None
            if key is None:
                diag = [k for k, n in (('NW', (x - 1, y - 1)), ('NE', (x + 1, y - 1)), ('SW', (x - 1, y + 1)), ('ES', (x + 1, y + 1))) if rock_beyond(n) and n not in ring]
                key = {'NW': 'W', 'NE': 'E', 'SW': 'S', 'ES': 'S'}.get(diag[0]) if len(diag) == 1 else None
            if key:
                land[c] = (hx(rngs[zone].choice(EDGE_TILES[key])), FLOOR_Z)
                counts['%s cave ring edge tile' % zone] += 1
                continue
        land[c] = (weighted(rngs[zone], look['ring']), FLOOR_Z)
        counts['%s cave ring' % zone] += 1
    for c, d in sorted(dl.items()):
        if c in land or c in floor:
            continue
        if di.get(c, 9) <= 2 or c[0] < layout['buildFromX']:
            continue   # near an item zone, or west of the build line (the ramp is cosmetic)
        if d == 2:
            # the ramp takes the ring texture of the nearest ring tile's zone
            zone = next((ring[(c[0] + a, c[1] + b)] for a in (-1, 0, 1) for b in (-1, 0, 1) if (c[0] + a, c[1] + b) in ring), 'Warren')
            land[c] = (weighted(rngs[zone], zones[zone]['ring']), RAMP_Z)
            counts['cave ramp +12'] += 1
        elif d == 3:
            land[c] = (VOID, TOP_Z)
            counts['void raised +20'] += 1

    # 5. decor on floors, by the zone's rules: clustered, seeded, never on a path that matters
    keep_clear = set()
    for sx, sy in spawners + list(pts.values()) + list(opening) + crawl:
        for ddx in range(-2, 3):
            for ddy in range(-2, 3):
                keep_clear.add((sx + ddx, sy + ddy))
    solid = lambda c: c not in floor
    near_wall = lambda c: any(solid((c[0] + a, c[1] + b)) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0))
    wall_face = lambda c: solid((c[0], c[1] - 1)) or solid((c[0] - 1, c[1]))

    def roomy(c):
        """An impassable piece may stand here: it never pinches a path (3 of 4 orthogonal neighbours stay floor, none
        an opening) and the room is at least 6 wide and deep."""
        x1, y1, x2, y2 = rect_of[c]
        if x2 - x1 + 1 < 6 or y2 - y1 + 1 < 6:
            return False
        x, y = c
        orth = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return sum(1 for n in orth if anyfloor(n)) >= 3 and not any(n in opening for n in orth)
    taken = set(by_tile)
    decor_blocked = set()
    by_zone = collections.defaultdict(list)
    for c, z in floor.items():
        if c not in opening and c not in keep_clear and c not in taken:
            by_zone[z].append(c)
    for zone, tiles in sorted(by_zone.items()):
        rng = rngs[zone]
        for rule in zones[zone].get('decor', []):
            where = rule.get('where', 'any')
            if where == 'nearWall':
                elig = [c for c in tiles if near_wall(c)]
            elif where == 'open':
                elig = [c for c in tiles if not near_wall(c)]
            elif where == 'wallFace':
                elig = [c for c in tiles if wall_face(c)]
            else:
                elig = list(tiles)
            S.scatter(rng, rule, elig, taken, by_tile, put, roomy, impassable, decor_blocked)

    # 6. doorway frames: every opening group framed by its wall set's rule (item zones) or the zone's gap pieces
    #    (cave zones); the crawlway's flanking rocks
    groups = W.opening_groups(opening, solid)
    frames = []
    for g in groups:
        zone = zone_of_wall(g['tiles'][0]) if g['tiles'][0] in wall_zone else floor[g['tiles'][0]]
        # an opening between two zones takes the wall set of the wall tiles beside it
        beside = [(g['tiles'][0][0] + a, g['tiles'][0][1] + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (g['tiles'][0][0] + a, g['tiles'][0][1] + b) in wall_zone]
        if beside:
            zone = wall_zone[beside[0]]
        look = zones[zone]
        if not (g['before_solid'] or g['after_solid']):
            frames.append((zone, g['axis'], g['tiles'], 'passage, no frame'))
            continue   # a passage between two floors (the crawlway), not a doorway in a wall line
        if look['kind'] == 'item':
            ws = rules['wallSets'][look['wallSet']]
            for (x, y, tid, role, replaces) in W.frame_pieces(g, ws):
                if replaces:
                    unput(x, y, lambda why: ' wall ' in why)
                put(x, y, tid, '%s %s' % (zone, role))
            frames.append((zone, g['axis'], g['tiles'], look['wallSet']))
        else:
            gap = look.get('gapFrame')
            if gap:
                for c in (g['before'], g['after']):
                    if c in ring:
                        put(c[0], c[1], S.pick_unlike(rngs[zone], gap['ids'], c, by_tile), '%s gap frame' % zone, z=0)
                frames.append((zone, g['axis'], g['tiles'], 'rock'))
    for (fx, fy) in rules['crawlway'].get('frame', []):
        assert (fx, fy) in ring or (fx, fy) in walls, (fx, fy)
        put(fx, fy, S.pick_unlike(rngs['Warren'], rules['crawlway']['frameIds'], (fx, fy), by_tile), 'crawlway frame rocks')
    report['frames'] = frames

    # 7. corners: every inner corner of every zone, dressed by the zone's corner rules (notes/map-building-playbook.md)
    hard = lambda c: c in walls and c not in item_blocks   # walls, rings and walled pillars; not shelving, crystals, mounds
    concave = W.concave_corners(floor, hard, skip=opening)
    convex = W.convex_corners(floor, hard, skip=opening)
    corner_log = collections.defaultdict(collections.Counter)
    for (x, y, nm) in concave:
        zone = floor[(x, y)]
        rule = zones[zone].get('corners')
        corner_log[zone]['concave'] += 1
        if not rule:
            continue
        rng = rngs[zone]
        c = (x, y)
        placed = []
        if zones[zone]['kind'] == 'item':
            # on the corner floor tile: passable decor only (webs, bones, stains, a torch on the N or W wall, a brazier);
            # passable pieces may sit on a spawner home, never on an opening
            if c not in opening and c not in taken:
                for dec in rule.get('floor', []):
                    if rng.random() < dec['p']:
                        tid = S.pick_unlike(rng, dec['ids'], c, by_tile)
                        if impassable(tid):
                            continue
                        put(x, y, tid, '%s corner %s' % (zone, dec['name']), z=rng.choice(dec.get('z', [0])))
                        placed.append(dec['name'])
                torch = rule.get('torch')
                if torch and rng.random() < torch['p']:
                    side = 'north' if 'N' in nm else ('west' if 'W' in nm else None)
                    if side and torch.get(side):
                        put(x, y, S.pick_unlike(rng, torch[side], c, by_tile), '%s corner torch' % zone)
                        placed.append('torch')
                taken.add(c)
            # on the visible strip (the wall tiles south and east of the corner): rubble, bones, a candelabra
            strip = W.visible_strip_tiles((x, y, nm), hard)
            for dec in rule.get('strip', []):
                for t in strip:
                    around = [t, (t[0] + 1, t[1]), (t[0] - 1, t[1]), (t[0], t[1] + 1), (t[0], t[1] - 1)]
                    if rng.random() < dec['p'] and not any(tid in by_tile.get(n, []) for n in around for tid in map(hx, dec['ids'])):
                        put(t[0], t[1], S.pick_unlike(rng, dec['ids'], t, by_tile), '%s corner %s' % (zone, dec['name']), z=rng.choice(dec.get('z', [0])))
                        placed.append(dec['name'])
                        break   # one of each kind per corner (two candelabra side by side read as a copy)
            pillar = rule.get('pillar')
            if pillar and nm == 'SE':
                x1, y1, x2, y2 = rect_of[c]
                if x2 - x1 + 1 >= pillar['minRoom'] and y2 - y1 + 1 >= pillar['minRoom'] and hard((x + 1, y + 1)):
                    put(x + 1, y + 1, weighted(rng, pillar['ids']), '%s corner pillar' % zone)
                    placed.append('pillar')
        else:
            # cave: the ring tiles round the corner (non-walkable rock) get a cluster of the zone's corner pieces
            tiles = [t for t in ((x + (1 if 'E' in nm else -1), y + (1 if 'S' in nm else -1)), (x + (1 if 'E' in nm else -1), y), (x, y + (1 if 'S' in nm else -1))) if t in ring]
            dec = rule.get('ring')
            if dec and tiles and rng.random() < dec['p']:
                k = rng.randint(dec['count'][0], dec['count'][1])
                rng.shuffle(tiles)
                for t in tiles[:k]:
                    put(t[0], t[1], S.pick_unlike(rng, dec['ids'], t, by_tile), '%s corner %s' % (zone, dec['name']), z=rng.choice(dec.get('z', [0])))
                    placed.append(dec['name'])
            if zones[zone].get('ringEdge'):
                placed.append('edge tile')
        if not placed:
            # every inner corner gets at least one thing (Chase, round 2): the first strip piece, else the first
            # floor piece (passable), else the ring cluster's first piece
            if zones[zone]['kind'] == 'item':
                strip = W.visible_strip_tiles((x, y, nm), hard)
                clear = []
                for dec in rule.get('strip', []):
                    for t in strip:
                        around = [t, (t[0] + 1, t[1]), (t[0] - 1, t[1]), (t[0], t[1] + 1), (t[0], t[1] - 1)]
                        if not any(tid in by_tile.get(n, []) for n in around for tid in map(hx, dec['ids'])):
                            clear.append((dec, t))
                if clear:
                    dec, t = clear[0]
                    put(t[0], t[1], S.pick_unlike(rng, dec['ids'], t, by_tile), '%s corner %s' % (zone, dec['name']), z=rng.choice(dec.get('z', [0])))
                    placed.append(dec['name'])
                elif rule.get('floor') and c not in opening:
                    dec = rule['floor'][0]
                    put(x, y, S.pick_unlike(rng, dec['ids'], c, by_tile), '%s corner %s' % (zone, dec['name']), z=rng.choice(dec.get('z', [0])))
                    placed.append(dec['name'])
            else:
                dec = rule.get('ring')
                tiles = [t for t in ((x + (1 if 'E' in nm else -1), y + (1 if 'S' in nm else -1)), (x + (1 if 'E' in nm else -1), y), (x, y + (1 if 'S' in nm else -1))) if t in ring]
                if dec and tiles:
                    t = tiles[0]
                    put(t[0], t[1], S.pick_unlike(rng, dec['ids'], t, by_tile), '%s corner %s' % (zone, dec['name']), z=rng.choice(dec.get('z', [0])))
                    placed.append(dec['name'])
        if placed:
            corner_log[zone]['concave dressed'] += 1
            for p in placed:
                corner_log[zone][p] += 1
    for (x, y, nm) in convex:
        zone = floor[(x, y)]
        rule = zones[zone].get('corners')
        corner_log[zone]['convex'] += 1
        if not rule or zones[zone]['kind'] != 'land':
            continue
        dec = rule.get('convex')
        tip = (x + (1 if 'E' in nm else -1), y + (1 if 'S' in nm else -1))
        rng = rngs[zone]
        if dec and tip in ring and rng.random() < dec['p'] and not by_tile.get(tip):
            put(tip[0], tip[1], S.pick_unlike(rng, dec['ids'], tip, by_tile), '%s corner %s' % (zone, dec['name']), z=0)
            corner_log[zone]['convex dressed'] += 1
    report['corners'] = corner_log

    # 8. the lair mouth webs (P180's proposal, carried with (a))
    for (wx, wy, wz, wid) in rules.get('proposals', {}).get('mouthWebs', []):
        put(wx, wy, hx(wid), 'lair mouth webs', z=wz)

    # 9. checks: the walkable set is exactly the floor (every floor tile free of impassable statics and on passable land,
    #    every obstacle tile blocked), nothing outside the area or west of the build line; one wall piece per tile;
    #    the slope audit
    blocked = lambda c: any(impassable(t) for t in by_tile.get(c, [])) or (c in land and land_flags[land[c][0]][0] & uofiles.IMPASSABLE)
    bad_floor = sorted(c for c in floor if blocked(c) and c not in crawl and c not in decor_blocked)
    bad_obst = sorted(c for c in obstacles if not blocked(c) and c not in wall_blocks)
    assert not bad_floor, ('floor tiles blocked by something other than roomy decor', bad_floor[:10])
    assert all(roomy(c) and c not in keep_clear for c in decor_blocked), 'impassable decor on a tile that matters'
    counts['floor tiles under impassable decor (each with 3 open sides, in a room 6+ wide, off every path and spawn)'] = len(decor_blocked)
    assert not bad_obst, ('obstacle tiles open', bad_obst[:10])
    for c in wall_blocks:
        assert c not in walls or by_tile.get(c), ('pillar ring tile without a wall piece', c)
    doubled = W.check_wall_tiles(statics, items)
    doubled = [(c, v) for c, v in doubled if not all(items[t]['name'] in ('marble column', 'stone pillar') or items[t]['flags'] & uofiles.WALL and items[t]['height'] < 20 for t in v[1:])]
    report['doubled wall tiles'] = doubled
    area = layout['area']
    for (x, y) in list(land) + [(s[0], s[1]) for s in statics]:
        assert area[0] <= x <= area[2] and area[1] <= y <= area[3], (x, y)
        assert x >= layout['buildFromX'], (x, y)
    flags = audit.slope_audit(land, limit=12)
    report['slope audit'] = flags
    stats = dict(floor=len(floor) - len(opening), openings=len(opening), walls=len(walls),
                 obstacles=len(obstacles), land_tiles=len(land), statics=len(statics))
    return land, statics, stats, counts, floor, opening, walls, report


# ------------------------------------------------------------------------------------------------ test rooms (P180 s1.1, P181)

def test_room_scenes(rules):
    """A 5 x 5 room and an L-shaped room in each item wall set, built by walls_for, plus the stone set's arched
    north-south doorway two ways and a framed marble gap. Returns {name: (land, statics)} for isorender."""
    floors = {'dungeon': 0x0245, 'marble': 0x0486, 'stone': 0x0440}
    out = {}
    for name, ws in rules['wallSets'].items():
        sq = {(x, y) for x in range(0, 5) for y in range(0, 5)}
        L = {(x, y) for x in range(10, 18) for y in range(0, 5)} | {(x, y) for x in range(10, 14) for y in range(5, 10)}
        for label, fl in (('%s 5x5' % name, sq), ('%s L' % name, L)):
            statics, ring = W.walls_for(fl, set(), ws)
            land = {c: (floors[name], 0) for c in fl | ring}
            xs = [c[0] for c in land]; ys = [c[1] for c in land]
            for x in range(min(xs) - 1, max(xs) + 2):
                for y in range(min(ys) - 1, max(ys) + 2):
                    land.setdefault((x, y), (VOID, 0))
            out[label] = (land, [(x, y, z, tid) for (x, y, z, tid, role) in statics])
    ws = rules['wallSets']['stone']
    for label, gap, north_at, south_at in (('stone mouth 3 open', [2, 3, 4], 2, 5), ('stone mouth 2 open', [2, 3], 2, 4)):
        fl = {(x, y) for x in range(0, 9) for y in range(0, 7) if x != 4} | {(4, y) for y in gap}
        openings = {(4, y) for y in gap}
        statics, ring = W.walls_for(fl, openings, ws)
        statics = [s for s in statics if not (s[0] == 4 and s[1] == south_at)]
        statics += [(4, north_at, 0, hx(ws['frameNS']['first']), 'arch'), (4, south_at, 0, hx(ws['frameNS']['after']), 'arch')]
        land = {c: (floors['stone'], 0) for c in fl | ring | {(4, y) for y in range(0, 7)}}
        out[label] = (land, [(x, y, z, tid) for (x, y, z, tid, role) in statics])
    # a marble room split by a wall with a 2-tile gap each way, framed by the marble rule
    ws = rules['wallSets']['marble']
    for label, axis in (('marble gap N-S wall', 'y'), ('marble gap E-W wall', 'x')):
        if axis == 'y':
            fl = {(x, y) for x in range(0, 9) for y in range(0, 7) if x != 4} | {(4, 2), (4, 3)}
            openings = {(4, 2), (4, 3)}
        else:
            fl = {(x, y) for x in range(0, 9) for y in range(0, 7) if y != 3} | {(3, 3), (4, 3)}
            openings = {(3, 3), (4, 3)}
        statics, ring = W.walls_for(fl, openings, ws)
        solid = lambda c: c not in fl
        for g in W.opening_groups(openings, solid):
            for (x, y, tid, role, replaces) in W.frame_pieces(g, ws):
                if replaces:
                    statics = [s for s in statics if not (s[0] == x and s[1] == y)]
                statics.append((x, y, 0, tid, role))
        land = {c: (floors['marble'], 0) for c in fl | ring | openings}
        out[label] = (land, [(x, y, z, tid) for (x, y, z, tid, role) in statics])
    return out


def cave_test_scenes(rules):
    """An L-shaped cave room with the ring profile two ways: rock at the foot (round 2) and the Khaldun edge tile at
    the foot (round 3's Tangle). Returns {name: (land, statics)}."""
    out = {}
    fl = {(x, y) for x in range(4, 14) for y in range(4, 10)} | {(x, y) for x in range(4, 8) for y in range(10, 15)}
    ring = W.ring_of(fl)
    rng = random.Random(7)
    tangle = rules['zones']['Tangle']
    for label, edge in (('cave ring: rock foot (round 2)', False), ('cave ring: edge-tile foot (round 3)', True)):
        land = {c: (0x0245, 0) for c in fl}
        d2 = W.ring_of(fl | ring) - ring
        d3 = W.ring_of(fl | ring | d2) - ring - d2
        rock_beyond = lambda c: c not in fl and c not in ring
        for (x, y) in ring:
            if edge:
                sides = ''.join(k for k, n in (('N', (x, y - 1)), ('E', (x + 1, y)), ('S', (x, y + 1)), ('W', (x - 1, y))) if rock_beyond(n))
                key = sides if sides in EDGE_TILES else None
                if key is None:
                    diag = [k for k, n in (('NW', (x - 1, y - 1)), ('NE', (x + 1, y - 1)), ('SW', (x - 1, y + 1)), ('ES', (x + 1, y + 1))) if rock_beyond(n)]
                    key = {'NW': 'W', 'NE': 'E', 'SW': 'S', 'ES': 'S'}.get(diag[0]) if len(diag) == 1 else None
                land[(x, y)] = (hx(rng.choice(EDGE_TILES[key])), 0) if key else (weighted(rng, tangle['ring']), 0)
            else:
                land[(x, y)] = (weighted(rng, tangle['ring']), 0)
        for c in d2:
            land[c] = (weighted(rng, tangle['ring']), RAMP_Z)
        for c in d3:
            land[c] = (VOID, TOP_Z)
        xs = [c[0] for c in land]; ys = [c[1] for c in land]
        for x in range(min(xs) - 1, max(xs) + 2):
            for y in range(min(ys) - 1, max(ys) + 2):
                land.setdefault((x, y), (VOID, TOP_Z))
        out[label] = (land, [])
    return out


# ------------------------------------------------------------------------------------------------ main

def main():
    folder = sys.argv[1]
    plan_only = '--plan-only' in sys.argv
    layout = json.load(open(LAYOUT, encoding='utf-8'))
    rules = json.load(open(RULES, encoding='utf-8'))
    spawners, pts = read_points()
    land, statics, stats, counts, floor, opening, walls, report = plan(layout, rules, spawners, pts)
    print('stats', stats)
    for k, v in sorted(counts.items()):
        if v:
            print('  %5d  %s' % (v, k))
    print('corners per zone (concave, dressed, convex, what went in):')
    for zone, c in sorted(report['corners'].items()):
        print('  %-10s %s' % (zone, dict(c)))
    print('frames:', len(report['frames']), [(z, ax, len(t), ws) for z, ax, t, ws in report['frames']])
    print('doubled wall tiles:', report['doubled wall tiles'])
    print(audit.summary(report['slope audit']))
    # the walkable set must be the previous build's (P141's layout fixes it)
    if os.path.exists(CELLS):
        prev = json.load(open(CELLS))
        same = uofiles.same_cells(prev, floor, opening, walls)
        print('walkable floor, openings and wall tiles unchanged from plan-cells.json:', same)
        assert same, 'the walkable set changed: refusing to write'
    with open(os.path.join(HERE, 'statics-placed.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['x', 'y', 'z', 'id_hex', 'why'])
        for (x, y, z, tid, why) in sorted(statics):
            w.writerow([x, y, z, '0x%04X' % tid, why])
    byid = collections.Counter()
    for (x, y), (tid, z) in land.items():
        byid[(tid, z)] += 1
    with open(os.path.join(HERE, 'land-summary.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['land_id_hex', 'z', 'tiles'])
        for (tid, z), n in sorted(byid.items()):
            w.writerow(['0x%04X' % tid, z, n])
    json.dump({'floor': sorted(floor), 'opening': sorted(opening), 'walls': sorted(walls)}, open(CELLS, 'w'))
    with open(os.path.join(HERE, 'build-report.json'), 'w') as f:
        json.dump({'stats': stats, 'counts': counts, 'corners': {z: dict(c) for z, c in report['corners'].items()},
                   'frames': report['frames'], 'doubled': report['doubled wall tiles'], 'slope': report['slope audit']}, f, indent=1, default=list)
    if plan_only:
        return
    if '--fresh' in sys.argv:
        uofiles.restore_scratch(folder, FACET)
    changed = uofiles.write_land(folder, FACET, land)
    olds = collections.Counter(changed.values())
    print('land tiles written', len(changed), 'their old values', dict(olds))
    nblocks, kept = uofiles.write_statics(folder, FACET, statics)
    print('statics written', len(statics), 'in', nblocks, 'blocks; blocks that already held statics:', kept)
    bad, same, n = uofiles.verify(folder, FACET, land, statics)
    print('verify: land mismatches', bad, '; statics round-trip', same, '(%d read back)' % n)
    assert bad == 0 and same


if __name__ == '__main__':
    main()
