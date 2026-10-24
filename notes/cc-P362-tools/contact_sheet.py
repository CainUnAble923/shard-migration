"""cc-P362: a contact sheet of source images (to look at, never committed with third-party pixels).
    python -P contact_sheet.py OUT.png GLOB [GLOB ...]"""
import glob, os, sys
from PIL import Image, ImageDraw

out, pats = sys.argv[1], sys.argv[2:]
files = [f for p in pats for f in sorted(glob.glob(p))]
cell = 270
cols = 6
rows = (len(files) + cols - 1) // cols
sheet = Image.new('RGB', (cols * cell, rows * cell), (60, 60, 60))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert('RGB')
    im.thumbnail((cell - 10, cell - 24))
    x, y = (i % cols) * cell, (i // cols) * cell
    sheet.paste(im, (x + 5, y + 18))
    d.text((x + 3, y + 2), os.path.basename(f)[-44:], fill=(255, 255, 0))
sheet.save(out)
print(sheet.size, len(files))
