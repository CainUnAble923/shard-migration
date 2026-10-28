def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


C = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/"
T = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Tutorial/"

edit(C + "TutorialGreeting.cs", [
("""    // When each NPC last greeted each player (in memory: a restart greets again, which is harmless).
    private static readonly Dictionary<(Serial Npc, Serial Player), DateTime> _said = new();""",
 """    // When each NPC last greeted each player, in Core.TickCount milliseconds (in memory: a restart greets again, which is
    // harmless). The tick count, not Core.Now: a test host's NetState resets Core.Now to the wall clock as it sends (D16).
    private static readonly Dictionary<(Serial Npc, Serial Player), long> _said = new();"""),
("""        if (_said.TryGetValue(key, out var at) && Core.Now - at < Interval)
        {
            return false;
        }

        npc.SayTo(pm, line);
        _said[key] = Core.Now; // after the line: a test host's NetState sets Core.Now as it sends (D16)
        return true;""", """        if (_said.TryGetValue(key, out var at) && Core.TickCount - at < (long)Interval.TotalMilliseconds)
        {
            return false;
        }

        _said[key] = Core.TickCount;
        npc.SayTo(pm, line);
        return true;"""),
])

edit(C + "TutorialSkillPace.cs", [
("""    // When each player last gained each skill on the isle (in memory).
    private static readonly Dictionary<(Serial Player, SkillName Skill), DateTime> _last = new();""",
 """    // When each player last gained each skill on the isle, in Core.TickCount milliseconds (in memory).
    private static readonly Dictionary<(Serial Player, SkillName Skill), long> _last = new();"""),
("""        !Applies(m) || !_last.TryGetValue((m.Serial, skill.SkillName), out var at) || Core.Now - at >= Interval;""",
 """        !Applies(m) || !_last.TryGetValue((m.Serial, skill.SkillName), out var at) ||
        Core.TickCount - at >= (long)Interval.TotalMilliseconds;"""),
("""            _last[(m.Serial, skill.SkillName)] = Core.Now;""", """            _last[(m.Serial, skill.SkillName)] = Core.TickCount;"""),
])

edit(T + "TutorialIsleWalkFixesVerification.cs", [
("""        Assert.True(TutorialGreeting.NeedsGuide(p.Pm));
        var seen = new List<string>();
        foreach (var m in tamsin.GetMobilesInRange(TutorialGreeting.Range)) { seen.Add(m.GetType().Name + " " + m.Serial); }
        var around = TutorialGreeting.GreetAround(tamsin, TutorialGreeting.NeedsGuide, TutorialGreeting.TamsinLine);
        var direct = TutorialGreeting.TryGreet(tamsin, p.Pm, TutorialGreeting.TamsinLine);
        Assert.True(around == 1, $"around={around} direct={direct} now={Core.Now:O} seen={string.Join(", ", seen)}");
""", """        Assert.True(TutorialGreeting.NeedsGuide(p.Pm));
        Assert.Equal(1, TutorialGreeting.GreetAround(tamsin, TutorialGreeting.NeedsGuide, TutorialGreeting.TamsinLine));
"""),
])
print("ok")
