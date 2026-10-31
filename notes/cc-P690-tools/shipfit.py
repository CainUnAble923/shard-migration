import sys, collections
sys.path.insert(0, r'D:\UO\golems\Iron\shard-migration\scripts')
from mapbuild import uofiles
ov = r'D:\UO\golems\Iron\p690-proof\overlay'
m = uofiles.MapFile(ov, 1)
st = collections.defaultdict(list)
for s in uofiles.statics_in(ov, 1, 3600, 2640, 3720, 2760):
    st[(s[0], s[1])].append(s)
def water_ok(x, y, z=-5):
    t, lz = m.get(x, y)
    has = lz == z and (168 <= t <= 171 or 310 <= t <= 311)
    for s in st.get((x, y), []):
        w = 0x1796 <= s[3] <= 0x17B2
        if s[2] == z and w:
            has = True
        elif s[2] >= z and not w:
            return False
    return has
def fits(cx, cy):
    return all(water_ok(cx + dx, cy + dy) for dx in range(-3, 4) for dy in range(-6, 7))
best = []
for cx in range(3630, 3690):
    for cy in range(2660, 2720):
        if fits(cx, cy):
            for px, py in ((3647, 2682), (3650, 2675), (3662, 2682)):
                best.append((max(abs(cx - px), abs(cy - py)), (cx, cy), (px, py)))
best.sort()
print(best[:8])
print('at the ship spot:', [(hex(s[3]), s[2]) for s in st.get((3641, 2684), [])], 'land', m.get(3641, 2684))
