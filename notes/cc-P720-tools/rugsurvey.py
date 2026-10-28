"""cc-P720: how OSI lays a carpet: print the grid of carpet ids (0x0AC6-0x0AD0 red, 0x0ABD-0x0AC5 blue) in stock
Trammel areas: python -P rugsurvey.py lo hi x1 y1 x2 y2"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
from mapbuild import uofiles
lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16)
x1, y1, x2, y2 = (int(v) for v in sys.argv[3:7])
g = {}
for s in uofiles.statics_in(uofiles.CLIENT, 1, x1, y1, x2, y2):
    if lo <= s[3] <= hi:
        g[(s[0], s[1])] = s[3]
if not g:
    print('none'); sys.exit()
xs = [c[0] for c in g]; ys = [c[1] for c in g]
print('cells', len(g), 'x', min(xs), max(xs), 'y', min(ys), max(ys))
for y in range(min(ys), max(ys) + 1):
    print('%d ' % y + ' '.join(('%03X' % (g[(x, y)] & 0xFFF)) if (x, y) in g else ' . ' for x in range(min(xs), max(xs) + 1)))
