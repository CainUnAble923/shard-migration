"""cc-P682 (SoS swap S10): people for the author's new towns and keeps, and wild creatures on his new land.

    python tools/tests/test_sos_new_spawns.py      (SL_SHARD_REPO: another work copy of the shard repo)

Facts, from the SoS map files and the shard's spawn set (server/data/Spawns/sos, made by
notes/cc-P682-tools/build_spawns.py):
  1. Every spawner of the set has its home on walkable SoS land: P681's walk test (regrade.Grader.passes), re-run here.
  2. Every new town has a banker, a healer, a smith and a provisioner on each facet, inside the town's region (P676),
     standing indoors (a roof over the tile) on a tile a player walks to from the town's go point or the land around.
  3. No wild spawner stands in a town (or within 10 of one), an S14 closure, a dungeon region, within 12 of an author
     dungeon entrance, or past x 5120; none copies a held stock spawner (P698's B3 tier, chests, camps); every entry
     name is one stock's data uses.
  4. Each of the five keeps has its garrison (OrderGuard only) on each facet, within 40 tiles of the author's point.
  5. Density per 100 dry tiles: every new town at or above 95 percent of stock's town median on its facet; each new-land
     area within 10 percent of stock's rate for its terrain (out/density.txt).
  6. Guids are unique, are none of stock's, and the set is on Trammel and Felucca only.
Needs the SoS map files; skipped without them.
"""
import collections
import csv
import json
import os
import sys
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent.parent
TOOLS = DOCS / "notes" / "cc-P682-tools"
SHARD = Path(os.environ.get("SL_SHARD_REPO", r"D:\ShatteredLegacy"))
os.environ["SL_SHARD"] = str(SHARD)
SET = SHARD / "server" / "data" / "Spawns" / "sos"
SOS = DOCS / "notes" / "cc-P481-tools" / "scratch" / "sos" / "Map1.mul"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(DOCS / "notes" / "cc-P681-tools"))


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def spawn_set():
    out = {}
    for p in sorted(SET.rglob("*.json")):
        out[p.relative_to(SET).as_posix()] = json.loads(p.read_text(encoding="utf-8"))
    return out


@unittest.skipUnless(SET.exists() and SOS.exists(), "needs the shard repo's SoS spawn set and the SoS map files")
class SosNewSpawns(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import common
        import build_spawns
        cls.common, cls.bs = common, build_spawns
        cls.files = spawn_set()
        cls.regions = common.regions()

    def test_1_every_home_passes_the_walk_on_sos(self):
        import regrade
        gr = regrade.Grader()
        bad = []
        for rel, recs in self.files.items():
            for r in recs:
                x, y, z = r["location"]
                if not gr.passes(x, y, z, r["homeRange"], False):
                    bad.append(f"{rel} {r['map']} {r['name']} at {x},{y},{z}")
        self.assertEqual([], bad)

    def test_2_every_new_town_has_its_core_services_indoors_and_reachable(self):
        g = self.common.grid()
        recs = self.common.region_records()
        missing, bad = [], []
        for town in self.common.TOWNS:
            rects = self.regions[town]
            rec = next(r for r in recs if r.get("Name") == town)
            t = self.bs.Town(town, rects, (rec["GoLocation"]["x"], rec["GoLocation"]["y"]), margin=20)
            pts = self.bs.author_points().get(town, {})
            tb = self.bs.Town(town, rects, pts["Bank"][:2], margin=20) if "Bank" in pts else t
            for facet in ("Trammel", "Felucca"):
                rows = [r for r in self.files["towns/" + town.replace(" ", "") + ".json"] if r["map"] == facet]
                for role in ("Banker", "Healer", "Blacksmith", "Provisioner"):
                    have = [r for r in rows if any(e["name"] == role for e in r["entries"])]
                    if not have:
                        missing.append(f"{facet} {town} {role}")
                    for r in have:
                        x, y, _ = r["location"]
                        why = []
                        if not self.common.in_rects(x, y, rects):
                            why.append("outside the region")
                        if not g["covered"][x, y]:
                            why.append("not indoors")
                        if not (t.reach[x - t.x1, y - t.y1] or tb.reach[x - tb.x1, y - tb.y1]):
                            why.append("not reachable")
                        if why:
                            bad.append(f"{facet} {town} {role} at {x},{y}: {', '.join(why)}")
        self.assertEqual([], missing)
        self.assertEqual([], bad)

    def test_3_wild_spawners_keep_out_of_towns_closures_and_dungeons(self):
        areas, isl, ok = self.bs.wild_mask()
        stock_names = set()
        for root in ("post-uoml", "shared"):
            for p in (Path(self.common.PINNED) / "Spawns" / root).rglob("*.json"):
                for s in json.loads(p.read_text()):
                    stock_names.update(e["name"] for e in s["entries"])
        bad = []
        for rel, recs in self.files.items():
            if not rel.startswith("wild/"):
                continue
            for r in recs:
                x, y, _ = r["location"]
                if not ok[x, y]:
                    bad.append(f"{rel} {r['name']} at {x},{y}: in a town, closure or dungeon, or not open land")
                for e in r["entries"]:
                    if self.bs.held(e["name"]) or e["name"] not in stock_names:
                        bad.append(f"{rel} {r['name']}: {e['name']}")
        self.assertEqual([], bad)
        self.assertGreater(sum(len(v) for k, v in self.files.items() if k.startswith("wild/")), 500)

    def test_4_every_keep_has_its_garrison(self):
        pts = {k: v for d in self.bs.author_points().values() for k, v in d.items()}
        pts["Khalahandra Keep"] = self.bs.author_points()["Khalahandra Keep"]["Entrance"]
        for keep, n in self.bs.KEEPS.items():
            recs = self.files["keeps/" + keep.replace(" ", "") + ".json"]
            for facet in ("Trammel", "Felucca"):
                rows = [r for r in recs if r["map"] == facet]
                self.assertEqual(n, sum(r["count"] for r in rows), f"{facet} {keep}")
                for r in rows:
                    self.assertEqual(["OrderGuard"], [e["name"] for e in r["entries"]])
                    x, y, _ = r["location"]
                    self.assertLessEqual(max(abs(x - pts[keep][0]), abs(y - pts[keep][1])), 40, f"{keep} {x},{y}")

    def test_5_density_meets_stocks(self):
        rows = read_csv(TOOLS / "out" / "density.csv")
        for facet in ("Trammel", "Felucca"):
            st = sorted(float(r["per100"]) for r in rows if r["facet"] == facet and r["kind"] == "stock town")
            med = st[len(st) // 2]
            for town in self.common.TOWNS:
                dry = next(int(r["dry"]) for r in rows if r["facet"] == facet and r["kind"] == "new town" and r["name"] == town)
                n = sum(r["count"] for r in self.files["towns/" + town.replace(" ", "") + ".json"] if r["map"] == facet)
                self.assertGreaterEqual(100.0 * n / dry, 0.95 * med, f"{facet} {town}")
            wd = read_csv(TOOLS / "out" / f"wild-density-{facet.lower()}.csv")
            target = collections.Counter()
            for r in wd:
                target[r["file"]] += float(r["target"])
            for f, want in target.items():
                have = sum(r["count"] for r in self.files["wild/" + f + ".json"] if r["map"] == facet)
                self.assertLess(abs(have - want), 0.10 * want, f"{facet} {f}: {have} placed, stock's rate gives {want:.0f}")

    def test_6_guids_are_unique_and_not_stocks(self):
        stock = set()
        for root in ("post-uoml", "shared", "uoml"):
            for p in (Path(self.common.PINNED) / "Spawns" / root).rglob("*.json"):
                stock.update(s["guid"] for s in json.loads(p.read_text()))
        guids = [r["guid"] for recs in self.files.values() for r in recs]
        self.assertEqual(len(guids), len(set(guids)))
        self.assertEqual(set(), set(guids) & stock)
        self.assertEqual({"Trammel", "Felucca"}, {r["map"] for recs in self.files.values() for r in recs})


if __name__ == "__main__":
    unittest.main()
