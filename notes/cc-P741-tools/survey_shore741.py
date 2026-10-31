"""cc-P741: OSI's gentle sandy coasts, learned the way OSI lays them: the first sand tiles beside the sea stand at the
sea's height (Z -5) and carry the surf piece for their edge; the sea keeps its water land (and a plain water static
0x1797). For each such sand cell, by its 8-neighbour sea pattern (N NE E SE S SW W NW, 'S' sea, '.' land), the shore
statics OSI lays on it; and for each sea cell beside one, what lies on it.
    python -P survey_shore741.py <out.json>"""
import collections, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import uofiles
C = 'D:/UO/UltimaOnlineVanilla'
W, H = 5120, 4096
mf = uofiles.MapFile(C, 1)
reg = mf.region(0, 0, W - 1, H - 1)
ids = np.zeros((W, H), dtype=np.int32); zz = np.zeros((W, H), dtype=np.int32)
for (x, y), (t, z) in reg.items():
    if 0 <= x < W and 0 <= y < H:
        ids[x, y] = t; zz[x, y] = z
sea = np.isin(ids, [0xA8, 0xA9, 0xAA, 0xAB])
sand = ((ids >= 0x16) & (ids <= 0x19)) | ((ids >= 0x33) & (ids <= 0x3E))
# statics: shore pieces by cell
DT = np.dtype([('id', '<u2'), ('x', 'u1'), ('y', 'u1'), ('z', 'i1'), ('hue', '<i2')])
idx, sta = uofiles.load_statics_index(C, 1)
rec = np.frombuffer(sta[:len(sta) // 7 * 7], dtype=DT)
hit = np.nonzero((rec['id'] >= 0x1796) & (rec['id'] <= 0x17B2))[0]
looks = idx[:, 0]
valid = np.nonzero((looks >= 0) & (idx[:, 1] > 0))[0]
order = valid[np.argsort(looks[valid])]
starts = looks[order]
pieces = collections.defaultdict(list)
for i in hit:
    off = int(i) * 7
    k = np.searchsorted(starts, off, side='right') - 1
    b = int(order[k])
    if not (looks[b] <= off < looks[b] + idx[b, 1]):
        continue
    bx, by = divmod(b, H // 8)
    r = rec[i]
    x, y = bx * 8 + int(r['x']), by * 8 + int(r['y'])
    if x < W:
        pieces[(x, y)].append('%04X@%d' % (int(r['id']), int(r['z'])))
NB = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
land_table = collections.defaultdict(collections.Counter)
sea_table = collections.defaultdict(collections.Counter)
xs, ys = np.nonzero(sand & (zz >= -6) & (zz <= -4))
for x, y in zip(xs, ys):
    if not (2 <= x < W - 2 and 2 <= y < H - 2):
        continue
    pat = ''.join('S' if sea[x + a, y + b] else '.' for a, b in NB)
    if 'S' not in pat:
        continue
    # gentle: every sea neighbour at -5, and no cliff piece (OSI's -15 shelves are another coast)
    if any(sea[x + a, y + b] and zz[x + a, y + b] != -5 for a, b in NB):
        continue
    land_table[pat]['+'.join(sorted(pieces.get((x, y), [])))] += 1
    for a, b in NB:
        if sea[x + a, y + b]:
            pat2 = ''.join('S' if sea[x + a + c, y + b + d] else '.' for c, d in NB)
            sea_table[pat2]['+'.join(sorted(pieces.get((x + a, y + b), [])))] += 1
out = {'land': {k: v.most_common(6) for k, v in sorted(land_table.items(), key=lambda kv: -sum(kv[1].values()))},
       'sea': {k: v.most_common(4) for k, v in sorted(sea_table.items(), key=lambda kv: -sum(kv[1].values()))}}
json.dump(out, open(sys.argv[1], 'w'), indent=0)
for k, v in list(out['land'].items())[:40]:
    print('L', k, sum(n for _, n in land_table[k].items()), v[:4])
for k, v in list(out['sea'].items())[:15]:
    print('S', k, v[:3])
