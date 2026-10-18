"""cc-P166: the paperdoll head, bald and with the kit's hair, with the ears of our gump moved down by DY rows.
    python -P pd_ears.py OUT.png [--dys 0,2,3,4] [--gump PNG ...]
Rows: female (64783 on body 13, hair 60701), male (54783 on 12, hair 50701); per DY: bald | hair."""
import argparse, os
import numpy as np
from PIL import Image, ImageDraw
V = r'D:\ShatteredLegacy\player-package\vendor'
EAR_ROWS = 45   # gump rows above this are the ears (the tail starts far below)


def rgba(p):
    return np.array(Image.open(p).convert('RGBA'))


def over(dst, src):
    a = src[..., 3:4] > 0
    return np.where(a, src, dst)


def moved_ears(g, dy):
    out = g.copy()
    ears = g.copy(); ears[EAR_ROWS:] = 0
    out[:EAR_ROWS] = 0
    sh = np.zeros_like(g); sh[dy:] = ears[:g.shape[0] - dy] if dy else ears
    return over(out, sh)


ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--dys', default='0,2,3,4')
ap.add_argument('--female'); ap.add_argument('--male')
a = ap.parse_args()
rows = []
for sex, gump, body, hair, src in (('F', '64783', '13', '60701', a.female), ('M', '54783', '12', '50701', a.male)):
    g = rgba(src or os.path.join(V, 'shattered-legacy-art', 'gumps', gump + '.png'))
    b = rgba(os.path.join(V, 'paperdoll-sos', 'bodies-sfw', body + '.png'))
    h = rgba(os.path.join(V, 'paperdoll-sos', 'ExternalImages', 'gumps', hair + '.png'))
    cells = []
    for dy in [int(x) for x in a.dys.split(',')]:
        e = moved_ears(g, dy)
        bg = np.zeros_like(b); bg[...] = (40, 34, 30, 255)
        for withhair in (False, True):
            c = over(bg, b)
            if withhair:
                c = over(c, h)
            c = over(c, e)
            cells.append(c[15:75, 65:120])
    rows.append(np.concatenate(cells, 1))
im = Image.fromarray(np.concatenate(rows, 0)).convert('RGB')
im = im.resize((im.width * 4, im.height * 4), Image.NEAREST)
d = ImageDraw.Draw(im)
for i, dy in enumerate(a.dys.split(',')):
    d.text((i * 2 * 55 * 4 + 4, 2), 'down %s: bald | hair' % dy, fill=(255, 255, 0))
im.save(a.out)
