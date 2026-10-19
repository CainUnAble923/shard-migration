"""cc-P167 / cc-P180: builds the Rootdeep Burrows (P141's approved layout, notes/art/rootdeep-mockup/layout.json) into
a SCRATCH copy of Trammel (map1LegacyMUL.uop in place, statics1.mul/staidx1.mul rewritten per block). Never run against
the client-data folder either repo or the shard reads: pass the scratch folder (D:/UO/cc-p167-work/scratch-client).

    python -P build_burrows.py <scratch folder> [--plan-only] [--fresh]

  --plan-only   writes the CSVs and plan-cells.json, touches no map file
  --fresh       first restores the scratch map, statics and index from the shard's client-data copy (read only; the
                copies must hash as ORIGINAL-SHA256.txt beside them), so a rebuild never stacks on an old build

The look comes from plan-sets.json beside this file (one seed per zone, tile weights, decor rules, the proposals);
nothing about the look is in this code. P141's layout fixes the walkable floor; this builder never changes it (it
checks its walkable set against the previous build's plan-cells.json and refuses to write if they differ).

Walls (cc-P180, notes/uo-wall-orientation.md, measured on OSI buildings and house multis): a wall piece's art stands
on its own tile's SOUTH edge (the "ew" piece, running along x) or EAST edge (the "ns" piece, running along y); the
corner piece carries both; the post marks the tile's south-east corner point. So for a solid tile T beside floor F:
    needS = F north or south of T, or a diagonal floor to the SW or NW with no floor west of T (an outer corner)
    needE = F east or west of T, or a diagonal floor to the NE or NW with no floor north of T
    both -> corner; needS -> ew; needE -> ns; neither but floor to the SE -> post (the room's NW corner)
Openings (the doorway, the gaps, the lair mouth, the crawlway) are floor that demands no slab, as a door tile in a
house does. P167 had the two pieces swapped and the corner and post on the wrong corners, because it assumed the art
sat on the north and west edges: that is the saw-tooth Chase saw.

Cave zones (Warren, Brood Pit, Tangle, Dawnseam) use raised cave-rock land, as OSI's caves do: ring at floor level,
then +12, then void at +20. Every floor is Z 0 (RootdeepVault.cs points and the seeder's GetAverageZ read Z 0).
"""
import collections, csv, hashlib, json, os, random, re, shutil, struct, sys

sys.path.insert(0, r'D:\UO\shard-migration\notes\cc-P36-tools')
import uodata  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LAYOUT = r'D:\UO\shard-migration\notes\art\rootdeep-mockup\layout.json'
RULES = os.path.join(HERE, 'plan-sets.json')
CELLS = os.path.join(HERE, 'plan-cells.json')
SEEDER = r'D:\ShatteredLegacy\server\customizations\ClusterFRootdeepSeeder.cs'
VAULT = r'D:\ShatteredLegacy\server\customizations\Regions\RootdeepVault.cs'
CLIENT = uodata.NEW
FACET_W, FACET_H = 7168, 4096
BH = FACET_H // 8
VOID = 0x0244
FLOOR_Z = 0
RAMP_Z, TOP_Z = 12, 20
IMPASSABLE = 1 << 6
ITEM_ZONE_PRIORITY = ['Vault', 'Landing', 'Gloom lair', 'Gloom']

_TILEDATA = None


def tiledata():
    global _TILEDATA
    if _TILEDATA is None:
        _TILEDATA = uodata.read_tiledata(CLIENT)
    return _TILEDATA


def hx(v):
    return int(v, 16) if isinstance(v, str) else int(v)


def weighted(rng, table):
    ids = [hx(k) for k in table]
    return rng.choices(ids, weights=[table[k] for k in table])[0]


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


# ------------------------------------------------------------------------------------------------ the wall rule

def wall_pieces(F, x, y, ws):
    """Pieces for the solid tile (x, y). F(c) is true for a floor tile that demands a wall (openings excluded).
    Returns a list of (tileId, role); role is one of ew, ns, corner, post."""
    N, S, E, W = F((x, y - 1)), F((x, y + 1)), F((x + 1, y)), F((x - 1, y))
    NE, NW, SE, SW = F((x + 1, y - 1)), F((x - 1, y - 1)), F((x + 1, y + 1)), F((x - 1, y + 1))
    needS = N or S or (SW and not W and not S) or (NW and not W and not N)
    needE = E or W or (NE and not N and not E) or (NW and not N and not W)
    if needS and needE:
        if ws.get('corner'):
            return [(hx(ws['corner']), 'corner')]
        return [(hx(ws['ew']), 'ew'), (hx(ws['ns']), 'ns')]
    if needS:
        return [(hx(ws['ew']), 'ew')]
    if needE:
        return [(hx(ws['ns']), 'ns')]
    if SE:
        return [(hx(ws['post']), 'post')]
    return []


def walls_for(floor, openings, ws):
    """Wall statics (x, y, z, id, role) for a floor set (openings are floor tiles that cut a wall line)."""
    F = lambda c: c in floor and c not in openings
    ring = set()
    for (x, y) in floor:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (x + dx, y + dy) not in floor:
                    ring.add((x + dx, y + dy))
    out = []
    for (x, y) in sorted(ring):
        for tid, role in wall_pieces(F, x, y, ws):
            out.append((x, y, FLOOR_Z, tid, role))
    return out, ring


# ------------------------------------------------------------------------------------------------ the plan

def plan(layout, rules, spawners, pts, quiet=False):
    """Returns land {(x,y): (id, z)}, statics [(x,y,z,id,why)], stats, counts, and the sets the notes report."""
    items = tiledata()[1]
    impassable = lambda tid: bool(items[tid]['flags'] & IMPASSABLE)
    zones = rules['zones']
    rngs = {z: random.Random(zones[z]['seed']) for z in zones}
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
    walls = set()
    for (x, y) in floor:
        for ddx in (-1, 0, 1):
            for ddy in (-1, 0, 1):
                n = (x + ddx, y + ddy)
                if n not in floor:
                    walls.add(n)

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

    # 1. floors: weighted draw per tile from the zone's table, one rng per zone
    for c, zone in sorted(floor.items()):
        land[c] = (weighted(rngs[zone], zones[zone]['floor']), FLOOR_Z)
    for c in crawl:
        land[c] = (hx(next(iter(zones['Warren']['floor']))), FLOOR_Z)
        put(c[0], c[1], weighted(rngs['Warren'], rules['crawlway']['rocks']), 'crawlway rocks')

    # 2. obstacles (solid blocks inside a floor), by the rule named after the block
    def obstacle_rule(name):
        for key, rule in rules['obstacles'].items():
            if name.startswith(key):
                return key, rule
        raise KeyError(name)
    wall_blocks = set()
    for c, (zone, name, rect) in sorted(obstacles.items()):
        x, y = c
        key, rule = obstacle_rule(name)
        rng = rngs[zone]
        if rule['kind'] == 'walls':
            land[c] = (weighted(rng, zones[zone]['floor']), FLOOR_Z)
            wall_blocks.add(c)
        elif rule['kind'] == 'items':
            land[c] = (weighted(rng, zones[zone]['floor']), FLOOR_Z)
            if key == 'Stacks shelving' and not rules['proposals'].get('stacksBookcases', True):
                put(x, y, 0x0B40, 'Stacks shelving (counter)')
            else:
                tid = pick_unlike(rng, rule['ids'], c, by_tile)
                put(x, y, tid, rule['why'], z=rng.choice(rule.get('z', [0])))
            for extra in rule.get('extra', []):
                if rng.random() < extra['p']:
                    put(x, y, pick_unlike(rng, extra['ids'], c, by_tile), extra['why'], z=rng.choice(extra['z']))
        elif rule['kind'] == 'mound':
            x1, y1, x2, y2 = rect
            rim = x in (x1, x2) or y in (y1, y2)
            land[c] = (weighted(rng, rule['rim']), FLOOR_Z) if rim else (weighted(rng, rule['inside']), rule['insideZ'])
            dec = rule['rimDecor'] if rim else rule['insideDecor']
            if rng.random() < dec['p']:
                put(x, y, pick_unlike(rng, dec['ids'], c, by_tile), dec['why'], z=rng.choice(dec['z']))
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
        for tid, role in wall_pieces(F, x, y, rules['wallSets'][look['wallSet']]):
            put(x, y, tid, '%s wall %s' % (zone, role))
    for c in sorted(wall_blocks):
        if c not in walls:   # an inner tile of a pillar block: floor land, nothing else (the ring tiles carry the walls)
            continue

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
    ring_zone_near = {}
    for c, zone in sorted(ring.items()):
        land[c] = (weighted(rngs[zone], zones[zone]['ring']), FLOOR_Z)
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
            scatter(rng, rule, elig, taken, by_tile, put, roomy, impassable, decor_blocked)

    # 6. the proposals Chase has not answered (P167 s5): shown, not approved
    props = rules.get('proposals', {})
    arch = props.get('lairArch')
    if arch and arch.get('on'):
        for key in ('north', 'south'):
            tid, (ax, ay) = hx(arch[key][0]), tuple(arch[key][1])
            if (ax, ay) in walls:
                statics[:] = [s for s in statics if not (s[0] == ax and s[1] == ay and 'wall' in s[4])]
                counts['Gloom lair wall ns'] -= 1
            put(ax, ay, tid, 'lair mouth arch (proposal)')
    for (wx, wy, wz, wid) in props.get('mouthWebs', []):
        put(wx, wy, hx(wid), 'lair mouth webs (proposal)', z=wz)

    # 7. checks: the walkable set is exactly the floor (every floor tile free of impassable statics and on passable land,
    #    every obstacle tile blocked), nothing outside the area or west of the build line
    land_flags = tiledata()[0]
    blocked = lambda c: any(impassable(t) for t in by_tile.get(c, [])) or (c in land and land_flags[land[c][0]][0] & IMPASSABLE)
    bad_floor = sorted(c for c in floor if blocked(c) and c not in crawl and c not in decor_blocked)
    bad_obst = sorted(c for c in obstacles if not blocked(c) and c not in wall_blocks)
    assert not bad_floor, ('floor tiles blocked by something other than roomy decor', bad_floor[:10])
    assert all(roomy(c) and c not in keep_clear for c in decor_blocked), 'impassable decor on a tile that matters'
    counts['floor tiles under impassable decor (each with 3 open sides, in a room 6+ wide, off every path and spawn)'] = len(decor_blocked)
    assert not bad_obst, ('obstacle tiles open', bad_obst[:10])
    for c in wall_blocks:
        assert c not in walls or by_tile.get(c), ('pillar ring tile without a wall piece', c)
    area = layout['area']
    for (x, y) in list(land) + [(s[0], s[1]) for s in statics]:
        assert area[0] <= x <= area[2] and area[1] <= y <= area[3], (x, y)
        assert x >= layout['buildFromX'], (x, y)
    stats = dict(floor=len(floor) - len(opening), openings=len(opening), walls=len(walls),
                 obstacles=len(obstacles), land_tiles=len(land), statics=len(statics))
    return land, statics, stats, counts, floor, opening, walls


def pick_unlike(rng, table, c, by_tile, tries=8):
    """A weighted draw that avoids the ids already on the 8 neighbouring tiles (no two identical pieces side by side)."""
    x, y = c
    near = set()
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            near.update(by_tile.get((x + a, y + b), []))
    tid = weighted(rng, table)
    for _ in range(tries):
        if tid not in near:
            break
        tid = weighted(rng, table)
    return tid


def scatter(rng, rule, eligible, taken, by_tile, put, roomy, impassable, decor_blocked):
    """Clusters with gaps: cluster centres at least `spacing` apart, each with cluster [min,max] pieces within
    `radius`, ids drawn by weight and never equal to a neighbour's, z from the rule's list."""
    elig = [c for c in eligible if c not in taken]
    eligset = set(elig)
    n = rule.get('count') or int(round(len(elig) * rule['density']))
    spacing, radius, size = rule.get('spacing', 3), rule.get('radius', 1), rule.get('cluster', [1, 1])
    rng.shuffle(elig)
    centres = []
    for c in elig:
        if len(centres) >= n:
            break
        if all(max(abs(c[0] - o[0]), abs(c[1] - o[1])) >= spacing for o in centres):
            centres.append(c)
    for c in centres:
        k = rng.randint(size[0], size[1])
        cand = [(c[0] + a, c[1] + b) for a in range(-radius, radius + 1) for b in range(-radius, radius + 1) if (a, b) != (0, 0)]
        cand = [t for t in cand if t in eligset and t not in taken]
        rng.shuffle(cand)
        for t in [c] + cand[:k - 1]:
            if t in taken:
                continue
            tid = pick_unlike(rng, rule['ids'], t, by_tile)
            if impassable(tid):
                if not roomy(t):
                    continue
                decor_blocked.add(t)
            put(t[0], t[1], tid, rule['name'], z=rng.choice(rule.get('z', [0])))
            taken.add(t)


# ------------------------------------------------------------------------------------------------ test rooms (P180 s1.1)

def test_room_scenes(rules):
    """A 5 x 5 room and an L-shaped room in each item wall set, built by walls_for, plus the stone set's arched
    north-south doorway two ways. Returns {name: (land, statics)} for isorender (floor land per set)."""
    floors = {'dungeon': 0x0245, 'marble': 0x0486, 'stone': 0x0440}
    out = {}
    for name, ws in rules['wallSets'].items():
        sq = {(x, y) for x in range(0, 5) for y in range(0, 5)}
        L = {(x, y) for x in range(10, 18) for y in range(0, 5)} | {(x, y) for x in range(10, 14) for y in range(5, 10)}
        for label, fl in (('%s 5x5' % name, sq), ('%s L' % name, L)):
            statics, ring = walls_for(fl, set(), ws)
            land = {c: (floors[name], 0) for c in fl | ring}
            # a little ground around, so the picture has an edge
            xs = [c[0] for c in land]; ys = [c[1] for c in land]
            for x in range(min(xs) - 1, max(xs) + 2):
                for y in range(min(ys) - 1, max(ys) + 2):
                    land.setdefault((x, y), (VOID, 0))
            out[label] = (land, [(x, y, z, tid) for (x, y, z, tid, role) in statics])
    # the lair mouth both ways: a 9 x 7 stone room split by a north-south wall at x 4 with a gap; (a) 3 tiles open,
    # arch halves on the first open tile and the wall tile after the gap; (b) OSI's 2-tile doorway
    ws = rules['wallSets']['stone']
    for label, gap, north_at, south_at in (('stone mouth 3 open', [2, 3, 4], 2, 5), ('stone mouth 2 open', [2, 3], 2, 4)):
        fl = {(x, y) for x in range(0, 9) for y in range(0, 7) if x != 4} | {(4, y) for y in gap}
        openings = {(4, y) for y in gap}
        statics, ring = walls_for(fl, openings, ws)
        statics = [s for s in statics if not (s[0] == 4 and s[1] == south_at)]
        statics += [(4, north_at, 0, hx(ws['archNS'][0]), 'arch'), (4, south_at, 0, hx(ws['archNS'][1]), 'arch')]
        land = {c: (floors['stone'], 0) for c in fl | ring | {(4, y) for y in range(0, 7)}}
        out[label] = (land, [(x, y, z, tid) for (x, y, z, tid, role) in statics])
    return out


# ------------------------------------------------------------------------------------------------ writing the files

def restore_scratch(folder):
    """--fresh: copy the three Trammel files from the shard's client-data copy (never written to) over the scratch
    ones, and prove them pristine against ORIGINAL-SHA256.txt."""
    want = {}
    for line in open(os.path.join(folder, 'ORIGINAL-SHA256.txt')):
        h, _, name = line.strip().partition(' *scratch-client/')
        if name:
            want[name] = h
    for name in ('map1LegacyMUL.uop', 'statics1.mul', 'staidx1.mul'):
        src = os.path.join(CLIENT, name)
        h = hashlib.sha256(open(src, 'rb').read()).hexdigest()
        assert h == want[name], (name, h, want[name])
        shutil.copyfile(src, os.path.join(folder, name))
        print('restored', name, h[:12])


def write_land(folder, land):
    path = os.path.join(folder, 'map1LegacyMUL.uop')
    ver, ents, data, allents = uodata.uop_by_name(path, 'map1legacymul', '.dat', 0x14000, 8)
    data = bytearray(data)
    starts = []
    pos = 0
    for i in sorted(ents):
        e = ents[i]
        assert e['flag'] == 0
        starts.append((pos, pos + e['dl'], e['off'] + e['hl']))
        pos += e['dl']

    def file_offset(b):
        off = b * 196
        for s, e_, fo in starts:
            if s <= off < e_:
                return fo + (off - s)
        raise ValueError(b)
    changed = {}
    for (x, y), (tid, z) in land.items():
        b = (x >> 3) * BH + (y >> 3)
        cell = (y & 7) * 8 + (x & 7)
        o = file_offset(b) + 4 + cell * 3
        old = struct.unpack_from('<Hb', data, o)
        struct.pack_into('<Hb', data, o, tid, z)
        changed[(x, y)] = old
    open(path, 'wb').write(data)
    return changed


def write_statics(folder, statics):
    idx_path, sta_path = os.path.join(folder, 'staidx1.mul'), os.path.join(folder, 'statics1.mul')
    idx = bytearray(open(idx_path, 'rb').read())
    sta = bytearray(open(sta_path, 'rb').read())
    by_block = collections.defaultdict(list)
    for (x, y, z, tid, why) in statics:
        by_block[(x >> 3) * BH + (y >> 3)].append((tid, x & 7, y & 7, z, 0))
    kept = []
    for b, rows in sorted(by_block.items()):
        look, ln, extra = struct.unpack_from('<iii', idx, b * 12)
        existing = []
        if look >= 0 and ln > 0:
            for p in range(look, look + (ln // 7) * 7, 7):
                existing.append(struct.unpack_from('<HBBbh', sta, p))
        rows = existing + rows
        newlook = len(sta)
        for r in rows:
            sta += struct.pack('<HBBbh', *r)
        struct.pack_into('<iii', idx, b * 12, newlook, len(rows) * 7, extra)
        if existing:
            kept.append((b, len(existing)))
    open(idx_path, 'wb').write(idx)
    open(sta_path, 'wb').write(sta)
    return len(by_block), kept


def verify(folder, land, statics):
    """Re-read the scratch files with the P36 readers and compare every planned tile."""
    ver, ents, data, allents = uodata.uop_by_name(os.path.join(folder, 'map1LegacyMUL.uop'), 'map1legacymul', '.dat', 0x14000, 8)
    raw = b''.join(data[ents[i]['off'] + ents[i]['hl']:ents[i]['off'] + ents[i]['hl'] + ents[i]['dl']] for i in sorted(ents))
    bad = 0
    for (x, y), (tid, z) in land.items():
        o = ((x >> 3) * BH + (y >> 3)) * 196 + 4 + ((y & 7) * 8 + (x & 7)) * 3
        if struct.unpack_from('<Hb', raw, o) != (tid, z):
            bad += 1
    idx, sta = uodata.load_statics_index(folder, 1)
    want = collections.Counter((x, y, z, tid) for (x, y, z, tid, _) in statics)
    have = collections.Counter()
    for b in {(x >> 3) * BH + (y >> 3) for (x, y, _, _, _) in statics}:
        bx, by = divmod(b, BH)
        for (tid, cx, cy, z, hue) in uodata.block_statics(idx, sta, b):
            have[(bx * 8 + cx, by * 8 + cy, z, tid)] += 1
    return bad, want == have, sum(have.values())


def main():
    folder = sys.argv[1]
    plan_only = '--plan-only' in sys.argv
    layout = json.load(open(LAYOUT, encoding='utf-8'))
    rules = json.load(open(RULES, encoding='utf-8'))
    spawners, pts = read_points()
    land, statics, stats, counts, floor, opening, walls = plan(layout, rules, spawners, pts)
    print('stats', stats)
    for k, v in sorted(counts.items()):
        print('  %5d  %s' % (v, k))
    # the walkable set must be the previous build's (P141's layout fixes it)
    if os.path.exists(CELLS):
        prev = json.load(open(CELLS))
        same = (sorted(map(tuple, prev['floor'])) == sorted(floor) and sorted(map(tuple, prev['opening'])) == sorted(opening)
                and sorted(map(tuple, prev['walls'])) == sorted(walls))
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
    json.dump({'floor': sorted(floor), 'opening': sorted(opening), 'walls': sorted(walls)},
              open(CELLS, 'w'))
    if plan_only:
        return
    if '--fresh' in sys.argv:
        restore_scratch(folder)
    changed = write_land(folder, land)
    olds = collections.Counter(changed.values())
    print('land tiles written', len(changed), 'their old values', dict(olds))
    nblocks, kept = write_statics(folder, statics)
    print('statics written', len(statics), 'in', nblocks, 'blocks; blocks that already held statics:', kept)
    bad, same, n = verify(folder, land, statics)
    print('verify: land mismatches', bad, '; statics round-trip', same, '(%d read back)' % n)
    assert bad == 0 and same


if __name__ == '__main__':
    main()
