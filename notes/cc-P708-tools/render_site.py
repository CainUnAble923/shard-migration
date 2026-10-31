"""cc-P708: renders a site on the SoS land the hall checks read (make_sosclient.py), with the statics above a cut Z left
out (to see into a building), a coordinate tick every 5 tiles, and lettered marks.
    python -P render_site.py x1 y1 x2 y2 zcut out.png [label:x,y ...]   (RENDER_WIDTH=n scales the picture down to n px)
Read only (writes out.png).
"""
import os
import sys

from PIL import ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import isorender as iso  # noqa: E402

SOS = 'D:/UO/golems/Iron/p708-work/sosclient'


def render(x1, y1, x2, y2, zcut, out, marks=()):
    sc = iso.Scene.from_map(SOS, 1, x1, y1, x2, y2)
    sc.statics = [s for s in sc.statics if s[2] <= zcut]
    im = iso.render(sc, x1, y1, x2, y2)
    d = ImageDraw.Draw(im)
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if x % 5 == 0 and y % 5 == 0:
                px, py = iso.tile_px(im, x, y)
                d.text((px - 14, py + 14), '%d,%d' % (x, y), fill=(255, 255, 0))
    for label, (x, y) in marks:
        px, py = iso.tile_px(im, x, y)
        d.ellipse((px - 6, py + 16, px + 6, py + 28), outline=(255, 0, 0), width=2)
        d.text((px + 8, py + 14), label, fill=(255, 64, 64))
    w = int(os.environ.get('RENDER_WIDTH', '0'))
    if w and im.width > w:
        info = im.info
        im = im.resize((w, int(im.height * w / im.width)))
        im.info.update(info)
    print(out, iso.save(im, out))


if __name__ == '__main__':
    a = sys.argv[1:]
    x1, y1, x2, y2, zcut = (int(v) for v in a[:5])
    marks = []
    for m in a[6:]:
        lab, xy = m.split(':')
        marks.append((lab, tuple(int(v) for v in xy.split(','))))
    render(x1, y1, x2, y2, zcut, a[5], marks)
