r"""cc-P684 (SoS swap S11): boats at the author's docks, and SOS bottles' random water, on the SoS map.

    python -P docks_sos.py      writes out\docks.csv, out\sos-picks.csv and out\docks-sos.txt

DOCKS. For each of the author's dock points (P669's spots.csv, his go-menu's "Docks" entries): the nearest place within
15 tiles where a small boat (multi 0x0 facing north, or 0x1 east: their footprints from the client's multi.mul) passes
BaseBoat.CanFit at Z -5 on every tile, and every tile of it is in a sea (sea.py's seas: a connected body of boat water
of 100,000 tiles or more, so a boat that leaves the dock reaches the rest of that sea and comes back; the open sea, or the
Lost Lands' own for Papua). And that the dock point is in a
no-housing region (a town's, a dungeon's or a dock's NoHousingRegion, P676's regions-trammel.json).

SOS. SOS.cs FindLocation, replayed 1,000 times with a fixed seed: up to 50 tries, a random tile of (0, 0, 5120, 4096)
(BritRegions, Trammel and Felucca), accepted when it and the 20 tiles 5 to 25 out on its four diagonals are deep water
by land id (ValidateDeepWater). Every accepted pick must be in the open sea (boat water, reachable), so not on the new
continent's land, not void. (Picks over water inside his Nujelm Desert and Moonglow Forest region boxes are counted:
his boxes reach over the sea.) The isle (6594-6865, 3905-4049) is outside the
sampled rectangle, so no pick can reach it: the check is stated, not sampled (P699 R15). Picks that exhaust 50 tries
return Point3D.Zero: counted, and none allowed.
"""
import csv
import json
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sea  # noqa: E402

OUT = os.path.join(sea.HERE, "out")
SPOTS = os.path.join(sea.NOTES, "cc-P669-tools", "out", "spots.csv")
REGIONS = os.path.join(sea.SHARD, "server", "data", "regions-trammel.json")
ISLE = (6594, 3905, 6865, 4049)
BRIT = (0, 0, 5120, 4096)
SEED = 682684
PICKS = 1000
# client multi.mul (D:\UO\UltimaOnlineVanilla), multis 0x0 and 0x1: the component offsets (vseUOAware get_multi)
SMALL_NORTH = {(0, 0), (1, 4), (0, -4), (2, 0), (-2, 0), (0, -2), (1, -3), (0, -3), (-1, -3), (1, -1), (-1, -1), (1, -2),
               (-1, -2), (0, -1), (-1, 0), (1, 0), (1, -4), (-1, -4), (2, -1), (-2, -1), (0, -5), (-1, 1), (0, 1), (1, 1),
               (-1, 2), (0, 2), (1, 2), (2, 1), (-2, 1), (-2, 2), (-1, 3), (0, 3), (1, 3), (-1, 4), (0, 4), (0, 5)}
SMALL_EAST = {(0, 0), (-4, 0), (4, 0), (0, 2), (0, -2), (0, -1), (1, 1), (-1, 1), (0, 1), (1, 0), (1, -1), (-1, 0),
              (-1, -1), (-1, -2), (-2, 0), (-2, -1), (-1, 2), (2, 1), (1, -2), (2, -1), (2, 0), (1, 2), (-2, 1), (3, 0),
              (3, -1), (-3, -1), (-3, 0), (2, -2), (3, 1), (-3, 1), (4, 1), (4, -1), (-4, 1), (-4, -1), (-5, 0), (5, 0)}
DOCK_RANGE = 15


def regions():
    return json.load(open(REGIONS, encoding="utf-8"))


def rects(r):
    return [(a["x1"], a["y1"], a["x2"], a["y2"]) for a in r.get("Area", [])]


def inside(x, y, rs):
    return any(x1 <= x < x2 and y1 <= y < y2 for x1, y1, x2, y2 in rs)


def no_housing(x, y, regs):
    """The region types pinned forbids housing in (GuardedRegion and its TownRegion, DungeonRegion) or that are
    NoHousingRegions, holding the point."""
    return [r["Name"] for r in regs if r["$type"] in ("TownRegion", "GuardedRegion", "DungeonRegion", "NoHousingRegion")
            and inside(x, y, rects(r))]


def docks():
    out = []
    for r in csv.DictReader(open(SPOTS, encoding="utf-8")):
        if "dock" in r["name"].lower():
            out.append((r["group"].split("/")[-1].strip() + " " + r["name"], int(r["x"]), int(r["y"]), int(r["z"])))
    return out


def boat_spot(S, x0, y0, ok=None, reach=DOCK_RANGE):
    """The nearest (distance, x, y, facing) within reach where a small boat fits on ok (a sea unless given), or None."""
    ok = S.boat & S.seas if ok is None else ok
    for d in range(0, reach + 1):
        ring = [(x0 + dx, y0 + dy) for dx in range(-d, d + 1) for dy in range(-d, d + 1) if max(abs(dx), abs(dy)) == d]
        for x, y in ring:
            for face, fp in (("north", SMALL_NORTH), ("east", SMALL_EAST)):
                if all(0 <= x + a < sea.W and 0 <= y + b < sea.H and ok[x + a, y + b] for a, b in fp):
                    return d, x, y, face
    return None


def sos_pick(S, rng):
    """SOS.cs FindLocation on Trammel or Felucca: (x, y) or None for Point3D.Zero."""
    for _ in range(50):
        x = rng.randrange(BRIT[0], BRIT[0] + BRIT[2])
        y = rng.randrange(BRIT[1], BRIT[1] + BRIT[3])

        def deep(a, b):
            return 0 <= a < sea.W and 0 <= b < sea.H and bool(S.deep[a, b])

        if not deep(x, y):
            continue
        if all(deep(x + o, y + o) and deep(x + o, y - o) and deep(x - o, y + o) and deep(x - o, y - o)
               for o in range(5, 30, 5)):
            return x, y
    return None


def main():
    S = sea.load()
    regs = regions()
    os.makedirs(OUT, exist_ok=True)
    lines = []
    rows = []
    bad_docks = []
    lab = None
    for name, x, y, z in docks():
        spot = boat_spot(S, x, y)
        nh = no_housing(x, y, regs)
        # no house stands on water: a dock point over water needs no no-housing region (HousePlacement wants land)
        water = bool(((S.ids[x, y] >= 168) & (S.ids[x, y] <= 171)) | ((S.ids[x, y] >= 310) & (S.ids[x, y] <= 311)))
        why = ""
        if spot is None:
            if lab is None:
                lab = sea.components(S.boat)
            near = boat_spot(S, x, y, S.boat, 60)
            if near:
                size = int((lab == lab[near[1], near[2]]).sum())
                why = (f"no boat fits in a sea within {DOCK_RANGE}; the nearest boat water a small boat fits is "
                       f"{near[0]} away at {near[1]},{near[2]}, in a closed body of {size} tiles")
            else:
                why = "no boat fits in any water within 60"
        rows.append([name, x, y, z, *(spot or ("", "", "", "")), "; ".join(nh), "water" if water else "land", why])
        if spot is None or not (nh or water):
            bad_docks.append(f"{name} at {x},{y}: {why} {'' if nh or water else 'not in a no-housing region, on land'}")
    with open(os.path.join(OUT, "docks.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dock", "x", "y", "z", "boat_distance", "boat_x", "boat_y", "facing", "no_housing_regions",
                    "ground", "problem"])
        w.writerows(rows)
    lines.append(f"docks: {len(rows)}; a small boat floats in the open sea within {DOCK_RANGE} of each: "
                 f"{len(rows) - len(bad_docks)} of {len(rows)}")
    lines += ["  " + b for b in bad_docks]
    # SOS
    desert = [rects(r) for r in regs if r.get("Name") in ("Nujelm Desert", "Moonglow Forest")]
    desert = [a for rs in desert for a in rs]
    rng = random.Random(SEED)
    zero, bad, picks, in_regions = 0, [], [], 0
    for i in range(PICKS):
        p = rng and sos_pick(S, rng)
        if p is None:
            zero += 1
            picks.append([i, "", "", "Point3D.Zero"])
            continue
        x, y = p
        why = []
        if not S.ocean[x, y]:
            why.append("not open sea" + ("" if S.boat[x, y] else " (no boat water: under statics or not at Z -5)"))
        if inside(x, y, desert):
            in_regions += 1
        if S.ids[x, y] in (0x244, 0x2):
            why.append("void")
        if ISLE[0] <= x <= ISLE[2] and ISLE[1] <= y <= ISLE[3]:
            why.append("in the isle's box")
        picks.append([i, x, y, "; ".join(why) or "ok"])
        if why:
            bad.append(f"pick {i} at {x},{y}: {', '.join(why)}")
    with open(os.path.join(OUT, "sos-picks.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pick", "x", "y", "verdict"])
        w.writerows(picks)
    lines.append(f"SOS picks: {PICKS} (seed {SEED}); Point3D.Zero {zero}; accepted not in the open sea, in the new "
                 f"continent, void or the isle: {len(bad)}")
    lines += ["  " + b for b in bad[:40]]
    lines.append(f"accepted picks in the open sea inside the rectangles of the author's Nujelm Desert or Moonglow Forest "
                 f"regions (water his region boxes reach over, not his land): {in_regions}")
    lines.append(f"the isle's box {ISLE} lies outside SOS.cs's Trammel and Felucca rectangle {BRIT}: no pick can land there")
    text = "\n".join(lines) + "\n"
    open(os.path.join(OUT, "docks-sos.txt"), "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
