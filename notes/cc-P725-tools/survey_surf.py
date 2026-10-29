"""cc-P725: how OSI's Trammel draws its coastline. P662 found plain sand against the sea with the static water 0x1797
on the first sand ring; this survey counts every static water piece 0x1796-0x17B2 on the mainland (x < 5120), the land
under it, its Z, and which of its 8 neighbours are wet (water land or a water static), so the isle's shoreline can be
laid with OSI's edge and corner pieces by the same rule.

    python -P survey_surf.py <client folder> <out json>
"""
import collections, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import uofiles  # noqa: E402

WSTAT = set(range(0x1796, 0x17B3))
NB = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]   # N NE E SE S SW W NW


def main():
    folder, out = sys.argv[1], sys.argv[2]
    ids, zs = uofiles.load_land(folder, 1)
    land_td = uofiles.read_tiledata(folder)[0]
    wet_land = np.zeros(ids.shape, bool)
    for t in range(0x4000):
        if land_td[t][0] & uofiles.WET:
            wet_land[ids == t] = True
    idx, sta = uofiles.load_statics_index(folder, 1)
    bh = 4096 >> 3
    wstat = {}
    for bx in range(5120 >> 3):
        for by in range(bh):
            for (tid, cx, cy, z, hue) in uofiles.block_statics(idx, sta, bx * bh + by):
                if tid in WSTAT:
                    wstat[(bx * 8 + cx, by * 8 + cy)] = (tid, z)
    wet = lambda x, y: (x, y) in wstat or (0 <= x < 5120 and 0 <= y < 4096 and wet_land[x, y])
    rep = {}
    for (x, y), (tid, z) in wstat.items():
        r = rep.setdefault('0x%04X' % tid, dict(n=0, z=collections.Counter(), land=collections.Counter(),
                                                landz=collections.Counter(), pattern=collections.Counter(),
                                                example=None))
        r['n'] += 1
        r['z'][z] += 1
        r['land']['0x%04X' % int(ids[x, y])] += 1
        r['landz'][int(zs[x, y]) - z] += 1
        r['pattern'][''.join('W' if wet(x + a, y + b) else '.' for a, b in NB)] += 1
        if r['example'] is None and x > 1000:
            r['example'] = (x, y)
    out_rep = {}
    for k in sorted(rep):
        r = rep[k]
        out_rep[k] = dict(n=r['n'], z=dict(r['z'].most_common(4)), land=dict(r['land'].most_common(5)),
                          land_minus_static_z=dict(r['landz'].most_common(5)),
                          pattern=dict(r['pattern'].most_common(6)), example=r['example'])
        print(k, r['n'], 'z', dict(r['z'].most_common(3)), 'land', dict(r['land'].most_common(3)),
              'dz', dict(r['landz'].most_common(3)), 'pat', r['pattern'].most_common(3), r['example'])
    json.dump(out_rep, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
