"""cc-P685 (SoS swap S12): Felucca's 17 champion spawns on the Siege of Sosaria land.

    python tools/tests/test_sos_champions.py      (SL_SHARD_REPO: another work copy of the shard repo)

Facts, from the SoS map files (notes/cc-P685-tools/champs.py) and the shard's patch:
  1. A fact per altar: each of the 17 shipped sites passes champs.py's test on SoS. The platform is on its floor (or
     misses it on exactly the tiles it misses on stock, at stock's site). The 48 x 48 spawn area is walkable at least
     as stock's is, and clear of every town and guard zone (Trammel's SoS regions, the land Felucca shares) and S14's
     closures. The eject point has a floor. And no two spawn areas overlap.
  2. The patch (server/patches/GenChamps-sos-sites.patch) puts in GenChamps.cs exactly champs.py's sites: pinned's,
     with P696's three moves and LL08's new eject point.
Needs the SoS map files; skipped without them.
"""
import os
import re
import sys
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent.parent
TOOLS = DOCS / "notes" / "cc-P685-tools"
SHARD = Path(os.environ.get("SL_SHARD_REPO", r"D:\ShatteredLegacy"))
os.environ["SL_SHARD"] = str(SHARD)
PATCH = SHARD / "server" / "patches" / "GenChamps-sos-sites.patch"
SOS = DOCS / "notes" / "cc-P481-tools" / "scratch" / "sos" / "Map1.mul"
sys.path.insert(0, str(TOOLS))


@unittest.skipUnless(SOS.exists() and PATCH.exists(), "needs the SoS map files and the shard repo's patch")
class SosChampions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import champs
        cls.c = champs
        cls.g = champs.sosgrid.load()
        cls.k = champs.sosgrid.load("felucca")
        cls.surf = champs.sosgrid.Surfaces("sos")
        cls.stock_surf = champs.sosgrid.Surfaces("felucca")
        cls.guards = champs.guard_rects()
        cls.stock = {i: c for i, _, _, c, _ in champs.STOCK}

    def test_1_every_altar_passes_on_sos(self):
        for i, kind, typ, c, e, action in self.c.sites():
            with self.subTest(altar=i):
                why, s, s0 = self.c.judge(self.surf, self.g["stand"], self.k["stand"], self.guards, i, c, e,
                                          self.stock[i], self.stock_surf)
                self.assertEqual([], why, f"{i} at {c} ({action})")
        ss = self.c.sites()
        for a in range(len(ss)):
            for b in range(a + 1, len(ss)):
                self.assertFalse(self.c.overlaps(self.c.area(*ss[a][3][:2]), self.c.area(*ss[b][3][:2])), (ss[a][0], ss[b][0]))

    def test_2_the_patch_ships_exactly_these_sites(self):
        text = PATCH.read_text(encoding="utf-8")
        added = re.findall(r"^\+.*new Point3D\((-?\d+), (-?\d+), (-?\d+)\), Map\.Felucca, new Point3D\((-?\d+), (-?\d+), "
                           r"(-?\d+)\), Map\.Felucca\)", text, re.M)
        removed = re.findall(r"^-.*new Point3D\((-?\d+), (-?\d+), (-?\d+)\), Map\.Felucca, new Point3D\((-?\d+), (-?\d+), "
                             r"(-?\d+)\), Map\.Felucca\)", text, re.M)
        want_new = {tuple(nc) + tuple(ne) for nc, ne in self.c.MOVES.values()}
        want_old = {tuple(c) + tuple(e) for i, _, _, c, e in self.c.STOCK if i in self.c.MOVES}
        self.assertEqual(want_new, {tuple(int(v) for v in a) for a in added})
        self.assertEqual(want_old, {tuple(int(v) for v in r) for r in removed})


if __name__ == "__main__":
    unittest.main()
