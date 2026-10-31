"""cc-P741: every lesson sign moves to its spot before the seeder looks for it (run once). The seed on load placed 10
new signs on a world laid before cc-P741: P720's MoveOldMarkers moves only a marker still on its stop, and the signs
stood beside their stops at P720's spots."""
p = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/TutorialCorePlacement.cs'
s = open(p, encoding='utf-8').read()
old = '''    /// <summary>cc-P720: moves every lesson marker still on its stop (a rune, before cc-P720) to its sign spot.</summary>
    public static int MoveOldMarkers(Map map)
    {
        var moved = new List<TutorialStationMarker>();
        foreach (var station in TutorialStations.Core)
        {
            foreach (var item in map.GetItemsInRange<TutorialStationMarker>(TutorialWorld.Ground(map, new Point2D(MarkerSpot(station.Key).X, MarkerSpot(station.Key).Y)), 0))
            {
                if (!item.Deleted && item.StationKey == station.Key && item.Location != TutorialWorld.Ground(map, SignPoint(station.Key))) { moved.Add(item); }
            }
        }
        foreach (var m in moved) { m.MoveToSign(); }
        return moved.Count;
    }'''
new = '''    /// <summary>
    /// cc-P720: moves every lesson marker still on its stop (a rune, before cc-P720) to its sign spot. cc-P741: every
    /// lesson marker anywhere on the isle that is not at its sign spot (the signs moved north of their paths), and one
    /// sign per lesson: a second one for a lesson is removed. Returns how many it moved or removed.
    /// </summary>
    public static int MoveOldMarkers(Map map)
    {
        var moved = new List<TutorialStationMarker>();
        var seen = new Dictionary<string, TutorialStationMarker>();
        var extra = new List<TutorialStationMarker>();
        var all = new List<TutorialStationMarker>();
        foreach (var item in map.GetItemsInRange<TutorialStationMarker>(TutorialWorld.Ground(map, IsleCentre), IsleReach))
        {
            if (!item.Deleted && item.StationKey != null) { all.Add(item); }
        }

        // the one already at its spot is kept first
        foreach (var item in all.OrderBy(i => i.Location == TutorialWorld.Ground(map, SignPoint(i.StationKey)) ? 0 : 1))
        {
            if (seen.ContainsKey(item.StationKey)) { extra.Add(item); continue; }
            seen[item.StationKey] = item;
            if (item.Location != TutorialWorld.Ground(map, SignPoint(item.StationKey))) { moved.Add(item); }
        }
        foreach (var m in extra) { m.Delete(); }
        foreach (var m in moved) { m.MoveToSign(); }
        return moved.Count + extra.Count;
    }

    /// <summary>cc-P741: the isle's middle and a reach that covers it all (x 6594-6865, y 3905-4049).</summary>
    public static readonly Point2D IsleCentre = new(6730, 3977);
    public const int IsleReach = 140;'''
assert old in s
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf-8', newline='\n').write(s)

p = 'D:/UO/golems/Iron/ShatteredLegacy/server/tests/Tutorial/TutorialIsleCoastVerification.cs'
s = open(p, encoding='utf-8').read()
old = '''//   4. The chat lesson's farm signpost, laid on the road's edge before, is moved north of the road, not doubled.'''
new = '''//   4. The chat lesson's farm signpost, laid on the road's edge before, is moved north of the road, not doubled.
//   5. A lesson sign standing where P720 put it is moved north of its path by the next seeding, not doubled.'''
assert old in s
s = s.replace(old, new, 1)
old = '''    [Fact]
    public void TheChatSignpostIsMovedNorthOfTheRoadNotDoubled()'''
new = '''    [Fact]
    public void ALessonSignFromBeforeIsMovedNorthOfItsPathNotDoubled()
    {
        var map = SeededCopy();
        try
        {
            // P720's spots: the movement lesson's south of the road, the death lesson's inside the yard's gate
            var before = new Dictionary<string, Point2D> { ["core.movement"] = new(6646, 3994), ["core.death"] = new(6736, 3996) };
            foreach (var (key, at) in before)
            {
                var sign = TutorialCorePlacement.FindMarker(key, map)!;
                sign.MoveToWorld(TutorialWorld.Ground(map, at), map);
            }

            TutorialCorePlacement.SeedOn(map, false, false);

            var signs = Items<TutorialStationMarker>(map);
            Assert.Equal(TutorialStations.Core.Count(), signs.Count);
            foreach (var key in before.Keys)
            {
                var one = Assert.Single(signs, m => m.StationKey == key);
                Assert.Equal(TutorialCorePlacement.SignSpot(key).X, one.X);
                Assert.Equal(TutorialCorePlacement.SignSpot(key).Y, one.Y);
            }
        }
        finally
        {
            TutorialCopies.Reset(LastSlot);
        }
    }

    [Fact]
    public void TheChatSignpostIsMovedNorthOfTheRoadNotDoubled()'''
assert old in s
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
