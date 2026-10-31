"""cc-P751: straight test coasts, sea west of the land (x < 6) and sea south of it (y > 6), each panel one way of
laying the surf: which pieces on the first sand, whether the sea beside it carries the water diamond 0x1797.
    python -P edge_test.py out.jpg"""
import sys
from mapbuild import isorender as iso
from PIL import Image, ImageDraw
art = iso.Art()
N = 10
def panel(title, sea_west, sand_w, sand_s, diamond, sea_w=None, sea_s=None):
    land, st = {}, []
    for x in range(-1, N + 1):
        for y in range(-1, N + 1):
            sea = x < 4 if sea_west else y > 5
            if sea:
                land[(x, y)] = (0xA8, -5)
                if diamond: st.append((x, y, -5, 0x1797))
                if sea_west and x == 3 and sea_w: st.append((x, y, -5, sea_w[y % len(sea_w)]))
                if not sea_west and y == 6 and sea_s: st.append((x, y, -5, sea_s[x % len(sea_s)]))
            else:
                first = (x == 4) if sea_west else (y == 5)
                land[(x, y)] = (0x16, -5 if first else (-3 if ((x == 5) if sea_west else (y == 4)) else 0))
                if first:
                    pcs = sand_w if sea_west else sand_s
                    if pcs: st.append((x, y, -5, pcs[(y if sea_west else x) % len(pcs)]))
    im = iso.render(iso.Scene(land, st), 0, 0, N - 1, N - 1, art=art).convert('RGB')
    im.thumbnail((380, 380)); d = ImageDraw.Draw(im); d.text((5, 5), title, fill=(255, 220, 120)); return im
P = [('W: 179D/E on sand, diamonds', True, [0x179D, 0x179E], None, True),
     ('W: 179D/E on sand, no diamonds', True, [0x179D, 0x179E], None, False),
     ('W: nothing on sand, 17A3/4 on sea', True, None, None, True, [0x17A3, 0x17A4]),
     ('W: 179D/E on sand + sea 17A3/4', True, [0x179D, 0x179E], None, True, [0x17A3, 0x17A4]),
     ('S: 179F/A0 on sand, diamonds', False, None, [0x179F, 0x17A0], True),
     ('S: nothing on sand, 17A1/2 on sea', False, None, None, True, None, [0x17A1, 0x17A2])]
ims = [panel(t, *a) for (t, *a) in P]
W = max(i.width for i in ims); H = max(i.height for i in ims)
sheet = Image.new('RGB', (W * 3, H * 2))
for k, im in enumerate(ims): sheet.paste(im, ((k % 3) * W, (k // 3) * H))
sheet.save(sys.argv[1], quality=90); print(sheet.size)
