# cc-P678 read only: cc-P237-tools/validate.py's checks on SoS Haven. Checks every row of art/placement.json against
# the SoS map files (sosbase.SosFacet, pinned's z rules), soswalk (pinned's movement rules) and the protected tiles
# (art_protected.py), prints the notes table and writes art-validate.out.txt. Exit 1 if any row fails.
# P237's rules, kept as they were:
#   every row  a unique key; no two rows on one tile at one z; the item is one of this set's IDs (art_src); the tile is
#              not protected (art_protected.py: doors and swings, seeded coordinates, pinned spawners and their ring,
#              pinned decoration, teleporters, kept-clear tiles (HavenSpots, homes.csv, the hatch), the way in)
#   ground     the ground's top surface (pinned GetTopSurfaceZ at the land's z) is the row's z, nothing impassable in
#              the way, not a road or plaza walkway
#   camp       as ground, and the camp rules: at least 3 tiles from every tile of the way in, and outside every pinned
#              creature spawner's walking box (location +/- walkingRange, or homeRange when larger). Spawners whose
#              range covers the whole town (50 or more) are left out and named in the output.
#   edge       as ground, a walkway allowed (beside steps or a door)
#   indoor     a floor surface within 2 of z, nothing impassable in the way
#   wall       north-wall art: a wall at the floor z on the tile's north neighbour, a floor within 2 of z, and no
#              wall decoration on the tile or either neighbour along the wall (WALLART)
#   posttop    a pier post whose top is z (the lantern sits on it)
#   beam       a floor surface at z with a deck (Surface) 10 to 20 above it on the same tile
# Added for SoS (cc-P678):
#   stand      every row but posttop and beam: soswalk stands a walker on the tile at the row's z (within 2), and the
#              tile is reachable on foot from New Haven's start (3634,2586)
#   camp       also outside the town (pinned's "Haven" region box, 3568-3761, 2460-2712)
#   in the way every impassable piece put down at once (as statics, into soswalk) leaves every tile that was reachable
#              from the start still reachable, but the pieces' own tiles: no row cuts a way, a door or an NPC off
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'cc-P237-tools'))
import sosbase as B, art_protected as PR, p678_extra as X
import art_src as S
import soswalk
F = B.sos()
OURS = set(first for first, key, what, pack, files, how in S.GROUPS)
TOWN = (3568, 2460, 3761, 2712)
TOWNWIDE = 50
WALLART = ('painting', 'portrait', 'picture', 'tapestry', 'banner', 'map', 'sign', 'mirror', 'trophy', 'mounted', 'shield', 'flag', 'deer head', 'bear head')
WALK = X.walk()
REACH = set(WALK.flood(X.START))


def creature_spawners():
    out, skipped = [], []
    for (mp, x, y, z, hr, wr, names, fn) in B.spawns_all():
        if not (3500 <= x <= 3800 and 2420 <= y <= 2740): continue
        r = max(hr, wr)
        (skipped if r >= TOWNWIDE else out).append((x, y, r, '/'.join(n for n in names if n)[:40] or 'Spawner', fn))
    return out, skipped
SPAWN, SKIPPED = creature_spawners()


def check(r, seen_keys, seen_tiles):
    x, y, z, item, mode = r['x'], r['y'], r['z'], r['itemId'], r['mode']
    errs = []
    if r['key'] in seen_keys: errs.append('duplicate key')
    if (x, y, z) in seen_tiles: errs.append('another row on this tile at this z: ' + seen_tiles[(x, y, z)])
    seen_keys.add(r['key']); seen_tiles[(x, y, z)] = r['key']
    if item not in OURS: errs.append('not one of this set\'s IDs')
    if not PR.inbox(x, y): errs.append('outside the checked box %s' % (PR.BOX,))
    if (x, y) in PR.P: errs.append('protected: ' + '; '.join(sorted(set(PR.P[(x, y)]))))
    if mode in ('ground', 'camp', 'edge'):
        g = F.avgz(x, y)
        s = F.top_surface(x, y, g + 2)
        if s != z: errs.append('ground surface %s, row z %s' % (s, z))
        if F.blocked(x, y, z): errs.append('blocked by ' + F.blocked(x, y, z))
        if mode != 'edge' and B.walkway(F, x, y, z): errs.append('walkway ' + B.walkway(F, x, y, z))
        if mode == 'camp':
            d = min(max(abs(x - px), abs(y - py)) for px, py in PR.PATH)
            if d < 3: errs.append('%d tiles from the way in' % d)
            if TOWN[0] <= x <= TOWN[2] and TOWN[1] <= y <= TOWN[3]: errs.append('inside the town')
            for sx, sy, sr, n, fn in SPAWN:
                if abs(x - sx) <= sr and abs(y - sy) <= sr: errs.append('inside spawner %s at %d,%d range %d (%s)' % (n, sx, sy, sr, fn))
    elif mode == 'indoor':
        s = F.top_surface(x, y, z + 2)
        if s is None or abs(s - z) > 2: errs.append('floor %s, row z %s' % (s, z))
        if F.blocked(x, y, z): errs.append('blocked by ' + F.blocked(x, y, z))
    elif mode == 'wall':
        s = F.top_surface(x, y, z + 2)
        if s is None or abs(s - z) > 2: errs.append('floor %s, row z %s' % (s, z))
        if not F.wall_at(x, y - 1, z): errs.append('no wall at the north neighbour %d,%d z%d' % (x, y - 1, z))
        if not r['art'].startswith('ptg-'): errs.append('wall mode for an item that is not wall art')
        for dx in (-1, 0, 1):
            for s, sz in F.statics(x + dx, y) + F.statics(x + dx, y - 1):
                if any(w in B.iname(s).lower() for w in WALLART) and z - 2 <= sz <= z + 30:
                    errs.append('wall art already beside it: 0x%04X %s at %d,%d' % (s, B.iname(s), x + dx, y))
    elif mode == 'posttop':
        if not any(B.iname(s) == 'pier' and sz + B.iheight(s) == z for s, sz in F.statics(x, y)): errs.append('no pier post with its top at z%d' % z)
    elif mode == 'beam':
        s = F.top_surface(x, y, z + 2)
        if s != z: errs.append('floor %s, row z %s' % (s, z))
        if not any(B.iflags(s) & B.SURF and 10 <= sz - z <= 20 for s, sz in F.statics(x, y)): errs.append('no deck 10-20 above')
    else:
        errs.append('unknown mode ' + mode)
    if mode not in ('posttop', 'beam'):
        st = WALK.stand.get((x, y))
        if st is None or abs(st - z) > 2: errs.append('soswalk: %s (stand z %s)' % (WALK.why.get((x, y)), st))
        elif (x, y) not in REACH: errs.append('not reachable on foot from the start')
    return errs


# Our art's tiledata records (the client copy's tiledata has none for them): records.json, the package's source of
# the 19 records the server applies (ClusterFCommunityArtRecords); an ID without a record is an animation frame.
REC = {r['id']: r for r in json.load(open('D:/UO/golems/Iron/ShatteredLegacy/player-package/vendor/shattered-legacy-art/records.json'))['tiledata']}


def in_the_way(rows):
    """Every impassable piece at once: the tiles reachable from the start that no longer are."""
    imp = [(r['x'], r['y'], r['z'], r['itemId']) for r in rows if int(REC.get(r['itemId'], {}).get('flags', '0'), 16) & B.IMP]
    items = soswalk.files()['items']
    for x, y, z, i in imp:   # soswalk reads the client copy's tiledata: give it our records for the walk
        items[i] = dict(items[i], flags=int(REC[i]['flags'], 16), height=REC[i]['height'], name=REC[i]['name'])
    w2 = soswalk.Walk(WALK.rect, extra=imp)
    after = set(w2.flood(X.START))
    own = {(x, y) for x, y, z, i in imp}
    lost = sorted(p for p in REACH - after if p not in own)
    return len(imp), lost


def main():
    rows = json.load(open(os.path.join(HERE, 'placement.json')))
    seen_keys, seen_tiles = set(), {}
    bad = 0
    out = ['| key | area | x,y,z | item | mode | why | check |', '|---|---|---|---|---|---|---|']
    for r in rows:
        errs = check(r, seen_keys, seen_tiles)
        bad += bool(errs)
        out.append('| %s | %s | %d,%d,%d | 0x%04X %s | %s | %s | %s |' % (r['key'], r['area'], r['x'], r['y'], r['z'], r['itemId'], r['name'], r['mode'], r['why'], 'ok' if not errs else 'FAIL: ' + ' / '.join(errs)))
    out.append('')
    n, lost = in_the_way(rows)
    out.append('In the way: %d impassable pieces put down at once; %s' % (n, 'every tile reachable from the start before is still reachable' if not lost else 'FAIL: cut off %d tiles: %s' % (len(lost), lost[:40])))
    bad += bool(lost)
    out.append('%d rows, %d failing. Protected tiles %d (the way in: %d tiles). Camp rules used %d spawners near Haven (every pinned folder); left out as town-wide (range >= %d): %s' % (
        len(rows), bad, len(PR.P), len(PR.PATH), len(SPAWN), TOWNWIDE, '; '.join('%s at %d,%d range %d (%s)' % (n, x, y, r, f) for x, y, r, n, f in SKIPPED)))
    camp = [r for r in rows if r['mode'] == 'camp']
    for x, y, sr, n, f in SKIPPED:
        inside = [r['key'] for r in camp if abs(r['x'] - x) <= sr and abs(r['y'] - y) <= sr]
        out.append('  %s at %d,%d range %d (%s): %s' % (n, x, y, sr, f, ('the camp is inside its range: ' + ', '.join(inside)) if inside else 'the camp is outside it'))
    text = '\n'.join(out)
    print(text)
    open(os.path.join(HERE, 'art-validate.out.txt'), 'w', encoding='ascii', newline='\n').write(text + '\n')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
