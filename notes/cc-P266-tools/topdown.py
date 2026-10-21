# cc-P266 read only: a top-down plan of New Haven with every winter row marked (the prompt's "top-down preview
# image"). One square per tile, north up: roads and plazas grey, grass green, water blue, walls and blocking statics
# dark, buildings' floors at their height tan; rows as coloured squares with a legend (tree, light, garland, snow,
# presents and toys, calendar, OSI pieces), new rows ringed in magenta. Writes topdown.png here and the copy Chase
# gets in notes/art/winter-decor/.
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, '..', 'cc-P237-tools'))
import nhbase as B
import art_src as S
from PIL import Image, ImageDraw, ImageFont

F = B.Facet(1)
X0, Y0, X1, Y1 = 3410, 2480, 3545, 2640
T = 7   # pixels per tile
WATER = ('water',)
GRASS = ('grass', 'forest', 'jungle', 'furrows', 'snow', 'dirt')

KIND = {}
for first, key, what, pack, files, how in S.GROUPS:
    k = 'tree' if key.startswith('tree') else 'light' if key in ('candle-tall', 'candle-short', 'antler', 'advent') else \
        'garland' if key.startswith('ribbon') else 'calendar' if key.startswith('calendar') else 'toys'
    for i in range(first, first + len(files)): KIND[i] = k
for i in (0x3C52, 0x2377): KIND[i] = 'tree'
for i in (0x3C45, 0x3C4A, 0x3C4E, 0x3C60): KIND[i] = 'light'
for i in (0x3C61, 0x3C62, 0x232C, 0x232D, 0x2374, 0x2375, 0x3C57, 0x3C58): KIND[i] = 'garland'
for i in (0x08E2, 0x08E0, 0x08E6, 0x08E5, 0x08E3, 0x3C6B, 0x3C6C, 0x3C6D, 0x2328): KIND[i] = 'snow'
for i in (0x3C53, 0x3C54, 0x3C55, 0x3C56, 0x3C6E, 0x3C40): KIND[i] = 'toys'
COLOUR = {'tree': (30, 160, 50), 'light': (255, 200, 40), 'garland': (220, 40, 60), 'snow': (240, 240, 255),
          'calendar': (200, 120, 255), 'toys': (255, 120, 40), 'other': (180, 180, 180)}


def ground_colour(x, y):
    g = F.avgz(x, y)
    lid, lz = F.land(x, y)
    ln = B.lname(lid).lower()
    st = F.statics(x, y)
    if any(B.iflags(s) & B.WALL for s, z in st): return (60, 50, 45)
    roofed = any(B.iflags(s) & B.ROOF for s, z in st)
    floor = any(B.iflags(s) & B.SURF and not B.iflags(s) & B.WET and z >= g for s, z in st)
    if any(w in ln for w in WATER) or any(B.iflags(s) & B.WET for s, z in st): return (70, 110, 180)
    if roofed: return (150, 120, 90)
    if floor: return (190, 170, 140)
    if B.walkway(F, x, y, g): return (140, 140, 140)
    if any(B.iflags(s) & B.IMP for s, z in st): return (70, 90, 60)
    if any(w in ln for w in GRASS): return (90, 150, 70)
    return (120, 130, 110)


def main(out=None):
    rows = json.load(open(os.path.join(HERE, 'placement.json')))
    W, H = (X1 - X0 + 1) * T, (Y1 - Y0 + 1) * T
    im = Image.new('RGB', (W + 230, H + 40), (20, 20, 30))
    d = ImageDraw.Draw(im)
    for y in range(Y0, Y1 + 1):
        for x in range(X0, X1 + 1):
            c = ground_colour(x, y)
            px, py = (x - X0) * T, (y - Y0) * T + 30
            d.rectangle((px, py, px + T - 1, py + T - 1), fill=c)
    try: f = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 12)
    except Exception: f = ImageFont.load_default()
    for x in range(X0 - X0 % 10 + 10, X1 + 1, 10):
        px = (x - X0) * T
        d.line((px, 30, px, H + 30), fill=(0, 0, 0), width=1)
        d.text((px + 2, 16), str(x), fill=(230, 230, 230), font=f)
    for y in range(Y0 - Y0 % 10 + 10, Y1 + 1, 10):
        py = (y - Y0) * T + 30
        d.line((0, py, W, py), fill=(0, 0, 0), width=1)
        d.text((2, py + 1), str(y), fill=(230, 230, 230), font=f)
    for k, r in enumerate(rows):
        kind = KIND.get(r['itemId'], 'other')
        px, py = (r['x'] - X0) * T, (r['y'] - Y0) * T + 30
        d.rectangle((px, py, px + T - 1, py + T - 1), fill=COLOUR[kind], outline=(255, 0, 255) if k >= 61 else (0, 0, 0))
    lx = W + 12
    d.text((lx, 34), 'New Haven winter decor', fill=(255, 255, 255), font=f)
    d.text((lx, 50), '%d rows: %d of P34, %d new' % (len(rows), 61, len(rows) - 61), fill=(230, 230, 230), font=f)
    yy = 76
    for kind, name in (('tree', 'trees (lit)'), ('light', 'candles, firepit, stoves'), ('garland', 'garlands, wreaths, arches'),
                       ('snow', 'snow, snowman'), ('toys', 'presents, toys, statue'), ('calendar', 'advent calendar'), ('other', 'other')):
        d.rectangle((lx, yy, lx + 12, yy + 12), fill=COLOUR[kind], outline=(0, 0, 0))
        d.text((lx + 18, yy - 1), name, fill=(230, 230, 230), font=f); yy += 18
    d.rectangle((lx, yy, lx + 12, yy + 12), fill=(90, 90, 90), outline=(255, 0, 255)); d.text((lx + 18, yy - 1), 'magenta ring: new in P266', fill=(230, 230, 230), font=f); yy += 24
    for col, name in (((140, 140, 140), 'road, plaza, pier'), ((90, 150, 70), 'grass'), ((150, 120, 90), 'under a roof'), ((190, 170, 140), 'floor, deck'), ((60, 50, 45), 'wall'), ((70, 110, 180), 'water')):
        d.rectangle((lx, yy, lx + 12, yy + 12), fill=col); d.text((lx + 18, yy - 1), name, fill=(230, 230, 230), font=f); yy += 18
    yy += 8
    for area, where in (('bank', 'x3478-3493, y2564-2581'), ('square', 'x3496-3516, y2566-2586'), ('inn', 'x3492-3510, y2512-2526'), ('healer hall', 'x3452-3463, y2545-2555'),
                        ('field office', 'x3453-3464, y2594-2603'), ('docks', 'x3486-3524, y2592-2612')):
        d.text((lx, yy), '%s: %s' % (area, where), fill=(200, 200, 200), font=f); yy += 16
    out = out or os.path.join(HERE, 'topdown.png')
    im.save(out, optimize=True)
    print(out, im.size)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
