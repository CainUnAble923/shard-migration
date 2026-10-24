"""cc-P413: the Rootdeep Burrows' way in becomes an ant-hill burrow: OSI's own 6 x 6 sinkhole set (0x30E7-0x310A, a dirt
crater round a dark hole, as OSI lays it at Trammel 5575-5580, 3015-3020) in the Second Bank of Old Haven, with a rim of
loose rocks and debris, in place of P188's single hole 0x1B71. Built into a SCRATCH copy of Trammel; never the
client-data folder either repo or the shard reads.

    python -P build_anthill.py <pristine folder> <work folder> [--ox 3614] [--oy 2616] [--plan-only]

  1. <work>/current = pristine + the shipped trammel.mapops (mapops.apply): today's map.
  2. <work>/edited = current, minus the hole 0x1B71 at 3619,2620, plus the sinkhole and the rim (ADD below).
  3. Verifies by re-reading, writes statics-placed.csv and statics-removed.csv beside this file, the walk report
     (walk-report.json: New Haven's east edge to every mouth tile, spawner boxes), renders into this folder, and the new
     map patch (mapops.diff pristine -> edited, then mapops.check) to <work>/trammel.mapops.

The renderer's tiledata, texmaps and radar colours come from the pristine folder (uofiles.CLIENT is pointed there before
any mapbuild import), never from a repo's client-data.
"""
import argparse, csv, json, os, random, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(NOTES), 'scripts'))

ap = argparse.ArgumentParser()
ap.add_argument('pristine')
ap.add_argument('work')
ap.add_argument('--ox', type=int, default=3615)
ap.add_argument('--oy', type=int, default=2616)
ap.add_argument('--plan-only', action='store_true')
ap.add_argument('--tag', default='')
ap.add_argument('--mapops', default=os.path.join(os.path.dirname(os.path.dirname(NOTES)), 'ShatteredLegacy',
                                                 'player-package', 'vendor', 'shattered-legacy-map', 'trammel.mapops'))
a = ap.parse_args()

from mapbuild import uofiles  # noqa: E402
uofiles.CLIENT = a.pristine
from mapbuild import isorender, mapops  # noqa: E402
sys.path.insert(0, os.path.join(NOTES, 'cc-P188-tools'))
import build_way_in as bwi  # noqa: E402
bwi.CLIENT = a.pristine
from PIL import Image, ImageDraw  # noqa: E402

FACET = 1
OLD_HOLE = (3619, 2620, 0, 0x1B71)
SINK_FIRST, SINK_LAST = 0x30E7, 0x310A


def sink_id(c, r):
    """OSI's layout of the set (Trammel 5575,3015 is c 0, r 0): the id falls by one per column east, six per row south."""
    return SINK_LAST - c - 6 * r


OX, OY = a.ox, a.oy
# The dark core of the set: columns 2-4, rows 1-4 (the pieces 34 to 100 percent dark; the rim pieces round them 0 to 48).
MOUTH = [(OX + c, OY + r) for r in range(1, 5) for c in range(2, 5)]
SET_TILES = [(OX + c, OY + r) for r in range(6) for c in range(6)]
BANK_FLOOR = (3616, 2610, 3625, 2621)   # the bank's wooden floor inside its walls (the survey in the notes)
RIM_PIECES = [0x1771, 0x1773, 0x1774, 0x1775, 0x1776, 0x1777, 0x1778, 0x1779, 0x177B, 0x177C, 0x0C2E, 0x0C2F, 0x0C30]
SEED = 413
SPAWNER_BOXES = [(sx - r, sy - r, sx + r, sy + r, what) for sx, sy, r, what in bwi.SPAWNERS]
NEW_HAVEN_EDGE = bwi.NEW_HAVEN_EDGE
LADDER_LANDING = (3619, 2623)   # ClusterFRootdeepSeeder.BesideMound: outside the collapsed wall, facing the mound


def in_box(t):
    return [w for x1, y1, x2, y2, w in SPAWNER_BOXES if x1 <= t[0] <= x2 and y1 <= t[1] <= y2]


def plan():
    add = [(x, y, 0, sink_id(x - OX, y - OY), 'sinkhole (OSI set 0x30E7-0x310A), %s' % ('mouth' if (x, y) in MOUTH else 'rim'))
           for (x, y) in SET_TILES]
    rng = random.Random(SEED)
    fx1, fy1, fx2, fy2 = BANK_FLOOR
    rim = [t for t in SET_TILES if t not in MOUTH and fx1 <= t[0] <= fx2 and fy1 <= t[1] <= fy2]
    placed = {}
    for t in rim:
        if rng.random() < 0.65:
            nb = {placed.get((t[0] + dx, t[1] + dy)) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
            pick = rng.choice([p for p in RIM_PIECES if p not in nb])
            placed[t] = pick
            add.append((t[0], t[1], rng.choice((0, 0, 1)), pick, 'rim: loose rock or debris (passable)'))
    return add, [OLD_HOLE + ('P188 hole, replaced by the burrow',)]


def main():
    add, remove = plan()
    report = {'ox': OX, 'oy': OY, 'mouth': MOUTH, 'set': [SET_TILES[0], SET_TILES[-1]],
              'mouth tiles in a spawner box': {str(t): in_box(t) for t in MOUTH if in_box(t)},
              'set tiles in a spawner box': {str(t): in_box(t) for t in SET_TILES if in_box(t)},
              'ladder landing in a spawner box': in_box(LADDER_LANDING)}
    print(json.dumps(report, indent=1))
    if a.plan_only:
        return
    cur = os.path.join(a.work, 'current')
    ed = os.path.join(a.work, 'edited' + a.tag)
    if not os.path.exists(os.path.join(cur, 'statics1.mul')):
        mapops.apply(open(a.mapops).read(), a.pristine, cur, FACET)
    os.makedirs(ed, exist_ok=True)
    for f in mapops._files(FACET):
        shutil.copyfile(os.path.join(cur, f), os.path.join(ed, f))
    removed, missing = uofiles.remove_statics(ed, FACET, remove)
    assert removed == 1 and not missing, (removed, missing)
    uofiles.write_statics(ed, FACET, add)
    x1, y1, x2, y2 = 3612, 2606, 3626, 2627
    after = uofiles.statics_in(ed, FACET, x1, y1, x2, y2)
    before = uofiles.statics_in(cur, FACET, x1, y1, x2, y2)
    want = [s for s in before if (s[0], s[1], s[2], s[3]) != OLD_HOLE] + [(s[0], s[1], s[2], s[3]) for s in add]
    assert sorted(after) == sorted(want), 'verify: the re-read statics differ from the plan'
    print('verify: %d statics in the bank rect re-read as planned (%d before)' % (len(after), len(before)))

    # The walk, before and after: New Haven's east edge to the old hole / to every mouth tile.
    w = bwi.Walk(ed, bwi.OVERVIEW_RECT)
    start = NEW_HAVEN_EDGE if w.stand[NEW_HAVEN_EDGE] is not None else w.nearest_open(NEW_HAVEN_EDGE)
    prev = w.flood(start)
    walk = {'start': start, 'mouth': {}}
    for t in MOUTH:
        p = w.path(start, t)
        walk['mouth'][str(t)] = {'reachable': p is not None, 'steps': len(p) - 1 if p else None,
                                 'stand z': w.stand.get(t),
                                 'path tiles in a spawner box': sorted({x for c in (p or []) for x in in_box(c)})}
    best = min((v['steps'] for v in walk['mouth'].values() if v['steps'] is not None), default=None)
    walk['shortest steps to the mouth'] = best
    lp = w.path(LADDER_LANDING, start)
    walk['ladder landing'] = {'at': LADDER_LANDING, 'stand z': w.stand.get(LADDER_LANDING),
                              'walk back to New Haven steps': len(lp) - 1 if lp else None,
                              'is a mouth tile': LADDER_LANDING in MOUTH}
    wc = bwi.Walk(cur, bwi.OVERVIEW_RECT)
    pc = wc.path(start, (OLD_HOLE[0], OLD_HOLE[1]))
    walk['before: steps to the old hole'] = len(pc) - 1 if pc else None
    walk['reachable tiles after'] = len(prev)
    walk['reachable tiles before'] = len(wc.flood(start))
    shortest = min((w.path(start, t) for t in MOUTH), key=lambda p: len(p) if p else 10 ** 9)
    walk['shortest path'] = shortest
    report['walk'] = walk
    print(json.dumps({k: v for k, v in walk.items() if k != 'shortest path'}, indent=1))

    with open(os.path.join(HERE, 'walk-report%s.json' % a.tag), 'w') as f:
        json.dump(report, f, indent=1)
    with open(os.path.join(HERE, 'statics-placed%s.csv' % a.tag), 'w', newline='') as f:
        cw = csv.writer(f, lineterminator='\n')
        cw.writerow(['x', 'y', 'z', 'id', 'what'])
        for s in add:
            cw.writerow([s[0], s[1], s[2], '0x%04X' % s[3], s[4]])
    with open(os.path.join(HERE, 'statics-removed%s.csv' % a.tag), 'w', newline='') as f:
        cw = csv.writer(f, lineterminator='\n')
        cw.writerow(['x', 'y', 'z', 'id', 'what'])
        for s in remove:
            cw.writerow([s[0], s[1], s[2], '0x%04X' % s[3], s[4]])

    # Pictures: the bank before and after (iso), a close-up, and the walk in radar colours.
    art = isorender.Art(client=a.pristine)
    rect = (3606, 2604, 3630, 2630)
    b = bwi.label(bwi.iso(cur, rect, art), 'before: P188 hole 0x1B71 at 3619,2620')
    c = bwi.label(bwi.iso(ed, rect, art), 'after: the burrow, mouth x %d-%d, y %d-%d' % (MOUTH[0][0], MOUTH[-1][0], MOUTH[0][1], MOUTH[-1][1]))
    isorender.save(bwi.side_by_side(b, c), os.path.join(HERE, 'entrance-before-after%s.png' % a.tag))
    close = (3611, 2612, 3624, 2626)
    isorender.save(bwi.label(bwi.iso(ed, close, art), 'close-up: the burrow in the Second Bank'), os.path.join(HERE, 'entrance-close%s.png' % a.tag))
    marks = [(t[0], t[1], (255, 0, 255), '') for t in MOUTH]
    marks += [(LADDER_LANDING[0], LADDER_LANDING[1], (0, 255, 255), 'ladder up lands'), (start[0], start[1], (0, 255, 0), 'New Haven east edge')]
    marks += [(sx, sy, (255, 140, 0), 'spawner') for sx, sy, r, what in bwi.SPAWNERS]
    ov = bwi.radar_overview(ed, bwi.OVERVIEW_RECT, shortest, marks)
    d = ImageDraw.Draw(ov)
    s6 = 6
    for x1b, y1b, x2b, y2b, what in SPAWNER_BOXES:
        X1, Y1 = (x1b - bwi.OVERVIEW_RECT[0]) * s6, (y1b - bwi.OVERVIEW_RECT[1]) * s6
        X2, Y2 = (x2b - bwi.OVERVIEW_RECT[0] + 1) * s6, (y2b - bwi.OVERVIEW_RECT[1] + 1) * s6
        d.rectangle((X1, Y1, X2, Y2), outline=(255, 140, 0))
    ov.save(os.path.join(HERE, 'walk-overview%s.png' % a.tag))

    text = mapops.diff(a.pristine, ed, FACET)
    out = os.path.join(a.work, 'trammel%s.mapops' % a.tag)
    open(out, 'w', newline='\n').write(text)
    dr, mi, le, bad = mapops.check(text, a.pristine, ed, FACET)
    print('mapops: %d bytes, check drifted %d missing %d land identical %s blocks differing %d' % (len(text), len(dr), len(mi), le, len(bad) if isinstance(bad, (list, tuple, set, dict)) else bad))


main()
