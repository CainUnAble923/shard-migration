"""cc-P167 / cc-P180: renders the scratch Rootdeep Burrows for Chase: one top-down overview (radar colours, 4 px per
tile), an isometric render of each zone, the wall test rooms beside their OSI comparisons (walls-check.png), the lair
mouth both ways (lair-mouth-check.png), and the index page with round 1 beside round 2. Round 1's files are kept in
round1/. Isometric pictures come from isorender.py (the client's tile layout, sloped land drawn); round 1 used
vseUOAware's renderer, which drew statics half a tile high and flat land only.

    python -P render_burrows.py <scratch folder>
"""
import html, json, os, shutil, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import isorender, build_burrows  # noqa: E402
from isorender import Scene, render, save, tile_px  # noqa: E402

OUT = r'D:\UO\shard-migration\notes\art\rootdeep-build'
ROUND1 = os.path.join(OUT, 'round1')
RESEARCH = r'D:\UO\shard-migration\notes\art\wall-research'
CLIENT = isorender.CLIENT
E = html.escape

# name, x, y, w, h (tiles), what the picture shows
ZONES = [
    ('landing', 5174, 1128, 36, 39, 'The Landing (safe), the arrival, the ankh wall, the Vault doorway at x 5179, and the tunnel south to the Warren'),
    ('vault', 5138, 1128, 45, 37, 'The Vault (tutorial only): Counting Room, the Stacks with its bookcase rows (proposal), Deposit Hall, the Strongroom with its two walled pillars, the crawlway in the south wall at x 5160'),
    ('warren-west', 5140, 1158, 51, 43, 'The Warren, west: Crawl Den (the crawlway lands at 5160,1162) and the Great Burrow west half'),
    ('warren-east', 5182, 1158, 63, 41, 'The Warren, east: Tunnel Foot (the landing tunnel lands here), the Great Burrow east half, and the Brood Pit through its mouth at x 5209-5211'),
    ('tangle', 5138, 1194, 59, 43, 'The Tangle (tier 2): the root cavern with its five rock-and-log root masses, the Thicket behind its gap at x 5157, the passage east to the Dawnseam'),
    ('dawnseam', 5190, 1194, 57, 43, 'The Dawnseam (tier 2): the crystal seam with its five crystal clusters, the Seam Heart behind its gap at x 5227'),
    ('gloom-west', 5146, 1226, 56, 39, 'The Gloom, west half (tier 3): the descent from the Tangle, the ring tunnels, two web masses, the lair mouth at x 5183 with the proposed arch and webs'),
    ('gloom-east', 5190, 1226, 51, 39, 'The Gloom, east half: the descent from the Dawnseam, the Queen\'s lair with its two web pillars, the east and south runs'),
]
OVERVIEW = (5120, 1112, 144, 168)
# OSI comparison rooms for walls-check.png: set -> (label, source, rect or multi)
OSI_ROOMS = {
    'dungeon': [('Deceit, Trammel 5184-5191 x 535-546 (map)', 'map', (5182, 533, 5194, 548)),
                ('Deceit, Trammel 5188-5200 x 556-570 (map)', 'map', (5186, 554, 5202, 572))],
    'marble': [('Nujel\'m, Trammel 3672-3696 x 1231-1247 (map; roofed)', 'map', (3670, 1229, 3698, 1249)),
               ('large marble house, multi 0x96 (roof left off)', 'multi', (0x96, 24))],
    'stone': [('Terathan Keep, Trammel 5467-5479 x 3128-3140 (map; two storeys)', 'map', (5465, 3126, 5481, 3142)),
              ('tower house, multi 0x7A (roof left off)', 'multi', (0x7A, 26))],
}


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
    """Crop a render to the tiles x1..x2, y1..y2 (plus wall height above and a margin)."""
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
    """rows: list of lists of (title, image)."""
    ncol = max(len(r) for r in rows)
    W = ncol * (cell[0] + gap) + gap
    H = len(rows) * (cell[1] + 18 + gap) + gap
    out = Image.new('RGB', (W, H), (40, 40, 44))
    for r, row in enumerate(rows):
        for c, (title, im) in enumerate(row):
            p = label(fit(im, cell[0], cell[1]), title)
            out.paste(p, (gap + c * (cell[0] + gap), gap + r * (cell[1] + 18 + gap)))
    return out


def walls_check(rules, art, scratch):
    scenes = build_burrows.test_room_scenes(rules)
    rows = []
    for name in ('dungeon', 'marble', 'stone'):
        row = []
        for key in ('%s 5x5' % name, '%s L' % name):
            land, statics = scenes[key]
            xs = [c[0] for c in land]
            ys = [c[1] for c in land]
            im = render(Scene(land, statics), min(xs), min(ys), max(xs), max(ys), art)
            row.append(('test room: %s (our builder)' % key, im))
        for title, kind, spec in OSI_ROOMS[name]:
            if kind == 'map':
                x1, y1, x2, y2 = spec
                im = render(Scene.from_map(CLIENT, 1, x1, y1, x2, y2), x1, y1, x2, y2, art)
            else:
                sc = Scene.from_multi(spec[0], spec[1])
                xs = [c[0] for c in sc.land]
                ys = [c[1] for c in sc.land]
                im = render(sc, min(xs), min(ys), max(xs) - 1, max(ys) - 1, art)
            row.append(('OSI: ' + title, im))
        rows.append(row)
    # the built Burrows rooms in the same three sets, from the scratch map
    built = [('built: Landing NW corner, 5178-5196 x 1130-1140 (dungeon set)', (5178, 1130, 5196, 1140)),
             ('built: Vault Counting Room, 5168-5181 x 1130-1144 (marble set)', (5168, 1130, 5181, 1144)),
             ('built: Gloom lair NW corner, 5180-5196 x 1235-1246 (stone set)', (5180, 1235, 5196, 1246))]
    rows.append([(t, render(Scene.from_map(scratch, 1, *r), *r, art)) for t, r in built])
    return panel_grid(rows), scenes


def mouth_check(rules, art, scenes, scratch):
    row = []
    for key, what in (('stone mouth 3 open', '(a) proposed: mouth 3 tiles open as the spec says; 0x01D8 on the first open tile, 0x01D9 on the wall tile after the gap'),
                      ('stone mouth 2 open', '(b) OSI\'s 2-tile doorway: 0x01D8, open, 0x01D9; the third mouth tile would close')):
        land, statics = scenes[key]
        xs = [c[0] for c in land]
        ys = [c[1] for c in land]
        row.append((what, render(Scene(land, statics), min(xs), min(ys), max(xs), max(ys), art)))
    r = (5177, 1240, 5190, 1254)
    row.append(('built: the lair mouth at 5183,1246-1248 with (a) and the webs', render(Scene.from_map(scratch, 1, *r), *r, art)))
    return panel_grid([row], cell=(520, 420))


def main():
    folder = sys.argv[1]
    rules = json.load(open(os.path.join(HERE, 'plan-sets.json'), encoding='utf-8'))
    art = isorender.Art()
    # keep round 1 (vseUOAware renders, 2026-10-18) beside the new pictures
    if not os.path.isdir(ROUND1):
        os.makedirs(ROUND1)
        for name in os.listdir(OUT):
            if name.endswith('.png') or name == 'index.html':
                shutil.move(os.path.join(OUT, name), os.path.join(ROUND1, name))
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
    # the proposals, cropped from the zone renders
    crops = {
        'stacks': (zone_images['vault'], 5154, 1131, 5170, 1143, 'The Stacks as bookcases (0x0A97, 0x0A99, 0x0A9B, 0x0A9D mixed), x 5156-5168, y 1135 and 1139'),
        'doorway': (zone_images['landing'], 5175, 1133, 5184, 1142, 'The Vault doorway at 5179,1137-1138 with no door'),
        'cavering': (zone_images['warren-west'], 5143, 1159, 5160, 1172, 'A cave ring as it is: rock at floor level, +12, then the void at +20 (Crawl Den NW corner)'),
    }
    for key, (im, x1, y1, x2, y2, what) in crops.items():
        save(crop_tiles(im, x1, y1, x2, y2), os.path.join(OUT, 'proposal-%s.png' % key))
    wc, scenes = walls_check(rules, art, folder)
    save(wc, os.path.join(OUT, 'walls-check.png'))
    save(mouth_check(rules, art, scenes, folder), os.path.join(OUT, 'lair-mouth-check.png'))
    page(made, crops)
    for name in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, name)
        if os.path.isfile(p):
            print('%8d  %s' % (os.path.getsize(p), name))


def page(made, crops):
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
         '<h1>Rootdeep Burrows: the build, rendered from the scratch map (round 2)</h1>',
         '<p class="muted">cc-P180, 2026-10-19. P141\'s approved layout built into a scratch copy of Trammel (outside both repos); nothing has touched the real map files. '
         'Drawn by notes/cc-P167-tools/isorender.py from the real tiles with the client\'s layout (statics on the land diamond\'s bottom, sloped land drawn with its texture; no hues, no lighting). '
         'Round 1 (2026-10-18) is kept in <a href="round1/index.html">round1/</a>.</p>',
         '<div class="ask"><b>Approve these renders, or say what to change.</b><br>'
         'What changed since round 1: (1) <b>walls</b> follow the rules measured on OSI buildings and house multis (notes/uo-wall-orientation.md): the piece that runs along x sits on its tile\'s south edge, the one along y on its east edge, '
         'the corner piece closes a room\'s south-east corner and a T-junction, the post marks the north-west corner; round 1 had the two pieces swapped and the corners inverted, which drew every run as a saw-tooth. '
         '(2) <b>Variety</b>: every zone draws its floor from all the stock variants of its texture by weight, the cave rings and ramps from eight rock tiles each, and crystals, webs, stalagmites, hay, rubble, mushrooms, logs, vines and bones are placed in seeded clusters with gaps, mixed sizes and no two identical pieces side by side; one seed per zone in plan-sets.json. '
         '(3) The <b>renderer</b>: round 1\'s drew every static half a tile too high and could not draw slopes, so the cave rings showed black seams; this one draws them as the client does. '
         'The walkable floor, the openings, the crawlway and every wall tile are exactly round 1\'s (checked by the builder).</div>',
         '<h2>Round 1 and round 2 side by side: the Vault</h2>',
         '<table class="pair"><tr><th>Round 1 (not approved)</th><th>Round 2</th></tr><tr><td><a href="round1/vault.png"><img src="round1/vault.png" alt="vault round 1"></a></td><td><a href="vault.png"><img src="vault.png" alt="vault round 2"></a></td></tr></table>',
         '<h2>Walls check: our test rooms beside OSI rooms of the same set</h2>',
         '<p class="muted">Each row is one wall set: a 5 x 5 room and an L-shaped room built by the builder\'s wall rule, then OSI rooms from the stock map and a house design, then the same set as built in the Burrows. '
         'The OSI rooms: Deceit (Trammel 5184-5191 x 535-546 and 5188-5200 x 556-570), Nujel\'m (3672-3696 x 1231-1247, roofed) with the large marble house multi 0x96, Terathan Keep (5467-5479 x 3128-3140, two storeys) with the tower house multi 0x7A. '
         'More OSI renders and the statics dumps behind the rules are in <a href="../wall-research/">notes/art/wall-research/</a>.</p>',
         '<p><a href="walls-check.png"><img src="walls-check.png" alt="walls check"></a></p>',
         '<h2>Shown, not approved (P167 section 5 items 1, 2, 3 and 5)</h2>']
    o.append('<h3>1. The Stacks as bookcases instead of counters</h3><p class="muted">%s. Say bookcases, counters, or something else.</p><p><a href="proposal-stacks.png"><img src="proposal-stacks.png" alt="stacks"></a></p>' % E(crops['stacks'][5]))
    o.append('<h3>2. An arch and webs at the lair mouth</h3><p class="muted">The Terathan stone set\'s north-south doorway is two pieces over a 2-tile gap (0x01D8 passable half on the first open tile, 0x01D9 jamb half on the wall tile after the gap: Terathan Keep 5431,3132-3134 and the tower house multi 0x7A both do it that way). '
             'The approved mouth is 3 tiles (y 1246-1248), so (a) keeps all three open and puts the jamb one tile further south, leaving the arch top open in the middle; (b) is OSI\'s 2-tile doorway, which would close 5183,1248. (a) is what the Gloom render shows. Say (a), (b), or no arch.</p><p><a href="lair-mouth-check.png"><img src="lair-mouth-check.png" alt="lair mouth"></a></p>')
    o.append('<h3>3. The cave rings as they are</h3><p class="muted">%s. Impassable sloped land, as OSI\'s caves; no wall items on top (they would block sight and spells like the item-walled zones do).</p><p><a href="proposal-cavering.png"><img src="proposal-cavering.png" alt="cave ring"></a></p>' % E(crops['cavering'][5]))
    o.append('<h3>5. The Vault doorway with no door</h3><p class="muted">%s. The region refuses non-trainees at the tile; a door item would have to do the same.</p><p><a href="proposal-doorway.png"><img src="proposal-doorway.png" alt="doorway"></a></p>' % E(crops['doorway'][5]))
    o.append('<h2>Overview (top-down, radar colours, 4 px per tile; x 5120-5263, y 1112-1279)</h2><p><a href="overview.png"><img src="overview.png" alt="top-down overview"></a></p>')
    o.append('<h2>Zones (isometric, real tiles)</h2>')
    for name, x, y, w, h, what, size in made:
        o.append('<h3>%s</h3><p class="muted">x %d-%d, y %d-%d (%d x %d tiles). %s. %d KB</p><p><a href="%s.png"><img src="%s.png" alt="%s"></a></p>'
                 % (E(name), x, x + w - 1, y, y + h - 1, w, h, E(what), size // 1024, E(name), E(name), E(name)))
    o.append('<h2>What was placed</h2><p class="muted">Every static placed is in <code>notes/cc-P167-tools/statics-placed.csv</code>; land by id and Z in <code>land-summary.csv</code>; the rules (seeds, weights, clusters, proposals) in <code>plan-sets.json</code>; the builder is <code>build_burrows.py</code>, the renders <code>render_burrows.py</code> and <code>isorender.py</code>.</p>')
    o.append('</body></html>')
    text = '\n'.join(o)
    text.encode('ascii')
    open(os.path.join(OUT, 'index.html'), 'w', encoding='ascii', newline='\n').write(text)


if __name__ == '__main__':
    main()
