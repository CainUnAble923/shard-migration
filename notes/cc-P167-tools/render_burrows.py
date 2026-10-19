"""cc-P167 / cc-P180 / cc-P181: renders the scratch Rootdeep Burrows for Chase: one top-down overview (radar colours,
4 px per tile), an isometric render of each zone, the wall test rooms beside their OSI comparisons (walls-check.png),
the Stacks before and after beside OSI's Lycaeum (stacks-check.png), six corners before and after (corners-check.png),
the doorway frames (frames-check.png), the cave-foot test (cave-foot-check.png), the OSI rooms studied
(osi-reference.png), and the index page with round 2 beside round 3. Round 1 is kept in round1/, round 2 in round2/.
Isometric pictures come from scripts/mapbuild/isorender.py (the client's tile layout, sloped land drawn).

    python -P render_burrows.py <scratch folder> [<round 2 scratch folder>] [--page-only]

The second folder (default D:/UO/cc-p167-work/scratch-round2) holds round 2's map files for the "before" crops.
"""
import html, json, os, shutil, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
import build_burrows  # noqa: E402
from mapbuild import isorender, survey  # noqa: E402
from mapbuild.isorender import Scene, render, save, tile_px  # noqa: E402

OUT = r'D:\UO\shard-migration\notes\art\rootdeep-build'
ROUND1 = os.path.join(OUT, 'round1')
ROUND2 = os.path.join(OUT, 'round2')
CLIENT = isorender.CLIENT
E = html.escape

# name, x, y, w, h (tiles), what the picture shows
ZONES = [
    ('landing', 5174, 1128, 36, 39, 'The Landing (safe), the arrival, the ankh wall, the Vault doorway at x 5179 with its marble arch, and the tunnel south to the Warren'),
    ('vault', 5138, 1128, 45, 37, 'The Vault (tutorial only): Counting Room, the Stacks with its two bookcase rows, Deposit Hall, the Strongroom with its two walled pillars, the three arched gaps, the crawlway in the south wall at x 5160'),
    ('warren-west', 5140, 1158, 51, 43, 'The Warren, west: Crawl Den (the crawlway lands at 5160,1162) and the Great Burrow west half'),
    ('warren-east', 5182, 1158, 63, 41, 'The Warren, east: Tunnel Foot (the landing tunnel lands here), the Great Burrow east half, and the Brood Pit through its mouth at x 5209-5211'),
    ('tangle', 5138, 1194, 59, 43, 'The Tangle (tier 2): the root cavern with its five rock-and-log root masses, the Thicket behind its framed gap at x 5157, the passage east to the Dawnseam'),
    ('dawnseam', 5190, 1194, 57, 43, 'The Dawnseam (tier 2): the crystal seam with its five crystal clusters, the Seam Heart behind its framed gap at x 5227'),
    ('gloom-west', 5146, 1226, 56, 39, 'The Gloom, west half (tier 3): the descent from the Tangle, the ring tunnels, two web masses, the lair mouth at x 5183 with arch (a) and the webs'),
    ('gloom-east', 5190, 1226, 51, 39, 'The Gloom, east half: the descent from the Dawnseam, the Queen\'s lair with its two web pillars, the east and south runs'),
]
OVERVIEW = (5120, 1112, 144, 168)
OSI_ROOMS = {
    'dungeon': [('Deceit, Trammel 5184-5191 x 535-546 (map)', 'map', (5182, 533, 5194, 548)),
                ('Deceit, Trammel 5188-5200 x 556-570 (map)', 'map', (5186, 554, 5202, 572))],
    'marble': [('Nujel\'m, Trammel 3672-3696 x 1231-1247 (map; roofed)', 'map', (3670, 1229, 3698, 1249)),
               ('large marble house, multi 0x96 (roof left off)', 'multi', (0x96, 24))],
    'stone': [('Terathan Keep, Trammel 5467-5479 x 3128-3140 (map; two storeys)', 'map', (5465, 3126, 5481, 3142)),
              ('tower house, multi 0x7A (roof left off)', 'multi', (0x7A, 26))],
}
# the six corners for corners-check.png: kind, title, rect
CORNERS = [
    ('item wall', 'Vault: Strongroom SE corner, 5170-5181 x 1150-1161 (marble; candelabra on the strip, column at the corner, torch)', (5170, 1150, 5181, 1161)),
    ('item wall', 'Gloom lair: SE corner, 5216-5228 x 1246-1258 (stone; webs high, skull and rubble on the strip, pillar)', (5216, 1246, 5228, 1258)),
    ('cave', 'Warren: Crawl Den NW corner, 5143-5156 x 1159-1170 (stalagmite cluster on the ring)', (5143, 1159, 5156, 1170)),
    ('cave', 'Tangle: NW corner and the Thicket wall, 5140-5152 x 1196-1208 (roots and stones on the ring)', (5140, 1196, 5152, 1208)),
    ('doorway', 'Vault doorway, 5175-5184 x 1133-1142 (marble piers 0x0115 and the half arch 0x0116)', (5175, 1133, 5184, 1142)),
    ('doorway', 'Thicket gap, 5151-5163 x 1217-1229 (stalagmites on the rock either side)', (5151, 1217, 5163, 1229)),
]


def radar_overview(folder, x, y, w, h):
    """Top-down, one radar colour per tile (the topmost static's, else the land's), 4 px a tile."""
    rc = np.frombuffer(open(os.path.join(CLIENT, 'radarcol.mul'), 'rb').read(), dtype='<u2')
    sc = Scene.from_map(folder, 1, x, y, x + w - 1, y + h - 1, pad=0)
    top = {}
    for (sx, sy, z, tid) in sc.statics:
        if (sx, sy) not in top or z >= top[(sx, sy)][0]:
            top[(sx, sy)] = (z, tid)
    im = Image.new('RGB', (w, h))
    px = im.load()
    for (tx, ty), (tid, z) in sc.land.items():
        if not (x <= tx < x + w and y <= ty < y + h):
            continue
        i = 0x4000 + top[(tx, ty)][1] if (tx, ty) in top else tid
        c = int(rc[i]) if i < len(rc) else 0
        px[tx - x, ty - y] = isorender.rgb555(c)
    return im.resize((w * 4, h * 4), Image.NEAREST)


def crop_tiles(im, x1, y1, x2, y2, up=110, pad=30):
    lx, _ = tile_px(im, x1, y2)
    rx, _ = tile_px(im, x2, y1)
    _, ty = tile_px(im, x1, y1)
    _, by = tile_px(im, x2, y2)
    box = (max(0, lx - 22 - pad), max(0, ty - up), min(im.width, rx + 22 + pad), min(im.height, by + 44 + pad))
    return im.crop(box)


def label(im, text):
    out = Image.new('RGB', (im.width, im.height + 18), (24, 24, 28))
    out.paste(im.convert('RGB'), (0, 18))
    ImageDraw.Draw(out).text((4, 3), text, fill=(255, 230, 120))
    return out


def fit(im, w, h):
    s = min(w / im.width, h / im.height, 1.0)
    if s < 1.0:
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    return im


def panel_grid(rows, cell=(430, 400), gap=10):
    ncol = max(len(r) for r in rows)
    W = ncol * (cell[0] + gap) + gap
    H = len(rows) * (cell[1] + 18 + gap) + gap
    out = Image.new('RGB', (W, H), (40, 40, 44))
    for r, row in enumerate(rows):
        for c, (title, im) in enumerate(row):
            p = label(fit(im, cell[0], cell[1]), title)
            out.paste(p, (gap + c * (cell[0] + gap), gap + r * (cell[1] + 18 + gap)))
    return out


def scene_render(scenes, key, art):
    land, statics = scenes[key]
    xs = [c[0] for c in land]
    ys = [c[1] for c in land]
    return render(Scene(land, statics), min(xs), min(ys), max(xs), max(ys), art)


def map_render(folder, rect, art, deco=False, zmax=None):
    x1, y1, x2, y2 = rect
    sc = Scene.from_map(folder, 1, x1, y1, x2, y2)
    if zmax is not None:
        sc.statics = [s for s in sc.statics if s[2] <= zmax]
    if deco:
        for (x, y, z, tid, typ, src) in survey.decoration(rect=(x1, y1, x2, y2)):
            if tid < 0x4000 and (zmax is None or z <= zmax):
                sc.statics.append((x, y, z, tid))
    return render(sc, x1, y1, x2, y2, art)


def walls_check(scenes, art, scratch):
    rows = []
    for name in ('dungeon', 'marble', 'stone'):
        row = []
        for key in ('%s 5x5' % name, '%s L' % name):
            row.append(('test room: %s (our builder)' % key, scene_render(scenes, key, art)))
        for title, kind, spec in OSI_ROOMS[name]:
            if kind == 'map':
                im = map_render(CLIENT, spec, art)
            else:
                sc = Scene.from_multi(spec[0], spec[1])
                xs = [c[0] for c in sc.land]
                ys = [c[1] for c in sc.land]
                im = render(sc, min(xs), min(ys), max(xs) - 1, max(ys) - 1, art)
            row.append(('OSI: ' + title, im))
        rows.append(row)
    built = [('built: Landing NW corner, 5178-5196 x 1130-1140 (dungeon set)', (5178, 1130, 5196, 1140)),
             ('built: Vault Counting Room, 5168-5181 x 1130-1144 (marble set)', (5168, 1130, 5181, 1144)),
             ('built: Gloom lair NW corner, 5180-5196 x 1235-1246 (stone set)', (5180, 1235, 5196, 1246))]
    rows.append([(t, map_render(scratch, r, art)) for t, r in built])
    return panel_grid(rows)


def mouth_check(scenes, art, scratch):
    row = [('(a) as approved: mouth 3 tiles open; 0x01D8 on the first open tile, 0x01D9 on the wall tile after the gap', scene_render(scenes, 'stone mouth 3 open', art)),
           ('(b) not taken: OSI\'s 2-tile doorway, which would close the third mouth tile', scene_render(scenes, 'stone mouth 2 open', art)),
           ('built: the lair mouth at 5183,1246-1248 with (a) and the webs', map_render(scratch, (5177, 1240, 5190, 1254), art))]
    return panel_grid([row], cell=(520, 420))


def stacks_check(art, scratch, before):
    r = (5154, 1131, 5170, 1143)
    row = [('round 2: mixed facings (0x0A99 faces east), rows wander', map_render(before, r, art)),
           ('round 3: south-facing 0x0A97/0x0A98/0x0A9B only, candelabra ends', map_render(scratch, r, art)),
           ('OSI: the Lycaeum, Moonglow 4284-4296 x 959-981 (map + decoration items)', map_render(CLIENT, (4284, 959, 4296, 981), art, deco=True, zmax=19))]
    return panel_grid([row], cell=(560, 520))


def corners_check(art, scratch, before):
    rows = []
    for kind, title, rect in CORNERS:
        rows.append([('%s, round 2: %s' % (kind, title), map_render(before, rect, art)),
                     ('%s, round 3' % kind, map_render(scratch, rect, art))])
    return panel_grid(rows, cell=(560, 440))


def frames_check(scenes, art, scratch):
    rows = [[('test room: marble gap in a north-south wall (0x0115 piers, 0x0116 half arch)', scene_render(scenes, 'marble gap N-S wall', art)),
             ('test room: marble gap in an east-west wall (0x0113 piers, 0x0114 half arch)', scene_render(scenes, 'marble gap E-W wall', art)),
             ('OSI: Nujel\'m 3734-3742 x 1319-1327, the 0x0113 / 0x0114 doorway (roof left off)', map_render(CLIENT, (3734, 1319, 3742, 1327), art, zmax=19))],
            [('built: Deposit Hall to Strongroom gap, 5142-5152 x 1139-1147 (3 tiles)', map_render(scratch, (5142, 1139, 5152, 1147), art)),
             ('built: Counting Room to Stacks gap, 5165-5173 x 1136-1145', map_render(scratch, (5165, 1136, 5173, 1145), art)),
             ('built: the crawlway, 5155-5165 x 1156-1166 (rocks in the slot and on the rock either side)', map_render(scratch, (5155, 1156, 5165, 1166), art))],
            [('built: Seam Heart gap, 5222-5233 x 1217-1229 (crystals either side)', map_render(scratch, (5222, 1217, 5233, 1229), art)),
             ('built: Brood Pit mouth, 5205-5216 x 1176-1187 (a passage, not an opening: no frame)', map_render(scratch, (5205, 1176, 5216, 1187), art)),
             ('built: lair mouth (a), 5178-5190 x 1242-1252', map_render(scratch, (5178, 1242, 5190, 1252), art))]]
    return panel_grid(rows, cell=(480, 400))


def cave_foot_check(scenes, art):
    row = [('rock foot (kept): ring rock at 0, rock +12, void +20', scene_render(scenes, 'cave ring: rock foot (round 2)', art)),
           ('edge-tile foot (tried, rejected): Khaldun\'s cave edge tile at the ring; on a one-tile sloped ring the wedge stretches into teeth', scene_render(scenes, 'cave ring: edge-tile foot (round 3)', art)),
           ('OSI: Khaldun 5438-5470 x 1296-1322, rock mounds with the flat edge-tile foot', map_render(CLIENT, (5438, 1296, 5470, 1322), art))]
    return panel_grid([row], cell=(520, 440))


def osi_reference(art):
    rows = [[('Deceit room with its decoration items, 5182-5214 x 533-560 (torches on the west wall, webs and bones in corners)', map_render(CLIENT, (5182, 533, 5214, 560), art, deco=True)),
             ('Terathan Keep NW room, 5422-5446 x 3110-3122 at Z -60 (webs, a cocoon, torches)', map_render(CLIENT, (5422, 3110, 5446, 3122), art, deco=True, zmax=-40))],
            [('Khaldun 5438-5470 x 1296-1322 (stone set rooms, rock mounds, rubble)', map_render(CLIENT, (5438, 1296, 5470, 1322), art)),
             ('Covetous cave 5650-5690 x 1936-1962 (rock rings with gradual Z)', map_render(CLIENT, (5650, 1936, 5690, 1962), art))]]
    return panel_grid(rows, cell=(560, 480))


def main():
    folder = sys.argv[1]
    if '--page-only' in sys.argv:
        # rewrite index.html from the pictures already on disk
        made = [(name, x, y, w, h, what, os.path.getsize(os.path.join(OUT, '%s.png' % name))) for name, x, y, w, h, what in ZONES]
        page(made)
        return
    before = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else 'D:/UO/cc-p167-work/scratch-round2'
    rules = json.load(open(os.path.join(HERE, 'plan-sets.json'), encoding='utf-8'))
    art = isorender.Art()
    # keep round 2 beside the new pictures (round 1 is already in round1/)
    if not os.path.isdir(ROUND2):
        os.makedirs(ROUND2)
        for name in os.listdir(OUT):
            if name.endswith('.png') or name == 'index.html':
                shutil.move(os.path.join(OUT, name), os.path.join(ROUND2, name))
    made = []
    x, y, w, h = OVERVIEW
    radar_overview(folder, x, y, w, h).save(os.path.join(OUT, 'overview.png'), optimize=True)
    zone_images = {}
    for name, x, y, w, h, what in ZONES:
        sc = Scene.from_map(folder, 1, x, y, x + w - 1, y + h - 1)
        im = render(sc, x, y, x + w - 1, y + h - 1, art)
        zone_images[name] = im
        size = save(im, os.path.join(OUT, '%s.png' % name))
        made.append((name, x, y, w, h, what, size))
        print(name, im.size, size, flush=True)
    scenes = build_burrows.test_room_scenes(rules)
    scenes.update(build_burrows.cave_test_scenes(rules))
    checks = {
        'stacks-check.png': stacks_check(art, folder, before),
        'corners-check.png': corners_check(art, folder, before),
        'frames-check.png': frames_check(scenes, art, folder),
        'cave-foot-check.png': cave_foot_check(scenes, art),
        'walls-check.png': walls_check(scenes, art, folder),
        'lair-mouth-check.png': mouth_check(scenes, art, folder),
        'osi-reference.png': osi_reference(art),
    }
    for name, im in checks.items():
        print(name, save(im, os.path.join(OUT, name)), flush=True)
    page(made)
    for name in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, name)
        if os.path.isfile(p):
            print('%8d  %s' % (os.path.getsize(p), name))


def page(made):
    o = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">',
         '<title>Rootdeep Burrows Build</title><style>',
         ':root { --bg:#f6f4ef; --fg:#1f1d1a; --muted:#6b6560; --card:#ffffff; --line:#ddd6cc; --accent:#8a5a1c; }',
         '@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#16151a; --fg:#ece8e1; --muted:#a39d95; --card:#211f26; --line:#3a3640; --accent:#e0a85a; } }',
         ':root[data-theme="dark"] { --bg:#16151a; --fg:#ece8e1; --muted:#a39d95; --card:#211f26; --line:#3a3640; --accent:#e0a85a; }',
         'body { background:var(--bg); color:var(--fg); font:15px/1.5 system-ui, sans-serif; margin:0 auto; max-width:1180px; padding:16px; }',
         'h1 { font-size:24px; margin:8px 0 4px; } h2 { font-size:19px; margin:28px 0 8px; border-bottom:1px solid var(--line); } h3 { font-size:16px; margin:18px 0 4px; }',
         '.muted { color:var(--muted); } .ask { background:var(--card); border:2px solid var(--accent); border-radius:8px; padding:12px 16px; }',
         'img { max-width:100%; height:auto; border:1px solid var(--line); background:#000; } table { border-collapse:collapse; font-size:13px; width:100%; }',
         'td, th { border-bottom:1px solid var(--line); padding:4px 8px; text-align:left; vertical-align:top; } .pair td { width:50%; }',
         '</style></head><body>',
         '<h1>Rootdeep Burrows: the build, rendered from the scratch map (round 3)</h1>',
         '<p class="muted">cc-P181, 2026-10-19. P141\'s approved layout built into a scratch copy of Trammel (outside both repos); nothing has touched the real map files. '
         'Drawn by scripts/mapbuild/isorender.py from the real tiles with the client\'s layout (no hues, no lighting). '
         'Round 1 (2026-10-18) is kept in <a href="round1/index.html">round1/</a>, round 2 (2026-10-19 00:23) in <a href="round2/index.html">round2/</a>.</p>',
         '<div class="ask"><b>Approve these renders, or say what to change.</b><br>'
         'Your answer on round 2 was: A looks the best; line up all the bookcases; spend more time on the corners. What changed: '
         '(1) <b>The Stacks</b>: both rows use only the south-facing bookcases (round 2 mixed in 0x0A99, which faces east, so pieces stepped out of line), every piece at Z 0, flush end to end, '
         'a candelabra stand on each row end as OSI\'s Lycaeum library does. The rows\' footprint is P141\'s (11 tiles each, 3-tile aisle, 3 tiles from each wall; the two-tile stagger between them is the approved layout, the walkable floor is unchanged). '
         '(2) <b>Corners</b>: all 64 inner corners dressed by zone rules taken from Deceit, Khaldun, Covetous and Terathan Keep: webs, bones and stains on the corner tile, a wall torch on the north or west wall at some, rubble, skulls or a candelabra on the visible strip beside the corner, a column or stone pillar at the south-east corner of the big rooms; '
         'in the caves a stalagmite, root or crystal cluster on the rock round every inner corner and a piece on about half the rock tips the floor wraps round. '
         '(3) <b>Openings</b>: the four Vault gaps carry the marble pier-and-arch frame OSI uses at Nujel\'m and Magincia, the Thicket and Seam Heart gaps have stalagmites or crystals either side, the crawlway a rock either side, the lair mouth keeps (a). '
         '(4) The cave rings stay as built (your call on round 2); the edge-tile foot Khaldun uses was tried and dropped (picture below). '
         'The walkable floor, the 18 openings, the crawlway and all 1,614 wall tiles are exactly round 2\'s (the builder refuses to write otherwise).</div>',
         '<h2>Round 2 and round 3 side by side: the Vault</h2>',
         '<table class="pair"><tr><th>Round 2</th><th>Round 3</th></tr><tr><td><a href="round2/vault.png"><img src="round2/vault.png" alt="vault round 2"></a></td><td><a href="vault.png"><img src="vault.png" alt="vault round 3"></a></td></tr></table>',
         '<h2>Round 2 and round 3 side by side: the Gloom, west</h2>',
         '<table class="pair"><tr><th>Round 2</th><th>Round 3</th></tr><tr><td><a href="round2/gloom-west.png"><img src="round2/gloom-west.png" alt="gloom west round 2"></a></td><td><a href="gloom-west.png"><img src="gloom-west.png" alt="gloom west round 3"></a></td></tr></table>',
         '<h2>The Stacks: before, after, and OSI\'s library</h2>',
         '<p class="muted">OSI\'s Lycaeum (Moonglow, Trammel 4286-4293 x 962-999, from ModernUO\'s Britannia/moonglow.cfg decoration file) runs its east-west rows with 0x0A97, 0x0A98 and 0x0A9B only, its north-south column with 0x0A99, 0x0A9A and 0x0A9C only, and puts a candelabra stand (0x0B26) at a row\'s end. Round 2 mixed both facings in one row.</p>',
         '<p><a href="stacks-check.png"><img src="stacks-check.png" alt="stacks check"></a></p>',
         '<h2>Corners: six before and after (two item-wall, two cave, two doorways)</h2>',
         '<p><a href="corners-check.png"><img src="corners-check.png" alt="corners check"></a></p>',
         '<h2>Doorway frames</h2>',
         '<p class="muted">Marble: pier 0x0113/0x0115 on the wall tile each side of the gap and the half arch 0x0114/0x0116 on the first open tile (Nujel\'m 3737-3740 x 1323; Magincia column 3716, y 2064-2070). Stone (the lair mouth): 0x01D8 on the first open tile, 0x01D9 on the wall tile after (Terathan Keep column 5431). Cave gaps: a stalagmite or crystal on the rock either side. Passages between two floors (the Brood Pit mouth, the tunnels) have no wall line to frame and stay as OSI leaves a run\'s end: plain.</p>',
         '<p><a href="frames-check.png"><img src="frames-check.png" alt="frames check"></a></p>',
         '<h2>The cave foot: what was tried</h2>',
         '<p><a href="cave-foot-check.png"><img src="cave-foot-check.png" alt="cave foot check"></a></p>',
         '<h2>Walls check: our test rooms beside OSI rooms of the same set (unchanged from round 2)</h2>',
         '<p><a href="walls-check.png"><img src="walls-check.png" alt="walls check"></a></p>',
         '<h2>The lair mouth (a), as approved</h2>',
         '<p><a href="lair-mouth-check.png"><img src="lair-mouth-check.png" alt="lair mouth"></a></p>',
         '<h2>The OSI rooms the corner rules came from</h2>',
         '<p class="muted">Densities measured in notes/cc-P181-cont-rootdeep-round3.md (map statics plus the decoration items ModernUO adds): Deceit level 1 has something within one tile of 48 percent of its 386 inner corners (bones, small webs, rubble, garbage, torches), Covetous 66 percent of 247 (spiderwebs, debris, skulls), Khaldun 38 percent of 432 (rubble, braziers, skulls), Terathan Keep 59 percent of 98 (rubble, torches, webs, a cocoon). Our rule: every inner corner gets at least one thing, most get two or three.</p>',
         '<p><a href="osi-reference.png"><img src="osi-reference.png" alt="OSI reference rooms"></a></p>',
         '<h2>Overview (top-down, radar colours, 4 px per tile; x 5120-5263, y 1112-1279)</h2><p><a href="overview.png"><img src="overview.png" alt="top-down overview"></a></p>',
         '<h2>Zones (isometric, real tiles)</h2>']
    for name, x, y, w, h, what, size in made:
        o.append('<h3>%s</h3><p class="muted">x %d-%d, y %d-%d (%d x %d tiles). %s. %d KB</p><p><a href="%s.png"><img src="%s.png" alt="%s"></a></p>'
                 % (E(name), x, x + w - 1, y, y + h - 1, w, h, E(what), size // 1024, E(name), E(name), E(name)))
    o.append('<h2>What was placed</h2><p class="muted">Every static placed is in <code>notes/cc-P167-tools/statics-placed.csv</code>; land by id and Z in <code>land-summary.csv</code>; the rules (seeds, weights, clusters, corners, frames) in <code>plan-sets.json</code>; the builder is <code>build_burrows.py</code> on <code>scripts/mapbuild/</code>, the renders <code>render_burrows.py</code>; the corner table and checklist in <code>notes/cc-P181-cont-rootdeep-round3.md</code>.</p>')
    o.append('</body></html>')
    text = '\n'.join(o)
    text.encode('ascii')
    open(os.path.join(OUT, 'index.html'), 'w', encoding='ascii', newline='\n').write(text)


if __name__ == '__main__':
    main()
