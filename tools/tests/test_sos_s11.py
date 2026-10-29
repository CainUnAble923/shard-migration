"""cc-P684 (SoS swap S11): treasure maps, houses, boats and docks, and SOS bottles on the Siege of Sosaria land.

    python tools/tests/test_sos_s11.py      (SL_SHARD_REPO: another work copy of the shard repo)

Facts, from the SoS map files and the shard's data (notes/cc-P684-tools):
  1. treasure.cfg: the shipped file is treasure.py's output; every spot passes TreasureMap.ValidateLocation's land rules
     on SoS (or is stock-tolerated: fails them on stock's own map too, on a tile SoS left alone), and none is in a town,
     a dungeon or an S14 closure; the new land holds one spot per 7,000 of its dry tiles; the Haven box keeps spots
     for the level-0 maps.
  2. Houses: each of the author's new towns is a guarded TownRegion and each of his dungeons a DungeonRegion in P676's
     regions-trammel.json, so pinned's HousePlacement refuses a house there (GuardedRegion and DungeonRegion
     AllowHousing are false).
  3. Docks: at every author dock but the two the map closes (Haven's harbour is a closed body of water on SoS, and
     Nujel'm's docks are inland now), a small boat floats within 15 tiles in a sea a boat sails out of and back; those
     two still fail as stated, so a change to the map that fixes them shows.
  4. SOS bottles: 1,000 replays of SOS.cs FindLocation never return Point3D.Zero and every pick is open sea (not the new
     continent's land, not void); the isle lies outside its rectangle.
Needs the SoS map files; skipped without them.
"""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent.parent
TOOLS = DOCS / "notes" / "cc-P684-tools"
SHARD = Path(os.environ.get("SL_SHARD_REPO", r"D:\ShatteredLegacy"))
SOS = DOCS / "notes" / "cc-P481-tools" / "scratch" / "sos" / "Map1.mul"
AUTHOR_REGIONS = DOCS / "notes" / "sos-author-data" / "Regions.xml"
NEW_TOWNS = ["Valunstead", "Hammerhill", "Kameron Kove", "Elmhaven", "Kettleburg", "Fort Yondall", "Elandrim Nur Shaz"]
CLOSED_DOCKS = {
    "Haven Docks": "in a closed body of",
    "Nujel'm Docks": "no boat fits in any water within 60",
}


def run(script, **env):
    e = dict(os.environ, SL_SHARD=str(SHARD), **env)
    r = subprocess.run([sys.executable, "-P", str(TOOLS / script)], capture_output=True, text=True, env=e)
    if r.returncode:
        raise AssertionError(r.stderr[-3000:])
    return r.stdout


@unittest.skipUnless(SOS.exists() and (SHARD / "server" / "data" / "treasure.cfg").exists(),
                     "needs the SoS map files and the shard repo's treasure.cfg")
class SosS11(unittest.TestCase):
    def test_1_treasure_spots(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "treasure.cfg")
            text = run("treasure.py", P684_TREASURE_OUT=out)
            self.assertEqual(Path(out).read_bytes(), (SHARD / "server" / "data" / "treasure.cfg").read_bytes())
        sys.path.insert(0, str(TOOLS))
        os.environ["SL_SHARD"] = str(SHARD)
        import sea
        import treasure
        S = sea.load()
        ok, excluded = treasure.judge_mask(S)
        K = treasure.stock_map()
        stock_ok, _ = treasure.judge_mask(K, treasure.stock_regions(), [])
        spots = treasure.read_cfg(SHARD / "server" / "data" / "treasure.cfg")
        self.assertEqual(len(spots), len(set(spots)))
        bad = [(x, y) for x, y in spots
               if excluded[x, y] or not (ok[x, y] or (not stock_ok[x, y] and treasure.same_tile(S, K, x, y)))]
        self.assertEqual([], bad)
        rows = list(csv.DictReader(open(TOOLS / "out" / "treasure.csv")))
        added = sum(1 for r in rows if r["action"] == "added")
        n_new = int(text.split("new land: ")[1].split(" ")[0])
        self.assertEqual(round(n_new / 7000), added)
        self.assertGreater(added, 200)
        bx = treasure.HAVEN_BOX
        self.assertGreaterEqual(sum(1 for x, y in spots if bx[0] <= x <= bx[2] and bx[1] <= y <= bx[3]), 5)

    def test_2_new_towns_and_the_authors_dungeons_refuse_houses(self):
        import re
        regs = {r["Name"]: r for r in json.load(open(SHARD / "server" / "data" / "regions-trammel.json", encoding="utf-8"))
                if r.get("Name")}
        for t in NEW_TOWNS:
            self.assertEqual("TownRegion", regs[t]["$type"], t)
            self.assertFalse(regs[t].get("GuardsDisabled", False), t)
        xml = AUTHOR_REGIONS.read_text(encoding="utf-8", errors="replace")
        xml = xml[xml.index('<Facet name="Trammel">'):]
        xml = xml[:xml.index("</Facet>")]          # his Trammel block (the file holds every facet's)
        dungeons = set(re.findall(r'<region type="DungeonRegion"[^>]*name="([^"]+)"', xml))
        self.assertGreater(len(dungeons), 20)
        missing = sorted(d for d in dungeons if d not in regs)
        wrong = sorted(d for d in dungeons if d in regs and regs[d]["$type"] != "DungeonRegion")
        self.assertEqual([], wrong)
        self.assertEqual([], missing)

    def test_3_and_4_docks_float_a_boat_and_sos_picks_are_open_sea(self):
        text = run("docks_sos.py")
        rows = list(csv.DictReader(open(TOOLS / "out" / "docks.csv", encoding="utf-8")))
        self.assertEqual(11, len(rows))
        for r in rows:
            if r["dock"] in CLOSED_DOCKS:
                self.assertEqual("", r["boat_distance"], r["dock"])
                self.assertIn(CLOSED_DOCKS[r["dock"]], r["problem"], r["dock"])
                continue
            self.assertNotEqual("", r["boat_distance"], r["dock"] + ": " + r["problem"])
            # in a no-housing region, or over water (no house stands there); Skara Brae's east dock point is one tile
            # east of pinned's own one-tile dock strip, which P676 kept as stock drew it
            self.assertTrue(r["no_housing_regions"] or r["ground"] == "water" or r["dock"] == "Skara Brae East Docks",
                            r["dock"])
        self.assertIn("Point3D.Zero 0;", text)
        self.assertIn("accepted not in the open sea, in the new continent, void or the isle: 0", text)


if __name__ == "__main__":
    unittest.main()
