# cc-P678 read only: cc-P266's row rules (notes/cc-P266-tools/validate.py) on SoS Haven, shared by draft.py (which
# searches for the nearest tile that passes) and validate.py (which checks every row). Rules by mode, as P266's:
#   every row  a unique key; one row per tile; the tile is not protected (protected.py); an item ID that is a winter ID
#              (P34's 0x3C40-0x3C6E, registered in registry.csv, or P266's 0x3388-0x33B6) or an OSI holiday ID;
#              NEW on SoS: the tile (a table: a tile beside it) is reached on foot from the start (3634,2586) by soswalk's walk (doorways open),
#              and its z is the walk's standing z (pinned movement rules and GetAverageZ) except on a table or post
#   floor      GetTopSurfaceZ within 2 of z, no Impassable static in the way, not a walkway (road, plaza, pier, floor)
#   square     as floor, a walkway allowed      pier: the same on the docks
#   wallfoot   as square, and a wall static on an orthogonal neighbour at or above the ground
#   table      a Surface static named table or counter whose top is z (SoS's tables are Surface, not Impassable, in
#              the vanilla tiledata, so P266's Surface+Impassable test would find none)
#   wall       a wall at the floor z on the north (north facing) or west (west facing) neighbour, a floor within 2 of z
#   post       a pinned cfg lamp post (LampPost1, an item on Trammel: SoS has no lamp post statics) on the tile, at its z;
#              that lamp post's own "decor" protection is the one the row may share
#   indoor     as floor, on a floor (boards and tiles allowed), under a roof
#   wallout    a wall piece hung outside: the wall at z on the neighbour, the ground at or below z
# The walk check after all rows (validate.py): every tile reached on foot from the start before the decor is still
# reached with every blocking row in place.
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))   # cc-P678-tools: soswalk
sys.path.append(os.path.join(HERE, '..', '..', 'cc-P266-tools'))   # art_src (after HERE: our protected.py wins)
import sosbase as B, protected as PR, soswalk, art_src as S

F = B.facet()
NORTH = {0x232C, 0x2374, 0x2BD9, 0x2BDB, 15457, 15459, 15461, 15464, 15466, S.ID['ribbon-n'], S.ID['calendar-n']}
WEST = {0x232D, 0x2375, 0x2BDA, 0x2BDC, 15458, 15460, 15462, 15463, 15465, S.ID['ribbon-w'], S.ID['calendar-w']}
OSI = {0x2328, 0x2329, 0x232C, 0x232D, 0x2374, 0x2375, 0x2BD9, 0x2BDA, 0x2BDB, 0x2BDC, 0x1C12,
       0x08E2, 0x08E0, 0x08E6, 0x08E5, 0x08E3, 0x2377}
REG = 'D:/UO/golems/Iron/ShatteredLegacy/player-package/vendor/shattered-legacy-art/registry.csv'
REGISTERED = {int(r['id']) for r in csv.DictReader(l for l in open(REG, encoding='ascii') if not l.startswith('#')) if r['kind'] == 'art'}
OURS = set(range(S.P34_FIRST, S.P34_LAST + 1)) | set(range(S.FIRST, S.LAST + 1))
# rows that block a walker: our art with Impassable (ClusterFWinterDecorArt.Records), the arches (taken as blocking:
# no record says otherwise) and the OSI pieces whose vanilla tiledata says Impassable
BLOCKING = {0x3C40, 0x3C45, 0x3C4A, 0x3C4E, 0x3C52, 0x3C60, 0x3C6E, 0x3388, 0x3393, 0x33A0, 0x33A8, 0x33B1, 0x3C57, 0x3C58}
BLOCKING |= {i for i in OSI if B.iflags(i) & B.IMP}
START = (3634, 2586)
W = soswalk.Walk((3540, 2440, 3790, 2730))
REACH = set(W.flood(START))


def tables(x, y):
    return [sz + B.calch(sid) for sid, sz in F.statics(x, y)
            if B.iflags(sid) & B.SURF and any(w in B.iname(sid).lower() for w in ('table', 'counter'))]


def wall_beside(x, y, g):
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        for sid, sz in F.statics(nx, ny):
            if B.iflags(sid) & B.WALL and sz >= g - 2: return '0x%04X at %d,%d z%d' % (sid, nx, ny, sz)
    return ''


def zfor(mode, x, y):
    """The row's z on this tile for the mode, or None."""
    if mode == 'table':
        t = tables(x, y)
        return max(t) if t else None
    if mode == 'post':
        return PR.LAMPS.get((x, y))
    return W.stand.get((x, y))


def check(r, taken=None):
    """-> list of failures for one row (dict with x, y, z, itemId, mode, key)."""
    x, y, z, item, mode = r['x'], r['y'], r['z'], r['itemId'], r['mode']
    errs = []
    if taken is not None and (x, y) in taken: errs.append('another row on this tile: ' + taken[(x, y)])
    if item in OURS:
        if S.P34_FIRST <= item <= S.P34_LAST and item not in REGISTERED: errs.append('not registered')
    elif item not in OSI: errs.append('neither a winter ID nor an OSI holiday ID')
    prot = set(PR.P.get((x, y), ()))
    if mode == 'table':
        prot = {p for p in prot if not p.startswith('spawner ') or p.split(' at ')[1].split(' ')[0] == '%d,%d' % (x, y)}
        prot = {p for p in prot if not p.startswith('swing of doorgen')}
    if mode == 'post':
        prot = {p for p in prot if not p.startswith('decor LampPost')}
    if prot: errs.append('protected: ' + '; '.join(sorted(prot)))
    stand = W.stand.get((x, y))
    if mode == 'table':   # a table top is reached from a tile beside it
        if not any(n in REACH for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))): errs.append('no tile beside the table is reached on foot')
    elif (x, y) not in REACH: errs.append('not reached on foot from the start (%s)' % (W.why.get((x, y)) or 'cut off'))
    if mode not in ('table', 'post') and stand != z: errs.append('walk z %s, row z %s' % (stand, z))
    s = F.top_surface(x, y, z + 2)
    if mode in ('floor', 'square', 'pier', 'wallfoot', 'indoor'):
        if s is None or abs(s - z) > 2: errs.append('surface %s, row z %s' % (s, z))
        if F.blocked(x, y, z): errs.append('blocked by ' + F.blocked(x, y, z))
        if mode == 'floor' and B.walkway(F, x, y, z): errs.append('walkway ' + B.walkway(F, x, y, z))
        if mode == 'floor' and F.roof_over(x, y, z): errs.append('under a roof')
        if mode == 'indoor' and not F.roof_over(x, y, z): errs.append('not under a roof')
        if mode == 'wallfoot' and not wall_beside(x, y, z): errs.append('no wall beside it')
    elif mode == 'wallout':
        if s is None or s > z: errs.append('ground %s above the row z %s' % (s, z))
        if item in NORTH and not F.wall_at(x, y - 1, z): errs.append('north-wall art with no wall at %d,%d' % (x, y - 1))
        if item in WEST and not F.wall_at(x - 1, y, z): errs.append('west-wall art with no wall at %d,%d' % (x - 1, y))
        if item not in NORTH and item not in WEST: errs.append('wallout mode for an item with no wall facing')
    elif mode == 'table':
        if z not in tables(x, y): errs.append('no table top at z%s (tops %s)' % (z, tables(x, y)))
    elif mode == 'wall':
        if s is None or abs(s - z) > 2: errs.append('floor %s, row z %s' % (s, z))
        if F.blocked(x, y, z): errs.append('blocked by ' + F.blocked(x, y, z))
        if item in NORTH and not F.wall_at(x, y - 1, z): errs.append('north-wall art with no wall at %d,%d' % (x, y - 1))
        if item in WEST and not F.wall_at(x - 1, y, z): errs.append('west-wall art with no wall at %d,%d' % (x - 1, y))
        if item not in NORTH and item not in WEST: errs.append('wall mode for an item with no wall facing')
    elif mode == 'post':
        if (x, y) not in PR.LAMPS: errs.append('no cfg lamp post')
        elif z != PR.LAMPS[(x, y)]: errs.append('lamp post z %d, row z %d' % (PR.LAMPS[(x, y)], z))
    else:
        errs.append('unknown mode ' + mode)
    return errs


def walk_cut(rows):
    """Tiles reached from the start before the decor and not after it, with every blocking row in place."""
    stand = dict(W.stand)
    blocked = {(r['x'], r['y']) for r in rows if r['itemId'] in BLOCKING and r['mode'] not in ('wall', 'wallout', 'post', 'table')}
    for t in blocked: stand[t] = None
    saved, W.stand = W.stand, stand
    try:
        after = set(W.flood(START))
    finally:
        W.stand = saved
    return sorted(REACH - after - blocked)
