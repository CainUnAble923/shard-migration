"""cc-P705: the test changes, as guarded replacements (see edit_code.py).

    python -P edit_tests.py <code copy>/server
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_code import edit  # noqa: E402  (edit_code's module body needs argv[1]: the same server folder)

edit('tests/Tutorial/TutorialTestStart.cs', [
    ("""    public static void Begin(PlayerMobile pm, TutorialStart.Choice choice = TutorialStart.Choice.Isle)
    {
        FoldMaps.Configure();""", """    public static void Begin(PlayerMobile pm, TutorialStart.Choice choice = TutorialStart.Choice.Isle)
    {
        FoldMaps.Configure();
        // cc-P705: the test world's map is void at the isle's site (no P662 patch in the host); it stands in for the land.
        TutorialWorld.IsleReady = () => true;"""),
])

edit('tests/Tutorial/TutorialIsleVerification.cs', [
    ("""    private readonly Action<PlayerMobile> _rewards = ClusterFTutorial.GraduationRewards;
""", """    private readonly Action<PlayerMobile> _rewards = ClusterFTutorial.GraduationRewards;
    private readonly Func<bool> _isleReady = TutorialWorld.IsleReady;
"""),
    ("""        TutorialCorePlacement.FitsOn = (_, _) => true;
        ClusterFTutorial.GraduationRewards = _ => { };
    }""", """        TutorialCorePlacement.FitsOn = (_, _) => true;
        ClusterFTutorial.GraduationRewards = _ => { };
        TutorialWorld.IsleReady = () => true; // cc-P705: the host's map is void at the isle; it stands in for P662's land
    }"""),
    ("""        TutorialCorePlacement.FitsOn = _fits;
        ClusterFTutorial.GraduationRewards = _rewards;
    }""", """        TutorialCorePlacement.FitsOn = _fits;
        ClusterFTutorial.GraduationRewards = _rewards;
        TutorialWorld.IsleReady = _isleReady;
    }"""),
    ("""        Assert.Equal(TutorialStart.Choice.Haven, TutorialStart.ChoiceOf(cities[1]));
    }
}""", """        Assert.Equal(TutorialStart.Choice.Haven, TutorialStart.ChoiceOf(cities[1]));
    }

    // ---------------------------------------------------------------- cc-P705: the Codex findings on P663

    // P1: the dock's stops stand on the planks, not on the sea floor under them; a floor is stood on, a roof is not.
    [Fact]
    public void TheGroundIsTheWalkableSurfaceNotTheLandUnderIt()
    {
        Assert.Equal(-2, TutorialWorld.SurfaceZ(-5, [(-3, 0x07C9)]));          // a dock plank (height 1) over the sea
        Assert.Equal(0, TutorialWorld.SurfaceZ(0, [(0, 0x0515), (20, 0x049C)])); // a cobble floor under a slate roof
        Assert.Equal(-5, TutorialWorld.SurfaceZ(-5, [(-5, 0x1797)]));            // static water is no surface
        Assert.Equal(3, TutorialWorld.SurfaceZ(3, []));                          // bare land
    }

    // P2: the tutorial-off list's New Haven entry follows HavenSpots, as every other New Haven spot does (S7 moves them).
    [Fact]
    public void TheTutorialOffListReadsNewHavensStartFromHavenSpots()
    {
        var start = HavenSpots.Start;
        try
        {
            HavenSpots.Start = new Point3D(3510, 2580, 15);
            var city = Assert.Single(Server.Engines.CharacterCreation.CharacterCreation.TutorialOffCities());
            Assert.Equal("New Haven", city.City);
            Assert.Equal(HavenSpots.Start, city.Location);
            Assert.Same(HavenSpots.Map, city.Map);
        }
        finally
        {
            HavenSpots.Start = start;
        }
    }

    // P2: staff who keep the default "Tutorial Island" start at New Haven's start, never at the entry's display spot.
    [Fact]
    public void StaffWhoPickTheIsleStartInNewHavenNotInTheSea()
    {
        using var t = new Trainees();
        var gm = t.Add();
        gm.AccessLevel = AccessLevel.GameMaster;
        var (at, map) = TutorialStart.OnCreated(gm, TutorialStart.Cities()[0]);
        Assert.Equal((HavenSpots.Start, HavenSpots.Map), (at, map));
        Assert.NotEqual(TutorialStart.IsleDisplay, at);
        Assert.Equal(TutorialStart.Choice.None, TutorialStart.Pending(gm)); // staff are never enrolled
    }

    // The missing isle: a release with the start choice but before P662's map patch never strands a character in the
    // void. The pick starts in New Haven, and the account's tutorial stays unused.
    [Fact]
    public void WithoutTheIslesLandTheIslePickStartsInNewHaven()
    {
        using var t = new Trainees();
        var pm = t.Add();
        TutorialWorld.IsleReady = () => false;
        Create(pm, TutorialStart.Choice.Isle);
        Assert.Same(HavenSpots.Map, pm.Map);
        Assert.Equal(HavenSpots.Start, pm.Location);
        Assert.Equal(TutorialStart.Outcome.IsleMissing, TutorialStart.ConsumeAtLogin(pm));
        Assert.Same(HavenSpots.Map, pm.Map);
        Assert.Equal(HavenSpots.Start, pm.Location);
        Assert.Equal(TutorialState.NotStarted, t.Record.State);
        Assert.False(ClusterFTutorial.IsParticipant(pm));
        Assert.Equal(TutorialStart.Choice.None, TutorialStart.Pending(pm));

        // Once the land is there, a new character of the account goes to the isle as usual.
        TutorialWorld.IsleReady = () => true;
        var next = t.Add();
        Create(next, TutorialStart.Choice.Isle);
        Assert.Equal(TutorialStart.Outcome.Isle, TutorialStart.ConsumeAtLogin(next));
        Assert.True(TutorialWorld.IsOnIsle(next));
    }

    // The real check: on the host's map (stock Trammel's file, void at site A) the isle is not ready.
    [Fact]
    public void OnAMapWithoutTheIslesPatchTheIsleIsNotReady()
    {
        Assert.False(_isleReady());
    }
}"""),
])
