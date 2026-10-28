"""cc-P720: a labelled sheet of item art: python -P artsheet.py out.png id id ... (hex)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
from PIL import Image, ImageDraw
from mapbuild import isorender
art = isorender.Art()
ids = [int(h, 16) for h in sys.argv[2:]]
cell = 120
cols = 10
sheet = Image.new('RGB', (cols * cell, ((len(ids) + cols - 1) // cols) * (cell + 14)), (40, 40, 40))
d = ImageDraw.Draw(sheet)
for i, t in enumerate(ids):
    im = art.static(t)
    x, y = (i % cols) * cell, (i // cols) * (cell + 14)
    if im is not None:
        im = im.copy(); im.thumbnail((cell - 4, cell - 4))
        sheet.paste(im, (x + 2, y + 2), im if im.mode == 'RGBA' else None)
    d.text((x + 2, y + cell), '%04X' % t, fill=(255, 255, 0))
sheet.save(sys.argv[1]); print(sys.argv[1])
