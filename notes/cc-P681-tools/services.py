r"""cc-P681: every stock town keeps its bank, healer, smith and provisioner on the SoS land.
For each Trammel and Felucca TownRegion in pinned regions.json that the shard registers (MinExpansion and MaxExpansion
around ML-era Endless Journey, as RegionJsonSerializer.LoadRegions filters), the stock spawners whose home lies in it
after regrade.py's moves and drops (out/ledger.csv), by role: Banker, Healer (or HealerGuildmaster, or a
WanderingHealer), Blacksmith (or BlacksmithGuildmaster, Weaponsmith, Armorer, IronWorker), Provisioner.
New Haven is S7's (P678: pre-UOML Haven's own spawners, uoml/trammel/Vendors.json), so it reads those for Trammel.
    python -P services.py > out/services.txt        (exit 1 when a town lost a role stock gives it)
A role stock never had in a town (a field, the Heartwood, Cove's bank) is listed, not counted.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PINNED = "D:/UO/ModernUO-pinned/Distribution/Data"
ROLES = {
    "bank": {"banker"},
    "healer": {"healer", "healerguildmaster", "wanderinghealer"},
    "smith": {"blacksmith", "blacksmithguildmaster", "weaponsmith", "armorer", "ironworker"},
    "provisioner": {"provisioner"},
}
EXPANSIONS = ["None", "T2A", "UOR", "UOTD", "LBR", "AOS", "SE", "ML", "SA", "HS", "TOL", "EJ"]
SHARD_EXPANSION = "EJ"
# towns that are not towns for this check: no stock vendors by design
NOT_TOWNS = {"Haven"}      # pinned's pre-UOML Haven ends at SE; S7 registers it as New Haven


def towns():
    out = []
    for r in json.load(open(os.path.join(PINNED, "regions.json"))):
        if r.get("$type") != "TownRegion" or r.get("Map") not in ("Trammel", "Felucca") or not r.get("Name"):
            continue
        lo = EXPANSIONS.index(r.get("MinExpansion", "None"))
        hi = EXPANSIONS.index(r.get("MaxExpansion", "EJ"))
        if not lo <= EXPANSIONS.index(SHARD_EXPANSION) <= hi or r["Name"] in NOT_TOWNS:
            continue
        rects = [(a["x1"], a["y1"], a["x2"], a["y2"]) for a in r["Area"]]
        out.append((r["Map"], r["Name"], rects))
    return out


def inside(x, y, rects):
    return any(a <= x < c and b <= y < d for a, b, c, d in rects)   # x2, y2 exclusive, as the converter builds them


def homes(stock=False):
    """stock: every imported spawner at its stock home (the baseline: what stock already lacks)."""
    out = []
    for l in csv.DictReader(open(os.path.join(HERE, "out", "ledger.csv"))):
        if l["action"] == "skip" or (l["action"] == "drop" and not stock):
            continue
        x, y = (int(l["nx"]), int(l["ny"])) if l["action"] == "move" and not stock else (int(l["x"]), int(l["y"]))
        names = {e.strip().lower() for e in l["entries"].split("|")}
        out.append((l["facet"], x, y, names))
    # S7's New Haven: pinned uoml/trammel/Vendors.json inside the town (P678's ClusterFHavenTownSpawns admits these)
    for s in json.load(open(os.path.join(PINNED, "Spawns", "uoml", "trammel", "Vendors.json"))):
        x, y, _ = s["location"]
        if 3568 <= x <= 3761 and 2460 <= y <= 2712:
            out.append(("Trammel", x, y, {e["name"].lower() for e in s["entries"]}))
    return out


def main():
    stock = sys.argv[1:] == ["--stock"]
    hs = homes(stock)
    base = homes(True)
    missing = 0
    for facet, name, rects in towns():
        if name == "New Haven" and facet == "Trammel":
            rects = [(3590, 2460, 3709, 2686), (3568, 2552, 3591, 2632), (3708, 2558, 3762, 2713), (3695, 2685, 3709, 2713)]
        have = {role: sum(1 for f, x, y, n in hs if f == facet and inside(x, y, rects) and n & names)
                for role, names in ROLES.items()}
        had = {role: sum(1 for f, x, y, n in base if f == facet and inside(x, y, rects) and n & names)
               for role, names in ROLES.items()}
        lack = [r for r, c in have.items() if c == 0 and had[r] > 0]       # lost on SoS
        never = [r for r, c in have.items() if c == 0 and had[r] == 0]     # stock never had it there
        missing += len(lack)
        print("%-8s %-28s %s%s%s" % (facet, name, " ".join("%s %d" % kv for kv in have.items()),
                                     ("   LOST " + ", ".join(lack)) if lack else "",
                                     ("   (stock has none: " + ", ".join(never) + ")") if never else ""))
    print("MISSING", missing)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
