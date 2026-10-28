r"""cc-P681 (SoS swap S9): every stock Trammel and Felucca spawner graded on the Siege of Sosaria files, and the
failing ones re-placed or dropped. Both facets read the SoS file on swap day (S2, P675).

Starts from P698's ledger (p698-spawner-plan.csv, copied from P698's commit 34502e9: source, guid, home, ranges,
entries, population kind, import status) and checks every home on the map with sosgrid (the playbook's walk rules).

A home PASSES when:
  - land spawners: the home tile is standable (sosgrid.stand) within 5 Z of the data's Z, and at least a share of the
    tiles in its home range is standable (MIN_SHARE: 25 percent, 10 percent for ranges of 50 and more, which reach
    over the sea by design); a range of 0 or 1 checks the home alone;
  - sea life: the home tile is open water (sosgrid.wet) and at least 25 percent of its range is.
A PASSING home stays; a spawner that stands still (range 0 or 1) whose floor on SoS is 3 to 5 off its Z takes that
floor's Z. A ranged spawner's Z is left as the data has it: the spawner picks each spawn's Z itself.

A home that passes but no longer FITS its purpose is searched for too (P698's rules): a standing town NPC that was
indoors on the stock map and is outdoors on SoS (its building is gone); a wild spawner inside one of the author's seven
new towns (S10's civic space); a wild spawner whose land changed habitat (green, sand, snow, swamp, rock, lava).

A FAILING home is searched for, ring by ring out to 20 tiles (Chebyshev; P673's rule), the nearest tile that passes
the same test and also:
  - town services, town NPCs, town animals and the wandering healer: a covered tile (inside a building) first, then
    any; services keep searching out to 40 so a town does not lose its only banker, healer, smith or provisioner;
  - wild encounters, wildlife, reagents, crops, graveyards and town-edge encounters: the same terrain group as the old
    home had on the stock map (green, sand, snow, swamp, rock, lava, civic), outdoors;
  - dungeon spawners: within 10 Z of the old home (the same floor);
  - sea life: water.
No tile: the spawner is DROPPED (S10 fills new land; P698's rule), except one whose only fault is a changed habitat:
its home and range still pass the walk, so it is kept where it is.

A spawner that fails the same test on its stock map too (about 35 a facet: Shame's and Ice's rooms, a few Magincia
vendors over stacked floors, the test's limits rather than a fault, since it works today) is STOCK-TOLERATED: kept
where it is. Only what the SoS land breaks moves or goes.

Left out of the table, with a reason in the ledger: records the shard never imports (uoml/**, the import hooks'
Despise and crier exclusions), and the Haven island spawners S7 (P678) refuses or owns (its ClusterFHavenTownSpawns:
the ML plaza's town spawners, the ruin's spawners in the town); the 25 records with an explicit spawn rectangle are
kept or dropped, never moved (the rectangle would stay behind). P698's new drop recommendations for the north-east
snow closure (S14) are applied.

    python -P regrade.py --baseline   -> out/baseline-stock.txt, out/stock-pass.json: the same test on the stock maps
    python -P regrade.py         -> out/ledger.csv, out/summary.txt, and the C# table
                                   (SL_SHARD_REPO/server/customizations/ClusterFSosSpawnPlacements.cs)
"""
import collections
import csv
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sosgrid  # noqa: E402

PINNED = "D:/UO/ModernUO-pinned/Distribution/Data"
SHARD = os.environ.get("SL_SHARD_REPO", r"D:\ShatteredLegacy")
OUT = os.path.join(HERE, "out")
NONE = sosgrid.NONE
SEARCH, SERVICE_SEARCH = 20, 40

CIVIC = {"town service", "town NPC or prop", "town animals", "wandering healer"}
WILD = {"wild encounter", "wildlife", "reagent", "crop or livestock", "graveyard", "town-edge encounter"}
SERVICE_ROLES = {"banker": "bank", "healer": "healer", "blacksmith": "smith", "provisioner": "provisioner"}

HABITATS = {"green", "sand", "snow", "swamp", "rock", "lava"}
GROUP = {"grass": "green", "forest": "green", "dirt": "green", "jungle": "swamp", "swamp": "swamp", "sand": "sand",
         "snow": "snow", "rock": "rock", "cave": "rock", "lava": "lava", "road": "civic", "floor": "civic",
         "water": "water", "void": "void", "other": "other"}

# S7 (P678), ClusterFHavenTownSpawns: the ML plaza's town files and the ruin's entries inside the town
PLAZA_FILES = {"Spawns/post-uoml/trammel/Vendors.json", "Spawns/post-uoml/trammel/TownsLife.json"}
RUIN = {"zombie", "skeleton", "spellbinder", "brigandcamp", "mongbat", "healer"}
HAVEN_TOWN = (3568, 2460, 3761, 2712)       # HavenSpots.Town, inclusive
HAVEN_ISLAND = (3314, 2345, 3813, 3094)     # HavenSpots.IslandBounds, inclusive
NE_SNOW = (4224, 4479, 256, 767)            # P673's S14 closure, P698's drops

# The author's new towns S10 peoples (P673's list), their TownRegion rectangles from his Regions.xml (reference only;
# notes/sos-author-data): a wild spawner inside one moves out (P698: civic space is S10's).
NEW_TOWNS = ("Valunstead", "Hammerhill", "Kameron Kove", "Elmhaven", "Kettleburg", "Fort Yondall", "Elandrim Nur Shaz")


def new_town_rects():
    import re
    xml = open(os.path.join(os.path.dirname(HERE), "sos-author-data", "Regions.xml"), encoding="utf-8", errors="replace").read()
    out = []
    for m in re.finditer(r'<region type="TownRegion" name="([^"]+)">(.*?)</region>', xml, re.S):
        if m.group(1) in NEW_TOWNS:
            for r in re.finditer(r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"', m.group(2)):
                x, y, w, h = (int(v) for v in r.groups())
                out.append((m.group(1), x, y, x + w - 1, y + h - 1))
    return out


def in_box(x, y, b):
    return b[0] <= x <= b[2] and b[1] <= y <= b[3]


def s7_owned(r):
    x, y = int(r["x"]), int(r["y"])
    if r["facet"] != "Trammel":
        return None
    if r["source"] in PLAZA_FILES and 3416 <= x <= 3545 and 2480 <= y <= 2648:
        return "S7 (P678) refuses: the ML plaza's town spawner"
    names = {e.split(":")[0].strip().lower() for e in r["entries"].split("|")}
    if in_box(x, y, HAVEN_TOWN) and "/uoml/" not in r["source"] and names & RUIN:
        return "S7 (P678) refuses: Old Haven's ruin inside the town"
    return None


class Grader:
    def __init__(self, name="sos"):
        self.g = sosgrid.load(name)
        self.stand = self.g["stand"]
        self.wet = self.g["wet"]
        self.cov = self.g["covered"]
        self.terr = self.g["terrain"]
        self.names = sosgrid.CLASS_NAMES
        self.surf = sosgrid.Surfaces(name)
        self.towns = new_town_rects()
        self.stock = {}

    def stock_grid(self, facet):
        if facet not in self.stock:
            g = sosgrid.load(facet.lower())
            self.stock[facet] = {"covered": g["covered"], "terrain": g["terrain"]}
        return self.stock[facet]

    def new_town(self, x, y):
        return next((t[0] for t in self.towns if t[1] <= x <= t[3] and t[2] <= y <= t[4]), None)

    def unfit(self, x, y, hr, kind, facet):
        """Why a home that passes the walk no longer serves its purpose on SoS, or None (P698's purpose rules)."""
        st = self.stock_grid(facet)
        if kind in CIVIC and hr <= 1 and st["covered"][x, y] and not self.cov[x, y]:
            return "its building is gone (indoors on the stock map, outdoors on SoS)"
        if kind in WILD:
            town = self.new_town(x, y)
            if town:
                return "inside the author's new town %s (S10's civic space)" % town
            want = GROUP.get(self.names[int(st["terrain"][x, y])], "other")
            have = self.group(self.terr, x, y)
            if want in HABITATS and have != want:
                return "its habitat changed (%s on the stock map, %s on SoS)" % (want, have)
        return None

    def group(self, arr, x, y):
        return GROUP.get(self.names[int(arr[x, y])], "other")

    def share(self, mask, x, y, hr):
        """The share of mask's tiles in the home range box (sampled on a grid of at most 25 x 25)."""
        if hr <= 1:
            return 1.0 if mask[x, y] else 0.0
        step = max(1, (2 * hr + 1) // 25)
        xs = np.clip(np.arange(x - hr, x + hr + 1, step), 0, sosgrid.W - 1)
        ys = np.clip(np.arange(y - hr, y + hr + 1, step), 0, sosgrid.H - 1)
        return float(mask[np.ix_(xs, ys)].mean())

    def floor(self, x, y, z, ztol=5):
        """The standable Z on the tile nearest z, within ztol, or None."""
        zs = [c for c in self.surf.at(x, y) if abs(c - z) <= ztol]
        return min(zs, key=lambda c: abs(c - z)) if zs else None

    def passes(self, x, y, z, hr, sea, ztol=5):
        if not (0 <= x < sosgrid.W and 0 <= y < sosgrid.H):
            return False
        if sea:
            return bool(self.wet[x, y]) and self.share(self.wet, x, y, min(hr, 60)) >= 0.25
        if hr <= 1:
            # it stands where it is: a floor of the tile within ztol of its Z
            return self.floor(x, y, z, ztol) is not None
        land = self.stand != NONE
        if hr >= 100:
            # a reagent field scatters items over 200 tiles each way, from wherever its home is (some stand at sea):
            # land somewhere in its range is what it needs
            return self.share(land, x, y, hr) >= 0.05
        # a ranged spawner picks each spawn's tile and Z itself (stock data gives most of them Z 0 and some sit on a tree
        # or a rock): its home needs walkable ground within 2 tiles, and its range land (a tenth for dungeon rooms and
        # ranges of 50 or more, a quarter otherwise)
        if not land[max(x - 2, 0):x + 3, max(y - 2, 0):y + 3].any():
            return False
        need = 0.10 if hr >= 50 or x >= 5120 else 0.25
        return self.share(land, x, y, min(hr, 60)) >= need


_anchors = None
SMITHS = {"armorer": "blacksmith", "weaponsmith": "blacksmith", "ironworker": "blacksmith"}   # the smithy is theirs too


def haven_anchors():
    """{entry name (lower case): (x, y, z)} of pinned's pre-UOML Haven spawners inside the town (S7's shops)."""
    global _anchors
    if _anchors is None:
        _anchors = {}
        for s in json.load(open(os.path.join(PINNED, "Spawns", "uoml", "trammel", "Vendors.json"))):
            x, y, z = s["location"]
            if in_box(x, y, HAVEN_TOWN):
                for e in s["entries"]:
                    _anchors.setdefault(e["name"].lower(), (x, y, z))
    return _anchors


# ML New Haven's outlying vendors (post-uoml/trammel/Vendors.json, by the halls S7 moved into the author's town): the
# entry, and the hall's new home in P678's homes table (p678-homes.csv, copied from golem/Iron/P678) or the stock shop
OUTLYING = {
    "holymage": ("Haven Magery School", (3647, 2472)),
    "evilwanderinghealer": ("the east house (Keepers of the Last Door)", (3732, 2636)),
    "actor": ("the Bardic Guild in Haven", (3667, 2537)),
    "miner": ("the Mystic Mines of Haven", (3754, 2703)),
}


def p678_tiles():
    with open(os.path.join(HERE, "p678-homes.csv")) as f:
        return {(int(r["x"]), int(r["y"])) for r in csv.DictReader(f)}


def outlying(gr, r, hr):
    names = [e.strip().lower() for e in r["entries"].split("|")]
    hit = next((OUTLYING[n] for n in names if n in OUTLYING), None)
    if not hit:
        return None
    hall, (ax, ay) = hit
    taken = p678_tiles() | {tuple(a[:2]) for a in haven_anchors().values()}
    for d in range(0, 7):
        for (cx, cy) in ([(ax, ay)] if d == 0 else ring(ax, ay, d)):
            s = int(gr.stand[cx, cy])
            if s == NONE or (cx, cy) in taken or (not gr.cov[cx, cy] and hall != OUTLYING["miner"][0]):  # the mines are open ground
                continue
            f = gr.floor(cx, cy, s)
            if f is not None and gr.passes(cx, cy, f, hr, False):
                return cx, cy, f, "into the author's town by its hall's new home, %s (P678)" % hall
    return None


def ring(x, y, d):
    """The tiles at Chebyshev distance d, nearest (Euclidean) first."""
    pts = [(x + dx, y + dy) for dx in range(-d, d + 1) for dy in range(-d, d + 1) if max(abs(dx), abs(dy)) == d]
    return sorted(pts, key=lambda p: ((p[0] - x) ** 2 + (p[1] - y) ** 2, p))


def search(gr, r, x, y, z, hr, kind, facet):
    sea = kind == "sea life"
    if kind in CIVIC and in_box(x, y, HAVEN_TOWN):
        # the author's Haven is pre-UOML Haven rebuilt: the shop of the trade, as pinned's pre-UOML data places it
        for name in (e.split(":")[0].strip().lower() for e in r["entries"].split("|")):
            a = haven_anchors().get(SMITHS.get(name, name))
            if a:
                for d in range(0, 4):
                    for (cx, cy) in ([(a[0], a[1])] if d == 0 else ring(a[0], a[1], d)):
                        f = gr.floor(cx, cy, a[2])
                        if f is not None and gr.passes(cx, cy, f, hr, False):
                            return cx, cy, f, "town: the Haven shop of its trade (pinned's pre-UOML %s, %d,%d)" % (name, a[0], a[1])
    stock_terr = gr.g["terrain_" + facet.lower()]
    want = gr.group(stock_terr, x, y)
    limit = SERVICE_SEARCH if kind in CIVIC and r["_role"] else SEARCH
    passes = []
    for d in range(1, limit + 1):
        for (cx, cy) in ring(x, y, d):
            if sea:
                if gr.passes(cx, cy, 0, hr, True):
                    return cx, cy, -5, "sea: the nearest open water %d away" % d
                continue
            if not (0 <= cx < sosgrid.W and 0 <= cy < sosgrid.H):
                continue
            s = int(gr.stand[cx, cy])
            if s == NONE:
                continue
            if kind == "dungeon":
                if abs(s - z) <= 10 and gr.passes(cx, cy, s, hr, False):
                    return cx, cy, s, "dungeon: the same floor %d away" % d
                continue
            if not gr.passes(cx, cy, s, hr, False):
                continue
            if kind in CIVIC:
                if gr.cov[cx, cy]:
                    return cx, cy, s, "town: indoors %d away" % d
                passes.append((d, cx, cy, s))
                continue
            # wild
            if gr.group(gr.terr, cx, cy) != want or gr.cov[cx, cy] or gr.new_town(cx, cy):
                continue
            return cx, cy, s, "wild: %s ground %d away" % (want, d)
        if kind in CIVIC and passes and d >= SEARCH:
            dd, cx, cy, s = passes[0]
            return cx, cy, s, "town: outdoors %d away (no building within %d)" % (dd, SEARCH)
    if kind in CIVIC and passes:
        dd, cx, cy, s = passes[0]
        return cx, cy, s, "town: outdoors %d away" % dd
    return None


def role(entries):
    names = {e.split(":")[0].strip().lower() for e in entries.split("|")}
    return ",".join(sorted(v for k, v in SERVICE_ROLES.items() if k in names))


def main():
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "p698-spawner-plan.csv"))) if r["record_kind"] == "stock"]
    stock_pass = json.load(open(os.path.join(OUT, "stock-pass.json")))   # regrade.py --baseline writes it
    gr = Grader()
    ledger = []
    for r in rows:
        r["_role"] = role(r["entries"])
        x, y, z = int(r["x"]), int(r["y"]), int(r["z"])
        hr = int(r["home_range"]) if r["home_range"] else 0
        kind = r["population_kind"]
        out = dict(facet=r["facet"], source=r["source"], guid=r["guid"], kind=kind, role=r["_role"], entries=r["entries"],
                   x=x, y=y, z=z, home_range=hr, p698=r["decision"], p669=r["p669_grade"])
        if r["import_status"] in ("not imported", "excluded by import hook"):
            out.update(action="skip", reason="never imported (" + r["import_status"] + ")")
        elif s7_owned(r):
            out.update(action="skip", reason=s7_owned(r))
        elif (r["facet"] == "Trammel" and r["source"] == "Spawns/post-uoml/trammel/Vendors.json"
              and in_box(x, y, HAVEN_ISLAND) and not in_box(x, y, HAVEN_TOWN)
              and stock_pass.get(r["facet"] + "/" + r["guid"], True)):
            found = outlying(gr, r, hr)
            if found:
                nx, ny, nz, why = found
                out.update(action="move", nx=nx, ny=ny, nz=nz, reason="ML New Haven's outlying hall, forest or rock on SoS; " + why)
            else:
                out.update(action="drop", reason="ML New Haven's outlying hall, forest or rock on SoS; no floor by its hall's new home")
        elif r["facet"] in ("Trammel", "Felucca") and NE_SNOW[0] <= x <= NE_SNOW[1] and NE_SNOW[2] <= y <= NE_SNOW[3]:
            out.update(action="drop", reason="inside P673's north-east snow closure (S14), P698's drop")
        elif gr.passes(x, y, z, hr, kind == "sea life") and not gr.unfit(x, y, hr, kind, r["facet"]):
            # a spawner that stands still keeps its floor; when SoS's floor there is 3 to 5 off, it takes SoS's (a ranged
            # one picks each spawn's Z itself, so its Z stays as the data has it)
            f = gr.floor(x, y, z) if hr <= 1 and kind != "sea life" else None
            if f is not None and abs(f - z) > 2:
                out.update(action="move", nx=x, ny=y, nz=f, reason="passes; Z corrected from %d to the floor at %d" % (z, f))
            else:
                out.update(action="keep", reason="passes on SoS")
        elif not stock_pass.get(r["facet"] + "/" + r["guid"], True):
            out.update(action="keep", reason="stock-tolerated: fails the same test on the stock map, where it works today")
        elif r["spawn_bounds"]:
            out.update(action="drop", reason="fails on SoS, and its explicit spawn rectangle cannot move with it")
        else:
            first = gr.unfit(x, y, hr, kind, r["facet"]) if gr.passes(x, y, z, hr, kind == "sea life") else "fails the walk"
            found = search(gr, r, x, y, z, hr, kind, r["facet"])
            if found:
                nx, ny, nz, why = found
                out.update(action="move", nx=nx, ny=ny, nz=nz, reason="%s; %s" % (first, why))
            elif first.startswith("its habitat changed"):
                # its range is still walkable land; a spawner on the wrong ground beats none
                out.update(action="keep", reason="%s; nothing matching within %d, kept (its home and range still pass the walk)"
                           % (first, SEARCH))
            else:
                out.update(action="drop", reason="%s; nothing matching within %d" % (first, SERVICE_SEARCH if r["_role"] else SEARCH))
        ledger.append(out)

    os.makedirs(OUT, exist_ok=True)
    cols = ["facet", "source", "guid", "kind", "role", "action", "x", "y", "z", "nx", "ny", "nz", "home_range", "p669", "p698",
            "reason", "entries"]
    with open(os.path.join(OUT, "ledger.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(ledger)
    c = collections.Counter((l["facet"], l["action"]) for l in ledger)
    k = collections.Counter((l["facet"], l["kind"], l["action"]) for l in ledger)
    with open(os.path.join(OUT, "summary.txt"), "w") as f:
        for key in sorted(c):
            print(*key, c[key], file=f)
        print(file=f)
        for key in sorted(k):
            print(*key, k[key], file=f)
    write_cs(ledger)
    print(open(os.path.join(OUT, "summary.txt")).read())


def write_cs(ledger):
    moves = sorted((l for l in ledger if l["action"] == "move"), key=lambda l: (l["facet"], l["guid"]))
    drops = sorted((l for l in ledger if l["action"] == "drop"), key=lambda l: (l["facet"], l["guid"]))
    lines = []
    lines.append("// GENERATED by shard-migration notes/cc-P681-tools/regrade.py from P698's ledger and the SoS map files. Do not")
    lines.append("// edit by hand: change regrade.py and re-run it. One row per stock spawner whose home moves or goes on the Siege of")
    lines.append("// Sosaria land (both facets read it). The ledger with a reason per spawner: notes/cc-P681-tools/out/ledger.csv.")
    lines.append("")
    lines.append("namespace Server;")
    lines.append("")
    lines.append("public static partial class ClusterFSosSpawnPlacements")
    lines.append("{")
    lines.append("    /// <summary>Spawners whose home moves: (facet, guid, x, y, z).</summary>")
    lines.append("    public static readonly (string Facet, string Guid, int X, int Y, int Z)[] Moves =")
    lines.append("    [")
    for l in moves:
        lines.append('        ("%s", "%s", %d, %d, %d),' % (l["facet"], l["guid"], l["nx"], l["ny"], l["nz"]))
    lines.append("    ];")
    lines.append("")
    lines.append("    /// <summary>Spawners left out on the SoS land: (facet, guid).</summary>")
    lines.append("    public static readonly (string Facet, string Guid)[] Drops =")
    lines.append("    [")
    for l in drops:
        lines.append('        ("%s", "%s"),' % (l["facet"], l["guid"]))
    lines.append("    ];")
    lines.append("}")
    path = os.path.join(SHARD, "server", "customizations", "ClusterFSosSpawnPlacementsTable.cs")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", path, len(moves), "moves", len(drops), "drops")


def baseline():
    """The same pass test on the stock maps, each facet on its own: a rule that fails stock data is the rule's fault."""
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "p698-spawner-plan.csv"))) if r["record_kind"] == "stock"
            and r["import_status"] not in ("not imported", "excluded by import hook")]
    out = collections.Counter()
    fails = []
    passed = {}
    for facet in ("Trammel", "Felucca"):
        gr = Grader(facet.lower())
        for r in rows:
            if r["facet"] != facet:
                continue
            hr = int(r["home_range"]) if r["home_range"] else 0
            ok = gr.passes(int(r["x"]), int(r["y"]), int(r["z"]), hr, r["population_kind"] == "sea life")
            out[(facet, r["population_kind"], ok)] += 1
            passed[facet + "/" + r["guid"]] = ok
            if not ok:
                fails.append((facet, r["population_kind"], r["source"], r["x"], r["y"], r["z"], hr))
    with open(os.path.join(OUT, "stock-pass.json"), "w") as f:
        json.dump(passed, f)
    with open(os.path.join(OUT, "baseline-stock.txt"), "w") as f:
        print("the pass test on the stock maps (True = passes)", file=f)
        for k in sorted(out):
            print(*k, out[k], file=f)
        print(file=f)
        for x in fails:
            print(*x, file=f)
    print(open(os.path.join(OUT, "baseline-stock.txt")).read()[:3000])


if __name__ == "__main__":
    if sys.argv[1:] == ["--baseline"]:
        baseline()
    else:
        main()
