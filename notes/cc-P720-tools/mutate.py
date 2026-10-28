"""cc-P720 red runs: writes a copy of the customizations the probe mounts with old behaviour put back, the new API kept.

    python -P mutate.py <customizations> <out folder> <old|fine> <original TutorialIsleFarmLayout.cs>

old   every item as before P720: P663's farm layout (the hillside cottage, the old fence) and no relaying of an old
      farm; the rune markers on their stops, named by title, never moved; the doors hung WestCW and never rehung; no
      League board; the bank arrow on Merrin from the start
fine  the new layout and doors, but: the signs named by title alone; the bank arrow never turns to Merrin; an old farm
      is kept
"""
import os, re, shutil, sys

src, out, kind, old_layout = sys.argv[1:5]
if os.path.exists(out):
    shutil.rmtree(out)
os.makedirs(out)
for name in ('Tutorial', 'Fold'):
    shutil.copytree(os.path.join(src, name), os.path.join(out, name))
for name in ('LeagueRegistrar.cs', 'ClusterFSkillGain.cs'):
    shutil.copy(os.path.join(src, name), os.path.join(out, name))
T = os.path.join(out, 'Tutorial')


def edit(name, pairs):
    p = os.path.join(T, name)
    s = open(p, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) >= 1, (name, a[:80])
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='').write(s)


if kind == 'old':
    lay = open(old_layout, encoding='utf-8').read()
    lay = lay.replace('    /// <summary>Every piece:', '    public static readonly Point3D OldDoorSpot = new(6694, 3975, 13);\n\n    /// <summary>Every piece:')
    open(os.path.join(T, 'TutorialIsleFarmLayout.cs'), 'w', encoding='utf-8', newline='').write(lay)
    edit('TutorialFarm.cs', [
        ('            return wanted.SequenceEqual(placed);', '            return true;'),
        ('new DarkWoodDoor(DoorFacing.WestCW);', 'new DarkWoodDoor(DoorFacing.SouthCW);'),
    ])
    edit('TutorialCorePlacement.cs', [
        ('    public static Point2D SignPoint(string key) => key switch',
         '    public static Point2D SignPoint(string key) => new Point2D(MarkerSpot(key).X, MarkerSpot(key).Y);\n    public static Point2D SignPointUnused(string key) => key switch'),
        ('return i < 0 ? TutorialStations.Find(key)?.Title ?? key : $"Lesson {i + 1}: {core[i].Title}";',
         'return TutorialStations.Find(key)?.Title ?? key;'),
        ('    public TutorialStationMarker(string key) : base(TutorialCorePlacement.SignpostId)',
         '    public TutorialStationMarker(string key) : base(TutorialCorePlacement.OldMarkerId)'),
        ('        if (Deleted) { return; }\n        ItemID = TutorialCorePlacement.SignpostId;',
         '        return;\n        ItemID = TutorialCorePlacement.SignpostId;'),
        ('new DarkWoodDoor(DoorFacing.WestCCW);', 'new DarkWoodDoor(DoorFacing.WestCW);'),
        ('closed == spot && door.ClosedId != DoorClosedId', 'closed == spot && false'),
        ('        var boardMissing = !HasItem<TutorialLeagueBoard>(map, Ground(LeagueBoard));', '        var boardMissing = false;'),
    ])
    edit('TutorialCoreTrials.cs', [
        ('"core.banking" when !TutorialCorePlacement.InBank(t.Player.Location)', '"core.banking" when false'),
    ])
elif kind == 'fine':
    edit('TutorialFarm.cs', [('            return wanted.SequenceEqual(placed);', '            return true;')])
    edit('TutorialCorePlacement.cs', [
        ('return i < 0 ? TutorialStations.Find(key)?.Title ?? key : $"Lesson {i + 1}: {core[i].Title}";',
         'return TutorialStations.Find(key)?.Title ?? key;')])
    edit('TutorialCoreTrials.cs', [('            case "core.banking" when Destination(trial) != trial.ArrowAt:',
                                    '            case "core.banking" when false && Destination(trial) != trial.ArrowAt:')])
else:
    raise SystemExit('unknown ' + kind)
print('mutant', kind, 'in', out)
