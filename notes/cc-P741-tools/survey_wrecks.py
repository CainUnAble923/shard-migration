"""cc-P741: where OSI lays the ShipwreckBow art (0x479A-0x490F) on the stock facets, and what lies with it.
    python -P survey_wrecks.py"""
import collections, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import uofiles
CLIENT = 'D:/UO/UltimaOnlineVanilla'
td = uofiles.read_tiledata(CLIENT)[1]
WRECK = np.array(sorted(t for t in range(0x479A, 0x4910) if 'ShipwreckBow' in td[t]['name']))
DT = np.dtype([('id', '<u2'), ('x', 'u1'), ('y', 'u1'), ('z', 'i1'), ('hue', '<i2')])
SIZES = {0: (7168, 4096), 1: (7168, 4096), 2: (2304, 1600), 3: (2560, 2048), 4: (1448, 1448), 5: (1280, 4096)}
for fi, (w, h) in SIZES.items():
    if not os.path.exists(os.path.join(CLIENT, 'statics%d.mul' % fi)):
        continue
    idx, sta = uofiles.load_statics_index(CLIENT, fi)
    rec = np.frombuffer(sta[:len(sta) // 7 * 7], dtype=DT)
    hit = np.nonzero(np.isin(rec['id'], WRECK))[0]
    print('facet', fi, 'wreck pieces', len(hit))
    if not len(hit):
        continue
    looks = idx[:, 0]
    valid = np.nonzero((looks >= 0) & (idx[:, 1] > 0))[0]
    order = valid[np.argsort(looks[valid])]
    starts = looks[order]
    out = []
    for i in hit:
        off = i * 7
        k = np.searchsorted(starts, off, side='right') - 1
        b = order[k]
        if not (looks[b] <= off < looks[b] + idx[b, 1]):
            continue
        bx, by = divmod(int(b), h // 8)
        r = rec[i]
        out.append((bx * 8 + int(r['x']), by * 8 + int(r['y']), int(r['z']), int(r['id'])))
    cl = collections.defaultdict(list)
    for s in out:
        cl[(s[0] // 24, s[1] // 24)].append(s)
    for k, v in sorted(cl.items()):
        xs = [s[0] for s in v]; ys = [s[1] for s in v]
        print('  %d,%d-%d,%d  %d pieces  %s' % (min(xs), min(ys), max(xs), max(ys), len(v),
              dict(collections.Counter(td[s[3]]['name'] for s in v))))
