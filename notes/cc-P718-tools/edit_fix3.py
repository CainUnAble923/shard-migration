def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


T = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Tutorial/"
C = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/"

edit(T + "TutorialTradeTrialVerification.cs", [
("""        Assert.Equal(38, TutorialStations.All.Length); // cc-P663: core.farm joined the core
        Assert.Equal(20, TutorialWingTrials.Trades.Length); // 28 wing stations less P290's 8
        Assert.Equal(28, TutorialStations.All.Count(s => !s.IsCore));""",
 """        Assert.Equal(39, TutorialStations.All.Length); // cc-P663: core.farm joined the core; cc-P718: client.tips
        Assert.Equal(20, TutorialWingTrials.Trades.Length); // 28 wing stations less P290's 8
        Assert.Equal(28, TutorialStations.All.Count(s => !s.IsCore && !TutorialStations.IsAnytime(s.Key)));"""),
])

edit(C + "TutorialCorePlacement.cs", [
("""        // cc-P718: the old wall-arm signpost a seeded world still has makes way for the standing one.
        var oldSignposts = new List<Item>();
        foreach (var i in map.GetItemsInRange<Static>(Ground(ChatSignpost), 0))
        { if (!i.Deleted && i.ItemID == OldSignpostId && i.Name == OldChatSignpostName) { oldSignposts.Add(i); } }
""", ""),
("""            foreach (var old in oldSignposts) { old.Delete(); }
""", """            RemoveOldSignpost(map); // cc-P718
"""),
("""    private static void Place(Mobile m, Point3D spot, Map map)""", """    /// <summary>cc-P718: removes the old wall-arm chat signpost a seeded world still has. Returns how many.</summary>
    public static int RemoveOldSignpost(Map map)
    {
        var old = new List<Item>();
        foreach (var i in map.GetItemsInRange<Static>(Ground(ChatSignpost), 0))
        { if (!i.Deleted && i.ItemID == OldSignpostId && i.Name == OldChatSignpostName) { old.Add(i); } }
        foreach (var i in old) { i.Delete(); }
        return old.Count;
    }

    private static void Place(Mobile m, Point3D spot, Map map)"""),
])

edit(T + "TutorialIsleWalkFixesVerification.cs", [
("""        // The seeder swaps the old wall-arm post for the standing one.
        TutorialCorePlacement.IsTestShard = () => true;
        TutorialFarm.IsTestShard = () => true;
        TutorialCorePlacement.FitsOn = (_, _) => true;
        var isle = TutorialWorld.Isle;
        var old = new Static(TutorialCorePlacement.OldSignpostId) { Name = TutorialCorePlacement.OldChatSignpostName };
        old.MoveToWorld(TutorialWorld.Ground(TutorialCorePlacement.ChatSignpost), isle);
        TutorialCorePlacement.SeedOn(isle, false, withHaven: false);
        Assert.True(old.Deleted);
        var posts = new List<Static>();
        foreach (var post in isle.GetItemsInRange<Static>(TutorialWorld.Ground(TutorialCorePlacement.ChatSignpost), 0))
        {
            posts.Add(post);
        }

        Assert.Contains(posts, s => s.ItemID == TutorialCorePlacement.SignpostId && s.Name == TutorialCorePlacement.ChatSignpostName);""",
 """        // The seeder removes the old wall-arm post (then places the standing one from Props).
        var isle = TutorialWorld.Isle;
        var old = new Static(TutorialCorePlacement.OldSignpostId) { Name = TutorialCorePlacement.OldChatSignpostName };
        var other = new Static(TutorialCorePlacement.OldSignpostId) { Name = "someone else's post" };
        old.MoveToWorld(TutorialWorld.Ground(TutorialCorePlacement.ChatSignpost), isle);
        other.MoveToWorld(TutorialWorld.Ground(TutorialCorePlacement.ChatSignpost), isle);
        try
        {
            Assert.Equal(1, TutorialCorePlacement.RemoveOldSignpost(isle));
            Assert.True(old.Deleted);
            Assert.False(other.Deleted);
        }
        finally
        {
            old.Delete();
            other.Delete();
        }"""),
("""        var tamsin = p.Add(new TutorialGuide());
        tamsin.MoveToWorld(Beside(p.Pm, 2), p.Pm.Map);
""", """        var tamsin = p.Add(new TutorialGuide());
        tamsin.MoveToWorld(Beside(p.Pm, 2), p.Pm.Map);
        TutorialGreeting.Forget(tamsin, p.Pm); // arriving beside the trainee may already have greeted (OnMovement)
"""),
("""        var wren = p.Add(new TutorialFarmhand());
        wren.MoveToWorld(Beside(p.Pm, 2), p.Pm.Map);
""", """        var wren = p.Add(new TutorialFarmhand());
        wren.MoveToWorld(Beside(p.Pm, 2), p.Pm.Map);
        TutorialGreeting.Forget(wren, p.Pm);
"""),
])
print("ok")
