def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:80], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


C = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/"
edit(C + "Fold/FoldRegions.cs", [
("""        Server.Tutorial.TutorialVisionScene.AlterLight(m, ref global, ref personal); // cc-P665: the vision's light, per player""",
 """        Server.Tutorial.TutorialVisionScene.AlterLight(m, ref global, ref personal); // cc-P665: the vision's light, per player
        Server.Tutorial.TutorialWake.AlterLight(m, ref global, ref personal); // cc-P721: waking on the beach"""),
])
edit(C + "Tutorial/TutorialStart.cs", [
("""                if (!ClusterFTutorial.TryEnter(pm, quiet: true))
                {
                    ClusterFTutorial.AdoptOrphanedRecord(pm);
                }

                SendToIsle(pm);
                break;""", """                if (!ClusterFTutorial.TryEnter(pm, quiet: true))
                {
                    ClusterFTutorial.AdoptOrphanedRecord(pm);
                }

                SendToIsle(pm, atNextLesson: false, wake: true); // cc-P721: the first arrival wakes on the sand
                break;"""),
("""    public static void SendToIsle(PlayerMobile pm, bool atNextLesson)
    {""", """    public static void SendToIsle(PlayerMobile pm, bool atNextLesson) => SendToIsle(pm, atNextLesson, wake: false);

    /// <summary>cc-P721: <paramref name="wake"/> plays the washed-ashore wake-up (TutorialWake) before the first lines.</summary>
    public static void SendToIsle(PlayerMobile pm, bool atNextLesson, bool wake)
    {"""),
("""        ClusterFTutorial.SystemLine(pm, "You wake on a quiet shore: the Wakening Isle.");
        ClusterFTutorial.SystemLine(pm, "Follow the arrow and double-click Tamsin, your guide, with two quick left clicks. Tamsin's window starts each lesson.");
        TutorialGuide.PointTo(pm);""", """        void FirstLines()
        {
            ClusterFTutorial.SystemLine(pm, "You wake on a quiet shore: the Wakening Isle.");
            ClusterFTutorial.SystemLine(pm, "Follow the arrow and double-click Tamsin, your guide, with two quick left clicks. Tamsin's window starts each lesson.");
            TutorialGuide.PointTo(pm);
        }

        if (wake)
        {
            TutorialWake.Play(pm, FirstLines);
        }
        else
        {
            FirstLines();
        }"""),
])
edit(C + "Tutorial/TutorialCoreTrials.cs", [
("""        "core.farm" => "Follow the arrow east along the road to the farm gate and double-click Wren the Farmhand, who wears a straw hat. Choose your pet, clear the pests in the cabbage rows, then heal with a bandage.",""",
 """        "core.farm" => "Follow the arrow east along the road to the farm gate and double-click Wren the Farmhand, who wears a straw hat. Choose your pet and learn its commands, hold a pitchfork and switch to war mode (press Tab), clear the pests in the cabbage rows, then heal Pip with a bandage.","""),
("""Watch the vision; it lasts under a minute, holds you still, and will not change your character.""",
 """Watch the vision; it lasts about a minute, holds you still, and will not change your character."""),
("""        // cc-P665: the 45-second scene; its last beat finishes the lesson, an early end lets the stone start it again.""",
 """        // cc-P665: the scene (61 s since cc-P721); its last beat finishes the lesson, an early end lets the stone start it again."""),
])
print("ok")
