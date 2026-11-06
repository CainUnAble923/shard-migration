"""cc-P799: a line-for-line Python port of pinned Projects/UOContent/Engines/Pathing/Movement.cs (CheckMovement, Check, IsOk,
GetStartZ) for a living player below GameMaster, over the client's land and statics plus the immovable items we know of:
stock Decoration cfg items and the release's mine camp pieces. Doors (generated, decoration, static) count as passable:
the client opens them on the way. Mobiles are ignored.

The BFS is 8-way with the player's diagonal rule (both side tiles must pass Check), one step per move, walking speed not
counted. Results are cached in bfs-<tag>.pkl next to the script. Read only.

    P799_CLIENT / P799_DATA pick the client and the Decoration root (default: stock).
    import move; W = move.World(); W.bfs((3503,2574,14)); W.steps(x,y,z); W.path(x,y,z)
"""
import os
import pickle
import re
from collections import deque

import hallbase as H

IMP, WET, SURF, BRIDGE, DOORF = 0x40, 0x80, 0x200, 0x400, 1 << 29
PERSON = 16
STEPH = 2
DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]  # N NE E SE S SW W NW (Direction 0-7)
HERE = os.path.dirname(os.path.abspath(__file__))
ISLE = (3370, 2430, 3770, 2830)


def fa(a, b):
    v = a + b
    if v < 0:
        v -= 1
    return int(v / 2)


class World:
    def __init__(self, box=ISLE, camp=True, fi=1):
        self.F = H.Facet(fi)
        self.box = box
        self._st = {}
        self._it = {}
        self.dist = {}
        self.prev = {}
        x1, y1, x2, y2 = box
        self.doors = {(x, y) for (x, y, z, f) in H.generated_doors(self.F, x1, y1, x2, y2)}
        for (x, y, z, typ, iid, f) in H.decoration_in(fi, x1, y1, x2, y2):
            if 'Door' in typ or 'Gate' in typ:
                self.doors.add((x, y))
                continue
            try:
                i = int(iid, 16) & 0x3FFF
            except ValueError:
                continue
            self.add_item(x, y, z, i)
        if camp:
            self.add_camp()

    def add_item(self, x, y, z, i):
        if H.iflags(i) & (IMP | SURF):
            self._it.setdefault((x, y), []).append((i, z))

    def add_camp(self):
        p = 'D:/UO/golems/Iron/p799-isle/server/customizations/ClusterFMineCampLayout.cs'
        if os.path.exists(p):
            for m in re.finditer(r'new\("\w+", 0x([0-9A-Fa-f]+), "[^"]*", (\d+), (\d+), (-?\d+)\)', open(p, encoding='utf-8').read()):
                self.add_item(int(m[2]), int(m[3]), int(m[4]), int(m[1], 16))

    def st(self, x, y):
        k = (x, y)
        if k not in self._st:
            self._st[k] = self.F.statics(x, y)
        return self._st[k]

    def ground(self, x, y):
        """(low, centre, top) as Map.GetAverageZ."""
        L = self.F.landz
        t, l, r, b = L(x, y), L(x, y + 1), L(x + 1, y), L(x + 1, y + 1)
        c = fa(l, r) if abs(t - b) > abs(l - r) else fa(t, b)
        return min(t, l, r, b), c, max(t, l, r, b)

    def isok(self, ourz, ourtop, x, y):
        for s, z in self.st(x, y):
            f = H.iflags(s)
            if f & DOORF:          # a static door: open
                continue
            if f & (IMP | SURF):
                if z + H.calch(s) > ourz and ourtop > z:
                    return False
        for s, z in self._it.get((x, y), ()):
            if H.iflags(s) & (IMP | SURF):
                if z + H.calch(s) > ourz and ourtop > z:
                    return False
        return True

    def startz(self, x, y, lz):
        lid, _ = self.F.land(x, y)
        blocks = bool(H.LAND[lid][0] & IMP)
        low, centre, top = self.ground(x, y)
        consider = not self.F.ignored_land(lid)
        zl = zt = zc = 0
        isset = False
        if consider and not blocks and lz >= centre:
            zl, zc, zt = low, centre, top
            isset = True
        for s, z in list(self.st(x, y)) + list(self._it.get((x, y), ())):
            f = H.iflags(s)
            ct = z + H.calch(s)
            if (isset and ct < zc) or lz < ct or not f & SURF:
                continue
            zl, zc = z, ct
            t = z + H.iheight(s)
            if not isset or t > zt:
                zt = t
            isset = True
        if not isset:
            zl = zt = lz
        elif lz > zt:
            zt = lz
        return zl, zt

    def check(self, x, y, startz, starttop, mz):
        lid, _ = self.F.land(x, y)
        blocks = bool(H.LAND[lid][0] & IMP)
        consider = not self.F.ignored_land(lid)
        low, centre, _ = self.ground(x, y)
        ok = False
        newz = 0
        steptop = starttop + STEPH
        checktop = startz + PERSON
        for s, z in list(self.st(x, y)) + list(self._it.get((x, y), ())):
            f = H.iflags(s)
            if not f & SURF or f & IMP:
                continue
            itemtop = z
            ourz = z + H.calch(s)
            testtop = checktop
            if ok:
                cmp = abs(ourz - mz) - abs(newz - mz)
                if cmp > 0 or (cmp == 0 and ourz > newz):
                    continue
            if ourz + PERSON > testtop:
                testtop = ourz + PERSON
            if not f & BRIDGE:
                itemtop += H.iheight(s)
            if steptop < itemtop:
                continue
            landcheck = z + min(H.iheight(s), STEPH)
            if consider and landcheck < centre and centre > ourz and testtop > low:
                continue
            if self.isok(ourz, testtop, x, y):
                newz = ourz
                ok = True
        if not consider or blocks or steptop < low:
            return ok, newz
        testtop = checktop
        if centre + PERSON > testtop:
            testtop = centre + PERSON
        should = True
        if ok:
            cmp = abs(centre - mz) - abs(newz - mz)
            if cmp > 0 or (cmp == 0 and centre > newz):
                should = False
        if should and self.isok(centre, testtop, x, y):
            newz = centre
            ok = True
        return ok, newz

    def move(self, x, y, z, d):
        dx, dy = DIRS[d]
        sz, st = self.startz(x, y, z)
        ok, nz = self.check(x + dx, y + dy, sz, st, z)
        if not ok:
            return None
        if d & 1:
            lx, ly = DIRS[(d - 1) & 7]
            rx, ry = DIRS[(d + 1) & 7]
            if not self.check(x + lx, y + ly, sz, st, z)[0] or not self.check(x + rx, y + ry, sz, st, z)[0]:
                return None
        return nz

    def bfs(self, start=(3503, 2574, 14), tag='stock'):
        p = os.path.join(HERE, 'bfs-%s.pkl' % tag)
        if os.path.exists(p):
            self.dist, self.prev = pickle.load(open(p, 'rb'))
            return
        x1, y1, x2, y2 = self.box
        self.dist = {start: 0}
        self.prev = {start: None}
        q = deque([start])
        while q:
            c = q.popleft()
            x, y, z = c
            for d in range(8):
                nx, ny = x + DIRS[d][0], y + DIRS[d][1]
                if not (x1 <= nx <= x2 and y1 <= ny <= y2):
                    continue
                nz = self.move(x, y, z, d)
                if nz is None:
                    continue
                n = (nx, ny, nz)
                if n not in self.dist:
                    self.dist[n] = self.dist[c] + 1
                    self.prev[n] = c
                    q.append(n)
        pickle.dump((self.dist, self.prev), open(p, 'wb'))

    def zs(self, x, y):
        return sorted(k[2] for k in self.dist if k[0] == x and k[1] == y)

    def steps(self, x, y, z):
        return self.dist.get((x, y, z))

    def path(self, x, y, z):
        c = (x, y, z)
        out = []
        while c:
            out.append(c)
            c = self.prev.get(c)
        return out[::-1]

    def gridmap(self, x0, y0, x1, y1, doors=True):
        """Reachable floor: Z of the tile mod 100 as two digits (or .. = unreachable), DD = a door tile, per tile."""
        byxy = {}
        for (x, y, z), d in self.dist.items():
            if x0 <= x <= x1 and y0 <= y <= y1:
                byxy.setdefault((x, y), []).append(z)
        head = '      ' + ''.join('%3d' % (x % 100) for x in range(x0, x1 + 1))
        rows = [head]
        for y in range(y0, y1 + 1):
            r = '%5d ' % y
            for x in range(x0, x1 + 1):
                zs = byxy.get((x, y))
                if doors and (x, y) in self.doors:
                    r += ' DD' if zs else ' dd'
                elif zs:
                    r += '%3d' % max(zs)
                else:
                    r += '  .'
            rows.append(r)
        return '\n'.join(rows)


LETTER = {'grass': 'g', 'forest': 'f', 'dirt': 'd', 'cobblestones': 'c', 'rock': 'R', 'sand': 's', 'water': '~', 'wooden floor': 'w',
          'flagstone': 'F', 'stone': 't', 'brick': 'b', 'tile': 'T', 'planks': 'p', 'furrows': 'u', 'NoName': '?', 'void': ' ', 'jungle': 'j'}


def landmap(W, x0, y0, x1, y1):
    """Land name letters; upper layer: # = wall/impassable static over the tile at floor height, o = other static."""
    rows = ['      ' + ''.join(str(x // 10 % 10) if x % 10 == 0 else str(x % 10) for x in range(x0, x1 + 1))]
    for y in range(y0, y1 + 1):
        r = ''
        for x in range(x0, x1 + 1):
            lid = W.F.land(x, y)[0]
            c = LETTER.get(H.lname(lid), '?')
            st = W.st(x, y)
            if any(H.iflags(s) & IMP and H.iheight(s) > 2 for s, z in st):
                c = '#'
            r += c
        rows.append('%5d %s' % (y, r))
    return '\n'.join(rows)


def gridz(W, x0, y0, x1, y1, zlo, zhi):
    """Reachable floor between zlo and zhi only: the Z, or '.'; door tiles dd/DD."""
    byxy = {}
    for (x, y, z), d in W.dist.items():
        if x0 <= x <= x1 and y0 <= y <= y1 and zlo <= z <= zhi:
            byxy[(x, y)] = z
    rows = ['      ' + ''.join('%3d' % (x % 100) for x in range(x0, x1 + 1))]
    for y in range(y0, y1 + 1):
        r = '%5d ' % y
        for x in range(x0, x1 + 1):
            z = byxy.get((x, y))
            r += (' DD' if z is not None else ' dd') if (x, y) in W.doors else ('  .' if z is None else '%3d' % z)
        rows.append(r)
    return '\n'.join(rows)
