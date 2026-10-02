# cc-P31: copy of notes/cc-P19-tools/office_z.py, unchanged, run against the 14-component layout.json.
# cc-P19 Part A 1 and 2 (read only). For every component of design/registrar-office/layout.json, and for the
# door, doorway and Registrar tiles: land z, Map.GetAverageZ (pinned Projects/Server/Maps/Map.cs:237-296), the
# statics on the tile with z, height and flags, and a port of Map.GetTopSurfaceZ(Point3D) (Map.cs:491-565):
# the highest land average z or Surface/Wet static top (tile.Z + CalcHeight) at or below p.Z. Map files are the
# ones the server reads (TileMatrix.cs:94-141), loaded through design/registrar-office/uorender.py.
# World items are not in this port; Part A 3 covers them separately.
import json
src = open(r'D:/ShatteredLegacy/design/registrar-office/uorender.py').read()
src = src.replace("os.path.expanduser('~/mnt/ShatteredLegacy/client-data/classic-client')",
                  "r'D:/ShatteredLegacy/client-data/classic-client'")
src = src.split('def persp_coeffs')[0].replace('from PIL import Image, ImageDraw, ImageFont', '')
ns = {}; exec(compile(src, 'uor', 'exec'), ns)
M = ns['Map'](1); T = ns['Tiles']()
IMP, WET, SURF, BRIDGE, DOOR = 0x40, 0x80, 0x200, 0x400, 0x20000000

def landz(x, y): return M.land(x, y)[1]
def floor_avg(a, b):
    v = a + b
    if v < 0: v -= 1
    return int(v / 2)
def avgz(x, y):
    t, l, r, b = landz(x, y), landz(x, y + 1), landz(x + 1, y), landz(x + 1, y + 1)
    return floor_avg(l, r) if abs(t - b) > abs(l - r) else floor_avg(t, b)
def ignored(i): return i == 2 or i == 0x1DB or 0x1AE <= i <= 0x1B5
def calch(sid):
    h = T.sheight[sid]; return h // 2 if T.sflags[sid] & BRIDGE else h
def statics(x, y):
    return [(sid, sz) for (sid, sx, sy, sz, hue) in M.statics(x >> 3, y >> 3) if (x & 7, y & 7) == (sx, sy)]
def top_surface_z(x, y, pz):
    s = None
    lid, _ = M.land(x, y)
    if not ignored(lid):
        a = avgz(x, y)
        if a <= pz: s = a
    for sid, sz in statics(x, y):
        f = T.sflags[sid]
        if f & SURF or f & WET:
            tz = sz + calch(sid)
            if (s is None or tz > s) and tz <= pz: s = tz
    return s
def flags(f):
    out = []
    for n, b in (('imp', IMP), ('wet', WET), ('surf', SURF), ('bridge', BRIDGE), ('door', DOOR)):
        if f & b: out.append(n)
    return '|'.join(out) or '-'
def describe(x, y):
    return ' '.join(f"0x{s:04X}@{sz}+{T.sheight[s]}[{flags(T.sflags[s])}]({T.sname[s].strip()})" for s, sz in statics(x, y)) or 'none'

if __name__ == '__main__':
    L = json.load(open(r'D:/ShatteredLegacy/design/registrar-office/layout.json'))
    print('area,id,name,x,y,layout_z,land_z,avg_z,GetTopSurfaceZ(layout_z),diff,statics')
    for c in L['components']:
        x, y, z = c['x'], c['y'], c['z']
        s = top_surface_z(x, y, z)
        print(f"{c['area']},{c['id']},{c['name']},{x},{y},{z},{landz(x,y)},{avgz(x,y)},{s},{None if s is None else z - s},{describe(x,y)}")
    print()
    print('tile,label,land_z,avg_z,GetTopSurfaceZ(z+0),statics')
    for (x, y, z, label) in [(3459, 2596, 15, 'front door (P17 DarkWoodDoor 0x06A9 WestCCW z15)'),
                             (3459, 2597, 18, 'inside the front door'), (3459, 2595, 15, 'outside the front door'),
                             (3458, 2596, 18, 'west of the front door'), (3460, 2596, 18, 'east of the front door'),
                             (3457, 2599, 18, 'office doorway (P17 DarkWoodDoor 0x06B3 NorthCW z18)'),
                             (3456, 2599, 18, 'west of the doorway'), (3458, 2599, 18, 'east of the doorway'),
                             (3457, 2598, 18, 'north of the doorway'), (3457, 2600, 18, 'south of the doorway'),
                             (3459, 2601, 18, 'Registrar'), (3459, 2600, 18, 'north of the Registrar'),
                             (3460, 2601, 18, 'east of the Registrar'), (3459, 2602, 18, 'south of the Registrar'),
                             (3458, 2600, 24, 'desk north'), (3458, 2601, 24, 'desk south')]:
        print(f"{x} {y} {z},{label},{landz(x,y)},{avgz(x,y)},{top_surface_z(x,y,z)},{describe(x,y)}")
    print()
    print('statics in the house box x3452-3464 y2594-2604, by tile')
    for y in range(2594, 2605):
        for x in range(3452, 3465):
            st = statics(x, y)
            if st: print(f"{x},{y}: {describe(x,y)}")

# Walkability with the props in place: pinned Map.CanSpawnMobile(x, y, minZ, maxZ, canSwim false, cantWalk false)
# (Map.cs:1137-1275), ported in notes/cc-P16-tools/camp_z.py, with every layout component on the tile added as an
# item at its layout z. P17's doors are not added: a closed door is a door, opened by double-click (BaseDoor.cs:414-423).
if __name__ == '__main__':
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location('camp_z', r'D:/UO/shard-migration/notes/cc-P16-tools/camp_z.py')
    cz = importlib.util.module_from_spec(spec); sys.argv = ['x']; spec.loader.exec_module(cz)
    on = {}
    for c in L['components']:
        on.setdefault((c['x'], c['y']), []).append((int(c['id'], 16), c['z']))
    print()
    print('tile,label,props on tile,CanSpawnMobile z 2..34 (lowest standable z)')
    for (x, y, label) in [(3459, 2595, 'outside the front door'), (3459, 2597, 'inside the front door'),
                          (3456, 2599, 'west of the office doorway'), (3458, 2599, 'east of the office doorway'),
                          (3459, 2598, 'path'), (3459, 2599, 'path'), (3459, 2600, 'north of the Registrar, beside the desk'),
                          (3460, 2600, 'NE of the Registrar'), (3460, 2601, 'east of the Registrar'),
                          (3460, 2602, 'SE of the Registrar'), (3459, 2601, 'Registrar (chair)')]:
        ex = on.get((x, y), [])
        print(f"{x} {y},{label},{ex or 'none'},{cz.can_spawn_mobile(x, y, 2, 34, ex)}")
