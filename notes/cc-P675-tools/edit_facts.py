"""cc-P675 (S2 part 5): FoldVerification follows the mirror and the beach to site A; the real-data adapter fact reads
the SoS map. Edits the code copy's tests in place; run once."""
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


edit(r'server\tests\Regions\FoldVerification.cs', [
    ('''//   2. (Real client data only; skips without it, run by hand with the client mounted.) A player moved to 32 and to 40
//      stands on Trammel's land tile and Z at that spot, and the same statics are there.
''', '''//   2. (Real client data only; skips without it, run by hand with the client mounted.) A player moved to 32 and to 40
//      stands on Trammel's land tile and Z at that spot, and the same statics are there. cc-P675: the spots are on the
//      SoS map (Valunstead, the New Haven start, the isle's beach), run with the server's map overlay mounted.
'''),
    ('''//   4. A player found on Trammel over void C is sent to the New Haven start; staff are left there; travel into it is
//      refused for a player.
''', '''//   4. A player found on Trammel over void C is sent to the New Haven start; staff are left there; travel into it is
//      refused for a player. cc-P675: the mirror is site A's empty room (x 6160-7167, y 3744-4095) on Trammel and on
//      Felucca; a player at the isle's beach (6638, 3993) on either is sent home, and one inside the author's Passage
//      of Lost Souls level 2 (6202, 2116, void C on stock Trammel) is left where they are.
'''),
    ('''//   7. [Fold goto: test shard only; n 0 to 16; the arrival beach by default, or x y.
''', '''//   7. [Fold goto: test shard only; n 0 to 16; the arrival beach by default (6638, 3993 since cc-P675), or x y.
'''),
    ('''        FoldMaps.Configure();
        FoldMirrorRegion.Initialize();
    }

    private static readonly Point3D Spot = new(6214, 2001, 0);          // the arrival beach, in void C
    private static readonly Point3D Elsewhere = new(1220, 1220, 0);     // ordinary Trammel, as YoungPlayerVerification
    private static readonly Point3D InVoidC = new(6300, 2000, 0);
''', '''        FoldMaps.Configure();
        SosMaps.Configure(); // cc-P675: Felucca on Trammel's files, before the mirror's Felucca twin
        FoldMirrorRegion.Initialize();
    }

    private static readonly Point3D Spot = new(6638, 3993, 0);          // the arrival beach (cc-P675: site A)
    private static readonly Point3D Elsewhere = new(1220, 1220, 0);     // ordinary Trammel, as YoungPlayerVerification
    private static readonly Point3D InMirror = Spot;                    // the beach, on Trammel or Felucca
    private static readonly Point3D InPassage = new(6202, 2116, -9);    // the author's Passage of Lost Souls, level 2
'''),
    ('''        // New Haven: land 0x03E9 at Z 14, statics 0x0B24 and 0x0D33 on the tile north (cc-P135 5.1, cc-P134 section 4).
        foreach (var (x, y) in new[] { (3503, 2574), (3503, 2573), (6214, 2001) })
''', '''        // cc-P675, the SoS map: Valunstead's open ground and a floor of its hall, the New Haven start, the isle's beach.
        foreach (var (x, y) in new[] { (504, 384), (479, 388), (3634, 2586), (6638, 3993) })
'''),
    ('''        Assert.Equal(0x03E9, Map.Maps[32].Tiles.GetLandTile(3503, 2574).ID);
        Assert.Equal(14, Map40.Tiles.GetLandTile(3503, 2574).Z);
        Assert.Equal(0x0244, Map40.Tiles.GetLandTile(6214, 2001).ID); // void C is still void until F2 paints the isle
''', '''        Assert.Equal(0x0003, Map.Maps[32].Tiles.GetLandTile(504, 384).ID);   // stock Trammel: sea 0x00A8-0x00AB at -5
        Assert.Equal(15, Map40.Tiles.GetLandTile(504, 384).Z);
        Assert.Equal(0x0073, Map40.Tiles.GetLandTile(6638, 3993).ID);        // the isle's beach (trammel.mapops)
'''),
    ('''    [Fact]
    public void APlayerFoundOnTrammelsMirrorIsSentToNewHaven()
    {
        ShardTestClock.Arm();
        var outside = Player(Elsewhere, Map.Trammel);
        var trainee = Player(InVoidC, Map.Trammel);
        var staff = Player(InVoidC, Map.Trammel, AccessLevel.GameMaster);
        try
        {
            Assert.IsType<FoldMirrorRegion>(Region.Find(new Point3D(6160, 1832, 0), Map.Trammel));
            Assert.IsType<FoldMirrorRegion>(Region.Find(new Point3D(6639, 2279, 0), Map.Trammel));
            Assert.IsNotType<FoldMirrorRegion>(Region.Find(new Point3D(6159, 2000, 0), Map.Trammel));
            Assert.IsNotType<FoldMirrorRegion>(Region.Find(new Point3D(6640, 2000, 0), Map.Trammel));
            Assert.IsNotType<FoldMirrorRegion>(Region.Find(InVoidC, Map.Maps[32]));
            Assert.False(SpellHelper.CheckTravel(outside, Map.Trammel, InVoidC, TravelCheckType.RecallTo, out _));

            ShardTestClock.Advance(TimeSpan.FromMilliseconds(100));

            // cc-P663: the New Haven start (HavenSpots); the start list's first entry is the isle's now.
            Assert.Same(Map.Trammel, trainee.Map);
            Assert.Equal(Server.Tutorial.HavenSpots.Start, trainee.Location);
            Assert.Equal(InVoidC, staff.Location);
        }
        finally
        {
            outside.Delete();
            trainee.Delete();
            staff.Delete();
        }
    }
''', '''    [Fact]
    public void APlayerFoundOnTrammelsMirrorIsSentToNewHaven()
    {
        ShardTestClock.Arm();
        var outside = Player(Elsewhere, Map.Trammel);
        var trainee = Player(InMirror, Map.Trammel);
        var feluccan = Player(InMirror, Map.Felucca);
        var staff = Player(InMirror, Map.Trammel, AccessLevel.GameMaster);
        var delvers = new[] { Player(InPassage, Map.Trammel), Player(InPassage, Map.Felucca) };
        try
        {
            foreach (var map in new[] { Map.Trammel, Map.Felucca })
            {
                // cc-P675: site A's empty room, to the map's east and south edges.
                Assert.IsType<FoldMirrorRegion>(Region.Find(new Point3D(6160, 3744, 0), map));
                Assert.IsType<FoldMirrorRegion>(Region.Find(new Point3D(7167, 4095, 0), map));
                Assert.IsType<FoldMirrorRegion>(Region.Find(InMirror, map));
                Assert.IsNotType<FoldMirrorRegion>(Region.Find(new Point3D(6159, 3900, 0), map));
                Assert.IsNotType<FoldMirrorRegion>(Region.Find(new Point3D(6600, 3743, 0), map));
                Assert.IsNotType<FoldMirrorRegion>(Region.Find(InPassage, map));
                Assert.IsNotType<FoldMirrorRegion>(Region.Find(new Point3D(6300, 2000, 0), map)); // void C, P661's mirror
                Assert.False(SpellHelper.CheckTravel(outside, map, InMirror, TravelCheckType.RecallTo, out _), map.Name);
            }

            Assert.IsNotType<FoldMirrorRegion>(Region.Find(InMirror, Map.Maps[32]));

            ShardTestClock.Advance(TimeSpan.FromMilliseconds(100));

            // cc-P663: the New Haven start (HavenSpots); the start list's first entry is the isle's now.
            foreach (var sent in new[] { trainee, feluccan })
            {
                Assert.Same(Server.Tutorial.HavenSpots.Map, sent.Map);
                Assert.Equal(Server.Tutorial.HavenSpots.Start, sent.Location);
            }

            Assert.Equal(InMirror, staff.Location);
            Assert.Same(Map.Trammel, delvers[0].Map);
            Assert.Same(Map.Felucca, delvers[1].Map);
            Assert.All(delvers, d => Assert.Equal(InPassage, d.Location));
        }
        finally
        {
            outside.Delete();
            trainee.Delete();
            feluccan.Delete();
            staff.Delete();
            foreach (var d in delvers)
            {
                d.Delete();
            }
        }
    }
'''),
    ('''            Assert.Equal(new Point2D(6214, 2001), new Point2D(gm.X, gm.Y));
''', '''            Assert.Equal(new Point2D(6638, 3993), new Point2D(gm.X, gm.Y));
'''),
])

edit(r'server\tests\Misc\MapCheckRealDataVerification.cs', [
    ('''//   1. check the real adapter (Map.Tiles and TileData) against New Haven tiles read independently from the UOP by name
//      hash in cc-P134 (notes/cc-P134-vseuoaware-art-checks-mcp.md section 4): Trammel 3503,2574 is land 0x03E9 Z 14
//      with no statics, and 3503,2573 holds statics 0x0D33 and 0x0B24 at Z 14;
''', '''//   1. check the real adapter (Map.Tiles and TileData) against tiles read independently from the UOP by name hash.
//      cc-P675: on the Siege of Sosaria map (the server's map overlay mounted over the client folder; shard-migration
//      notes/cc-P675-tools/spots.py read them): Trammel 3503,2574 (stock New Haven, forest now) is land 0x0006 Z 14 with
//      no statics, and Valunstead 479,388 holds floors 0x04AB at Z 20 and 40 and roof 0x0596 at 49 on land 0x0006 Z 15.
//      It was cc-P134's stock read (notes/cc-P134-vseuoaware-art-checks-mcp.md section 4) until the swap;
'''),
    ('''    public void TheRealAdapterReadsNewHavenAsTheIndependentUopReadDid()
    {
        TileDataRequirement.SkipIfMissing();
        var src = new ClusterFMapTileSource(Map.Trammel);
        var land = src.GetLandTile(3503, 2574);
        Assert.Equal(0x03E9, land.ID);
        Assert.Equal(14, land.Z);
        Assert.Empty(src.GetStaticTiles(3503, 2574));
        var statics = src.GetStaticTiles(3503, 2573).Select(s => (s.ID, s.Z)).OrderBy(s => s.ID).ToArray();
        Assert.Equal(new[] { (0x0B24, 14), (0x0D33, 14) }, statics);
''', '''    public void TheRealAdapterReadsTheSosMapAsTheIndependentUopReadDid()
    {
        TileDataRequirement.SkipIfMissing();
        var src = new ClusterFMapTileSource(Map.Trammel);
        var land = src.GetLandTile(3503, 2574);
        Assert.Equal(0x0006, land.ID);
        Assert.Equal(14, land.Z);
        Assert.Empty(src.GetStaticTiles(3503, 2574));
        Assert.Equal(0x0006, src.GetLandTile(479, 388).ID);
        Assert.Equal(15, src.GetLandTile(479, 388).Z);
        var statics = src.GetStaticTiles(479, 388).Select(s => (s.ID, s.Z)).OrderBy(s => s.Z).ToArray();
        Assert.Equal(new[] { (0x04AB, 20), (0x04AB, 40), (0x0596, 49) }, statics);
'''),
])
