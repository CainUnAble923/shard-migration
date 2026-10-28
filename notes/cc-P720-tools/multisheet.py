"""cc-P720: a contact sheet of house multis (isorender), flags shown: python -P multisheet.py out.png id id ..."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw  # noqa: E402
from mapbuild import isorender  # noqa: E402
import multis  # noqa: E402

out = sys.argv[1]
ims = []
for h in sys.argv[2:]:
    mid = int(h, 16)
    m = multis.multi(mid)
    xs = [s[0] for s in m]; ys = [s[1] for s in m]
    x1, y1, x2, y2 = min(xs) - 1, min(ys) - 1, max(xs) + 1, max(ys) + 1
    land = {(x, y): (0x0003, 0) for x in range(x1 - 1, x2 + 3) for y in range(y1 - 1, y2 + 3)}
    sc = isorender.Scene(land, [(s[0], s[1], s[2], s[3]) for s in m if s[4] == 0])
    im = isorender.render(sc, x1, y1, x2, y2).convert('RGB')
    im.thumbnail((520, 520))
    d = ImageDraw.Draw(im)
    d.text((4, 4), '0x%04X' % mid, fill=(255, 255, 0))
    ims.append(im)
W = 520 * min(4, len(ims)); H = 520 * ((len(ims) + 3) // 4)
sheet = Image.new('RGB', (W, H))
for i, im in enumerate(ims):
    sheet.paste(im, ((i % 4) * 520, (i // 4) * 520))
sheet.save(out)
print(out)
