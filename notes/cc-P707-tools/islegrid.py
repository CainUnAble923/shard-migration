"""cc-P707: cc-P480's walk grid, with one change for the isle: a surface static (dock planks, a bridge) over water or
impassable land is standable, as pinned Movement.cs lets a mobile stand on a surface item whatever the land under it.
P480's grid (New Haven's plaza) rejected the tile on its land flags first, so the dock was a wall."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "cc-P480-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))
import playthrough as base

IMP, WET, SURF, PERSON = base.IMP, base.WET, base.SURF, base.PERSON


def _tile(self, x, y, sts):
    t = self.m.get(x, y)
    land_ok = not (self.land[t[0]][0] & (IMP | WET))
    zs = [self.m.get(x, y)[1], self.m.get(x + 1, y)[1], self.m.get(x, y + 1)[1], self.m.get(x + 1, y + 1)[1]]
    z = (min(zs) + max(zs)) // 2
    top, low, hi = (z, min(zs), max(zs)) if land_ok else (None, None, None)
    for s in sts:
        it = self.items[s[3]]
        if it["flags"] & SURF and (top is None or (s[2] + it["height"] >= top and s[2] <= z + PERSON)):
            st = s[2] + it["height"]
            top, low, hi = (st, s[2], st) if top is None else (max(top, st), s[2], max(top, st))
    if top is None:
        return None, None, None
    for s in sts:
        it = self.items[s[3]]
        if (it["flags"] & IMP) and not (it["flags"] & SURF) and s[2] < top + PERSON and s[2] + max(it["height"], 1) > top:
            return None, None, None
    return top, low, hi


base.Grid._tile = _tile
Grid = base.Grid
