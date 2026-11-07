# cc-P812: one folder per break under mutants/, each with the one mutated file. Each break must turn a fact red.
import os, shutil
SRC = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/'
OUT = 'D:/UO/golems/Iron/shard-migration/notes/cc-P812-tools/mutants'
D, A, T, V = 'StaffBuildTools/DecorCapture.cs', 'StaffBuildTools/AnimLocator.cs', 'StaffBuildTools/StaffBuildToolsSettings.cs', 'ClusterFVisualBuilder.cs'
X = [
 ('nofacing', D, '        if (item is BaseDoor door && FacingOf(door) is { } facing)', '        if (false && item is BaseDoor door && FacingOf(door) is { } facing)'),
 ('wrongfacing', D, '                if (probe?.ClosedId == door.ClosedId)', '                if (probe?.OpenedId == door.ClosedId)'),
 ('nohue', D, '        if (item.Hue != 0)\n        {\n            props.Add', '        if (false)\n        {\n            props.Add'),
 ('noname', D, '            props.Add($"Name={Clean(item.Name)}");', '            _ = item;'),
 ('noflatten', D, '        else if (item is AddonComponent || type.GetConstructor(Type.EmptyTypes) == null)', '        else if (type.GetConstructor(Type.EmptyTypes) == null)'),
 ('flatcount', D, '            if (flat)\n            {\n                flattened++;', '            if (false)\n            {\n                flattened++;'),
 ('opendoor', D, '                at = new Point3D(at.X - d.Offset.X, at.Y - d.Offset.Y, at.Z - d.Offset.Z);', '                _ = d;'),
 ('noskip', D, '            if (S.CaptureSkipTypes.Contains(t.Name))', '            if (false)'),
 ('nosizecap', D, '        if (x2 - x1 + 1 > S.CaptureMaxSide || y2 - y1 + 1 > S.CaptureMaxSide)', '        if (false)'),
 ('nopiececap', D, '        if (pieces.Count > S.CaptureMaxPieces)', '        if (false)'),
 ('norelative', D, '        var o = origin ?? Point3D.Zero;', '        var o = Point3D.Zero;'),
 ('lastcut', A, '        var action = run.Next++;', '        var action = run.Next++;\n        if (run.Next > run.Last) { Finish(run); return -1; }'),
 ('nonamecheck', D, '        if (bad != null)\n        {\n            return "Refused: " + bad + ".";\n        }\n\n        var pieces', '        var pieces'),
 ('nobuildhint', D, '? $"Build form: 0 0 0 is {origin.X} {origin.Y} {origin.Z}. Put it in server/data/Decoration/Builds and use [PlaceBuild {name}."', '? $"Build form."'),
 ('vbnocapture', V, '                    DecorCapture.Begin(from, e.GetString(1), !world);', '                    _ = world;'),
 ('typecount', A, '    public static int ActionCount(int body) => S.ActionsFor(new Body(body).Type);', '    public static int ActionCount(int body) => 22;'),
 ('noname2', A, '                return e.What;', '                return "?";'),
 ('nofirst', A, '        Step(run);\n        Timer.StartTimer', '        Timer.StartTimer'),
 ('keepstand', A, '        if (run.MadeStand)\n        {\n            run.Subject?.Delete();\n        }\n    }\n\n    public static bool Stop', '    }\n\n    public static bool Stop'),
 ('deltarget', A, '    public static void Finish(AnimRun run)\n    {\n        run.Timer.Cancel();', '    public static void Finish(AnimRun run)\n    {\n        run.Timer.Cancel();\n        run.Subject?.Delete();'),
 ('nostop', A, '        run.Timer.Cancel();\n        if (run.MadeStand)\n        {\n            run.Subject?.Delete();\n        }\n\n        return true;', '        return true;'),
 ('notfrozen', A, '        Frozen = true;\n        CantWalk', '        CantWalk'),
 ('gumpanyone', A, '        if (from.AccessLevel < AccessLevel.GameMaster)\n        {\n            return;\n        }\n\n        if (id == BtnPrev', '        if (id == BtnPrev'),
 ('standstays', A, '    private void AfterDeserialization() => Timer.DelayCall(TimeSpan.Zero, Delete);', '    private void AfterDeserialization() { }'),
 ('foldercheck', T, '            s.CaptureFolder.Contains(".."))', '            false)'),
 ('typecheck', T, '            if (!Enum.TryParse<BodyType>(type, out _))', '            if (false)'),
]
shutil.rmtree(OUT, ignore_errors=True)
n = 0
for name, f, old, new in X:
    s = open(SRC + f, encoding='utf-8', newline='').read()
    if '\r\n' in s:
        old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
    if s.count(old) != 1:
        print('NO MATCH', name, s.count(old)); continue
    d = os.path.join(OUT, name); os.makedirs(d)
    open(os.path.join(d, os.path.basename(f)), 'w', encoding='utf-8', newline='').write(s.replace(old, new)); n += 1
print(n, 'mutants')
