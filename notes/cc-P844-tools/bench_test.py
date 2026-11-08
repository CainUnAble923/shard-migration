"""cc-P844: which wooden bench joins along y (north-south)? Two pieces of 0x0B2D (left) and of 0x0B2C (right), each on
two tiles one above the other in y, as Pip's bench stands (6704,3975 and 6704,3976), drawn on open grass.
    python -P bench_test.py <map folder> <out.png>"""
import sys
from mapbuild import isorender as iso
from PIL import Image
folder, out = sys.argv[1], sys.argv[2]
x1, y1, x2, y2 = 6720, 3964, 6727, 3971
sc = iso.Scene.from_map(folder, 1, x1, y1, x2, y2)
sc.statics = [(6721, 3967, 0, 0x0B2D), (6721, 3968, 0, 0x0B2D), (6725, 3965, 0, 0x0B2C), (6725, 3966, 0, 0x0B2C)]
im = iso.render(sc, x1, y1, x2, y2).convert('RGB')
im = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
im.save(out)
print(out, im.size)
