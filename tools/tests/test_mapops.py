"""cc-P188: the map patch (scripts/mapbuild/mapops.py) and its two appliers agree.

    python -m unittest tools/tests/test_mapops.py

Facts, on a synthetic facet (the real layout, one chunk, no EA bytes):
  1. diff finds exactly the cells and statics that changed, and apply rebuilds the edited files: land byte for byte,
     statics block by block; EA's statics file is a prefix of the output; a block emptied by removals is unlinked.
  2. A block EA changed after the patch was made is reported as drifted and still patched; a static EA moved is
     reported as missing and left alone.
  3. The PowerShell applier (player-package/payload/app/Apply-MapOps.ps1, what players run) writes the same three files
     byte for byte as the Python one, and its stamp makes the second run a skip.
  4. The shipped patch (player-package/vendor/shattered-legacy-map/trammel.mapops) parses, lists its touched blocks,
     and every line lies inside the Burrows rectangle (x 5136-5247, y 1128-1263) or the way in (the Second Bank of
     Haven, 3614-3626 x 2608-2624), but for cc-P276's four removals in the tutorial farm (the two trees inside its
     fence, x 3381-3399, y 2603-2619, and nothing else there); when the pristine client data and P167's scratch build
     are on this PC, the patch without the farm's lines rebuilds the scratch build exactly (the farm was never in it).
ASCII only. Temporary folders only.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(DOCS / "scripts"))
from mapbuild import mapops, uofiles  # noqa: E402

SHARD = Path(r"D:\ShatteredLegacy")
APPLIER = SHARD / "player-package" / "payload" / "app" / "Apply-MapOps.ps1"
SHIPPED = SHARD / "player-package" / "vendor" / "shattered-legacy-map" / "trammel.mapops"
SCRATCH = Path(r"D:\UO\cc-p167-work\scratch-client")
FACET = 1

BURROWS = (5136, 1128, 5247, 1263)
WAY_IN = (3614, 2608, 3626, 2624)
FARM = (3381, 2603, 3399, 2619)
# cc-P276: the two trees inside the tutorial farm's fence, trunk and foliage (design/tutorial-farm/west_v3_layout.json).
FARM_REMOVALS = ["S- 3388 2607 19 3302 0", "S- 3388 2607 19 3303 0", "S- 3396 2616 38 3296 0", "S- 3396 2616 38 3297 0"]


def inside(x, y, r):
    return r[0] <= x <= r[2] and r[1] <= y <= r[3]


def without_farm(text):
    """The patch as P167's scratch build knows it: the farm's removals and their two block fingerprints dropped."""
    farm_blocks = {(int(l.split()[1]) >> 3) * 512 + (int(l.split()[2]) >> 3) for l in FARM_REMOVALS}
    keep = [l for l in text.splitlines() if l not in FARM_REMOVALS and not (l.startswith("B ") and int(l.split()[1]) in farm_blocks)]
    return "\n".join(keep) + "\n"


def read(folder, name):
    with open(os.path.join(folder, name), "rb") as f:
        return f.read()


class Synthetic(unittest.TestCase):
    """base: the synthetic facet with a few 'EA' statics; edited: base plus our changes, made with uofiles' writers."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="p188-mapops-")
        self.base = mapops.synthetic_facet(os.path.join(self.tmp, "base"), FACET)
        # EA's own pieces: two in block (x 8-15, y 16-23), one alone in block (x 40-47, y 8-15)
        uofiles.write_statics(self.base, FACET, [(10, 20, 0, 0x0E31), (11, 20, 5, 0x0B26), (42, 9, 0, 0x1363)])
        self.edited = os.path.join(self.tmp, "edited")
        shutil.copytree(self.base, self.edited)
        self.land = {(10, 20): (0x0245, 0), (12, 21): (0x0246, -3), (40, 100): (0x025A, 12)}
        uofiles.write_land(self.edited, FACET, self.land)
        self.added = [(10, 21, 0, 0x0242), (13, 20, 13, 0x0A0C), (40, 101, 20, 0x0244)]
        uofiles.write_statics(self.edited, FACET, self.added)
        uofiles.remove_statics(self.edited, FACET, [(11, 20, 5, 0x0B26), (42, 9, 0, 0x1363)])
        self.ops = mapops.diff(self.base, self.edited, FACET)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def lines(self, kind):
        return [l for l in self.ops.splitlines() if l.startswith(kind + " ")]

    def test_1_the_diff_is_exactly_the_change_and_apply_rebuilds_it(self):
        self.assertEqual(["L 10 20 581 0", "L 12 21 582 -3", "L 40 100 602 12"], self.lines("L"))
        self.assertEqual(["S+ 10 21 0 578 0", "S+ 13 20 13 2572 0", "S+ 40 101 20 580 0"], self.lines("S+"))
        self.assertEqual(["S- 11 20 5 2854 0", "S- 42 9 0 4963 0"], self.lines("S-"))
        self.assertEqual(["F 1 3"], [l for l in self.ops.splitlines() if l.startswith("F ")])
        self.assertEqual(3, len(self.lines("B")))
        out = os.path.join(self.tmp, "out")
        drifted, missing = mapops.apply(self.ops, self.base, out, FACET)
        self.assertEqual(([], []), (drifted, missing))
        land_equal, bad = mapops.compare(out, self.edited, FACET)
        self.assertTrue(land_equal)
        self.assertEqual([], bad)
        self.assertTrue(read(out, "statics1.mul").startswith(read(self.base, "statics1.mul")))
        # the block that lost its only EA piece is unlinked
        idx = read(out, "staidx1.mul")
        b = (42 >> 3) * 512 + (9 >> 3)
        self.assertEqual(b"\xff\xff\xff\xff\xff\xff\xff\xff", idx[b * 12:b * 12 + 8])

    def test_2_drift_is_reported_and_patched_and_a_moved_static_is_left(self):
        moved = os.path.join(self.tmp, "moved")
        shutil.copytree(self.base, moved)
        uofiles.write_land(moved, FACET, {(9, 17): (0x0003, 1)})            # EA changed a cell in our first block
        uofiles.remove_statics(moved, FACET, [(42, 9, 0, 0x1363)])         # EA moved the piece we remove
        out = os.path.join(self.tmp, "out2")
        drifted, missing = mapops.apply(self.ops, moved, out, FACET)
        # both blocks EA touched drift: the cell and the moved piece
        self.assertEqual([(8 >> 3) * 512 + (16 >> 3), (42 >> 3) * 512 + (9 >> 3)], drifted)
        self.assertEqual([((42 >> 3) * 512 + (9 >> 3), (0x1363, 2, 1, 0, 0))], missing)
        m = uofiles.MapFile(out, FACET)
        self.assertEqual((0x0245, 0), m.get(10, 20))
        self.assertEqual((0x0003, 1), m.get(9, 17))

    @unittest.skipUnless(shutil.which("powershell") and APPLIER.exists(), "needs Windows PowerShell and the shard repo")
    def test_3_the_powershell_applier_writes_the_same_bytes_and_skips_on_its_stamp(self):
        ops = os.path.join(self.tmp, "trammel.mapops")
        with open(ops, "w", newline="\n") as f:
            f.write(self.ops)
        py = os.path.join(self.tmp, "py")
        mapops.apply(self.ops, self.base, py, FACET)
        ps = os.path.join(self.tmp, "ps")
        script = "$ErrorActionPreference='Stop'; . '%s'; Build-MapOverride -UoDir '%s' -Ops '%s' -OutDir '%s'" % (APPLIER, self.base, ops, ps)
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script], capture_output=True, text=True, timeout=600)
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        lines = [l for l in r.stdout.splitlines() if "=" in l]
        self.assertEqual(["map1legacymul.uop", "statics1.mul", "staidx1.mul"], [l.split("=")[0] for l in lines])
        for name in ("map1LegacyMUL.uop", "statics1.mul", "staidx1.mul"):
            self.assertEqual(read(py, name), read(ps, name), name)
        stamp = read(ps, "map-stamp.txt")
        self.assertTrue(stamp.startswith(b"uo-map 1\n"))
        before = os.path.getmtime(os.path.join(ps, "statics1.mul"))
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script], capture_output=True, text=True, timeout=600)
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        self.assertNotIn("patched copies", r.stdout)
        self.assertEqual(before, os.path.getmtime(os.path.join(ps, "statics1.mul")))


class Shipped(unittest.TestCase):
    @unittest.skipUnless(SHIPPED.exists(), "needs the shard repo")
    def test_4_the_shipped_patch_is_the_burrows_and_the_way_in_only(self):
        text = SHIPPED.read_text()
        facet, fps, land, adds, removes = mapops.parse(text)
        self.assertEqual(1, facet)
        self.assertEqual(int([l for l in text.splitlines() if l.startswith("F ")][0].split()[2]), len(fps))
        self.assertGreater(len(land), 11000)
        for x, y, t, z in land:
            self.assertTrue(inside(x, y, BURROWS), (x, y))
        for lines in (adds, removes):
            for b, rows in lines.items():
                bx, by = divmod(b, 512)
                for tid, cx, cy, z, hue in rows:
                    x, y = bx * 8 + cx, by * 8 + cy
                    self.assertTrue(inside(x, y, BURROWS) or inside(x, y, WAY_IN) or inside(x, y, FARM), (x, y, hex(tid)))
                    self.assertEqual(0, hue)
        self.assertEqual(3 + len(FARM_REMOVALS), sum(len(r) for r in removes.values()))
        farm = [l for l in text.splitlines() if l.startswith(("L ", "S+ ", "S- ")) and inside(int(l.split()[1]), int(l.split()[2]), FARM)]
        self.assertEqual(FARM_REMOVALS, farm)
        self.assertTrue(all(b in fps for b in set(adds) | set(removes)))

    @unittest.skipUnless(SHIPPED.exists() and SCRATCH.exists() and Path(uofiles.CLIENT).exists(), "needs the scratch build and the pristine client data")
    def test_5_the_shipped_patch_rebuilds_the_scratch_build_exactly(self):
        tmp = tempfile.mkdtemp(prefix="p188-mapops-real-")
        try:
            drifted, missing, land_equal, bad = mapops.check(without_farm(SHIPPED.read_text()), uofiles.CLIENT, str(SCRATCH), FACET, scratch=tmp)
            self.assertEqual(([], [], True, []), (drifted, missing, land_equal, bad))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
