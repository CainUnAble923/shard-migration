# cc-P237 read only: checks every row of placement.json against the server's map files and the protected tiles, and
# prints the notes table (validate.out.txt). Exit 1 if any row fails. Rules:
#   every row  a unique key; no two rows on one tile at one z; the item is one of this set's IDs (art_src); the tile is
#              not protected (protected.py: doors and swings, every seeded coordinate, pinned spawners and their ring,
#              pinned decoration, teleporters, P188's walk)
#   ground     the ground's top surface (pinned GetTopSurfaceZ at the land's z) is the row's z, nothing impassable in
#              the way, not a road or plaza walkway
#   camp       as ground, and the camp rules: at least 3 tiles from every tile of P188's walk, and outside every pinned
#              creature spawner's walking box (location +/- walkingRange, or homeRange when larger). Spawners whose
#              range covers the whole town (reagents, 200; town animals, 100 and 80; wildlife, 50) are left out and named in the output.
#   edge       as ground, a walkway allowed (beside steps)
#   indoor     a floor surface within 2 of z, nothing impassable in the way
#   wall       north-wall art: a wall at the floor z on the tile's north neighbour, a floor within 2 of z, and no
#              OSI wall decoration on the tile or either neighbour along the wall (WALLART). Every
#              painting is drawn for a north wall (art_src), the face the client draws
#   posttop    a pier post whose top is z (the lantern sits on it)
#   beam       a floor surface at z with a deck (Surface) 10 to 20 above it on the same tile: under the boardwalk
import sys, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nhbase as B, protected as PR, art_src as S
F = B.Facet(1)
OURS = set()
for first, key, what, pack, files, how in S.GROUPS:
    OURS.add(first)

TOWNWIDE = 50
# names of OSI wall decoration: a painting may not hang on, or next to, a tile that already has one
WALLART = ('painting', 'portrait', 'picture', 'tapestry', 'banner', 'map', 'sign', 'mirror', 'trophy', 'mounted', 'shield', 'flag', 'deer head', 'bear head')
def creature_spawners():
    out, skipped = [], []
    # the folders the shard imports: shared and post-uoml (Core.SA; pinned AdminGump.cs:4031, as nhbase.spawns)
    for f in glob.glob(B.PINNED + '/Distribution/Data/Spawns/shared/trammel/*.json') + glob.glob(B.PINNED + '/Distribution/Data/Spawns/post-uoml/trammel/*.json'):
        for e in json.load(open(f, encoding='utf-8-sig')):
            loc = e.get('location')
            if not loc or e.get('map') != 'Trammel': continue
            r = max(e.get('walkingRange', 0) or 0, e.get('homeRange', 0) or 0)
            if not (3380 <= loc[0] <= 3700 and 2440 <= loc[1] <= 2700): continue
            (skipped if r >= TOWNWIDE else out).append((loc[0], loc[1], r, e.get('name'), os.path.basename(f)))
    return out, skipped
SPAWN, SKIPPED = creature_spawners()


def check(r, seen_keys, seen_tiles):
    x, y, z, item, mode = r['x'], r['y'], r['z'], r['itemId'], r['mode']
    errs = []
    if r['key'] in seen_keys: errs.append('duplicate key')
    if (x, y, z) in seen_tiles: errs.append('another row on this tile at this z: ' + seen_tiles[(x, y, z)])
    seen_keys.add(r['key']); seen_tiles[(x, y, z)] = r['key']
    if item not in OURS: errs.append('not one of this set\'s IDs')
    if (x, y) in PR.P: errs.append('protected: ' + '; '.join(sorted(set(PR.P[(x, y)]))))
    if mode in ('ground', 'camp', 'edge'):
        g = F.avgz(x, y)
        s = F.top_surface(x, y, g + 2)
        if s != z: errs.append('ground surface %s, row z %s' % (s, z))
        if F.blocked(x, y, z): errs.append('blocked by ' + F.blocked(x, y, z))
        if mode != 'edge' and B.walkway(F, x, y, z): errs.append('walkway ' + B.walkway(F, x, y, z))
        if mode == 'camp':
            d = min(max(abs(x - px), abs(y - py)) for px, py in PR.PATH)
            if d < 3: errs.append('%d tiles from P188\'s walk' % d)
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
    return errs


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
    out.append('%d rows, %d failing. Camp rules used %d creature spawners near Haven; left out as town-wide (range >= %d): %s' % (
        len(rows), bad, len(SPAWN), TOWNWIDE, '; '.join('%s at %d,%d range %d (%s)' % (n, x, y, r, f) for x, y, r, n, f in SKIPPED)))
    camp = [r for r in rows if r['mode'] == 'camp']
    for x, y, sr, n, f in SKIPPED:
        inside = [r['key'] for r in camp if abs(r['x'] - x) <= sr and abs(r['y'] - y) <= sr]
        out.append('  %s at %d,%d range %d (%s): %s' % (n, x, y, sr, f, ('the camp is inside its range: ' + ', '.join(inside)) if inside else 'the camp is outside it'))
    text = '\n'.join(out)
    print(text)
    open(os.path.join(HERE, 'validate.out.txt'), 'w', encoding='ascii', newline='\n').write(text + '\n')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
