# Per shot: pixels that change between the burst frames (beyond JPEG noise), as a mask image and a coarse grid.
import sys, glob, os
import numpy as np
from PIL import Image
d = sys.argv[1]
for base in sorted(glob.glob(os.path.join(d, '[0-9]-*.jpg'))):
    if '-f' in os.path.basename(base)[2:]:
        continue
    stem = base[:-4]
    fr = [base] + sorted(glob.glob(stem + '-f*.jpg'))
    a = [np.asarray(Image.open(f).convert('L'), dtype=np.int16) for f in fr]
    diff = np.zeros_like(a[0])
    for i in range(1, len(a)):
        diff = np.maximum(diff, np.abs(a[i] - a[0]))
    m = diff > 40
    m[:60] = False  # title bar and menu
    ys, xs = np.nonzero(m)
    print(os.path.basename(stem), len(fr), 'frames;', int(m.sum()), 'changed px')
    # cluster on a 40px grid
    cells = {}
    for y, x in zip(ys, xs):
        cells[(y // 40, x // 40)] = cells.get((y // 40, x // 40), 0) + 1
    hot = sorted(((c, k) for k, c in cells.items() if c > 30), reverse=True)[:12]
    print('   hot 40px cells (y,x):', [(k[0] * 40, k[1] * 40, c) for c, k in hot])
    img = Image.open(base).convert('RGB')
    arr = np.asarray(img).copy()
    arr[m] = [255, 0, 255]
    Image.fromarray(arr).save(stem.replace('shots', 'diffs') + '-diff.png')
