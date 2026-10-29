"""cc-P725: a labelled sheet of art (statics s:0x..., land l:0x...) to pick shore pieces by eye.
    python -P artsheet.py out.png s:0x1796-0x17B2 l:0x001A-0x0032 ..."""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
from mapbuild import isorender as R

art = R.Art()
out, specs = sys.argv[1], sys.argv[2:]
tiles = []
for sp in specs:
    k, rng = sp.split(':')
    a, _, b = rng.partition('-')
    for t in range(int(a, 16), int(b or a, 16) + 1):
        im = art.static(t) if k == 's' else art.land(t)
        if im is not None:
            tiles.append(('%s%04X' % (k, t), im))
cw, ch, cols = 110, 130, 10
sheet = Image.new('RGBA', (cw * cols, ch * ((len(tiles) + cols - 1) // cols)), (60, 60, 60, 255))
d = ImageDraw.Draw(sheet)
for i, (lab, im) in enumerate(tiles):
    x, y = (i % cols) * cw, (i // cols) * ch
    im = im.copy(); im.thumbnail((cw - 6, ch - 20))
    sheet.alpha_composite(im, (x + 3, y + 3))
    d.text((x + 3, y + ch - 14), lab, fill=(255, 255, 0, 255))
sheet.convert('RGB').save(out)
