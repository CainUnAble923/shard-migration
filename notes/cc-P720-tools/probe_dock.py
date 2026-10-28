"""cc-P720 item 7: the dock's land and statics along its rows, read from a built map folder."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
from mapbuild import uofiles
folder = sys.argv[1]
m = uofiles.MapFile(folder, 1)
td = uofiles.read_tiledata(uofiles.CLIENT)[1]
st = {}
for s in uofiles.statics_in(folder, 1, 6800, 3985, 6835, 3996):
    st.setdefault((s[0], s[1]), []).append((s[2], s[3]))
for y in range(3988, 3995):
    print('row', y)
    for x in range(6806, 6834):
        tid, z = m.get(x, y)
        ss = ' '.join('%04X@%d(h%d,f%x)' % (t, sz, td[t]['height'], td[t]['flags'] & 0x650) for sz, t in sorted(st.get((x, y), [])))
        print('  %d land %04X z%d  %s' % (x, tid, z, ss))
