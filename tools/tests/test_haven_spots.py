"""cc-P678 (SoS swap S7): every New Haven spot in HavenSpots.cs stands on open ground of Siege of Sosaria 3.0's Haven.

    python -m unittest tools/tests/test_haven_spots.py      (SL_SHARD_REPO: another work copy of the shard repo)

Facts, read from the code and the map files, nothing hand-copied:
  1. Every Point3D in server/customizations/Tutorial/HavenSpots.cs is open on SoS (not water, void or under an impassable
     static; notes/cc-P678-tools/townmap.py's reading), and its Z is that tile's floor (within 2).
  2. The start, Rook, the moongate's way out and the quest board are within 3 tiles of each other, as on the old plaza,
     and the bank, healer, dock and public moongate are inside the Haven town (x 3600-3760, y 2500-2665).
  3. The Fountain of Youth's 4 x 4 addon stands on open, flat tiles holding no static.
Needs the SoS map files (notes/cc-P481-tools/scratch/sos); skipped without them.
"""
import os
import re
import sys
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent.parent
SHARD = Path(os.environ.get("SL_SHARD_REPO", r"D:\ShatteredLegacy"))
SPOTS = SHARD / "server" / "customizations" / "Tutorial" / "HavenSpots.cs"
SOS = DOCS / "notes" / "cc-P481-tools" / "scratch" / "sos" / "Map1.mul"
sys.path.insert(0, str(DOCS / "notes" / "cc-P678-tools"))
TOWN = (3600, 2500, 3760, 2665)


def spots():
    """{name: (x, y, z)} for every Point3D in HavenSpots.cs (a property's initializer or a readonly field)."""
    text = SPOTS.read_text()
    out = {}
    for m in re.finditer(r"Point3D (\w+)(?: \{ get; set; \})? = new\((\d+), (\d+), (-?\d+)\);", text):
        out[m.group(1)] = (int(m.group(2)), int(m.group(3)), int(m.group(4)))
    return out


@unittest.skipUnless(SPOTS.exists() and SOS.exists(), "needs the shard repo and the SoS map files")
class HavenSpotsOnSos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import townmap
        cls.tile = staticmethod(townmap.tile)
        cls.spots = spots()

    def test_1_every_spot_is_open_ground_at_its_floor(self):
        self.assertGreaterEqual(len(self.spots), 8, self.spots)
        bad = []
        for name, (x, y, z) in sorted(self.spots.items()):
            kind, fz = self.tile(x, y)
            if kind != "open" or abs(fz - z) > 2:
                bad.append("%s %d,%d,%d is %s at Z %d" % (name, x, y, z, kind, fz))
        self.assertEqual([], bad)

    def test_3_the_fountain_of_youth_fits_flat_on_clear_ground(self):
        """Its addon (pinned StoneFountainAddon's pieces) covers x -2..+1, y -2..+1: every tile open, one Z, no static."""
        import townmap
        c = townmap.load()
        x0, y0, z0 = self.spots["FountainOfYouth"]
        for x in range(x0 - 2, x0 + 2):
            for y in range(y0 - 2, y0 + 2):
                self.assertEqual(("open", z0), self.tile(x, y), (x, y))
                self.assertFalse(((c["sx"] == x) & (c["sy"] == y)).any(), "a static at %d,%d under the fountain" % (x, y))

    def test_2_the_start_group_is_together_and_the_services_are_in_the_town(self):
        s = self.spots
        group = [s[n] for n in ("Start", "Rook", "MoongateExit", "QuestBoard")]
        for a in group:
            for b in group:
                self.assertLessEqual(max(abs(a[0] - b[0]), abs(a[1] - b[1])), 3, (a, b))
        cx, cy, _ = s["Centre"]
        vx, vy, _ = s["VetSpot"]
        self.assertLessEqual(max(abs(vx - cx), abs(vy - cy)), 60, "the vet is within 60 tiles of the centre (FindTownVet)")
        for n in ("Bank", "Healer", "Dock", "PublicMoongate", "Centre", "VetSpot"):
            x, y, _ = s[n]
            self.assertTrue(TOWN[0] <= x <= TOWN[2] and TOWN[1] <= y <= TOWN[3], "%s %d,%d is outside the Haven town" % (n, x, y))


if __name__ == "__main__":
    unittest.main()
