# cc-P16 Part A 2 and 3 (read only). For every component and NPC tile in the mine-camp layout:
# the server's land z (Map.Tiles.GetLandTile(x, y).Z) and average z (Map.GetAverageZ, pinned
# Projects/Server/Maps/Map.cs:243-296, including FloorAverage :286-296), the statics on the tile, and
# for the NPC tiles a port of pinned Map.CanSpawnMobile (Map.cs:1137-1275), land and statics only.
# Reads the same client files the server reads (TileMatrix.cs:94-141): map1LegacyMUL.uop, staidx1.mul,
# statics1.mul, tiledata.mul in D:/ShatteredLegacy/client-data/classic-client.
# Also re-derives the layout's deco z values the way camp.py did, to show the mockup read these files.
import json, struct
src = open(r'D:/ShatteredLegacy/design/mine-camp-tents/uorender.py').read()
src = src.replace("os.path.expanduser('~/mnt/ShatteredLegacy/client-data/classic-client')",
                  "r'D:/ShatteredLegacy/client-data/classic-client'")
src = src.split('def persp_coeffs')[0].replace('from PIL import Image, ImageDraw, ImageFont', '')
ns = {}; exec(compile(src, 'uor', 'exec'), ns)
M = ns['Map'](1); T = ns['Tiles']()
IMP, SURF, BRIDGE, WET = 0x40, 0x200, 0x400, 0x80

def landz(x, y): return M.land(x, y)[1]
def floor_avg(a, b):
    v = a + b
    if v < 0: v -= 1
    return int(v / 2)
def avgz(x, y):  # pinned GetAverageZ: returns (low, avg, top)
    t, l, r, b = landz(x, y), landz(x, y + 1), landz(x + 1, y), landz(x + 1, y + 1)
    avg = floor_avg(l, r) if abs(t - b) > abs(l - r) else floor_avg(t, b)
    return min(t, l, r, b), avg, max(t, l, r, b)
def ignored(i): return i == 2 or i == 0x1DB or 0x1AE <= i <= 0x1B5   # LandTile.Ignored
def calch(sid):
    h = T.sheight[sid]; return h // 2 if T.sflags[sid] & BRIDGE else h
def statics(x, y):
    return [(sid, sz) for (sid, sx, sy, sz, hue) in M.statics(x >> 3, y >> 3) if (x & 7, y & 7) == (sx, sy)]

def can_spawn_mobile(x, y, minz, maxz, extra=()):
    """Port of Map.CanSpawnMobile(x, y, minZ, maxZ, canSwim=false, cantWalk=false). extra: (id, z) items."""
    lid, _ = M.land(x, y); low, avg, _ = avgz(x, y)
    blocked = set(); surf = set()
    if not ignored(lid):
        lf = T.lflags.get(lid & 0x3FFF, 0)
        if lf & IMP:
            blocked.update(range(low - 16 + 1, avg))
        if minz <= avg <= maxz and not lf & IMP:
            surf.add(avg)
    for sid, sz in list(statics(x, y)) + list(extra):
        f = T.sflags[sid]; top = sz + calch(sid)
        if f & SURF or f & IMP:
            blocked.update(range(sz - 16 + 1, top))
        if minz <= top <= maxz and f & SURF and not f & IMP:
            surf.add(top)
    ok = sorted(z for z in surf if z not in blocked)
    return ok[0] if ok else None

if __name__ == '__main__':
    L = json.load(open(r'D:/ShatteredLegacy/design/mine-camp-tents/layout.json'))
    # camp.py's own avgz (its line 3-5) to re-derive deco z = avgz + dz
    def camp_avgz(x, y):
        t = landz(x, y); l = landz(x, y + 1); r = landz(x + 1, y); b = landz(x + 1, y + 1)
        return (l + r) // 2 if abs(t - b) > abs(l - r) else (t + b) // 2
    print('addon,group,id,name,x,y,layout_z,land_z,avg_z,low,top,statics')
    for a in L['addons']:
        for c in a['components']:
            x, y, z = c['x'], c['y'], c['z']
            low, avg, top = avgz(x, y)
            st = ' '.join(f"0x{s:04X}@{sz}({T.sname[s]})" for s, sz in statics(x, y))
            print(f"{a['name']},{c['group']},{c['id']},{c['name']},{x},{y},{z},{landz(x,y)},{avg},{low},{top},{st}")
    print()
    print('npc,to,land_z,avg_z,CanSpawnMobile(z-16..z+16),statics')
    for n in L['npcs']:
        x, y, z = n['to']
        low, avg, top = avgz(x, y)
        st = ' '.join(f"0x{s:04X}@{sz}({T.sname[s]})" for s, sz in statics(x, y))
        print(f"{n['type']},{x} {y} {z},{landz(x,y)},{avg},{can_spawn_mobile(x, y, z - 16, z + 16)},{st}")
    for n in L['npcs']:
        x, y, z = n['from']
        print(f"{n['type']} from,{x} {y} {z},{landz(x,y)},{avgz(x,y)[1]},{can_spawn_mobile(x, y, z - 16, z + 16)}")
