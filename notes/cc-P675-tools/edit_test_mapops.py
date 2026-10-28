"""cc-P675: test_mapops.py facts 4-6 follow the patch onto the Siege of Sosaria map (run once, from anywhere)."""
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'tests', 'test_mapops.py')
s = open(P, newline='').read()


def sub(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


sub('''  4. The shipped patch (player-package/vendor/shattered-legacy-map/trammel.mapops) parses, lists its touched blocks,
     and every line lies inside the Burrows rectangle (x 5136-5247, y 1128-1263) or the way in (the Second Bank of
     Haven, 3614-3626 x 2608-2624), but for cc-P276's four removals in the tutorial farm (the two trees inside its
     fence, x 3381-3399, y 2603-2619, and nothing else there); when the pristine client data and P167's scratch build
     are on this PC, the patch without the farm's lines rebuilds the scratch build exactly (the farm was never in it).
     cc-P413: the same comparison puts P188's hole back in place of the burrow, which the scratch build never had.
  6. cc-P413: the shipped patch's additions in the Second Bank are exactly notes/cc-P413-tools/statics-placed.csv
     (OSI's 6 x 6 sinkhole at x 3615-3620, y 2616-2621 and its rim), P188's hole 0x1B71 is gone, the set is laid as
     OSI lays it, and its dark core is the mouth (x 3617-3619, y 2617-2620, ClusterFRootdeepSeeder.Mouth).
''', '''  4. The shipped patch (player-package/vendor/shattered-legacy-map/trammel.mapops) parses, lists its touched blocks,
     and every line lies inside the Burrows rectangle (x 5136-5247, y 1128-1263) or the Wakening Isle; it adds and
     changes, and removes nothing of the map's (cc-P675).
  5. cc-P675 (SoS swap S2): the patch is made on the Siege of Sosaria map. On a pristine copy of it (the package's
     vendor/sos-trammel-map/files, at notes/cc-P675-tools/sos-base/ORIGINAL-SHA256.txt) it applies with no block
     drifted and no removal missing, and diffing that copy against the result gives the shipped patch line for line.
  6. cc-P675: the way in from Old Haven is gone from the patch (S7's hatch is a server item in the author's Second
     Bank of Haven): no line and no fingerprint in its two blocks (x 3608-3623, y 2616-2623), none of P413's burrow
     or P188's hole, and none of cc-P276's farm removals (the farm is on the isle; the spot is the author's forest).
''')

sub('''SCRATCH = Path(r"D:\\UO\\cc-p167-work\\scratch-client")
''', '')
sub('''WAY_IN = (3614, 2608, 3626, 2624)
FARM = (3381, 2603, 3399, 2619)
''', '''# cc-P675: the way in's and the old farm's blocks, whole; the patch has no line in either since the SoS re-base.
WAY_IN_BLOCKS = (3608, 2616, 3623, 2623)
FARM_BLOCKS = (3384, 2600, 3399, 2623)
''')
sub('''SINK_FIRST, SINK_LAST = 0x30E7, 0x310A
MOUTH = [(x, y) for y in range(2617, 2621) for x in range(3617, 3620)]
''', '')

# the helpers that rebuilt P167's stock-Trammel scratch build go with fact 5's old form
a = s.index('def without_farm(text):')
b = s.index('def read(folder, name):')
s = s[:a] + s[b:]

a = s.index('    @unittest.skipUnless(SHIPPED.exists(), "needs the shard repo")\n    def test_4_')
b = s.index('    @unittest.skipUnless(SHIPPED.exists(), "needs the shard repo")\n    def test_7_')
s = s[:a] + '''    @unittest.skipUnless(SHIPPED.exists(), "needs the shard repo")
    def test_4_the_shipped_patch_is_the_burrows_and_the_isle_only(self):
        text = SHIPPED.read_text()
        facet, fps, land, adds, removes = mapops.parse(text)
        self.assertEqual(1, facet)
        self.assertEqual(int([l for l in text.splitlines() if l.startswith("F ")][0].split()[2]), len(fps))
        self.assertGreater(len(land), 11000)
        for x, y, t, z in land:
            self.assertTrue(inside(x, y, BURROWS) or inside(x, y, ISLE), (x, y))
        for b, rows in adds.items():
            bx, by = divmod(b, 512)
            for tid, cx, cy, z, hue in rows:
                x, y = bx * 8 + cx, by * 8 + cy
                self.assertTrue(inside(x, y, BURROWS) or inside(x, y, ISLE), (x, y, hex(tid)))
                self.assertEqual(0, hue)
        self.assertEqual(0, sum(len(r) for r in removes.values()))
        self.assertTrue(all(b in fps for b in set(adds)))

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

''' + s[b:]

sub('''SOS_THIRD = Path(r"D:\\UO\\third-party\\sos-trammel-map")
''', '''SOS_THIRD = Path(r"D:\\UO\\third-party\\sos-trammel-map")
SOS_HASHES = DOCS / "notes" / "cc-P675-tools" / "sos-base" / "ORIGINAL-SHA256.txt"
''')
# SOS_VENDOR and SOS_HASHES are read by facts 4-6 now, so they move up beside SHIPPED
a = s.index('# cc-P674: the Siege of Sosaria map, shipped as the base the launcher patches.\n')
b = s.index('\n\n', a)
block = s[a:b + 1]
s = s[:a] + s[b + 2:]
sub('FACET = 1\n', 'FACET = 1\n' + block)
sub('''Facts 4 and 5 allow the isle and leave it out.''', '''Fact 4 allows the isle.''')
open(P, 'w', newline='').write(s)
print('ok')
