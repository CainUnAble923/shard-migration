"""cc-P718 red run: a copy of the customizations probe.sh mounts (Tutorial/, Fold/, LeagueRegistrar.cs, ClusterFSkillGain.cs)
with behaviour put back to the old, behind the new API so the new facts compile.
  old:  every item at once, as before P718 (each new fact must fail for its own reason)
  copies: a refused copy seeding still counts as seeded (the P718 bot run's empty copy)
  fine: the finer rules: greetings without their interval, greetings that never stop, Wren past the pet, the cloak
        taken back when the lesson ends
Usage: python -I mutate.py <src customizations dir> <dest dir> <old|fine>"""
import os, shutil, sys

src, dest, name = sys.argv[1], sys.argv[2], sys.argv[3]
if os.path.exists(dest):
    shutil.rmtree(dest)
os.makedirs(dest)
for d in ("Tutorial", "Fold"):
    shutil.copytree(os.path.join(src, d), os.path.join(dest, d))
for f in ("LeagueRegistrar.cs", "ClusterFSkillGain.cs"):
    shutil.copy(os.path.join(src, f), os.path.join(dest, f))


def edit(path, old, new):
    p = os.path.join(dest, path)
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == 1, (path, old[:70], s.count(old))
    open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))


G, P, T, F = "Tutorial/TutorialGreeting.cs", "Tutorial/TutorialCorePlacement.cs", "Tutorial/TutorialCoreTrials.cs", "Tutorial/TutorialFarm.cs"

if name == "old":
    # 1. No NPC speaks first.
    edit(G, "        if (npc.Deleted || pm.Deleted", "        if (true || npc.Deleted || pm.Deleted")
    # 2 and 5. The cloak goes into the backpack, and can go anywhere.
    edit(P, "        var cloak = new WakeningIsleCloak(pm);\n        var table = TutorialWorld.Ground(map, TutorialCorePlacement.ClothesTable);\n"
            "        cloak.MoveToWorld(new Point3D(table.X, table.Y, table.Z + TutorialCorePlacement.TableHeight), map);\n        return cloak;",
         "        var cloak = new WakeningIsleCloak(pm);\n        pm.AddToBackpack(cloak);\n        return cloak;")
    edit(P, "    public override bool Nontransferable => true;", "    public override bool Nontransferable => false;")
    # 3. No client tips outside the wings.
    edit("Tutorial/TutorialStations.cs", "    public static bool IsAnytime(string key) => key.Equals(TutorialClientTips.Key, StringComparison.OrdinalIgnoreCase);",
         "    public static bool IsAnytime(string key) => false;")
    # 4. The bag alone finishes the backpack lesson.
    edit("Tutorial/TutorialTrialProgress.cs", '"core.backpack" => [TutorialAction.OpenedPaperdoll, TutorialAction.OpenedBag],',
         '"core.backpack" => [TutorialAction.OpenedBag],')
    # 6. The old wall-arm signposts, and the arrow at the stop.
    edit(P, "        (SignpostId, ChatSignpost, ChatSignpostName),", "        (OldSignpostId, ChatSignpost, OldChatSignpostName),")
    edit(P, '        "core.chat" => Ground(ChatSignpost), // cc-P718: the post itself, not the stop in front of it',
         '        "core.chat" => Ground(TutorialWorld.Signpost),')
    edit(P, "        foreach (var i in old) { i.Delete(); }\n        return old.Count;", "        return 0;")
    edit(F, "            OldSignArm => GateSignpost,\n            OldSignBoard => null,", "")
    edit(F, "                if (c.ItemID == OldSignArm)", "                if (false)")
    edit(F, "                else if (c.ItemID == OldSignBoard)", "                else if (false)")
    # 7. Pests fight any trainee, and roam.
    edit(F, "            return player is PlayerMobile pm && TutorialFarm.PestPartOn(pm);", "            return TutorialCreature.Engages(player);")
    edit(F, "            if (!TutorialFarm.PestField.Contains(new Point2D(x, y)) && FoldMaps.IsFold(Map))", "            if (false)")
    edit(F, "            if (from.AccessLevel == AccessLevel.Player && !Open &&", "            if (false &&")
    # 8. No isle pace.
    edit("Tutorial/TutorialSkillPace.cs", "        !Applies(m) || !_last.TryGetValue", "        true || !_last.TryGetValue")
    # 9. The old bandage lines.
    edit(F, 'public const string HealLine = "Here are some bandages. To heal, double-click a bandage in your backpack, then click yourself or your hurt pet. A successful heal finishes this step.";',
         'public const string HealLine = "Double-click a bandage in your backpack, then click yourself or an injured pet. A successful heal finishes this step.";')
    edit(F, 'public const string MakeBandagesLine = "Later you can make your own bandages: double-click a pair of scissors, then click a pile of cloth to cut it into bandages.";',
         'public const string MakeBandagesLine = "";')
    # 10. No commands, no pet kill needed, the pet keeps following.
    edit(F, "        public static bool CommandsDone(PlayerMobile pm) => Has(pm, FollowKey) && Has(pm, GuardKey);",
         "        public static bool CommandsDone(PlayerMobile pm) => true;")
    edit(F, "            if (!_petKilled.Contains(pm.Serial) && PetsOf(pm).Count > 0)", "            if (false)")
elif name == "fine":
    # 1. Greetings with no interval.
    edit(G, "        if (_said.TryGetValue(key, out var at) && Core.TickCount - at < (long)Interval.TotalMilliseconds)", "        if (false)")
elif name == "fine2":
    # 1. Tamsin keeps prompting after she was used; Wren after the pet.
    edit(G, "        ClusterFTutorial.IsParticipant(pm) && !_usedGuide.Contains(pm.Serial) &&", "        ClusterFTutorial.IsParticipant(pm) &&")
    edit(G, "        ClusterFTutorial.RecordOf(pm) is { StationsDone.Count: 0 } && TutorialCoreTrials.Current(pm) == null;", "        true;")
    edit(G, "        TutorialFarm.StepOf(pm) == 1 && ClusterFTutorial.RecordOf(pm) is { } record &&", "        TutorialFarm.StepOf(pm) >= 1 && ClusterFTutorial.RecordOf(pm) is { } record &&")
    # 2. The cloak is taken back when the lesson ends (the old practice item's rule).
    edit(T, "        trial.Supply?.Delete(); // exact supplied instance only, even if moved to the bank",
         "        trial.Supply?.Delete(); // exact supplied instance only, even if moved to the bank\n        if (trial.Station.Key == \"core.paperdoll\") { WakeningIsleCloak.On(pm)?.Delete(); }")
elif name == "copies":
    # The copy seeding rule before P718: refused seeding still marks the copy seeded, and a claim never retries it.
    C = "Tutorial/TutorialCopies.cs"
    edit(C, "        slot.Seeded = slot.Placed.Count > 0;", "        slot.Seeded = true;")
    edit(C, "            if (!free.Seeded || free.Placed.Count == 0)", "            if (!free.Seeded)")
else:
    raise SystemExit("unknown mutant " + name)
