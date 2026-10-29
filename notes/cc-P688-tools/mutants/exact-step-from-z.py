r"""cc-P688 (SoS swap S15): pinned Movement.cs step by step over one rectangle of the map files, every level of a tile
kept apart (walkgrid.py keeps one level a tile, so it cannot follow a walker from a z14 floor onto z13 logs at
Papua's bank door, or up a castle's floors). For the places the whole-map survey leaves alone: is it the map, or the
survey?

A walker is (x, y, z). A step in one of 8 directions (Movement.cs CheckMovement :40-181, Check :236-484, GetStartZ
:487-581, IsOk; pinned Map.GetAverageZ):
  GetStartZ at (x, y, z): the land when z >= its centre, then each Surface with calcTop <= z and >= the centre so far:
    zLow, zTop (the highest z + height), zTop at least z. stepTop = zTop + 2, checkTop = zLow + 16.
  Candidates on the next tile: each walkable Surface static (not Impassable) with itemTop (z + height, a Bridge's z)
    <= stepTop, ourZ = z + CalcHeight, not buried (landCheck), and the land when walkable and landZ (the low corner)
    <= stepTop, ourZ = the land's centre. Each must pass IsOk: no Impassable or Surface static overlapping
    (ourZ, max(checkTop, ourZ + 16)). Of those that pass, the walker takes the one closest to its own z (a tie: lower).
  A diagonal also needs both side tiles to pass from the same start (a player below GameMaster).
Not modelled: doors and other items (decoration), mobiles, multis. Static doors are statics: they block, as in game.

    python -P exact.py x1 y1 x2 y2 sx sy sz gx gy     -> reached or not, the path length, the nearest the walk came
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # MUTANT copy lives in mutants/
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P678-tools"))
import soswalk  # noqa: E402  (its files(): the SoS land, statics and tiledata)

IMP, WET, SURF, BRIDGE = 0x40, 0x80, 0x200, 0x400
PERSON, STEP = 16, 2
DIRS = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))   # N NE E SE S SW W NW


class Exact:
    def __init__(self, rect, files=None):
        f = files or soswalk.files()
        self.f = f
        self.items = f["items"]
        self.land = f["land"]
        self.rect = x1, y1, x2, y2 = rect
        m = (f["sx"] >= x1 - 1) & (f["sx"] <= x2 + 1) & (f["sy"] >= y1 - 1) & (f["sy"] <= y2 + 1)
        self.sts = collections.defaultdict(list)
        for x, y, z, i in zip(f["sx"][m], f["sy"][m], f["sz"][m], f["sid"][m]):
            it = self.items[int(i)]
            self.sts[(int(x), int(y))].append((int(z), it["flags"], it["height"]))

    def inside(self, x, y):
        x1, y1, x2, y2 = self.rect
        return x1 <= x <= x2 and y1 <= y <= y2

    def avgz(self, x, y):
        zs = self.f["zs"]
        t, l, r, b = int(zs[x, y]), int(zs[x, y + 1]), int(zs[x + 1, y]), int(zs[x + 1, y + 1])
        avg = (l + r) // 2 if abs(t - b) > abs(l - r) else (t + b) // 2
        return min(t, l, r, b), avg, max(t, l, r, b)

    def land_blocks(self, x, y):
        return bool(self.land[int(self.f["ids"][x, y])][0] & IMP)

    def start(self, x, y, z):
        """GetStartZ: (zLow, zTop)."""
        landz, center, landtop = self.avgz(x, y)
        isset, zlow, ztop, zc = False, 0, 0, 0
        if not self.land_blocks(x, y) and z >= center:
            zlow, zc, ztop, isset = landz, center, landtop, True
        for sz, fl, h in self.sts.get((x, y), ()):
            calc = sz + (h // 2 if fl & BRIDGE else h)
            if (isset and calc < zc) or z < calc or not fl & SURF:
                continue
            zlow, zc = sz, calc
            if not isset or sz + h > ztop:
                ztop = sz + h
            isset = True
        if not isset:
            return z, z
        return zlow, max(ztop, z)

    def is_ok(self, x, y, ourz, testtop):
        for sz, fl, h in self.sts.get((x, y), ()):
            if fl & (IMP | SURF):
                top = sz + (h // 2 if fl & BRIDGE else h)
                if top > ourz and testtop > sz:
                    return False
        return True

    def check(self, x, y, z, startz, starttop):
        """Movement.Check onto (x, y) for a walker at z: the new z, or None."""
        steptop, checktop = z + STEP, startz + PERSON   # MUTANT: the step from the walker's z, not GetStartZ's zTop
        landz, center, _ = self.avgz(x, y)
        best = None
        for sz, fl, h in self.sts.get((x, y), ()):
            if not fl & SURF or fl & IMP:
                continue
            ourz = sz + (h // 2 if fl & BRIDGE else h)
            itemtop = sz if fl & BRIDGE else sz + h
            if steptop < itemtop:
                continue
            testtop = max(checktop, ourz + PERSON)
            if sz + min(h, STEP) < center and center > ourz and testtop > landz:
                continue
            if best is not None and (abs(ourz - z) > abs(best - z) or (abs(ourz - z) == abs(best - z) and ourz > best)):
                continue
            if self.is_ok(x, y, ourz, testtop):
                best = ourz
        if not self.land_blocks(x, y) and steptop >= landz:
            testtop = max(checktop, center + PERSON)
            if best is None or abs(center - z) < abs(best - z) or (abs(center - z) == abs(best - z) and center < best):
                if self.is_ok(x, y, center, testtop):
                    best = center
        return best

    def moves(self, x, y, z):
        startz, starttop = self.start(x, y, z)
        for d, (dx, dy) in enumerate(DIRS):
            nx, ny = x + dx, y + dy
            if not self.inside(nx, ny):
                continue
            nz = self.check(nx, ny, z, startz, starttop)
            if nz is None:
                continue
            if dx and dy:
                if self.check(x + dx, y, z, startz, starttop) is None or self.check(x, y + dy, z, startz, starttop) is None:
                    continue
            yield nx, ny, nz

    def flood(self, sx, sy, sz, goal=None, limit=2_000_000):
        q = collections.deque([(sx, sy, sz)])
        prev = {(sx, sy, sz): None}
        while q and len(prev) < limit:
            c = q.popleft()
            if goal and (c[0], c[1]) == goal:
                return prev, c
            for n in self.moves(*c):
                if n not in prev:
                    prev[n] = c
                    q.append(n)
        return prev, None


def walk(rect, start, goal):
    """(reached, path length or None, nearest (x, y) to the goal, tiles reached)."""
    e = Exact(rect)
    prev, end = e.flood(start[0], start[1], start[2], goal)
    tiles = {(x, y) for x, y, _ in prev}
    near = min(tiles, key=lambda t: max(abs(t[0] - goal[0]), abs(t[1] - goal[1])))
    if end is None:
        return False, None, near, len(tiles)
    n, c = 0, end
    while c is not None:
        n += 1
        c = prev[c]
    return True, n, near, len(tiles)


if __name__ == "__main__":
    a = [int(v) for v in sys.argv[1:10]]
    print(walk(tuple(a[:4]), tuple(a[4:7]), tuple(a[7:9])))
