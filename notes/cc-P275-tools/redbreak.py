"""cc-P275 red runs: break the code on purpose (variant A or B), or restore it. Originals saved beside this script."""
import os, shutil, sys

ROOT = r"D:\ShatteredLegacy\server\customizations"
HERE = os.path.dirname(os.path.abspath(__file__))
SAVE = os.path.join(HERE, "red-originals")

FILES = {
    "rules": os.path.join(ROOT, r"Items\Traps\Deployable\DeployableTraps.cs"),
    "trap": os.path.join(ROOT, r"Items\Traps\Deployable\DeployedTrap.cs"),
    "lesson": os.path.join(ROOT, r"Items\Traps\Deployable\TrapLesson.cs"),
    "seeder": os.path.join(ROOT, r"ClusterFRootdeepSeeder.cs"),
}

A = [
    # fact 1 (and 2's Trammel half): pets, summons and players count as targets
    ("rules", "        if (!monster && !(PvpEnabled && trap.Map == Map.Felucca))\n        {\n            return false;\n        }\n", ""),
    # fact 3: the presence range is ignored
    ("rules", "return trap.Kind == DeployableTrapKind.Alarm || owner.InRange(trap.GetWorldLocation(), PresenceRange);", "return true;"),
    # fact 5: the set's gain window is wrong
    ("rules", "        return (min, min + 50);\n    }\n\n    /// <summary>A hit's", "        return (min, min + 60);\n    }\n\n    /// <summary>A hit's"),
    # fact 6: the Den's Master never trusted with bosses
    ("rules", "public static bool OwnerMayTrapBosses(Mobile owner) => ThievesDenStealRules.DenRank(owner) >= ClusterFGuildSystem.RankMaster;",
     "public static bool OwnerMayTrapBosses(Mobile owner) => false;"),
    # fact 8: guard zones allowed
    ("rules", "(region.GetRegion<GuardedRegion>() is { } guarded && !guarded.IsDisabled() || region.IsPartOf<HouseRegion>() ||",
     "(region.IsPartOf<HouseRegion>() ||"),
    # fact 10: the shackle's gate
    ("rules", '[(DeployableTrapKind.Shackle, "tinkering")] = 110,', '[(DeployableTrapKind.Shackle, "tinkering")] = 100,'),
    # round trip: a loaded trap is not registered
    ("trap", "            DeployableTraps.Placed.Add(this);\n        }\n    }\n}", "        }\n    }\n}"),
]

B = [
    # fact 4: a hand re-set does not restore the charges
    ("trap", "        ResetCharges();\n\n        var (min, max) = DeployableTraps.SetGainWindow(Kind);\n        from.CheckSkill(SkillName.RemoveTrap, min, max);\n        from.SendMessage($\"You re-set",
     "        var (min, max) = DeployableTraps.SetGainWindow(Kind);\n        from.CheckSkill(SkillName.RemoveTrap, min, max);\n        from.SendMessage($\"You re-set"),
    # fact 7: flyers trip ground traps
    ("rules", "        if (IsGround(kind) && IsFlying(m))\n        {\n            return \"flying\";\n        }\n", ""),
    # fact 9: a netted rat completes nothing
    ("lesson", "        if (ClusterFTutorial.RecordOf(pm)!.StationsDone.Add(LessonKey))", "        if (false)"),
    # floor traps: T3 moved into the rotworm's walking box
    ("seeder", 'new("T3 Warren west descent: spikes", "Warren", 5161, 1195,', 'new("T3 Warren west descent: spikes", "Warren", 5165, 1195,'),
    # fact 2: the owner is not flagged
    ("trap", "        if (t is PlayerMobile || t is BaseCreature { Controlled: true })\n        {\n            Owner!.DoHarmful(t);\n        }\n", ""),
]


def restore():
    for key, path in FILES.items():
        saved = os.path.join(SAVE, key + ".cs")
        if os.path.exists(saved):
            shutil.copyfile(saved, path)
    print("restored")


def apply(edits):
    os.makedirs(SAVE, exist_ok=True)
    for key, path in FILES.items():
        saved = os.path.join(SAVE, key + ".cs")
        if not os.path.exists(saved):
            shutil.copyfile(path, saved)
    for key, old, new in edits:
        path = FILES[key]
        with open(path, encoding="utf-8", newline="") as f:
            s = f.read()
        old_n = old.replace("\n", "\r\n") if "\r\n" in s and old.replace("\n", "\r\n") in s else old
        new_n = new.replace("\n", "\r\n") if old_n != old else new
        if s.count(old_n) != 1:
            sys.exit(f"break not found once in {key}: {old[:70]!r}")
        s = s.replace(old_n, new_n)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(s)
    print(f"applied {len(edits)} breaks")


if __name__ == "__main__":
    {"A": lambda: apply(A), "B": lambda: apply(B), "restore": restore}[sys.argv[1]]()
