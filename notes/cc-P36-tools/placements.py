# Per-file summary of literal placement coordinates in our seeders/decorators, from coords_all.csv
import csv, os
from collections import defaultdict
here = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(here, "coords_all.csv"))))
B = "\\"
files = {
    "ClusterFNewHavenSeeder.cs": "Trammel", "ClusterFNewHavenServicesSeeder.cs": "Trammel",
    "ClusterFInstitutionSeeder.cs": "Trammel (+1 TerMur)", "ClusterFMineCampSeeder.cs": "Trammel",
    "ClusterFMineCampLayout.cs": "Trammel", "ClusterFRegistrarOfficeLayout.cs": "Trammel",
    "ClusterFRegistrarOfficeSeeder.cs": "Trammel", "ClusterFRoyalCitySeeder.cs": "TerMur",
    "ClusterFGuildHallSeeder.cs": "via GuildLocations", "ClusterFGuildStarterPath.cs": "Trammel (+1 TerMur)",
    "ClusterFOldHavenSeeder.cs": "Trammel", "ClusterFOldHavenCleanup.cs": "Trammel",
    "ClusterFSouthMineDecor.cs": "Trammel", "ClusterFResetStone.cs": "Trammel", "ClusterFAreaScan.cs": "Trammel",
    "CharacterCreation.cs": "Trammel", B.join(["Engines", "ML Quests", "Items", "NewHavenQuestBoard.cs"]): "Trammel",
    B.join(["Services", "Revamped Dungeons", "DespiseRevamped", "Setup.cs"]): "Trammel",
    B.join(["Services", "Revamped Dungeons", "DespiseRevamped", "DespiseSpawns.cs"]): "Trammel",
    B.join(["Services", "Revamped Dungeons", "DespiseRevamped", "DespiseController.cs"]): "Trammel",
    B.join(["Services", "Revamped Dungeons", "DespiseRevamped", "Region.cs"]): "Trammel",
    B.join(["Services", "Revamped Dungeons", "Shame Revamped", "Generate.cs"]): "Fel+Tram",
    B.join(["Services", "Revamped Dungeons", "Shame Revamped", "ShameSpawns.cs"]): "Fel+Tram",
    B.join(["Services", "Revamped Dungeons", "Shame Revamped", "ShameWall.cs"]): "Fel+Tram",
}
by = defaultdict(list)
for r in rows:
    if r["file"] in files: by[r["file"]].append(r)
out = []
for f, m in files.items():
    rs = by.get(f, [])
    w = [r for r in rs if int(r["x"]) >= 300 and int(r["y"]) >= 10]
    if not w:
        print(f"| {f} | {m} | 0 | - | - | - | - |"); continue
    lines = sorted(int(r["line"]) for r in w)
    hit = any(r["hit0"] == "True" or r["hit1"] == "True" for r in w)
    d = min(min(float(r["d0"]), float(r["d1"])) for r in w)
    print(f"| {f} | {m} | {len(w)} | {lines[0]}-{lines[-1]} | {min(int(r['x']) for r in w)}-{max(int(r['x']) for r in w)} | "
          f"{min(int(r['y']) for r in w)}-{max(int(r['y']) for r in w)} | {'HIT' if hit else 'no'}, {d:.0f} |")
    out += [dict(r, facet=m) for r in w]
with open(os.path.join(here, "coords_placements.csv"), "w", newline="", encoding="ascii", errors="replace") as fh:
    wr = csv.DictWriter(fh, fieldnames=list(out[0].keys())); wr.writeheader(); wr.writerows(out)
print("rows", len(out), "hits", sum(1 for r in out if r["hit0"] == "True" or r["hit1"] == "True"))
