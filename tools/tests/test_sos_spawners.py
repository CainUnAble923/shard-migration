"""cc-P681 (SoS swap S9): pinned's stock spawners on the Siege of Sosaria land.

    python tools/tests/test_sos_spawners.py      (SL_SHARD_REPO: another work copy of the shard repo)

Facts, from the SoS map files, P698's ledger of the stock data, cc-P681's ledger and the shard's generated table:
  1. Every stock spawner the shard imports and does not leave out has its home and range on walkable land on SoS (sea
     life: on water), at the home the table gives it: the walk test of notes/cc-P681-tools/regrade.py (Grader.passes),
     re-run here, not read from the ledger. The only exceptions are the stock-tolerated ones, which fail the same test on
     the stock map where they work today (listed in the ledger, under 2 percent).
  2. Every move stays within 20 tiles of the stock home (40 for a town's banker, healer, smith or provisioner; a Haven
     shopkeeper goes to its trade's shop in the author's town, and ML New Haven's outlying vendors go by their hall's new
     home there, wherever in the town), and the
     shard's table (server/customizations/ClusterFSosSpawnPlacementsTable.cs) holds exactly the ledger's moves and drops.
  3. Every stock town keeps the bank, healer, smith and provisioner it has in stock (notes/cc-P681-tools/services.py).
Needs the SoS and stock map files; skipped without them.
"""
import csv
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent.parent
TOOLS = DOCS / "notes" / "cc-P681-tools"
SHARD = Path(os.environ.get("SL_SHARD_REPO", r"D:\ShatteredLegacy"))
TABLE = SHARD / "server" / "customizations" / "ClusterFSosSpawnPlacementsTable.cs"
SOS = DOCS / "notes" / "cc-P481-tools" / "scratch" / "sos" / "Map1.mul"
sys.path.insert(0, str(TOOLS))


def ledger():
    with open(TOOLS / "out" / "ledger.csv") as f:
        return list(csv.DictReader(f))


@unittest.skipUnless(TABLE.exists() and SOS.exists(), "needs the shard repo and the SoS map files")
class SosSpawners(unittest.TestCase):
    def test_1_every_kept_or_moved_home_passes_the_walk_on_sos(self):
        import regrade
        gr = regrade.Grader()
        bad, tolerated = [], 0
        for l in ledger():
            if l["action"] in ("skip", "drop"):
                continue
            x, y, z = (int(l["nx"]), int(l["ny"]), int(l["nz"])) if l["action"] == "move" else (int(l["x"]), int(l["y"]), int(l["z"]))
            if gr.passes(x, y, z, int(l["home_range"]), l["kind"] == "sea life"):
                continue
            if l["reason"].startswith("stock-tolerated"):
                tolerated += 1
                continue
            bad.append("%s %s %s at %d,%d,%d" % (l["facet"], l["source"], l["guid"], x, y, z))
        self.assertEqual([], bad)
        self.assertLess(tolerated, 0.02 * len(ledger()), tolerated)

    def test_2_moves_stay_near_and_the_table_is_the_ledger(self):
        rows = ledger()
        for l in rows:
            if l["action"] == "move":
                if "the Haven shop of its trade" in l["reason"] or "into the author's town" in l["reason"]:
                    # to its trade's shop in the author's Haven town, wherever in the town that is
                    self.assertTrue(3568 <= int(l["nx"]) <= 3761 and 2460 <= int(l["ny"]) <= 2712, l["guid"])
                    continue
                d = max(abs(int(l["nx"]) - int(l["x"])), abs(int(l["ny"]) - int(l["y"])))
                self.assertLessEqual(d, 40 if l["role"] else 20, l["guid"])
        text = TABLE.read_text(encoding="utf-8")
        moves = set(re.findall(r'\("(\w+)", "([0-9a-f-]{36})", (-?\d+), (-?\d+), (-?\d+)\)', text))
        drops = set(re.findall(r'\("(\w+)", "([0-9a-f-]{36})"\),', text))
        self.assertEqual({(l["facet"], l["guid"], l["nx"], l["ny"], l["nz"]) for l in rows if l["action"] == "move"}, moves)
        self.assertEqual({(l["facet"], l["guid"]) for l in rows if l["action"] == "drop"}, drops)

    def test_3_no_town_loses_a_core_service(self):
        r = subprocess.run([sys.executable, "-P", str(TOOLS / "services.py")], capture_output=True, text=True)
        self.assertEqual(0, r.returncode, r.stdout[-2000:])
        self.assertIn("MISSING 0", r.stdout)


if __name__ == "__main__":
    unittest.main()
