"""cc-P705 round 2 (green run 1): SurfaceZ takes each tile's flags and height (the test host loads no tiledata), and the
host-map readiness fact goes (the host has no map data: CanFit succeeds anywhere).

    python -P edit_round2.py <code copy>/server
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_code import edit  # noqa: E402

edit('customizations/Tutorial/TutorialWorld.cs', [
    ("""        var statics = new List<(int Z, int ItemId)>();
        foreach (var tile in map.Tiles.GetStaticAndMultiTiles(p.X, p.Y))
        {
            statics.Add((tile.Z, tile.ID));
        }""", """        var statics = new List<(int Z, TileFlag Flags, int Height)>();
        foreach (var tile in map.Tiles.GetStaticAndMultiTiles(p.X, p.Y))
        {
            var data = TileData.ItemTable[tile.ID & TileData.MaxItemValue];
            statics.Add((tile.Z, data.Flags, data.CalcHeight));
        }"""),
    ("""    public static int SurfaceZ(int landAvg, IEnumerable<(int Z, int ItemId)> statics)
    {
        var best = landAvg;
        foreach (var (z, id) in statics)
        {
            var data = TileData.ItemTable[id & TileData.MaxItemValue];
            if (!data.Surface || data.Impassable)
            {
                continue;
            }

            var top = z + data.CalcHeight;""", """    public static int SurfaceZ(int landAvg, IEnumerable<(int Z, TileFlag Flags, int Height)> statics)
    {
        var best = landAvg;
        foreach (var (z, flags, height) in statics)
        {
            if ((flags & TileFlag.Surface) == 0 || (flags & TileFlag.Impassable) != 0)
            {
                continue;
            }

            var top = z + height;"""),
    ("""    /// The highest walkable surface (Surface and not Impassable) whose top is above the land""",
     """    /// The highest walkable surface (Surface and not Impassable; height as ItemData.CalcHeight) whose top is above the land"""),
])

edit('tests/Tutorial/TutorialIsleVerification.cs', [
    ("""        Assert.Equal(-2, TutorialWorld.SurfaceZ(-5, [(-3, 0x07C9)]));          // a dock plank (height 1) over the sea
        Assert.Equal(0, TutorialWorld.SurfaceZ(0, [(0, 0x0515), (20, 0x049C)])); // a cobble floor under a slate roof
        Assert.Equal(-5, TutorialWorld.SurfaceZ(-5, [(-5, 0x1797)]));            // static water is no surface
        Assert.Equal(3, TutorialWorld.SurfaceZ(3, []));                          // bare land""",
     """        // Flags and heights as stock tiledata has them (the host loads none): plank 0x07C9, cobbles 0x0515, grey slate
        // 0x049C, static water 0x1797.
        const TileFlag plank = TileFlag.Background | TileFlag.Surface | TileFlag.NoShoot;
        const TileFlag water = TileFlag.Background | TileFlag.Impassable | TileFlag.Wet;
        Assert.Equal(-2, TutorialWorld.SurfaceZ(-5, [(-3, plank, 1)]));                  // a dock plank over the sea
        Assert.Equal(0, TutorialWorld.SurfaceZ(0, [(0, plank, 0), (20, plank, 0)]));     // a floor under a slate roof
        Assert.Equal(-5, TutorialWorld.SurfaceZ(-5, [(-5, water, 0)]));                  // static water is no surface
        Assert.Equal(3, TutorialWorld.SurfaceZ(3, []));                                  // bare land"""),
    ("""

    // The real check: on the host's map (stock Trammel's file, void at site A) the isle is not ready.
    [Fact]
    public void OnAMapWithoutTheIslesPatchTheIsleIsNotReady()
    {
        Assert.False(_isleReady());
    }""", ""),
])
