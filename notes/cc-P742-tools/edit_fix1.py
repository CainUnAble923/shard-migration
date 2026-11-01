"""cc-P742 (after probe 1): slots 28 apart, so the next room's nearest wall is more than a client's 18 tiles from the
onlooker (at 24 it was exactly 18); the Gem's height on the pedestal falls back to the pedestal's tiledata height (9)
where no tiledata is loaded (the test host read 0); the fact about spacing says what it means.
Usage: python -P edit_fix1.py <code copy>"""
import sys

root = sys.argv[1]


def edit(path, pairs):
    p = root + path
    s = open(p, encoding="utf-8", newline="").read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, s.count(a), a[:90])
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)
    print("edited", p)


edit("/server/customizations/Tutorial/TutorialVisionChamber.cs", [
    ('''    /// <summary>Tiles between slots: more than a client's view (18) plus the room (9).</summary>
    public const int Spacing = 24;

    /// <summary>Slots on one map: x 6170 to 6554, all west of the isle (6594) and of its sea.</summary>
    public const int Slots = 17;''',
     '''    /// <summary>Tiles between slots: the next room's nearest wall is 22 tiles from the onlooker, past a client's view (18).</summary>
    public const int Spacing = 28;

    /// <summary>Slots on one map: corners x 6170 to 6562, rooms ending by x 6570, all west of the isle (6594).</summary>
    public const int Slots = 15;

    /// <summary>The pedestal's height (tiledata 0x1223), where the server has no tiledata loaded (the test host).</summary>
    public const int PedestalHeight = 9;'''),
    ('''// How: the room is placed per scene from TutorialVisionChamberLayout (114 pieces, all TutorialVisionProp, never kept by
// a save) when the vision starts, and taken away when it ends. One slot per scene on a map, 24 tiles apart so no two
// scenes are in each other's view (18 tiles): on a private copy that is always slot 0; on the shared Fold the first free
// slot.''', '''// How: the room is placed per scene from TutorialVisionChamberLayout (114 pieces, all TutorialVisionProp, never kept by
// a save) when the vision starts, and taken away when it ends. One slot per scene on a map, 28 tiles apart so no two
// scenes are in each other's view (18 tiles): on a private copy that is always slot 0; on the shared Fold the first free
// slot.'''),
])
edit("/server/customizations/Tutorial/TutorialVisionScene.cs", [
    ('''                var top = s.Pedestal is { } pedestal
                    ? new Point3D(pedestal.X, pedestal.Y, pedestal.Z + TileData.ItemTable[PedestalId].CalcHeight)
                    : C(s, TutorialVisionChamber.Pedestal);''',
     '''                var height = TileData.ItemTable[PedestalId].CalcHeight;
                var top = s.Pedestal is { } pedestal
                    ? new Point3D(pedestal.X, pedestal.Y, pedestal.Z + (height > 0 ? height : TutorialVisionChamber.PedestalHeight))
                    : C(s, TutorialVisionChamber.Pedestal);'''),
])
edit("/server/tests/Tutorial/TutorialVisionChamberVerification.cs", [
    ('''        Assert.True(TutorialVisionChamber.Spacing >= 18 + TutorialVisionChamber.Size);''',
     '''        // the next room's nearest piece, east or west, is out of the onlooker's view (a client sees 18 tiles)
        var o = TutorialVisionChamber.Onlooker;
        Assert.True(TutorialVisionChamber.Spacing - o.X > 18);
        Assert.True(TutorialVisionChamber.Spacing - (TutorialVisionChamber.Size - 1) + o.X > 18);
        Assert.True(TutorialVisionChamber.Corner(TutorialVisionChamber.Slots - 1).X + TutorialVisionChamber.Size <= TutorialWorld.Area.X);'''),
])
