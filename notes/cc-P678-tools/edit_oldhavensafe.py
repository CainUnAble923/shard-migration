r"""cc-P678: OldHavenNewPlayerSafeVerification for Old Haven Training in the north woods (x 3590-3710, y 2378-2459) and
Drelgor at the moved undead field (3640,2418,34).
    python -P edit_oldhavensafe.py
"""
import re

P = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Regions/OldHavenNewPlayerSafeVerification.cs"
s = open(P, encoding="utf-8").read()

REPS = [
    ("""//   S1. The seeder places ServUO's Drelgor at 3651,2509 and no OldHavenMage or Vorlak spawner.""",
     """//   S1. The seeder places ServUO's Drelgor at 3640,2418 and no OldHavenMage or Vorlak spawner.
//
// cc-P678: on the Siege of Sosaria map Old Haven is the author's Haven town, New Haven now, so Old Haven's undead field,
// Drelgor and "Old Haven Training" moved to the north woods between the town and the shore (x 3590-3710, y 2378-2459;
// ClusterFHavenTownSpawns.TrainingField). The facts below are the same facts on the new ground."""),
    ("""//   A1. "Old Haven Training" is registered at start, as ServUO draws it plus the walk to the Rootdeep hole, and not over
//       New Haven.
//   A2. Drelgor's broadcast test holds for him at his spawn and a player at the hole (Drelgor.cs BroadcastMessage).""",
     """//   A1. "Old Haven Training" is registered at start over the north woods, and not over New Haven.
//   A2. Drelgor's broadcast test holds for him at his spawn and a player at the woods' east edge (Drelgor.cs
//       BroadcastMessage)."""),
    ("""    private static readonly Point3D DrelgorHome = new(3651, 2509, 0);
    private static readonly Point3D Hole = new(3619, 2620, 0);
    private static readonly Point3D NewHavenBank = new(3485, 2572, 0);
    // P371: outside Old Haven Training, while remaining on the tutorial island before graduation.
    private static readonly Point3D FarAway = new(3503, 2574, 14);""",
     """    private static readonly Point3D DrelgorHome = new(3640, 2418, 34);
    // inside Old Haven Training: the north woods' east side
    private static readonly Point3D WoodsEdge = new(3700, 2440, 0);
    // P371: outside Old Haven Training, while remaining on the tutorial island before graduation (cc-P678: the start).
    private static readonly Point3D FarAway = new(3634, 2586, 0);"""),
    ("""s.X is >= 3520 and <= 3680 && s.Y is >= 2420 and <= 2600)""",
     """s.X is >= 3590 and <= 3710 && s.Y is >= 2378 and <= 2459)"""),
    ("""            Assert.Equal(["Drelgor at 3651,2509"], names);""",
     """            Assert.Equal(["Drelgor at 3640,2418"], names);"""),
    ("""            Mages = Place(new Point3D(3600, 2510, 0), "OldHavenMage");
            OldVorlak = Place(new Point3D(3622, 2488, 0), "DrelgorTheImpaler"); // placed before cc-P129's rename
            Drelgor = Place(DrelgorHome, "Drelgor");
            Skeletons = Place(new Point3D(3650, 2509, 0), "Skeleton");          // pinned's Outdoors.json spawner's spot
            Mixed = Place(new Point3D(3618, 2540, 0), "OldHavenMage", "Skeleton");""",
     """            Mages = Place(new Point3D(3600, 2400, 0), "OldHavenMage");
            OldVorlak = Place(new Point3D(3622, 2420, 0), "DrelgorTheImpaler"); // placed before cc-P129's rename
            Drelgor = Place(DrelgorHome, "Drelgor");
            Skeletons = Place(new Point3D(3660, 2430, 0), "Skeleton");          // an undead spawner in the woods
            Mixed = Place(new Point3D(3618, 2440, 0), "OldHavenMage", "Skeleton");"""),
    ("""            Stray.MoveToWorld(new Point3D(3590, 2470, 0), Map.Trammel);""",
     """            Stray.MoveToWorld(new Point3D(3595, 2410, 0), Map.Trammel);"""),
    ("""        Assert.Single(real, l => l.StartsWith("[MIXED, KEPT] Spawner at (3618,2540,", StringComparison.Ordinal));""",
     """        Assert.Single(real, l => l.StartsWith("[MIXED, KEPT] Spawner at (3618,2440,", StringComparison.Ordinal));"""),
    ("""    public void A1_OldHavenTrainingCoversServUOsRectangleAndTheWalkToTheHole()
    {
        Region At(int x, int y) => Region.Find(new Point3D(x, y, 0), Map.Trammel);

        foreach (var (x, y) in new[] { (3589, 2443), (3703, 2542), (3651, 2509), (3619, 2620), (3546, 2600), (3703, 2650) })""",
     """    public void A1_OldHavenTrainingCoversTheNorthWoods()
    {
        Region At(int x, int y) => Region.Find(new Point3D(x, y, 0), Map.Trammel);

        foreach (var (x, y) in new[] { (3590, 2378), (3710, 2378), (3590, 2459), (3710, 2459), (3640, 2418), (3700, 2440) })"""),
    ("""        foreach (var (x, y) in new[] { (3588, 2443), (3704, 2500), (3545, 2600), (3600, 2651), (3485, 2572), (3589, 2442) })""",
     """        // outside: one past each edge, the town's start, the bank (and the cellar hatch beside it), the old ruin's field
        foreach (var (x, y) in new[] { (3589, 2418), (3711, 2418), (3640, 2377), (3640, 2460), (3634, 2586), (3618, 2620), (3651, 2509) })"""),
    ("""    public void A2_DrelgorsBroadcastTestHoldsBetweenHisHomeAndTheHole()""",
     """    public void A2_DrelgorsBroadcastTestHoldsBetweenHisHomeAndTheWoodsEdge()"""),
]
for a, b in REPS:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
s = re.sub(r"\bHole\b", "WoodsEdge", s)
open(P, "w", encoding="utf-8", newline="").write(s)
print("ok", s.count("WoodsEdge"))
