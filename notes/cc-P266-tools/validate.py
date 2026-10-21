# cc-P266 read only: checks every row of placement.json against the server's map files (through cc-P237's loader,
# nhbase.py: the client copy whose map, statics and art are SHA-256 equal to the shard's) and the protected tiles,
# and writes the notes table (validate.out.txt). Exit 1 if any row fails. Rules by mode (P34's, plus wallfoot):
#   every row  a unique key; no two rows on one tile at one z; the tile is not protected (protected.py); an item ID
#              that is one of the winter IDs (P34's 0x3C40-0x3C6E or this set's) or an OSI holiday ID
#   floor      GetTopSurfaceZ within 2 of z, no Impassable static in the way, not a walkway (road, plaza, pier, floor)
#   square     as floor, a walkway allowed (the square is all road)      pier: the same on the pier
#   wallfoot   as square, and a wall or column static on an orthogonal neighbour at or above the ground: a street tile
#              at the foot of a building's outer face (P267's "outside" rule), never a tile in the open
#   table      a Surface static whose top is z (a table)
#   wall       a wall at the floor z on the north (north facing) or west (west facing) neighbour, a floor within 2 of z
#   post       a lamp post static on the tile
#   indoor     as floor, on a floor (boards and tiles allowed)
#   wallout    a wall piece hung outside: the wall at z on the neighbour, the ground at or below z
import json, sys, csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, '..', 'cc-P237-tools'))   # after HERE: P237 has an art_src.py of its own
import nhbase as B, protected as PR, art_src as S
F = B.Facet(1)
NORTH = {0x232C, 0x2374, 0x2BD9, 0x2BDB, 15457, 15459, 15461, 15464, 15466, S.ID['ribbon-n'], S.ID['calendar-n']}
WEST = {0x232D, 0x2375, 0x2BDA, 0x2BDC, 15458, 15460, 15462, 15463, 15465, S.ID['ribbon-w'], S.ID['calendar-w']}
# the OSI holiday IDs pinned's own classes use (the test's OsiIds list, WinterDecorVerification.cs)
OSI = {0x2328, 0x2329, 0x232C, 0x232D, 0x2374, 0x2375, 0x2BD9, 0x2BDA, 0x2BDB, 0x2BDC, 0x1C12,
       0x08E2, 0x08E0, 0x08E6, 0x08E5, 0x08E3, 0x2377}
REG = 'D:/UO/golems/Bronze/ShatteredLegacy/player-package/vendor/shattered-legacy-art/registry.csv'
REGISTERED = {int(r['id']) for r in csv.DictReader(l for l in open(REG, encoding='ascii') if not l.startswith('#')) if r['kind'] == 'art'}
OURS = set(range(S.P34_FIRST, S.P34_LAST + 1)) | set(range(S.FIRST, S.LAST + 1))
A = B.art()


def tops(x, y):
    return [sz + B.calch(sid) for sid, sz in F.statics(x, y) if B.iflags(sid) & B.SURF and B.iflags(sid) & B.IMP]


def wall_or_column_beside(x, y, g):
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        for sid, sz in F.statics(nx, ny):
            if B.iflags(sid) & B.WALL and sz >= g: return '0x%04X at %d,%d z%d' % (sid, nx, ny, sz)
    return ''


def check(r, seen_keys, seen_tiles):
    x, y, z, item, mode = r['x'], r['y'], r['z'], r['itemId'], r['mode']
    errs = []
    if r['key'] in seen_keys: errs.append('duplicate key')
    if (x, y, z) in seen_tiles: errs.append('another row on this tile at this z: ' + seen_tiles[(x, y, z)])
    seen_keys.add(r['key']); seen_tiles[(x, y, z)] = r['key']
    if item in OURS:
        if S.P34_FIRST <= item <= S.P34_LAST and item not in REGISTERED: errs.append('not registered')
    elif item not in OSI: errs.append('neither a winter ID nor an OSI holiday ID')
    if item in OSI and A.static(item) is None: errs.append('no OSI art')
    prot = set(PR.P.get((x, y), ()))
    if mode == 'table':
        # a piece on a table top blocks nothing: a spawner's ring (an NPC's steps) does not bar the table beside it,
        prot = {p for p in prot if not p.startswith('spawner ') or p.split(' at ')[1].split(' ')[0] == '%d,%d' % (x, y)}
        # and the door scan's guessed swing cannot pass through a table either (a seeded door's swing still bars it)
        prot = {p for p in prot if not p.startswith('swing of doorgen')}
    if prot: errs.append('protected: ' + '; '.join(sorted(prot)))
    s = F.top_surface(x, y, z + 2)
    if mode in ('floor', 'square', 'pier', 'wallfoot'):
        if s is None or abs(s - z) > 2: errs.append('surface %s, row z %s' % (s, z))
        if F.blocked(x, y, z): errs.append('blocked by ' + F.blocked(x, y, z))
        if mode == 'floor' and B.walkway(F, x, y, z): errs.append('walkway ' + B.walkway(F, x, y, z))
        if mode == 'wallfoot' and not wall_or_column_beside(x, y, z): errs.append('no wall or column beside it')
    elif mode == 'indoor':
        if s is None or abs(s - z) > 2: errs.append('surface %s, row z %s' % (s, z))
        if F.blocked(x, y, z): errs.append('blocked by ' + F.blocked(x, y, z))
    elif mode == 'wallout':
        g = F.top_surface(x, y, z + 2)
        if g is None or g > z: errs.append('ground %s above the row z %s' % (g, z))
        if item in NORTH and not F.wall_at(x, y - 1, z): errs.append('north-wall art with no wall at %d,%d' % (x, y - 1))
        if item in WEST and not F.wall_at(x - 1, y, z): errs.append('west-wall art with no wall at %d,%d' % (x - 1, y))
        if item not in NORTH and item not in WEST: errs.append('wallout mode for an item with no wall facing')
    elif mode == 'table':
        if z not in tops(x, y): errs.append('no table top at z%d (tops %s)' % (z, tops(x, y)))
    elif mode == 'wall':
        if s is None or abs(s - z) > 2: errs.append('floor %s, row z %s' % (s, z))
        if item in NORTH and not F.wall_at(x, y - 1, z): errs.append('north-wall art with no wall at %d,%d' % (x, y - 1))
        if item in WEST and not F.wall_at(x - 1, y, z): errs.append('west-wall art with no wall at %d,%d' % (x - 1, y))
        if item not in NORTH and item not in WEST: errs.append('wall mode for an item with no wall facing')
    elif mode == 'post':
        if not any('lamp post' in B.iname(sid).lower() for sid, sz in F.statics(x, y)): errs.append('no lamp post')
    else:
        errs.append('unknown mode ' + mode)
    return errs


def main():
    rows = json.load(open(os.path.join(HERE, 'placement.json')))
    seen_keys, seen_tiles = set(), {}
    bad = 0
    out = ['| key | area | x,y,z | item | layer | mode | why | check |', '|---|---|---|---|---|---|---|---|']
    for r in rows:
        errs = check(r, seen_keys, seen_tiles)
        bad += bool(errs)
        out.append('| %s | %s | %d,%d,%d | 0x%04X %s | %s | %s | %s | %s |' % (r['key'], r['area'], r['x'], r['y'], r['z'], r['itemId'], r['name'], r['layer'], r['mode'], r['why'], 'ok' if not errs else 'FAIL: ' + ' / '.join(errs)))
    out.append('')
    out.append('%d rows, %d failing (%d of P34, %d new).' % (len(rows), bad, 61, len(rows) - 61))
    text = '\n'.join(out)
    print(text)
    open(os.path.join(HERE, 'validate.out.txt'), 'w', encoding='ascii', newline='\n').write(text + '\n')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
