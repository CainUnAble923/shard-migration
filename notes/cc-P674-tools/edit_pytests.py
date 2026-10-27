"""cc-P674: the Python facts for the SoS base (tools/tests/test_mapops.py in the docs copy)."""
p = 'D:/UO/golems/Iron/shard-migration/tools/tests/test_mapops.py'
t = open(p, encoding='utf-8').read()

DOC = """     (the landing: P663's seeder fits the gate at the land's height). Facts 4 and 5 allow the isle and leave it out.
"""
DOC_NEW = DOC + """  8. cc-P674 (SoS swap S1): pack writes a whole map MUL as the facet's UOP the way the client reads it (every block
     back, entries found by their names, tables chained), and rename gives another facet the same land under its own
     names (only the 8-byte name hashes differ), refusing a file that is not the first facet's map.
  9. cc-P674: the PowerShell applier on a shipped base (-BaseDir, base-<name> files) patches the base, not the player's
     own files, writes Felucca's copy (-AlsoAs 0) and its three override lines, all the same bytes as the Python apply
     and rename; its stamp names the base, so a changed base rebuilds and an unchanged one skips.
 10. cc-P674: vendor/sos-trammel-map/manifest.csv is the author's download (sizes and SHA-256 of D:\\UO\\third-party's
     files), and packing his Map1.mul gives exactly the manifest's shipped UOP (the pack is deterministic).
"""

STAMP = '        self.assertTrue(stamp.startswith(b"uo-map 1\\n"))'
STAMP_NEW = '        self.assertTrue(stamp.startswith(b"uo-map 2\\n"))   # cc-P674: 2 names the base files by path'

TAIL = '\n\nif __name__ == "__main__":'
TAIL_NEW = r'''

# cc-P674: the Siege of Sosaria map, shipped as the base the launcher patches.
SOS_VENDOR = SHARD / "player-package" / "vendor" / "sos-trammel-map"
SOS_THIRD = Path(r"D:\UO\third-party\sos-trammel-map")


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


if __name__ == "__main__":'''

for o, n in [(DOC, DOC_NEW), (STAMP, STAMP_NEW), (TAIL, TAIL_NEW)]:
    assert t.count(o) == 1, o[:50]
    t = t.replace(o, n)
open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
