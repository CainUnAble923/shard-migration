"""cc-P742: P721's vision fact (TutorialIsleBandageWaitVerification.TheVisionIsLitWalksUpStrikesTheGemAndRunsLonger)
measured the Stranger from where the player stood and counted the braziers among the scene's props. In the chamber the
braziers are part of the room and the Stranger walks from the chamber's corner, so the fact reads the chamber's spots.
What it checks is unchanged: lit from the second beat, two braziers, the Stranger at a distance, then beside the Gem
facing it, the strike, the Gem whole until later, 61 s.
Usage: python -P edit_tests.py <code copy>"""
import sys

p = sys.argv[1] + "/server/tests/Tutorial/TutorialIsleBandageWaitVerification.cs"
s = open(p, encoding="utf-8", newline="").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100])
    s = s.replace(a, b)


rep('''        var origin = TutorialVisionScene.Current(p.Pm)!.Origin;

        ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Beats.Lights + 0.5));
        Assert.Equal(TutorialVisionScene.Lit, TutorialVisionScene.LightOf(p.Pm));
        var scene = TutorialVisionScene.Current(p.Pm)!;
        Assert.Equal(2, scene.Placed.OfType<Item>().Count(i => i.ItemID == TutorialVisionScene.BrazierId));
        var stranger = scene.Stranger!;
        Assert.Equal(origin.X + 6, stranger.X); // at a distance

        ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Beats.Face - TutorialVisionScene.Beats.Lights));
        Assert.Equal(origin.X + 3, stranger.X); // walked up beside the Gem
        Assert.Equal(Direction.Up, stranger.Direction & Direction.Mask); // facing it''',
'''        ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Beats.Lights + 0.5));
        Assert.Equal(TutorialVisionScene.Lit, TutorialVisionScene.LightOf(p.Pm));
        var scene = TutorialVisionScene.Current(p.Pm)!;
        // cc-P742: the braziers are the chamber's, and the Stranger walks from its corner
        Assert.Equal(2, scene.Chamber.Count(i => i.ItemID == TutorialVisionScene.BrazierId));
        var stranger = scene.Stranger!;
        var pedestal = scene.Pedestal!;
        Assert.True(stranger.GetDistanceToSqrt(pedestal) > 4); // at a distance

        ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Beats.Face - TutorialVisionScene.Beats.Lights));
        Assert.True(stranger.InRange(pedestal.Location, 1)); // walked up beside the Gem
        Assert.Equal(Direction.Down, stranger.Direction & Direction.Mask); // facing it (south-east of him)''')
open(p, "w", encoding="utf-8", newline="").write(s)
print("edited", p)
