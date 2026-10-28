r"""cc-P681: the whole SoS Trammel map as arrays, for grading 4,304 stock spawners at once.
The playbook's walk rules (cc-P188 build_way_in.Walk, cc-P678 soswalk.py: pinned Movement.cs reduced to the files),
vectorized over the map:
  stand[x, y]  the standing Z on the tile, or NONE when land is Impassable or Wet with no surface over it, or an
               Impassable non-Surface static overlaps the walker's 16 above the standing Z;
  wet[x, y]    the land is Wet (water) and no surface stands over it (sea creatures' ground);
  covered[x,y] a static stands 10 or more above the standing Z (a roof or an upper floor: inside a building);
  terrain[x,y] the land tile's terrain class (TERRAINS), from its tiledata name, on SoS; stock_terrain the same on the
               stock Trammel and Felucca maps, for what a spawner was designed for.
The surface pass takes the highest surface top within 16 above the land (soswalk's loop takes them in file order; the
two differ only where surfaces stack more than 16 apart, which a standing check does not reach). GetAverageZ is
pinned's (the diagonal with the smaller slope, halved toward zero).
    python -P sosgrid.py        builds the cache (CACHE, about 400 MB, outside the repo) and prints a summary
Use: import sosgrid; g = sosgrid.load()
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(NOTES), "scripts"))
import islands  # noqa: E402
from mapbuild import uofiles  # noqa: E402

CACHE = os.environ.get("P681_CACHE", r"C:\Users\ckfle\AppData\Local\Temp\p681-sosgrid")
IMP, WET, SURF, BRIDGE = 0x40, 0x80, 0x200, 0x400
PERSON = 16
NONE = -32768
W, H = 7168, 4096

# terrain classes by tiledata land name (first match wins)
TERRAINS = [
    ("water", ("water",)),
    ("void", ("nodraw", "void")),
    ("snow", ("snow", "ice")),
    ("swamp", ("swamp",)),
    ("jungle", ("jungle",)),
    ("sand", ("sand", "desert", "beach")),
    ("lava", ("lava",)),
    ("cave", ("cave", "dungeon")),
    ("rock", ("rock", "mountain", "stone")),
    ("forest", ("forest", "leaves")),
    ("grass", ("grass",)),
    ("dirt", ("dirt", "furrow", "mud")),
    ("road", ("cobble", "road", "paver", "brick", "marble", "tile", "flagstone")),
    ("floor", ("floor", "wood", "plank", "carpet")),
]
CLASS_NAMES = [t for t, _ in TERRAINS] + ["other"]


def classify(name):
    n = (name or "").lower()
    for i, (_, words) in enumerate(TERRAINS):
        if any(w in n for w in words):
            return i
    return len(TERRAINS)


def tables():
    land, items = uofiles.read_tiledata(uofiles.CLIENT)
    lflags = np.array([l[0] for l in land], dtype=np.uint64)
    lclass = np.array([classify(l[2]) for l in land], dtype=np.int8)
    iflags = np.array([it["flags"] for it in items], dtype=np.uint64)
    iheight = np.array([it["height"] for it in items], dtype=np.int16)
    return lflags, lclass, iflags, iheight


def average_z(zs):
    """pinned GetAverageZ for every tile (the map's last row and column use themselves)."""
    z = zs.astype(np.int32)
    t = z
    r = np.vstack([z[1:, :], z[-1:, :]])          # x + 1
    l = np.hstack([z[:, 1:], z[:, -1:]])          # y + 1
    b = np.vstack([l[1:, :], l[-1:, :]])          # x + 1, y + 1
    lr = np.trunc((l + r) / 2).astype(np.int32)
    tb = np.trunc((t + b) / 2).astype(np.int32)
    return np.where(np.abs(t - b) > np.abs(l - r), lr, tb)


def build(name="sos"):
    lflags, lclass, iflags, iheight = tables()
    ids, zs = islands.load_land(name)
    sx, sy, sz, sid = islands.load_statics(name)
    if ids.shape[0] < W:          # stock Felucca's file is the old 6144 wide; pad with void
        ids = np.pad(ids, ((0, W - ids.shape[0]), (0, 0)), constant_values=0x244)
        zs = np.pad(zs, ((0, W - zs.shape[0]), (0, 0)))
    sx, sy, sz, sid = sx.astype(np.int64), sy.astype(np.int64), sz.astype(np.int32), sid.astype(np.int64)
    sid = np.minimum(sid, len(iflags) - 1)
    lf = lflags[ids]
    avg = average_z(zs)
    land_ok = ((lf & np.uint64(IMP)) == 0) & ((lf & np.uint64(WET)) == 0)
    wet_land = (lf & np.uint64(WET)) != 0
    flat = sx * H + sy
    f = iflags[sid]
    h = iheight[sid].astype(np.int32)
    is_surf = (f & np.uint64(SURF)) != 0
    is_imp = (f & np.uint64(IMP)) != 0
    base = avg.reshape(-1)[flat]
    ok = land_ok.reshape(-1)[flat]
    # surfaces: on dry land, those whose top is at or above the land and that start within 16 above it; over water or
    # rock, any surface
    top_c = sz + h
    use = is_surf & ((~ok) | ((top_c >= base) & (sz <= base + PERSON)))
    top = np.where(land_ok, avg, NONE).astype(np.int32).reshape(-1)
    np.maximum.at(top, flat[use], top_c[use])
    has = top != NONE
    # blocking: an impassable non-surface static overlapping 16 above the standing Z
    tt = top[flat]
    blk = is_imp & ~is_surf & has[flat] & (sz < tt + PERSON) & (sz + np.maximum(h, 1) > tt)
    blocked = np.zeros(W * H, dtype=bool)
    blocked[flat[blk]] = True
    stand = np.where(has & ~blocked, top, NONE).astype(np.int16).reshape(W, H)
    # covered: any static 10 or more above the standing Z
    cov = np.zeros(W * H, dtype=bool)
    st = stand.reshape(-1)[flat].astype(np.int32)
    roof = (st != NONE) & (sz >= st + 10)
    cov[flat[roof]] = True
    surfaced = np.zeros(W * H, dtype=bool)
    surfaced[flat[is_surf]] = True
    wet = (wet_land.reshape(-1) & ~surfaced).reshape(W, H)
    terrain = lclass[ids]
    out = dict(stand=stand, wet=wet, covered=cov.reshape(W, H), terrain=terrain)
    for name in ("trammel", "felucca"):
        sids, _ = islands.load_land(name)
        out["terrain_" + name] = lclass[sids][:W, :H] if sids.shape[0] >= W else np.pad(lclass[sids], ((0, W - sids.shape[0]), (0, 0)))
    return out


class Surfaces:
    """Every standable Z on a tile (not only the highest, as stand holds): the land, when walkable, and each surface
    static's top, each with no impassable non-surface static overlapping the 16 above it. For spawners that stand
    still (range 0 or 1), whose Z picks one floor of a building."""

    def __init__(self, name="sos"):
        lflags, _, iflags, iheight = tables()
        self.ids, zs = islands.load_land(name)
        self.avg = average_z(zs)
        self.lflags, self.iflags, self.iheight = lflags, iflags, iheight
        sx, sy, sz, sid = islands.load_statics(name)
        key = sx.astype(np.int64) * H + sy.astype(np.int64)
        order = np.argsort(key, kind="stable")
        self.key, self.sz, self.sid = key[order], sz.astype(np.int32)[order], np.minimum(sid.astype(np.int64)[order], len(iflags) - 1)

    def at(self, x, y):
        if not (0 <= x < self.ids.shape[0] and 0 <= y < H):
            return []
        k = x * H + y
        a, b = np.searchsorted(self.key, k), np.searchsorted(self.key, k, side="right")
        sts = [(int(self.sz[i]), int(self.iflags[self.sid[i]]), int(self.iheight[self.sid[i]])) for i in range(a, b)]
        lf = int(self.lflags[self.ids[x, y]])
        cands = [int(self.avg[x, y])] if not (lf & IMP or lf & WET) else []
        cands += [z + h for z, f, h in sts if f & SURF]
        out = []
        for c in sorted(set(cands)):
            if not any((f & IMP) and not (f & SURF) and z < c + PERSON and z + max(h, 1) > c for z, f, h in sts):
                out.append(c)
        return out


def load(name="sos"):
    """name: "sos" (the swap's land), or "trammel" / "felucca" (stock, for a baseline of the same rules)."""
    path = CACHE + ("" if name == "sos" else "-" + name) + ".npz"
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        np.savez_compressed(path, **build(name))
    d = np.load(path)
    return {k: d[k] for k in d.files}


if __name__ == "__main__":
    g = load()
    s = g["stand"]
    print("standable tiles", int((s != NONE).sum()), "wet", int(g["wet"].sum()), "covered", int(g["covered"].sum()))
