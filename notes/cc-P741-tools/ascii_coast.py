"""cc-P741: the isle's land/sea mask as text (one char a tile): '~' sea, 's' sand, 'g' grass/dirt/other, 'o' a sea
cell carrying a shore static, '#' impassable filled notch (0x001A). Also counts one-tile notches and spurs.
    python -P ascii_coast.py <map folder> [x1 y1 x2 y2]"""
import collections, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import uofiles
folder = sys.argv[1]
x1, y1, x2, y2 = (int(v) for v in sys.argv[2:6]) if len(sys.argv) > 5 else (6594, 3905, 6865, 4049)
mf = uofiles.MapFile(folder, 1)
land = mf.region(x1, y1, x2, y2)
st = collections.defaultdict(list)
for (x, y, z, t) in uofiles.statics_in(folder, 1, x1, y1, x2, y2):
    st[(x, y)].append(t)
SEA = {0xA8, 0xA9, 0xAA, 0xAB}
sea = lambda c: land.get(c, (0xA8, -5))[0] in SEA or land.get(c, (0, 0))[0] == 0x1A
rows = []
for y in range(y1, y2 + 1):
    r = ''
    for x in range(x1, x2 + 1):
        t, z = land[(x, y)]
        shore = any(0x179D <= s <= 0x17B2 for s in st[(x, y)])
        if t == 0x1A:
            r += '#'
        elif t in SEA:
            r += 'o' if shore else '~'
        elif 0x16 <= t <= 0x19 or 0x33 <= t <= 0x3E:
            r += 's' if not shore else 'S'
        else:
            r += 'g'
    rows.append(r)
print('\n'.join(rows))
# a one-tile notch: a sea cell with land on 3 of its 4 sides; a spur: a land cell with sea on 3 of 4 sides
n4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
notch = spur = 0
for y in range(y1 + 1, y2):
    for x in range(x1 + 1, x2):
        k = sum(sea((x + a, y + b)) for a, b in n4)
        if sea((x, y)) and k <= 1: notch += 1
        if not sea((x, y)) and k >= 3: spur += 1
print('one-tile notches', notch, 'spurs', spur, file=sys.stderr)
