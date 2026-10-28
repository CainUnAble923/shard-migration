r"""cc-P678: NewHavenSeederFloorVerification's measured floors, re-measured on SoS. Every ClusterFNewHavenSeeder entry is
read from the code copy; each tile's standing Z by soswalk (pinned's movement rules and GetAverageZ on the SoS files) must
equal the entry's Z, or the script stops. The table in the test is rewritten from them; the legacy-tile fact moves from Jun
(whose WasAt went with the plaza) to Jacob Waltz, the one entry that keeps one.
    python -P edit_floorfact.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import soswalk  # noqa: E402

CODE = "D:/UO/golems/Iron/ShatteredLegacy/server/"
seeder = open(CODE + "customizations/ClusterFNewHavenSeeder.cs", encoding="utf-8").read()
rows = re.findall(r'new(?: SeedEntry)?\("([^"]+)", "[^"]+", typeof\(\w+\), \(\) => new \w+\(\), (\d+), (\d+), Direction\.\w+, (-?\d+)\)', seeder)
assert len(rows) >= 40, len(rows)

w = soswalk.Walk((3480, 2440, 3790, 2770))
bad = []
for name, x, y, z in rows:
    p = (int(x), int(y))
    if w.stand.get(p) != int(z):
        bad.append((name, p, int(z), w.stand.get(p), w.why.get(p)))
for b in bad:
    print("NOT ON ITS FLOOR", b)

test = CODE + "tests/Misc/NewHavenSeederFloorVerification.cs"
s = open(test, encoding="utf-8").read()
i = s.index('        ["Sir Helper"]') if '["Sir Helper"]' in s else s.index('        ["Andric"]')
j = s.index("    };", i)
table = "".join('        ["%s"] = new(%s, %s, %s),\n' % r for r in rows)
s = s[:i] + table + s[j:]

old_hdr = """// The test host has no map files, so no fact here can ask the map where the floor is. The floors
// below were measured offline by a port of pinned Map.CanFit (Map.cs:925-1010, height 16) over the
// client map, statics and pinned's New Haven decoration, and every one fits."""
new_hdr = """// The test host has no map files, so no fact here can ask the map where the floor is. The floors
// below were measured offline: cc-P678 re-measured every one on the Siege of Sosaria files with the playbook's walk
// (pinned's movement rules and GetAverageZ, shard-migration notes/cc-P678-tools/soswalk.py; edit_floorfact.py writes
// this table and stops if a tile is not its floor). Before, a port of pinned Map.CanFit over the old client map."""
assert s.count(old_hdr) == 1
s = s.replace(old_hdr, new_hdr)

s = s.replace("""        // The Anatomy quest giver, by name.
        Assert.Equal(new Point3D(3458, 2551, 35), entries.Single(e => e.Type == typeof(AndreasVesalius)).GetLocation());""",
              """        // The Anatomy quest giver, by name (cc-P678: in the Healers of Haven).
        Assert.Equal(MeasuredFloor["Andreas Vesalius"], entries.Single(e => e.Type == typeof(AndreasVesalius)).GetLocation());""")

old2 = """        var entry = ClusterFNewHavenSeeder.Entries.Single(e => e.Type == typeof(Jun));
        Assert.True(entry.HasLegacyLocation);

        var jun = new Jun();
        try
        {
            // As the seeder placed him before PT-05: inside a lantern at 3426,2520,21.
            Place(jun, new Point3D(3426, 2520, 21));"""
new2 = """        // cc-P678: Jun's legacy tile went with the ML plaza (a fresh world on swap day); Jacob Waltz at the mine camp keeps
        // his (the tile before PT-05, 3511,2744,0).
        var entry = ClusterFNewHavenSeeder.Entries.Single(e => e.Type == typeof(JacobWaltz));
        Assert.True(entry.HasLegacyLocation);

        var jun = new JacobWaltz();
        try
        {
            // As the seeder placed him before PT-05.
            Place(jun, new Point3D(3511, 2744, 0));"""
assert s.count(old2) == 1, "fact 2"
s = s.replace(old2, new2)
s = s.replace("""            Place(jun, new Point3D(3430, 2530, 21));""", """            Place(jun, new Point3D(3515, 2750, 0));""")
open(test, "w", encoding="utf-8", newline="").write(s)
print("%d entries, %d not on their floor" % (len(rows), len(bad)))
sys.exit(1 if bad else 0)
