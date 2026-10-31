"""cc-P741: each piece alone at full size over one sand tile (land 0x0016 at -5, piece at -5) with sea around it,
so the surf's side shows. python -P piece_big.py out.jpg id,id,..."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import isorender as iso
from PIL import Image, ImageDraw
out, ids = sys.argv[1], [int(v, 16) for v in sys.argv[2].split(',')]
art = iso.Art(); cells = []
for tid in ids:
    land = {(x, y): (0xA8, -5) for x in range(-1, 3) for y in range(-1, 3)}
    land[(0, 0)] = (0x16, -5); land[(1, 0)] = (0x16, -5); land[(0, 1)] = (0x16, -5); land[(1, 1)] = (0x16, -5)
    im = iso.render(iso.Scene(land, [(0, 0, -5, tid)]), -1, -1, 1, 1, art=art).convert('RGB')
    cells.append((tid, im))
W = max(im.width for _, im in cells); H = max(im.height for _, im in cells) + 20
sheet = Image.new('RGB', (W * 4, H * ((len(cells) + 3) // 4)), (27, 27, 27)); d = ImageDraw.Draw(sheet)
for i, (tid, im) in enumerate(cells):
    x, y = (i % 4) * W, (i // 4) * H
    sheet.paste(im, (x, y + 20)); d.text((x + 5, y + 3), '0x%04X (piece on the top sand tile)' % tid, fill=(240, 198, 116))
sheet.save(out, quality=90); print(out, sheet.size)
