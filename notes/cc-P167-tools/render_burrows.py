"""cc-P167 / cc-P180 / cc-P181 / cc-P185: renders the scratch Rootdeep Burrows for Chase: one top-down overview
(radar colours, 4 px per tile), an isometric render of each zone, the junction sheets (every wall end, L, T, mixed
join, wall-to-rock join and mounted torch, cropped with its coordinates), a before-and-after sheet per marked
screenshot of Chase's round 3 answer (numbered to match), the pillar, torch and arch checks beside OSI, the OSI
junction references, the wall test rooms beside OSI rooms (walls-check.png), the Stacks beside OSI's Lycaeum
(stacks-check.png), six corners before and after (corners-check.png), the doorway frames (frames-check.png), the
cave-foot test (cave-foot-check.png), the OSI rooms studied (osi-reference.png), and the index page. Round 1 is kept
in round1/, round 2 in round2/, round 3 in round3/. Isometric pictures come from scripts/mapbuild/isorender.py.

    python -P render_burrows.py <scratch folder> [<previous round's scratch folder>] [--page-only]

The second folder (default D:/UO/cc-p167-work/scratch-round3) holds the previous round's map files for the "before"
crops.
"""
import html, json, os, random, shutil, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
import build_burrows  # noqa: E402
from mapbuild import isorender, junctions as J, survey, walls as W  # noqa: E402
from mapbuild.isorender import Scene, render, save, tile_px  # noqa: E402

OUT = r'D:\UO\shard-migration\notes\art\rootdeep-build'
ROUND1 = os.path.join(OUT, 'round1')
ROUND2 = os.path.join(OUT, 'round2')
ROUND3 = os.path.join(OUT, 'round3')
CLIENT = isorender.CLIENT
E = html.escape

# name, x, y, w, h (tiles), what the picture shows
ZONES = [
    ('landing', 5174, 1128, 36, 39, 'The Landing (safe), the arrival, the ankh wall, the Vault doorway at x 5179 with its marble arch, and the tunnel south to the Warren'),
    ('vault', 5138, 1128, 45, 37, 'The Vault (tutorial only): Counting Room, the Stacks with its two bookcase rows, Deposit Hall, the Strongroom with its two solid pillars, the three arched gaps, the crawlway in the south wall at x 5160'),
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
    ('doorway', 'Vault doorway, 5175-5184 x 1133-1142 (run piece before, half arch 0x0116 on the first open tile, pier 0x0115 after)', (5175, 1133, 5184, 1142)),
    ('doorway', 'Thicket gap, 5151-5163 x 1217-1229 (stalagmites on the rock either side)', (5151, 1217, 5163, 1229)),
]
# Chase's marks on the round 3 screenshots (cc-P185): screenshot, mark number, crop rect, what was wrong, the fix
MARKS = [
    ('1-vault', 1, (5147, 1146, 5157, 1157), 'the west Strongroom block (5151-5153 x 1149-1154) read as an open three-sided box', 'ring pieces by the run rule (post, ew, ns, corner at its four corners) and a marble floor at Z 20 on all 18 tiles: a solid plinth (pillar-check.png, variant f)'),
    ('1-vault', 2, (5141, 1139, 5150, 1147), 'Deposit Hall to Strongroom gap: half a tile of nothing between the wall and the pier at 5145,1143', 'the tile before the gap keeps its run piece 0x00F9; the arch top 0x0114 on the first open tile, the pier 0x0113 only after the gap (OSI Nujel\'m row 1323)'),
    ('1-vault', 3, (5163, 1146, 5173, 1157), 'the east Strongroom block (5167-5169 x 1149-1154), the same open box', 'as mark 1'),
    ('1-vault', 4, (5151, 1129, 5159, 1137), 'Stacks to Deposit Hall gap: the pier at 5155,1132 stood half a tile off the north wall', 'run piece 0x00FA at 5155,1132, arch top 0x0116 at 5155,1133, pier 0x0115 at 5155,1135'),
    ('1-vault', 5, (5167, 1129, 5175, 1136), 'the wall torch at 5170,1132 drawn at floor height', 'Z 13 above the floor on the floor tile in front of the north wall (OSI: Deceit, Khaldun and Covetous mount every torch at floor + 13)'),
    ('1-vault', 6, (5175, 1131, 5183, 1141), 'the Vault doorway: the pier at 5179,1136 stood off the wall above it', 'run piece 0x00FA at 5179,1136, arch top 0x0116 at 5179,1137, pier 0x0115 at 5179,1139'),
    ('1-vault', 7, (5176, 1129, 5184, 1136), 'arrow: the Landing torch at 5180,1132 at floor height', 'Z 13'),
    ('2-landing', 1, (5187, 1157, 5199, 1165), 'the tunnel mouth into the Warren: corner pieces at 5191,1161 and 5196,1161 put a slab stub across the end of each wall where it meets the rock', 'a run end takes its plain run piece 0x0242, as OSI ends a wall at rock (Wrong 5686,564; Khaldun 5440,1343)'),
    ('2-landing', 2, (5175, 1132, 5183, 1141), 'the Vault doorway seen from the Landing: the north pier off the wall', 'as 1-vault mark 6'),
    ('2-landing', 3, (5175, 1128, 5185, 1136), 'where the marble Vault wall meets the dungeon brick wall (5179-5180, 1131) and the torch at 5180,1132 at floor height', 'the join is a T (walls W, E and S: the north run continues, ew; the pieces there were already right); the torch at Z 13'),
    ('2-landing', 4, (5187, 1141, 5195, 1149), 'the west stub where the tunnel leaves the Landing: a corner piece at 5191,1145 made a pocket in the mouth', 'walls W and S meet: the NE-corner piece, ew 0x0241 (OSI Deceit 5215,535)'),
    ('2-landing', 5, (5193, 1141, 5201, 1149), 'the east stub at 5196,1145: a corner piece made a pocket in the mouth', 'walls E and S meet: the post 0x0244 (OSI Deceit 5190,562)'),
    ('3-warren-east', 1, (5186, 1157, 5199, 1166), 'the tunnel mouth from the cave side: the stub across the wall end at 5191,1161', 'plain run piece; the rock takes over on the next tile'),
    ('4-tangle', 1, (5162, 1225, 5173, 1234), 'the stone stubs of the descent to the Gloom (5165 and 5170, y 1229) each ended in a corner piece: a slab across the top of the stub into the rock', 'a run end into rock takes the plain run piece 0x01D1 (OSI Khaldun 5440,1340-1343)'),
    ('5-dawnseam', 1, (5210, 1225, 5221, 1234), 'the same at the descent to the Gloom (5213 and 5218, y 1229)', 'plain run piece'),
    ('6-gloom-west', 1, (5179, 1253, 5188, 1261), 'the lair\'s south-west corner at 5183,1257: a corner piece with a stub into the Gloom', 'walls N and E meet: ns 0x01D1 (the SW corner of an outline)'),
    ('6-gloom-west', 2, (5162, 1226, 5174, 1236), 'the descent from the Tangle: stubs at both ends of its walls (5165 and 5170 x 1229 at the rock; 5170,1233 where it opens into the Gloom)', 'run ends plain; 5170,1233 is an L (walls N and E): ns; 5165,1233 keeps its corner (walls N and W)'),
    ('6-gloom-west', 3, (5179, 1233, 5188, 1242), 'the lair\'s north-west corner at 5183,1237: a corner piece put two stubs into the corridor and the west hall', 'walls E and S meet: the post 0x01D2 (the NW corner of an outline; OSI Deceit 5190,562, Khaldun 5392,1320)'),
    ('7-gloom-east', 1, (5210, 1226, 5222, 1236), 'the descent from the Dawnseam: the same stubs', 'as 6-gloom-west mark 2'),
    ('7-gloom-east', 2, (5223, 1233, 5232, 1242), 'the lair\'s north-east corner at 5227,1237: a corner piece with a stub up into the corridor', 'walls W and S meet: ew 0x01D0 (the NE corner)'),
]
SCREENSHOTS = ['1-vault', '2-landing', '3-warren-east', '4-tangle', '5-dawnseam', '6-gloom-west', '7-gloom-east']


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
    W_ = ncol * (cell[0] + gap) + gap
    H = len(rows) * (cell[1] + 18 + gap) + gap
    out = Image.new('RGB', (W_, H), (40, 40, 44))
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


def map_render(folder, rect, art, deco=False, zmax=None, zmin=None):
    x1, y1, x2, y2 = rect
    sc = Scene.from_map(folder, 1, x1, y1, x2, y2)
    if zmax is not None:
        sc.statics = [s for s in sc.statics if s[2] <= zmax]
    if zmin is not None:
        sc.statics = [s for s in sc.statics if s[2] >= zmin]
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
    row = [('round 3: south-facing 0x0A97/0x0A98/0x0A9B only, candelabra ends', map_render(before, r, art)),
           ('round 4: unchanged', map_render(scratch, r, art)),
           ('OSI: the Lycaeum, Moonglow 4284-4296 x 959-981 (map + decoration items)', map_render(CLIENT, (4284, 959, 4296, 981), art, deco=True, zmax=19))]
    return panel_grid([row], cell=(560, 520))


def corners_check(art, scratch, before):
    rows = []
    for kind, title, rect in CORNERS:
        rows.append([('%s, round 3: %s' % (kind, title), map_render(before, rect, art)),
                     ('%s, round 4' % kind, map_render(scratch, rect, art))])
    return panel_grid(rows, cell=(560, 440))


def frames_check(scenes, art, scratch):
    rows = [[('test room: marble gap in a north-south wall (run piece before, 0x0116 half arch on the first open tile, 0x0115 pier after)', scene_render(scenes, 'marble gap N-S wall', art)),
             ('test room: marble gap in an east-west wall (run piece before, 0x0114 half arch, 0x0113 pier after)', scene_render(scenes, 'marble gap E-W wall', art)),
             ('OSI: Nujel\'m 3728-3742 x 1319-1327, the arcade: wall end, 0x0114, open, 0x0113, 0x0114, open, 0x0113 (roof left off)', map_render(CLIENT, (3728, 1319, 3742, 1327), art, zmax=19))],
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


# ------------------------------------------------------------------------------------------------ cc-P185 pictures

def marks_sheet(shot, art, scratch, before):
    rows = []
    for s, n, rect, wrong, fix in MARKS:
        if s != shot:
            continue
        rows.append([('%s mark %d, round 3: %s' % (s, n, wrong), map_render(before, rect, art)),
                     ('mark %d, round 4: %s' % (n, fix), map_render(scratch, rect, art))])
    return panel_grid(rows, cell=(540, 430))


def pillar_check(rules, art):
    """The Strongroom pillar seven ways in a marble test room; f was picked (no floor shows, and it is how every UO
    building reads from above: walls with the next storey's floor on them)."""
    ws = rules['wallSets']['marble']

    def room(variant):
        block = {(x, y) for x in range(5, 8) for y in range(4, 10)}
        fl = {(x, y) for x in range(0, 13) for y in range(0, 14)} - block
        ring = W.ring_of(fl)
        if variant.startswith('a'):
            F = lambda c: c in fl
            statics = [(x, y, 0, tid, role) for (x, y) in sorted(ring) for tid, role in W.wall_pieces_p180(F, x, y, ws)]
        else:
            statics, ring = W.walls_for(fl, set(), ws)
        land = {c: (0x0486, 0) for c in fl | ring}
        if variant.startswith('b'):
            for c in block - ring:
                statics.append((c[0], c[1], 0, 0x00F8, 'fill'))
        elif variant.startswith('c'):
            statics = [s for s in statics if (s[0], s[1]) not in block] + [(c[0], c[1], 0, 0x00F8, 'fill') for c in block]
        elif variant.startswith('d'):
            statics = [s for s in statics if (s[0], s[1]) not in block] + [(c[0], c[1], 0, 0x011B, 'col') for c in block]
        elif variant.startswith('e'):
            for c in block - ring:
                land[c] = (0x0244, 0)
        elif variant.startswith('f'):
            statics += [(c[0], c[1], 20, 0x0495, 'top') for c in block]
        elif variant.startswith('g'):
            statics = [s for s in statics if (s[0], s[1]) not in block] + [(c[0], c[1], 0, 0x011B, 'col') for c in block & ring] + [(c[0], c[1], 20, 0x0495, 'top') for c in block]
        xs = [c[0] for c in land]
        ys = [c[1] for c in land]
        for x in range(min(xs) - 1, max(xs) + 2):
            for y in range(min(ys) - 1, max(ys) + 2):
                land.setdefault((x, y), (0x0244, 0))
        return render(Scene(land, [(x, y, z, t) for (x, y, z, t, r) in statics]), 3, 2, 10, 12, art)
    variants = ['a: round 3 (P180 floor rule: corner pieces at all four corners, floor showing inside)',
                'b: ring by the run rule + corner pieces on the inside tiles (a crate)',
                'c: every block tile a corner piece (a lattice)',
                'd: marble columns 0x011B on every block tile (a colonnade, not a pillar)',
                'e: ring by the run rule, the land inside void (a pit)',
                'f: PICKED. ring by the run rule (post / ew / ns / corner) + marble floor at Z 20 on every block tile (a solid plinth)',
                'g: columns on the ring tiles + floor at Z 20 (a canopy)']
    rows = [[(v, room(v)) for v in variants[:4]], [(v, room(v)) for v in variants[4:]]]
    return panel_grid(rows, cell=(420, 380))


def torch_check(art, scratch, before):
    rows = [[('round 3: Counting Room torch 5170,1132 at Z 0 (5167-5175 x 1129-1136)', map_render(before, (5167, 1129, 5175, 1136), art)),
             ('round 4: the same torch at Z 13 on the floor tile in front of the north wall', map_render(scratch, (5167, 1129, 5175, 1136), art)),
             ('round 4: Vault west torches 0x0A07 at 5142,1144 and 5142,1159 (west wall), Z 13', map_render(scratch, (5140, 1141, 5148, 1162), art))],
            [('OSI: Deceit 5156-5164 x 560-568, wall torch 0x0A07 at 5160,564 on the west wall, Z 15 over floor 0', map_render(CLIENT, (5156, 560, 5164, 568), art)),
             ('OSI: Khaldun 5452-5460 x 1295-1303, wall torch 0x0A05 at 5456,1299 (west wall), Z 13', map_render(CLIENT, (5452, 1295, 5460, 1303), art)),
             ('OSI: Khaldun 5442-5450 x 1316-1324, wall torch 0x0A0A at 5447,1320 (north wall), Z 13', map_render(CLIENT, (5442, 1316, 5450, 1324), art))]]
    return panel_grid(rows, cell=(480, 420))


def arch_check(art, scratch, before):
    rows = [[('round 3: Deposit Hall to Strongroom gap, pier on the tile before (5145,1143): half a tile of nothing', map_render(before, (5141, 1139, 5150, 1147), art)),
             ('round 4: run piece before, 0x0114 on the first open tile, 0x0113 after', map_render(scratch, (5141, 1139, 5150, 1147), art)),
             ('OSI: Nujel\'m row 1323, x 3728-3742: wall end 0x0105, 0x0114, open, 0x0113, 0x0114, open, 0x0113 (roof off)', map_render(CLIENT, (3728, 1319, 3742, 1327), art, zmax=19))],
            [('round 3: Stacks to Deposit Hall gap, pier at 5155,1132 off the north wall', map_render(before, (5151, 1129, 5159, 1137), art)),
             ('round 4: run piece at 5155,1132, 0x0116 at 5155,1133, 0x0115 at 5155,1135', map_render(scratch, (5151, 1129, 5159, 1137), art)),
             ('OSI: Magincia column 3716, y 2058-2072: 0x011B, 0x0116, open, 0x0115, 0x0116, open, 0x0115 ... (roof off)', map_render(CLIENT, (3712, 2058, 3720, 2072), art, zmax=19))]]
    return panel_grid(rows, cell=(480, 420))


def osi_junctions(art):
    rows = [[('OSI Deceit 5210-5220 x 531-541: a wall turning at 5215,535 with floor north and east takes ew (walls W and S meet), the NW corner at 5215,540 the post', map_render(CLIENT, (5210, 531, 5220, 541), art)),
             ('OSI Deceit 5180-5194 x 536-546: the interior wall from the west meets the east wall at 5184,539 with the corner piece (walls N, S, W)', map_render(CLIENT, (5180, 536, 5194, 546), art)),
             ('OSI Deceit 5186-5194 x 562-570: a corridor leaving a room: the stubs 5190,562 post (walls E, S) and the run ends plain', map_render(CLIENT, (5186, 560, 5194, 570), art))],
            [('OSI Wrong 5682-5698 x 560-568: dungeon walls run into cave rock with the plain run piece (5686,564; 5694,563), no corner', map_render(CLIENT, (5682, 558, 5698, 568), art)),
             ('OSI Khaldun 5436-5452 x 1315-1323: a stone wall along the rock foot, ends plain (5440,1319 is a run end)', map_render(CLIENT, (5436, 1315, 5452, 1323), art)),
             ('OSI Khaldun 5436-5444 x 1340-1346: a stone wall ending at rock with 0x01D1 at 5440,1343', map_render(CLIENT, (5436, 1338, 5444, 1346), art))],
            [('OSI Despise 5380-5392 x 674-696: a dungeon-brick room cut into rock; the NE corner 5389,678 ew, the SE corner 5389,693 corner', map_render(CLIENT, (5380, 674, 5392, 696), art)),
             ('OSI Terathan Keep 5440-5447 x 3128-3137 (Z -60 storey): the T at 5444,3131 (walls W, N, S: ns) and 5444,3135 (walls N, E, S: ns)', map_render(CLIENT, (5440, 3128, 5447, 3137), art, zmax=-41)),
             ('OSI Nujel\'m 3680-3689 x 1244-1250: marble walls meeting at 3682,1244 (corner) and 3686,1244 (ns)', map_render(CLIENT, (3680, 1242, 3689, 1250), art, zmax=19))]]
    return panel_grid(rows, cell=(480, 420))


def main():
    folder = sys.argv[1]
    if '--page-only' in sys.argv:
        made = [(name, x, y, w, h, what, os.path.getsize(os.path.join(OUT, '%s.png' % name))) for name, x, y, w, h, what in ZONES]
        junction_files = sorted(f for f in os.listdir(OUT) if f.startswith('junctions-'))
        page(made, junction_files)
        return
    before = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else 'D:/UO/cc-p167-work/scratch-round3'
    rules = json.load(open(os.path.join(HERE, 'plan-sets.json'), encoding='utf-8'))
    art = isorender.Art()
    # keep round 3 beside the new pictures (rounds 1 and 2 are already in their folders)
    if not os.path.isdir(ROUND3):
        os.makedirs(ROUND3)
        for name in os.listdir(OUT):
            if name.endswith('.png') or name == 'index.html':
                shutil.move(os.path.join(OUT, name), os.path.join(ROUND3, name))
    made = []
    x, y, w, h = OVERVIEW
    radar_overview(folder, x, y, w, h).save(os.path.join(OUT, 'overview.png'), optimize=True)
    for name, x, y, w, h, what in ZONES:
        sc = Scene.from_map(folder, 1, x, y, x + w - 1, y + h - 1)
        im = render(sc, x, y, x + w - 1, y + h - 1, art)
        size = save(im, os.path.join(OUT, '%s.png' % name))
        made.append((name, x, y, w, h, what, size))
        print(name, im.size, size, flush=True)
    # the junction sheets, from the wall layer of the plan
    layout = json.load(open(build_burrows.LAYOUT, encoding='utf-8'))
    spawners, pts = build_burrows.read_points()
    land, statics, stats, counts, floor, opening, walls, report = build_burrows.plan(layout, rules, spawners, pts, quiet=True)
    junctions = J.find_junctions(report['wall tiles'], report['rock tiles'], statics)
    for name in os.listdir(OUT):
        if name.startswith('junctions-'):
            os.remove(os.path.join(OUT, name))
    sheets = J.sheets(folder, junctions, os.path.join(OUT, 'junctions'), art)
    for path, n, size in sheets:
        print(os.path.basename(path), n, 'crops', size, flush=True)
    print('junctions:', len(junctions), J.summary(junctions))
    scenes = build_burrows.test_room_scenes(rules)
    scenes.update(build_burrows.cave_test_scenes(rules))
    checks = {}
    for shot in SCREENSHOTS:
        checks['marks-%s.png' % shot] = marks_sheet(shot, art, folder, before)
    checks.update({
        'pillar-check.png': pillar_check(rules, art),
        'torch-check.png': torch_check(art, folder, before),
        'arch-check.png': arch_check(art, folder, before),
        'junction-osi.png': osi_junctions(art),
        'stacks-check.png': stacks_check(art, folder, before),
        'corners-check.png': corners_check(art, folder, before),
        'frames-check.png': frames_check(scenes, art, folder),
        'cave-foot-check.png': cave_foot_check(scenes, art),
        'walls-check.png': walls_check(scenes, art, folder),
        'lair-mouth-check.png': mouth_check(scenes, art, folder),
        'osi-reference.png': osi_reference(art),
    })
    for name, im in checks.items():
        print(name, save(im, os.path.join(OUT, name)), flush=True)
    page(made, [os.path.basename(p) for p, n, s in sheets])
    for name in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, name)
        if os.path.isfile(p):
            print('%8d  %s' % (os.path.getsize(p), name))


def page(made, junction_files):
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
         '<h1>Rootdeep Burrows: the build, rendered from the scratch map (round 4)</h1>',
         '<p class="muted">cc-P185, 2026-10-19. P141\'s approved layout built into a scratch copy of Trammel (outside both repos); nothing has touched the real map files. '
         'Drawn by scripts/mapbuild/isorender.py from the real tiles with the client\'s layout (no hues, no lighting). '
         'Round 1 (2026-10-18) is in <a href="round1/index.html">round1/</a>, round 2 in <a href="round2/index.html">round2/</a>, round 3 (the one you marked) in <a href="round3/index.html">round3/</a>.</p>',
         '<div class="ask"><b>Approve these renders, or say what to change.</b><br>'
         'Your marks on round 3 were: spaces next to the archways, torches too low, bad corners in the centre of the Vault, and the odd corners at wall ends, '
         'stubs and junctions in every zone. What changed: '
         '(1) <b>Junctions</b>: the piece a wall tile takes now comes from the runs meeting at it (which neighbours are wall tiles), measured on 9,744 OSI wall tiles in nine dungeons: '
         'a run\'s free end takes its plain piece, the four corners of an outline take post / ew / ns / corner, a T takes the through run\'s piece. 23 tiles changed; every mark you drew is one of them or a torch, pier or pillar. '
         '(2) <b>Torches</b> sit at Z 13 above the floor on the floor tile in front of the wall, as every OSI dungeon torch does. '
         '(3) <b>Arches</b>: the wall before a gap keeps its run piece, the arch top goes on the first open tile and the pier only on the wall tile after, which is OSI\'s bay (Nujel\'m, Magincia); the half-tile gaps are gone. '
         '(4) <b>The Strongroom pillars</b> are solid plinths: the walled ring with a marble floor at wall height on top (seven variants below; f picked). '
         'The walkable floor, the 18 openings, the crawlway and all 1,614 wall tiles are exactly round 3\'s (the builder refuses to write otherwise).</div>',
         '<h2>Your marks, before and after (numbered as on your screenshots)</h2>']
    for shot in SCREENSHOTS:
        marks = [(n, wrong, fix) for s, n, rect, wrong, fix in MARKS if s == shot]
        o.append('<h3>%s.png</h3><table><tr><th>Mark</th><th>What was wrong</th><th>The fix</th></tr>' % E(shot))
        for n, wrong, fix in marks:
            o.append('<tr><td>%d</td><td>%s</td><td>%s</td></tr>' % (n, E(wrong), E(fix)))
        o.append('</table><p><a href="marks-%s.png"><img src="marks-%s.png" alt="marks %s"></a></p>' % (E(shot), E(shot), E(shot)))
    o.append('<h2>The junction sheet: every wall end, L, T, mixed join, wall-to-rock join and torch, as built</h2>')
    o.append('<p class="muted">Made from the wall layer by scripts/mapbuild/junctions.py; the red diamond is the tile named in the caption. The builder reviewed every crop before this page was written (the count and what was fixed are in notes/cc-P185-cont-rootdeep-round4.md).</p>')
    for f in junction_files:
        o.append('<p><a href="%s"><img src="%s" alt="%s"></a></p>' % (E(f), E(f), E(f)))
    o += ['<h2>The Strongroom pillar: seven ways, f picked</h2>',
          '<p><a href="pillar-check.png"><img src="pillar-check.png" alt="pillar check"></a></p>',
          '<h2>Torches: ours beside OSI\'s</h2>',
          '<p class="muted">Every wall torch in Deceit, Khaldun, Covetous, Hythloth and the Terathan Keep stands on the floor tile in front of its wall, 13 to 15 above the floor, facing a wall directly north or west of it (150 of 150 in the surveyed blocks; 16 measured for Z).</p>',
          '<p><a href="torch-check.png"><img src="torch-check.png" alt="torch check"></a></p>',
          '<h2>Arches: ours beside OSI\'s bay</h2>',
          '<p><a href="arch-check.png"><img src="arch-check.png" alt="arch check"></a></p>',
          '<h2>The OSI junctions the rule came from</h2>',
          '<p><a href="junction-osi.png"><img src="junction-osi.png" alt="OSI junctions"></a></p>',
          '<h2>Round 3 and round 4 side by side: the Vault</h2>',
          '<table class="pair"><tr><th>Round 3</th><th>Round 4</th></tr><tr><td><a href="round3/vault.png"><img src="round3/vault.png" alt="vault round 3"></a></td><td><a href="vault.png"><img src="vault.png" alt="vault round 4"></a></td></tr></table>',
          '<h2>Round 3 and round 4 side by side: the Landing</h2>',
          '<table class="pair"><tr><th>Round 3</th><th>Round 4</th></tr><tr><td><a href="round3/landing.png"><img src="round3/landing.png" alt="landing round 3"></a></td><td><a href="landing.png"><img src="landing.png" alt="landing round 4"></a></td></tr></table>',
          '<h2>Corners: six before and after (round 3, round 4)</h2>',
          '<p><a href="corners-check.png"><img src="corners-check.png" alt="corners check"></a></p>',
          '<h2>Doorway frames</h2>',
          '<p class="muted">Marble: the wall tile before the gap keeps its run piece, the half arch 0x0114/0x0116 goes on the first open tile, the pier 0x0113/0x0115 replaces the run piece on the wall tile after the gap (Nujel\'m row 1323 and column 3682; Magincia column 3716). Stone (the lair mouth): 0x01D8 on the first open tile, 0x01D9 after (Terathan Keep column 5431). Cave gaps: a stalagmite or crystal on the rock either side. Passages between two floors (the Brood Pit mouth, the tunnels) have no wall line and stay plain.</p>',
          '<p><a href="frames-check.png"><img src="frames-check.png" alt="frames check"></a></p>',
          '<h2>The Stacks (unchanged since round 3) and OSI\'s library</h2>',
          '<p><a href="stacks-check.png"><img src="stacks-check.png" alt="stacks check"></a></p>',
          '<h2>The cave foot: what was tried (unchanged)</h2>',
          '<p><a href="cave-foot-check.png"><img src="cave-foot-check.png" alt="cave foot check"></a></p>',
          '<h2>Walls check: our test rooms beside OSI rooms of the same set</h2>',
          '<p><a href="walls-check.png"><img src="walls-check.png" alt="walls check"></a></p>',
          '<h2>The lair mouth (a), as approved</h2>',
          '<p><a href="lair-mouth-check.png"><img src="lair-mouth-check.png" alt="lair mouth"></a></p>',
          '<h2>The OSI rooms the corner rules came from</h2>',
          '<p><a href="osi-reference.png"><img src="osi-reference.png" alt="OSI reference rooms"></a></p>',
          '<h2>Overview (top-down, radar colours, 4 px per tile; x 5120-5263, y 1112-1279)</h2><p><a href="overview.png"><img src="overview.png" alt="top-down overview"></a></p>',
          '<h2>Zones (isometric, real tiles)</h2>']
    for name, x, y, w, h, what, size in made:
        o.append('<h3>%s</h3><p class="muted">x %d-%d, y %d-%d (%d x %d tiles). %s. %d KB</p><p><a href="%s.png"><img src="%s.png" alt="%s"></a></p>'
                 % (E(name), x, x + w - 1, y, y + h - 1, w, h, E(what), size // 1024, E(name), E(name), E(name)))
    o.append('<h2>What was placed</h2><p class="muted">Every static placed is in <code>notes/cc-P167-tools/statics-placed.csv</code>; land by id and Z in <code>land-summary.csv</code>; the rules (seeds, weights, clusters, corners, frames, torches, the pillar top) in <code>plan-sets.json</code>; the builder is <code>build_burrows.py</code> on <code>scripts/mapbuild/</code> (the wall rule in <code>walls.py</code>, the junction sheet in <code>junctions.py</code>), the renders <code>render_burrows.py</code>; the checklist, the mark table and the OSI measurements in <code>notes/cc-P185-cont-rootdeep-round4.md</code>.</p>')
    o.append('</body></html>')
    text = '\n'.join(o)
    text.encode('ascii')
    open(os.path.join(OUT, 'index.html'), 'w', encoding='ascii', newline='\n').write(text)


if __name__ == '__main__':
    main()
