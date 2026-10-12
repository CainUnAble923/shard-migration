# cc-P34 read only: checks every row of placement.json against the map and the protected tiles, and prints the
# notes table. Exit 1 if any row fails. Rules by mode:
#   all     not a protected tile (protected.py: doors and swings, NPC posts, spawners, board, arrival, Reset Stone,
#           the field office's components); an item ID that is registered (ours) or has art (OSI)
#   floor   GetTopSurfaceZ within 2 of z, no Impassable static in the way, not a walkway
#   square  as floor, a walkway allowed (the square is all road)    pier: the same on the pier
#   table   a Surface static whose top is z (a table)
#   wall    a wall at the floor z on the north (north facing) or west (west facing) neighbour, surface at z
#   post    a lamp post static on the tile
#   indoor  as floor, on a floor (boards and tiles allowed)
#   wallout a wall piece hung outside: the wall at z on the neighbour, the ground at or below z
import json, sys, csv
exec(open('pick.py').read())
NORTH = {0x232C, 0x2374, 0x2BD9, 0x2BDB, 15457, 15459, 15461, 15464, 15466}
WEST = {0x232D, 0x2375, 0x2BDA, 0x2BDC, 15458, 15460, 15462, 15463, 15465}
REG = {int(r['id']) for r in csv.DictReader(l for l in open(r'D:/ShatteredLegacy/player-package/vendor/shattered-legacy-art/registry.csv') if not l.startswith('#'))}
ART = RNS['Art']()
rows = json.load(open('placement.json'))
bad = 0
seen_keys, seen_tiles = set(), set()
out = []
for r in rows:
    x, y, z, item, mode = r['x'], r['y'], r['z'], r['itemId'], r['mode']
    errs = []
    if (x, y) in P: errs.append('protected: ' + '; '.join(P[(x, y)]))
    if item >= 15424 and item not in REG: errs.append('not registered')
    if item < 15424 and ART.static(item) is None: errs.append('no OSI art')
    if r['key'] in seen_keys: errs.append('duplicate key')
    if (x, y, item) in seen_tiles: errs.append('duplicate tile and item')
    seen_keys.add(r['key']); seen_tiles.add((x, y, item))
    s = top_surface(x, y, z + 2)
    if mode in ('floor', 'square', 'pier'):
        if s is None or abs(s - z) > 2: errs.append('surface %s, row z %s' % (s, z))
        if blocked(x, y, z): errs.append('blocked by ' + blocked(x, y, z))
        if mode == 'floor' and walkway(x, y, z): errs.append('walkway ' + walkway(x, y, z))
    elif mode == 'indoor':
        if s is None or abs(s - z) > 2: errs.append('surface %s, row z %s' % (s, z))
        if blocked(x, y, z): errs.append('blocked by ' + blocked(x, y, z))
    elif mode == 'wallout':
        g = top_surface(x, y, z + 2)
        if g is None or g > z: errs.append('ground %s above the row z %s' % (g, z))
        if item in NORTH and not wall_at(x, y - 1, z): errs.append('north-wall art with no wall at %d,%d' % (x, y - 1))
        if item in WEST and not wall_at(x - 1, y, z): errs.append('west-wall art with no wall at %d,%d' % (x - 1, y))
    elif mode == 'table':
        tops = [sz + calch(sid) for sid, sz in statics(x, y) if T.sflags[sid] & SURF and T.sflags[sid] & IMP]
        if z not in tops: errs.append('no table top at z%d (tops %s)' % (z, tops))
    elif mode == 'wall':
        if s is None or abs(s - z) > 2: errs.append('floor %s, row z %s' % (s, z))
        if item in NORTH and not wall_at(x, y - 1, z): errs.append('north-wall art with no wall at %d,%d' % (x, y - 1))
        if item in WEST and not wall_at(x - 1, y, z): errs.append('west-wall art with no wall at %d,%d' % (x - 1, y))
        if item not in NORTH and item not in WEST: errs.append('wall mode for an item with no wall facing')
    elif mode == 'post':
        if not any('lamp post' in name(sid).lower() for sid, sz in statics(x, y)): errs.append('no lamp post')
    else:
        errs.append('unknown mode')
    ok = 'ok' if not errs else 'FAIL: ' + ' | '.join(errs)
    bad += bool(errs)
    out.append('| %s | %s | %d,%d,%s | 0x%04X %s | %s | %s | %s | %s |' % (r['key'], r['area'], x, y, z, item, r['name'], r['layer'], r['mode'], r['why'], ok))
print('| key | area | x,y,z | item | layer | mode | why | check |')
print('|---|---|---|---|---|---|---|---|')
print('\n'.join(out))
print('\n%d rows, %d failing' % (len(rows), bad))
sys.exit(1 if bad else 0)
