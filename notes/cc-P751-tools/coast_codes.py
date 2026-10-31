"""cc-P751: the coast as text, one char a tile, with the surf piece each tile carries.
'~' bare sea, 'g' land that is not sand, '.' bare sand; a surf piece as a letter:
  sand pieces (near coasts): W=0x179D/0x179E (sea west), S=0x179F/0x17A0 (sea south), I=0x17A9 (inside corner),
  D=0x17A5 (SW diagonal only), other 0x17A5-0x17B2 small surf: d
  sea pieces (far coasts): s=0x17A1/0x17A2 (land south), w=0x17A3/0x17A4 (land west), c=0x17AB (inside corner), o other
    python -P coast_codes.py <map folder> x1 y1 x2 y2"""
import collections, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import uofiles
folder = sys.argv[1]
x1, y1, x2, y2 = (int(v) for v in sys.argv[2:6])
mf = uofiles.MapFile(folder, 1)
land = mf.region(x1, y1, x2, y2)
st = collections.defaultdict(list)
for (x, y, z, t) in uofiles.statics_in(folder, 1, x1, y1, x2, y2):
    st[(x, y)].append(t)
SEA = {0xA8, 0xA9, 0xAA, 0xAB}
SANDP = {0x179D: 'W', 0x179E: 'W', 0x179F: 'S', 0x17A0: 'S', 0x17A9: 'I', 0x17A5: 'D'}
SEAP = {0x17A1: 's', 0x17A2: 's', 0x17A3: 'w', 0x17A4: 'w', 0x17AB: 'c'}
SAND = set(range(0x16, 0x1A)) | set(range(0x33, 0x3F)) | set(range(0x44, 0x4C)) | set(range(0x11E, 0x12E)) | set(range(0x192, 0x1A0))
print('      ' + ''.join(str(x % 10) for x in range(x1, x2 + 1)))
for y in range(y1, y2 + 1):
    r = ''
    for x in range(x1, x2 + 1):
        t, z = land[(x, y)]
        surf = [s for s in st[(x, y)] if 0x1797 <= s <= 0x17B2]
        if t in SEA:
            r += (SEAP.get(surf[0], 'o') if surf else '~')
        elif surf:
            r += SANDP.get(surf[0], 'd')
        elif t in SAND:
            r += '.'
        else:
            r += 'g'
    print(y, r)
