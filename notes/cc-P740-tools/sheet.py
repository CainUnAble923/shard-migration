"""cc-P740: a contact sheet of TazUO shots, each cropped around the character (the game view's centre), labelled.
Usage: python -P sheet.py <out.jpg> <cols> <crop w> <crop h> <image>[=label] ...
The crop is centred on SHEET_CX, SHEET_CY (environment; default 390, 370: the player in a 1280x829 TazUO window shot,
its game view at the left)."""
import os
import sys
from PIL import Image, ImageDraw

out, cols, cw, ch = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
items = []
for a in sys.argv[5:]:
    path, _, label = a.partition("=")
    items.append((path, label or path.replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0]))
rows = (len(items) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cw, rows * ch), "black")
d = ImageDraw.Draw(sheet)
for i, (path, label) in enumerate(items):
    im = Image.open(path).convert("RGB")
    cx, cy = int(os.environ.get('SHEET_CX', 390)), int(os.environ.get('SHEET_CY', 370))
    tile = im.crop((cx - cw // 2, cy - ch // 2, cx + cw // 2, cy + ch // 2))
    x, y = (i % cols) * cw, (i // cols) * ch
    sheet.paste(tile, (x, y))
    d.rectangle((x, y, x + 8 * len(label) + 6, y + 14), fill="black")
    d.text((x + 3, y + 1), label, fill="yellow")
sheet.save(out, quality=88)
print("wrote", out, sheet.size)
