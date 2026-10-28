"""cc-P675 (S2 part 4): the Fold's mirror region moves to the empty room of site A, with a Felucca twin; [Fold goto's
default is the isle's beach on the SoS map. Edits the code copy in place; run once."""
import os

CODE = os.environ.get('SL_SHARD_REPO', r'D:\UO\golems\Iron\ShatteredLegacy')


def edit(rel, pairs):
    p = os.path.join(CODE, rel)
    s = open(p, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (rel, old[:90])
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('edited', rel)


edit(r'server\customizations\Fold\FoldRegions.cs', [
    ('''// FoldMirrorRegion: Trammel over void C (x 6160-6639, y 1832-2279), where the Wakening Isle's tiles are painted (design
// 3.1). The same tiles exist on Trammel, where no road, gate or teleporter reaches them; if a bug or a future teleporter
// ever puts a player there, they are sent to the New Haven start (HavenSpots.Start, cc-P663). Staff are left
// alone, so they can inspect the tiles on Trammel. Travel into it is refused for players too, so a rune never lands
// one there. P24 and P481 found void C in no pinned region and no ServUO Trammel region.
//
// FoldMirrorRegion is registered in Initialize, after RegionJsonSerializer.LoadRegions and World.Load (Main.cs:669-673),
// every start. Neither holds saved data.
''', '''// FoldMirrorRegion: Trammel and Felucca over the empty room of site A (x 6160-7167, y 3744-4095; cc-P673 1.4), where the
// Wakening Isle's tiles are painted (trammel.mapops, cc-P662). The same tiles exist on Trammel, and on Felucca since it
// reads Trammel's files (SosMaps.cs, cc-P675), where no road, gate or teleporter reaches them; if a bug or a future
// teleporter ever puts a player there, they are sent to the New Haven start (HavenSpots.Start, cc-P663). Staff are left
// alone, so they can inspect the tiles. Travel into it is refused for players too, so a rune never lands one there.
// cc-P675: it was void C (x 6160-6639, y 1832-2279) on stock Trammel; on the Siege of Sosaria map that is the author's
// Passage of Lost Souls (level 2 at 6202, 2116), so it moved before the swap goes live. P673 found the room void in the
// SoS file, in no region, spawner, decoration or teleporter of his or ours, the whole width to the map's east edge.
//
// FoldMirrorRegion is registered in Initialize, after RegionJsonSerializer.LoadRegions and World.Load (Main.cs:669-673),
// every start, once on each map. Neither holds saved data.
'''),
    ('''    /// <summary>Void C, x 6160-6639, y 1832-2279 inclusive (Rectangle3D's end is exclusive).</summary>
    public static readonly Rectangle3D Area = new(new Point3D(6160, 1832, MinZ), new Point3D(6640, 2280, MaxZ));
''', '''    /// <summary>Site A's empty room, x 6160-7167, y 3744-4095 inclusive (Rectangle3D's end is exclusive): to the map's edges.</summary>
    public static readonly Rectangle3D Area = new(new Point3D(6160, 3744, MinZ), new Point3D(7168, 4096, MaxZ));
'''),
    ('''    public static FoldMirrorRegion Instance { get; private set; }

    public FoldMirrorRegion() : base(RegionName, Map.Trammel, DefaultPriority, Area)
    {
    }

    public static void Initialize()
    {
        if (Instance != null || Map.Trammel == null)
        {
            return;
        }

        Instance = new FoldMirrorRegion();
        Instance.Register();
    }
''', '''    /// <summary>Trammel's mirror.</summary>
    public static FoldMirrorRegion Instance { get; private set; }

    /// <summary>cc-P675: Felucca's twin (Felucca reads Trammel's files).</summary>
    public static FoldMirrorRegion FeluccaInstance { get; private set; }

    public FoldMirrorRegion(Map map) : base(RegionName, map, DefaultPriority, Area)
    {
    }

    public static void Initialize()
    {
        if ((Instance == null || Instance.Map != Map.Trammel) && Map.Trammel != null)
        {
            Instance = new FoldMirrorRegion(Map.Trammel);
            Instance.Register();
        }

        if ((FeluccaInstance == null || FeluccaInstance.Map != Map.Felucca) && Map.Felucca != null)
        {
            FeluccaInstance = new FoldMirrorRegion(Map.Felucca);
            FeluccaInstance.Register();
        }
    }

    /// <summary>True on the two maps the mirror covers.</summary>
    public static bool Mirrors(Map map) => map != null && (map == Map.Trammel || map == Map.Felucca);
'''),
    ('''    /// <summary>Moves <paramref name="m"/> to the New Haven start if it is still a player inside the mirror.</summary>
    public static void SendHome(Mobile m)
    {
        if (m == null || m.Deleted || !SendsHome(m) || m.Map != Map.Trammel || !Area.Contains(m.Location))
''', '''    /// <summary>Moves <paramref name="m"/> to the New Haven start if it is still a player inside the mirror.</summary>
    public static void SendHome(Mobile m)
    {
        if (m == null || m.Deleted || !SendsHome(m) || !Mirrors(m.Map) || !Area.Contains(m.Location))
'''),
])

edit(r'server\customizations\Fold\FoldCommands.cs', [
    ('''    /// <summary>The Wakening Isle's west beach, where a trainee wakes (design 11.2, stop 0).</summary>
    public static readonly Point2D Arrival = new(6214, 2001);
''', '''    /// <summary>The Wakening Isle's west beach, where a trainee wakes (design 11.2, stop 0; cc-P675: site A, TutorialWorld.Beach).</summary>
    public static Point2D Arrival => Server.Tutorial.TutorialWorld.Beach;
'''),
    ('Without x y, the isle\'s arrival beach (6214, 2001); Z is', 'Without x y, the isle\'s arrival beach (6638, 3993); Z is'),
])

edit(r'server\customizations\Fold\FoldMaps.cs', [
    ('''//   index 32       "TheFold"        the Fold itself (the Wakening Isle is painted into Trammel's void C, F2)''',
     '''//   index 32       "TheFold"        the Fold itself (the Wakening Isle is painted into Trammel's site A, F2; P673 1.4)'''),
])
