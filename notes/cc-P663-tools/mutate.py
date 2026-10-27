"""cc-P663 red run: a copy of the Tutorial customizations with each new behaviour put back to the old one, behind the new
API (so the new facts compile). Usage: python -I mutate.py <src Tutorial dir> <dest dir>"""
import os, shutil, sys

src, dest = sys.argv[1], sys.argv[2]
only = sys.argv[3] if len(sys.argv) > 3 else "all"


def on(name):
    return only in ("all", name)

if os.path.exists(dest):
    shutil.rmtree(dest)
shutil.copytree(src, dest)


def edit(name, old, new):
    p = os.path.join(dest, name)
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == 1, (name, old[:60], s.count(old))
    open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))


# 1. The order: the old one (farm optional, travel seventh) and the old done rule.
if on("order"):
    p = os.path.join(dest, "TutorialStations.cs")
    s = open(p, encoding="utf-8").read()
    a = s.index('        new("core.farm", TutorialWing.Core')
    b = s.index('        new("core.death", TutorialWing.Core')
    farm = s[a:b]
    s = s[:a] + s[b:]
    a = s.index('        new("core.travel", TutorialWing.Core')
    b = s.index("\n\n", a)
    travel = s[a:b + 1]
    s = s[:a] + s[b + 1:]
    i = s.index('        new("core.league", TutorialWing.Core')
    s = s[:i] + travel + s[i:]
    s = s.replace(farm.replace("TutorialWing.Core", "TutorialWing.Core"), "")
    i = s.index("        // -- Combat wing --")
    s = s[:i] + farm.replace("TutorialWing.Core", "TutorialWing.Animals") + s[i:]
    open(p, "w", encoding="utf-8", newline="\n").write(s)
    edit("ClusterFTutorial.cs", "        if (key != TutorialStations.LastCore)\n", "        if (true)\n")

# 2. Pets: the old gate moved only the player.
if on("pets"):
    edit("TutorialWorld.cs", "        foreach (var pet in pets)\n        {\n            pet.MoveToWorld(to, map);\n        }\n", "")

# 3. Eligibility: no table, the choice alone decides.
if on("table"):
    edit("TutorialStart.cs", "        var orphaned = record.IsActive && ClusterFTutorial.IsRecordedCharacter(pm, record);",
         "        return c == Choice.Isle ? Outcome.Isle : Outcome.Skip;\n#pragma warning disable CS0162\n        var orphaned = record.IsActive && ClusterFTutorial.IsRecordedCharacter(pm, record);")

# 4 and 5. The choice: one loose account flag kept in memory, not saved per character.
if on("choice"):
    edit("TutorialStart.cs", '    private static string Key(Mobile m) => $"character:{(uint)m.Serial}:start";',
         '    private static string Key(Mobile m) => "account:start";\n    private static readonly System.Collections.Generic.Dictionary<string, string> Loose = new();')
    edit("TutorialStart.cs", "data.FlagValues.TryGetValue(Key(m), out var v)", "Loose.TryGetValue(Key(m) + (uint)acct.GetHashCode(), out var v)")
    edit("TutorialStart.cs", "            ClusterFAccountPersistence.GetOrCreate(acct).FlagValues[Key(m)] = Text(c);",
         "            Loose[Key(m) + (uint)acct.GetHashCode()] = Text(c);")
    edit("TutorialStart.cs", "        ClusterFAccountPersistence.GetOrCreate(acct).FlagValues.Remove(Key(pm));",
         "        Loose.Remove(Key(pm) + (uint)acct.GetHashCode());")

# 6. The moongate: double-click only (pinned's Item.OnMoveOver).
if on("step"):
    edit("TutorialCorePlacement.cs", "        if (m is PlayerMobile pm) { Timer.DelayCall(TimeSpan.Zero, () => Use(pm, Location)); }\n", "")

# 7. A reconnect: the trial and its supply kept through the login.
if on("reconnect"):
    edit("ClusterFTutorial.cs", "    public static void OnLogin(PlayerMobile pm)\n    {\n        TutorialCoreTrials.Cancel(pm);",
         "    public static void OnLogin(PlayerMobile pm)\n    {")

# 8. Remedial: restarted at Rook, no trip to the isle.
if on("remedial"):
    edit("ClusterFTutorial.cs", "        TutorialStart.SendToIsle(pm);\n        return true;", "        return true;")

# The city list: New Haven only.
if on("cities"):
    edit("TutorialStart.cs", "        new(IsleCity, \"The Wakening Isle\"", "        // new(IsleCity, \"The Wakening Isle\"")
# 9. Before go-live: the old login entered any fresh account's character.
if on("golive"):
    edit("ClusterFTutorial.cs", "                AdoptOrphanedRecord(pm);\n                if (IsParticipant(pm) && TutorialWorld.IsOnIsle(pm))",
         "                AdoptOrphanedRecord(pm);\n                TryEnter(pm);\n                if (IsParticipant(pm) && TutorialWorld.IsOnIsle(pm))")
print("mutant", only, "written to", dest)

# 10. Live: the choice recorded with the tutorial off.
if on("live"):
    edit("TutorialStart.cs", "        var choice = ClusterFTutorial.Enabled ? ChoiceOf(city) : Choice.None;", "        var choice = ChoiceOf(city);")
    print("mutant live applied")
