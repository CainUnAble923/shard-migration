"""cc-P762: one mutant per part, each undoing one piece of the change in a copy of the code copy's customizations.
Writes <out>/<name>/Tutorial (and <out>/<name>/ClusterFDevTools.cs for the reset mutant).
Usage: python -P mutate762.py <code copy customizations> <out folder>"""
import pathlib, shutil, sys
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
T = "Tutorial/"
MUTANTS = {
    # part 1: the start decision ignores the lock (the P663 table again)
    "havenopen": (T + "TutorialStart.cs", "if (!NewCharacterRules.HavenStartOpenFor(pm.Account))\n", "if (false)\n"),
    # part 1: the creation screen shows New Haven unlocked
    "citylist": (T + "TutorialStart.cs", "        if (NewCharacterRules.HavenStartOpenFor(account))\n        {\n            return cities;",
                 "        if (true)\n        {\n            return cities;"),
    # part 1 (P717 Codex P2): the reset leaves the tutorial record
    "noreset": ("ClusterFDevTools.cs", "            data.ResetTutorial();\n", ""),
    # part 2: any race asked for is made
    "racefree": (T + "NewCharacterRules.cs", "        refused = !RaceAllowed(account, requested);", "        refused = false;"),
    # part 3: New Haven's switch defaults to open
    "defaultopen": (T + "NewCharacterRules.cs", "public static bool HavenStartOpen => ServerConfiguration.GetSetting(HavenStartKey, false);",
                    "public static bool HavenStartOpen => ServerConfiguration.GetSetting(HavenStartKey, true);"),
    # part 3: the race switch is ignored (Human only, always)
    "raceswitch": (T + "NewCharacterRules.cs", "            var text = ServerConfiguration.GetSetting(RacesKey, DefaultRaces) ?? DefaultRaces;",
                   "            var text = DefaultRaces;"),
    # part 4: staff are locked too
    "staffnotexempt": (T + "NewCharacterRules.cs", "public static bool IsExempt(IAccount? account) => account?.AccessLevel >= AccessLevel.GameMaster;",
                       "public static bool IsExempt(IAccount? account) => false;"),
    # part 4: the bot's staff command takes any account
    "botstaffany": (T + "NewCharacterRules.cs", "if (username == null || !username.StartsWith(BotStaffPrefix, StringComparison.OrdinalIgnoreCase))",
                    "if (username == null)"),
    # part 5: the gate never counts a skip
    "noskip": (T + "TutorialGateSkip.cs", "        return earlyInLessons || !ClusterFTutorial.IsParticipant(pm);", "        return false;"),
    # part 5: a finisher counts as a skipper
    "finisher": (T + "TutorialGateSkip.cs", "        return earlyInLessons || !ClusterFTutorial.IsParticipant(pm);", "        return true;"),
    # part 5: no box
    "nobox": (T + "TutorialGateSkip.cs", "        var scroll = new PetChoiceScroll();\n        scroll.Internalize();\n        box.Contents.Add(scroll);\n", ""),
    # part 5: the scroll gives no pet
    "nopet": (T + "TutorialGateSkip.cs", "        BaseCreature pet = dog ? new Dog() : new Cat();", "        BaseCreature pet = new Cat();"),
    # part 5: skipping is not final
    "goback": (T + "ClusterFTutorial.cs", "        if (TutorialStart.GateSkipped(pm))\n", "        if (false)\n"),
    # part 5: once per character: the gate stays eligible after the skip
    "twice": (T + "TutorialGateSkip.cs", "!TutorialStart.StillOnFirstVisit(pm))", "!TutorialStart.IsIsleStarter(pm))"),
}
for name, (rel, a, b) in MUTANTS.items():
    d = out / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(src / "Tutorial", d / "Tutorial")
    shutil.copyfile(src / "ClusterFDevTools.cs", d / "ClusterFDevTools.cs")
    f = d / rel
    s = f.read_text(encoding="utf-8")
    assert s.count(a) == 1, (name, a)
    f.write_text(s.replace(a, b), encoding="utf-8", newline="")
    print("mutant", name)
