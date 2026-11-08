"""cc-P803: the League board's spot and art in Appraiser.cs (ClusterFRequisitionSeeder) of one copy.
    python -P notes/cc-P803-tools/edit_board.py <release|main> <root>"""
import sys
which, root = sys.argv[1], sys.argv[2]
p = root + "/server/customizations/Requisitions/Appraiser.cs"
s = open(p, encoding="utf-8").read()
nl = "\r\n" if "\r\n" in s else "\n"
s = s.replace("\r\n", "\n")
if which == "main":
    old = s[s.index("    // cc-P678: the office moved into SoS Haven's hall"):s.index("\n", s.index("public static readonly Post OfficeBoard")) + 1]
    new = '''    // cc-P678: the office moved into SoS Haven's hall (walls x3658-3674, y2547-2562, floor z0).
    // cc-P803: the board stood ON the north wall's tile (3662,2547), in the wall line, with the art that hangs on a west
    // wall (0x1E5E), so it showed edge-on from the wrong side. It hangs on the floor tile in front of the wall now, between
    // the bookcases and the flowerpot, with the north-wall art 0x1E5F (both rendered against a wall: notes/cc-P803-review).
    public static readonly Post OfficeBoard = new("New Haven", "League field office, north wall", 1, 3662, 2548, 0, Direction.North, true);

    /// <summary>cc-P803: the board's art for its wall: 0x1E5F hangs on a north wall, 0x1E5E on a west wall.</summary>
    public const int OfficeBoardItemID = 0x1E5F;
'''
else:
    old = s[s.index("    /// <summary>The League board in the field office: on the north wall"):s.index("\n", s.index("public static readonly Post OfficeBoard")) + 1]
    new = '''    /// <summary>The League board in the field office.</summary>
    // cc-P803: it stood on the front door's own tile (3459,2596,18), in the north wall's line, where the door and its frame
    // drew over it, and its art (0x1E5E) hangs on a west wall, not a north one. It hangs on the office's west wall now,
    // the wall beside the way in (the dividing wall, x3457), on the floor tile 3458,2598 north of the doorway's approach,
    // where 0x1E5E faces into the room (rendered against a wall: notes/cc-P803-review).
    public static readonly Post OfficeBoard = new("New Haven", "League field office, west wall", 1, 3458, 2598, 18, Direction.East, true);

    /// <summary>cc-P803: the board's art for its wall: 0x1E5E hangs on a west wall, 0x1E5F on a north wall.</summary>
    public const int OfficeBoardItemID = 0x1E5E;
'''
new += '''
    /// <summary>cc-P803: where earlier layouts stood the board, in a wall's line (the old New Haven house's front door; SoS
    /// Haven's hall north wall). A League board found on one of these tiles moves to OfficeBoard on load, the same item.</summary>
    public static readonly Point3D[] OldOfficeBoardSpots = [new(3459, 2596, 18), new(3662, 2547, 0)];
'''
assert s.count(old) == 1
s = s.replace(old, new)

old2 = '''            if (FindItem<RequisitionsBoard>(officeMap, OfficeBoard.X, OfficeBoard.Y, 5) is { } board)
            {
                present++;
                if (verbose) report.Add($"League board: already at {board.Location}.");
            }
            else
            {
                var item = new RequisitionsBoard();
                item.MoveToWorld(new Point3D(OfficeBoard.X, OfficeBoard.Y, OfficeBoard.Z), officeMap);'''
new2 = '''            if (MoveOldOfficeBoard(officeMap) is { } moved)
            {
                report.Add(moved);
            }

            if (FindItem<RequisitionsBoard>(officeMap, OfficeBoard.X, OfficeBoard.Y, 5) is { } board)
            {
                present++;
                if (board.IsLeagueBoard && board.ItemID != OfficeBoardItemID && board.X == OfficeBoard.X && board.Y == OfficeBoard.Y)
                {
                    board.ItemID = OfficeBoardItemID; // cc-P803: the art that hangs on its wall
                }

                if (verbose) report.Add($"League board: already at {board.Location}.");
            }
            else
            {
                var item = new RequisitionsBoard { ItemID = OfficeBoardItemID };
                item.MoveToWorld(new Point3D(OfficeBoard.X, OfficeBoard.Y, OfficeBoard.Z), officeMap);'''
assert s.count(old2) == 1
s = s.replace(old2, new2)

old3 = '''    private static Map MapOf(int index) =>'''
new3 = '''    /// <summary>
    /// cc-P803: a League board standing on one of OldOfficeBoardSpots (an earlier layout put it in a wall's line) moves to
    /// OfficeBoard and takes OfficeBoardItemID. Same item, so nothing a player holds changes. Returns the report line, or
    /// null when there was nothing to move. Idempotent: a moved board is no longer on an old spot.
    /// </summary>
    public static string MoveOldOfficeBoard(Map map)
    {
        RequisitionsBoard old = null;
        foreach (var i in World.Items.Values)
        {
            if (i is RequisitionsBoard b && !b.Deleted && b.IsLeagueBoard && b.Map == map &&
                Array.Exists(OldOfficeBoardSpots, p => p.X == b.X && p.Y == b.Y && p.Z == b.Z))
            {
                old = b;
                break;
            }
        }

        if (old == null)
        {
            return null;
        }

        var from = old.Location;
        old.ItemID = OfficeBoardItemID;
        old.MoveToWorld(new Point3D(OfficeBoard.X, OfficeBoard.Y, OfficeBoard.Z), map);
        return $"League board: moved from {from} to {old.Location} ({OfficeBoard.Where}).";
    }

    private static Map MapOf(int index) =>'''
assert s.count(old3) == 1
s = s.replace(old3, new3)
open(p, "w", encoding="utf-8", newline=nl).write(s)
print("ok", p)
