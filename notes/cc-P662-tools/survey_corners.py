"""cc-P662: the stock sand/grass transition tiles by corner pattern, the beach's Z profile, and the statics OSI puts
on the waterline. Reads stock Trammel's mainland (x < 5120).

A land tile's diamond has four corners, each a map vertex: top (x, y), right (x+1, y), bottom (x+1, y+1), left (x, y+1).
A transition tile shows grass on some corners and sand on others. A vertex's terrain is read from the other three
tiles round it that are plain grass or plain sand (all of them must agree). Each transition id is then tabulated by
its corner pattern (top, right, bottom, left; g or s), and the build picks ids by pattern.

    python -P survey_corners.py <client folder> <out json>
"""
import collections, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import uofiles  # noqa: E402

WATER = [0x00A8, 0x00A9, 0x00AA, 0x00AB]
SAND = [0x0016, 0x0017, 0x0018, 0x0019]
GRASS = [0x0003, 0x0004, 0x0005, 0x0006]
TRANS = list(range(0x0033, 0x003F))     # the survey_shore.py result: 0x33-0x3A sand-named, 0x3B-0x3E grass-named


def main():
    folder, out = sys.argv[1], sys.argv[2]
    ids, zs = uofiles.load_land(folder, 1)
    ids = ids[:5120].astype(np.int32)
    zs = zs[:5120].astype(np.int32)
    w, h = ids.shape
    cls = np.full(ids.shape, '.', dtype='<U1')
    cls[np.isin(ids, SAND)] = 's'
    cls[np.isin(ids, GRASS)] = 'g'
    cls[np.isin(ids, WATER)] = 'w'
    tab = collections.defaultdict(collections.Counter)
    xs, ys = np.nonzero(np.isin(ids, TRANS))
    # the three other tiles round each corner vertex, as offsets from the tile
    around = {'t': [(-1, -1), (0, -1), (-1, 0)], 'r': [(0, -1), (1, -1), (1, 0)],
              'b': [(1, 0), (1, 1), (0, 1)], 'l': [(-1, 0), (-1, 1), (0, 1)]}
    for x, y in zip(xs.tolist(), ys.tolist()):
        if not (1 <= x < w - 1 and 1 <= y < h - 1):
            continue
        pat = ''
        for k in 'trbl':
            seen = {cls[x + dx, y + dy] for dx, dy in around[k]} & {'s', 'g'}
            pat += seen.pop() if len(seen) == 1 else '?'
        tab['0x%04X' % ids[x, y]][pat] += 1
    print('transition ids by corner pattern (top right bottom left):')
    best = {}
    for tid in sorted(tab):
        c = tab[tid]
        full = [(p, n) for p, n in c.most_common() if '?' not in p]
        tot = sum(n for _, n in full)
        print(' ', tid, sum(c.values()), full[:4])
        if full:
            best[tid] = {'pattern': full[0][0], 'share': round(full[0][1] / tot, 2), 'n': tot}
    by_pat = collections.defaultdict(list)
    for tid, b in best.items():
        by_pat[b['pattern']].append(tid)
    print('patterns:', dict(by_pat))
    # the beach: Z of plain sand by Chebyshev distance from the plain sea (1..5), and Z of the sea beside it
    sea = np.isin(ids, WATER)
    dist = np.full(ids.shape, 99, dtype=np.int32)
    frontier = sea.copy()
    reach = sea.copy()
    for d in range(1, 7):
        grown = np.zeros_like(reach)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                grown[max(0, dx):w + min(0, dx), max(0, dy):h + min(0, dy)] |= \
                    reach[max(0, -dx):w + min(0, -dx), max(0, -dy):h + min(0, -dy)]
        ring = grown & ~reach
        dist[ring] = d
        reach = grown
    beach = {}
    for d in range(1, 7):
        m = (dist == d) & np.isin(ids, SAND)
        beach[d] = collections.Counter(zs[m].tolist()).most_common(6)
        print('sand at distance', d, 'from the sea: Z', beach[d])
    print('sea Z beside sand:', collections.Counter(zs[sea & (dist == 99)].tolist()).most_common(3))
    # statics on the shore: on sand tiles 1-2 from the sea and on sea tiles beside sand
    idx, sta = uofiles.load_statics_index(folder, 1)
    items = uofiles.read_tiledata(folder)[1]
    shore = collections.Counter()
    seaside = collections.Counter()
    bh = h >> 3
    near_sand = np.zeros_like(sea)
    sandm = np.isin(ids, SAND)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            near_sand[max(0, dx):w + min(0, dx), max(0, dy):h + min(0, dy)] |= \
                sandm[max(0, -dx):w + min(0, -dx), max(0, -dy):h + min(0, -dy)]
    want_sand = (dist <= 2) & sandm
    want_sea = sea & near_sand
    blocks = set()
    for m in (want_sand, want_sea):
        bx, by = np.nonzero(m)
        blocks |= set(((bx >> 3) * bh + (by >> 3)).tolist())
    for b in blocks:
        for (tid, cx, cy, z, hue) in uofiles.block_statics(idx, sta, b):
            x, y = (b // bh) * 8 + cx, (b % bh) * 8 + cy
            if x >= 5120:
                continue
            if want_sand[x, y]:
                shore[(tid, items[tid]['name'])] += 1
            elif want_sea[x, y]:
                seaside[(tid, items[tid]['name'])] += 1
    print('statics on sand within 2 of the sea:', [('0x%04X' % t, n, c) for (t, n), c in shore.most_common(25)])
    print('statics on sea tiles beside sand:', [('0x%04X' % t, n, c) for (t, n), c in seaside.most_common(25)])
    json.dump({'corners': {k: dict(v) for k, v in tab.items()}, 'best': best, 'by_pattern': by_pat,
               'beach': beach,
               'shore_statics': [['0x%04X' % t, n, c] for (t, n), c in shore.most_common(40)],
               'seaside_statics': [['0x%04X' % t, n, c] for (t, n), c in seaside.most_common(40)]},
              open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
