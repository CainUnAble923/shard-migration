r"""cc-P678: RootdeepWayInVerification for the cellar hatch in the Second Bank of Haven (SoS). W1 and W2 are rewritten for
the one-tile mouth, the hatch item and New Haven's regions; W3-W5 (the Old Haven crier and skeleton spawners) move to
HavenTownSpawnsVerification, whose facts they now are; W6 (a world P188 seeded) goes: the test shard starts a fresh world
on swap day (Chase 2026-10-27).
    python -P edit_wayin.py
"""
P = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Regions/RootdeepWayInVerification.cs"
s = open(P, encoding="utf-8").read()

# the header's fact list
i = s.index("// Facts:\n")
j = s.index("// server/tests/<path> is mirrored")
s = s[:i] + """// Facts:
//   W1. cc-P678 (was P188's two ends, then P413's twelve-tile mouth): on the Siege of Sosaria map the way down is a
//       cellar hatch in the Second Bank of Haven's main hall (3618,2620, the region's Entrance): the seeder places the
//       hatch item (0x3E65, one below the floor so its top is within a step) and one teleporter down on its tile,
//       landing on the Landing's arrival (5193,1138), and one at the foot of the ladder (5193,1132) that lands three
//       tiles from the hatch in the same hall (3621,2620); a player on the hatch goes down, the ladder brings them up
//       beside it; a creature is not moved; the hatch and the landing are in New Haven, the ladder's foot in the Burrows;
//       a re-run places nothing again.
//   W2. The region rectangles match the built floors: the Vault's region is exactly the Vault's floor extent of the
//       approved layout (x 5142-5178, y 1132-1159), and the Burrows' region holds every zone's floor with the wall
//       ring and the ladder's wall tile inside it (the layout's extents, notes/art/rootdeep-mockup/layout.json, as
//       build_burrows.py prints them: land x 5140-5245, y 1131-1261), and the hatch is outside both and inside the
//       Second Bank of Haven, in New Haven.
// (W3-W5, the Old Haven crier and skeleton spawners, are HavenTownSpawnsVerification's since cc-P678; W6, a world
// P188's seeder seeded, went with the fresh test world of swap day.)
//
""" + s[j:]

# the constructor registers New Haven's regions
a = """        RootdeepVaultRegion.Initialize();
        ApprenticeTrainingRegion.Initialize();"""
assert s.count(a) == 1
s = s.replace(a, a + "\n        HavenTownRegions.Initialize();")

# Seeded() also collects the hatch
a = """        foreach (var row in ClusterFRootdeepSeeder.FloorTraps) // cc-P275: the seeder lays these too"""
assert s.count(a) == 1
s = s.replace(a, """        if (ClusterFRootdeepSeeder.FindHatch(Map.Trammel) is { } hatch) // cc-P678
        {
            placed.Add(hatch);
        }

""" + a)

# W1
i = s.index("    // The mouth by hand, row by row")
j = s.index("    // ---------------------------------------------------------------- W2")
w1 = s[i:j]
w1 = w1.replace("""    // The mouth by hand, row by row (the map patch's dark core: notes/cc-P413-tools/statics-placed.csv).
    private static readonly (int X, int Y)[] Mouth =
    [
        (3617, 2617), (3618, 2617), (3619, 2617),
        (3617, 2618), (3618, 2618), (3619, 2618),
        (3617, 2619), (3618, 2619), (3619, 2619),
        (3617, 2620), (3618, 2620), (3619, 2620),
    ];

    private static readonly Point3D BesideMound = new(3619, 2623, 0);
""", """    // The mouth by hand: cc-P678's hatch, one tile (notes/cc-P678-tools/crosscheck.py found it clear of every layout).
    private static readonly (int X, int Y)[] Mouth = [(3618, 2620)];

    private static readonly Point3D BesideHatch = new(3621, 2620, 0);
""")
w1 = w1.replace("W1_EveryMouthTileTakesAPlayerDownAndTheLadderLandsBesideTheMound", "W1_TheHatchTakesAPlayerDownAndTheLadderLandsBesideIt")
w1 = w1.replace("BesideMound", "BesideHatch")
a = """            Assert.Equal(rows.Length, first.Teleporters);
            Assert.Equal(0, first.TeleportersRetargeted);"""
assert w1.count(a) == 1
w1 = w1.replace(a, a + """
            Assert.Equal((1, 0), (first.Hatches, first.HatchesPresent));
            var hatch = ClusterFRootdeepSeeder.FindHatch(Map.Trammel)!;
            Assert.Equal(new Point3D(3618, 2620, -1), hatch.Location);
            Assert.Equal(0x3E65, hatch.ItemID);
            Assert.False(hatch.Movable);
            Assert.Equal(ClusterFRootdeepSeeder.HatchName, hatch.Name);""")
a = """            // The mouth is in Old Haven Training, the ladder's foot in the Burrows, its landing back in Old Haven Training.
            Assert.All(down, r => Assert.Equal(ApprenticeTraining.OldHavenTraining, Region.Find(r.At, Map.Trammel).Name));
            Assert.IsType<OldHavenBurrowsRegion>(Region.Find(ladder.At, Map.Trammel));
            Assert.Equal(ApprenticeTraining.OldHavenTraining, Region.Find(ladder.To, Map.Trammel).Name);"""
assert w1.count(a) == 1
w1 = w1.replace(a, """            // The hatch is in the Second Bank of Haven, in New Haven; the ladder's foot in the Burrows; its landing in the bank.
            Assert.All(down, r => Assert.Equal("the Second Bank of Haven", Region.Find(r.At, Map.Trammel).Name));
            Assert.All(down, r => Assert.True(Region.Find(r.At, Map.Trammel).IsPartOf(HavenTownRegions.TownName)));
            Assert.IsType<OldHavenBurrowsRegion>(Region.Find(ladder.At, Map.Trammel));
            Assert.Equal("the Second Bank of Haven", Region.Find(ladder.To, Map.Trammel).Name);""")
w1 = w1.replace("""            Assert.Equal((0, 0), (again.Teleporters, again.TeleportersRetargeted));""",
                """            Assert.Equal((0, 0), (again.Teleporters, again.TeleportersRetargeted));
            Assert.Equal((0, 1), (again.Hatches, again.HatchesPresent));""")
w1 = w1.replace("// Down from this mouth tile:", "// Down the hatch:").replace("// Up the ladder: beside the mound, on no mouth tile.", "// Up the ladder: beside the hatch, not on it.")
s = s[:i] + w1 + s[j:]

# W2's hole lines
a = """        // the hole: outside the Burrows and the Vault, inside Old Haven Training
        var hole = OldHavenBurrowsRegion.HoleEntrance;
        Assert.False(OldHavenBurrowsRegion.IsInside(Map.Trammel, hole));
        Assert.False(RootdeepVault.IsInside(Map.Trammel, hole));
        Assert.Equal(ApprenticeTraining.OldHavenTraining, Region.Find(hole, Map.Trammel).Name);"""
assert s.count(a) == 1
s = s.replace(a, """        // the hatch: outside the Burrows and the Vault, inside the Second Bank of Haven in New Haven (cc-P678)
        var hole = OldHavenBurrowsRegion.HoleEntrance;
        Assert.Equal(new Point3D(ClusterFRootdeepSeeder.Hole.X, ClusterFRootdeepSeeder.Hole.Y, 0), hole);
        Assert.False(OldHavenBurrowsRegion.IsInside(Map.Trammel, hole));
        Assert.False(RootdeepVault.IsInside(Map.Trammel, hole));
        Assert.Equal("the Second Bank of Haven", Region.Find(hole, Map.Trammel).Name);
        Assert.True(Region.Find(hole, Map.Trammel).IsPartOf(HavenTownRegions.TownName));""")

# drop W3 to the end of the class
i = s.index("    // ---------------------------------------------------------------- W3")
s = s[:i].rstrip() + "\n}\n"
open(P, "w", encoding="utf-8", newline="").write(s)
print("ok")
