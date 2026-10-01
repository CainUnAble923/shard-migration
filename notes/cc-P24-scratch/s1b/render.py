# Top-down before/after renders (114 left, 117 right) using radarcol colours. usage: render.py facet x0 y0 x1 y1 scale name [px,py ...]
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw
from uodata import *

here = os.path.dirname(os.path.abspath(__file__))

def radar(folder):
    d = open(os.path.join(folder, "radarcol.mul"), "rb").read()
    c = np.frombuffer(d, dtype="<u2")
    r = ((c >> 10) & 31) * 255 // 31; g = ((c >> 5) & 31) * 255 // 31; b = (c & 31) * 255 // 31
    return np.stack([r, g, b], 1).astype(np.uint8)

def render(folder, fi, x0, y0, x1, y1, land):
    col = radar(folder)
    w, h = x1 - x0 + 1, y1 - y0 + 1
    img = np.zeros((h, w, 3), np.uint8)
    ids = land["ids"][x0:x1 + 1, y0:y1 + 1]
    img[:, :, :] = col[ids.T]
    topz = land["z"][x0:x1 + 1, y0:y1 + 1].T.astype(int).copy()
    idx, sta = load_statics_index(folder, fi)
    bh = FACETS[fi][2] >> 3
    for bx in range(x0 >> 3, (x1 >> 3) + 1):
        for by in range(y0 >> 3, (y1 >> 3) + 1):
            for tid, sx, sy, z, hue in sorted(block_statics(idx, sta, bx * bh + by), key=lambda s: s[3]):
                X, Y = bx * 8 + sx - x0, by * 8 + sy - y0
                if 0 <= X < w and 0 <= Y < h and z >= topz[Y, X] - 0:
                    img[Y, X] = col[0x4000 + tid]
                    topz[Y, X] = z
    return img

def main():
    fi, x0, y0, x1, y1, scale = map(int, sys.argv[1:7]); name = sys.argv[7]
    pts = [tuple(map(int, p.split(","))) for p in sys.argv[8:]]
    st = json.load(open(os.path.join(here, "changed_statics.json")))[str(fi)]["blocks"]
    ld = json.load(open(os.path.join(here, "changed_land.json")))[str(fi)]["blocks"]
    bh = FACETS[fi][2] >> 3
    panels = []
    for folder in (OLD, NEW):
        land = load_land(folder, fi)
        im = Image.fromarray(render(folder, fi, x0, y0, x1, y1, land)).resize(((x1 - x0 + 1) * scale, (y1 - y0 + 1) * scale), Image.NEAREST)
        d = ImageDraw.Draw(im)
        for b in (set(st) | set(ld)) if scale >= 3 else []:
            bx, by = b // bh * 8, b % bh * 8
            if bx + 8 > x0 and bx <= x1 and by + 8 > y0 and by <= y1:
                c = (255, 0, 255) if b in st else (255, 255, 0)
                d.rectangle([(bx - x0) * scale, (by - y0) * scale, (bx + 8 - x0) * scale - 1, (by + 8 - y0) * scale - 1], outline=c)
        for px, py in pts:
            cx, cy = (px - x0) * scale + scale // 2, (py - y0) * scale + scale // 2
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], outline=(255, 0, 0), width=2)
        panels.append(im)
    W = panels[0].width
    out = Image.new("RGB", (W * 2 + 10, panels[0].height + 18), (30, 30, 30))
    out.paste(panels[0], (0, 18)); out.paste(panels[1], (W + 10, 18))
    d = ImageDraw.Draw(out)
    d.text((4, 3), f"7.0.114.40  {FACETS[fi][0]} x{x0}-{x1} y{y0}-{y1}  (magenta=statics-changed block, yellow=land-only)", fill=(255, 255, 255))
    d.text((W + 14, 3), "7.0.117.0", fill=(255, 255, 255))
    out.save(os.path.join(here, name + ".png"))
    print("wrote", name)

main()
