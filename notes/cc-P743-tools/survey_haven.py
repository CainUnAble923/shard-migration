"""cc-P743: what stands in New Haven on the SoS land (P708's p281sos copy of P281's hall tools): named decoration (signs and
their text), training dummies, archery buttes, stable and farm pieces, benches, mining land, cave and mountain tiles.

    SL_SHARD_REPO=D:/UO/golems/Iron/ShatteredLegacy python -u -P -W ignore notes/cc-P743-tools/survey_haven.py [x0 y0 x1 y1]
"""
import os
import re
import sys
from collections import Counter, defaultdict

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P708-tools', 'p281sos'))
import hallbase as H  # noqa: E402

box = tuple(int(a) for a in sys.argv[1:5]) if len(sys.argv) >= 5 else (3314, 2345, 3814, 3095)
x0, y0, x1, y1 = box
F = H.Facet(1)

print('== decoration (signs and named things) in', box)
for d in H.decoration_in(1, x0, y0, x1, y1):
    if 'Sign' in d[3] or 'Name' in d[4] or 'Label' in d[4]:
        print('  (%d,%d,%d) %s %s [%s]' % (d[0], d[1], d[2], d[3], d[4][:90], d[5]))

KEYS = re.compile(r'training dummy|pickaxe|archery butte|hay|trough|stall|bench|anvil|forge|crops|wheat|corn|cabbage|'
                  r'carrot|turnip|lettuce|pumpkin|cotton|flax|fence|scarecrow|cave|mine|ore|stalag|piano|harp|lute|'
                  r'drum|stage|podium|crystal ball|pentagram|spellbook|bookcase|alchemy|keg|barrel|bar|counter|ankh',
                  re.I)
hits = defaultdict(list)
for bx in range(x0 >> 3, (x1 >> 3) + 1):
    for by in range(y0 >> 3, (y1 >> 3) + 1):
        for (sid, sx, sy, sz, hue) in F.block(bx, by):
            x, y = bx * 8 + sx, by * 8 + sy
            if not (x0 <= x <= x1 and y0 <= y <= y1):
                continue
            n = H.iname(sid)
            if KEYS.search(n):
                hits[n].append((x, y, sz, sid))

print('== statics by name')
for n in sorted(hits):
    pts = hits[n]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    print('  %-24s %4d  x %d-%d y %d-%d  e.g. %s' % (n, len(pts), min(xs), max(xs), min(ys), max(ys),
                                                    ' '.join('(%d,%d,%d)' % p[:3] for p in pts[:6])))

print('== land kinds')
land = Counter()
cave = []
for x in range(x0, x1 + 1, 2):
    for y in range(y0, y1 + 1, 2):
        lid, z = F.land(x, y)
        name = H.lname(lid)
        land[name] += 1
        if name in ('cave', 'cave floor', 'mountain', 'rock') or 'cave' in name:
            cave.append((x, y, z, name))
for name, c in land.most_common(25):
    print('  %-20s %d' % (name, c))
print('== cave-like land samples:', cave[:40])
