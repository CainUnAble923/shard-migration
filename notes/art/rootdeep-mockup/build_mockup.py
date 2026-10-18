"""cc-P141: the Rootdeep Burrows layout mockup and look swatches, for Chase to approve before the map batch starts.

    python -P build_mockup.py            (from this folder; needs Pillow and the local vseUOAware server, .mcp.json)

Reads:
  layout.json                                   the layout spec (zones, floors, obstacles, marks)
  D:/ShatteredLegacy/server/customizations/ClusterFRootdeepSeeder.cs    the spawners, arrival and ankh (the seeder's data)
  D:/ShatteredLegacy/server/customizations/Regions/RootdeepVault.cs     the doorway, crawlway and landing spot
Calls vseUOAware (P134's fixed copy): export_map_region_png for the radar base (its UOP map reading), render_art_tile
for every stock swatch. Writes layout.png, swatches/*.png, index.html beside this file. Third-party previews go to
local-previews/ (git-ignored: those packs' terms forbid reposting, and both repos are public).
"""
import html, json, os, re, shutil, sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vse import Vse  # noqa: E402

SEEDER = r'D:\ShatteredLegacy\server\customizations\ClusterFRootdeepSeeder.cs'
VAULT = r'D:\ShatteredLegacy\server\customizations\Regions\RootdeepVault.cs'
THIRD = r'D:\UO\third-party'
S = 7                      # pixels per tile
MARGIN = (32, 24, 24, 24)  # tiles around the Burrows rectangle shown from the radar base: left, top, right, bottom

# ---------------------------------------------------------------------------------------------------------- inputs

def read_seeder():
    src = open(SEEDER, encoding='utf-8').read()
    rows = []
    pat = re.compile(r'new\("([^"]+)", "([^"]+)", (\d+), (\d+), (\d+), (\d+), (true|false), (\d+), (\d+), ((?:"[A-Za-z]+"(?:, )?)+)\)')
    for m in pat.finditer(src):
        rows.append({'label': m.group(1), 'zone': m.group(2), 'x': int(m.group(3)), 'y': int(m.group(4)),
                     'count': int(m.group(5)), 'home': int(m.group(6)), 'group': m.group(7) == 'true',
                     'min': int(m.group(8)), 'max': int(m.group(9)), 'types': re.findall(r'"([A-Za-z]+)"', m.group(10))})
    pt = lambda name, text: tuple(int(v) for v in re.search(name + r' = new\((\d+), (\d+)', text).groups())
    vault = open(VAULT, encoding='utf-8').read()
    return rows, {'arrival': pt('Arrival', src), 'ankh': pt('AnkhAt', src), 'doorway': pt('Doorway', vault),
                  'landingSpot': pt('LandingSpot', vault), 'mouth': pt('CrawlwayMouth', vault), 'exit': pt('CrawlwayExit', vault)}


def cells(rect):
    x1, y1, x2, y2 = rect
    return {(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}


# ---------------------------------------------------------------------------------------------------------- the plan

def build_plan(layout, rows, pts, radar_path):
    ax1, ay1, ax2, ay2 = layout['area']
    ox, oy = ax1 - MARGIN[0], ay1 - MARGIN[1]
    w, h = (ax2 - ax1 + 1) + MARGIN[0] + MARGIN[2], (ay2 - ay1 + 1) + MARGIN[1] + MARGIN[3]

    floor = {}
    for f in layout['floors']:
        for c in cells(f['rect']):
            floor[c] = f['zone']
    solid = set()
    for o in layout['obstacles']:
        solid |= cells(o['rect'])
    for c in solid:
        floor.pop(c, None)
    walls = set()
    for (x, y) in floor:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (x + dx, y + dy)
                if n not in floor:
                    walls.add(n)

    # Checks the spec must pass before it goes in front of Chase.
    problems = []
    for (x, y) in list(floor) + list(walls):
        if not (ax1 <= x <= ax2 and ay1 <= y <= ay2):
            problems.append('tile %d,%d outside the Burrows rectangle' % (x, y))
        if x < layout['buildFromX']:
            problems.append('tile %d,%d west of x %d' % (x, y, layout['buildFromX']))
    for r in rows:
        if (r['x'], r['y']) not in floor:
            problems.append('spawner "%s" at %d,%d is not on a floor' % (r['label'], r['x'], r['y']))
    for name in ('arrival', 'ankh', 'landingSpot', 'mouth', 'exit'):
        if pts[name] not in floor:
            problems.append('%s at %s is not on a floor' % (name, pts[name]))
    # The doorway and the crawlway are cut through walls: a floor must lie on each side of them.
    dx, dy = pts['doorway']
    if (dx - 1, dy) not in floor or (dx + 1, dy) not in floor or floor.get((dx - 1, dy)) != 'Vault':
        problems.append('the Vault doorway at %d,%d does not join the Vault to the landing' % (dx, dy))
    if floor.get(pts['mouth']) != 'Vault' or floor.get(pts['exit']) != 'Warren':
        problems.append('the crawlway does not run from the Vault to the Warren')
    # A spawner picks any walkable tile in its bounds (BaseSpawner home range), so every floor tile in the bounds must be
    # reachable from the spawner inside them; otherwise it would spawn through a wall into the next room.
    for r in rows:
        hr = r['home']
        inb = lambda c: abs(c[0] - r['x']) <= hr and abs(c[1] - r['y']) <= hr
        seen, todo = {(r['x'], r['y'])}, [(r['x'], r['y'])]
        while todo:
            x, y = todo.pop()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n in floor and inb(n) and n not in seen:
                    seen.add(n)
                    todo.append(n)
        stray = [c for c in floor if inb(c) and c not in seen]
        if stray:
            problems.append('spawner "%s": home range %d reaches %d floor tiles beyond a wall (e.g. %s)' % (r['label'], hr, len(stray), stray[0]))
    zones = {z['key']: z for z in layout['zones']}
    for r in rows:
        zx1, zy1, zx2, zy2 = zones[r['zone']]['rect']
        if not (zx1 <= r['x'] <= zx2 and zy1 <= r['y'] <= zy2):
            problems.append('spawner "%s" outside its zone %s' % (r['label'], r['zone']))

    base = Image.open(radar_path).convert('RGB')
    assert base.size == (w, h), (base.size, (w, h))
    img = base.resize((w * S, h * S), Image.NEAREST)
    img = Image.blend(img, Image.new('RGB', img.size, (18, 18, 22)), 0.35)
    d = ImageDraw.Draw(img, 'RGBA')
    font = ImageFont.load_default()
    try:
        font = ImageFont.truetype('arial.ttf', 11)
        big = ImageFont.truetype('arialbd.ttf', 14)
    except OSError:
        big = font

    def box(x, y, fill, outline=None):
        px, py = (x - ox) * S, (y - oy) * S
        d.rectangle([px, py, px + S - 1, py + S - 1], fill=fill, outline=outline)

    def hexrgb(c, a=255):
        return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)

    # the Burrows rectangle and the building line
    d.rectangle([(ax1 - ox) * S, (ay1 - oy) * S, (ax2 - ox + 1) * S - 1, (ay2 - oy + 1) * S - 1], outline=(200, 200, 200, 255), width=2)
    bx = (layout['buildFromX'] - ox) * S
    d.line([bx, (ay1 - oy) * S, bx, (ay2 - oy + 1) * S], fill=(200, 80, 80, 200), width=1)
    # grid, one cell per tile, inside the rectangle
    for x in range(ax1, ax2 + 2):
        d.line([(x - ox) * S, (ay1 - oy) * S, (x - ox) * S, (ay2 - oy + 1) * S], fill=(255, 255, 255, 18))
    for y in range(ay1, ay2 + 2):
        d.line([(ax1 - ox) * S, (y - oy) * S, (ax2 - ox + 1) * S, (y - oy) * S], fill=(255, 255, 255, 18))

    for c in walls:
        box(*c, fill=(92, 84, 76, 255))
    for c in solid:
        box(*c, fill=(40, 36, 34, 255))
    for c, z in floor.items():
        box(*c, fill=hexrgb(zones[z]['color'], 200))

    marks = layout['marks']
    # fight space and kite loops
    fx1, fy1, fx2, fy2 = marks['fightSpace']['rect']
    d.rectangle([(fx1 - ox) * S, (fy1 - oy) * S, (fx2 - ox + 1) * S - 1, (fy2 - oy + 1) * S - 1], outline=(255, 70, 70, 255), width=2)
    for (kx1, ky1, kx2, ky2) in marks['kiteLoops']:
        for i in range(kx1, kx2 + 1):
            for j in (ky1, ky2):
                if (i + j) % 2 == 0:
                    box(i, j, fill=(255, 255, 255, 150))
        for j in range(ky1, ky2 + 1):
            for i in (kx1, kx2):
                if (i + j) % 2 == 0:
                    box(i, j, fill=(255, 255, 255, 150))
    # doorway and crawlway (cut through the walls)
    for c in cells(marks['vaultDoorway']['rect']):
        box(*c, fill=(255, 230, 40, 255), outline=(0, 0, 0, 255))
    for c in cells(marks['crawlway']['rect']):
        box(*c, fill=(255, 140, 20, 255), outline=(0, 0, 0, 255))
    cx, cy = (pts['mouth'][0] - ox) * S + S // 2, (pts['mouth'][1] - oy) * S
    d.line([cx, cy - 4 * S, cx, cy + 4 * S], fill=(255, 140, 20, 255), width=2)
    d.polygon([(cx - 6, cy + 4 * S - 6), (cx + 6, cy + 4 * S - 6), (cx, cy + 4 * S + 4)], fill=(255, 140, 20, 255))
    d.text(((pts['mouth'][0] - ox + 2) * S, (pts['mouth'][1] - oy + 1) * S), 'one way', fill=(255, 170, 60, 255), font=font)

    # ankh, arrival, landing spot
    ax, ay = pts['ankh']
    box(ax, ay, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
    box(ax, ay + 1, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
    d.text(((ax - ox - 5) * S, (ay - oy - 2) * S), 'ankh', fill=(255, 255, 255, 255), font=font)
    rx, ry = pts['arrival']
    d.ellipse([(rx - ox) * S - 3, (ry - oy) * S - 3, (rx - ox + 1) * S + 2, (ry - oy + 1) * S + 2], outline=(120, 220, 255, 255), width=2)
    d.text(((rx - ox - 4) * S, (ry - oy + 2) * S), 'arrival (B1 hole)', fill=(160, 230, 255, 255), font=font)

    # spawners: numbered dots, decoy chests as squares
    for i, r in enumerate(rows, 1):
        px, py = (r['x'] - ox) * S + S // 2, (r['y'] - oy) * S + S // 2
        if r['types'] == ['SafeDepositBox']:
            d.rectangle([px - 6, py - 6, px + 6, py + 6], fill=(150, 90, 30, 255), outline=(255, 220, 120, 255), width=2)
        else:
            rad = 7 if r['count'] == 1 and r['min'] >= 10 else 6
            d.ellipse([px - rad, py - rad, px + rad, py + rad], fill=(20, 20, 20, 230), outline=(255, 255, 255, 255), width=1)
        d.text((px - 5 if i < 10 else px - 7, py - 6), str(i), fill=(255, 255, 255, 255), font=font)
        if r['home']:
            hr = r['home']
            d.rectangle([(r['x'] - hr - ox) * S, (r['y'] - hr - oy) * S, (r['x'] + hr - ox + 1) * S, (r['y'] + hr - oy + 1) * S],
                        outline=(255, 255, 255, 40))

    # zone labels
    # Labels sit in the rock above each zone where there is room, otherwise inside along a quiet edge.
    inside_bottom = {'Warren', 'Gloom lair'}
    inside_top = {'Brood Pit'}
    for z in layout['zones']:
        x1, y1, x2, y2 = z['rect']
        label = z['name'] if z['tier'] in ('tutorial', 'safe') else '%s  (tier %s)' % (z['name'], z['tier'])
        ly = y2 - 2 if z['key'] in inside_bottom else y1 + 0.3 if z['key'] in inside_top else y1 - 3.2
        d.text(((x1 - ox) * S + 3, int((ly - oy) * S)), label, fill=(255, 255, 255, 255), font=big,
               stroke_width=2, stroke_fill=(0, 0, 0, 255))
    # axis ticks every 10 tiles
    for x in range((ax1 // 10 + 1) * 10, ax2 + 1, 10):
        d.text(((x - ox) * S - 12, (ay1 - oy) * S - 14), str(x), fill=(220, 220, 220, 255), font=font)
    for y in range((ay1 // 10 + 1) * 10, ay2 + 1, 10):
        d.text(((ax1 - ox) * S - 34, (y - oy) * S - 6), str(y), fill=(220, 220, 220, 255), font=font)
    d.text(((ax1 - ox) * S, (ay2 - oy + 2) * S), 'Trammel x %d-%d, y %d-%d; one cell per tile; base: vseUOAware radar export' %
           (ax1, ax2, ay1, ay2), fill=(220, 220, 220, 255), font=font)
    img.save(os.path.join(HERE, 'layout.png'), optimize=True)

    stats = {'floor': len(floor), 'walls': len(walls), 'solid': len(solid)}
    sx1, sy1, sx2, sy2 = marks['fightSpace']['rect']
    strong = cells([sx1, sy1, sx2, sy2])
    stats['strongroomFloor'] = len([c for c in strong if c in floor])
    stats['strongroomSize'] = (sx2 - sx1 + 1, sy2 - sy1 + 1)
    return problems, stats, (ox, oy, w, h)


# ---------------------------------------------------------------------------------------------------------- swatches

# Stock candidates: tiles OSI's own Trammel dungeons are built from (dungeon-survey.json counts them), by zone.
# Each set: (key, name, where OSI uses it, [(role, id, kind)]); kind 'land' ids < 0x4000, 'item' ids as tiledata items.
STOCK = {
    'Landing': [
        ('L-A', 'Dungeon stone cave', 'Deceit, Hythloth', [('floor', 0x245, 'land'), ('wall', 0x242, 'item'), ('wall', 0x241, 'item'), ('arch', 0x247, 'item')]),
        ('L-B', 'Rough cave', 'Orc Cave, Covetous', [('floor', 0x53D, 'item'), ('wall', 0x25A, 'land'), ('steps', 0x79E, 'item'), ('decor', 0x8E1, 'item')]),
    ],
    'Vault': [
        ('V-A', 'Marble strongroom', 'stock marble (banks, Wind)', [('floor', 0x486, 'land'), ('wall', 0x0F8, 'item'), ('door', 0x675, 'item'), ('decor', 0xB40, 'item')]),
        ('V-B', 'Sandstone vault', 'stock sandstone', [('floor', 0x51D, 'item'), ('wall', 0x158, 'item'), ('arch', 0x190, 'item'), ('door', 0x824, 'item')]),
        ('V-C', 'Dungeon stone vault', 'Wrong, Terathan Keep', [('floor', 0x43E, 'land'), ('wall', 0x01A, 'item'), ('door', 0x6F5, 'item'), ('arch', 0x1E6, 'item')]),
    ],
    'Warren': [
        ('W-A', 'Dirt burrows', 'stock dirt, cave walls', [('floor', 0x071, 'land'), ('wall', 0x25A, 'land'), ('decor', 0x8E1, 'item'), ('decor', 0xF34, 'item')]),
        ('W-B', 'Cave burrows', 'Destard, Despise', [('floor', 0x246, 'land'), ('wall', 0x241, 'item'), ('decor', 0x8E5, 'item'), ('decor', 0x10EE, 'item')]),
    ],
    'Tangle': [
        ('T-A', 'Rooted cave', 'Despise (mushrooms), stock vines', [('floor', 0x246, 'land'), ('wall', 0x266, 'land'), ('decor', 0xCF1, 'item'), ('decor', 0xD16, 'item'), ('decor', 0xCF3, 'item')]),
        ('T-B', 'Root forest under earth', 'stock dirt and o\'hii roots', [('floor', 0x071, 'land'), ('wall', 0x25A, 'land'), ('decor', 0xC9E, 'item'), ('decor', 0xD0C, 'item')]),
    ],
    'Dawnseam': [
        ('D-A', 'Crystal seam', 'stock crystal (Ter Mur style)', [('floor', 0x3867, 'land'), ('wall', 0x25A, 'land'), ('decor', 0x2224, 'item'), ('decor', 0x2228, 'item')]),
        ('D-B', 'Stone seam', 'Wrong, Hythloth', [('floor', 0x441, 'land'), ('wall', 0x2FE, 'item'), ('decor', 0x8E3, 'item'), ('decor', 0x8E8, 'item')]),
    ],
    'Gloom': [
        ('G-A', 'Terathan dark stone', 'Terathan Keep', [('floor', 0x440, 'land'), ('wall', 0x1D0, 'item'), ('wall', 0x1EA, 'item'), ('decor', 0x10B8, 'item'), ('decor', 0xEE3, 'item')]),
        ('G-B', 'Webbed cave', 'Covetous, Terathan Keep', [('floor', 0x25A, 'land'), ('wall', 0x242, 'item'), ('floor', 0x523, 'item'), ('decor', 0x10B8, 'item')]),
    ],
    'Gloom lair': [
        ('Q-A', 'Lair arch and webs', 'Terathan Keep', [('arch', 0x1E6, 'item'), ('wall', 0x1E9, 'item'), ('decor', 0xEE3, 'item'), ('decor', 0x10B8, 'item')]),
    ],
    'Crawlway': [
        ('C-A', 'Cave-in and crawlway (as built)', 'the RootdeepCrawlway item: closed rocks, open hole', [('closed', 0x1367, 'item'), ('open', 0x1B71, 'item')]),
    ],
}

# Third-party candidates (ART-LIBRARY.md section 2, Dungeon kits). Flags as the library writes them, plus each SOURCE.txt's terms.
THIRD_PARTY = {
    'Landing': [('X-1', 'Custom cave entrances (otimpyre)', r'custom-caves\Custom Caves Entrances', ['1.bmp', '5.bmp', '9.bmp'],
                 'CREDIT (otimpyre); no terms stated: ship only in the player package or a private repo, never repost')],
    'Vault': [('X-2', 'Blue stone tiles (DRC1K)', r'drc1k-uoassets\Blue_Stone_Assets', ['church_wall.bmp', 'arch_west.bmp', 'round.bmp'],
               'CREDIT (DRC1K); non-commercial; no redistribution outside the client; NO MODIFICATIONS (recolour needs his OK)'),
              ('X-3', 'Ultimate Dungeon Wall Set (DRC1K)', r'drc1k-uoassets\The Ultimate Dungeon Wall Set by-DRC1K', ['Ruined_Dungeon_Wall_1.bmp', 'Round_Ruined_Dungeon_Wall_1.bmp', 'Dungeon_Stairs_1.bmp'],
               'CREDIT (DRC1K); non-commercial; no redistribution outside the client; NO MODIFICATIONS')],
    'Warren': [('X-4', 'Gray rocks (DRC1K)', r'drc1k-uoassets\gray-rocks-asset-by-DRC1K', ['rock1.bmp', 'rock4.bmp', 'rock8.bmp'],
                'CREDIT (DRC1K); non-commercial; no redistribution outside the client; NO MODIFICATIONS')],
    'Gloom': [('X-5', 'Ruined dungeon walls, dark (DRC1K)', r'drc1k-uoassets\The Ultimate Dungeon Wall Set by-DRC1K', ['Ruined_Dungeon_Wall_20.bmp', 'Ruined_Dungeon_Wall_30.bmp'],
               'CREDIT (DRC1K); non-commercial; no redistribution outside the client; NO MODIFICATIONS')],
    'Crawlway': [('X-6', 'Cave hole (otimpyre)', r'holes\Holes\[Custom Art] Hole Cave', ['1.bmp', '2.bmp', '3.bmp', '4.bmp'],
                  'EA (built from EA solen hole art: ship as patch records only); CREDIT (otimpyre); no terms stated, never repost')],
}
QUEUED = {
    'Tangle': 'Giant Blue / Red Mushrooms (Q#235, Q#236) are queued, not on disk yet.',
    'Dawnseam': 'Crystal Set (Q#284) and Crystal Wall (Q#302) are queued, not on disk yet; Ore Stalagmite deposits Q#299 too.',
    'Landing': 'Cave Entrances (Q#347) is queued, not on disk yet.',
}


def render_stock(v):
    out = os.path.join(HERE, 'swatches')
    os.makedirs(out, exist_ok=True)
    art = v.uo('artLegacyMUL.uop')
    names = {}
    for sets in STOCK.values():
        for (_, _, _, tiles) in sets:
            for (_, tid, kind) in tiles:
                full = tid if kind == 'land' else tid + 0x4000
                fn = '%s-%04X.png' % (kind, tid)
                path = os.path.join(out, fn)
                if not os.path.exists(path):
                    # vseUOAware saves under its own exports folder whatever path it is given (P134 section 7.2); copy it.
                    res = v.call('render_art_tile', {'artUopFilePath': art, 'tileId': full, 'outputPngPath': fn})
                    shutil.copyfile(res.rsplit(' to: ', 1)[1].strip(), path)
                if (kind, tid) not in names:
                    meta = v.call('get_land_tile' if kind == 'land' else 'get_item_tile',
                                  {'tileDataFilePath': v.uo('tiledata.mul'), 'tileId': full})
                    m = re.search(r'"([^"]*)"', meta)
                    names[(kind, tid)] = m.group(1) if m else ''
    return names


def render_third_party():
    out = os.path.join(HERE, 'local-previews')
    os.makedirs(out, exist_ok=True)
    made = {}
    for sets in THIRD_PARTY.values():
        for (key, _, folder, files, _) in sets:
            for f in files:
                src = os.path.join(THIRD, folder, f)
                dst = os.path.join(out, '%s-%s.png' % (key, os.path.splitext(f)[0].replace(' ', '_')))
                if os.path.exists(src):
                    im = Image.open(src).convert('RGBA')
                    bg = im.getpixel((0, 0))
                    px = im.load()
                    for y in range(im.height):
                        for x in range(im.width):
                            if px[x, y][:3] == bg[:3]:
                                px[x, y] = (0, 0, 0, 0)
                    im.save(dst)
                    made[(key, f)] = os.path.basename(dst)
    return made


# ---------------------------------------------------------------------------------------------------------- the page

CSS = """
:root { --bg:#f6f4ef; --fg:#1f1d1a; --muted:#6b6560; --card:#ffffff; --line:#ddd6cc; --accent:#8a5a1c; --warn:#a33; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#16151a; --fg:#ece8e1; --muted:#a39d95; --card:#211f26; --line:#3a3640; --accent:#e0a85a; --warn:#f27; } }
:root[data-theme="dark"] { --bg:#16151a; --fg:#ece8e1; --muted:#a39d95; --card:#211f26; --line:#3a3640; --accent:#e0a85a; --warn:#f27; }
body { background:var(--bg); color:var(--fg); font:15px/1.5 system-ui, sans-serif; margin:0 auto; max-width:1180px; padding:16px; }
h1 { font-size:24px; margin:8px 0 4px; } h2 { font-size:19px; margin:28px 0 8px; border-bottom:1px solid var(--line); }
h3 { font-size:16px; margin:16px 0 6px; } .muted { color:var(--muted); }
.ask { background:var(--card); border:2px solid var(--accent); border-radius:8px; padding:12px 16px; }
.plan img { width:100%; height:auto; image-rendering:pixelated; border:1px solid var(--line); }
.sets { display:flex; flex-wrap:wrap; gap:12px; }
.set { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:10px; min-width:240px; flex:1 1 260px; }
.tiles { display:flex; flex-wrap:wrap; gap:8px; align-items:flex-end; }
.tile { text-align:center; font-size:12px; color:var(--muted); }
.tile img { display:block; margin:0 auto; max-height:120px; image-rendering:pixelated; background:repeating-conic-gradient(#8882 0 25%, transparent 0 50%) 50% / 12px 12px; }
.flag { display:inline-block; font-size:12px; border:1px solid var(--warn); color:var(--warn); border-radius:4px; padding:0 5px; margin:2px 0; }
table { border-collapse:collapse; width:100%; font-size:13px; } td, th { border-bottom:1px solid var(--line); padding:4px 6px; text-align:left; vertical-align:top; }
.scroll { overflow-x:auto; } code { font-size:13px; }
"""


def page(layout, rows, pts, stats, problems, names, thirdmade):
    E = html.escape
    zones = {z['key']: z for z in layout['zones']}
    o = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">',
         '<title>Rootdeep Burrows Mockup</title><style>%s</style></head><body>' % CSS,
         '<h1>Rootdeep Burrows: layout and look</h1>',
         '<p class="muted">cc-P141, 2026-10-18. Drawn from the layout spec (<code>layout.json</code>) and the seeder\'s data '
         '(<code>ClusterFRootdeepSeeder.cs</code>), over a vseUOAware radar export of the same rectangle. Nothing is placed '
         'and no map is edited until you approve.</p>',
         '<div class="ask"><b>Approve this layout and look, or tell me what to change.</b><br>Open choices:<ol>'
         '<li>The layout as drawn (zones, rooms, the Vault\'s four rooms, the crawlway at x 5160, the landing ankh).</li>'
         '<li>One look per zone: pick a set below (or mix: say which floor, wall and door).</li>'
         '<li>The Warren fillers: Rotworm (rare tank) and Grubber (rare runner) kept; BloodWorm moved to the Gloom (it has 374-422 hits, too strong for tier 1). Or drop it.</li>'
         '<li>A Young trainee who dies in the Vault wakes at New Haven\'s healer (pinned\'s Young rule), not the landing: keep, or ask for a Vault rule (needs a pinned patch).</li>'
         '<li>Third-party kits: DRC1K\'s terms forbid modifications and reposting; say if any of them should be asked for or used.</li>'
         '</ol></div>']
    if problems:
        o.append('<h2>Spec problems</h2><ul>%s</ul>' % ''.join('<li>%s</li>' % E(p) for p in problems))
    o.append('<h2>The layout</h2><div class="plan"><a href="layout.png"><img src="layout.png" alt="Top-down layout of the Rootdeep Burrows"></a></div>')
    o.append('<p class="muted">Legend: zone colours are floor; brown-gray is wall; near-black is a solid block (pillar, shelving, roots, crystal, webs); '
             'yellow is the Vault doorway; orange is the one-way crawlway (arrow south); white is the ankh; the blue ring is the arrival from the B1 hole; '
             'numbered dots are spawners (table below), brown squares are the decoy chests; the red box is the Overdraft\'s fight space and the dotted '
             'white rings are its kite loops around the two pillars; faint squares are each spawner\'s home range; the red line is x 5140.</p>')
    sw, sh = stats['strongroomSize']
    o.append('<h3>Does the Vault fit the Overdraft fight?</h3><p>Yes. The Strongroom is %d x %d tiles (%d walkable after the two 3 x 6 pillars). '
             'The Overdraft is one mobile on one tile, drawn about 89 x 83 px at 1.5x (about two tiles wide on screen) and walks at 0.4 s a tile; '
             'a running player covers a tile in 0.2 s. Each pillar loop is 22 tiles round, so a player can kite it around either pillar or in a figure '
             'eight through the 13-tile gap between them, with the three decoy chests a room away in the Deposit Hall. Nothing more is needed; the '
             'spare room is the space between the pillars and the walls (4 to 8 tiles each side).</p>' % (sw, sh, stats['strongroomFloor']))
    # spawner table
    o.append('<h2>Spawners (the seeder\'s data)</h2><div class="scroll"><table><tr><th>#</th><th>Where</th><th>Zone</th><th>Tile</th><th>Creatures</th>'
             '<th>At once</th><th>Home</th><th>Group</th><th>Respawn (min)</th></tr>')
    for i, r in enumerate(rows, 1):
        o.append('<tr><td>%d</td><td>%s</td><td>%s</td><td>%d,%d</td><td>%s</td><td>%d</td><td>%d</td><td>%s</td><td>%d-%d</td></tr>' %
                 (i, E(r['label']), E(r['zone']), r['x'], r['y'], E(', '.join(r['types'])), r['count'], r['home'],
                  'yes' if r['group'] else 'no', r['min'], r['max']))
    o.append('</table></div><p class="muted">Placed by <code>[ClusterFSeedRootdeep</code> once the walls exist (it refuses on void land). '
             'Also placed: the landing ankh at %d,%d (AnkhWest, P137\'s method) and the crawlway at %d,%d.</p>' % (pts['ankh'] + pts['mouth']))
    # swatches
    o.append('<h2>Look: candidate tiles per zone</h2><p class="muted">Stock tiles are rendered by vseUOAware\'s <code>render_art_tile</code> '
             'from the client\'s art; every one is a tile OSI\'s own Trammel dungeons use (see <code>dungeon-survey.json</code>). vseUOAware has no '
             'texture (texmaps) renderer, so floors show as their land-art diamond, which is how the client draws flat land anyway. Third-party '
             'previews are local only (their terms forbid reposting and both repos are public): they show when this page is opened from Chase\'s PC '
             'after <code>build_mockup.py</code> has run.</p>')
    for zkey in ['Landing', 'Vault', 'Warren', 'Tangle', 'Dawnseam', 'Gloom', 'Gloom lair', 'Crawlway']:
        title = zones[zkey]['name'] if zkey in zones else 'The crawlway'
        o.append('<h3>%s</h3><div class="sets">' % E(title))
        for (key, name, where, tiles) in STOCK.get(zkey, []):
            o.append('<div class="set"><b>%s %s</b><br><span class="muted">stock (EA art, ships as is); used in %s</span><div class="tiles">' % (key, E(name), E(where)))
            for (role, tid, kind) in tiles:
                o.append('<div class="tile"><img src="swatches/%s-%04X.png" alt="%s 0x%04X"><div>%s<br>%s 0x%04X</div><div>%s</div></div>' %
                         (kind, tid, kind, tid, E(role), kind, tid, E(names.get((kind, tid), ''))))
            o.append('</div></div>')
        for (key, name, folder, files, flags) in THIRD_PARTY.get(zkey, []):
            o.append('<div class="set"><b>%s %s</b><br><span class="muted">third-party: <code>third-party\\%s</code></span><br><span class="flag">%s</span><div class="tiles">' %
                     (key, E(name), E(folder), E(flags)))
            for f in files:
                fn = thirdmade.get((key, f))
                o.append('<div class="tile"><img src="local-previews/%s" alt="%s (local preview)"><div>%s</div></div>' % (E(fn or ''), E(f), E(f)))
            o.append('</div></div>')
        o.append('</div>')
        if zkey in QUEUED:
            o.append('<p class="muted">%s</p>' % E(QUEUED[zkey]))
    o.append('<h2>Floors and blocks in the spec</h2><div class="scroll"><table><tr><th>Zone</th><th>Piece</th><th>Tiles (x1,y1 to x2,y2)</th></tr>')
    for f in layout['floors']:
        o.append('<tr><td>%s</td><td>%s</td><td>%d,%d to %d,%d</td></tr>' % ((E(f['zone']), E(f['name'])) + tuple(f['rect'])))
    for b in layout['obstacles']:
        o.append('<tr><td>%s</td><td>%s (solid)</td><td>%d,%d to %d,%d</td></tr>' % ((E(b['zone']), E(b['name'])) + tuple(b['rect'])))
    o.append('</table></div><p class="muted">%d floor tiles, %d wall tiles, %d solid tiles.</p></body></html>' %
             (stats['floor'], stats['walls'], stats['solid']))
    text = '\n'.join(o)
    text.encode('ascii')  # the repo rule: ASCII only
    open(os.path.join(HERE, 'index.html'), 'w', encoding='ascii', newline='\n').write(text)


def main():
    layout = json.load(open(os.path.join(HERE, 'layout.json'), encoding='utf-8'))
    rows, pts = read_seeder()
    expected = len(re.findall(r'^\s+new\("', open(SEEDER, encoding='utf-8').read(), re.M))
    assert len(rows) == expected, (len(rows), expected)  # every row of the seeder was read
    ax1, ay1, ax2, ay2 = layout['area']
    x0, y0 = ax1 - MARGIN[0], ay1 - MARGIN[1]
    w, h = (ax2 - ax1 + 1) + MARGIN[0] + MARGIN[2], (ay2 - ay1 + 1) + MARGIN[1] + MARGIN[3]
    radar = os.path.join(HERE, 'radar-base.png')
    with Vse() as v:
        res = v.call('export_map_region_png', {'x': x0, 'y': y0, 'width': w, 'height': h, 'facet': 1,
                                               'radarColFilePath': v.uo('radarcol.mul'), 'outputPngPath': 'rootdeep-radar-base.png'})
        shutil.copyfile(re.search(r'PNG \(.*?\): (.*\.png)', res).group(1), radar)
        names = render_stock(v)
    problems, stats, _ = build_plan(layout, rows, pts, radar)
    thirdmade = render_third_party()
    page(layout, rows, pts, stats, problems, names, thirdmade)
    print('rows', len(rows), 'stats', stats)
    print('problems:', problems or 'none')


if __name__ == '__main__':
    main()
