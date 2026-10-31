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
     and every line lies inside the Burrows rectangle (x 5136-5247, y 1128-1263) or the Wakening Isle, or is one of
     cc-P687's seam boulders (S14: an S+ of OSI's boulders 0x1357-0x135C on the surface, x < 5120; checked on the SoS
     land by tools/tests/test_sos_fences.py fact 4); it adds and changes, and removes nothing of the map's (cc-P675).
  5. cc-P675 (SoS swap S2): the patch is made on the Siege of Sosaria map. On a pristine copy of it (the package's
     vendor/sos-trammel-map/files, at notes/cc-P675-tools/sos-base/ORIGINAL-SHA256.txt) it applies with no block
     drifted and no removal missing, and diffing that copy against the result gives the shipped patch line for line.
  6. cc-P675: the way in from Old Haven is gone from the patch (S7's hatch is a server item in the author's Second
     Bank of Haven): no line and no fingerprint in its two blocks (x 3608-3623, y 2616-2623), none of P413's burrow
     or P188's hole, and none of cc-P276's farm removals (the farm is on the isle; the spot is the author's forest).
  7. cc-P662: the Wakening Isle (site A, x 6594-6865, y 3905-4049; P673 1.4). Every cell of its drawn area is an L
     line, their tiles and heights are notes/cc-P662-tools/land-summary.csv, its S+ lines are exactly that build's
     statics-placed.csv, it removes nothing of EA's, and the moongate's tile (6832, 3991) is land with nothing on it
     (the landing: P663's seeder fits the gate at the land's height). Fact 4 allows the isle.
  8. cc-P674 (SoS swap S1): pack writes a whole map MUL as the facet's UOP the way the client reads it (every block
     back, entries found by their names, tables chained), and rename gives another facet the same land under its own
     names (only the 8-byte name hashes differ), refusing a file that is not the first facet's map.
  9. cc-P674: the PowerShell applier on a shipped base (-BaseDir, base-<name> files) patches the base, not the player's
     own files, writes Felucca's copy (-AlsoAs 0) and its three override lines, all the same bytes as the Python apply
     and rename; its stamp names the base, so a changed base rebuilds and an unchanged one skips.
 12. cc-P691: Blackthorn's dungeon, copied from stock Trammel into site A in two pieces (notes/cc-P691-tools/
     build_fold.py): fact 4 allows its two boxes (EA's hues kept there); every L and S+ line in them is stock Trammel's
     own cell or static at the line's spot less its piece's offset, and every stock cell and static of the two pieces
     is there (needs D:/UO/UltimaOnlineVanilla, or MAPBUILD_STOCK).
 10. cc-P674: vendor/sos-trammel-map/manifest.csv is the author's download (sizes and SHA-256 of the files in
     D:/UO/third-party/sos-trammel-map), and packing his Map1.mul gives exactly the manifest's shipped UOP (the pack is deterministic).
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
FACET = 1
# cc-P674: the Siege of Sosaria map, shipped as the base the launcher patches.
SOS_VENDOR = SHARD / "player-package" / "vendor" / "sos-trammel-map"
SOS_THIRD = Path(r"D:\UO\third-party\sos-trammel-map")
SOS_HASHES = DOCS / "notes" / "cc-P675-tools" / "sos-base" / "ORIGINAL-SHA256.txt"

BURROWS = (5136, 1128, 5247, 1263)
# cc-P675: the way in's and the old farm's blocks, whole; the patch has no line in either since the SoS re-base.
WAY_IN_BLOCKS = (3608, 2616, 3623, 2623)
FARM_BLOCKS = (3384, 2600, 3399, 2623)
# cc-P662: the Wakening Isle's drawn area with its sea (P481 11.2 shifted to site A, P673 1.4).
ISLE = (6594, 3905, 6865, 4049)
# cc-P691: Blackthorn's two pieces on the Fold: (box, offset from stock Trammel, the stock source box).
BLACKTHORN = {
    "dungeon": ((6217, 3805, 6511, 4051), (40, 1248), (6177, 2557, 6471, 2803)),
    "invasion": ((6904, 3795, 7146, 4067), (656, 1480), (6248, 2315, 6490, 2587)),
}
STOCK = Path(os.environ.get("MAPBUILD_STOCK", r"D:/UO/UltimaOnlineVanilla"))
SEAM_BOULDERS = range(0x1357, 0x135D)   # cc-P687: S14's seam dressing (notes/cc-P687-tools/dress.py)
ISLE_TOOLS = DOCS / "notes" / "cc-P662-tools"
# cc-P276: the two trees inside the tutorial farm's fence, trunk and foliage (design/tutorial-farm/west_v3_layout.json).
FARM_REMOVALS = ["S- 3388 2607 19 3302 0", "S- 3388 2607 19 3303 0", "S- 3396 2616 38 3296 0", "S- 3396 2616 38 3297 0"]


# cc-P413: the burrow that replaced P188's hole (notes/cc-P413-tools/build_anthill.py writes the csv).
BURROW_CSV = DOCS / "notes" / "cc-P413-tools" / "statics-placed.csv"
P188_HOLE = "S+ 3619 2620 0 7025 0"


def burrow_lines():
    import csv
    with open(BURROW_CSV, newline="") as f:
        return ["S+ %s %s %s %d 0" % (r["x"], r["y"], r["z"], int(r["id"], 16)) for r in csv.DictReader(f)]


def inside(x, y, r):
    return r[0] <= x <= r[2] and r[1] <= y <= r[3]


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
        self.assertTrue(stamp.startswith(b"uo-map 2\n"))   # cc-P674: 2 names the base files by path
        before = os.path.getmtime(os.path.join(ps, "statics1.mul"))
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script], capture_output=True, text=True, timeout=600)
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        self.assertNotIn("patched copies", r.stdout)
        self.assertEqual(before, os.path.getmtime(os.path.join(ps, "statics1.mul")))


class Shipped(unittest.TestCase):
    @unittest.skipUnless(SHIPPED.exists(), "needs the shard repo")
    def test_4_the_shipped_patch_is_the_burrows_and_the_isle_only(self):
        text = SHIPPED.read_text()
        facet, fps, land, adds, removes = mapops.parse(text)
        self.assertEqual(1, facet)
        self.assertEqual(int([l for l in text.splitlines() if l.startswith("F ")][0].split()[2]), len(fps))
        self.assertGreater(len(land), 11000)
        bt = [box for box, _, _ in BLACKTHORN.values()]
        for x, y, t, z in land:
            self.assertTrue(inside(x, y, BURROWS) or inside(x, y, ISLE) or any(inside(x, y, b) for b in bt), (x, y))
        for b, rows in adds.items():
            bx, by = divmod(b, 512)
            for tid, cx, cy, z, hue in rows:
                x, y = bx * 8 + cx, by * 8 + cy
                seam = x < 5120 and tid in SEAM_BOULDERS
                blackthorn = any(inside(x, y, b) for b in bt)
                self.assertTrue(inside(x, y, BURROWS) or inside(x, y, ISLE) or seam or blackthorn, (x, y, hex(tid)))
                if not blackthorn:
                    self.assertEqual(0, hue)
        self.assertEqual(0, sum(len(r) for r in removes.values()))
        self.assertTrue(all(b in fps for b in set(adds)))

    @unittest.skipUnless(SHIPPED.exists() and (STOCK / "statics1.mul").exists(), "needs the shard repo and stock Trammel")
    def test_12_blackthorn_is_stock_trammels_copied_by_its_offsets(self):
        import collections
        from mapbuild import uofiles
        facet, fps, land, adds, removes = mapops.parse(SHIPPED.read_text())
        ids, zs = uofiles.load_land(str(STOCK), 1)
        for name, (box, (dx, dy), src) in BLACKTHORN.items():
            lines = [(x, y, t, z) for x, y, t, z in land if inside(x, y, box)]
            self.assertGreater(len(lines), 20000, name)
            for x, y, t, z in lines:
                self.assertEqual((int(ids[x - dx, y - dy]), int(zs[x - dx, y - dy])), (t, z), (name, x, y))
            have = collections.Counter()
            for b, rows in adds.items():
                bx, by = divmod(b, 512)
                for tid, cx, cy, z, hue in rows:
                    x, y = bx * 8 + cx, by * 8 + cy
                    if inside(x, y, box):
                        have[(x - dx, y - dy, z, tid, hue)] += 1
            # the stock statics of the piece: every one in the source box (the dungeon's box excludes the invasion block)
            idx, sta = uofiles.load_statics_index(str(STOCK), 1)
            want = collections.Counter()
            other = BLACKTHORN["invasion"][2]
            for bx in range(src[0] >> 3, (src[2] >> 3) + 1):
                for by in range(src[1] >> 3, (src[3] >> 3) + 1):
                    for tid, cx, cy, z, hue in uofiles.block_statics(idx, sta, bx * 512 + by):
                        x, y = bx * 8 + cx, by * 8 + cy
                        if inside(x, y, src) and (name == "invasion" or not inside(x, y, other)):
                            want[(x, y, z, tid, hue)] += 1
            self.assertEqual(want, have, name)

    @unittest.skipUnless(SHIPPED.exists() and (SOS_VENDOR / "files" / "base-map1legacymul.uop").exists(),
                         "needs the shard repo and its SoS map files (vendor/sos-trammel-map/Add-SosMap.ps1)")
    def test_5_the_shipped_patch_is_made_on_the_sos_map(self):
        import hashlib
        tmp = tempfile.mkdtemp(prefix="p675-sos-")
        try:
            sos = os.path.join(tmp, "sos")
            os.makedirs(sos)
            want = dict(reversed(l.strip().split(" *")) for l in open(SOS_HASHES) if l.strip())
            for name in ("map1LegacyMUL.uop", "statics1.mul", "staidx1.mul"):
                dst = os.path.join(sos, name)
                shutil.copyfile(SOS_VENDOR / "files" / ("base-" + name.lower()), dst)
                self.assertEqual(want[name], hashlib.sha256(read(sos, name)).hexdigest(), name)
            text = SHIPPED.read_text()
            drifted, missing = mapops.apply(text, sos, os.path.join(tmp, "out"), FACET)
            self.assertEqual(([], []), (drifted, missing))
            self.assertEqual(text, mapops.diff(sos, os.path.join(tmp, "out"), FACET))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    @unittest.skipUnless(SHIPPED.exists(), "needs the shard repo")
    def test_6_the_way_in_from_old_haven_is_gone(self):
        text = SHIPPED.read_text()
        facet, fps, land, adds, removes = mapops.parse(text)
        for box in (WAY_IN_BLOCKS, FARM_BLOCKS):
            blocks = {(x >> 3) * 512 + (y >> 3) for x in range(box[0], box[2] + 1, 8) for y in range(box[1], box[3] + 1, 8)}
            self.assertEqual(set(), blocks & set(fps), box)
            self.assertEqual([], [l for l in text.splitlines() if l.split() and l.split()[0] in ("L", "S+", "S-")
                                  and inside(int(l.split()[1]), int(l.split()[2]), box)], box)
        lines = set(text.splitlines())
        self.assertNotIn(P188_HOLE, lines)
        self.assertEqual(set(), set(burrow_lines()) & lines)
        self.assertEqual(set(), set(FARM_REMOVALS) & lines)

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

    def test_11_the_isle_has_osis_surf_and_tropical_plants(self):
        """cc-P725 (Chase 10-28: "island needs shore tiles"; "dress it as a tropical island"): the coast is drawn with
        OSI's surf pieces, never P662's plain water diamond on a walkable sand tile, every sea tile with the island
        north or west of it (the coasts the camera looks across) carries a surf-edged piece, and the island is planted
        with stock tropical trees and plants."""
        lines = SHIPPED.read_text().splitlines()
        isle = [l.split() for l in lines if l.split() and l.split()[0] in ("L", "S+")
                and inside(int(l.split()[1]), int(l.split()[2]), ISLE)]
        land = {(int(f[1]), int(f[2])): int(f[3]) for f in isle if f[0] == "L"}
        pieces = {}
        for f in isle:
            if f[0] == "S+":
                pieces.setdefault((int(f[1]), int(f[2])), []).append(int(f[4]))
        sea = {c for c, t in land.items() if t in (0x00A8, 0x00A9, 0x00AA, 0x00AB)}
        plain = set(range(0x1797, 0x179D))
        surf = set(range(0x179D, 0x17B3))
        sand = set(range(0x0016, 0x001A)) | set(range(0x0033, 0x003B))
        self.assertEqual([], sorted(c for c, ids in pieces.items() if plain & set(ids) and land.get(c) in sand),
                         "a plain water diamond on walkable sand (the sawtooth)")
        self.assertGreater(sum(1 for ids in pieces.values() for t in ids if t in surf), 500, "OSI's surf pieces")
        back = [c for c in sea if (c[0], c[1] - 1) in land and (c[0], c[1] - 1) not in sea
                and (c[0] + 1, c[1]) in sea and (c[0], c[1] + 1) in sea]
        self.assertGreater(len(back), 50)
        self.assertEqual([], sorted(c for c in back if not surf & set(pieces.get(c, []))), "north coast without surf")
        tropical = {0x0C95, 0x0C96, 0x0C99, 0x0C9A, 0x0C9B, 0x0C9C, 0x0C9D, 0x0C9E, 0x0CA8, 0x0CAA, 0x0CAB}
        jungle = set(range(0x0D41, 0x0D94))
        self.assertGreater(sum(1 for ids in pieces.values() for t in ids if t in tropical), 100, "palms, banana, o'hii")
        self.assertGreater(sum(1 for ids in pieces.values() for t in ids if t in jungle), 40, "OSI's jungle trees")



def blocks(n, seed):
    """n distinct 196-byte map blocks (a 4-byte header, then 64 cells), different for each seed."""
    import struct
    out = bytearray()
    for b in range(n):
        out += struct.pack("<I", 0) + b"".join(struct.pack("<Hb", (b * 7 + c + seed) % 0x4000, (b + c) % 100 - 50) for c in range(64))
    return bytes(out)


def same_blocks(m, land):
    return [b for b in mapops.blocks_present(m) if m.data[m.block_offset(b):m.block_offset(b) + 196] != land[b * 196:b * 196 + 196]]


class SosBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="p674-sos-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_8_pack_writes_the_whole_map_as_the_client_reads_it_and_rename_gives_felucca_the_same_land(self):
        land = blocks(3 * 4096 - 5, 1)          # three chunks, the last one short
        mul = os.path.join(self.tmp, "Map1.mul")
        with open(mul, "wb") as f:
            f.write(land)
        d = os.path.join(self.tmp, "d")
        os.makedirs(d)
        self.assertEqual(3, mapops.write_map_uop(os.path.join(d, "map1LegacyMUL.uop"), 1, land, table_size=2))
        ver, entries, data = uofiles.read_uop(os.path.join(d, "map1LegacyMUL.uop"))
        names = [uofiles.hashlittle2("build/map1legacymul/%08d.dat" % c) for c in range(3)]
        self.assertEqual(names, [e["hash"] for e in entries])
        first = int.from_bytes(data[12:20], "little")
        self.assertEqual(2, int.from_bytes(data[first:first + 4], "little"), "two tables, chained: 2 entries, then 1")
        m = uofiles.MapFile(d, 1)
        self.assertEqual(3 * 4096 - 5, len(mapops.blocks_present(m)))
        self.assertEqual([], same_blocks(m, land))
        self.assertEqual(3, mapops.pack(mul, os.path.join(self.tmp, "p.uop"), 1))
        self.assertEqual(3, mapops.rename_uop(os.path.join(d, "map1LegacyMUL.uop"), os.path.join(d, "map0LegacyMUL.uop"), 1, 0))
        self.assertEqual([], same_blocks(uofiles.MapFile(d, 0), land))
        a, b = read(d, "map1LegacyMUL.uop"), read(d, "map0LegacyMUL.uop")
        self.assertEqual(len(a), len(b))
        differing = sum(1 for i in range(len(a)) if a[i] != b[i])
        self.assertTrue(0 < differing <= 3 * 8, "only the three 8-byte name hashes differ, got %d bytes" % differing)
        with self.assertRaises(ValueError):
            mapops.rename_uop(os.path.join(d, "map0LegacyMUL.uop"), os.path.join(d, "x.uop"), 1, 0)

    @unittest.skipUnless(shutil.which("powershell") and APPLIER.exists(), "needs Windows PowerShell and the shard repo")
    def test_9_the_powershell_applier_patches_a_shipped_base_and_writes_feluccas_copy(self):
        ea = mapops.synthetic_facet(os.path.join(self.tmp, "ea"), FACET, fill=(0x0003, 0))
        base = mapops.synthetic_facet(os.path.join(self.tmp, "sos"), FACET, fill=(0x0010, 5))
        uofiles.write_statics(base, FACET, [(10, 20, 0, 0x0E31), (11, 20, 5, 0x0B26)])
        shipped = os.path.join(self.tmp, "app-map")
        os.makedirs(shipped)
        for n in ("map1LegacyMUL.uop", "statics1.mul", "staidx1.mul"):
            shutil.copyfile(os.path.join(base, n), os.path.join(shipped, "base-" + n.lower()))
        ops_text = "F 1 0\nL 10 20 581 -3\nS- 11 20 5 2854 0\nS+ 13 20 13 2572 0\n"
        ops = os.path.join(self.tmp, "trammel.mapops")
        with open(ops, "w", newline="\n") as f:
            f.write(ops_text)
        py = os.path.join(self.tmp, "py")
        mapops.apply(ops_text, base, py, FACET)
        mapops.rename_uop(os.path.join(py, "map1LegacyMUL.uop"), os.path.join(py, "map0LegacyMUL.uop"), 1, 0)
        ps = os.path.join(self.tmp, "ps")
        script = ("$ErrorActionPreference='Stop'; . '%s'; Build-MapOverride -UoDir '%s' -Ops '%s' -OutDir '%s' -BaseDir '%s' -AlsoAs 0"
                  % (APPLIER, ea, ops, ps, shipped))

        def run():
            return subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script], capture_output=True, text=True, timeout=600)

        r = run()
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        lines = [l for l in r.stdout.splitlines() if "=" in l]
        self.assertEqual(["map1legacymul.uop", "statics1.mul", "staidx1.mul", "map0legacymul.uop", "statics0.mul", "staidx0.mul"],
                         [l.split("=")[0] for l in lines])
        self.assertTrue(lines[4].endswith("statics1.mul") and lines[5].endswith("staidx1.mul"), "Felucca reads Trammel's statics")
        for name in ("map1LegacyMUL.uop", "statics1.mul", "staidx1.mul", "map0LegacyMUL.uop"):
            self.assertEqual(read(py, name), read(ps, name), name)
        self.assertEqual((581, -3), uofiles.MapFile(ps, 0).get(10, 20), "Felucca has our patch on the base's land")
        self.assertEqual((0x0010, 5), uofiles.MapFile(ps, 1).get(11, 21), "the base's land, not the player's")
        before = os.path.getmtime(os.path.join(ps, "map0LegacyMUL.uop"))
        r = run()
        self.assertNotIn("patched copies", r.stdout)
        self.assertEqual(before, os.path.getmtime(os.path.join(ps, "map0LegacyMUL.uop")))
        uofiles.write_land(base, FACET, {(1, 1): (0x0011, 0)})          # a new base ships
        shutil.copyfile(os.path.join(base, "map1LegacyMUL.uop"), os.path.join(shipped, "base-map1legacymul.uop"))
        r = run()
        self.assertIn("patched copies", r.stdout)
        self.assertEqual((0x0011, 0), uofiles.MapFile(ps, 0).get(1, 1))

    @unittest.skipUnless((SOS_VENDOR / "manifest.csv").exists() and SOS_THIRD.exists(), "needs the shard repo and the SoS download")
    def test_10_the_manifest_is_the_authors_download_and_the_pack_is_its_shipped_uop(self):
        import csv, hashlib
        with open(SOS_VENDOR / "manifest.csv", newline="") as f:
            rows = list(csv.DictReader(l for l in f if not l.startswith("#")))

        def sha(p):
            return hashlib.sha256(open(p, "rb").read()).hexdigest().upper()

        src = {r["file"]: r for r in rows if r["kind"] == "source"}
        ship = {r["file"]: r for r in rows if r["kind"] == "ship"}
        self.assertEqual({"base-map1legacymul.uop", "base-statics1.mul", "base-staidx1.mul"}, set(ship))
        for r in src.values():
            p = SOS_THIRD / r["from"]
            self.assertEqual(int(r["bytes"]), p.stat().st_size, r["file"])
            self.assertEqual(r["sha256"], sha(p), r["file"])
        self.assertEqual(src["Statics1.mul"]["sha256"], ship["base-statics1.mul"]["sha256"])
        self.assertEqual(src["Staidx1.mul"]["sha256"], ship["base-staidx1.mul"]["sha256"])
        out = os.path.join(self.tmp, "base-map1legacymul.uop")
        self.assertEqual(112, mapops.pack(str(SOS_THIRD / src["Map1.mul"]["from"]), out, 1))
        self.assertEqual(int(ship["base-map1legacymul.uop"]["bytes"]), os.path.getsize(out))
        self.assertEqual(ship["base-map1legacymul.uop"]["sha256"], sha(out))


if __name__ == "__main__":
    unittest.main()
