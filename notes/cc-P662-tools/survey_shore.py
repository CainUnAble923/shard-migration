"""cc-P662: what OSI's Trammel puts between the sea and the sand, and between the sand and the grass.

Every land tile in stock Trammel's mainland (x < 5120) whose 8 neighbours include the plain sea (0x00A8-0x00AB) or
the plain sand (0x0016-0x0019) is histogrammed by id, its Z and the pattern of which neighbours are which, so the
build can copy the stock transitions instead of guessing them.

    python -P survey_shore.py <client folder> <out json>
"""
import collections, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import uofiles  # noqa: E402

WATER = {0x00A8, 0x00A9, 0x00AA, 0x00AB}
SAND = {0x0016, 0x0017, 0x0018, 0x0019}
GRASS = {0x0003, 0x0004, 0x0005, 0x0006}
NB = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]   # NW N NE E SE S SW W


def main():
    folder, out = sys.argv[1], sys.argv[2]
    ids, zs = uofiles.load_land(folder, 1)
    ids = ids[:5120]
    zs = zs[:5120]
    land_names = uofiles.read_tiledata(folder)[0]
    cls = np.zeros(ids.shape, dtype=np.int8)       # 0 other, 1 water, 2 sand, 3 grass
    cls[np.isin(ids, list(WATER))] = 1
    cls[np.isin(ids, list(SAND))] = 2
    cls[np.isin(ids, list(GRASS))] = 3
    w, h = ids.shape
    near = {}
    for k, (dx, dy) in enumerate(NB):
        sh = np.zeros_like(cls)
        xs = slice(max(0, -dx), w - max(0, dx)); xd = slice(max(0, dx), w - max(0, -dx))
        ys = slice(max(0, -dy), h - max(0, dy)); yd = slice(max(0, dy), h - max(0, -dy))
        sh[xs, ys] = cls[xd, yd]
        near[k] = sh
    any_w = np.zeros(cls.shape, bool)
    any_s = np.zeros(cls.shape, bool)
    any_g = np.zeros(cls.shape, bool)
    for k in near:
        any_w |= near[k] == 1
        any_s |= near[k] == 2
        any_g |= near[k] == 3
    report = {}
    for label, mask in (('touching sea and sand', any_w & any_s & (cls != 1) & (cls != 2)),
                        ('sand touching sea', any_w & (cls == 2)),
                        ('touching sand and grass', any_s & any_g & (cls != 2) & (cls != 3)),
                        ('grass touching sand', any_s & (cls == 3)),
                        ('sea touching sand', any_s & (cls == 1))):
        xs, ys = np.nonzero(mask)
        byid = collections.Counter()
        zby = collections.defaultdict(collections.Counter)
        pat = collections.defaultdict(collections.Counter)
        for x, y in zip(xs.tolist(), ys.tolist()):
            t = int(ids[x, y])
            byid[t] += 1
            zby[t][int(zs[x, y])] += 1
            p = ''.join('wsg.'[[1, 2, 3, 0].index(int(near[k][x, y]))] for k in range(8))
            pat[t][p] += 1
        report[label] = {'tiles': int(len(xs)), 'ids': [
            {'id': '0x%04X' % t, 'name': land_names[t][2], 'n': n, 'z': dict(zby[t].most_common(4)),
             'patterns': dict(pat[t].most_common(4))} for t, n in byid.most_common(80)]}
        print(label, len(xs))
        for r in report[label]['ids'][:40]:
            print('  %s %-8s %6d z %s %s' % (r['id'], r['name'], r['n'], r['z'], list(r['patterns'].items())[:2]))
    json.dump(report, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
