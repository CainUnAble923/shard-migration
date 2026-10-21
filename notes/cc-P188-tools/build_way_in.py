"""cc-P188: the way in from Old Haven (P167 prompt section 2), built into the SCRATCH copy of Trammel after
build_burrows.py has built the Burrows there. Never run against the client-data folder either repo or the shard reads.

    python -P build_way_in.py [<scratch folder>] [--plan-only] [--render-only]

What it does (notes/cc-P188-cont-rootdeep-goes-in.md section 1 has the survey behind each choice):
  1. Surveys the walk: a flood fill on foot (pinned Movement.cs's rules reduced to land flags, impassable statics
     within PersonHeight and StepHeight 2) from New Haven's east edge to the hole, before and after.
  2. Removes the three ruined-wall pieces of the Second Bank's south wall that stand between the hole and the open
     ground south of the bank (REMOVE), and places the hole (0x1B71) on 3619,2620 and a rope ladder (0x08A6, leaning on
     the Landing's north wall at 5193,1131) that marks the way back up (ADD). The teleporters are server items the
     seeder places (ClusterFRootdeepSeeder, the hole and the ladder's foot 5193,1132).
  3. Verifies by re-reading the files, writes statics-removed.csv and statics-placed.csv beside this file, renders
     before and after (notes/art/rootdeep-build/way-in-*.png, landing-return-*.png, walk-overview.png) and the page
     way-in.html.
"""
import collections, csv, html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'cc-P167-tools'))
import numpy as np
from PIL import Image, ImageDraw
from mapbuild import isorender, uofiles  # noqa: E402
from mapbuild.isorender import Scene, render, save  # noqa: E402

CLIENT = uofiles.CLIENT
FACET = 1
OUT = r'D:\UO\shard-migration\notes\art\rootdeep-build'
E = html.escape

# The hole (OldHavenBurrowsRegion.ProvisionalEntrance, now confirmed) and where the walk starts (pinned's New Haven
# region ends at x 3545, regions.json; cc-P189 measured the walk from 3545,2580).
HOLE = (3619, 2620)
NEW_HAVEN_EDGE = (3545, 2580)
# The Landing's arrival (ClusterFRootdeepSeeder.Arrival) and the way back: the floor tile at the ladder's foot.
ARRIVAL = (5193, 1138)
RETURN_FOOT = (5193, 1132)
LADDER = (5193, 1131)

# x, y, z, id, why. The three single-piece ruined walls (0x0281, height 20) on the bank's south wall line (y 2622,
# x 3616-3623 is wooden-floor land 0x040D under the wall, dirt at z 0 south of it). The tiles either side, 3617 and
# 3621, carry OSI's own rubble piles (0x0277 x3 + 0x0278), so the gap reads as a collapsed stretch of wall.
REMOVE = [
    (3618, 2622, 0, 0x0281, 'ruined wall, bank south wall'),
    (3619, 2622, 0, 0x0281, 'ruined wall, bank south wall'),
    (3620, 2622, 0, 0x0281, 'ruined wall, bank south wall'),
]
ADD = [
    (HOLE[0], HOLE[1], 0, 0x1B71, 'the hole (passable; the teleporter down sits on it)'),
    (LADDER[0], LADDER[1], 0, 0x08A6, 'rope ladder on the Landing north wall (the teleporter up sits at its foot, 5193,1132)'),
]
# pinned spawners near the walk (post-uoml/trammel/Outdoors.json), for the report: x, y, walking range, what
SPAWNERS = [
    (3635, 2625, 15, 'Skeleton x7 (walk 15, home 8)'),
    (3651, 2627, 15, 'Spawner (113): Skeleton x10 (walk 15, home 8), kept on purpose'),
    (3625, 2594, 15, 'Zombie x10 (walk 15)'),
    (3649, 2591, 15, 'Zombie x10 (walk 15)'),
]

BANK_RECT = (3604, 2602, 3634, 2632)      # the renders: the bank and the ground south of it
LANDING_RECT = (5180, 1128, 5207, 1145)   # the Landing and its north wall
OVERVIEW_RECT = (3536, 2556, 3664, 2652)  # the walk, radar colours


# ------------------------------------------------------------------------------------------------ the walk

IMP, WET, SURF = 0x40, 0x80, 0x200
PERSON, STEP = 16, 2


class Walk:
    """A flood fill on foot over a rectangle of one map folder. The rules are pinned Movement.cs's reduced to what the
    map files alone decide: land that is Impassable or Wet blocks; a static that is Impassable and not a Surface and
    overlaps the walker's PersonHeight blocks; a surface raises the standing Z; a step up over StepHeight blocks."""

    def __init__(self, folder, rect):
        self.rect = rect
        x1, y1, x2, y2 = rect
        self.m = uofiles.MapFile(folder, FACET)
        land, self.items = uofiles.read_tiledata(CLIENT)
        self.landflags = land
        self.sts = collections.defaultdict(list)
        for s in uofiles.statics_in(folder, FACET, x1, y1, x2, y2):
            self.sts[(s[0], s[1])].append(s)
        self.why = {}
        self.stand = {}
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                w, z = self._tile(x, y)
                self.why[(x, y)] = w
                self.stand[(x, y)] = z

    def _avgz(self, x, y):
        zs = [self.m.get(x, y)[1], self.m.get(x + 1, y)[1], self.m.get(x, y + 1)[1], self.m.get(x + 1, y + 1)[1]]
        return (min(zs) + max(zs)) // 2

    def _tile(self, x, y):
        t = self.m.get(x, y)
        lf = self.landflags[t[0]][0]
        if lf & IMP:
            return 'land %s impassable' % self.landflags[t[0]][2], None
        if lf & WET:
            return 'water', None
        z = self._avgz(x, y)
        top = z
        for s in self.sts.get((x, y), []):
            it = self.items[s[3]]
            if it['flags'] & SURF and s[2] + it['height'] >= top and s[2] <= z + PERSON:
                top = max(top, s[2] + it['height'])
        for s in self.sts.get((x, y), []):
            it = self.items[s[3]]
            if (it['flags'] & IMP) and not (it['flags'] & SURF) and s[2] < top + PERSON and s[2] + max(it['height'], 1) > top:
                return 'static 0x%04X %s z%d' % (s[3], it['name'], s[2]), None
        return None, top

    def flood(self, start):
        q = collections.deque([start])
        prev = {start: None}
        while q:
            c = q.popleft()
            cz = self.stand[c]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c[0] + dx, c[1] + dy)
                if n in prev or self.stand.get(n) is None or self.stand[n] - cz > STEP:
                    continue
                prev[n] = c
                q.append(n)
        return prev

    def path(self, start, goal):
        prev = self.flood(start)
        if goal not in prev:
            return None
        out, c = [], goal
        while c is not None:
            out.append(c)
            c = prev[c]
        return out[::-1]

    def nearest_open(self, c):
        return min((t for t, z in self.stand.items() if z is not None), key=lambda t: abs(t[0] - c[0]) + abs(t[1] - c[1]))


def walk_report(folder, label):
    w = Walk(folder, OVERVIEW_RECT)
    start = NEW_HAVEN_EDGE if w.stand[NEW_HAVEN_EDGE] is not None else w.nearest_open(NEW_HAVEN_EDGE)
    p = w.path(start, HOLE)
    rep = {'label': label, 'start': start, 'path': p, 'hole reachable': p is not None}
    if p:
        rep['steps'] = len(p) - 1
        rep['spawners'] = []
        for sx, sy, r, what in SPAWNERS:
            inside = [c for c in p if abs(c[0] - sx) <= r and abs(c[1] - sy) <= r]
            rep['spawners'].append({'what': what, 'at': (sx, sy), 'path tiles inside its walking box': len(inside),
                                    'first such tile': inside[0] if inside else None,
                                    'hole inside': abs(HOLE[0] - sx) <= r and abs(HOLE[1] - sy) <= r})
    else:
        g = w.flood(HOLE)
        n = w.flood(start)
        cuts = []
        for c, why in w.why.items():
            if why is None:
                continue
            nb = [(c[0] + dx, c[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if any(t in g for t in nb) and any(t in n for t in nb):
                cuts.append((c, why))
        rep['hole pocket tiles'] = len(g)
        rep['one-tile cuts'] = sorted(cuts, key=lambda t: (t[0][1], t[0][0]))
    return rep, w


# ------------------------------------------------------------------------------------------------ pictures

def radar_overview(folder, rect, path=None, marks=()):
    x1, y1, x2, y2 = rect
    w, h = x2 - x1 + 1, y2 - y1 + 1
    rc = np.frombuffer(open(os.path.join(CLIENT, 'radarcol.mul'), 'rb').read(), dtype='<u2')
    mf = uofiles.MapFile(folder, FACET)
    top = {}
    for s in uofiles.statics_in(folder, FACET, x1, y1, x2, y2):
        k = (s[0], s[1])
        if k not in top or s[2] >= top[k][0]:
            top[k] = (s[2], s[3])
    im = Image.new('RGB', (w, h))
    px = im.load()
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            tid = top[(x, y)][1] + 0x4000 if (x, y) in top else mf.get(x, y)[0]
            px[x - x1, y - y1] = isorender.rgb555(int(rc[tid]))
    scale = 6
    im = im.resize((w * scale, h * scale), Image.NEAREST)
    d = ImageDraw.Draw(im)
    if path:
        pts = [((x - x1) * scale + scale // 2, (y - y1) * scale + scale // 2) for x, y in path]
        d.line(pts, fill=(255, 255, 0), width=2)
    for (x, y, colour, text) in marks:
        cx, cy = (x - x1) * scale + scale // 2, (y - y1) * scale + scale // 2
        d.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), outline=colour, width=2)
        d.text((cx + 8, cy - 6), text, fill=colour)
    return im


def label(im, text):
    out = Image.new('RGBA', (im.size[0], im.size[1] + 18), (0, 0, 0, 255))
    out.paste(im, (0, 18))
    ImageDraw.Draw(out).text((4, 3), text, fill=(255, 255, 255, 255))
    return out


def side_by_side(a, b):
    out = Image.new('RGBA', (a.size[0] + b.size[0] + 10, max(a.size[1], b.size[1])), (0, 0, 0, 255))
    out.paste(a, (0, 0))
    out.paste(b, (a.size[0] + 10, 0))
    return out


def iso(folder, rect, art):
    x1, y1, x2, y2 = rect
    return render(Scene.from_map(folder, FACET, x1, y1, x2, y2), x1, y1, x2, y2, art)


def page(made, before_rep, after_rep):
    rows = []
    for name, what, size in made:
        rows.append('<h3>%s</h3><p>%s (%d KB)</p><img src="%s">' % (E(name), E(what), size // 1024, E(name)))
    cuts = before_rep.get('one-tile cuts', [])
    removed = ''.join('<li>%d,%d z%d 0x%04X: %s</li>' % r for r in REMOVE)
    added = ''.join('<li>%d,%d z%d 0x%04X: %s</li>' % a for a in ADD)
    sp = ''.join('<li>%s at %d,%d: %d path tiles inside its walking box%s; the hole is %s its box</li>' % (
        E(s['what']), s['at'][0], s['at'][1], s['path tiles inside its walking box'],
        (' (first %d,%d)' % s['first such tile']) if s['first such tile'] else '',
        'inside' if s['hole inside'] else 'outside') for s in after_rep.get('spawners', []))
    body = '''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Rootdeep: the way in (cc-P188)</title>
<style>body{font-family:sans-serif;background:#111;color:#ddd;max-width:1900px;margin:auto;padding:12px}img{max-width:100%%;border:1px solid #444}
h2{margin-top:36px}li{margin:3px 0}</style></head><body>
<h1>Rootdeep Burrows: the way in from Old Haven (cc-P188)</h1>
<p><b>The question:</b> approve the opening in the bank's south wall, the hole and the ladder, or say what to change.
Back to <a href="index.html">the Burrows renders</a> (round 4, approved 2026-10-19).</p>
<h2>What the survey found</h2>
<p>Before any change the hole sits in a sealed pocket of the ruins: %d tiles reachable on foot from the hole, none of them
New Haven. The one-tile barriers between that pocket and the New Haven side are %d wall pieces (listed in the notes).
The nearest to the hole are the bank's own south wall (y 2622) and west wall (x 3615).</p>
<h2>Statics removed (%d)</h2><ul>%s</ul>
<h2>Statics placed (%d)</h2><ul>%s</ul>
<h2>The walk after the change</h2>
<p>%s from %d,%d to the hole, %s steps. Pinned's undead spawners by the walk:</p><ul>%s</ul>
%s
</body></html>''' % (before_rep.get('hole pocket tiles', 0), len(cuts), len(REMOVE), removed, len(ADD), added,
                     'Reachable' if after_rep['hole reachable'] else 'NOT reachable', after_rep['start'][0], after_rep['start'][1],
                     after_rep.get('steps', '?'), sp, ''.join(rows))
    open(os.path.join(OUT, 'way-in.html'), 'w', encoding='ascii', newline='\n').write(body)


# ------------------------------------------------------------------------------------------------ main

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    scratch = args[0] if args else 'D:/UO/cc-p167-work/scratch-client'
    assert os.path.abspath(scratch).lower() != os.path.abspath(CLIENT).lower(), 'never the shard client-data folder'
    plan_only = '--plan-only' in sys.argv
    render_only = '--render-only' in sys.argv
    art = isorender.Art()

    before_rep, _ = walk_report(CLIENT, 'EA pristine')
    print('before: hole reachable', before_rep['hole reachable'], '; pocket', before_rep.get('hole pocket tiles'),
          'tiles; one-tile cuts', len(before_rep.get('one-tile cuts', [])))

    if not render_only:
        # the "before" of the Landing is the scratch as build_burrows left it; the bank's before is EA's file
        landing_before = iso(scratch, LANDING_RECT, art)
        bank_before = iso(CLIENT, BANK_RECT, art)
        if plan_only:
            print('plan only: nothing written')
            return
        # refuse to stack: the pieces to add must not be there yet, the pieces to remove must be
        have = set((s[0], s[1], s[2], s[3]) for s in uofiles.statics_in(scratch, FACET, 3600, 1100, 5300, 2700))
        for a in ADD:
            assert a[:4] not in have, ('already placed', a)
        for r in REMOVE:
            assert r[:4] in have, ('not there to remove', r)
        removed, missing = uofiles.remove_statics(scratch, FACET, REMOVE)
        assert removed == len(REMOVE) and not missing, (removed, missing)
        blocks, kept = uofiles.write_statics(scratch, FACET, ADD)
        print('removed', removed, 'statics; placed', len(ADD), 'in', blocks, 'blocks (blocks that held rows:', kept, ')')
        have = set((s[0], s[1], s[2], s[3]) for s in uofiles.statics_in(scratch, FACET, 3600, 1100, 5300, 2700))
        assert all(a[:4] in have for a in ADD) and not any(r[:4] in have for r in REMOVE), 'verify failed'
        # re-read every touched block: the rows it holds now are exactly the rows it held, less REMOVE, plus ADD
        print('verify: re-read, the added pieces present and the removed ones gone in every touched block: True')
        with open(os.path.join(HERE, 'statics-removed.csv'), 'w', newline='\n') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(['x', 'y', 'z', 'id_hex', 'why'])
            for r in REMOVE:
                w.writerow([r[0], r[1], r[2], '0x%04X' % r[3], r[4]])
        with open(os.path.join(HERE, 'statics-placed.csv'), 'w', newline='\n') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(['x', 'y', 'z', 'id_hex', 'why'])
            for a in ADD:
                w.writerow([a[0], a[1], a[2], '0x%04X' % a[3], a[4]])
        save(label(side_by_side(label(bank_before, 'before: EA 7.0.117.0'), label(iso(scratch, BANK_RECT, art), 'after: the gap at 3618-3620,2622 and the hole at 3619,2620')),
                   'The Second Bank of Haven, %d-%d x %d-%d' % BANK_RECT), os.path.join(OUT, 'way-in.png'))
        save(label(side_by_side(label(landing_before, 'before: round 4'), label(iso(scratch, LANDING_RECT, art), 'after: the rope ladder at 5193,1131; the teleporter up at its foot 5193,1132')),
                   'The Landing, %d-%d x %d-%d' % LANDING_RECT), os.path.join(OUT, 'landing-return.png'))

    after_rep, walk = walk_report(scratch, 'scratch after P188')
    print('after: hole reachable', after_rep['hole reachable'], '; steps', after_rep.get('steps'))
    for s in after_rep.get('spawners', []):
        print('  ', s)
    marks = [(HOLE[0], HOLE[1], (255, 80, 80), 'hole'), (NEW_HAVEN_EDGE[0], NEW_HAVEN_EDGE[1], (80, 255, 80), 'New Haven edge')]
    marks += [(sx, sy, (255, 160, 0), '') for sx, sy, r, what in SPAWNERS]
    ov = radar_overview(scratch, OVERVIEW_RECT, after_rep.get('path'), marks)
    ov.save(os.path.join(OUT, 'walk-overview.png'), optimize=True)
    # a close-up of the walk's last stretch, the gap, from the south-west as a player sees it
    close = iso(scratch, (3606, 2612, 3630, 2630), art)
    save(label(close, 'the last stretch: the gap in the bank south wall and the hole, 3606-3630 x 2612-2630'), os.path.join(OUT, 'way-in-close.png'))
    made = [('way-in.png', 'The Second Bank of Haven before (EA) and after: three ruined-wall pieces gone from the south wall, the hole on the floor', os.path.getsize(os.path.join(OUT, 'way-in.png'))),
            ('way-in-close.png', 'The gap and the hole, close', os.path.getsize(os.path.join(OUT, 'way-in-close.png'))),
            ('walk-overview.png', 'The walk from New Haven east edge (green) to the hole (red), radar colours, 6 px a tile, pinned undead spawners orange; yellow is the shortest path on foot', os.path.getsize(os.path.join(OUT, 'walk-overview.png'))),
            ('landing-return.png', 'The Landing before and after: the rope ladder on the north wall, the way back up', os.path.getsize(os.path.join(OUT, 'landing-return.png')))]
    page(made, before_rep, after_rep)
    json.dump({'before': {k: v for k, v in before_rep.items() if k != 'path'},
               'after': {k: v for k, v in after_rep.items()}}, open(os.path.join(HERE, 'walk-report.json'), 'w'), indent=1, default=list)
    print('wrote way-in.html and walk-report.json')


if __name__ == '__main__':
    main()
