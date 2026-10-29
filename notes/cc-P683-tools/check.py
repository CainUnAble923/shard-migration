r"""cc-P683: the author's teleporters on the SoS map (out\ends.csv, out\check.txt).

    python -P check.py

  - Walkable: each end (the teleporter's tile and its PointDest) has a floor from 15 below to 5 above its Z on SoS (P681's
    sosgrid.Surfaces: the land when walkable, each surface static's top, nothing impassable over the 16 above it).
    A teleporter's own tile must be one a player steps on; its PointDest one a player lands on.
  - Collisions: no shipped teleporter (P679's teleporters-sos.json) or shipped decoration entry (P680's cfgs) stands on
    one of these tiles (Decorate.cs counts an existing Teleporter at the same XYZ as present, whatever its PointDest).
  - Other ways in: no shipped teleporter of P679's lands inside an author dungeon region (P676's DungeonRegions named
    after his 28 sections), so a sealed dungeon has no way in once its own entrances are out.
"""
import csv
import glob
import json
import os
import re
import sys

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\UltimaOnlineVanilla")   # tiledata: SoS ships none of its own
HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
DOCS = os.path.dirname(NOTES)
sys.path.insert(0, os.path.join(NOTES, "cc-P681-tools"))
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
sys.path.insert(0, os.path.join(DOCS, "scripts"))
import sosgrid  # noqa: E402  (P681: the SoS map with the playbook's walk rules)

SHARD = os.environ.get("SL_SHARD", os.path.join(os.path.dirname(DOCS), "ShatteredLegacy"))
OUT = os.path.join(HERE, "out")


def region_records():
    return json.load(open(os.path.join(SHARD, "server", "data", "regions-trammel.json"), encoding="utf-8"))


def in_rects(x, y, rects):
    return any(x1 <= x < x2 and y1 <= y < y2 for x1, y1, x2, y2 in rects)
ZTOL = 5


def placements():
    with open(os.path.join(OUT, "teleporters.csv"), newline="") as f:
        return [r for r in csv.DictReader(f) if r["x"]]


def floor(surf, x, y, z):
    """The floor a teleporter at z serves: pinned fires an item for a walker up to 15 below it (Mobile.cs Move:
    item.Z + height > newZ && newZ + 15 > item.Z), and a player put down at z steps down to a floor under him; ZTOL
    above, for the walk model's own error (P681's tolerance). Nearest first, or None."""
    zs = [c for c in surf.at(x, y) if z - 15 < c <= z + ZTOL]
    return min(zs, key=lambda c: abs(c - z)) if zs else None


# the cfg's section name -> the author's region name (Regions.xml), where they differ
REGION_NAME = {"Oboru Burial Grounds": "Oboru Burial Ground"}


def author_dungeon_rects(names):
    want = {REGION_NAME.get(n, n): n for n in names}
    out = {}
    for r in region_records():
        if r.get("$type") == "DungeonRegion" and r.get("Name") in want:
            out[want[r["Name"]]] = [(a["x1"], a["y1"], a["x2"], a["y2"]) for a in r["Area"]]
    return out


def deco_entries():
    """(facet, x, y, z, file, header) of every shipped decoration entry, our sos-dungeons.cfg excluded."""
    entry = re.compile(r"^\s*(-?\d+)\s+(-?\d+)\s+(-?\d+)")
    out = []
    root = os.path.join(SHARD, "server", "data", "Decoration")
    for folder in ("Britannia", "Trammel", "Felucca"):
        for path in sorted(glob.glob(os.path.join(root, folder, "*.cfg"))):
            if os.path.basename(path) == "sos-dungeons.cfg":
                continue
            header = None
            for raw in open(path, encoding="utf-8", errors="replace"):
                s = raw.strip()
                if not s:
                    header = None
                    continue
                if s.startswith("#"):
                    continue
                m = entry.match(s)
                if m and header:
                    for facet in (("Trammel", "Felucca") if folder == "Britannia" else (folder,)):
                        out.append((facet, int(m.group(1)), int(m.group(2)), int(m.group(3)), os.path.basename(path), header))
                else:
                    header = s
    return out


def main():
    surf = sosgrid.Surfaces("sos")
    rows = placements()
    lines, bad = [], []
    with open(os.path.join(OUT, "ends.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_line", "dungeon", "section", "state", "x", "y", "z", "floor_at_source", "dest_x", "dest_y",
                    "dest_z", "floor_at_dest"])
        for r in rows:
            x, y, z = int(r["x"]), int(r["y"]), int(r["z"])
            dx, dy, dz = int(r["dest_x"]), int(r["dest_y"]), int(r["dest_z"])
            a, b = floor(surf, x, y, z), floor(surf, dx, dy, dz)
            w.writerow([r["source_line"], r["dungeon"], r["section"], r["state"], x, y, z, "" if a is None else a,
                        dx, dy, dz, "" if b is None else b])
            if a is None or b is None:
                bad.append(f"line {r['source_line']} {r['dungeon']} / {r['section']} ({r['state']}): "
                           f"{'source ' + str((x, y, z)) if a is None else ''} {'dest ' + str((dx, dy, dz)) if b is None else ''}")
    ship = [r for r in rows if r["state"] == "ships"]
    lines.append(f"{len(rows)} placements, {len(ship)} ship; ends without a floor from 15 below to {ZTOL} above: {len(bad)}")
    lines += ["  " + b for b in bad]
    # collisions
    tele = json.load(open(os.path.join(SHARD, "server", "data", "teleporters-sos.json"), encoding="utf-8"))
    tsrc = {(t["src"]["map"], *t["src"]["loc"]) for t in tele}
    deco = {(f, x, y, z): (fn, h) for f, x, y, z, fn, h in deco_entries()}
    coll = []
    for r in ship:
        for facet in ("Trammel", "Felucca"):
            k = (facet, int(r["x"]), int(r["y"]), int(r["z"]))
            if k in tsrc:
                coll.append(f"{facet} {k[1:]}: a shipped teleporter (teleporters-sos.json) stands there")
            if k in deco and deco[k][1].startswith("Teleporter"):
                coll.append(f"{facet} {k[1:]}: a shipped decoration teleporter ({deco[k][0]}) stands there")
    lines.append(f"collisions with shipped teleporters on the same tile: {len(coll)}")
    lines += ["  " + c for c in coll]
    # other ways in
    names = {r["dungeon"] for r in rows}
    rects = author_dungeon_rects(names)
    lines.append(f"author dungeon regions found in regions-trammel.json: {len(rects)} of {len(names)} sections with placements"
                 f" (missing: {', '.join(sorted(names - set(rects))) or 'none'})")
    ways = []
    for t in tele:
        sx, sy, _ = t["src"]["loc"]
        dx, dy, _ = t["dst"]["loc"]
        for n, rs in rects.items():
            if in_rects(dx, dy, rs) and not in_rects(sx, sy, rs):
                ways.append(f"{t['src']['map']} {tuple(t['src']['loc'])} -> {tuple(t['dst']['loc'])} into {n}")
    lines.append(f"shipped teleporters into an author dungeon from outside it: {len(ways)}")
    lines += ["  " + w_ for w_ in ways]
    # the same walk test over the shard's own shipped teleporters (P679), which work in game: its calibration
    st = [t for t in tele if t["src"]["map"] == "Trammel"]
    miss = [t for t in st if floor(surf, *t["src"]["loc"]) is None or floor(surf, *t["dst"]["loc"]) is None]
    lines.append(f"calibration: of the shard's {len(st)} shipped Trammel teleporters, {len(miss)} fail the same test")
    text ="\n".join(lines) + "\n"
    open(os.path.join(OUT, "check.txt"), "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
