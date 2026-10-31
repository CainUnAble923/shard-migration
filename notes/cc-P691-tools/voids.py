"""Block-level (8x8) emptiness of the current Trammel file (SoS + our patch): empty = all 64 land cells VOID and no
statics. Prints the largest empty rectangles and draws a map with site A's zones."""
import sys, os
sys.path.insert(0, r"D:/UO/golems/Iron/shard-migration/scripts")
from mapbuild import uofiles
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CUR = os.path.join(HERE, "cur")
ids, zs = uofiles.load_land(CUR, 1)
W, H = ids.shape
idx, sta = uofiles.load_statics_index(CUR, 1)
bw, bh = W // 8, H // 8
landvoid = (ids == uofiles.VOID).reshape(bw, 8, bh, 8).all(axis=(1, 3))
nst = np.zeros(bw * bh, bool)
L = min(len(idx), bw * bh)
nst[:L] = (idx[:L, 0] >= 0) & (idx[:L, 1] > 0)
empty = landvoid & ~nst.reshape(bw, bh)
np.save(os.path.join(HERE, "empty-blocks.npy"), empty)


def maxrects(empty, need_w, need_h):
    """all maximal-height rectangles of width >= need_w and height >= need_h (in blocks), by histogram method."""
    out = []
    hist = np.zeros(empty.shape[0], int)
    for by in range(empty.shape[1]):
        hist = np.where(empty[:, by], hist + 1, 0)
        stack = []
        for bx in range(len(hist) + 1):
            h = hist[bx] if bx < len(hist) else 0
            start = bx
            while stack and stack[-1][1] >= h:
                s, sh = stack.pop()
                if sh >= need_h and bx - s >= need_w:
                    out.append((sh * (bx - s), s, by - sh + 1, bx - 1, by, sh, bx - s))
                start = s
            stack.append((start, h))
    return out


need_w, need_h = int(sys.argv[1]) if len(sys.argv) > 1 else 40, int(sys.argv[2]) if len(sys.argv) > 2 else 40
rs = maxrects(empty, need_w, need_h)
rs.sort(reverse=True)
seen = set()
for a, x0, y0, x1, y1, h, w in rs[:60]:
    key = (x0, y0, x1, y1)
    if key in seen: continue
    seen.add(key)
    print("tiles x %d-%d y %d-%d  (%d x %d)" % (x0 * 8, x1 * 8 + 7, y0 * 8, y1 * 8 + 7, w * 8, h * 8))
img = np.zeros((bh, bw, 3), np.uint8)
img[~empty.T] = (200, 200, 200)
Image.fromarray(img).resize((bw, bh)).save(os.path.join(HERE, "empty-blocks.png"))
