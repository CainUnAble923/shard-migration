"""cc-P769: one mutant per fix, each undoing one piece of the change in a copy of the code copy's customizations.
Writes <out>/<name>/ with the folders and files probe769.sh mounts (Tutorial, Regions, LeagueRegistrar.cs,
ClusterFQuestMilestones.cs).
Usage: python -P mutate769.py <code copy customizations> <out folder>"""
import pathlib, shutil, sys

src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
T = "Tutorial/"
C = T + "TutorialCoreTrials.cs"
MUTANTS = {
    # 1: the old wake hint
    "wakehint": (T + "TutorialWake.cs",
                 'public const string MoveHintLine = "To get up, take a step: hold the right mouse button on the ground, or press an arrow key.";',
                 'public const string MoveHintLine = "Move to get up.";'),
    # 2: the old backpack steps (double-click first, no Open Paperdoll)
    "backpack": (C,
                 '"core.backpack" => "Follow the arrow to the camp beside the road. 1. Open your character window: click your character once and choose Open Paperdoll in the small menu that appears (or double-click yourself). 2. In that window, double-click the backpack picture to open your backpack. 3. Inside your backpack, double-click the blue practice bag.",',
                 '"core.backpack" => "Follow the arrow to the camp beside the road. First open your character window: double-click your own character (two quick left clicks on yourself), or click the paperdoll button. Then double-click the backpack picture in that window, and inside your backpack double-click the blue practice bag.",'),
    # 3: no tip in the lesson window
    "notips": (C, "var tip = done ? null : TutorialCoreTrials.Tip(station.Key);", "var tip = (string?)null;"),
    # 4: "lesson" said aloud does nothing
    "nolessonword": (C, "{ Reopen(trainee); }", "{ }"),
    # 5: the old League hint
    "league": (C,
               '"core.league" => "Follow the arrow to the League lodge and double-click the door on its north side to enter. Double-click Elara Voss (or click her once and choose Talk): her League window opens and this lesson is done. In that window, click Join the League to join now, or the X to close it; you can join later in New Haven.",',
               '"core.league" => "Follow the arrow to the League lodge and double-click the door on its north side to enter. Double-click Elara Voss to finish this lesson; you can read about the League without joining.",'),
    # 6: "bank" in the bank starts nothing
    "nobank": (C, "    public static void BankWord(PlayerMobile pm)\n    {\n", "    public static void BankWord(PlayerMobile pm)\n    {\n        return;\n"),
    # 8: no lesson achievement
    "noach": (T + "ClusterFTutorial.cs", "        TutorialLessonAchievements.Grant(pm, key); // cc-P769 item 8: one per isle lesson\n", ""),
    # 8: the quest claim grants nothing
    "noquest": ("ClusterFQuestMilestones.cs", "        ClusterFAchievementSystem.TryGrant(acct, FirstQuestKey);\n        ClusterFAchievementSystem.RefreshNewHavenQuests(pm, acct);\n", ""),
    # 11: no escort destinations
    "noescort": ("Regions/HavenTownRegions.cs", "    private static Region? EscortParent(StockRegion shop)\n    {\n",
                 "    private static Region? EscortParent(StockRegion shop)\n    {\n        return null;\n"),
    # 12: no pointer back to Rook
    "nonext": (T + "TutorialWingTrials.cs", "            Line(pm, NextLessonLine);\n", ""),
    # 13: the curio's double-click does not use the skill
    "nocurio": (T + "TutorialTradeTrials.cs", "            from.UseSkill(SkillName.ItemID);\n", ""),
}
for name, (rel, a, b) in MUTANTS.items():
    d = out / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(src / "Tutorial", d / "Tutorial")
    shutil.copytree(src / "Regions", d / "Regions")
    for f in ("LeagueRegistrar.cs", "ClusterFQuestMilestones.cs"):
        shutil.copyfile(src / f, d / f)
    f = d / rel
    s = f.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in s else "\n"
    a2, b2 = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a2) == 1, (name, a)
    f.write_text(s.replace(a2, b2), encoding="utf-8", newline="")
    # copytree keeps the old times; MSBuild would not recompile them (P762's first mutant run). Newer than the DLL:
    for g in d.rglob("*"):
        g.touch()
    print("mutant", name)
