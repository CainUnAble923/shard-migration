"""cc-P725: the shoreline rule, learned from OSI's sandy coasts on stock Trammel's mainland.

A cell is SEA when its land is wet or it holds a whole-tile water piece: the plain water 0x1797-0x179C or one of the
large edge pieces (0x179D-0x17A4, 0x17A9-0x17AC: 481 to 1,012 opaque pixels of the diamond's 1,012). The small surf
pieces (0x17A5-0x17A8, 0x17AD-0x17B2: 109 to 216 pixels) lie on the last land cell, so their cell counts as LAND.
For every cell beside the sea/land line whose land neighbours are all sand (0x0016-0x003A), the water pieces on it are
counted by its own class and the 8-neighbour SEA pattern (N NE E SE S SW W NW). build_isle.py lays the isle's shore
from shore-rule.json: each shore cell takes OSI's water pieces for its pattern.

    python -P survey_rule.py <client folder> <out json>
"""
import collections, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import uofiles  # noqa: E402

WSTAT = set(range(0x1796, 0x17B3))
WHOLE = set(range(0x1797, 0x17A5)) | set(range(0x17A9, 0x17AD))
SANDISH = set(range(0x0016, 0x003B))
NB = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]   # N NE E SE S SW W NW
W = 5120


def main():
    folder, out = sys.argv[1], sys.argv[2]
    ids, zs = uofiles.load_land(folder, 1)
    land_td = uofiles.read_tiledata(folder)[0]
    wetland = np.array([bool(land_td[t][0] & uofiles.WET) for t in range(0x4000)])
    sea = wetland[ids[:W]].copy()
    idx, sta = uofiles.load_statics_index(folder, 1)
    bh = 4096 >> 3
    wst = collections.defaultdict(list)
    for bx in range(W >> 3):
        for by in range(bh):
            for (tid, cx, cy, z, hue) in uofiles.block_statics(idx, sta, bx * bh + by):
                if tid in WSTAT:
                    wst[(bx * 8 + cx, by * 8 + cy)].append((tid, z))
    for c, pieces in wst.items():
        if any(t in WHOLE for t, z in pieces):
            sea[c] = True
    sandish = np.isin(ids[:W], list(SANDISH))
    edge = np.zeros(sea.shape, bool)
    for a, b in NB:
        edge |= np.roll(np.roll(sea, -a, 0), -b, 1) != sea
    table = collections.defaultdict(collections.Counter)
    xs, ys = np.nonzero(edge)
    for x, y in zip(xs.tolist(), ys.tolist()):
        if not (1 <= x < W - 1 and 1 <= y < 4095):
            continue
        dry = [(x + a, y + b) for a, b in NB + [(0, 0)] if not sea[x + a, y + b]]
        if not dry or not all(sandish[c] for c in dry):
            continue
        # gentle beaches only: the land beside the sea within 6 of the sea's -5 (not OSI's sand cliffs)
        if any(not -11 <= int(zs[c]) <= 1 for c in dry):
            continue
        key = ('S' if sea[x, y] else 'L') + ':' + ''.join('S' if sea[x + a, y + b] else '.' for a, b in NB)
        pieces = tuple(sorted('0x%04X@%d' % (t, z - (-5)) for t, z in wst.get((x, y), []) if t != 0x1796))
        table[key][pieces] += 1
    rule = {}
    for key, cnt in sorted(table.items(), key=lambda kv: -sum(kv[1].values())):
        rule[key] = {'n': sum(cnt.values()), 'top': [[list(p), n] for p, n in cnt.most_common(6)]}
    json.dump(rule, open(out, 'w'), indent=1)
    for key, r in list(rule.items())[:60]:
        print(key, r['n'], r['top'][:3])


if __name__ == '__main__':
    main()
