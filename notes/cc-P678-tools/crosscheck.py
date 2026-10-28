r"""cc-P678: every tile our code now uses in SoS Haven, from the code copy, checked together.
Collects: HavenSpots, the NPC homes (out/homes.csv), the League office and Alembic hall props, community art, the
winter decor, the Halloween rows at the New Haven bank, the cellar hatch and the ladder's landing, the ankh, the
tutorial yards and the training field. Then checks:
  1. no two of them on one tile (props may share a table; NPCs, spots, the hatch and the landing may not share);
  2. every NPC, spot, the hatch and the landing is reachable on foot from the start with every blocking prop in place
     (a prop row counts as blocking when its item is Impassable in tiledata);
  3. nothing stands on or beside the hatch or the landing, and the walk from the start reaches the hatch with every blocking prop in place.
    python -P crosscheck.py > out/crosscheck.txt      (exit 1 on a failure)
"""
import collections
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import soswalk  # noqa: E402

# the shard repo's work copy: SL_SHARD_REPO, as tools/tests reads it (default the main checkout)
CODE = os.path.join(os.environ.get("SL_SHARD_REPO", r"D:\ShatteredLegacy"), "server", "customizations") + os.sep
START = (3634, 2586)
BOX = (3540, 2370, 3790, 2720)
HATCH, LANDING = (3618, 2620), (3621, 2620)


def src(name):
    with open(CODE + name, encoding="utf-8") as f:
        return f.read()


def rows():
    """(what, kind, x, y, z, item id or None); kind 'npc' or 'spot' (must stand) or 'prop'."""
    out = []
    for m in re.finditer(r"public static readonly Point3D (\w+) = new\((\d+), (\d+), (-?\d+)\)", src("Tutorial/HavenSpots.cs")):
        out.append(("HavenSpots." + m.group(1), "spot", int(m.group(2)), int(m.group(3)), int(m.group(4)), None))
    with open(os.path.join(HERE, "out", "homes.csv")) as f:
        homes = list(csv.DictReader(f))
    for r in homes:
        if r["kind"] != "stock":
            out.append(("home " + r["name"], "npc", int(r["x"]), int(r["y"]), int(r["z"]), None))
    for m in re.finditer(r'new\("(\w+)", (0x[0-9A-Fa-f]+), "([^"]+)", (\d+), (\d+), (-?\d+)\)', src("ClusterFRegistrarOfficeLayout.cs")):
        out.append(("office " + m.group(3), "prop", int(m.group(4)), int(m.group(5)), int(m.group(6)), int(m.group(2), 16)))
    for m in re.finditer(r'new\("([\w-]+)", "(\w+)", (\d+), (\d+), (-?\d+), (0x[0-9A-Fa-f]+)', src("ClusterFCommunityArtLayout.cs")):
        out.append(("art " + m.group(1), "prop", int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6), 16)))
    for m in re.finditer(r'new\("([\w-]+)", "([^"]+)", (\d+), (\d+), (-?\d+), (0x[0-9A-Fa-f]+)', src("ClusterFWinterDecorLayout.cs")):
        out.append(("winter " + m.group(1), "prop", int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6), 16)))
    for m in re.finditer(r'new\("(new-haven/[\w-]+)", "new-haven", "[^"]*", "Trammel", (\d+), (\d+), (-?\d+), (0x[0-9A-Fa-f]+)', src("ClusterFHalloweenDecorLayout.cs")):
        out.append(("halloween " + m.group(1), "prop", int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5), 16)))
    for m in re.finditer(r'new\("\w+", (0x[0-9A-Fa-f]+), "[^"]+", (\d+), (\d+), (-?\d+)\)', src("ClusterFAlembicGuild.cs")):
        out.append(("alembic prop", "prop", int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(1), 16)))
    m = re.search(r'new\("AnkhWest 0x0003", 1, (\d+), (\d+), (-?\d+), "ours', src("ClusterFAnkhs.cs"))
    if m:
        x, y, z = int(m.group(1)), int(m.group(2)), int(m.group(3))
        out += [("ankh", "prop", x, y, z, 0x3), ("ankh foot", "prop", x, y + 1, z, 0x2)]
    out += [("hatch", "spot", HATCH[0], HATCH[1], 2, None), ("ladder landing", "spot", LANDING[0], LANDING[1], 0, None)]
    for name, rx in (("training yard", r"Yard = new\((\d+), (\d+)\)"),):
        m = re.search(rx, src("Tutorial/TutorialWingTrials.cs"))
        out.append((name, "spot", int(m.group(1)), int(m.group(2)), 0, None))
    m = re.search(r"TradesYard = new\((\d+), (\d+)\)", src("Tutorial/TutorialTradeTrials.cs"))
    out.append(("trades yard", "spot", int(m.group(1)), int(m.group(2)), 0, None))
    return out


def main():
    rs = rows()
    f = soswalk.files()
    items = f["items"]
    imp = [r for r in rs if r[1] == "prop" and r[5] is not None and items[r[5]]["flags"] & soswalk.IMP]
    fails = 0
    print("%d rows: %s" % (len(rs), dict(collections.Counter(r[0].split()[0] for r in rs))))

    by = collections.defaultdict(list)
    for r in rs:
        by[(r[2], r[3])].append(r)
    for t, rr in sorted(by.items()):
        standers = [r for r in rr if r[1] in ("npc", "spot")]
        if len(standers) > 1 or (standers and any(r[1] == "prop" for r in rr)):
            print("SHARED", t, [r[0] for r in rr])
            fails += 1

    w = soswalk.Walk(BOX, extra=[(r[2], r[3], r[4], r[5]) for r in imp] + [(HATCH[0], HATCH[1], -1, 0x3E65)])
    reach = w.flood(START)
    for r in rs:
        if r[1] in ("npc", "spot") and (r[2], r[3]) not in reach:
            print("NOT REACHED", r[0], (r[2], r[3]), w.stand.get((r[2], r[3])), w.why.get((r[2], r[3])))
            fails += 1
    path = w.path(START, HATCH) or []
    # beside the hatch or the landing; the walk to the hatch already treats every blocking prop as a wall
    near = {(x + dx, y + dy) for x, y in [HATCH, LANDING] for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    for r in rs:
        if r[1] == "prop" and (r[2], r[3]) in near:
            print("BY THE HATCH", r[0], (r[2], r[3]))
            fails += 1
    if not path:
        print("NO WALK from the start to the hatch")
        fails += 1
    print("blocking props %d; tiles reached %d; start to hatch %d steps" % (len(imp), len(reach), len(path)))
    print("FAILURES", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
