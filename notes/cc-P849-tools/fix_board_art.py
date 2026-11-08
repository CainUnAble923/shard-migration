"""cc-P849 (P836's build review of P827): turn the League requisitions board's art the right way in one code copy.

A render of both arts against both walls (board_walls.py, notes/cc-P849-review/board-arts-on-walls.jpg) shows 0x1E5E hangs
flat on a NORTH wall (its frame runs east-west) and 0x1E5F on a WEST wall (north-south). P803 had them swapped. This sets
OfficeBoardItemID to the art for the wall the copy's board hangs on, fixes the facts' wall-to-art mapping and adds the
facts that pin it, in Appraiser.cs and LeagueOfficeDecorVerification.cs.

    python -I notes/cc-P849-tools/fix_board_art.py <code copy> north|west
"""
import os
import re
import sys

code, wall = sys.argv[1], sys.argv[2]
art = {'north': '0x1E5E', 'west': '0x1E5F'}[wall]
old_art = {'north': '0x1E5F', 'west': '0x1E5E'}[wall]

p = os.path.join(code, 'server/customizations/Requisitions/Appraiser.cs')
s = open(p, encoding='utf-8').read()
s, n = re.subn(r'public const int OfficeBoardItemID = 0x1E5[EF];', 'public const int OfficeBoardItemID = %s;' % art, s)
assert n == 1, 'OfficeBoardItemID not found'
s, n = re.subn(r'/// <summary>cc-P803: the board.s art for its wall: [^<]*</summary>',
               "/// <summary>cc-P849: the board's art for its wall: 0x1E5E hangs flat on a north wall (its frame runs east-west), "
               "0x1E5F on a west wall (north-south). P803 had them swapped, so the board stood edge-on (P836's build review; "
               "render notes/cc-P849-review/board-arts-on-walls.jpg).</summary>", s)
assert n == 1, 'summary not found'
old = '                    board.ItemID = OfficeBoardItemID; // cc-P803: the art that hangs on its wall\n'
new = ('                    var was = board.ItemID;\n'
       '                    board.ItemID = OfficeBoardItemID; // cc-P803: the art that hangs on its wall (cc-P849: the right one now)\n'
       '                    report.Add($"League board: art turned from 0x{was:X4} to 0x{OfficeBoardItemID:X4} at {board.Location}.");\n')
if old in s:
    s = s.replace(old, new, 1)
else:
    assert 'art turned from' in s, 'retag line not found'
open(p, 'w', encoding='utf-8', newline='').write(s)

p = os.path.join(code, 'server/tests/Misc/LeagueOfficeDecorVerification.cs')
s = open(p, encoding='utf-8').read()
s, n = re.subn(r'private const int BoardArt = 0x1E5[EF];', 'private const int BoardArt = %s;' % art, s)
assert n == 1, 'BoardArt not found'
s = s.replace('(0x1E5E on a west\n//      wall, 0x1E5F on a north wall: both rendered against a wall, notes/cc-P803-review/board-facings.png)',
              '(0x1E5E on a north\n//      wall, 0x1E5F on a west wall: cc-P849 rendered both against both walls, notes/cc-P849-review/board-arts-on-walls.jpg;\n'
              '//      P803 had them swapped)')
old = 'Assert.True(BoardArt == 0x1E5E ? post.X == room.WestX + 1 : post.Y == room.NorthY + 1);'
assert old in s, 'room mapping not found'
s = s.replace(old, 'Assert.True(BoardArt == NorthWallBoard ? post.Y == room.NorthY + 1 : post.X == room.WestX + 1);')
old = 'Point2D[] beside = BoardArt == 0x1E5E\n'
assert old in s, 'beside mapping not found'
s = s.replace(old, 'Point2D[] beside = BoardArt == WestWallBoard\n')
s = s.replace('    private const int BoardArt = %s;\n' % art,
              '    private const int BoardArt = %s;\n\n'
              '    // cc-P849: the art that hangs flat on each wall (render notes/cc-P849-review/board-arts-on-walls.jpg).\n'
              '    private const int NorthWallBoard = 0x1E5E; // frame runs east-west, faces south\n'
              '    private const int WestWallBoard = 0x1E5F;  // frame runs north-south, faces east\n' % art, 1)
facts = '''
    // ---------------------------------------------------------------- 9 (cc-P849, P836's build review)

    [Fact]
    public void TheBoardsArtIsTheOneThatHangsFlatOnItsWall()
    {
        var post = ClusterFRequisitionSeeder.OfficeBoard;
        var room = Rooms.Single(r => post.X >= r.X1 && post.X <= r.X2 && post.Y >= r.Y1 && post.Y <= r.Y2);
        var onNorth = post.Y == room.NorthY + 1;
        var onWest = post.X == room.WestX + 1;
        Assert.True(onNorth ^ onWest, "the board stands in front of exactly one wall");
        var want = onNorth ? NorthWallBoard : WestWallBoard;
        var art = ClusterFRequisitionSeeder.OfficeBoardItemID;
        Assert.True(art == want, $"the board art 0x{art:X4} stands edge-on on its {(onNorth ? "north" : "west")} wall; 0x{want:X4} hangs flat there");
    }

    [Fact]
    public void ABoardWithTheEdgeOnArtIsTurnedOnLoadOnceAndStaysTheSameItem()
    {
        var made = ClearBoards();
        var appraisers = Appraisers();
        var wrong = ClusterFRequisitionSeeder.OfficeBoardItemID == NorthWallBoard ? WestWallBoard : NorthWallBoard;
        var board = new RequisitionsBoard { ItemID = wrong };
        try
        {
            board.MoveToWorld(BoardSpot, Map.Trammel);
            var serial = board.Serial;
            var first = ClusterFRequisitionSeeder.Seed(false);
            Assert.False(board.Deleted);
            Assert.Equal(serial, board.Serial);
            Assert.Equal(BoardArt, board.ItemID);
            Assert.Contains(first, l => l.Contains("art turned from"));

            var second = ClusterFRequisitionSeeder.Seed(false);
            Assert.DoesNotContain(second, l => l.Contains("art turned from"));
            Assert.Equal(BoardArt, Assert.Single(LeagueBoardsNear()).ItemID);
        }
        finally
        {
            ClearBoards();
            Restore(made);
            DeleteNewAppraisers(appraisers);
        }
    }
'''
if 'TheBoardsArtIsTheOneThatHangsFlatOnItsWall' not in s:
    i = s.index('    private static List<RequisitionsBoard> LeagueBoardsNear()')
    s = s[:i] + facts.lstrip('\n') + '\n' + s[i:]
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok', code, wall, art)
