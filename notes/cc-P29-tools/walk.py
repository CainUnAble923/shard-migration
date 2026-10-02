# cc-P29 Part D: a line-for-line port of pinned MovementImpl.CheckMovement / Check / GetStartZ / IsOk
# (Projects/UOContent/Engines/Pathing/Movement.cs:42-176, :182-235, :237-480, :482-580) and Map.GetAverageZ
# (Projects/Server/Maps/Map.cs:243-297) for a walking player (CanSwim false, CantWalk false, not flying, access
# Player) over the client map, statics and tiledata. No world items (pinned ships no Ter Mur decoration) and no
# mobiles, unless passed as `extra` statics. Then a breadth-first walk from pinned's teleporter landings into the
# Underworld (teleporters.json), following every teleporter whose source is in the box. Read only.
import sys, json
from collections import deque
sys.path.insert(0, r'D:/UO/shard-migration/notes/cc-P29-tools')
from uodata import *

PERSON, STEP = 16, 2
IMP_, WET_, SURF_, BRIDGE_ = 0x40, 0x80, 0x200, 0x400


class World:
    def __init__(self, cd, mapidx=5, extra=None):
        ns = load(cd)
        self.M = ns['Map'](mapidx)
        self.T = ns['Tiles']()
        self.extra = extra or {}  # (x, y) -> [(id, z)], items standing in for world items (stepping tiles)
        self._st = {}

    def land(self, x, y):
        return self.M.land(x, y)

    def statics(self, x, y):
        k = (x, y)
        if k not in self._st:
            self._st[k] = [(sid, sz) for (sid, sx, sy, sz, h) in self.M.statics(x >> 3, y >> 3)
                           if (sx, sy) == (x & 7, y & 7)]
        return self._st[k] + self.extra.get(k, [])

    def iflags(self, sid):
        return self.T.sflags[sid]

    def calch(self, sid):
        h = self.T.sheight[sid]
        return h // 2 if self.T.sflags[sid] & BRIDGE_ else h

    def avgz(self, x, y):
        zt = self.land(x, y)[1]
        zl = self.land(x, y + 1)[1]
        zr = self.land(x + 1, y)[1]
        zb = self.land(x + 1, y + 1)[1]
        z = min(zt, zl, zr, zb)
        top = max(zt, zl, zr, zb)

        def fa(a, b):  # Map.FloorAverage, C# division truncating toward zero
            v = a + b
            if v < 0:
                v -= 1
            return int(v / 2)

        avg = fa(zl, zr) if abs(zt - zb) > abs(zl - zr) else fa(zt, zb)
        return z, avg, top


def ignored(lid):
    return lid in (2, 0x1DB) or 0x1AE <= lid <= 0x1B5


def is_ok(w, ourZ, ourTop, x, y):
    for sid, sz in w.statics(x, y):
        if w.iflags(sid) & (IMP_ | SURF_):  # ItemData.ImpassableSurface: either flag
            if sz + w.calch(sid) > ourZ and ourTop > sz:
                return False
    return True


def check(w, x, y, startTop, startZ, mZ):
    newZ = 0
    lid, _ = w.land(x, y)
    landBlocks = bool(w.T.lflags[lid & 0x3FFF] & IMP_)  # cantWalk false, canSwim false
    considerLand = not ignored(lid)
    landZ, landCenter, _ = w.avgz(x, y)
    moveIsOk = False
    stepTop = startTop + STEP
    checkTop = startZ + PERSON
    for sid, sz in w.statics(x, y):
        f = w.iflags(sid)
        if not (f & SURF_) or (f & IMP_):  # canSwim false
            continue
        itemZ = sz
        itemTop = itemZ
        ourZ = itemZ + w.calch(sid)
        testTop = checkTop
        if moveIsOk:
            cmp = abs(ourZ - mZ) - abs(newZ - mZ)
            if cmp > 0 or (cmp == 0 and ourZ > newZ):
                continue
        if ourZ + PERSON > testTop:
            testTop = ourZ + PERSON
        if not (f & BRIDGE_):
            itemTop += w.T.sheight[sid]
        if stepTop < itemTop:
            continue
        landCheck = itemZ + min(w.T.sheight[sid], STEP)
        if considerLand and landCheck < landCenter and landCenter > ourZ and testTop > landZ:
            continue
        if is_ok(w, ourZ, testTop, x, y):
            newZ = ourZ
            moveIsOk = True
    if not considerLand or landBlocks or stepTop < landZ:
        return moveIsOk, newZ
    testTop = checkTop
    if landCenter + PERSON > testTop:
        testTop = landCenter + PERSON
    shouldCheck = True
    if moveIsOk:
        cmp = abs(landCenter - mZ) - abs(newZ - mZ)
        if cmp > 0 or (cmp == 0 and landCenter > newZ):
            shouldCheck = False
    if shouldCheck and is_ok(w, landCenter, testTop, x, y):
        newZ = landCenter
        moveIsOk = True
    return moveIsOk, newZ


def start_z(w, x, y, z):
    lid, _ = w.land(x, y)
    landBlocks = bool(w.T.lflags[lid & 0x3FFF] & IMP_)
    landZ, landCenter, landTop = w.avgz(x, y)
    considerLand = not ignored(lid)
    zCenter = zLow = zTop = 0
    isSet = False
    if considerLand and not landBlocks and z >= landCenter:
        zLow, zCenter, zTop, isSet = landZ, landCenter, landTop, True
    for sid, sz in w.statics(x, y):
        calcTop = sz + w.calch(sid)
        if (isSet and calcTop < zCenter) or z < calcTop or not (w.iflags(sid) & SURF_):
            continue
        zLow = sz
        zCenter = calcTop
        top = sz + w.T.sheight[sid]
        if not isSet or top > zTop:
            zTop = top
        isSet = True
    if not isSet:
        zLow = zTop = z
    elif z > zTop:
        zTop = z
    return zLow, zTop


OFF = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]  # N, Right, E, Down, S, Left, W, Up


def check_movement(w, x, y, z, d):
    fx, fy = x + OFF[d][0], y + OFF[d][1]
    lx, ly = x + OFF[(d - 1) & 7][0], y + OFF[(d - 1) & 7][1]
    rx, ry = x + OFF[(d + 1) & 7][0], y + OFF[(d + 1) & 7][1]
    sZ, sTop = start_z(w, x, y, z)
    ok, nz = check(w, fx, fy, sTop, sZ, z)
    if ok and (d & 1):  # a player below GameMaster needs both sides of a diagonal clear
        if not check(w, lx, ly, sTop, sZ, z)[0] or not check(w, rx, ry, sTop, sZ, z)[0]:
            ok = False
    return ok, fx, fy, nz


BOX = (898, 808, 1280, 1231)  # DungeonRegion "Underworld", regions.json:3938


def inbox(x, y):
    return BOX[0] <= x <= BOX[2] and BOX[1] <= y <= BOX[3]


def teleporters():
    tp = json.load(open(r'D:/UO/ModernUO-pinned/Distribution/Data/teleporters.json'))
    srcs = {}
    entries = []
    for t in tp:
        s, d = t.get('src', {}), t.get('dst', {})
        sin = s.get('map') == 'TerMur' and inbox(s['loc'][0], s['loc'][1])
        din = d.get('map') == 'TerMur' and inbox(d['loc'][0], d['loc'][1])
        if din and not sin:
            entries.append((s.get('map'), tuple(s.get('loc', [])), tuple(d['loc'])))
        if sin and d.get('map') == 'TerMur':
            srcs[(s['loc'][0], s['loc'][1])] = tuple(d['loc'])
    return entries, srcs


def walk(w, starts, srcs):
    seen = {}
    q = deque()
    for st in starts:
        if (st[0], st[1]) not in seen:
            seen[(st[0], st[1])] = (st[2], None)
            q.append(st)
    while q:
        x, y, z = q.popleft()
        for d in range(8):
            ok, fx, fy, nz = check_movement(w, x, y, z, d)
            if not ok or not inbox(fx, fy):
                continue
            nxt = [(fx, fy, nz)]
            if (fx, fy) in srcs:
                nxt.append(srcs[(fx, fy)])
            for p in nxt:
                if (p[0], p[1]) not in seen:
                    seen[(p[0], p[1])] = (p[2], (x, y))
                    q.append(p)
    return seen


def path(seen, x, y):
    out = []
    k = (x, y)
    while k is not None:
        out.append((k[0], k[1], seen[k][0]))
        k = seen[k][1]
    return out[::-1]
