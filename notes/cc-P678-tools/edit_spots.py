"""cc-P678 (SoS swap S7) step 1: New Haven's spots move into the author's Haven. Edits the code copy by exact replacement
(the Read tool is denied on the code copy in unattended runs). Every spot was checked open on SoS 3.0 by townmap.py."""
C = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/'


def edit(name, pairs):
    p = C + name
    t = open(p, 'rb').read().decode('utf-8')
    crlf = '\r\n' in t
    t = t.replace('\r\n', '\n')
    for old, new in pairs:
        assert t.count(old) == 1, (name, old[:70], t.count(old))
        t = t.replace(old, new)
    if crlf:
        t = t.replace('\n', '\r\n')
    open(p, 'wb').write(t.encode('utf-8'))


edit('Tutorial/HavenSpots.cs', [
    ("""// cc-P663 (P481 F3, P673 1.4): every New Haven spot the tutorial reads, in one place. P678 (P673 S7) moves New Haven into
// the Siege of Sosaria map's Haven town and changes only this file. Notes: shard-migration
// notes/cc-P663-tutorial-moves-to-isle.md.
""",
     """// cc-P663 (P481 F3, P673 1.4): every New Haven spot the tutorial reads, in one place. Notes: shard-migration
// notes/cc-P663-tutorial-moves-to-isle.md.
//
// cc-P678 (P673 S7): New Haven moved into the Siege of Sosaria map's Haven town (the author's restored pre-UOML Haven,
// x 3600-3760, y 2500-2665: Uzeraan's Mansion, the Second Bank of Haven, the smithy, the docks). The old plaza (3460-
// 3530, 2540-2600) is forest and shore on SoS. Every spot below was checked on SoS 3.0's own files (open ground, not
// under an impassable static, its floor's Z; shard-migration notes/cc-P678-tools/townmap.py and spots.py), and keeps
// its place relative to the start: the start on the square's east-west street north of the mansion's garden, Rook,
// the moongate's way out and the quest board beside it. Notes: notes/cc-P678-new-haven-moves.md.
"""),
    ("""    /// send-home (3503,2574,14). Settable only as a seam for tests; S7 changes the value here.
    /// </summary>
    public static Point3D Start { get; set; } = new(3503, 2574, 14);

    /// <summary>Rook Hallowell, on the plaza two tiles from the start (cc-P80).</summary>
    public static readonly Point3D Rook = new(3500, 2572, 14);

    /// <summary>Where the isle's dock moongate sets a trainee down: beside Rook (the old travel gate's exit, cc-P289).</summary>
    public static readonly Point3D MoongateExit = new(3501, 2572, 14);

    /// <summary>The town's centre, for "a vet in New Haven" (60 tiles round it).</summary>
    public static readonly Point3D Centre = new(3500, 2590, 0);

    /// <summary>The vet by the stables, placed when the town has none (cc-P480).</summary>
    public static readonly Point3D VetSpot = new(3526, 2578, 7);

    /// <summary>New Haven's public moongate (pinned PublicMoongate.cs:194), the travel tour's first stop.</summary>
    public static readonly Point3D PublicMoongate = new(3450, 2677, 25);

    /// <summary>The town healer's spawner (pinned Vendors.json; ClusterFNewHavenServicesSeeder).</summary>
    public static readonly Point3D Healer = new(3462, 2559, 35);
""",
     """    /// send-home. Settable only as a seam for tests. cc-P678: on the square, north of the mansion's garden (was the
    /// plaza's 3503,2574,14).
    /// </summary>
    public static Point3D Start { get; set; } = new(3634, 2586, 0);

    /// <summary>Rook Hallowell, two tiles from the start, as on the old plaza (cc-P80; was 3500,2572,14).</summary>
    public static readonly Point3D Rook = new(3631, 2584, 0);

    /// <summary>Where the isle's dock moongate sets a trainee down: beside Rook (the old travel gate's exit, cc-P289).</summary>
    public static readonly Point3D MoongateExit = new(3632, 2584, 0);

    /// <summary>The quest board, one tile from the start as on the old plaza (NewHavenQuestBoard; was 3502,2573,14).</summary>
    public static readonly Point3D QuestBoard = new(3633, 2585, 0);

    /// <summary>The reset stone (ClusterFResetStone; was 3501,2575,14).</summary>
    public static readonly Point3D ResetStone = new(3632, 2587, 0);

    /// <summary>The Fountain of Youth, in the mansion's garden (was 3497,2583,14 on the plaza).</summary>
    public static readonly Point3D FountainOfYouth = new(3628, 2595, 0);

    /// <summary>The town's centre: the square. The travel tour starts here; "a vet in New Haven" is 60 tiles round it.</summary>
    public static readonly Point3D Centre = new(3640, 2590, 0);

    /// <summary>The vet, by the farmhouse at the town's east edge, placed when the town has none (cc-P480).</summary>
    public static readonly Point3D VetSpot = new(3712, 2580, 20);

    /// <summary>
    /// New Haven's public moongate: the open field east of the square. S4 (P673) puts PMList's New Haven gate here; the
    /// travel tour points at it. (Was pinned PublicMoongate.cs:194's 3450,2677,25, sea on SoS.)
    /// </summary>
    public static readonly Point3D PublicMoongate = new(3696, 2570, 16);

    /// <summary>The town healer: pinned's pre-UOML Haven healer spawner (Spawns/uoml/trammel/Vendors.json).</summary>
    public static readonly Point3D Healer = new(3665, 2581, 0);

    /// <summary>The bank: the Second Bank of Haven, pinned's pre-UOML Haven banker spawner (uoml Vendors.json).</summary>
    public static readonly Point3D Bank = new(3620, 2617, 0);

    /// <summary>The docks (the author's "Haven / Docks" spot).</summary>
    public static readonly Point3D Dock = new(3650, 2653, 0);
"""),
])

edit('CharacterCreation.cs', [
    ('        new("New Haven", "The Bountiful Harvest Inn", 1150168, 3503, 2574, 14, Map.Trammel),',
     '        // cc-P678: the start moved with New Haven into the author\'s Haven (Tutorial/HavenSpots.cs, the one place).\n'
     '        new("New Haven", "The Bountiful Harvest Inn", 1150168, Server.Tutorial.HavenSpots.Start.X, Server.Tutorial.HavenSpots.Start.Y, Server.Tutorial.HavenSpots.Start.Z, Map.Trammel),'),
])

edit('Engines/ML Quests/Items/NewHavenQuestBoard.cs', [
    ('    public static readonly Point3D HomeLocation = new(3502, 2573, 14);',
     '    public static readonly Point3D HomeLocation = Server.Tutorial.HavenSpots.QuestBoard; // cc-P678: was 3502,2573,14'),
])
edit('ClusterFResetStone.cs', [
    ('        public static readonly Point3D Location = new(3501, 2575, 14);',
     '        public static readonly Point3D Location = Server.Tutorial.HavenSpots.ResetStone; // cc-P678: was 3501,2575,14'),
])
edit('FountainOfYouth/FountainOfYouth.cs', [
    ('    public static readonly Point3D NewHavenSpot = new(3497, 2583, 14);',
     '    public static readonly Point3D NewHavenSpot = Server.Tutorial.HavenSpots.FountainOfYouth; // cc-P678: was 3497,2583,14'),
])
edit('ClusterFNewHavenSeeder.cs', [
    ('        new("Sir Helper", "Town square", typeof(SirHelper), () => new SirHelper(), 3503, 2574, Direction.South, 14),',
     '        // cc-P678: on the new start, as on the old (Tutorial/HavenSpots.cs).\n'
     '        new("Sir Helper", "Town square", typeof(SirHelper), () => new SirHelper(), 3634, 2586, Direction.South, 0),'),
])
edit('Tutorial/TutorialTradeTrials.cs', [
    ('        public static readonly Point2D TourCentre = new(3460, 2590);',
     '        public static readonly Point2D TourCentre = new(HavenSpots.Centre.X, HavenSpots.Centre.Y); // cc-P678: was 3460,2590'),
])
edit('ClusterFAchievements.cs', [
    ('            TriggerKind.VisitOldHaven      => "found the ruins of Old Haven",',
     '            TriggerKind.VisitOldHaven      => "found the way beneath Haven", // cc-P678: the hatch; the key is unchanged'),
    ('            "Discover the ruins of Old Haven. Nobody lives there anymore. That is, objectively, information you now possess.",',
     '            "Find the way beneath Haven, through the hatch in the Second Bank. Nobody keeps their gold down there. That is, objectively, information you now possess.",'),
])
edit('LeagueRegistrarGump.cs', [
    ('            "<BASEFONT COLOR=#AAAAAA>The ruins of Old Haven lie to the southwest. " +',
     '            "<BASEFONT COLOR=#AAAAAA>Something lies beneath Haven: ask at the Second Bank. " +'),
])
print('ok')
