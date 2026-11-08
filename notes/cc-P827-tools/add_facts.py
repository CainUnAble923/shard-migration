"""cc-P827: P824's build-review fixes in LeagueOfficeDecorVerification.cs of one copy (main or the isle release copy).

    python -P notes/cc-P827-tools/add_facts.py main    D:/UO/golems/Iron/ShatteredLegacy
    python -P notes/cc-P827-tools/add_facts.py release D:/UO/golems/Iron/p803-isle

Moves the board's spot and adds two facts: the board has its stretch of wall to itself (no layout piece and none of the
map's own wall-hung or tall pieces on the tile each side of it along its wall, P824 items 1 and 4), and the sign hangs or
stands where the guide wants it (main: the arm from a plain south-wall piece, clear of the windows and the arch, item 3;
release: the signpost north of the road, off the door's line, item 2). The map pieces are read with
notes/cc-P803-tools/office_statics.py (client-data-copy for the release, p735-work/patched for main).
"""
import sys

which, root = sys.argv[1], sys.argv[2]
path = root + "/server/tests/Misc/LeagueOfficeDecorVerification.cs"
s = open(path, "rb").read().decode("utf-8")
assert "cc-P827" not in s, "already applied"

if which == "main":
    old_spot, new_spot = "new(3662, 2548, 0)", "new(3663, 2548, 0)"
    pieces = ("    // The map's own pieces on the north wall's floor row (bookcases, flowerpots, the fish trophy).\n"
              "    private static readonly Point2D[] MapWallPieces = [new(3665, 2548), new(3666, 2548), new(3667, 2548), "
              "new(3668, 2548), new(3669, 2548), new(3671, 2548)];\n")
    sign_fact = '''
    // The south wall's row and the arch's east tile (the hall's open doorway, 3667-3668,2562).
    private const int SouthWallY = 2562;
    private const int ArchEastX = 3668;

    [Fact]
    public void TheSignArmHangsFromAPlainWallClearOfTheWindowsAndTheArch()
    {
        // P824 item 3: at 3670 the arm and board hung on the stained-glass window 3670,2562. The arm hangs from the wall
        // north of its tile (guide 11.12), so that wall piece must be a plain one, and the sign stands two or more tiles
        // east of the arch (guide 2.5).
        var arm = Assert.Single(ClusterFRegistrarOfficeLayout.Outside, c => c.ItemID == 0x0B98);
        var board = Assert.Single(ClusterFRegistrarOfficeLayout.Outside, c => c.ItemID == 0x0BCF);
        Assert.Equal((arm.X, arm.Y), (board.X, board.Y));
        Assert.Equal(SouthWallY + 1, arm.Y);
        Assert.DoesNotContain(WindowFloor, w => w.X == arm.X); // the south wall's windows, by x
        Assert.True(arm.X - ArchEastX >= 2, $"the sign at {arm.X} is too close to the arch");
    }
'''
else:
    old_spot, new_spot = "new(3458, 2598, 18)", "new(3458, 2602, 18)"
    pieces = ("    // The map's own wall-hung piece on the office's west wall (the stretched hide in the north-west corner).\n"
              "    private static readonly Point2D[] MapWallPieces = [new(3458, 2597)];\n")
    sign_fact = '''
    // The road in front of the house runs along y 2592-2595; the front door is 3459,2596 (north wall).
    private const int RoadNorthY = 2592;
    private const int DoorX = 3459;

    [Fact]
    public void TheSignpostStandsNorthOfTheRoadOffTheDoorsLine()
    {
        // P824 item 2: at 3463,2596 the signpost stood south of the road with its back to the street. Every sign stands
        // north of its path, facing it (guide 6; 0xA854 reads from the south), so on the verge just north of the road,
        // and off the door's approach line.
        var post = Assert.Single(ClusterFRegistrarOfficeLayout.Outside, c => c.ItemID == 0xA854);
        Assert.Equal(RoadNorthY - 1, post.Y);
        Assert.NotEqual(DoorX, post.X);
        Assert.Equal("signpost", post.Name);
    }
'''

assert old_spot in s
s = s.replace("private static readonly Point3D BoardSpot = " + old_spot,
              "private static readonly Point3D BoardSpot = " + new_spot)

header_old = "//   5. On load, an office decor that is not the current layout is swapped for it; a current one, or one standing in\n" \
             "//      another building, is left alone; and running it again changes nothing.\n"
header_new = header_old + (
    "//   6. cc-P827 (P824's build review): the board has its stretch of wall to itself, no office piece and none of the\n"
    "//      map's own wall pieces on the tile each side of it along its wall (its art drew over the map's hide on the\n"
    "//      release and over a bookcase on main); and the sign hangs or stands where the building guide wants it.\n")
assert header_old in s
s = s.replace(header_old, header_new)

facts = '''    // ---------------------------------------------------------------- 6 (cc-P827)

''' + pieces + '''
    [Fact]
    public void TheBoardHasItsStretchOfWallToItself()
    {
        var post = ClusterFRequisitionSeeder.OfficeBoard;

        // Along a west wall the board's neighbours are the tiles north and south of it; along a north wall, west and east.
        Point2D[] beside = BoardArt == 0x1E5E
            ? [new(post.X, post.Y - 1), new(post.X, post.Y + 1)]
            : [new(post.X - 1, post.Y), new(post.X + 1, post.Y)];

        var crowded = ClusterFRegistrarOfficeLayout.Components
            .Where(c => beside.Any(b => b.X == c.X && b.Y == c.Y))
            .Select(c => $"0x{c.ItemID:X4} {c.Name} at {c.X},{c.Y}")
            .Concat(MapWallPieces.Where(m => beside.Any(b => b.X == m.X && b.Y == m.Y)).Select(m => $"map piece at {m.X},{m.Y}"))
            .ToList();
        _out.WriteLine(string.Join("\\n", crowded));
        Assert.Empty(crowded);
    }
''' + sign_fact + '''
    // ---------------------------------------------------------------- helpers
'''
anchor = "    // ---------------------------------------------------------------- helpers\n"
assert anchor in s
s = s.replace(anchor, facts, 1)
open(path, "wb").write(s.encode("utf-8"))
print(path, "updated")
