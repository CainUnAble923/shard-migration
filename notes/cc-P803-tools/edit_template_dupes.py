"""cc-P803 fix-up: the fact template gets each town's own old spots (@@OLDSPOTS@@), a duplicate fact, and on the release a
fact that main's old spot is another building there (@@FOREIGN@@). make_facts.py fills them in.
   python -P notes/cc-P803-tools/edit_template_dupes.py"""
import os

here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "LeagueOfficeDecorVerification.cs.template")
s = open(p, encoding="utf-8").read()

old = """    [InlineData(3459, 2596, 18)]
    [InlineData(3662, 2547, 0)]
"""
assert old in s
s = s.replace(old, "@@OLDSPOTS@@")

old = """//   2. A League board left on an old spot moves to the wall on the next seed, the same item (serial), and a second seed
//      changes nothing.
"""
new = """//   2. A League board left on an old spot moves to the wall on the next seed, the same item (serial), and a second seed
//      changes nothing. A second League board on an old spot, when the wall already has one, is removed, so the office
//      never shows two (the after run of 11-07 found two: the bot world is a main world, and the release had listed main's
//      old spot as its own, moved that board across town and left its own in the doorway). Only this town's own old spots
//      count: a board in another building is left alone.
"""
assert old in s
s = s.replace(old, new)

marker = "    // ---------------------------------------------------------------- 3\n"
assert marker in s
dupes = '''    [Fact]
    public void ASecondBoardOnAnOldSpotIsRemovedSoTheOfficeShowsOne()
    {
        var spots = ClusterFRequisitionSeeder.OldOfficeBoardSpots;
        var made = ClearBoards(spots[^1].X, spots[^1].Y);
        var appraisers = Appraisers();
        var extra = new List<RequisitionsBoard>();
        try
        {
            ClusterFRequisitionSeeder.Seed(false);
            var hung = Assert.Single(LeagueBoardsNear());
            foreach (var p in spots)
            {
                var b = new RequisitionsBoard();
                b.MoveToWorld(p, Map.Trammel);
                extra.Add(b);
            }

            ClusterFRequisitionSeeder.Seed(false);
            Assert.All(extra, b => Assert.True(b.Deleted));
            Assert.False(hung.Deleted);
            Assert.Equal(BoardSpot, hung.Location);
            Assert.Single(LeagueBoardsNear());

            // With the wall empty, two old boards leave one board, on the wall.
            hung.Delete();
            extra.Clear();
            foreach (var p in spots.Concat(spots))
            {
                var b = new RequisitionsBoard();
                b.MoveToWorld(p, Map.Trammel);
                extra.Add(b);
            }

            ClusterFRequisitionSeeder.Seed(false);
            var one = Assert.Single(LeagueBoardsNear());
            Assert.Equal(BoardSpot, one.Location);
            Assert.Equal(extra.Count - 1, extra.Count(b => b.Deleted));
            Assert.Null(ClusterFRequisitionSeeder.MoveOldOfficeBoard(Map.Trammel));
        }
        finally
        {
            foreach (var b in extra)
            {
                b.Delete();
            }

            ClearBoards(spots[^1].X, spots[^1].Y);
            Restore(made);
            DeleteNewAppraisers(appraisers);
        }
    }
@@FOREIGN@@
'''
s = s.replace(marker, dupes + "\n" + marker)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("edited", p)

m = os.path.join(here, "make_facts.py")
t = open(m, encoding="utf-8").read()
foreign = '''
    [Fact]
    public void ABoardInSoSHavensHallIsAnotherBuildingHereAndIsLeftAlone()
    {
        var at = new Point3D(3662, 2547, 0);
        Assert.DoesNotContain(ClusterFRequisitionSeeder.OldOfficeBoardSpots, p => p.X == at.X && p.Y == at.Y);
        var made = ClearBoards(at.X, at.Y);
        var appraisers = Appraisers();
        var other = new RequisitionsBoard();
        try
        {
            other.MoveToWorld(at, Map.Trammel);
            ClusterFRequisitionSeeder.Seed(false);
            Assert.False(other.Deleted);
            Assert.Equal(at, other.Location);
            var one = Assert.Single(LeagueBoardsNear());
            Assert.Equal(BoardSpot, one.Location);
        }
        finally
        {
            other.Delete();
            ClearBoards(at.X, at.Y);
            Restore(made);
            DeleteNewAppraisers(appraisers);
        }
    }
'''
old = '''             ROOMS="(3457, 2596, 3458, 2597, 3461, 2602), (3453, 2596, 3454, 2597, 3456, 2602)")'''
assert old in t
t = t.replace(old, '''             ROOMS="(3457, 2596, 3458, 2597, 3461, 2602), (3453, 2596, 3454, 2597, 3456, 2602)",
             OLDSPOTS="    [InlineData(3459, 2596, 18)]\\n", FOREIGN=FOREIGN)''')
old = '''             ROOMS="(3658, 2547, 3659, 2548, 3673, 2561)")'''
assert old in t
t = t.replace(old, '''             ROOMS="(3658, 2547, 3659, 2548, 3673, 2561)",
             OLDSPOTS="    [InlineData(3459, 2596, 18)]\\n    [InlineData(3662, 2547, 0)]\\n", FOREIGN="")''')
t = t.replace('P = lambda pts:', 'FOREIGN = open(os.path.join(here, "foreign-fact.cs.part")).read()\nP = lambda pts:')
open(m, "w", encoding="utf-8", newline="\n").write(t)
open(os.path.join(here, "foreign-fact.cs.part"), "w", encoding="utf-8", newline="\n").write(foreign)
print("edited", m)
