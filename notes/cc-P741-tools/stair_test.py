"""cc-P741: a test coast with the sea north-east of a one-step stair (land where x <= y) and straight north and east
runs, each sea cell beside the land given one candidate piece by its land side; one panel per candidate set.
    python -P stair_test.py out.jpg"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import isorender as iso
from PIL import Image, ImageDraw
art = iso.Art()
N = 12
def is_land(x, y):
    if y >= 9: return x <= 9            # a straight run along the north edge of the lower block (sea north of it)
    return x <= y
NB = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0), 'NE': (1, -1), 'SE': (1, 1), 'SW': (-1, 1), 'NW': (-1, -1)}
def panel(rule, title):
    land, st = {}, []
    for x in range(-1, N + 1):
        for y in range(-1, N + 1):
            if is_land(x, y):
                land[(x, y)] = (0x16, -5 if any(not is_land(x + a, y + b) for a, b in NB.values()) else 0)
            else:
                land[(x, y)] = (0xA8, -5)
                sides = {k for k, (a, b) in NB.items() if is_land(x + a, y + b)}
                for tid in rule(sides):
                    st.append((x, y, -5, tid))
    im = iso.render(iso.Scene(land, st), 0, 0, N - 1, N - 1, art=art).convert('RGB')
    im.thumbnail((420, 420)); d = ImageDraw.Draw(im); d.text((5, 5), title, fill=(255, 220, 120)); return im
def r(s_piece, w_piece, sw_piece, d_piece):
    def rule(sides):
        if 'S' in sides and 'W' in sides: return [sw_piece] if sw_piece else []
        if 'S' in sides: return [s_piece] if s_piece else []
        if 'W' in sides: return [w_piece] if w_piece else []
        if sides == {'SW'}: return [d_piece] if d_piece else []
        return []
    return rule
cands = [('none', r(0, 0, 0, 0)),
         ('S 17A1 W 17A3 SW 17AB d 17AB', r(0x17A1, 0x17A3, 0x17AB, 0x17AB)),
         ('S 17A2 W 17A4 SW 17A7 d 17AB', r(0x17A2, 0x17A4, 0x17A7, 0x17AB)),
         ('S 17A1 W 17A3 SW 17AA d 17A9', r(0x17A1, 0x17A3, 0x17AA, 0x17A9)),
         ('S 17A1 W 17A3 SW 17A6 d 17AC', r(0x17A1, 0x17A3, 0x17A6, 0x17AC)),
         ('S 17A1 W 17A3 SW 17AF d none', r(0x17A1, 0x17A3, 0x17AF, 0))]
ims = [panel(rule, t) for t, rule in cands]
W = max(i.width for i in ims); H = max(i.height for i in ims)
sheet = Image.new('RGB', (W * 3, H * 2))
for k, im in enumerate(ims):
    sheet.paste(im, ((k % 3) * W, (k // 3) * H))
sheet.save(sys.argv[1], quality=90); print(sheet.size)
