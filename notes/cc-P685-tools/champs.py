r"""cc-P685 (SoS swap S12): Felucca's 17 champion spawns (pinned GenChamps.cs) on the Siege of Sosaria land.

    python -P champs.py      writes out\champs.csv and out\champs.txt

Felucca reads the SoS map file (cc-P675). Each site is the invisible ChampionSpawn controller; ChampionSpawn puts the
5 x 5 platform at controller Z - 20 and the altar on it at Z - 15 (ChampionSpawn.cs:819-842, ChampionPlatform.cs), and
spawns in [X-24, X+24) x [Y-24, Y+24) (ChampionSpawn.cs:190-193). For each site, on SoS (P681's sosgrid walk rules):

  platform  every tile of the 5 x 5 has a floor within 5 Z of the platform's Z (Z - 20): it sits on the ground
            (or misses it on exactly the tiles it misses on stock Felucca at the same site: stock-tolerated)
  area      the walkable share of the 48 x 48 spawn area, against the same share on stock Felucca for the stock site:
            at least 80 percent of stock's, or a quarter of the area (dungeon rooms are walled; stock's own share is the
            measure)
  towns     no tile of the area in a TownRegion or GuardedRegion: Trammel's SoS regions (P676), which are where the
            towns stand on the land Felucca shares, and Felucca's own regions stay pinned's until S13
  closures  no tile of the area in an S14 closure box (P673)
  eject     the eject point (where the champion's spawn area throws players out) has a floor within 5 Z

The sites are pinned's, with P696's proposal (Valorite, golem/Valorite/P696, 4843d5b) applied where the stock site
fails: LL06, LL07 and LL11 move to its option A, and LL08 keeps its altar with a new eject point. MOVES below; the
shard's patch (server/patches/GenChamps-sos-sites.patch) is made from it.
"""
import csv
import json
import os
import sys

import numpy as np

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\UltimaOnlineVanilla")
HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
DOCS = os.path.dirname(NOTES)
sys.path.insert(0, os.path.join(NOTES, "cc-P681-tools"))
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
sys.path.insert(0, os.path.join(DOCS, "scripts"))
import sosgrid  # noqa: E402

SHARD = os.environ.get("SL_SHARD", os.path.join(os.path.dirname(DOCS), "ShatteredLegacy"))
OUT = os.path.join(HERE, "out")
NONE = sosgrid.NONE

# pinned GenChamps.cs:33-53, in source order: id, kind, type, controller, eject
STOCK = [
    ("LL01", "LL", None, (5511, 2360, 42), (5439, 2323, 26)),
    ("LL02", "LL", None, (6038, 2401, 47), (5988, 2340, 24)),
    ("LL03", "LL", None, (5549, 2640, 16), (5645, 2696, -8)),
    ("LL04", "LL", None, (5636, 2916, 37), (5721, 2949, 28)),
    ("LL05", "LL", None, (6035, 2943, 50), (6098, 2997, 17)),
    ("LL06", "LL", None, (5265, 3171, 105), (5314, 3232, 2)),
    ("LL07", "LL", None, (5282, 3368, 50), (5215, 3318, 3)),
    ("LL08", "LL", None, (5207, 3637, 20), (5263, 3687, 0)),
    ("LL09", "LL", None, (5954, 3475, 25), (6013, 3529, 0)),
    ("LL10", "LL", None, (5982, 3882, 20), (5929, 3820, -1)),
    ("LL11", "LL", None, (5724, 3991, 41), (5774, 4041, 26)),
    ("LL12", "LL", "ForestLord", (5559, 3757, 21), (5513, 3878, 3)),
    ("D1", "Dungeon", "UnholyTerror", (5179, 709, 20), (4111, 432, 5)),
    ("D2", "Dungeon", "VerminHorde", (5557, 827, 65), (5580, 632, 30)),
    ("D3", "Dungeon", "ColdBlood", (5259, 837, 64), (1176, 2637, 0)),
    ("D4", "Dungeon", "Abyss", (5815, 1352, 5), (2923, 3406, 8)),
    ("D5", "Dungeon", "Arachnid", (5190, 1607, 20), (5482, 3161, -54)),
]

# P696's option A (and LL08's eject): id -> (controller, eject)
MOVES = {
    "LL06": ((5432, 3220, 19), (5423, 3183, -3)),
    "LL07": ((5324, 3428, 15), (5296, 3428, -5)),
    "LL08": ((5207, 3637, 20), (5209, 3609, 0)),
    "LL11": ((5768, 4024, 20), (5768, 3996, 0)),
}

CLOSURES = [(2840, 1324, 3039, 1523), (4224, 256, 4479, 767), (3072, 2304, 3199, 2559), (4096, 2560, 4223, 2815),
            (2688, 2688, 2943, 3071)]
ZTOL = 5
HALF = 24


def guard_rects():
    out = []
    for r in json.load(open(os.path.join(SHARD, "server", "data", "regions-trammel.json"), encoding="utf-8")):
        if r["$type"] in ("TownRegion", "GuardedRegion"):
            out += [(r.get("Name", "(unnamed)"), a["x1"], a["y1"], a["x2"], a["y2"]) for a in r.get("Area", [])]
    return out


def area(x, y):
    return x - HALF, y - HALF, x + HALF, y + HALF      # half-open


def overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def floor(surf, x, y, z):
    zs = [c for c in surf.at(x, y) if abs(c - z) <= ZTOL]
    return min(zs, key=lambda c: abs(c - z)) if zs else None


def share(stand, x, y):
    x1, y1, x2, y2 = area(x, y)
    return float((stand[max(0, x1):x2, max(0, y1):y2] != NONE).mean())


def sites():
    """The shipped sites: (id, kind, type, controller, eject, action)."""
    out = []
    for i, kind, typ, c, e in STOCK:
        if i in MOVES:
            nc, ne = MOVES[i]
            out.append((i, kind, typ, nc, ne, "moved" if nc != c else "eject moved"))
        else:
            out.append((i, kind, typ, c, e, "kept"))
    return out


def core_misses(surf, x, y, pz):
    return [(x + dx, y + dy) for dx in range(-2, 3) for dy in range(-2, 3) if floor(surf, x + dx, y + dy, pz) is None]


def judge(surf, stand, stock_stand, guards, sid, c, e, stock_c, stock_surf=None):
    """The reasons the site fails (none: it passes), its walkable share and stock's. A platform that misses the floor
    on exactly the same tiles on stock Felucca, at the same site, is stock-tolerated (the platform's own pieces cover
    the uneven floor, as they do in stock today: Destard's and Fire's rooms)."""
    x, y, z = c
    why = []
    pz = z - 20
    bad_core = core_misses(surf, x, y, pz)
    tolerated = bool(bad_core) and stock_surf is not None and tuple(c) == tuple(stock_c) and \
        core_misses(stock_surf, x, y, pz) == bad_core
    if bad_core and not tolerated:
        why.append(f"platform: {len(bad_core)} of 25 tiles without a floor within {ZTOL} of Z {pz}")
    s = share(stand, x, y)
    s0 = share(stock_stand, stock_c[0], stock_c[1])
    need = min(0.8 * s0, 0.25)
    if s < need:
        why.append(f"area: {s:.2f} walkable, stock {s0:.2f}")
    a = area(x, y)
    towns = sorted({n for n, *r in guards if overlaps(a, r)})
    if towns:
        why.append("area in a guard zone: " + ", ".join(towns))
    if any(overlaps(a, (x1, y1, x2 + 1, y2 + 1)) for x1, y1, x2, y2 in CLOSURES):
        why.append("area in an S14 closure")
    if floor(surf, *e) is None:
        why.append(f"eject {e}: no floor within {ZTOL}")
    return why, s, s0


def main():
    g = sosgrid.load()
    k = sosgrid.load("felucca")
    surf = sosgrid.Surfaces("sos")
    stock_surf = sosgrid.Surfaces("felucca")
    guards = guard_rects()
    stock = {i: (c, e) for i, _, _, c, e in STOCK}
    rows, lines = [], []
    # the stock sites as they are, on SoS: the grade this prompt starts from
    stock_fail = []
    for i, kind, typ, c, e in STOCK:
        why, _, _ = judge(surf, g["stand"], k["stand"], guards, i, c, e, c)
        if why:
            stock_fail.append(f"{i} at {c}: {'; '.join(why)}")
    lines.append(f"stock sites failing on SoS: {len(stock_fail)} of {len(STOCK)}")
    lines += ["  " + s for s in stock_fail]
    bad = []
    for i, kind, typ, c, e, action in sites():
        why, s, s0 = judge(surf, g["stand"], k["stand"], guards, i, c, e, stock[i][0], stock_surf)
        tol = not why and core_misses(surf, c[0], c[1], c[2] - 20)
        rows.append([i, kind, typ or "random", *c, *e, action, f"{s:.3f}", f"{s0:.3f}",
                     "; ".join(why) or ("ok (platform stock-tolerated)" if tol else "ok")])
        if why:
            bad.append(f"{i} at {c}: {'; '.join(why)}")
    # no two shipped areas overlap
    ss = sites()
    for a in range(len(ss)):
        for b in range(a + 1, len(ss)):
            if overlaps(area(*ss[a][3][:2]), area(*ss[b][3][:2])):
                bad.append(f"{ss[a][0]} and {ss[b][0]}: spawn areas overlap")
    lines.append(f"shipped sites failing: {len(bad)} of {len(ss)}")
    lines += ["  " + b for b in bad]
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "champs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "kind", "type", "x", "y", "z", "eject_x", "eject_y", "eject_z", "action", "walkable_share",
                    "stock_share", "verdict"])
        w.writerows(rows)
    text = "\n".join(lines) + "\n"
    open(os.path.join(OUT, "champs.txt"), "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
