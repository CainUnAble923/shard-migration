"""cc-P725: OSI's sandy beaches, cell by cell. A cell is wet when it holds a static water piece (0x1796-0x17B2) or
wet land. For every cell within 2 of the wet/dry line on stock Trammel's mainland whose dry neighbours are sand
(0x0016-0x0019, 0x001A-0x0032, 0x0033-0x003A), the composition (land id, land Z, the water statics on it) is counted
by the cell's own wet flag and its 8-neighbour wet pattern. The isle's shore is then laid from this table: each cell
takes OSI's most common composition for its pattern. Also writes the 40 x 40 windows with the most sandy shoreline,
for renders.

    python -P survey_beach.py <client folder> <out json>
"""
import collections, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import uofiles  # noqa: E402

WSTAT = set(range(0x1796, 0x17B3))
SANDISH = set(range(0x0016, 0x003B))
NB = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]   # N NE E SE S SW W NW
W = 5120


def main():
    folder, out = sys.argv[1], sys.argv[2]
    ids, zs = uofiles.load_land(folder, 1)
    land_td = uofiles.read_tiledata(folder)[0]
    wetland = np.array([bool(land_td[t][0] & uofiles.WET) for t in range(0x4000)])
    wet = wetland[ids[:W]]
    idx, sta = uofiles.load_statics_index(folder, 1)
    bh = 4096 >> 3
    wst = collections.defaultdict(list)
    for bx in range(W >> 3):
        for by in range(bh):
            for (tid, cx, cy, z, hue) in uofiles.block_statics(idx, sta, bx * bh + by):
                if tid in WSTAT:
                    wst[(bx * 8 + cx, by * 8 + cy)].append((tid, z))
    for (x, y) in wst:
        wet[x, y] = True
    sandish = np.isin(ids[:W], list(SANDISH))
    # the wet/dry line and the distance to it (2 at most)
    edge = np.zeros(wet.shape, bool)
    for a, b in NB:
        sh = np.roll(np.roll(wet, -a, 0), -b, 1)
        edge |= sh != wet
    table = collections.defaultdict(collections.Counter)
    windows = collections.Counter()
    xs, ys = np.nonzero(edge)
    for x, y in zip(xs.tolist(), ys.tolist()):
        if not (1 <= x < W - 1 and 1 <= y < 4095):
            continue
        dry_nb = [(x + a, y + b) for a, b in NB + [(0, 0)] if not wet[x + a, y + b]]
        if not dry_nb or not all(sandish[c] for c in dry_nb):
            continue
        pat = ''.join('W' if wet[x + a, y + b] else '.' for a, b in NB)
        key = ('W' if wet[x, y] else 'D') + ':' + pat
        comp = ('0x%04X' % int(ids[x, y]), int(zs[x, y]),
                tuple(sorted(('0x%04X' % t, z) for t, z in wst.get((x, y), []))))
        table[key][comp] += 1
        windows[(x // 40, y // 40)] += 1
    rep = {'table': {k: [[list(c[:2]) + [list(map(list, c[2]))], n] for c, n in v.most_common(6)]
                     for k, v in sorted(table.items(), key=lambda kv: -sum(kv[1].values()))},
           'counts': {k: sum(v.values()) for k, v in table.items()},
           'windows': [[k[0] * 40, k[1] * 40, n] for k, n in windows.most_common(15)]}
    json.dump(rep, open(out, 'w'), indent=1)
    for k, v in sorted(table.items(), key=lambda kv: -sum(kv[1].values()))[:40]:
        print(k, sum(v.values()), v.most_common(3))
    print('windows', rep['windows'])


if __name__ == '__main__':
    main()
