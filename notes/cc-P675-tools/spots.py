"""cc-P675: the tiles the server facts pin, read independently (uofiles, by UOP name hash) from the overlay's map
(the pristine SoS copy + the re-based trammel.mapops, rebase.py's edited/) and from stock Trammel for contrast.
    python -P spots.py <edited folder>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import uofiles
sos = uofiles.MapFile(sys.argv[1], 1)
ea = uofiles.MapFile(r'D:/UO/UltimaOnlineVanilla', 1)

def avgz(m, x, y):
    t = m.get(x, y)[1]; l = m.get(x, y + 1)[1]; r = m.get(x + 1, y)[1]; b = m.get(x + 1, y + 1)[1]
    if abs(t - b) > abs(l - r):
        return (l + r) // 2 if (l + r) >= 0 else -((-(l + r) + 1) // 2)
    return (t + b) // 2 if (t + b) >= 0 else -((-(t + b) + 1) // 2)

def stat(folder, x, y):
    return sorted(uofiles.statics_in(folder, 1, x, y, x, y))

for name, (x0, y0, x1, y1) in [('valunstead', (476, 385, 482, 391)), ('pols2', (6200, 2114, 6204, 2118)),
                                ('beach', (6636, 3991, 6640, 3995)), ('havenstart', (3634, 2586, 3634, 2586)),
                                ('oldnewhaven', (3503, 2573, 3503, 2574))]:
    print('==', name)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            print('   %d,%d sos %04X@%d avg %d statics %s | ea %04X@%d statics %s' % (x, y, *sos.get(x, y), avgz(sos, x, y), stat(sys.argv[1], x, y), *ea.get(x, y), stat(r'D:/UO/UltimaOnlineVanilla', x, y)))
