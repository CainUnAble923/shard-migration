"""cc-P755: ASCII map of the SoS land round a New Haven sign. Land letter: d dirt/road, g grass, s sand, r rock/mountain,
w water, other first letter; upper case = a static stands there (T tree, X other blocking static).
    SL_SHARD_REPO=D:/UO/golems/Iron/ShatteredLegacy python -P notes/cc-P755-tools/ascii755.py x0 y0 x1 y1
"""
import os, sys
DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P708-tools', 'p281sos'))
import hallbase as H
x0, y0, x1, y1 = (int(a) for a in sys.argv[1:5])
F = H.Facet(1)
print('     ' + ''.join(str(x % 10) for x in range(x0, x1 + 1)))
names = {}
for y in range(y0, y1 + 1):
    row = ''
    for x in range(x0, x1 + 1):
        lid, lz = F.land(x, y)[:2]
        n = H.lname(lid).lower()
        c = 'd' if 'dirt' in n else 'g' if 'grass' in n else 's' if 'sand' in n else 'w' if 'water' in n else \
            'r' if ('rock' in n or 'mountain' in n) else (n[:1] or '?')
        st = F.statics(x, y)
        if st:
            sn = [H.iname(s[0]) for s in st]
            for s in st:
                names[H.iname(s[0])] = s[0]
            c = 'T' if any('tree' in v or 'leaves' in v or 'branch' in v for v in sn) else c.upper()
        row += c
    print('%4d %s' % (y, row))
print({k: hex(v) for k, v in sorted(names.items())})
