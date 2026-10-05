# P59, read-only render of the Part A sheet and the four Part C line sheets.
from p59anim import *
from PIL import Image, ImageDraw, ImageFont
import json

OUT = os.path.dirname(os.path.abspath(__file__))
TP = 'D:/UO/third-party/'
FONT = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 13)
FONTB = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 14)
BG = (214, 214, 206)

VD = {
    'KR Wolf': TP + 'kr-wolf/Wolf.vd',
    'Cerberus': TP + 'cerberus/Cerberus.vd',
    'L_Fox': TP + 'mobile-megapack/Mobile Pack/L_Fox.vd',
    'L_Bird 01': TP + 'mobile-megapack/Mobile Pack/L_Bird 01.vd',
    'L_Bird 02': TP + 'mobile-megapack/Mobile Pack/L_Bird 02.vd',
    'L_Griffin': TP + 'mobile-megapack/Mobile Pack/L_Griffin.vd',
}

def body_pair(b):
    sa, wa = stand_walk(b)
    st = frame_img(b, sa, 1, 0)
    wk = frame_img(b, wa, 1, 2)
    return st, wk

def vd_pair(path):
    v = vd_load(path)
    st = [f for f in v['block'](STAND[v['type']] * 5 + 1) if f]
    wk = [f for f in v['block'](0 * 5 + 1) if f]
    return (to_img(st[0]) if st else None), (to_img(wk[min(2, len(wk) - 1)]) if wk else None)

def bulk(im):
    return sum(1 for p in im.getdata() if p[3]) if im else 0

def sheet(items, path, scale, title):
    """items: list of (label lines, stand img, walk img). Stand on top, walk below, bottoms aligned."""
    cells = []
    for lab, st, wk in items:
        st = st.resize((st.width * scale, st.height * scale), Image.NEAREST)
        wk = wk.resize((wk.width * scale, wk.height * scale), Image.NEAREST) if wk else None
        tw = max(FONT.getlength(l) for l in lab) + 6
        cells.append((lab, st, wk, int(max(st.width, wk.width if wk else 0, tw)) + 14))
    hs = max(c[1].height for c in cells); hw = max((c[2].height if c[2] else 0) for c in cells)
    W = max(sum(c[3] for c in cells) + 20, int(FONTB.getlength(title)) + 30)
    H = 34 + hs + 12 + hw + 12 + 17 * max(len(c[0]) for c in cells) + 10
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((10, 8), title, font=FONTB, fill=(0, 0, 0))
    x = 10
    for lab, st, wk, w in cells:
        im.paste(st, (x + (w - st.width) // 2, 34 + hs - st.height), st)
        if wk: im.paste(wk, (x + (w - wk.width) // 2, 34 + hs + 12 + hw - wk.height), wk)
        y = 34 + hs + 12 + hw + 10
        for k, l in enumerate(lab):
            d.text((x + 4, y + 17 * k), l, font=FONTB if k == 0 else FONT, fill=(0, 0, 0) if k == 0 else (60, 60, 60))
        d.line((x + w - 2, 30, x + w - 2, H - 6), fill=(185, 185, 178))
        x += w
    im.save(path)
    return im.size

def build(entries, path, scale, title, sort=True):
    items = []
    for e in entries:
        if isinstance(e[0], int):
            st, wk = body_pair(e[0])
        else:
            st, wk = vd_pair(VD[e[0]])
        if st is None: continue
        items.append((bulk(st), e[1], st, wk))
    if sort: items.sort(key=lambda x: x[0])
    return sheet([(lab, st, wk) for _, lab, st, wk in items], path, scale, title), [(l[0], n) for n, l, _, _ in items]

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    A = [(0xD9, ['217 0xD9', 'Dog']), (225, ['225', 'Timber Wolf']), (25, ['25', 'Grey Wolf', '=225 hue 946']),
         (27, ['27', 'Grey Wolf', '=225 hue 947']), (34, ['34', 'White Wolf', '=225 hue 2301']),
         (37, ['37', 'White Wolf', '=225 hue 1154']), (23, ['23', 'Dire Wolf', '=225 hue 2305']),
         (98, ['98', 'Hell Hound', '=225 hue 1643']), (277, ['277', 'Cu Sidhe']),
         (0xC9, ['201 0xC9', 'Cat / Hellcat']), (63, ['63', 'Cougar', '=214 hue 0']), (0xD6, ['214 0xD6', 'Panther']),
         (64, ['64', 'Snow Leopard', '=214 hue 2301']), (65, ['65', 'Snow Leopard', '=214 hue 2301']),
         (127, ['127', 'Predator Hellcat', '=214 hue 1652']),
         (6, ['6', 'Bird']), (5, ['5', 'Eagle / Phoenix']), (254, ['254', 'Crane']), (243, ['243', 'Lesser Hiryu']),
         (246, ['246', 'Bake Kitsune']),
         ('KR Wolf', ['KR Wolf.vd', 'third-party']), ('Cerberus', ['Cerberus.vd', 'third-party']),
         ('L_Fox', ['L_Fox.vd', 'third-party']), ('L_Bird 01', ['L_Bird 01.vd', 'third-party']),
         ('L_Bird 02', ['L_Bird 02.vd', 'third-party']), ('L_Griffin', ['L_Griffin.vd', 'third-party'])]
    print(build(A, os.path.join(OUT, 'partA-candidates-1x.png'), 1,
                'P59 Part A: brief candidates, true scale (1x). Top: stand, frame 0. Bottom: walk, frame 2. Direction: south.',
                sort=False))

    U = ' (unused)'
    DOG = [(217, ['217', 'Dog']), (225, ['225', 'Timber Wolf', '(also 23,25,27,34,37,98)']),
           (277, ['277', 'Cu Sidhe']), (1069, ['1069', 'Ancient Hellhound', 'unused']),
           (1410, ['1410', 'Windrunner', 'unused']), (1546, ['1546', 'Newfoundland', 'unused']),
           (1547, ['1547', 'Alaskan Malamute', 'unused']), (1548, ['1548', 'Great Dane', 'unused']),
           (1549, ['1549', 'Saint Bernard', 'unused']), (1551, ['1551', 'Black Russian', 'Terrier, unused']),
           (1552, ['1552', 'Rottweiler', 'unused']), (1576, ['1576', 'Orc Hellhound', 'unused']),
           (739, ['739', 'Leather Wolf', 'unused']), (719, ['719', 'Dragon Wolf', 'unused']),
           ('KR Wolf', ['KR Wolf.vd', 'third-party']), ('Cerberus', ['Cerberus.vd', 'third-party'])]
    CAT = [(201, ['201', 'Cat / Hellcat']), (214, ['214', 'Panther', '(also 63,64,65,127)']),
           (1309, ['1309', 'Baby Tiger', 'unused']), (1254, ['1254', 'Tiger', 'unused']),
           (1255, ['1255', 'Tiger (ethereal', 'slot), unused']), (1416, ['1416', 'Sabertooth', 'unused']),
           (1426, ['1426', 'Lion', 'unused']), (1441, ['1441', 'Undead Tiger', 'unused']),
           (1553, ['1553', 'Manticore', 'unused']), (1573, ['1573', 'Manticore_L', 'unused'])]
    FOX = [(279, ['279', 'Ferret']), (1423, ['1423', 'Fox_Small', 'unused']), (246, ['246', 'Bake Kitsune']),
           ('L_Fox', ['L_Fox.vd', 'third-party'])]
    BIRD = [(6, ['6', 'Bird']), (5, ['5', 'Eagle / Phoenix']), (254, ['254', 'Crane']), (243, ['243', 'Lesser Hiryu', '/ Hiryu']),
            (282, ['282', 'Parrot', 'unused']), (283, ['283', 'Crow', 'unused']), (831, ['831', 'Parrot Bird']),
            (832, ['832', 'Phoenix Bird', 'unused']), (208, ['208', 'Chicken']), (1026, ['1026', 'Uber Turkey', 'unused']),
            (1440, ['1440', 'Peacock', 'unused']), (30, ['30', 'Harpy']),
            ('L_Bird 01', ['L_Bird 01.vd', 'third-party']), ('L_Bird 02', ['L_Bird 02.vd', 'third-party']),
            ('L_Griffin', ['L_Griffin.vd', 'third-party'])]
    for name, ents in (('dog', DOG), ('cat', CAT), ('fox', FOX), ('bird', BIRD)):
        print(name, build(ents, os.path.join(OUT, f'sheet-{name}.png'), 2,
                          f'P59 {name} line: every distinct body, 2x, sorted small to large by pixel count. '
                          'Top: stand. Bottom: walk. Direction: south. Client data 7.0.117.0.'))
