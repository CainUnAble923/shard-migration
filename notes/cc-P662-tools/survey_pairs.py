"""cc-P662: the stock transition tiles between two plain land groups, by corner pattern (the method of
survey_corners.py, over every id in the map rather than a known range). Used for the road (dirt and grass) and the
square (stone and grass).

    python -P survey_pairs.py <client folder> <a ids, comma hex> <b ids, comma hex>
"""
import collections, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import uofiles  # noqa: E402


def main():
    folder = sys.argv[1]
    A = [int(v, 16) for v in sys.argv[2].split(',')]
    B = [int(v, 16) for v in sys.argv[3].split(',')]
    ids, zs = uofiles.load_land(folder, 1)
    ids = ids[:5120].astype(np.int32)
    w, h = ids.shape
    cls = np.full(ids.shape, '.', dtype='<U1')
    cls[np.isin(ids, A)] = 'a'
    cls[np.isin(ids, B)] = 'b'
    near = np.zeros(ids.shape, bool)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            sl = (slice(max(0, dx), w + min(0, dx)), slice(max(0, dy), h + min(0, dy)))
            src = (slice(max(0, -dx), w + min(0, -dx)), slice(max(0, -dy), h + min(0, -dy)))
            near[sl] |= (cls[src] == 'a')
    nearb = np.zeros(ids.shape, bool)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            sl = (slice(max(0, dx), w + min(0, dx)), slice(max(0, dy), h + min(0, dy)))
            src = (slice(max(0, -dx), w + min(0, -dx)), slice(max(0, -dy), h + min(0, -dy)))
            nearb[sl] |= (cls[src] == 'b')
    xs, ys = np.nonzero(near & nearb & (cls == '.'))
    around = {'t': [(-1, -1), (0, -1), (-1, 0)], 'r': [(0, -1), (1, -1), (1, 0)],
              'b': [(1, 0), (1, 1), (0, 1)], 'l': [(-1, 0), (-1, 1), (0, 1)]}
    tab = collections.defaultdict(collections.Counter)
    for x, y in zip(xs.tolist(), ys.tolist()):
        if not (1 <= x < w - 1 and 1 <= y < h - 1):
            continue
        pat = ''
        for k in 'trbl':
            seen = {cls[x + dx, y + dy] for dx, dy in around[k]} & {'a', 'b'}
            pat += seen.pop() if len(seen) == 1 else '?'
        tab[int(ids[x, y])][pat] += 1
    names = uofiles.read_tiledata(folder)[0]
    by_pat = collections.defaultdict(list)
    for tid, c in sorted(tab.items(), key=lambda kv: -sum(kv[1].values())):
        full = [(p, n) for p, n in c.most_common() if '?' not in p and 'a' in p and 'b' in p]
        tot = sum(n for p, n in c.items() if '?' not in p)
        if not full or full[0][1] < int(os.environ.get("MIN_N", "25")) or full[0][1] < 0.6 * tot:
            continue
        by_pat[full[0][0]].append(('0x%04X' % tid, names[tid][2], full[0][1], round(full[0][1] / tot, 2)))
    for p in sorted(by_pat):
        print(p, by_pat[p])
    print(len(by_pat), 'patterns of 14 mixed')


if __name__ == '__main__':
    main()
