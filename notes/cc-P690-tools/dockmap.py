import sys, collections
sys.path.insert(0, r'D:\UO\golems\Iron\shard-migration\scripts')
from mapbuild import uofiles
ov = r'D:\UO\golems\Iron\p690-proof\overlay'
m = uofiles.MapFile(ov, 1)
land, items = uofiles.read_tiledata(r'D:\UO\tool-trials\client-data-copy')
st = collections.defaultdict(list)
for s in uofiles.statics_in(ov, 1, 3620, 2630, 3690, 2700):
    st[(s[0], s[1])].append(s)
print('x from 3624')
for y in range(2640, 2696, 2):
    r = ''
    for x in range(3624, 3690):
        t, z = m.get(x, y)
        wet = land[t][0] & 0x80
        sts = st.get((x, y), [])
        surf = any(items[s[3]]['flags'] & 0x200 for s in sts)
        r += 'D' if surf else ('~' if wet and not sts else ('s' if sts else '.'))
    print('%d %s' % (y, r))
print('--- statics at candidate spots (id, z, wet, surface, impassable, name)')
for p in [(3655, 2675), (3654, 2680), (3640, 2690), (3647, 2690), (3660, 2690), (3633, 2676), (3678, 2684)]:
    t, z = m.get(*p)
    print(p, 'land', hex(t), z, 'wet' if land[t][0] & 0x80 else '', [(hex(s[3]), s[2], bool(items[s[3]]['flags'] & 0x80), bool(items[s[3]]['flags'] & 0x200), bool(items[s[3]]['flags'] & 0x40), items[s[3]]['name']) for s in st.get(p, [])])
