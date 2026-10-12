# cc-P34 read only: per tile, the land tile's name, land z, Map.GetAverageZ (pinned Server/Maps/Map.cs:237-296),
# the statics with z, height and flags, a port of Map.GetTopSurfaceZ (Map.cs:491-565), and two flags of ours:
#   walkway  the land tile is a road or plaza (tiledata land name dirt road, cobblestones, flagstone ...) or a
#            static on it is a walkway (name contains road, path, stone path, planks, dock, pier, boards)
#   blocked  an Impassable static stands on it within 16 of the surface (pinned Map.CanFit, Map.cs:925-1010)
import sys
exec(open('nhbase.py').read())
def landname(x, y):
    lid = M.land(x, y)[0]; return T.lname[lid].strip() if hasattr(T, 'lname') else str(lid)
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
def top_surface(x, y, pz=127):
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
WALK_LAND = ('dirt', 'cobblestone', 'flagstone', 'road', 'sand stone', 'marble', 'brick', 'stone')
WALK_STATIC = ('road', 'path', 'planks', 'dock', 'pier', 'boards', 'cobblestone', 'flagstone', 'paving', 'tile', 'floor')
def walkway(x, y, z):
    ln = landname(x, y).lower()
    if top_surface(x, y, z + 2) is not None and any(w in ln for w in WALK_LAND) and abs(avgz(x, y) - z) <= 2: return 'land:' + ln
    for sid, sz in statics(x, y):
        n = name(sid).lower()
        if abs(sz + calch(sid) - z) <= 2 and any(w in n for w in WALK_STATIC): return 'static:' + n
    return ''
def blocked(x, y, z):
    for sid, sz in statics(x, y):
        f = T.sflags[sid]
        if f & IMP and sz < z + 16 and sz + calch(sid) > z: return f"0x{sid:04X}({name(sid)})"
    return ''
def report(x, y, z=None):
    s = top_surface(x, y, 127 if z is None else z + 2)
    zz = s if z is None else z
    return dict(x=x, y=y, land=landname(x, y), landz=landz(x, y), avgz=avgz(x, y), surface=s,
                walkway=walkway(x, y, zz if zz is not None else 0), blocked=blocked(x, y, zz if zz is not None else 0), statics=describe(x, y))
if __name__ == '__main__':
    x0, y0, x1, y1 = [int(v) for v in sys.argv[1:5]]
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            r = report(x, y)
            print(f"{x},{y} land={r['land']}@{r['landz']} avg={r['avgz']} top={r['surface']} walk={r['walkway'] or '-'} blk={r['blocked'] or '-'} | {r['statics']}")
