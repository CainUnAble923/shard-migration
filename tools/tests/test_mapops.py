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
     cc-P413: the same comparison puts P188's hole back in place of the burrow, which the scratch build never had.
  6. cc-P413: the shipped patch's additions in the Second Bank are exactly notes/cc-P413-tools/statics-placed.csv
     (OSI's 6 x 6 sinkhole at x 3615-3620, y 2616-2621 and its rim), P188's hole 0x1B71 is gone, the set is laid as
     OSI lays it, and its dark core is the mouth (x 3617-3619, y 2617-2620, ClusterFRootdeepSeeder.Mouth).
  7. cc-P662: the Wakening Isle (site A, x 6594-6865, y 3905-4049; P673 1.4). Every cell of its drawn area is an L
     line, their tiles and heights are notes/cc-P662-tools/land-summary.csv, its S+ lines are exactly that build's
     statics-placed.csv, it removes nothing of EA's, and the moongate's tile (6832, 3991) is land with nothing on it
     (the landing: P663's seeder fits the gate at the land's height). Facts 4 and 5 allow the isle and leave it out.
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

# cc-P413: SL_SHARD_REPO points the facts at another work copy of the shard repo (a Golem's own).
SHARD = Path(os.environ.get("SL_SHARD_REPO", r"D:\ShatteredLegacy"))
APPLIER = SHARD / "player-package" / "payload" / "app" / "Apply-MapOps.ps1"
SHIPPED = SHARD / "player-package" / "vendor" / "shattered-legacy-map" / "trammel.mapops"
SCRATCH = Path(r"D:\UO\cc-p167-work\scratch-client")
FACET = 1

BURROWS = (5136, 1128, 5247, 1263)
WAY_IN = (3614, 2608, 3626, 2624)
FARM = (3381, 2603, 3399, 2619)
# cc-P662: the Wakening Isle's drawn area with its sea (P481 11.2 shifted to site A, P673 1.4).
ISLE = (6594, 3905, 6865, 4049)
ISLE_TOOLS = DOCS / "notes" / "cc-P662-tools"
# cc-P276: the two trees inside the tutorial farm's fence, trunk and foliage (design/tutorial-farm/west_v3_layout.json).
FARM_REMOVALS = ["S- 3388 2607 19 3302 0", "S- 3388 2607 19 3303 0", "S- 3396 2616 38 3296 0", "S- 3396 2616 38 3297 0"]


# cc-P413: the burrow that replaced P188's hole (notes/cc-P413-tools/build_anthill.py writes the csv).
BURROW_CSV = DOCS / "notes" / "cc-P413-tools" / "statics-placed.csv"
P188_HOLE = "S+ 3619 2620 0 7025 0"
SINK_FIRST, SINK_LAST = 0x30E7, 0x310A
MOUTH = [(x, y) for y in range(2617, 2621) for x in range(3617, 3620)]


def burrow_lines():
    import csv
    with open(BURROW_CSV, newline="") as f:
        return ["S+ %s %s %s %d 0" % (r["x"], r["y"], r["z"], int(r["id"], 16)) for r in csv.DictReader(f)]


def inside(x, y, r):
    return r[0] <= x <= r[2] and r[1] <= y <= r[3]


def without_farm(text):
    """The patch as P167's scratch build knows it: the farm's removals and their two block fingerprints dropped."""
    farm_blocks = {(int(l.split()[1]) >> 3) * 512 + (int(l.split()[2]) >> 3) for l in FARM_REMOVALS}
    keep = [l for l in text.splitlines() if l not in FARM_REMOVALS and not (l.startswith("B ") and int(l.split()[1]) in farm_blocks)]
    return "\n".join(keep) + "\n"


def as_p188(text):
    """The patch as P188 left the Second Bank: the burrow's lines and the block only they touch dropped, the hole back.
    The F line's block count is left as it is: mapops.check never reads it."""
    burrow = set(burrow_lines())
    hole_block = (3619 >> 3) * 512 + (2620 >> 3)
    burrow_blocks = {(int(l.split()[1]) >> 3) * 512 + (int(l.split()[2]) >> 3) for l in burrow} - {hole_block}
    keep = [l for l in text.splitlines() if l not in burrow and not (l.startswith("B ") and int(l.split()[1]) in burrow_blocks)]
    keep.append(P188_HOLE)
    return "\n".join(keep) + "\n"


def without_isle(text):
    """The patch as P167's scratch build knows it: the isle's lines and the B lines of the blocks only they touch
    dropped (the isle's area is void in that build)."""
    isle_blocks = set()
    other_blocks = set()
    for l in text.splitlines():
        f = l.split()
        if f and f[0] in ("L", "S+", "S-"):
            b = (int(f[1]) >> 3) * 512 + (int(f[2]) >> 3)
            (isle_blocks if inside(int(f[1]), int(f[2]), ISLE) else other_blocks).add(b)
    only = isle_blocks - other_blocks
    keep = [l for l in text.splitlines()
            if not (l.split() and l.split()[0] in ("L", "S+", "S-") and inside(int(l.split()[1]), int(l.split()[2]), ISLE))
            and not (l.startswith("B ") and int(l.split()[1]) in only)]
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
            self.assertTrue(inside(x, y, BURROWS) or inside(x, y, ISLE), (x, y))
        for lines in (adds, removes):
            for b, rows in lines.items():
                bx, by = divmod(b, 512)
                for tid, cx, cy, z, hue in rows:
                    x, y = bx * 8 + cx, by * 8 + cy
                    self.assertTrue(inside(x, y, BURROWS) or inside(x, y, WAY_IN) or inside(x, y, FARM) or inside(x, y, ISLE), (x, y, hex(tid)))
                    self.assertEqual(0, hue)
        self.assertEqual(3 + len(FARM_REMOVALS), sum(len(r) for r in removes.values()))
        farm = [l for l in text.splitlines() if l.startswith(("L ", "S+ ", "S- ")) and inside(int(l.split()[1]), int(l.split()[2]), FARM)]
        self.assertEqual(FARM_REMOVALS, farm)
        self.assertTrue(all(b in fps for b in set(adds) | set(removes)))

    @unittest.skipUnless(SHIPPED.exists() and SCRATCH.exists() and Path(uofiles.CLIENT).exists(), "needs the scratch build and the pristine client data")
    def test_5_the_shipped_patch_rebuilds_the_scratch_build_exactly(self):
        tmp = tempfile.mkdtemp(prefix="p188-mapops-real-")
        try:
            drifted, missing, land_equal, bad = mapops.check(without_isle(as_p188(without_farm(SHIPPED.read_text()))), uofiles.CLIENT, str(SCRATCH), FACET, scratch=tmp)
            self.assertEqual(([], [], True, []), (drifted, missing, land_equal, bad))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    @unittest.skipUnless(SHIPPED.exists(), "needs the shard repo")
    def test_6_the_burrow_replaced_the_hole(self):
        lines = SHIPPED.read_text().splitlines()
        bank = [l for l in lines if l.startswith("S+ ") and inside(int(l.split()[1]), int(l.split()[2]), WAY_IN)]
        self.assertFalse(P188_HOLE in lines, "P188's hole 0x1B71 at 3619,2620 is still in the patch")
        self.assertEqual(sorted(burrow_lines()), sorted(bank))
        sink = {(int(l.split()[1]), int(l.split()[2])): int(l.split()[4]) for l in bank if SINK_FIRST <= int(l.split()[4]) <= SINK_LAST}
        self.assertEqual(36, len(sink))
        # OSI's layout (Trammel 5575,3015): id = 0x310A - column - 6 * row; the dark core is columns 2-4, rows 1-4.
        ox, oy = min(x for x, y in sink), min(y for x, y in sink)
        for (x, y), tid in sink.items():
            self.assertEqual(SINK_LAST - (x - ox) - 6 * (y - oy), tid, (x, y))
        self.assertEqual(sorted(MOUTH), sorted((ox + c, oy + r) for r in range(1, 5) for c in range(2, 5)))

    @unittest.skipUnless(SHIPPED.exists(), "needs the shard repo")
    def test_7_the_isle_is_the_build_and_nothing_else(self):
        import collections, csv
        lines = SHIPPED.read_text().splitlines()
        isle = [l.split() for l in lines if l.split() and l.split()[0] in ("L", "S+", "S-")
                and inside(int(l.split()[1]), int(l.split()[2]), ISLE)]
        land = [f for f in isle if f[0] == "L"]
        self.assertEqual((ISLE[2] - ISLE[0] + 1) * (ISLE[3] - ISLE[1] + 1), len(land), "every cell of the drawn area")
        self.assertEqual(len(land), len({(f[1], f[2]) for f in land}))
        with open(ISLE_TOOLS / "land-summary.csv", newline="") as f:
            want = {(int(r["land_id_hex"], 16), int(r["z"])): int(r["tiles"]) for r in csv.DictReader(f)}
        self.assertEqual(want, dict(collections.Counter((int(f[3]), int(f[4])) for f in land)))
        with open(ISLE_TOOLS / "statics-placed.csv", newline="") as f:
            placed = sorted("S+ %s %s %s %d 0" % (r["x"], r["y"], r["z"], int(r["id_hex"], 16)) for r in csv.DictReader(f))
        self.assertEqual(placed, sorted(" ".join(f) for f in isle if f[0] == "S+"))
        self.assertEqual([], [f for f in isle if f[0] == "S-"])
        gate = [f for f in land if (f[1], f[2]) == ("6832", "3991")]
        self.assertNotIn(int(gate[0][3]), (0x00A8, 0x00A9, 0x00AA, 0x00AB), "the moongate stands on land")
        self.assertEqual([], [f for f in isle if f[0] == "S+" and (f[1], f[2]) == ("6832", "3991")])


if __name__ == "__main__":
    unittest.main()
