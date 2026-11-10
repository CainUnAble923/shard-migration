# cc-P863: one folder per break under mutants/, each with the one mutated StaffHub file. Each break must turn a fact red.
import os, shutil
SRC = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/StaffHub'
OUT = 'D:/UO/golems/Iron/shard-migration/notes/cc-P863-tools/mutants'
C, G, H, T = 'StaffColorWars.cs', 'StaffColorWarsGump.cs', 'StaffHubGump.cs', 'StaffEventsSettings.cs'
X = [
 # opening
 ('nosizecheck', C, 'if (Math.Min(w, h) < S.CwMinSide || w * h > S.CwMaxTiles)', 'if (false)'),
 ('twoarenas', C, '        if (Active != null)\n        {\n            message = "Color Wars is already open.', '        if (false)\n        {\n            message = "Color Wars is already open.'),
 ('nostones', C, '            run.Stones.Add(stone);\n', ''),
 ('gateinside', C, 'if (map == run.Map && run.Contains(at.X, at.Y))', 'if (false)'),
 # the gate
 ('joinonstep', C, '        pm.CloseGump<ColorWarsJoinGump>();\n        pm.SendGump(new ColorWarsJoinGump());', '        StaffColorWars.Join(pm, out _);'),
 ('younglets', C, '        if (pm.Young)\n', '        if (false)\n'),
 ('deadlets', C, '        if (!pm.Alive)\n        {\n            return "The dead', '        if (false)\n        {\n            return "The dead'),
 ('mountlets', C, '        if (pm.Mounted)\n', '        if (false)\n'),
 ('stafflets', C, '        if (pm.AccessLevel > AccessLevel.Player)\n        {\n            return "Staff run', '        if (false)\n        {\n            return "Staff run'),
 ('havenlets', C, 'if (!Tutorial.TutorialIslandGate.CanMove(pm, run.Base(PickTeam(run)), run.Map, false))', 'if (false)'),
 # joining
 ('nostash', C, '        foreach (var item in pm.Backpack.Items.ToList())\n        {\n            bag.DropItem(item);\n        }\n', ''),
 ('noworn', C, '            p.Worn.Add(item);\n            bag.DropItem(item);\n', ''),
 ('nohuemod', C, '        pm.HueMod = Hue(team);\n', ''),
 ('unbalanced', C, '        return open[Utility.Random(open.Count)];', '        return ColorWarsTeam.Red;'),
 ('blessedkit', C, '            item.Hue = hue;\n            item.LootType = LootType.Regular;\n            p.Kit.Add(item);', '            item.Hue = hue;\n            p.Kit.Add(item);'),
 ('nomove', C, '        pm.MoveToWorld(run.Base(team), run.Map);\n        pm.PlaySound(0x1FE);', '        pm.PlaySound(0x1FE);'),
 # notoriety
 ('nonoto', C, '        return a == b ? Notoriety.Ally : Notoriety.Enemy;', '        return null;'),
 ('allenemy', C, '        return a == b ? Notoriety.Ally : Notoriety.Enemy;', '        return Notoriety.Enemy;'),
 # the fight
 ('fightwhilegather', C, '            return Run.Phase == ColorWarsPhase.Fighting && a != b;', '            return a != b;'),
 ('friendlyfire', C, '            return Run.Phase == ColorWarsPhase.Fighting && a != b;', '            return Run.Phase == ColorWarsPhase.Fighting;'),
 ('healfoes', C, '            return Staff(from) || a == b && a != null; // teammates only', '            return true;'),
 # a death
 ('lootable', C, '                foreach (var item in corpse.Items.ToList())\n                {\n                    pack.DropItem(item);\n                }\n', ''),
 ('noscore', C, '            run.Scores[(int)kt]++;\n', ''),
 ('teamkillscores', C, '        if (TeamOf(killer) is { } kt && kt != p.Team)', '        if (TeamOf(killer ?? pm) is { } kt)'),
 ('norevive', C, '        pm.Resurrect();\n        (pm.FindItemOnLayer(Layer.OuterTorso) as DeathRobe)?.Delete();\n\n        // Put the kit back on.', '\n        // Put the kit back on.'),
 ('nobase', C, '        pm.MoveToWorld(run.Base(p.Team), run.Map);\n        pm.Resurrect();', '        pm.Resurrect();'),
 # leaving
 ('kitstays', C, '            foreach (var item in p.Kit)\n            {\n                item.Delete();\n            }\n', ''),
 ('splitstays', C, '        p.Kit.Contains(item) ||\n        item.Hue == Hue(p.Team) && item is', '        p.Kit.Contains(item) ||\n        false && item is'),
 ('noreturn', C, '                foreach (var item in stash.Items.ToList())\n                {\n                    pm.Backpack.DropItem(item);\n                }\n', ''),
 ('nohome', C, '            else\n            {\n                pm.MoveToWorld(p.ReturnLocation, p.ReturnMap);\n            }\n', '\n'),
 ('stonefar', C, '        if (!from.InRange(GetWorldLocation(), 2))', '        if (true)'),
 # the end
 ('nopay', C, '                FestivalTokens.Grant(p.Mobile, S.CwWinTokens, $"Color Wars, the {Name(w)} team won");\n', ''),
 ('paydraw', C, '        return best > 0 && top.Count == 1 ? top[0] : null;', '        return top[0];'),
 ('arenastays', C, '        run.Region?.Unregister();\n        Active = null;\n        message = pay', '        Active = null;\n        message = pay'),
 ('stonesstay', C, '        foreach (var stone in run.Stones)\n        {\n            stone.Delete();\n        }\n', ''),
 ('nokillstowin', C, '            if (S.CwKillsToWin > 0 && run.Scores[(int)kt] >= S.CwKillsToWin)', '            if (false)'),
 # the arena
 ('learns', C, '    public override bool AllowGain(Mobile m, Skill skill, object obj) => false;', '    public override bool AllowGain(Mobile m, Skill skill, object obj) => true;'),
 ('travel', C, '        return Staff(m) && base.CheckTravel(m, newLocation, travelType, out message);', '        return base.CheckTravel(m, newLocation, travelType, out message);'),
 ('walkin', C, '        if (m is PlayerMobile pm && !Staff(m) && !Contains(oldLocation) && !Run.Players.ContainsKey(pm))', '        if (false)'),
 ('nopullback', C, '            Timer.DelayCall(TimeSpan.Zero, () => StaffColorWars.PullBack(pm, Run));', '            { }'),
 # logged out
 ('offlinehome', C, '            if (pm.Map == Map.Internal)\n', '            if (false)\n'),
 # the save
 ('noplayersave', C, '            if (p.Mobile != null)\n            {\n                run.Players[p.Mobile] = p;\n            }', '            { }'),
 ('anyversion', C, '        if (version is < 0 or > CurrentVersion)\n        {\n            throw new InvalidDataException($"StaffColorWarsStore', '        if (version < 0)\n        {\n            throw new InvalidDataException($"StaffColorWarsStore'),
 ('noregisterload', C, '        if (_pending is { } run && Active == null)', '        if (_pending is { } run && false)'),
 ('orphanstays', C, '    private void RemoveIfOrphaned()\n    {\n        if (!StaffColorWars.Owns(this))\n        {\n            Delete();\n        }\n    }\n}\n\n/// <summary>A team', '    private void RemoveIfOrphaned()\n    {\n    }\n}\n\n/// <summary>A team'),
 # the hub, the gump, the command, the settings
 ('nohubbutton', H, '        else if (id == BtnColorWars)\n', '        else if (id == -863)\n'),
 ('playergm', G, 'if (from.AccessLevel < AccessLevel.GameMaster || id == 0)', 'if (id == 0)'),
 ('nostartbutton', G, '            case BtnStart:\n', '            case 99:\n'),
 ('nocommand', G, '            CommandSystem.Register("ColorWars", AccessLevel.GameMaster, OnCommand);', '            { }'),
 ('norange', T, '        Range(s.CwWinTokens, 0, 10000, nameof(CwWinTokens), errors);\n', ''),
]
import sys
ONLY = sys.argv[2].split(',') if len(sys.argv) > 2 else None
if len(sys.argv) > 1:
    OUT = sys.argv[1]  # a new folder (round 2), so nothing is removed
elif os.path.isdir(OUT):
    shutil.rmtree(OUT)
for name, f, old, new in X:
    if ONLY and name not in ONLY:
        continue
    src = open(os.path.join(SRC, f), encoding='utf-8', newline='').read()
    n = src.count(old)
    if n != 1:
        raise SystemExit(f'{name}: pattern found {n} times')
    d = os.path.join(OUT, name)
    os.makedirs(d)
    open(os.path.join(d, f), 'w', encoding='utf-8', newline='').write(src.replace(old, new))
print(len(X), 'mutants')
