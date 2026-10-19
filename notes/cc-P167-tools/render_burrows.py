"""cc-P167: renders the scratch Rootdeep Burrows for Chase: one top-down overview (radar colours, 4 px per tile) and
isometric real-tile renders of each zone through vseUOAware's render_map_region (classic art, so the scratch folder
holds art.mul/artidx.mul unpacked from artLegacyMUL.uop by uop2art.py; at most 96 x 96 tiles a picture; saved as 256-colour PNGs). Writes into
notes/art/rootdeep-build/ with an index page.

    python -P render_burrows.py <scratch folder>
"""
import html, json, os, re, shutil, sys

sys.path.insert(0, r'D:\UO\shard-migration\notes\art\rootdeep-mockup')
from vse import Vse  # noqa: E402
from PIL import Image  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r'D:\UO\shard-migration\notes\art\rootdeep-build'
E = html.escape

# name, x, y, w, h (tiles), what the picture shows
ZONES = [
    ('landing', 5174, 1128, 36, 39, 'The Landing (safe), the arrival, the ankh wall, the Vault doorway at x 5179, and the tunnel south to the Warren'),
    ('vault', 5138, 1128, 45, 37, 'The Vault (tutorial only): Counting Room, the Stacks with its counter rows, Deposit Hall, the Strongroom with its two walled pillars, the crawlway in the south wall at x 5160'),
    ('warren-west', 5140, 1158, 51, 43, 'The Warren, west: Crawl Den (the crawlway lands at 5160,1162) and the Great Burrow west half'),
    ('warren-east', 5182, 1158, 63, 41, 'The Warren, east: Tunnel Foot (the landing tunnel lands here), the Great Burrow east half, and the Brood Pit through its mouth at x 5209-5211'),
    ('tangle', 5138, 1194, 59, 43, 'The Tangle (tier 2): the root cavern with its five rock-and-log root masses, the Thicket behind its gap at x 5157, the passage east to the Dawnseam'),
    ('dawnseam', 5190, 1194, 57, 43, 'The Dawnseam (tier 2): the crystal seam with its five crystal clusters, the Seam Heart behind its gap at x 5227'),
    ('gloom-west', 5146, 1226, 56, 39, 'The Gloom, west half (tier 3): the descent from the Tangle, the ring tunnels, two web masses, the lair mouth at x 5183'),
    ('gloom-east', 5190, 1226, 51, 39, 'The Gloom, east half: the descent from the Dawnseam, the Queen\'s lair with its two web pillars, the east and south runs'),
]
OVERVIEW = (5120, 1112, 144, 168)


def grab(text):
    m = re.search(r'([A-Z]:\\[^\r\n]*?\.png)', text)
    if not m:
        raise RuntimeError('no png path in: ' + text[:300])
    return m.group(1)


def main():
    folder = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    p = lambda n: os.path.join(folder, n)
    made = []
    with Vse() as v:
        x, y, w, h = OVERVIEW
        t = v.call('export_map_region_png', {'x': x, 'y': y, 'width': w, 'height': h, 'radarColFilePath': p('radarcol.mul'),
                                             'mapFilePath': p('map1LegacyMUL.uop'), 'staticsMulFilePath': p('statics1.mul'),
                                             'staIdxMulFilePath': p('staidx1.mul'), 'facetWidthBlocks': 896, 'facetHeightTiles': 4096,
                                             'includeStatics': True, 'outputPngPath': 'p167-overview.png'})
        im = Image.open(grab(t)).convert('RGB')
        assert im.size == (w, h), im.size
        im = im.resize((w * 4, h * 4), Image.NEAREST)
        im.save(os.path.join(OUT, 'overview.png'), optimize=True)
        for name, x, y, w, h, what in ZONES:
            t = v.call('render_map_region', {'mapFilePath': p('map1LegacyMUL.uop'), 'staticsMulFilePath': p('statics1.mul'),
                                             'staIdxMulFilePath': p('staidx1.mul'), 'artIdxFilePath': p('artidx.mul'),
                                             'artMulFilePath': p('art.mul'), 'facetWidthBlocks': 896, 'x': x, 'y': y,
                                             'width': w, 'height': h, 'outputPngPath': 'p167-%s.png' % name})
            src = grab(t)
            dst = os.path.join(OUT, '%s.png' % name)
            # 256-colour palette: the renders are flat classic art, the quantised file is a third the size and looks the same
            Image.open(src).convert('RGB').quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(dst, optimize=True)
            made.append((name, x, y, w, h, what, os.path.getsize(dst)))
            print(name, os.path.getsize(dst), flush=True)
    page(made)


def page(made):
    o = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">',
         '<title>Rootdeep Burrows Build</title><style>',
         ':root { --bg:#f6f4ef; --fg:#1f1d1a; --muted:#6b6560; --card:#ffffff; --line:#ddd6cc; --accent:#8a5a1c; }',
         '@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#16151a; --fg:#ece8e1; --muted:#a39d95; --card:#211f26; --line:#3a3640; --accent:#e0a85a; } }',
         ':root[data-theme="dark"] { --bg:#16151a; --fg:#ece8e1; --muted:#a39d95; --card:#211f26; --line:#3a3640; --accent:#e0a85a; }',
         'body { background:var(--bg); color:var(--fg); font:15px/1.5 system-ui, sans-serif; margin:0 auto; max-width:1180px; padding:16px; }',
         'h1 { font-size:24px; margin:8px 0 4px; } h2 { font-size:19px; margin:28px 0 8px; border-bottom:1px solid var(--line); }',
         '.muted { color:var(--muted); } .ask { background:var(--card); border:2px solid var(--accent); border-radius:8px; padding:12px 16px; }',
         'img { max-width:100%; height:auto; border:1px solid var(--line); background:#000; } table { border-collapse:collapse; font-size:13px; }',
         'td, th { border-bottom:1px solid var(--line); padding:4px 8px; text-align:left; vertical-align:top; }',
         '</style></head><body>',
         '<h1>Rootdeep Burrows: the build, rendered from the scratch map</h1>',
         '<p class="muted">cc-P167, 2026-10-18. P141\'s approved layout built into a scratch copy of Trammel (outside both repos), drawn by vseUOAware from the real tiles: '
         'the top-down overview in radar colours and an isometric render of each zone (classic art, no hues, no texture-mapped land, so flat land shows its art diamond, as the client draws it; the client adds lighting and the land textures). Nothing has touched the real map files.</p>',
         '<div class="ask"><b>Approve these renders, or say what to change.</b><br>Built as the mockup page proposed (its first set per zone, all stock EA tiles: no third-party art, so nothing new is registered): '
         'Landing L-A dungeon stone cave, Vault V-A marble strongroom (counters for the shelving, marble-walled pillars), Warren W-A dirt burrows, Tangle T-A rooted cave, Dawnseam D-A crystal seam, Gloom G-A Terathan dark stone, lair Q-A, crawlway C-A. '
         'Cave zones use sloped cave-rock land for their walls as OSI\'s own caves do; every floor is flat at Z 0. Things you might want changed: a zone\'s look, more or fewer rocks, mushrooms, crystals and webs, the pillars as walled blocks, the counters as shelving.</div>',
         '<h2>Overview (top-down, radar colours, 4 px per tile; x 5120-5263, y 1112-1279)</h2><p><a href="overview.png"><img src="overview.png" alt="top-down overview"></a></p>',
         '<h2>Zones (isometric, real tiles)</h2>']
    for name, x, y, w, h, what, size in made:
        o.append('<h3>%s</h3><p class="muted">x %d-%d, y %d-%d (%d x %d tiles). %s. %d KB</p><p><a href="%s.png"><img src="%s.png" alt="%s"></a></p>'
                 % (E(name), x, x + w - 1, y, y + h - 1, w, h, E(what), size // 1024, E(name), E(name), E(name)))
    o.append('<h2>What was placed</h2><p class="muted">Every static placed is in <code>notes/cc-P167-tools/statics-placed.csv</code>; land by id and Z in <code>land-summary.csv</code>; the builder is <code>build_burrows.py</code>, the renders <code>render_burrows.py</code>.</p>')
    o.append('</body></html>')
    text = '\n'.join(o)
    text.encode('ascii')
    open(os.path.join(OUT, 'index.html'), 'w', encoding='ascii', newline='\n').write(text)


if __name__ == '__main__':
    main()
