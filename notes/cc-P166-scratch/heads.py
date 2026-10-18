"""cc-P166: the head at 10x, bald / short / long hair, standing, server directions SE..NW, for the ears' height.
    python -P heads.py OUT.png [--src PNGDIR] [--body 401]"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import render_dirs as R
AX, AY, W, H = 80, 115, 160, 150
ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--src'); ap.add_argument('--body', type=int, default=401)
ap.add_argument('--action', type=int, default=4)
a = ap.parse_args()
rows = []
for hair in ('bald', 'short', 'long'):
    hanim = R.item_anim(R.HAIR[hair]) if R.HAIR[hair] else None
    cells = []
    for sd in range(8):
        d, m = R.DRAWN[sd]
        cv = np.zeros((H, W, 4), np.uint8); cv[...] = (60, 60, 60, 255)
        R.place(cv, R.frames(a.body, a.action, d)[0], m, AX, AY)
        if hanim:
            R.place(cv, R.frames(hanim, a.action, d)[0], m, AX, AY)
        ef = R.png_frames(a.src, a.action, d) if a.src else R.frames(4783, a.action, d)
        R.place(cv, ef[0], m, AX, AY)
        cv[:, -1] = (0, 0, 0, 255)
        cells.append(cv[30:66, 63:97])
    rows.append(np.concatenate(cells, 1))
im = Image.fromarray(np.concatenate(rows, 0)).convert('RGB')
im.resize((im.width * 8, im.height * 8), Image.NEAREST).save(a.out)
