r"""cc-P678 part 4: the way down becomes a cellar hatch in the Second Bank of Haven's back room.
    python -P edit_hatch.py      (edits ClusterFRootdeepSeeder.cs and OldHavenBurrowsRegion.cs in the code copy)
"""
CODE = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/"

REPS = {
    "ClusterFRootdeepSeeder.cs": [
        ("""//     not duplicated).
""", """//     not duplicated).
//     cc-P678 (SoS swap S7): on the Siege of Sosaria map the ruined Second Bank is the author's rebuilt Second Bank of
//     Haven, New Haven's bank, and the ant hill is gone (S2 drops it from the map patch). The way down is a cellar hatch in
//     the bank's back room (3621,2611; the north annex, entered from the main room by its door at 3616,2614): the
//     seeder places the hatch (art 0x3E65 "hatch", a walkable surface 3 high, a server item, so the town's statics are
//     untouched) and one teleporter down on its tile; the mouth is that one tile. The ladder up lands three tiles from it
//     in the same room (3618,2612). The retarget above still points an older ladder at the new landing.
"""),
        ("""    /// <summary>P188's hole in the Second Bank of Haven (OldHavenBurrowsRegion.HoleEntrance), now one tile of the mouth.</summary>
    public static readonly Point2D Hole = new(3619, 2620);

    /// <summary>
    /// cc-P413: the burrow's dark mouth, inclusive: the dark core (columns 2-4, rows 1-4) of OSI's sinkhole set, which
    /// the map patch lays with its first piece at 3615,2616. Every tile takes a player down.
    /// </summary>
    public const int MouthX1 = 3617, MouthY1 = 2617, MouthX2 = 3619, MouthY2 = 2620;""",
         """    /// <summary>cc-P678: the cellar hatch in the Second Bank of Haven's back room (OldHavenBurrowsRegion.HoleEntrance).</summary>
    public static readonly Point2D Hole = new(3621, 2611);

    /// <summary>The hatch: OSI's "hatch" art, a Surface 3 high, so a player walks onto it and the teleporter fires.</summary>
    public const int HatchItemId = 0x3E65;

    public const string HatchName = "a cellar hatch";

    /// <summary>
    /// The tiles that take a player down, inclusive. cc-P413 made it the ant hill's twelve-tile mouth; cc-P678 makes it
    /// the hatch's one tile.
    /// </summary>
    public const int MouthX1 = 3621, MouthY1 = 2611, MouthX2 = 3621, MouthY2 = 2611;"""),
        ("""    /// <summary>
    /// cc-P413: where the ladder up lands: outside the bank's collapsed south wall (the gap is 3618-3620,2622), facing
    /// the mound, two tiles south of the mouth, so nobody is sent straight back down. Outside every spawner's walking box.
    /// </summary>
    public static readonly Point2D BesideMound = new(3619, 2623);

    public static readonly TeleporterRow LadderUp =
        new("the rope ladder up to Old Haven", LadderFoot.X, LadderFoot.Y, BesideMound.X, BesideMound.Y);""",
         """    /// <summary>
    /// cc-P678: where the ladder up lands: the bank's back room, three tiles west of the hatch (cc-P413's was outside the
    /// ruined bank's south wall, by the mound), so nobody is sent straight back down. Floor Z 0, reached on foot from the
    /// town (notes/cc-P678-tools/soswalk.py).
    /// </summary>
    public static readonly Point2D BesideHatch = new(3618, 2612);

    public static readonly TeleporterRow LadderUp =
        new("the rope ladder up to the Second Bank of Haven", LadderFoot.X, LadderFoot.Y, BesideHatch.X, BesideHatch.Y);"""),
        ("""                rows.Add(new TeleporterRow($"the burrow mouth ({x},{y}) down to the Landing", x, y, Arrival.X, Arrival.Y));""",
         """                rows.Add(new TeleporterRow($"the cellar hatch ({x},{y}) down to the Landing", x, y, Arrival.X, Arrival.Y));"""),
        ("""        bool Refused, int Spawners, int Ankhs, int Crawlways, int Present, string Message, int Teleporters = 0, int FloorTraps = 0,
        int FloorTrapsPresent = 0, int TeleportersRetargeted = 0
    );""", """        bool Refused, int Spawners, int Ankhs, int Crawlways, int Present, string Message, int Teleporters = 0, int FloorTraps = 0,
        int FloorTrapsPresent = 0, int TeleportersRetargeted = 0, int Hatches = 0, int HatchesPresent = 0
    );"""),
        ("""        int floorTraps = 0, floorTrapsPresent = 0;
""", """        int hatches = 0, hatchesPresent = 0;
        if (FindHatch(map) != null)
        {
            hatchesPresent++;
        }
        else
        {
            if (!dryRun)
            {
                PlaceHatch(map);
            }

            hatches++;
        }

        int floorTraps = 0, floorTrapsPresent = 0;
"""),
        ("""{teleporters} teleporters, {floorTraps} floor traps; {(dryRun ? "would point" : "pointed")} {retargeted} teleporters at their new landing; already there {present} (and {floorTrapsPresent} floor traps).",
            teleporters, floorTraps, floorTrapsPresent, retargeted);""",
         """{teleporters} teleporters, {hatches} hatch, {floorTraps} floor traps; {(dryRun ? "would point" : "pointed")} {retargeted} teleporters at their new landing; already there {present} (and {hatchesPresent} hatch, {floorTrapsPresent} floor traps).",
            teleporters, floorTraps, floorTrapsPresent, retargeted, hatches, hatchesPresent);"""),
        ("""    /// <summary>A stock teleporter on the row's tile to the row's destination: players only, no delay, no effect.</summary>""",
         """    public static Point3D HatchAt => new(Hole.X, Hole.Y, 0);

    /// <summary>cc-P678: the cellar hatch, an immovable Static on the bank's floor.</summary>
    public static Static PlaceHatch(Map map)
    {
        var hatch = new Static(HatchItemId) { Name = HatchName };
        hatch.MoveToWorld(HatchAt, map);
        return hatch;
    }

    public static Static FindHatch(Map map)
    {
        foreach (var item in map.GetItemsInRange<Static>(HatchAt, 0))
        {
            if (!item.Deleted && item.ItemID == HatchItemId)
            {
                return item;
            }
        }

        return null;
    }

    /// <summary>A stock teleporter on the row's tile to the row's destination: players only, no delay, no effect.</summary>"""),
        ("""the eight floor traps and the two teleporters of the way in (the hole in Old Haven, the ladder up), where missing.""",
         """the eight floor traps, the cellar hatch in the Second Bank of Haven and the two teleporters of the way in (the hatch, the ladder up), where missing."""),
    ],
    "Regions/OldHavenBurrowsRegion.cs": [
        ("""    /// y 2617-2620 (ClusterFRootdeepSeeder.Mouth*); this tile is one of the twelve, so the Entrance stays here.
    /// </summary>
    public static readonly Point3D HoleEntrance = new(3619, 2620, 0);""",
         """    /// y 2617-2620 (ClusterFRootdeepSeeder.Mouth*); this tile is one of the twelve, so the Entrance stays here.
    /// cc-P678: on SoS the bank is the author's rebuilt Second Bank of Haven, New Haven's bank, and the way down is the
    /// cellar hatch in its back room (ClusterFRootdeepSeeder.Hole), so the Entrance moves there.
    /// </summary>
    public static readonly Point3D HoleEntrance = new(3621, 2611, 0);"""),
    ],
}

for name, reps in REPS.items():
    p = CODE + name
    s = open(p, encoding="utf-8").read()
    for a, b in reps:
        assert s.count(a) == 1, (name, a[:70])
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
