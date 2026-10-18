"""cc-P166: how far the fox ears sit above the head, bald and with hair, in every drawn direction and frame.

For each body, hair, action (walk, run, stand), drawn direction 0-4 and frame: the ears' lowest row, and the head's
topmost row (body, or body + hair) under the ears' columns. per ear column, gap = that column's head top - its lowest ear pixel - 1 (0 = touching,
positive = air between them, negative = the ears overlap the head or hair by that many rows).

    python -P measure_ears.py [--src PNGDIR]     summary per body x hair x direction; --src: anim-src PNGs instead
"""
import argparse, collections, os, sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_dirs as R

AX, AY, W, H = 80, 115, 160, 150
EAR_LIMIT = AY - 40     # anchor-relative y < -40 is ears (the art's layout, cc-P138 EAR_ROW)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src')
    ap.add_argument('--bodies', default='401,400,606,605')
    ap.add_argument('--hair', default='bald,short,long,ponytail')
    a = ap.parse_args()
    out = collections.OrderedDict()
    for body in [int(b) for b in a.bodies.split(',')]:
        for hair in a.hair.split(','):
            hanim = R.item_anim(R.HAIR[hair]) if R.HAIR[hair] else None
            for an, act in R.ACTIONS.items():
                for d in range(5):
                    bf = R.frames(body, act, d)
                    hf = R.frames(hanim, act, d) if hanim else []
                    ef = R.png_frames(a.src, act, d) if a.src else R.frames(4783, act, d)
                    for k in range(len(bf)):
                        if not ef:
                            continue
                        head = R.mask_of(bf[k], False, (W, H), AX, AY)
                        if hf:
                            head |= R.mask_of(hf[min(k, len(hf) - 1)], False, (W, H), AX, AY)
                        em = R.mask_of(ef[min(k, len(ef) - 1)], False, (W, H), AX, AY)
                        em[EAR_LIMIT:] = False
                        cols = np.where(em.any(0))[0]
                        if not len(cols):
                            continue
                        # per column: air between that column's lowest ear pixel and the head below it
                        gaps = [np.where(head[:, c])[0].min() - np.where(em[:, c])[0].max() - 1
                                for c in cols if head[:, c].any()]
                        if not gaps:
                            continue
                        out.setdefault((body, hair, d), []).append((min(gaps), max(gaps), len(cols) - len(gaps)))
    print('body hair  drawn-dir: per frame, the tightest and the widest ear column (rows of air under the ears; negative'
          ' = overlap), as median over walk, run and stand frames; and ear columns with no head under them at all')
    for (body, hair, d), g in out.items():
        lo = sorted(x[0] for x in g)
        hi = sorted(x[1] for x in g)
        free = sorted(x[2] for x in g)
        print('%d %-8s d%d  n=%2d  tightest %2d  widest %2d (worst %2d)  columns over nothing %d' % (
            body, hair, d, len(g), lo[len(lo) // 2], hi[len(hi) // 2], hi[-1], free[len(free) // 2]))


if __name__ == '__main__':
    main()
