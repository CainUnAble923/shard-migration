"""cc-P167: builds the Rootdeep Burrows (P141's approved layout, notes/art/rootdeep-mockup/layout.json) into a SCRATCH
copy of Trammel (map1LegacyMUL.uop in place, statics1.mul/staidx1.mul rewritten per block). Never run against the
client-data folder either repo or the shard reads: pass the scratch folder (D:/UO/cc-p167-work/scratch-client).

    python -P build_burrows.py <scratch folder> [--plan-only]

Look (Chase 10-18, P141-D8: the mockup page's proposed set per zone, its first set each):
  Landing   L-A dungeon stone cave: cave land 0x0245-0x0249, dungeon wall 0x0241 (west edge) / 0x0242 (north edge),
            corner 0x0243, post 0x0244
  Vault     V-A marble strongroom: marble land 0x0486-0x0489, marble wall 0x00F9 (west) / 0x00FA (north), corner 0x00F8,
            post 0x00FB; the Stacks' shelving rows are counters 0x0B40; the two Strongroom pillars are marble-walled blocks
  Warren    W-A dirt burrows: dirt 0x0071-0x0078, cave-rock ring 0x025A (OSI's cave walls are sloped land, not items:
            the Orc Cave at 5304-5308,1300 reads floor Z0 | 0x025A Z0 | Z10 | Z19 | Z26 | void), stalagmites, hay
  Tangle    T-A rooted cave: cave land, cave-rock ring 0x0266 (Deceit, Covetous), root masses as rock mounds with fallen
            logs, mushrooms
  Dawnseam  D-A crystal seam: crystal land 0x3867-0x386A, cave-rock ring 0x025A, crystal clusters 0x2224-0x2228
  Gloom     G-A Terathan dark stone: stone land 0x0440/0x0441, stone wall 0x01D0 (west) / 0x01D1 (north), post 0x01D2,
            web masses as stone pillars 0x01DA under webs 0x10B8, spiderwebs 0x0EE3
  Lair      Q-A: the Gloom's walls; web pillars the same way; more webs
  Crawlway  the two wall tiles 5160,1160-1161 are dirt under rocks 0x1367 (impassable); the server's RootdeepCrawlway
            item moves a credited player past them (RootdeepVault.cs)

Wall pieces (measured from the art, art-check in the notes): a piece whose pixels fill the LEFT half of its 44px tile
runs along the tile's WEST edge (the y axis on screen), one filling the RIGHT half runs along its NORTH edge (the x
axis). UO draws a room's north and west walls on the wall tiles' far edges and its south and east walls on the near
edges, so for a non-floor tile T: a north-edge piece when the tile south or north of T is floor, a west-edge piece
when the tile east or west of T is floor; the four outer corners follow from where the runs meet (NW both, NE west,
SW north, SE a post). Openings (the doorway, the gaps, the lair mouth, the crawlway) are passable and demand no
wall on their neighbours along the wall line, as a door tile in a house does not.

Every floor is Z 0 (the Vault's Doorway, LandingSpot and crawlway points in RootdeepVault.cs are Z 0, and the seeder
reads the floor Z with GetAverageZ). Rings beyond the cave zones rise to +12 then +20 (void), OSI's ramp.
"""
import json, os, random, re, struct, sys, csv, collections

sys.path.insert(0, r'D:\UO\shard-migration\notes\cc-P36-tools')
import uodata  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LAYOUT = r'D:\UO\shard-migration\notes\art\rootdeep-mockup\layout.json'
SEEDER = r'D:\ShatteredLegacy\server\customizations\ClusterFRootdeepSeeder.cs'
VAULT = r'D:\ShatteredLegacy\server\customizations\Regions\RootdeepVault.cs'
FACET_W, FACET_H = 7168, 4096
BH = FACET_H // 8
VOID = 0x0244
FLOOR_Z = 0
RAMP_Z, TOP_Z, MOUND_Z = 12, 20, 12

# zone key -> look. kind item: wall statics; kind land: cave-rock rings.
LOOK = {
    'Landing':   dict(kind='item', floor=[0x0245, 0x0246, 0x0247, 0x0248, 0x0249], W=0x0241, N=0x0242, C=[0x0243], P=0x0244),
    'Vault':     dict(kind='item', floor=[0x0486, 0x0487, 0x0488, 0x0489], W=0x00F9, N=0x00FA, C=[0x00F8], P=0x00FB),
    'Warren':    dict(kind='land', floor=[0x0071, 0x0072, 0x0073, 0x0074, 0x0075, 0x0076, 0x0077, 0x0078], ring=0x025A),
    'Brood Pit': dict(kind='land', floor=[0x0071, 0x0072, 0x0073, 0x0074, 0x0075, 0x0076, 0x0077, 0x0078], ring=0x025A),
    'Tangle':    dict(kind='land', floor=[0x0245, 0x0246, 0x0247, 0x0248, 0x0249], ring=0x0266),
    'Dawnseam':  dict(kind='land', floor=[0x3867, 0x3868, 0x3869, 0x386A], ring=0x025A),
    'Gloom':     dict(kind='item', floor=[0x0440, 0x0441], W=0x01D0, N=0x01D1, C=[0x01D0, 0x01D1], P=0x01D2),
    'Gloom lair': dict(kind='item', floor=[0x0440, 0x0441], W=0x01D0, N=0x01D1, C=[0x01D0, 0x01D1], P=0x01D2),
}
ITEM_ZONE_PRIORITY = ['Vault', 'Landing', 'Gloom lair', 'Gloom']
COUNTER, ROCKS, PILLAR, WEB, SPIDERWEB = 0x0B40, 0x1367, 0x01DA, 0x10B8, 0x0EE3
STALAGMITES = [0x08E1, 0x08E4, 0x08E5, 0x08E7]
HAY, MUSHROOMS, MUSHROOM, LOGS = 0x0F34, list(range(0x0D0C, 0x0D16)), 0x0D16, 0x0CF3
CRYSTALS = [0x2224, 0x2225, 0x2226, 0x2227, 0x2228]


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


def plan(layout, spawners, pts):
    """Returns land {(x,y): (id, z)}, statics [(x,y,z,id,why)], and the sets the notes report."""
    rng = random.Random(167)
    floor = {}        # (x,y) -> zone key, walkable floors incl. openings
    opening = set()   # floor tiles that cut through a wall line
    rect_of = {}      # (x,y) -> floor rect (for the corridor rule)
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

    obstacles = {}    # (x,y) -> (zone, name)
    for o in layout['obstacles']:
        for c in cells(o['rect']):
            obstacles[c] = (o['zone'], o['name'])
    for c in obstacles:
        floor.pop(c, None); opening.discard(c)
    F = lambda c: c in floor and c not in opening   # demands a wall
    anyfloor = lambda c: c in floor

    # Wall tiles: every non-floor tile touching a floor (8 neighbours). The mockup counts these (1,618).
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

    def put(x, y, tid, why, z=FLOOR_Z):
        statics.append((x, y, z, tid, why))
        counts[why] += 1

    # 1. floors (the openings too; the crawlway tiles get rocks below)
    for c, zone in floor.items():
        land[c] = (rng.choice(LOOK[zone]['floor']), FLOOR_Z)
    for c in crawl:
        land[c] = (LOOK['Warren']['floor'][0], FLOOR_Z)
        put(c[0], c[1], ROCKS, 'crawlway rocks')

    # 2. obstacles
    for c, (zone, name) in obstacles.items():
        x, y = c
        if zone == 'Vault' and 'shelving' in name:
            land[c] = (rng.choice(LOOK['Vault']['floor']), FLOOR_Z)
            put(x, y, COUNTER, 'Stacks shelving (counter)')
        elif zone == 'Vault':
            land[c] = (rng.choice(LOOK['Vault']['floor']), FLOOR_Z)   # pillar: walled by the wall rule below
        elif zone == 'Tangle':
            # a rock mound: rim tiles level with the floor, the inside raised; fallen logs on the rim
            x1, y1, x2, y2 = [r['rect'] for r in layout['obstacles'] if r['zone'] == 'Tangle' and c in cells(r['rect'])][0]
            rim = x in (x1, x2) or y in (y1, y2)
            land[c] = (LOOK['Tangle']['ring'], FLOOR_Z if rim else MOUND_Z)
            if rim and rng.random() < 0.35:
                put(x, y, LOGS, 'root mass: fallen log')
        elif zone == 'Dawnseam':
            land[c] = (rng.choice(LOOK['Dawnseam']['floor']), FLOOR_Z)
            put(x, y, rng.choice(CRYSTALS), 'crystal cluster')
        else:  # Gloom and lair web masses and pillars
            land[c] = (rng.choice(LOOK['Gloom']['floor']), FLOOR_Z)
            put(x, y, PILLAR, 'web mass: stone pillar')
            if rng.random() < 0.6:
                put(x, y, WEB, 'web mass: web', z=10)

    # 3. walls
    wall_zone = {c: zone_of_wall(c) for c in walls}
    ring = {}  # cave ring tiles -> zone
    for c in walls:
        if c in obstacles and obstacles[c][0] != 'Vault':
            continue   # the obstacle fill above stands
        x, y = c
        zone = wall_zone[c]
        look = LOOK[zone]
        if look['kind'] == 'land':
            ring[c] = zone
            continue
        land[c] = (rng.choice(look['floor']), FLOOR_Z)
        n = F((x, y + 1)) or F((x, y - 1)) \
            or (F((x + 1, y - 1)) and not F((x + 1, y)) and not F((x, y - 1))) \
            or (F((x + 1, y + 1)) and not F((x + 1, y)) and not F((x, y + 1)))
        w = F((x - 1, y)) or F((x + 1, y)) \
            or (F((x - 1, y + 1)) and not F((x - 1, y)) and not F((x, y + 1))) \
            or (F((x + 1, y + 1)) and not F((x + 1, y)) and not F((x, y + 1)))
        if n and w:
            for tid in look['C']:
                put(x, y, tid, '%s wall corner' % zone)
        elif n:
            put(x, y, look['N'], '%s wall north edge' % zone)
        elif w:
            put(x, y, look['W'], '%s wall west edge' % zone)
        elif F((x - 1, y - 1)):
            put(x, y, look['P'], '%s wall post' % zone)
        # else: a wall tile touching only an opening: floor land, no piece

    # 4. cave rings: ring tile at floor level, the next ring +12, the one beyond +20 (void), unless near an item zone
    def dist_to(targets, cmax):
        d = {}
        frontier = list(targets)
        for t in frontier:
            d[t] = 0
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
    land_floors = [c for c, z in floor.items() if LOOK[z]['kind'] == 'land']
    item_floors = [c for c, z in floor.items() if LOOK[z]['kind'] == 'item']
    dl = dist_to(land_floors, 3)
    di = dist_to(item_floors, 3)
    for c, zone in ring.items():
        land[c] = (LOOK[zone]['ring'], FLOOR_Z)
        counts['%s cave ring' % zone] += 1
    for c, d in dl.items():
        if c in land or c in floor:
            continue
        if di.get(c, 9) <= 2 or c[0] < layout['buildFromX']:
            continue   # near an item zone, or west of the build line (the ramp is cosmetic)
        if d == 2:
            land[c] = (LOOK[ring.get(c, 'Warren')]['ring'] if c in ring else 0x025A, RAMP_Z)
            counts['cave ramp +12'] += 1
        elif d == 3:
            land[c] = (VOID, TOP_Z)
            counts['void raised +20'] += 1

    # 5. decor on floors
    keep_clear = set()
    for sx, sy in spawners + list(pts.values()) + list(opening) + crawl:
        for ddx in range(-2, 3):
            for ddy in range(-2, 3):
                keep_clear.add((sx + ddx, sy + ddy))
    near_wall = lambda c: any((c[0] + a, c[1] + b) in walls for a in (-1, 0, 1) for b in (-1, 0, 1))
    def roomy(c):
        if c in keep_clear or c in opening:
            return False
        x1, y1, x2, y2 = rect_of[c]
        if x2 - x1 + 1 < 6 or y2 - y1 + 1 < 6:
            return False
        x, y = c
        # never pinch a path: at most one of the four orthogonal neighbours may be a wall, none an opening
        orth = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return sum(1 for n in orth if anyfloor(n)) >= 3 and not any(n in opening for n in orth)
    taken = {(s[0], s[1]) for s in statics}
    for c in sorted(floor):
        if c in taken or c in opening:
            continue
        zone = floor[c]
        x, y = c
        r = rng.random()
        if zone in ('Warren', 'Brood Pit'):
            if near_wall(c) and roomy(c) and r < 0.08:
                put(x, y, rng.choice(STALAGMITES), '%s stalagmites' % zone)
            elif not near_wall(c) and c not in keep_clear and r < 0.02:
                put(x, y, HAY, '%s hay' % zone)
        elif zone == 'Tangle':
            if c not in keep_clear and r < 0.05:
                put(x, y, rng.choice(MUSHROOMS) if r < 0.035 else MUSHROOM, 'Tangle mushrooms')
        elif zone == 'Dawnseam':
            if roomy(c) and r < 0.025:
                put(x, y, rng.choice(CRYSTALS), 'Dawnseam crystal')
        elif zone == 'Gloom':
            if near_wall(c) and c not in keep_clear and r < 0.08:
                put(x, y, WEB if r < 0.05 else SPIDERWEB, 'Gloom webs')
        elif zone == 'Gloom lair':
            if c not in keep_clear and r < 0.10:
                put(x, y, WEB if r < 0.06 else SPIDERWEB, 'lair webs')

    stats = dict(floor=len(floor) - len(opening) - len(crawl) + 0, openings=len(opening), walls=len(walls),
                 obstacles=len(obstacles), land_tiles=len(land), statics=len(statics))
    area = layout['area']
    for (x, y) in list(land) + [(s[0], s[1]) for s in statics]:
        assert area[0] <= x <= area[2] and area[1] <= y <= area[3], (x, y)
        assert x >= layout['buildFromX'], (x, y)
    return land, statics, stats, counts, floor, opening, walls


# ------------------------------------------------------------------------------------------------ writing the files

def write_land(folder, land):
    path = os.path.join(folder, 'map1LegacyMUL.uop')
    ver, ents, data, allents = uodata.uop_by_name(path, 'map1legacymul', '.dat', 0x14000, 8)
    data = bytearray(data)
    # chunk i holds dl bytes of consecutive 196-byte blocks, in name order
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
    removed = []
    for b, rows in sorted(by_block.items()):
        look, ln, extra = struct.unpack_from('<iii', idx, b * 12)
        existing = []
        if look >= 0 and ln > 0:
            for p in range(look, look + (ln // 7) * 7, 7):
                existing.append(struct.unpack_from('<HBBbh', sta, p))
        # nothing of EA's is in these blocks (P24 s2: the rectangle is void with zero statics); keep anything anyway
        rows = existing + rows
        newlook = len(sta)
        for r in rows:
            sta += struct.pack('<HBBbh', *r)
        struct.pack_into('<iii', idx, b * 12, newlook, len(rows) * 7, extra)
        if existing:
            removed.append((b, len(existing)))
    open(idx_path, 'wb').write(idx)
    open(sta_path, 'wb').write(sta)
    return len(by_block), removed


def verify(folder, land, statics):
    """Re-read the scratch files with the P36 readers and compare every planned tile."""
    # Cell order inside a block is (y & 7) * 8 + (x & 7) (pinned TileMatrix.GetLandTile); uodata.load_land's reshape
    # transposes the cells within a block, so the tiles are read here directly.
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
    spawners, pts = read_points()
    land, statics, stats, counts, floor, opening, walls = plan(layout, spawners, pts)
    print('stats', stats)
    for k, v in sorted(counts.items()):
        print('  %5d  %s' % (v, k))
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
              open(os.path.join(HERE, 'plan-sets.json'), 'w'))
    if plan_only:
        return
    changed = write_land(folder, land)
    olds = collections.Counter(changed.values())
    print('land tiles written', len(changed), 'their old values', dict(olds))
    nblocks, removed = write_statics(folder, statics)
    print('statics written', len(statics), 'in', nblocks, 'blocks; blocks that already held statics:', removed)
    bad, same, n = verify(folder, land, statics)
    print('verify: land mismatches', bad, '; statics round-trip', same, '(%d read back)' % n)
    assert bad == 0 and same


if __name__ == '__main__':
    main()
