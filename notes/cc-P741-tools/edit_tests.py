"""cc-P741: the existing tests that pin the farm's and the signs' old places (run once)."""
p = 'D:/UO/golems/Iron/ShatteredLegacy/server/tests/Tutorial/TutorialIsleWalkFixes2Verification.cs'
s = open(p, encoding='utf-8').read()


def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)


rep('''        // The cottage: walls x 6687-6693, y 3972-3978, its door in the south wall.
        var house = TutorialIsleFarmLayout.Pieces.Where(p => p.X is >= 6687 and <= 6693 && p.Y is >= 3972 and <= 3978).ToArray();''',
    '''        // The cottage: walls x 6699-6705, y 3972-3978 (cc-P741: east of the field), its door in the south wall.
        var house = TutorialIsleFarmLayout.Pieces.Where(p => p.X is >= 6699 and <= 6705 && p.Y is >= 3972 and <= 3978).ToArray();''')
rep('''        Assert.Equal(new Point3D(6690, 3978, 7), TutorialIsleFarmLayout.DoorSpot);''',
    '''        Assert.Equal(new Point3D(6702, 3978, 7), TutorialIsleFarmLayout.DoorSpot);''')
rep('''        var oldDoor = new DarkWoodDoor(DoorFacing.SouthCW);
        oldDoor.MoveToWorld(TutorialIsleFarmLayout.OldDoorSpot, isle);''',
    '''        var oldDoor = new DarkWoodDoor(DoorFacing.SouthCW);
        oldDoor.MoveToWorld(TutorialIsleFarmLayout.OldDoorSpots[0], isle);
        var p720Door = new DarkWoodDoor(DoorFacing.WestCW); // cc-P741: the cottage's door before it moved east
        p720Door.MoveToWorld(TutorialIsleFarmLayout.OldDoorSpots[1], isle);''')
rep('''        Assert.True(oldDoor.Deleted);''', '''        Assert.True(oldDoor.Deleted);
        Assert.True(p720Door.Deleted);''')
rep('''        var field = Ring(6695, 3967, 6713, 3983);
        var pen = Ring(6706, 3967, 6713, 3973);''',
    '''        var field = Ring(6677, 3967, 6695, 3983); // cc-P741: 18 west of P720's
        var pen = Ring(6688, 3967, 6695, 3973);''')
rep('''            Assert.NotEqual((at.X, at.Y), (sign.X, sign.Y)); // beside the stop, never on it
            Assert.True(Math.Max(Math.Abs(at.X - sign.X), Math.Abs(at.Y - sign.Y)) <= 2);''',
    '''            Assert.NotEqual((at.X, at.Y), (sign.X, sign.Y)); // beside the stop, never on it
            // cc-P741: north of its path, which puts a sign across the road from a stop south of it (the yard's, 6
            // north), and the travel lesson's where the road meets the dock (TutorialCorePlacement.DockRoadEnd)
            var near = key == "core.travel" ? TutorialCorePlacement.DockRoadEnd : new Point2D(at.X, at.Y);
            Assert.True(Math.Max(Math.Abs(near.X - sign.X), Math.Abs(near.Y - sign.Y)) <= 6, $"{key}'s sign at {sign.Location}");''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)

p = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/TutorialCorePlacement.cs'
s = open(p, encoding='utf-8').read()
rep('''    public static Point3D SignSpot(string key) => Ground(SignPoint(key));''',
    '''    public static Point3D SignSpot(string key) => Ground(SignPoint(key));

    /// <summary>cc-P741: where the road meets the dock; the travel lesson's sign stands north of it.</summary>
    public static readonly Point2D DockRoadEnd = new(6811, 3991);''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
