def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


C = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/"
T = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Tutorial/"

edit(C + "TutorialGreeting.cs", [
("""        _said[key] = Core.TickCount;
        npc.SayTo(pm, line);
        return true;""", """        _said[key] = Core.TickCount;
        npc.SayTo(pm, line);
        Greeted?.Invoke(npc, pm);
        return true;"""),
("""    /// <summary>Forgets every greeting by""", """    /// <summary>Raised after each greeting (tests count them, whichever path spoke: approach, think or a call).</summary>
    public static event Action<Mobile, PlayerMobile>? Greeted;

    /// <summary>Forgets every greeting by"""),
])

p = T + "TutorialIsleWalkFixesVerification.cs"
s = open(p, encoding="utf-8").read()
start = s.index("    [Fact]\n    public void TamsinGreetsANewTraineeNoFasterThanTheIntervalAndStopsOnceUsed()")
end = s.index("    [Fact]\n    public void WrenGreetsATraineeWhoseNextLessonIsTheFarmUntilThePetIsChosen()")
new_fact = """    [Fact]
    public void TamsinGreetsANewTraineeNoFasterThanTheIntervalAndStopsOnceUsed()
    {
        using var p = new Player();
        TutorialTestStart.Begin(p.Pm);
        var tamsin = p.Add(new TutorialGuide());

        // Every greeting by her to this trainee is counted, by whichever path spoke: her approach hook, her AI think
        // (which also runs while the clock advances) or the call here.
        var said = 0;
        void Count(Mobile npc, PlayerMobile pm)
        {
            if (npc == tamsin && pm == p.Pm)
            {
                said++;
            }
        }

        TutorialGreeting.Greeted += Count;
        try
        {
            Assert.True(TutorialGreeting.NeedsGuide(p.Pm));
            tamsin.MoveToWorld(Beside(p.Pm, 2), p.Pm.Map);
            TutorialGreeting.GreetAround(tamsin, TutorialGreeting.NeedsGuide, TutorialGreeting.TamsinLine);
            Assert.Equal(1, said); // on approach, once
            Assert.Contains("Double-click me", TutorialGreeting.TamsinLine);

            // Not again within the interval, however often she is asked.
            ShardTestClock.Advance(TutorialGreeting.Interval - TimeSpan.FromSeconds(1));
            TutorialGreeting.GreetAround(tamsin, TutorialGreeting.NeedsGuide, TutorialGreeting.TamsinLine);
            Assert.Equal(1, said);

            // Again once it has passed, while the trainee stays near and has not used her.
            ShardTestClock.Advance(TimeSpan.FromSeconds(2));
            TutorialGreeting.GreetAround(tamsin, TutorialGreeting.NeedsGuide, TutorialGreeting.TamsinLine);
            Assert.Equal(2, said);

            // Out of range: nothing.
            tamsin.MoveToWorld(Beside(p.Pm, TutorialGreeting.Range + 3), p.Pm.Map);
            ShardTestClock.Advance(TutorialGreeting.Interval + TimeSpan.FromSeconds(1));
            TutorialGreeting.GreetAround(tamsin, TutorialGreeting.NeedsGuide, TutorialGreeting.TamsinLine);
            Assert.Equal(2, said);

            // Used: the prompt stops.
            tamsin.MoveToWorld(Beside(p.Pm, 1), p.Pm.Map);
            tamsin.OnDoubleClick(p.Pm);
            Assert.False(TutorialGreeting.NeedsGuide(p.Pm));
            var before = said;
            ShardTestClock.Advance(TutorialGreeting.Interval + TimeSpan.FromSeconds(1));
            TutorialGreeting.GreetAround(tamsin, TutorialGreeting.NeedsGuide, TutorialGreeting.TamsinLine);
            Assert.Equal(before, said);
        }
        finally
        {
            TutorialGreeting.Greeted -= Count;
        }
    }

"""
s = s[:start] + new_fact + s[end:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
