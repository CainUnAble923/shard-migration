"""Land slope audit (cc-P181): finds ring steps and spikes the way vseUOAware's diagnose_land_transitions reports
them (each tile's four corner Z values: top = this tile, right = x+1, left = y+1, bottom = x+1,y+1), but over a whole
build and with the noise of weighted floor ids left out.

A tile is flagged when the spread of its four corners exceeds `limit`, unless all four tiles are void (black on
black is invisible). The Burrows' rings are built as floor 0 | rock 0 | rock +12 | void +20, so a correct ring has
spreads of 12 and 8; a 20 means the +12 ramp is missing beside a +20 tile (a spike or a cliff), which happens at
ring corners when the ramp ring is thinner than one tile diagonally."""


def corner_z(land, x, y, default=None):
    z = land.get((x, y))
    if z is None:
        return None
    own = z[1]
    g = lambda c: land[c][1] if c in land else (own if default is None else default)
    return own, g((x + 1, y)), g((x, y + 1)), g((x + 1, y + 1))


def slope_audit(land, limit=12, void=0x0244, outside_z=None):
    """[(x, y, spread, (top, right, left, bottom))] for the tiles whose corner spread exceeds limit. `land` is
    {(x, y): (id, z)}; tiles outside it count as their own Z (outside_z None) or as outside_z."""
    out = []
    for (x, y), (tid, z) in land.items():
        ids = [land.get(c, (void, None))[0] for c in ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1))]
        if all(i == void for i in ids):
            continue
        top, right, left, bottom = corner_z(land, x, y, outside_z)
        spread = max(top, right, left, bottom) - min(top, right, left, bottom)
        if spread > limit:
            out.append((x, y, spread, (top, right, left, bottom)))
    return out


def summary(flags):
    """A short text for the notes."""
    if not flags:
        return "slope audit: no tile over the limit"
    worst = max(f[2] for f in flags)
    return "slope audit: %d tiles over the limit, worst spread %d, first %s" % (len(flags), worst, flags[:5])
