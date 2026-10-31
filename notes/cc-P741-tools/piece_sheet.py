"""cc-P741: a labelled sheet of single pieces, each drawn on one tile of land in the middle of a 3x3 patch.
    python -P piece_sheet.py <out.jpg> <land id hex> <z of piece> id1,id2,... [cols]"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import isorender as iso
from PIL import Image, ImageDraw
out, land_id, pz, ids = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3]), [int(v, 16) for v in sys.argv[4].split(',')]
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 6
art = iso.Art()
cells = []
for tid in ids:
    land = {(x, y): (land_id, 0) for x in range(-1, 3) for y in range(-1, 3)}
    im = iso.render(iso.Scene(land, [(0, 0, pz, tid)]), -1, -1, 1, 1, art=art).convert('RGB')
    im.thumbnail((200, 200))
    cells.append((tid, im))
W, H = 210, 230
sheet = Image.new('RGB', (W * cols, H * ((len(cells) + cols - 1) // cols)), (27, 27, 27))
d = ImageDraw.Draw(sheet)
for i, (tid, im) in enumerate(cells):
    x, y = (i % cols) * W, (i // cols) * H
    sheet.paste(im, (x + 5, y + 25))
    d.text((x + 5, y + 5), '0x%04X %s' % (tid, art.item_data[tid]['name']), fill=(240, 198, 116))
sheet.save(out, quality=88)
print(out, sheet.size)
