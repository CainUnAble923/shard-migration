"""cc-P803 fix-up (after run, 11-07): the release after shots found two League boards in the office. The bot world is a main
world, so it holds main's board at 3662,2547 as well; the release listed main's old spot too, and MoveOldOfficeBoard moved
the first board it found (main's, across town) and stopped, leaving the release's own board in the doorway.
Now: each copy lists only the old spots its own town ever used (release: the ML house door; main: both, since main's
New Haven was the ML town before P678), and every League board on an old spot is handled: the first moves to the wall
when the wall has none, and any other is a duplicate and is deleted (a League board holds no state: no guild key).
   python -P notes/cc-P803-tools/edit_board_dupes.py <release|main> <root>"""
import sys

which, root = sys.argv[1], sys.argv[2]
p = root + "/server/customizations/Requisitions/Appraiser.cs"
s = open(p, encoding="utf-8").read()

if which == "release":
    old = """    /// <summary>cc-P803: where earlier layouts stood the board, in a wall's line (the old New Haven house's front door; SoS
    /// Haven's hall north wall). A League board found on one of these tiles moves to OfficeBoard on load, the same item.</summary>
    public static readonly Point3D[] OldOfficeBoardSpots = [new(3459, 2596, 18), new(3662, 2547, 0)];"""
    new = """    /// <summary>cc-P803: where earlier layouts stood the board, in a wall's line (this house's front door). A League board
    /// found here moves to OfficeBoard on load, the same item. Only this town's own old spot: SoS Haven's hall (main's
    /// old spot, 3662,2547) is another building here, and a board there is left alone.</summary>
    public static readonly Point3D[] OldOfficeBoardSpots = [new(3459, 2596, 18)];"""
    assert old in s, "release spots"
    s = s.replace(old, new)

old_fn_start = s.index("    /// <summary>\n    /// cc-P803: a League board standing on one of OldOfficeBoardSpots")
old_fn_end = s.index("    private static Map MapOf(int index)")
new_fn = '''    /// <summary>
    /// cc-P803: League boards standing on OldOfficeBoardSpots (an earlier layout put the board in a wall's line). The first
    /// moves to OfficeBoard and takes OfficeBoardItemID, the same item, when no League board hangs there yet; any other is
    /// a duplicate and is deleted (a League board holds no state). Returns the report line, or null when there was nothing
    /// on an old spot. Idempotent: afterwards no League board stands on an old spot.
    /// </summary>
    public static string MoveOldOfficeBoard(Map map)
    {
        var olds = new List<RequisitionsBoard>();
        RequisitionsBoard onWall = null;
        foreach (var i in World.Items.Values)
        {
            if (i is not RequisitionsBoard b || b.Deleted || !b.IsLeagueBoard || b.Map != map)
            {
                continue;
            }

            if (Array.Exists(OldOfficeBoardSpots, p => p.X == b.X && p.Y == b.Y && p.Z == b.Z))
            {
                olds.Add(b);
            }
            else if (b.X == OfficeBoard.X && b.Y == OfficeBoard.Y)
            {
                onWall = b;
            }
        }

        if (olds.Count == 0)
        {
            return null;
        }

        var lines = new List<string>();
        foreach (var old in olds)
        {
            var from = old.Location;
            if (onWall == null)
            {
                old.ItemID = OfficeBoardItemID;
                old.MoveToWorld(new Point3D(OfficeBoard.X, OfficeBoard.Y, OfficeBoard.Z), map);
                onWall = old;
                lines.Add($"League board: moved from {from} to {old.Location} ({OfficeBoard.Where}).");
            }
            else
            {
                old.Delete();
                lines.Add($"League board: a second one at {from} removed; the office's board is at {onWall.Location}.");
            }
        }

        return string.Join(" ", lines);
    }

'''
s = s[:old_fn_start] + new_fn + s[old_fn_end:]
if "using System.Collections.Generic;" not in s:
    assert "List<string>" in s  # Seed already uses List<string>, so the using (or a global one) is there
open(p, "w", encoding="utf-8", newline="").write(s)
print("edited", p)
