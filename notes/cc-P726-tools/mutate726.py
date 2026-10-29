"""cc-P726 red-first: a copy of the code copy's customizations with each item's behaviour put back behind the new API,
so the new facts compile and can be seen failing (probe.sh with SRC=<copy>). Usage: python mutate726.py <out-root>."""
import pathlib, shutil, sys

SRC = pathlib.Path("D:/UO/golems/Iron/ShatteredLegacy/server/customizations")
OUT = pathlib.Path(sys.argv[1]) / "old726"


def sub(rel, old, new):
    p = OUT / rel
    t = p.read_text(encoding="utf-8")
    if t.count(old) != 1:
        raise SystemExit(f"{rel}: {t.count(old)} matches for {old[:80]!r}")
    p.write_text(t.replace(old, new), encoding="utf-8", newline="\n")


if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)
# 1. the pet can be chosen before the pests (as before)
sub("Tutorial/TutorialFarm.cs", "if (StepOf(pm) != 2 || Array.IndexOf(FarmPetLines, line) < 0)",
    "if (StepOf(pm) is not (1 or 2) || Array.IndexOf(FarmPetLines, line) < 0)")
# 2. no Pet Info entry
sub("Mobiles/Evo/EvoPetInfo.cs", "                list.Add(new EvoPetInfo.PetInfoEntry());\n", "")
# 4. the heal does not finish a healing lesson, and an old farm heal does not count for it
sub("Tutorial/TutorialCoreTrials.cs",
    "        if (IsDoing(pm, TutorialFarm.HealingStationKey)) { Observe(pm, TutorialAction.Healed); }\n        else { ClusterFTutorial.CompleteStation(pm, TutorialFarm.HealingStationKey); }\n",
    "")
sub("Tutorial/ClusterFTutorial.cs",
    "return key == TutorialFarm.HealingStationKey && record.StationsDone.Contains(TutorialFarm.HealKey);",
    "return false;")
# 5. no regeneration from the starter gear
sub("Tutorial/TutorialStarterGear.cs", "if (m is not PlayerMobile pm)", "if (m is not PlayerMobile pm || m != null)")
# 6. the Quests button always opens pinned's log
sub("Tutorial/TutorialQuestLog.cs", "if (m is PlayerMobile pm && ClusterFTutorial.IsParticipant(pm))",
    "if (m is PlayerMobile pm && ClusterFTutorial.IsParticipant(pm) && m == null)")
print("wrote", OUT)
