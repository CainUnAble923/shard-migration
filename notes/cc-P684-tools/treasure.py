r"""cc-P684 (SoS swap S11): treasure.cfg on the SoS land.

    python -P treasure.py      writes the code copy's server\data\treasure.cfg and out\treasure.csv, out\treasure.txt

pinned's Data/treasure.cfg (193 spots, x y) still decides three things on this shard (server/patches/TreasureMap.cs,
the ServUO revamp): the level-0 maps' spots (the ones in TreasureMap.IsInHavenIsland's box), every map's spot when
treasureMaps.newChestLocations is off, and TreasureMapProtection's no-housing square round each spot on both facets.
(With it on, the default, a level 1+ map picks a random valid tile; ValidateLocation, and the closure and Felucca checks
this prompt adds there, judge that tile.)

Each spot is judged by TreasureMap.ValidateLocation's rules, read off the SoS files, plus this prompt's:
  the land tile not ignored (ids 2, 0x1DB, 0x1AE-0x1B5) and not impassable; not a road (its RoadIDs); diggable by name
  (dirt, grass, jungle, forest, snow); every static on the tile passable and diggable by name; not in a TownRegion or a
  DungeonRegion (P676's regions-trammel.json; Felucca stands on the same land); not in an S14 closure box (P673).
A spot that passes stays, and so does one that fails the same rule on stock's own map on a tile SoS left as it was
(stock-tolerated: pinned's spots predate ServUO's rule, and 34 of the 193 fail it on stock Trammel). One that fails moves to the nearest tile that passes within 20, or is dropped.
New spots: the new land (dry on SoS and not on stock Trammel, x under 5120, outside towns, dungeons and closures), one
per 7,000 of its tiles (P673's figure), on tiles that pass, spread out (each the passing tile farthest from all spots
so far, over a regular sample of them).
"""
import csv
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sea  # noqa: E402
import islands  # noqa: E402  (sea.py puts P481's and P681's tools on the path)
import sosgrid  # noqa: E402

OUT = os.path.join(sea.HERE, "out")
PINNED_CFG = r"D:\UO\ModernUO-pinned\Distribution\Data\treasure.cfg"
# P684_TREASURE_OUT: write elsewhere (the fact regenerates the file and compares)
SHIPPED = os.environ.get("P684_TREASURE_OUT", os.path.join(sea.SHARD, "server", "data", "treasure.cfg"))
REGIONS = os.path.join(sea.SHARD, "server", "data", "regions-trammel.json")
MOVE = 20
PER_NEW = 7000
# P673 S14's closure boxes, inclusive (and ClusterFSosTreasureLand.Closures in the code copy)
CLOSURES = [(2840, 1324, 3039, 1523), (4224, 256, 4479, 767), (3072, 2304, 3199, 2559), (4096, 2560, 4223, 2815),
            (2688, 2688, 2943, 3071)]
ROADS = [(0x0071, 0x0078), (0x00E8, 0x00EB), (0x07AE, 0x07B1), (0x3FF4, 0x3FF4), (0x3FF8, 0x3FFB), (0x0442, 0x0479),
         (0x0501, 0x0510), (0x0009, 0x0015), (0x0150, 0x015C)]
DIGGABLE = {"dirt", "grass", "jungle", "forest", "snow"}
IMP = 0x40
HAVEN_BOX = (3314, 2345, 3814, 3095)   # TreasureMap.IsInHavenIsland, inclusive


def read_cfg(path):
    out = []
    for line in open(path):
        p = line.split()
        if len(p) >= 2:
            out.append((int(p[0]), int(p[1])))
    return out


class _Map:
    pass


def stock_map():
    """Stock Trammel's land and statics, in the shape judge_mask reads."""
    m = _Map()
    m.ids, m.z = islands.load_land("trammel")
    sx, sy, sz, sid = islands.load_statics("trammel")
    key = sx.astype(np.int64) * sea.H + sy.astype(np.int64)
    o = np.argsort(key, kind="stable")
    m._key, m._sid, m._sz = key[o], sid[o].astype(np.int32), sz[o].astype(np.int32)
    return m


def stock_regions():
    """Pinned regions.json's Trammel regions, with x1 y1 x2 y2 areas."""
    out = []
    for r in json.load(open(os.path.join(r"D:\UO\ModernUO-pinned\Distribution\Data", "regions.json"))):
        if r.get("Map") == "Trammel":
            r = dict(r)
            r["Area"] = [a if "x1" in a else {"x1": a["x"], "y1": a["y"], "x2": a["x"] + a["width"], "y2": a["y"] + a["height"]}
                         for a in r.get("Area", [])]
            out.append(r)
    return out


def same_tile(S, K, x, y):
    """SoS left the tile as stock has it: the same land id and Z and the same statics."""
    def st(m):
        k = x * sea.H + y
        a, b = np.searchsorted(m._key, k), np.searchsorted(m._key, k, side="right")
        return sorted(zip(m._sz[a:b].tolist(), m._sid[a:b].tolist()))
    return int(S.ids[x, y]) == int(K.ids[x, y]) and int(S.z[x, y]) == int(K.z[x, y]) and st(S) == st(K)


def judge_mask(S, regions=None, closures=None):
    """W x H bool: the tile passes the land and region rules (regions: P676's Trammel regions unless given)."""
    land, items = sea.tiledata()
    lflags = np.array([l[0] for l in land], dtype=np.uint64)
    ldig = np.array([l[2].strip().lower() in DIGGABLE for l in land])
    ids = S.ids
    ok = ((lflags[ids] & np.uint64(IMP)) == 0) & ldig[ids]
    ok &= ~((ids == 2) | (ids == 0x1DB) | ((ids >= 0x1AE) & (ids <= 0x1B5)))
    for a, b in ROADS:
        ok &= ~((ids >= a) & (ids <= b))
    iflags = np.array([it["flags"] for it in items], dtype=np.uint64)
    idig = np.array([it["name"].strip().lower() in DIGGABLE for it in items])
    sx, sy, sid = S._key // sea.H, S._key % sea.H, np.minimum(S._sid, len(items) - 1)
    badst = ((iflags[sid] & np.uint64(IMP)) != 0) | ~idig[sid]
    flat = np.zeros(sea.W * sea.H, dtype=bool)
    flat[(sx * sea.H + sy)[badst]] = True
    ok &= ~flat.reshape(sea.W, sea.H)
    regions_bad = np.zeros((sea.W, sea.H), dtype=bool)
    for r in (regions if regions is not None else json.load(open(REGIONS, encoding="utf-8"))):
        if r["$type"] in ("TownRegion", "DungeonRegion"):
            for a in r.get("Area", []):
                regions_bad[max(0, a["x1"]):a["x2"], max(0, a["y1"]):a["y2"]] = True
    for x1, y1, x2, y2 in (CLOSURES if closures is None else closures):
        regions_bad[x1:x2 + 1, y1:y2 + 1] = True
    return ok & ~regions_bad, regions_bad


def nearest(ok, x, y):
    for d in range(1, MOVE + 1):
        best = None
        for dx in range(-d, d + 1):
            for dy in range(-d, d + 1):
                if max(abs(dx), abs(dy)) != d:
                    continue
                a, b = x + dx, y + dy
                if 0 <= a < sea.W and 0 <= b < sea.H and ok[a, b]:
                    e = dx * dx + dy * dy
                    if best is None or e < best[0]:
                        best = (e, a, b)
        if best:
            return best[1], best[2]
    return None


def main():
    S = sea.load()
    ok, excluded = judge_mask(S)
    K = stock_map()
    stock_ok, _ = judge_mask(K, stock_regions(), [])
    stock = read_cfg(PINNED_CFG)
    rows, keep = [], []
    for x, y in stock:
        if ok[x, y]:
            keep.append((x, y))
            rows.append(["stock", x, y, "kept", x, y, 0])
            continue
        if not stock_ok[x, y] and not excluded[x, y] and same_tile(S, K, x, y):
            # it fails the rule on stock's own map too, and SoS left the tile as it was: stock-tolerated, kept
            keep.append((x, y))
            rows.append(["stock", x, y, "kept (stock-tolerated)", x, y, 0])
            continue
        n = nearest(ok, x, y)
        if n:
            keep.append(n)
            rows.append(["stock", x, y, "moved", n[0], n[1], max(abs(n[0] - x), abs(n[1] - y))])
        else:
            rows.append(["stock", x, y, "dropped", "", "", ""])
    # the new land
    g = sosgrid.load()
    gt = sosgrid.load("trammel")
    new = (g["stand"] != sosgrid.NONE) & (gt["stand"] == sosgrid.NONE)
    new[5120:, :] = False
    new &= ~excluded
    n_new = int(new.sum())
    cand = new & ok
    want = round(n_new / PER_NEW)
    xs, ys = np.nonzero(cand)
    step = max(1, len(xs) // 200000)          # a regular subsample keeps the spread search quick
    pts = np.stack([xs[::step], ys[::step]], axis=1).astype(np.int32)
    have = np.array(keep, dtype=np.int32)
    d = np.full(len(pts), 10 ** 9, dtype=np.int64)
    for a, b in have:
        d = np.minimum(d, (pts[:, 0] - a) ** 2 + (pts[:, 1] - b) ** 2)
    added = []
    for _ in range(want):
        i = int(np.argmax(d))
        a, b = int(pts[i, 0]), int(pts[i, 1])
        added.append((a, b))
        rows.append(["new", "", "", "added", a, b, ""])
        d = np.minimum(d, (pts[:, 0] - a) ** 2 + (pts[:, 1] - b) ** 2)
    final = keep + added
    with open(SHIPPED, "w", newline="\r\n") as f:      # pinned's file has CRLF lines
        f.write("\n".join(f"{x} {y}" for x, y in final))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "treasure.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source", "x", "y", "action", "new_x", "new_y", "moved_by"])
        w.writerows(rows)
    haven = sum(1 for x, y in final if HAVEN_BOX[0] <= x <= HAVEN_BOX[2] and HAVEN_BOX[1] <= y <= HAVEN_BOX[3])
    c = {a: sum(1 for r in rows if r[3] == a) for a in ("kept", "kept (stock-tolerated)", "moved", "dropped", "added")}
    text = (f"stock spots {len(stock)}: kept {c['kept']} and {c['kept (stock-tolerated)']} stock-tolerated, moved "
            f"{c['moved']} (within {MOVE}), dropped {c['dropped']}\n"
            f"new land: {n_new} dry tiles (outside towns, dungeons and closures), {int(cand.sum())} pass; "
            f"one per {PER_NEW}: {c['added']} added\n"
            f"shipped: {len(final)} spots; {haven} in the Haven box (level-0 maps)\n")
    open(os.path.join(OUT, "treasure.txt"), "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
