"""cc-P680 (SoS swap S5): pinned's Trammel and Felucca decoration on the Siege of Sosaria land.

    python -P deco.py <overlay> [--write <code copy>]

Reads every cfg of pinned's Distribution/Data/Decoration/{Britannia,Trammel,Felucca} (Britannia's go on both facets,
Decorate.cs:35-37) and decides each entry (one item at x, y, z) against the land it was made for (EA's own Trammel for
Britannia and Trammel, EA's own Felucca for Felucca; maps.py) and the SoS land the server reads now:

  keep      its tile and the 8 round it are the same on both maps (P669's "unchanged", except that a re-textured
            floor at the same height and of the same kind counts as the same: maps.Map.same_tile);
  (doors)   a door the land change touched is kept where SoS still has a doorway on its tile (doors.py), else
            dropped: its building is its doorway;
  kept      the land changed, but the item's building is still there, at its tile: the structural statics round it
            (walls, floors, counters, posts: impassable, wall, window, surface, roof or door tiles in the 3 x 3, from 15
            below to 25 above it) are found again on SoS at the same offsets, at least 60 percent of them, with one
            height shift for all of at most 10 (written as a move when the shift is not 0);
  moved     not at its own tile, but within 8 tiles: the same match, at least 6 pieces and 80 percent, a height shift
            of at most 10. Where several fit, the shift its neighbours in the same file take wins, then the nearest;
            at least 3 other entries of the file within 24 tiles must take the same shift (a building moved whole);
  ground    it stood with no structure round it on EA's map: it stands on a floor or the land of SoS's tile within 5 Z
            of its own height (else of where the ground took it), with nothing impassable in its body and no floor slab
            less than 12 above it;
  dropped   everything else, with its reason: already a static on SoS's map (the author froze a decorated world into
            his statics: a Static entry whose art is on its tile is a duplicate; a working item over it is kept);
            water, void or cave-mouth land with nothing to stand on; SoS built on its tile; its building is gone (no
            match within 8).

Writes out-decisions.csv (one row per entry that is not "keep") and out-summary.txt. --write also writes the decided
cfgs to <code copy>/server/data/Decoration/<folder>/ (every file of the three folders, comments and order kept; a
dropped entry's line removed, a moved one's coordinates rewritten, a header left with no entries removed).
"""
import collections
import csv
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doors  # noqa: E402
import maps  # noqa: E402

PINNED = r'D:\UO\ModernUO-pinned\Distribution\Data\Decoration'
FOLDERS = ('Britannia', 'Trammel', 'Felucca')
STOCK_OF = {'Britannia': 'Trammel', 'Trammel': 'Trammel', 'Felucca': 'Felucca'}
ENTRY = re.compile(r'^(\s*)(-?\d+)(\s+)(-?\d+)(\s+)(-?\d+)(.*)$')
BAND = (-15, 25)
RATIO, MIN_MOVED, RADIUS, NEAR = 0.6, 6, 8, 24
FIT = 3             # a fit: on SoS's land or a floor within this of its own height (snapped onto it)
MOVE_RATIO = 0.8    # a move off its tile needs more: shared wall art matched other buildings (Ocllo, cc-P680 notes)
MAX_SHIFT = 10      # a building's height shift: more would match another storey's walls (Lord British's castle)
MIN_AGREE = 3       # a move needs this many other entries of its file taking the same shift (a building moved whole)


class Entry:
    __slots__ = ('folder', 'file', 'line', 'header', 'x', 'y', 'z', 'action', 'nx', 'ny', 'nz', 'why', 'cands',
                 'ctx')

    def __init__(self, folder, file, line, header, x, y, z):
        self.folder, self.file, self.line, self.header = folder, file, line, header
        self.x, self.y, self.z = x, y, z
        self.action, self.nx, self.ny, self.nz, self.why, self.cands, self.ctx = None, x, y, z, '', [], 0


def read_files():
    """{(folder, file): [lines]} and the entries, in order."""
    files, entries = {}, []
    for folder in FOLDERS:
        for path in sorted(glob.glob(os.path.join(PINNED, folder, '*.cfg'))):
            name = os.path.basename(path)
            lines = open(path, encoding='utf-8', newline='').read().splitlines(keepends=True)
            files[(folder, name)] = lines
            header = None
            for i, raw in enumerate(lines):
                s = raw.strip()
                if not s:
                    header = None
                    continue
                if s.startswith('#'):
                    continue
                m = ENTRY.match(raw.rstrip('\r\n'))
                if m and header is not None:
                    entries.append(Entry(folder, name, i, header, int(m.group(2)), int(m.group(4)), int(m.group(6))))
                else:
                    header = s
    return files, entries


def structure(M, x, y, z, extra=None, me=None):
    """The structural statics round (x, y) in the height band: [(dx, dy, sz - z, id)]. extra: the cfg's own statics on
    that facet ({(x, y): [(z, id)]}): some stock buildings are made of cfg walls, not map statics (New Haven's plaza).
    me: (z, id) of the entry itself, left out of its own surroundings."""
    out = []
    extra = extra or {}
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            own = list(extra.get((x + dx, y + dy), []))
            if me and (dx, dy) == (0, 0) and me in own:
                own.remove(me)
            for sz, tid in M.statics(x + dx, y + dy) + own:
                if M.flags(tid) & maps.STRUCT and BAND[0] <= sz - z <= BAND[1]:
                    out.append((dx, dy, sz - z, tid))
    return out


def match(S, ctx, x, y, z):
    """(matched, dz) of the stock structure ctx found on SoS round (x, y), with the commonest single height shift."""
    shifts = collections.Counter()
    want = collections.defaultdict(list)
    for dx, dy, dz, tid in ctx:
        want[(dx, dy, tid)].append(dz)
    have = {}
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for sz, tid in S.statics(x + dx, y + dy):
                if (dx, dy, tid) in want:
                    have.setdefault((dx, dy, tid), []).append(sz - z)
    if not have:
        return 0, 0
    for k, dzs in want.items():
        for a in dzs:
            for b in have.get(k, ()):
                if abs(b - a) <= MAX_SHIFT:
                    shifts[b - a] += 1
    if not shifts:
        return 0, 0
    dz, _ = shifts.most_common(1)[0]
    n = 0
    for k, dzs in want.items():
        got = list(have.get(k, ()))
        for a in dzs:
            if a + dz in got:
                got.remove(a + dz)
                n += 1
    return n, dz


def body_blocker(S, x, y, t):
    """What fills an item's space standing at t on SoS: something impassable from t to t+10, or a floor slab from 4 to
    11 above it (a rug or a step just above is no slab; a ceiling higher up is a storey). None when the space is free."""
    for sz, i in S.statics(x, y):
        f = S.flags(i)
        if f & maps.IMP and not f & maps.SURF and sz < t + 10 and sz + max(S.height(i), 1) > t:
            return '%s 0x%04X z%d' % (S.name(i) or 'static', i, sz)
        if f & maps.SURF and t + 3 < sz < t + 12:
            return '%s 0x%04X z%d (a floor over it)' % (S.name(i) or 'static', i, sz)
    return None


def tops_at(S, x, y, extra=None):
    """[(top, what)]: the land (unless water, void or cave-mouth land) and every floor's top on the tile, the map's
    statics and the cfg's own (extra: flowers stand on a cfg flowerbed). Impassable land counts: a crate tucked against
    a cave wall stands on rock nobody walks on (Destard)."""
    out = []
    if S.land_kind(x, y) in ('ground', 'rock'):
        out.append((S.avgz(x, y), 'the land'))
    for sz, i in S.statics(x, y):
        if S.flags(i) & maps.SURF:
            out.append((sz + S.height(i), '%s 0x%04X z%d' % (S.name(i) or 'floor', i, sz)))
    for sz, i in (extra or {}).get((x, y), []):
        if True:  # any cfg piece: the cfg stacks its own (flowers on a flowerbed in Moonglow's garden)
            out.append((sz + S.height(i), 'the cfg\'s %s 0x%04X z%d' % (S.name(i) or 'floor', i, sz)))
    return out


def fit(S, x, y, z, tol=FIT, extra=None):
    """(top, what) of the land or floor within tol of z, nearest first, with nothing in the item's space; else
    (None, why not)."""
    blocker = None
    for top, what in sorted(tops_at(S, x, y, extra), key=lambda tw: abs(tw[0] - z)):
        if abs(top - z) > tol:
            break
        blocker = body_blocker(S, x, y, top)
        if blocker is None:
            return top, what
    return None, blocker


NATURE = ('tree', 'trunk', 'leaves', 'bush', 'branch', 'rock', 'boulder', 'stalag', 'flowstone', 'fern', 'vine', 'cactus')


def man_made(S, i):
    """A wall, roof, window or door, or anything impassable that is not nature (a fence, a flowerbed, a statue)."""
    f = S.flags(i)
    if f & (maps.WALL | maps.ROOF | maps.WINDOW | maps.DOOR):
        return True
    name = (S.name(i) or '').lower()
    return bool(f & maps.IMP) and not any(n in name for n in NATURE)


def author_building(S, x, y, z):
    """True when SoS has something built round (x, y) at about z: a man-made piece in the 3 x 3 from 15 below to 25
    above (man_made), or a floor static under the tile within 3 Z."""
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for sz, i in S.statics(x + dx, y + dy):
                if man_made(S, i) and BAND[0] <= sz - z <= BAND[1]:
                    return True
    return any(S.flags(i) & maps.SURF and abs(sz + S.height(i) - z) <= FIT for sz, i in S.statics(x, y))


def item_id(header):
    """The art id a cfg header names (Decorate.cs: the number after the type, before any parameters)."""
    m = re.match(r'^\S+\s+(0x[0-9A-Fa-f]+|\d+)', header)
    return int(m.group(1), 0) if m else None


def decide(S, stocks, e, layout):
    K = stocks[STOCK_OF[e.folder]]
    x, y, z = e.x, e.y, e.z
    if all(S.same_tile(K, x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
        e.action = 'keep'
        return
    # A door's building is its doorway: kept where SoS still has one on its tile (door_pass checks it again against
    # the decoration as finally placed), dropped where not. The author kept his doorways where his buildings stand.
    if doors.is_door(e.header):
        f = 'Felucca' if e.folder == 'Felucca' else 'Trammel'
        ok, why = doors.in_doorway(S, x, y, z, *layout[f])
        if ok:
            e.action, e.why = 'kept', 'its doorway is still here on SoS'
        else:
            e.action, e.why = 'dropped', 'no doorway for it on SoS (%s): %s' % (f, why)
        return
    # The author froze a decorated world into his statics: the same art at the same tile is this entry already.
    iid = item_id(e.header)
    baked = [sz for sz, t in S.statics(x, y) if t == iid and abs(sz - z) <= 5] if iid is not None else []
    if baked:
        if e.header.split(' ')[0] in ('Static', 'LocalizedStatic'):
            e.action, e.why = 'dropped', 'already a static on SoS\'s map (the same art on its tile, z%d)' % baked[0]
        else:
            e.action, e.nz = 'kept', baked[0]
            e.why = 'kept as the working item over the same art on SoS\'s map (z%d)' % baked[0]
        return
    # Does it fit SoS where it is? Pinned's cfg was often made for an older map than EA's 7.0, and the author built
    # from a ServUO world with the same decoration: Lord British's castle library and Britain's inn rooms fit his
    # buildings floor for floor, where EA's own buildings differ. On SoS's land or a floor within 3 Z (snapped onto
    # it), with nothing in its space.
    # One guard: anything that stood in one of EA's own rooms (map walls or a roof round it) fits only among something
    # the author built (author_building), not on bare land where that building went. A feature the cfg builds itself
    # (Moonglow's garden: fences, flowerbeds, statues, a lamp post whose light the author baked in) carries its own.
    f = 'Felucca' if e.folder == 'Felucca' else 'Trammel'
    ctx = structure(K, x, y, z, layout[f][1], (z, iid) if iid is not None else None)
    e.ctx = len(ctx)
    kind = S.land_kind(x, y)
    own = {(x, y): [p for p in layout[f][1].get((x, y), []) if p != (z, iid)]}
    in_ea_building = any(K.flags(i) & (maps.WALL | maps.ROOF) for _, _, _, i in structure(K, x, y, z))  # a room
    top, what = (None, None) if in_ea_building and not author_building(S, x, y, z) else fit(S, x, y, z, extra=own)
    if top is not None:
        e.action, e.nz = 'kept', top
        e.why = 'it fits SoS as placed: on %s%s' % (what, ' (%+d Z)' % (top - z) if top != z else '')
        return
    if ctx:
        # Hung on a wall, or inside a building EA and SoS both have: its surroundings found again, maybe shifted.
        n, dz = match(S, ctx, x, y, z)
        if n and n >= RATIO * len(ctx):
            e.action, e.nz = 'kept', z + dz
            e.why = 'its building is still here (%d of %d pieces%s)' % (n, len(ctx), ', %+d Z' % dz if dz else '')
            return
        if len(ctx) >= MIN_MOVED:
            for ox in range(-RADIUS, RADIUS + 1):
                for oy in range(-RADIUS, RADIUS + 1):
                    if ox == 0 and oy == 0:
                        continue
                    n, dz = match(S, ctx, x + ox, y + oy, z)
                    if n >= MIN_MOVED and n >= MOVE_RATIO * len(ctx):
                        e.cands.append((ox, oy, dz, n))
        if e.cands:
            e.action = 'moved'  # the shift is chosen in pass 2
            return
        e.action = 'dropped'
        e.why = 'its building is gone: %d structural pieces round it, none of SoS within %d tiles fits, and %s' % (
            len(ctx), RADIUS, 'it fits nowhere on its tile (%s)' % what if what else 'no floor within %d Z' % FIT)
        return
    # Open ground on EA's map, and the ground moved: it follows the land's change of height if it fits there.
    solid = ('ground', 'rock')
    if kind in solid and K.land_kind(x, y) in solid:
        shift = S.avgz(x, y) - K.avgz(x, y)
        top2, what2 = fit(S, x, y, z + shift)
        if top2 is not None:
            e.action, e.nz = 'ground', top2
            e.why = 'open ground: it follows the ground (%+d Z), on %s' % (top2 - z, what2)
            return
        what = what or what2
    if kind in ('water', 'void', 'ignored') and not what:
        e.action = 'dropped'
        e.why = {'water': 'water', 'void': 'void', 'ignored': 'cave-mouth land with no floor'}[kind]
    elif what:
        e.action, e.why = 'dropped', 'SoS built on its tile: %s' % what
    else:
        e.action = 'dropped'
        e.why = 'nothing to stand on within %d Z on SoS (land and floors at %s)' % (
            FIT, ','.join(str(tp) for tp, _ in sorted(tops_at(S, x, y))) or 'none')


def choose_shifts(entries):
    """Pass 2: each moved entry takes the shift its neighbours in the same file share most, then the nearest."""
    by_file = collections.defaultdict(list)
    for e in entries:
        if e.action == 'moved':
            by_file[(e.folder, e.file)].append(e)
    for group in by_file.values():
        for e in group:
            votes = collections.Counter()
            for o in group:
                if abs(o.x - e.x) <= NEAR and abs(o.y - e.y) <= NEAR:
                    for ox, oy, dz, n in o.cands:
                        votes[(ox, oy)] += 1
            best = max(e.cands, key=lambda c: (votes[(c[0], c[1])], c[3], -(abs(c[0]) + abs(c[1]))))
            ox, oy, dz, n = best
            if votes[(ox, oy)] - 1 < MIN_AGREE:
                e.action = 'dropped'
                e.why = ('its building is gone: the nearest match (%d,%d, %d pieces) is a lone one; no other entry of '
                         'its file moves with it' % (ox, oy, n))
                continue
            e.nx, e.ny, e.nz = e.x + ox, e.y + oy, e.z + dz
            e.why = 'its building is %d,%d away (%d pieces%s; %d neighbours agree)' % (
                ox, oy, n, ', %+d Z' % dz if dz else '', votes[(ox, oy)] - 1)


def placed(entries):
    return [(e.folder, e.header, e.nx, e.ny, e.nz) for e in entries if e.action != 'dropped']


def door_pass(S, entries):
    """A door the land change touched (kept, moved or on the ground) must hang in a doorway on SoS (doors.py), the
    walls being SoS's statics and the cfg statics still placed; else it is dropped. Repeated until nothing changes,
    since dropping one leaf of a double door can leave its pair without a neighbour."""
    for _ in range(5):
        lay = {f: doors.facet_layout(placed(entries), f, None) for f in ('Trammel', 'Felucca')}
        changed = 0
        for e in entries:
            if e.action in ('keep', 'dropped') or not doors.is_door(e.header):
                continue
            facets = ('Trammel', 'Felucca') if e.folder == 'Britannia' else (e.folder,)
            for f in facets:
                d, extra = lay[f]
                ok, why = doors.in_doorway(S, e.nx, e.ny, e.nz, d, extra)
                if not ok:
                    e.action, e.why = 'dropped', 'no doorway for it on SoS (%s): %s' % (f, why)
                    changed += 1
                    break
        if not changed:
            return


def run(overlay):
    S = maps.sos(overlay)
    stocks = {'Trammel': maps.stock('Trammel'), 'Felucca': maps.stock('Felucca')}
    files, entries = read_files()
    layout = {f: doors.facet_layout([(e.folder, e.header, e.x, e.y, e.z) for e in entries], f, None)
              for f in ('Trammel', 'Felucca')}
    for i, e in enumerate(entries):
        decide(S, stocks, e, layout)
        if i % 5000 == 0:
            print('  graded', i, flush=True)
    choose_shifts(entries)
    door_pass(S, entries)
    return files, entries


def write_cfgs(files, entries, code):
    by_line = {(e.folder, e.file, e.line): e for e in entries}
    for (folder, name), lines in files.items():
        out, pending_header = [], None
        for i, raw in enumerate(lines):
            e = by_line.get((folder, name, i))
            if e is None:
                s = raw.strip()
                if s and not s.startswith('#') and not ENTRY.match(raw.rstrip('\r\n')):
                    if pending_header is not None and pending_header[1] == 0:
                        out.pop(pending_header[0])  # the previous header kept no entry
                    pending_header = [len(out), 0]
                elif not s:
                    if pending_header is not None and pending_header[1] == 0:
                        out.pop(pending_header[0])
                    pending_header = None
                out.append(raw)
                continue
            if e.action == 'dropped':
                continue
            if pending_header is not None:
                pending_header[1] += 1
            if (e.nx, e.ny, e.nz) != (e.x, e.y, e.z):
                m = ENTRY.match(raw.rstrip('\r\n'))
                end = raw[len(raw.rstrip('\r\n')):]
                raw = '%s%d%s%d%s%d%s%s' % (m.group(1), e.nx, m.group(3), e.ny, m.group(5), e.nz, m.group(7), end)
            out.append(raw)
        if pending_header is not None and pending_header[1] == 0:
            out.pop(pending_header[0])
        d = os.path.join(code, 'server', 'data', 'Decoration', folder)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, name), 'w', encoding='utf-8', newline='').write(''.join(out))


def main():
    overlay = sys.argv[1]
    files, entries = run(overlay)
    rows = [e for e in entries if e.action != 'keep']
    with open(os.path.join(HERE, 'out-decisions.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['folder', 'file', 'line', 'item', 'x', 'y', 'z', 'action', 'new_x', 'new_y', 'new_z', 'reason'])
        for e in rows:
            w.writerow([e.folder, e.file, e.line + 1, e.header, e.x, e.y, e.z, e.action, e.nx, e.ny, e.nz, e.why])
    summary = []
    for facet, folders in (('Trammel', ('Britannia', 'Trammel')), ('Felucca', ('Britannia', 'Felucca'))):
        c = collections.Counter(e.action for e in entries if e.folder in folders)
        summary.append('%s: %d entries: %s' % (facet, sum(c.values()), ', '.join('%s %d' % kv for kv in sorted(c.items()))))
    c = collections.Counter((e.folder, e.action) for e in entries)
    summary += ['  %s %s %d' % (k[0], k[1], v) for k, v in sorted(c.items())]
    why = collections.Counter(re.sub(r'\d+', 'N', e.why.split(':')[0]) for e in entries if e.action == 'dropped')
    summary += ['dropped, by reason:'] + ['  %6d %s' % (v, k) for k, v in why.most_common()]
    open(os.path.join(HERE, 'out-summary.txt'), 'w', encoding='utf-8').write('\n'.join(summary) + '\n')
    print('\n'.join(summary))
    if '--write' in sys.argv:
        write_cfgs(files, entries, sys.argv[sys.argv.index('--write') + 1])
        print('wrote the cfgs')


if __name__ == '__main__':
    main()
