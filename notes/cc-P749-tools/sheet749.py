"""cc-P749: contact sheets of shots, each cropped to the game view (or a box), 2 or 3 per row, with names.
Usage: python -P sheet749.py <out.jpg> <box x0,y0,x1,y1 or 'game'> <cols> <shot.jpg>...
"""
import os
import sys

from PIL import Image, ImageDraw

out, box, cols, files = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4:]
GAME = (14, 60, 812, 712)  # the game view in a 1280x829 TazUO window
b = GAME if box == "game" else tuple(int(v) for v in box.split(","))
tiles = []
for f in files:
    im = Image.open(f).convert("RGB").crop(b)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 8 * len(os.path.basename(f)) + 8, 16), fill=(0, 0, 0))
    d.text((4, 2), os.path.basename(f), fill=(255, 255, 0))
    tiles.append(im)
w, h = tiles[0].size
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (w * cols, h * rows))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * w, (i // cols) * h))
sheet.thumbnail((1900, 1900))
sheet.save(out, quality=85)
print(out, sheet.size)
