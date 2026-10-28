# cc-P281: the walk model for the guild hall checks, from the client files and pinned's world data (read only).
#
# A tile's standable heights: its land (pinned GetAverageZ, if the land is not impassable or ignored) and the top of every
# Surface static on it, kept only where pinned CanFit's blocked test passes (no impassable or surface static, and no
# impassable decoration item, crossing z..z+16). Doors are passable: the generator's and the decoration files' doors
# are items, not statics, and a Door-flagged static (Ter Mur, Tokuno) counts as open. A step goes to any of the 8
# neighbours whose height is within STEP of this one (STEP_BRIDGE onto or off a Bridge piece). That is coarser than pinned Movement.Check (it ignores the
# diagonal corner rule and stair geometry), so it proves "there is a way", and the screenshots and a walk in game prove
# the rest.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hallbase as H  # noqa: E402

STEP = 3
STEP_BRIDGE = 10   # a step onto or off a Bridge static (stairs, stilt ladders), which pinned climbs by half its height
BLOCKER_TYPES = ('Bookcase', 'Barrel', 'Crate', 'Armoire', 'Drawer', 'Dummy', 'Butte', 'Addon', 'LampPost', 'Forge',
                 'Anvil', 'Loom', 'Wheel', 'Chest', 'Table', 'Counter', 'Throne', 'Tree', 'Statue', 'Fountain')


def deco_blockers(fi, x1, y1, x2, y2):
    """{(x, y): [(z, top, what)]} decoration items that block a walker, and the set of decoration door tiles."""
    block, doors = {}, set()
    for (x, y, z, typ, iid, f) in H.decoration_in(fi, x1, y1, x2, y2):
        if 'Door' in typ or 'Gate' in typ:
            doors.add((x, y))
            continue
        h = None
        try:
            i = int(iid, 16)
            if H.iflags(i) & H.IMP:
                h = max(H.calch(i), 1)
        except ValueError:
            if any(b in typ for b in BLOCKER_TYPES):
                h = 16
        if h:
            block.setdefault((x, y), []).append((z, z + h, typ))
    return block, doors


class Walk:
    def __init__(self, fi, rect, pad=8, zlo=-128, zhi=127):
        self.F = H.Facet(fi) if not isinstance(fi, H.Facet) else fi
        self.fi = self.F.fi
        x1, y1, x2, y2 = rect
        self.box = (x1 - pad, y1 - pad, x2 + pad, y2 + pad)
        self.block, self.deco_doors = deco_blockers(self.fi, *self.box)
        self.gen_doors = {(x, y): (z, f) for (x, y, z, f) in H.generated_doors(self.F, *self.box)}
        self.static_doors = {(x, y) for (x, y, z, i) in H.static_doors(self.F, *self.box)}
        self.zlo, self.zhi = zlo, zhi
        self.extra = {}      # (x, y) -> [(z, top)] our own placed blockers (a guildmaster, decor)
        self._stand = {}
        self._bridge = {}

    def door_tiles(self):
        return set(self.gen_doors) | self.deco_doors | self.static_doors

    def fits(self, x, y, z):
        F = self.F
        lid, _ = F.land(x, y)
        for sid, sz in F.statics(x, y):
            f = H.iflags(sid)
            if f & H.DOOR:
                continue
            if (f & H.IMP or f & H.SURF) and sz < z + 16 and sz + H.calch(sid) > z:
                return False
        for (bz, top, _) in self.block.get((x, y), ()):
            if bz < z + 16 and top > z:
                return False
        for (bz, top) in self.extra.get((x, y), ()):
            if bz < z + 16 and top > z:
                return False
        return True

    def heights(self, x, y):
        k = (x, y)
        if k in self._stand and not self.extra:
            return self._stand[k]
        F = self.F
        cand = set()
        lid, _ = F.land(x, y)
        if not F.ignored_land(lid) and not H.LAND[lid][0] & H.IMP and not H.LAND[lid][0] & H.WET:
            cand.add(F.avgz(x, y))
        for sid, sz in F.statics(x, y):
            f = H.iflags(sid)
            if f & H.SURF and not f & H.IMP:
                cand.add(sz + H.calch(sid))
        out = sorted(z for z in cand if self.zlo <= z <= self.zhi and self.fits(x, y, z))
        if not self.extra:
            self._stand[k] = out
        return out

    def bridge_heights(self, x, y):
        k = (x, y)
        if k not in self._bridge:
            self._bridge[k] = {sz + H.calch(sid) for sid, sz in self.F.statics(x, y) if H.iflags(sid) & H.BRIDGE}
        return self._bridge[k]

    def flood(self, start):
        """Every (x, y, z) reachable from start (x, y, z) inside the box."""
        x1, y1, x2, y2 = self.box
        sx, sy, sz = start
        hs = self.heights(sx, sy)
        if not hs:
            return set()
        z0 = min(hs, key=lambda h: abs(h - sz))
        seen = {(sx, sy, z0)}
        todo = [(sx, sy, z0)]
        while todo:
            x, y, z = todo.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if (dx or dy) and x1 <= nx <= x2 and y1 <= ny <= y2:
                        for nz in self.heights(nx, ny):
                            step = STEP_BRIDGE if (z in self.bridge_heights(x, y) or nz in self.bridge_heights(nx, ny)) else STEP
                            if abs(nz - z) <= step and (nx, ny, nz) not in seen:
                                seen.add((nx, ny, nz))
                                todo.append((nx, ny, nz))
        return seen
