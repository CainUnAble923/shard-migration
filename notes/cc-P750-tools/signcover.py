import re, sys, json
import numpy as np
sys.path.insert(0, 'D:/UO/golems/Iron/shard-migration/notes/cc-P708-tools/p281sos')
import hallbase as H
from mapbuild import isorender as iso
src = open('D:/UO/ModernUO-pinned/Projects/UOContent/Items/Construction/Signs/Sign.cs').read()
body = src[src.index('enum SignType'):]; body = body[body.index('{') + 1:body.index('}')]
names = [n.strip().split('=')[0].strip() for n in re.sub(r'//.*', '', body).split(',') if n.strip()]
art = iso.Art(art_folder=H.CLIENT, client=H.CLIENT)
d = json.load(open('D:/UO/golems/Iron/ShatteredLegacy/design/guild-halls/halls.json'))
todo = []
for h in d['halls']:
    if h['key'] in ('league', 'merchants', 'healers', 'rangers', 'tinkers', 'custodians'):
        todo.append((h['key'], h['sign']))
for a in sys.argv[1:]:   # key:type:facing:x,y,z
    k, ty, fa, p = a.split(':'); x, y, z = map(int, p.split(','))
    todo.append((k + '?', {'type': ty, 'facing': fa, 'x': x, 'y': y, 'z': z}))
for key, s in todo:
    h = {'key': key}
    x, y, z = s['x'], s['y'], s['z']
    tid = 0xB95 + 2 * names.index(s['type']) + (1 if s['facing'] == 'West' else 0)
    sm = np.array(art.static(tid))[:, :, 3] > 0
    sh, sw = sm.shape
    L, T = (x - y) * 22 + 22 - sw // 2, (x + y) * 22 + 44 - sh - z * 4
    sc = iso.Scene.from_map(H.CLIENT, 1, x - 1, y - 1, x + 16, y + 16)
    cov = np.zeros_like(sm)
    for sx, sy, sz, t2 in sc.statics:
        later = sx + sy > x + y or ((sx, sy) == (x, y) and sz > z)
        if not later:
            continue
        im = art.static(t2)
        if im is None:
            continue
        m = np.array(im)[:, :, 3] > 0
        mh, mw = m.shape
        left, top = (sx - sy) * 22 + 22 - mw // 2, (sx + sy) * 22 + 44 - mh - sz * 4
        a0, b0, a1, b1 = max(L, left), max(T, top), min(L + sw, left + mw), min(T + sh, top + mh)
        if a0 < a1 and b0 < b1:
            cov[b0 - T:b1 - T, a0 - L:a1 - L] |= m[b0 - top:b1 - top, a0 - left:a1 - left]
    print('%-10s %s sign %s 0x%04X: %.0f%% of its pixels covered' % (h['key'], s['facing'], (x, y, z), tid, 100 * (cov & sm).sum() / sm.sum()))
