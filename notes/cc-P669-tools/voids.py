r"""cc-P669: empty void rectangles left in SoS 3.0 (and stock, for comparison) east of x 5120, on a 16-tile grid:
a cell is empty when every tile is void land (0x0244 / NoDraw) with no static. The largest empty rectangles, and
whether one fits the Fold's need (P481: void C was 480 x 448; the isle's drawn area 272 x 145).
    python -P voids.py -> out\voids.csv"""
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cc-P481-tools"))
import islands, sosdiff
G = 16
def largest(empty, k=6):
    """Greedy: the k largest all-empty rectangles of cells (histogram method), each removed before the next."""
    e = empty.copy(); out = []
    for _ in range(k):
        h = np.zeros(e.shape[1], int); best = (0, None)
        for i in range(e.shape[0]):
            h = np.where(e[i], h + 1, 0)
            st = []
            for j in range(len(h) + 1):
                cur = h[j] if j < len(h) else 0
                start = j
                while st and st[-1][1] >= cur:
                    s, hh = st.pop()
                    a = hh * (j - s)
                    if a > best[0]: best = (a, (i - hh + 1, s, i, j - 1))
                    start = s
                st.append((start, cur))
        if not best[1]: break
        i1, j1, i2, j2 = best[1]
        out.append((5120 + i1 * G, j1 * G, 5120 + (i2 + 1) * G - 1, (j2 + 1) * G - 1, (i2 - i1 + 1) * G, (j2 - j1 + 1) * G))
        e[i1:i2 + 1, j1:j2 + 1] = False
    return out
rows = []
for n in ("trammel", "sos"):
    _, kind, cnt, _, _, _ = islands.build(n)
    v = (kind == 2) & (cnt == 0)
    sub = v[5120:, :]
    cells = sub.reshape(sub.shape[0] // G, G, sub.shape[1] // G, G).all(axis=(1, 3))
    for r in largest(cells):
        rows.append([n] + list(r)); print(n, r, "fits 480x448" if r[4] >= 480 and r[5] >= 448 or r[4] >= 448 and r[5] >= 480 else ("fits 272x145" if min(r[4], r[5]) >= 145 and max(r[4], r[5]) >= 272 else ""))
with open(os.path.join(sosdiff.OUT, "voids.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["map", "x1", "y1", "x2", "y2", "w", "h"]); w.writerows(rows)
