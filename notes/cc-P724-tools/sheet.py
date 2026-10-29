"""cc-P724: a 2x2 contact sheet of the four shots in a folder (game area only). Usage: python -P sheet.py <folder> <out.jpg>"""
import sys
from PIL import Image
ims = [Image.open(sys.argv[1] + "/%s.jpg" % n).convert("RGB").crop((10, 50, 815, 720)) for n in ("wreck", "lighthouse", "frame", "fountain")]
o = Image.new("RGB", (1610, 1340))
for i, im in enumerate(ims):
    o.paste(im, ((i % 2) * 805, (i // 2) * 670))
o.thumbnail((1600, 1340))
o.save(sys.argv[2], quality=80)
