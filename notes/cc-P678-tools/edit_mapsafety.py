r"""cc-P678: RootdeepMapSafetyVerification with the one-tile hatch (no second mouth tile to stand a staff-off teleporter on):
the staff-off case becomes the hatch's own teleporter switched off by staff after the map is back.
    python -P edit_mapsafety.py
"""
import re

P = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Regions/RootdeepMapSafetyVerification.cs"
s = open(P, encoding="utf-8").read()

REPS = [
    ("""//   1. Seeded and saved with the map built, then started without it: the saved way down is shut (a step on the burrow
//      mouth stays in Old Haven), the ladder up still works, and starting again with the map restores it; a teleporter
//      staff switched off themselves stays off.""",
     """//   1. Seeded and saved with the map built, then started without it: the saved way down is shut (a step on the cellar
//      hatch stays in the Second Bank of Haven; cc-P678, was the burrow mouth in Old Haven), the ladder up still works,
//      and starting again with the map restores it; a teleporter staff switched off themselves stays off, through a
//      start without the map and one with it."""),
    ("""//   2. A Young player with a connection who steps into the burrow mouth gets the dungeon warning, and Young protection
//      holds on the approach and not on the Landing (P504 #2).""",
     """//   2. A Young player with a connection who steps onto the cellar hatch gets the dungeon warning, and Young protection
//      holds in the bank and not on the Landing (P504 #2)."""),
    ("""    private static readonly Point3D BesideMound = new(3619, 2623, 0);""",
     """    private static readonly Point3D BesideHatch = new(3621, 2620, 0); // cc-P678: where the ladder lands"""),
    ("""            var hole = ClusterFRootdeepSeeder.Teleporters.First(r => r.To == Arrival && r.X == 3619 && r.Y == 2620);
            var down = Reload(ClusterFRootdeepSeeder.PlaceTeleporter(Map.Trammel, hole));
            var other = ClusterFRootdeepSeeder.Teleporters.First(r => r.To == Arrival && r != hole);
            var staffOff = Reload(ClusterFRootdeepSeeder.PlaceTeleporter(Map.Trammel, other));
            staffOff.Active = false; // staff's own choice
            var up""",
     """            var hole = Assert.Single(ClusterFRootdeepSeeder.Teleporters, r => r.To == Arrival);
            Assert.Equal((3618, 2620), (hole.X, hole.Y));
            var down = Reload(ClusterFRootdeepSeeder.PlaceTeleporter(Map.Trammel, hole));
            var up"""),
    ("""            down.OnMoveOver(walker);
            Assert.Equal(Arrival, walker.Location);
            Assert.False(staffOff.Active, "a teleporter staff switched off stays off");""",
     """            down.OnMoveOver(walker);
            Assert.Equal(Arrival, walker.Location);

            // Staff switch it off themselves: a start without the map, then one with it, leave it off.
            down.Active = false;
            ClusterFRootdeepSeeder.MapBuilt = () => false;
            WorldUp();
            ClusterFRootdeepSeeder.MapBuilt = () => true;
            WorldUp();
            Assert.False(down.Active, "a teleporter staff switched off stays off");"""),
    ("""            var hole = ClusterFRootdeepSeeder.Teleporters.First(r => r.To == Arrival && r.X == 3619 && r.Y == 2620);
            t = ClusterFRootdeepSeeder.PlaceTeleporter(Map.Trammel, hole);""",
     """            var hole = Assert.Single(ClusterFRootdeepSeeder.Teleporters, r => r.To == Arrival);
            t = ClusterFRootdeepSeeder.PlaceTeleporter(Map.Trammel, hole);"""),
    ("""            Assert.True(approach.YoungProtected, "Old Haven's approach protects the Young");""",
     """            Assert.True(approach.YoungProtected, "the bank protects the Young");"""),
    ("""            t.OnMoveOver(pm); // the step into the mouth""",
     """            t.OnMoveOver(pm); // the step onto the hatch"""),
]
for a, b in REPS:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
s = re.sub(r"\bBesideMound\b", "BesideHatch", s)
open(P, "w", encoding="utf-8", newline="").write(s)
print("ok")
