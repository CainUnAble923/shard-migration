"""Apply named mutations to the shard tree, or restore it. Usage: redrun.py apply <set> | restore"""
import json, os, shutil, sys, hashlib

ROOT = "D:/ShatteredLegacy/server/"
SAVE = os.path.join(os.path.dirname(__file__), "redsave")
C = "customizations/"
PS = C + "Services/PointsSystems/"
CB = C + "Services/CleanUpBritannia/"

SETS = {
    "stage1": [
        # fact 1: a table value
        (PS + "CleanUpBritanniaData.cs", "Add(typeof(global::Server.Items.IronIngot), 0.10);", "Add(typeof(global::Server.Items.IronIngot), 0.11);"),
        # fact 2: a runic rate
        (PS + "CleanUpBritanniaData.cs", "CraftResource.Valorite   => 8000 * hammer.UsesRemaining,", "CraftResource.Valorite   => 7999 * hammer.UsesRemaining,"),
        # fact 3: the truncation
        (PS + "CleanUpBritanniaData.cs", "            return (int)award;", "            return (int)Math.Ceiling(award);"),
        # fact 4: our rate above our ingot value
        (PS + "CleanUpBritanniaData.cs", ">= CraftResource.Platinum and <= CraftResource.Celestial => ExtendedValue(resource),", ">= CraftResource.Platinum and <= CraftResource.Celestial => ExtendedValue(resource) * 1.1,"),
        # fact 5: OSI's wood rates flattened to board values
        (PS + "CleanUpBritanniaData.cs", "CraftResource.AshWood       => .33,", "CraftResource.AshWood       => .25,"),
        (PS + "CleanUpBritanniaData.cs", "CraftResource.YewWood       => .67,", "CraftResource.YewWood       => .50,"),
        (PS + "CleanUpBritanniaData.cs", "CraftResource.Frostwood     => 3.17,", "CraftResource.Frostwood     => 3.0,"),
        # fact 6: the guild bag's clamp removed (the D42 dupe)
        (C + "SmithGuildSalvageBag.cs", "return Math.Max(MinimumIngotReturn, Math.Min(amount, cost - 1));", "return Math.Max(MinimumIngotReturn, amount);"),
        # fact 7: points keyed by account (the first character)
        (PS + "PointsSystem.cs", "        if (from is not PlayerMobile pm)\n        {\n            return null;\n        }\n",
         "        if (from is not PlayerMobile pm)\n        {\n            return null;\n        }\n\n        if (pm.Account?[0] is PlayerMobile first) pm = first;\n"),
        # fact 8: lifetime follows points
        (PS + "CleanUpBritanniaData.cs", "            e.Lifetime += added;", "            e.Lifetime = e.Points;"),
        # fact 9: lifetime not written
        (PS + "CleanUpBritanniaData.cs", "        writer.Write(Points);\n        writer.Write(Lifetime);", "        writer.Write(Points);"),
    ],
    "stage1b": [
        (C + "SmithGuildSalvageBag.cs", "return Math.Max(MinimumIngotReturn, Math.Min(amount, cost - 1));", "return Math.Max(MinimumIngotReturn, amount);"),
        # print-only: fail the two measurement facts at their end so their output is shown
        ("tests/Services/CleanUpBritanniaPointsVerification.cs",
         "        Assert.DoesNotContain(excess, r => r.Resource == CraftResource.Heartwood);\n",
         "        Assert.DoesNotContain(excess, r => r.Resource == CraftResource.Heartwood);\n        foreach (var r in excess) _out.WriteLine($\"ROW {r}\");\n        Assert.Fail(\"print only\");\n"),
        ("tests/Services/CleanUpBritanniaPointsVerification.cs",
         "            Assert.Contains(rows, r => r.Resource == res);\n        }\n    }\n",
         "            Assert.Contains(rows, r => r.Resource == res);\n        }\n\n        Assert.Fail(\"print only\");\n    }\n"),
    ],
    "stage234": [
        # B1: appraisal reports a different number than the barrel pays
        (PS + "CleanUpBritanniaData.cs", "        var points = CleanUpBritanniaData.GetPoints(item);\n\n        if (points == 0)", "        var points = CleanUpBritanniaData.GetPoints(item) * 1.01;\n\n        if (points == 0)"),
        # B2: the Clean Up barrel takes anything
        (CB + "CleanupTrashBarrel.cs", "        if (!CleanUpTrash.AddCleanupItem(this, from, item))", "        if (!CleanUpTrash.AddCleanupItem(this, from, item) && false)"),
        # B3, B4: pinned's barrel and chest record nothing
        (CB + "CleanUpTrash.cs", "        var cleanup = For(trash);\n        var added = false;", "        if (trash is TrashBarrel or TrashChest) return false;\n\n        var cleanup = For(trash);\n        var added = false;"),
        # B5: no appraise entry
        (CB + "CleanUpTrash.cs", "        if (CleanUpBritanniaData.Enabled && from is PlayerMobile)\n        {\n            list.Add(new AppraiseforCleanup());", "        if (CleanUpBritanniaData.Enabled && from is PlayerMobile && false)\n        {\n            list.Add(new AppraiseforCleanup());"),
        # S1: OSI's section not sorted by price
        (CB + "CleanUpBritanniaRewards.cs", "SortedOsi { get; } = OsiRewards.OrderBy(r => r.Points).ToArray();", "SortedOsi { get; } = OsiRewards.OrderByDescending(r => r.Points).ToArray();"),
        # S2: a Custodian price off by one
        (CB + "CleanUpBritanniaRewards.cs", 'new(typeof(Bandage), 0xE21, "100 bandages", 15, 100, true),', 'new(typeof(Bandage), 0xE21, "100 bandages", 16, 100, true),'),
        # S3: the points check skipped
        (CB + "CleanUpBritanniaRewards.cs", "        if (cub.GetPoints(pm) < reward.Points)", "        if (cub.GetPoints(pm) < reward.Points && false)"),
        # S4: the store opens from afar
        (C + "SanitationWardenGump.cs", "    public const int StoreRange = 5;", "    public const int StoreRange = 30;"),
        # C1: a second bag leaves the first
        (C + "TrashBag.cs", "        foreach (var old in OwnedBy(pm))\n        {\n            old.Delete();\n        }", "        foreach (var old in OwnedBy(pm))\n        {\n        }"),
        # C3: anyone can dump a bag
        (C + "TrashBag.cs", "        if (bag.Owner != pm)\n        {", "        if (bag.Owner != pm && false)\n        {"),
        # C4: the standing no longer follows awards
        (PS + "CleanUpBritanniaData.cs", "        ClusterFCustodianSystem.SyncStanding(entry.Player);", ""),
        # C5: a player's corpse is litter again
        (C + "ClusterFCustodianSystem.cs", "        if (item is Corpse { Owner: PlayerMobile }) return false;", ""),
        # C6: the Apprentice task pays scrip again
        (C + "ClusterFGuildSystem.cs", "            joinRep: 0, joinScrip: 0));", "            joinRep: 0, joinScrip: 5));"),
        # C7: Craft X uses any trash bag in the pack
        (C + "ClusterFCraftRejects.cs", "TrashBag.OwnedBy(from).Find(b => b.IsChildOf(pack)) is { } trashBag", "pack.FindItemByType<TrashBag>() is { } trashBag"),
    ],
    # S5: the dry run places
    "stage3place": [
        (CB + "ClusterFCleanUpPlacement.cs", "            if (!dryRun)\n            {\n                new TheCleanupOfficer", "            if (true)\n            {\n                new TheCleanupOfficer"),
    ],
    # C4 (added): a non-member's points write a standing
    "stage4member": [
        (C + "ClusterFCustodianSystem.cs",
         "        if (guild == null ||\n            !guild.JoinedGuilds.Contains(\"custodians\") && !guild.GuildReputation.ContainsKey(\"custodians\"))\n        {\n            return;\n        }\n\n        guild.GuildReputation",
         "        guild ??= ClusterFAccountPersistence.GetOrCreateGuild(pm);\n\n        guild.GuildReputation"),
    ],
    # C2: the owner written at version 0, no bump (the mistake the version bump prevents)
    "stage234b": [
        (PS + "CleanUpBritanniaData.cs", "        ClusterFCustodianSystem.SyncStanding(entry.Player);", ""),
        (C + "TrashBag.cs", "[SerializationGenerator(1, false)]", "[SerializationGenerator(0, false)]"),
        (C + "TrashBag.cs", "    // A version 0 bag has no fields and no owner.\n    private void MigrateFrom(V0Content content)\n    {\n    }\n", ""),
    ],
}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def apply(name):
    os.makedirs(SAVE, exist_ok=True)
    manifest = {}
    for rel, old, new in SETS[name]:
        path = ROOT + rel
        bak = os.path.join(SAVE, rel.replace("/", "__"))
        if rel not in manifest:
            if not os.path.exists(bak):
                shutil.copyfile(path, bak)
            manifest[rel] = sha(bak)
        s = open(path, encoding="utf-8").read()
        if s.count(old) != 1:
            sys.exit(f"mutation not unique/found in {rel}: {old[:70]!r} ({s.count(old)})")
        open(path, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
    json.dump(manifest, open(os.path.join(SAVE, "manifest.json"), "w"))
    print(f"applied {len(SETS[name])} mutations to {len(manifest)} files")


def restore():
    manifest = json.load(open(os.path.join(SAVE, "manifest.json")))
    for rel, digest in manifest.items():
        bak = os.path.join(SAVE, rel.replace("/", "__"))
        shutil.copyfile(bak, ROOT + rel)
        assert sha(ROOT + rel) == digest, rel
        os.remove(bak)
        print("restored, identical to saved copy:", rel)
    os.remove(os.path.join(SAVE, "manifest.json"))


if __name__ == "__main__":
    apply(sys.argv[2]) if sys.argv[1] == "apply" else restore()
