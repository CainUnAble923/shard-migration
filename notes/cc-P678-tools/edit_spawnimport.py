r"""cc-P678: SpawnerImportVerification after the ML plaza's vendors are refused (ClusterFHavenTownSpawns) and the
services seeder (with its stand-in Healer) is retired. Fact 4 now counts what the hook admits; fact 5 goes.
    python -P edit_spawnimport.py
"""
import re

P = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Misc/SpawnerImportVerification.cs"
s = open(P, encoding="utf-8").read()

old_head = """//   4. Pinned's post-uoml/trammel/Vendors.json, imported for real, keeps every one of its spawners, the
//      eight New Haven vendors P17 found missing among them, and a second import changes nothing.
//   5. With pinned's Healer spawner back, the New Haven services seeder retires its own stand-in (P17's,
//      at 3462,2559,35) and places no second one; its dry run only reports it."""
new_head = """//   4. Pinned's post-uoml/trammel/Vendors.json, imported for real, keeps every one of its spawners the import hook
//      admits, and a second import changes nothing. cc-P678: on SoS the hook refuses the ML plaza's town spawners
//      (ClusterFHavenTownSpawns), which include the eight New Haven vendors P17 found missing, so those eight are now
//      the refused ones; fact 1 still proves stacked spawners survive. (Fact 5, the New Haven services seeder's
//      stand-in Healer, went with that seeder in cc-P678.)"""
assert s.count(old_head) == 1
s = s.replace(old_head, new_head)

old4 = """            foreach (var (x, y, z, spawns) in NewHavenLost)
            {
                var here = first.Where(s => s.X == x && s.Y == y && s.Z == z).ToList();
                _out.WriteLine($"  {x},{y},{z} {spawns}: {string.Join(", ", here.Select(s => s.Entries[0].SpawnedName))}");
                Assert.Contains(here, s => s.Entries.Any(e => e.SpawnedName == spawns));
            }

            Assert.Equal(guids.Count, first.Count);

            Import(dev, VendorsFile);
            var second = SpawnersWith(guids);
            Assert.Equal(guids.Count, second.Count);"""
new4 = """            var refused = guids.Where(ClusterFHavenTownSpawns.Refused.Contains).ToHashSet();
            _out.WriteLine($"  refused by the Haven hook: {refused.Count}");
            Assert.True(refused.Count >= 50, $"{refused.Count} ML plaza spawners refused");
            Assert.DoesNotContain(first, s => refused.Contains(s.Guid));

            foreach (var (x, y, z, spawns) in NewHavenLost)
            {
                // P17's eight: in the file, inside the old plaza, and refused now
                Assert.True(ClusterFHavenTownSpawns.InOldPlaza(new Point3D(x, y, z)), $"{x},{y},{z} {spawns}");
                Assert.DoesNotContain(first, s => s.X == x && s.Y == y && s.Z == z);
            }

            Assert.Equal(guids.Count - refused.Count, first.Count);

            Import(dev, VendorsFile);
            var second = SpawnersWith(guids);
            Assert.Equal(guids.Count - refused.Count, second.Count);"""
assert s.count(old4) == 1
s = s.replace(old4, new4)
s = s.replace("public void PinnedVendorsFileKeepsEverySpawnerWithNewHavensVendors()",
              "public void PinnedVendorsFileKeepsEverySpawnerTheHavenHookAdmits()")

# fact 5: from its banner to the end of the class
i = s.index("    // ---------------------------------------------------------------- 5")
j = s.rindex("}")            # the namespace-less file ends with the class's brace
s = s[:i].rstrip() + "\n}\n"
open(P, "w", encoding="utf-8", newline="").write(s)
print("ok", j)
