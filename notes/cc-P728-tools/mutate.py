"""cc-P728 red-first: writes copies of the code copy's customizations with behaviour put back, so the new facts can be seen
failing (probe.sh with SRC=<copy>). Usage: python mutate.py <out-root>. Writes <out-root>/old (every item as before
cc-P728, behind the new API so the facts compile). The PlayerMobile patch is left out with NOPATCH=1 in probe.sh."""
import pathlib, shutil, sys

SRC = pathlib.Path("D:/UO/golems/Iron/ShatteredLegacy/server/customizations")
OUT = pathlib.Path(sys.argv[1])


def sub(root, rel, old, new):
    p = root / rel
    t = p.read_text(encoding="utf-8")
    if t.count(old) != 1:
        raise SystemExit(f"{rel}: {t.count(old)} matches for {old[:80]!r}")
    p.write_text(t.replace(old, new), encoding="utf-8", newline="\n")


def old(root):
    # 1. Nothing waits for the wake-up; the guild welcome comes on the isle too.
    sub(root, "Tutorial/TutorialWake.cs",
        "IsLying(pm) || _held.ContainsKey(pm.Serial) || TutorialStart.WillWake(pm);", "false;")
    sub(root, "ClusterFGuildStarterPath.cs", "        if (FoldMaps.IsFold(pm.Map))\n            return;\n", "")
    # 2. Up after five seconds, as P721 had it.
    sub(root, "Tutorial/TutorialWake.cs", "if (s >= SafetySeconds)", "if (s >= 5)")
    # 3. The cloak lies loose on the table (P718), no chest.
    sub(root, "Tutorial/TutorialCorePlacement.cs",
        "        WakeningIsleCloak.OnTable(pm, map)?.Delete();\n",
        "        if (WakeningIsleCloak.OnTable(pm, map) == null) { var loose = new WakeningIsleCloak(pm); var t = TutorialWorld.Ground(map, TutorialCorePlacement.ClothesTable); loose.MoveToWorld(new Point3D(t.X, t.Y, t.Z + TutorialCorePlacement.TableHeight), map); }\n"
        "        if (WakeningIsleCloak.OnTable(pm, map) != null) { return null; }\n")
    # 4. The pitchfork only after the pet's commands (P721's order).
    sub(root, "Tutorial/TutorialFarm.cs",
        "return GivePitchfork(pm) != null || HoldsPitchfork(pm)",
        "return (Has(pm, GuardKey) && GivePitchfork(pm) != null) || HoldsPitchfork(pm)")
    sub(root, "Tutorial/TutorialFarm.cs",
        "            if (!Has(pm, WeaponKey))\n            {\n                if (HoldsPitchfork(pm))",
        "            if (!Has(pm, WeaponKey) && Has(pm, GuardKey))\n            {\n                if (HoldsPitchfork(pm))")
    # 6. "Defeat 0 more", the old echo line alone, no next-lesson pointer.
    sub(root, "Tutorial/TutorialFarm.cs",
        "return !_petKilled.Contains(pm.Serial) && PetsOf(pm).Count > 0 ? PetKillLine : StrikeLine;",
        "return string.Format(PestsLeftLine, Math.Max(0, left));")
    sub(root, "Tutorial/TutorialFarm.cs",
        "            hand?.SayTo(pm, EchoPestsLine);\n            TutorialCoreTrials.NowStep(",
        "            ClusterFTutorial.SystemLine(pm, EchoPestsLine);\n            if (map == null) TutorialCoreTrials.NowStep(")
    sub(root, "Tutorial/TutorialFarm.cs",
        '"The cabbage rows are clear! Go back to Wren at the farm gate and double-click her."',
        '"You cleared the farm pests. Return to Wren the Farmhand at the gate."')
    sub(root, "Tutorial/TutorialCoreTrials.cs",
        "        if (ClusterFTutorial.RecordOf(pm) is not { } record || ClusterFTutorial.CoreLeft(record).FirstOrDefault() is not { } next) { return; }\n        var line = string.Format(NextLessonLine",
        "        if (pm != null || ClusterFTutorial.RecordOf(pm) is not { } record || ClusterFTutorial.CoreLeft(record).FirstOrDefault() is not { } next) { return; }\n        var line = string.Format(NextLessonLine")
    # 7. No top-up of the copies at load.
    sub(root, "Tutorial/TutorialRecruiter.cs", "            lines.AddRange(TutorialCopies.TopUpSeeded());\n", "")


for name, fn in [("old", old)]:
    root = OUT / name
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(SRC, root)
    fn(root)
    print("wrote", root)
