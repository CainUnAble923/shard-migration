# cc-P810: one folder per break under mutants/, each with the one mutated StaffHub file. Each break must turn a fact red.
import os, shutil
SRC = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/StaffHub'
OUT = 'D:/UO/golems/Iron/shard-migration/notes/cc-P810-tools/mutants'
E, M, G, T = 'StaffEggHunt.cs', 'StaffMineMaze.cs', 'StaffEventsGump.cs', 'StaffEventsSettings.cs'
X = [
 ('noarrow', E, '        pm.QuestArrow = new EggHuntArrow(pm, Egg.Location);\n', ''),
 ('arrowstaff', E, 'if (!Running || pm.AccessLevel > AccessLevel.Player || pm.Map != Egg.Map)', 'if (!Running || pm.Map != Egg.Map)'),
 ('arrowallmaps', E, 'if (!Running || pm.AccessLevel > AccessLevel.Player || pm.Map != Egg.Map)', 'if (!Running || pm.AccessLevel > AccessLevel.Player)'),
 ('tickskips', E, '        PointEveryone();\n    }\n\n    /// <summary>A double-click', '    }\n\n    /// <summary>A double-click'),
 ('twohunts', E, '        if (Running)\n        {\n            message = "An egg hunt is already running.";', '        if (false)\n        {\n            message = "An egg hunt is already running.";'),
 ('anyrange', E, ' || !pm.InRange(egg.GetWorldLocation(), S.EggClaimRange)', ''),
 ('ghostwins', E, '        if (!pm.Alive)\n', '        if (false)\n'),
 ('staffwins', E, 'if (from is not PlayerMobile pm || pm.AccessLevel > AccessLevel.Player)', 'if (from is not PlayerMobile pm)'),
 ('notokens', E, '        FestivalTokens.Grant(pm, S.EggTokens, "the egg hunt");\n', ''),
 ('neverexpires', E, '        if (Core.Now >= EndsAt)', '        if (false)'),
 ('eggstays', E, '    private void AfterDeserialization() => Timer.DelayCall(TimeSpan.Zero, Delete);', '    private void AfterDeserialization() { }'),
 ('arrowstays', E, '                arrow.Stop();\n', ''),
 ('nopath', M, '            Mark(step, lane);\n\n', '\n'),
 ('fixedseed', M, '        var rng = new System.Random(Seed);', '        var rng = new System.Random(1);'),
 ('minestart', M, '        for (var step = 1; step < Length - 1; step++)', '        for (var step = 0; step < Length - 1; step++)'),
 ('nosizecheck', M, 'if (Math.Min(w, h) < S.MazeMinSide || w * h > S.MazeMaxTiles)', 'if (false)'),
 ('twomazes', M, '        if (Active != null)\n        {\n            message = "A mine maze is already laid out. End it first.";', '        if (false)\n        {\n            message = "A mine maze is already laid out. End it first.";'),
 ('wrongend', M, 'run.FromLow = run.AlongX ? first.X == run.X1 : first.Y == run.Y1;', 'run.FromLow = !(run.AlongX ? first.X == run.X1 : first.Y == run.Y1);'),
 ('nounregister', M, '        run.Region?.Unregister();\n        Active = null;\n        message = $"Mine maze removed.', '        Active = null;\n        message = $"Mine maze removed.'),
 ('noblast', M, '            Blast(pm, run);\n', '            { }\n'),
 ('lootable', M, '                pack.DropItem(item);\n            }\n        }\n\n        pm.SendMessage(0x44, $"Your belongings', '            }\n        }\n\n        pm.SendMessage(0x44, $"Your belongings'),
 ('norevive', M, '        pm.Resurrect();\n', ''),
 ('fourwinners', M, '        if (run.Winners.Count >= S.MazeWinners)', '        if (run.Winners.Count > S.MazeWinners)'),
 ('twiceprize', M, '        if (run.Winners.Contains(pm))\n        {\n            return;\n        }\n', ''),
 ('anyentry', M, '            if (!Run.IsStart(newLocation.X, newLocation.Y))', '            if (false)'),
 ('younglets', M, '            if (m is PlayerMobile { Young: true })', '            if (false)'),
 ('travel', M, '        return Exempt(m) && base.CheckTravel(m, newLocation, travelType, out message);', '        return base.CheckTravel(m, newLocation, travelType, out message);'),
 ('resetkeeps', M, '        run.Winners.Clear();\n\n        foreach', '\n        foreach'),
 ('resetstay', M, '                m.MoveToWorld(run.StartSpot(), run.Map);\n            }\n        }\n\n        World.Broadcast', '            }\n        }\n\n        World.Broadcast'),
 ('nowinnersave', M, '            if (r.ReadEntity<Mobile>() is { } m)\n            {\n                run.Winners.Add(m);\n            }', '            r.ReadEntity<Mobile>();'),
 ('anyversion', M, '        if (version is < 0 or > CurrentVersion)\n        {\n            throw new InvalidDataException($"StaffMineMazeStore', '        if (version < 0)\n        {\n            throw new InvalidDataException($"StaffMineMazeStore'),
 ('noregisterload', M, '        if (_pending is { } run && Active == null)', '        if (_pending is { } run && false)'),
 ('playergm', G, 'if (from.AccessLevel < AccessLevel.GameMaster || id == 0)', 'if (id == 0)'),
 ('eggbutton', G, '            case BtnEggHere:\n                Say', '            case 99:\n                Say'),
 ('prizecheck', T, '        if (!s.PrizeIsBox && !(s.MazePrize ?? "").Equals("Tokens", StringComparison.OrdinalIgnoreCase))', '        if (false)'),
]
shutil.rmtree(OUT, ignore_errors=True)
n = 0
for name, f, old, new in X:
    s = open(os.path.join(SRC, f), encoding='utf-8').read()
    if s.count(old) != 1:
        print('NO MATCH', name, s.count(old)); continue
    d = os.path.join(OUT, name); os.makedirs(d)
    open(os.path.join(d, f), 'w', encoding='utf-8', newline='').write(s.replace(old, new)); n += 1
print(n, 'mutants')
