"""cc-P720 items 3, 4, 5: TutorialCorePlacement.cs and TutorialCoreTrials.cs (and TutorialVisionScene.cs's line).

- Item 3: each lesson's marker is a standing signpost (0xA854) named "Lesson N: <title>", beside its stop (SignSpot),
  not a rune on the stop. The signpost is impassable, which is why it moves off the stop. A marker placed before is
  turned into the sign and moved when the world loads, and by the seeder.
- Items 4-5: the bank's and the lodge's doors hang WestCCW: open, the door folds back into the wall line instead of
  swinging out past it (Chase 10-28). A door hung before is rehung by the seeder.
- Item 5: the League notice board in the lodge (opens the League's window: read about it without joining).
- Item 4: the bank lesson's arrow points at the bank's door until the trainee is inside, then at Merrin.
"""
import sys

CODE = sys.argv[1] + '/server/customizations/Tutorial/'


class F:
    def __init__(self, name):
        self.p = CODE + name
        self.s = open(self.p, encoding='utf-8').read()

    def rep(self, old, new, count=1):
        assert self.s.count(old) == count, (self.p, old[:90], self.s.count(old))
        self.s = self.s.replace(old, new)

    def save(self):
        open(self.p, 'w', encoding='utf-8', newline='').write(self.s)
        print('edited', self.p)


c = F('TutorialCorePlacement.cs')

c.rep('''    // cc-P718 item 5: the clothes stop's table''', '''    /// <summary>
    /// cc-P720 item 3: where each lesson's signpost stands, beside its stop. The standing signpost is impassable, so it
    /// cannot stand on the stop (the road runs through it). Each is the nearest tile to the stop that is off the walked
    /// route and the road, outside every building, clear of every spot, door and gate, fits a person, and leaves the stop
    /// reachable (shard-migration notes/cc-P720-tools/sign_spots.py, on the built isle).
    /// </summary>
    public static Point2D SignPoint(string key) => key switch
    {
        "core.movement" => new Point2D(6646, 3994),
        "core.backpack" => new Point2D(6656, 3992),
        "core.paperdoll" => new Point2D(6665, 3993),
        "core.chat" => new Point2D(6692, 3991),
        "core.farm" => new Point2D(6714, 3981),
        "core.death" => new Point2D(6736, 3996),
        "core.banking" => new Point2D(6762, 3982),
        "core.league" => new Point2D(6780, 3994),
        "core.loop" => new Point2D(6794, 3981),
        "core.travel" => new Point2D(6831, 3992),
        _ => new Point2D(MarkerSpot(key).X, MarkerSpot(key).Y)
    };

    public static Point3D SignSpot(string key) => Ground(SignPoint(key));

    /// <summary>cc-P720 item 3: the lesson sign's name, shown on a single click: "Lesson 5: The farm: ...".</summary>
    public static string SignName(string key)
    {
        var core = TutorialStations.Core.ToList();
        var i = core.FindIndex(s => s.Key == key);
        return i < 0 ? TutorialStations.Find(key)?.Title ?? key : $"Lesson {i + 1}: {core[i].Title}";
    }

    public const int OldMarkerId = 0x1F14; // the rune the markers were before cc-P720

    /// <summary>
    /// cc-P720 item 4: the practice bank's floor (inside its walls). The bank lesson's arrow points at the door until the
    /// trainee stands in here, then at Merrin.
    /// </summary>
    public static readonly Rectangle2D BankFloor = new(new Point2D(6758, 3973), new Point2D(6767, 3980));

    public static bool InBank(Point3D p) => BankFloor.Contains(new Point2D(p.X, p.Y));

    // cc-P720 item 5: the League's notice board, inside the lodge on its north wall, west of the door.
    public static readonly Point2D LeagueBoard = new(6780, 3996);

    // cc-P718 item 5: the clothes stop's table''')

c.rep('''        foreach (var item in map.GetItemsInRange<TutorialStationMarker>(MarkerSpot(key), 0))''',
      '''        foreach (var item in map.GetItemsInRange<TutorialStationMarker>(TutorialWorld.Ground(map, SignPoint(key)), 0))''')

c.rep('''    /// <summary>The practice bank's and the lodge's doors, both in an east-west wall (south and north walls).</summary>
    public static BaseDoor MakeDoor() => new DarkWoodDoor(DoorFacing.WestCW);
''', '''    /// <summary>
    /// The practice bank's and the lodge's doors, both in an east-west wall (south and north walls). cc-P720: hung
    /// WestCCW, so open the door folds back into the wall line (pinned offset -1, 0); WestCW swung it out past the wall
    /// (Chase 10-28).
    /// </summary>
    public static BaseDoor MakeDoor() => new DarkWoodDoor(DoorFacing.WestCCW);

    public const int DoorClosedId = 0x06A9; // DarkWoodDoor WestCCW, closed

    /// <summary>cc-P720: a door at <paramref name="spot"/> hung another way (before cc-P720), or null.</summary>
    private static BaseDoor? OldDoor(Map map, Point3D spot)
    {
        foreach (var door in map.GetItemsInRange<BaseDoor>(spot, 2))
        {
            var closed = door.Open ? new Point3D(door.X - door.Offset.X, door.Y - door.Offset.Y, door.Z - door.Offset.Z) : door.Location;
            if (!door.Deleted && closed == spot && door.ClosedId != DoorClosedId) { return door; }
        }
        return null;
    }

    /// <summary>cc-P720: moves every lesson marker still on its stop (a rune, before cc-P720) to its sign spot.</summary>
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
    }
''')

c.rep('''        var haven = HavenSpots.Map;
        var markers = TutorialStations.Core.Where(s => FindMarker(s.Key, map) == null).ToArray();''',
      '''        var haven = HavenSpots.Map;
        if (!dryRun) { MoveOldMarkers(map); } // cc-P720: a rune on its stop becomes the sign beside it
        var markers = TutorialStations.Core.Where(s => FindMarker(s.Key, map) == null).ToArray();''')

c.rep('''        var doors = new[] { Ground(TutorialWorld.BankDoor), Ground(TutorialWorld.LodgeDoor) }.Where(p => !HasDoor(map, p)).ToArray();''',
      '''        var doorSpots = new[] { Ground(TutorialWorld.BankDoor), Ground(TutorialWorld.LodgeDoor) };
        var rehung = doorSpots.Select(p => OldDoor(map, p)).Where(d => d != null).ToArray(); // cc-P720
        var doors = doorSpots.Where(p => !HasDoor(map, p) || rehung.Any(d => d!.Map == map && OldSpot(d) == p)).ToArray();
        var boardMissing = !HasItem<TutorialLeagueBoard>(map, Ground(LeagueBoard));''')

c.rep('''        // Preflight the whole requested surface before mutation. Markers are passable, so NPCs can share their tile.''',
      '''        // Preflight the whole requested surface before mutation. cc-P720: the markers are signposts beside the stops now
        // (impassable), on tiles no NPC, door or prop uses.''')
c.rep('''        foreach (var point in markers.Select(s => MarkerSpot(s.Key)).Concat(mobiles.Select(r => r.Spot))''',
      '''        foreach (var point in markers.Select(s => SignSpot(s.Key)).Concat(mobiles.Select(r => r.Spot))''')
c.rep('''                     .Concat(doors).Concat(props.Select(p => Ground(p.At))))''',
      '''                     .Concat(doors.Where(p => !rehung.Any(d => OldSpot(d!) == p))).Concat(props.Select(p => Ground(p.At)))
                     .Concat(boardMissing ? new[] { Ground(LeagueBoard) } : []))''')
c.rep('''        if (TileData.ItemTable[0x1F14].Impassable)
        { return "Tutorial: refused. The station marker art is impassable in this tiledata."; }

''', '')
c.rep('''            foreach (var station in markers)
            { new TutorialStationMarker(station.Key).MoveToWorld(MarkerSpot(station.Key), map); }''',
      '''            foreach (var station in markers)
            { new TutorialStationMarker(station.Key).MoveToWorld(TutorialWorld.Ground(map, SignPoint(station.Key)), map); }''')
c.rep('''            foreach (var spot in doors) { MakeDoor().MoveToWorld(spot, map); }''',
      '''            foreach (var d in rehung) { d!.Delete(); } // cc-P720: rehung WestCCW
            foreach (var spot in doors) { MakeDoor().MoveToWorld(spot, map); }
            if (boardMissing) { new TutorialLeagueBoard().MoveToWorld(Ground(LeagueBoard), map); }''')
c.rep('''{(gateMissing ? 1 : 0)} moongate, {tiles} walking tiles, {doors.Length} doors, {props.Length} props. {farm.Message}";''',
      '''{(gateMissing ? 1 : 0)} moongate, {tiles} walking tiles, {doors.Length} doors, {props.Length + (boardMissing ? 1 : 0)} props. {farm.Message}";''')

c.rep('''    /// <summary>cc-P718: removes the old wall-arm chat signpost''', '''    private static Point3D OldSpot(BaseDoor d) => d.Open ? new Point3D(d.X - d.Offset.X, d.Y - d.Offset.Y, d.Z - d.Offset.Z) : d.Location;

    /// <summary>cc-P718: removes the old wall-arm chat signpost''')

# the marker itself: a signpost
c.rep('''    public TutorialStationMarker(string key) : base(0x1F14)
    {
        _stationKey = key; Movable = false; Hue = TutorialStyle.SupplyHue;
        Name = TutorialStations.Find(key)?.Title ?? key;
    }
    // cc-P480: markers placed before were pale gray (0x482).
    [AfterDeserialization(false)] private void Brighten() => Hue = TutorialStyle.SupplyHue;''',
      '''    // cc-P720 item 3: a standing signpost with its board, named for the lesson (it was a blue rune on the stop).
    public TutorialStationMarker(string key) : base(TutorialCorePlacement.SignpostId)
    {
        _stationKey = key; Movable = false;
        Name = TutorialCorePlacement.SignName(key);
    }

    // cc-P720: a marker placed before (a rune on its stop) becomes the sign beside the stop once the world has loaded.
    [AfterDeserialization(false)] private void AsSign() => Timer.DelayCall(TimeSpan.Zero, MoveToSign);

    /// <summary>cc-P720: the signpost's art and name, at its sign spot on its own map.</summary>
    public void MoveToSign()
    {
        if (Deleted) { return; }
        ItemID = TutorialCorePlacement.SignpostId;
        Hue = 0;
        Name = TutorialCorePlacement.SignName(StationKey);
        if (Map is { } map && map != Map.Internal)
        {
            var at = TutorialWorld.Ground(map, TutorialCorePlacement.SignPoint(StationKey));
            if (Location != at) { MoveToWorld(at, map); }
        }
    }''')

c.rep('''// cc-P480 Part 3: the walking lesson's two marks''', '''/// <summary>
/// cc-P720 item 5: the League's notice board in the lodge. Double-click it to read about the League without joining: it
/// opens the League's own window, as Elara does (LeagueRegistrarGump), and finishes no lesson.
/// </summary>
[SerializationGenerator(0, false)]
public partial class TutorialLeagueBoard : Item
{
    public const string BoardName = "League notice board: read about the League";

    [Constructible]
    public TutorialLeagueBoard() : base(0x1E5E) { Movable = false; Name = BoardName; }

    public override void OnDoubleClick(Mobile from)
    {
        if (from is not PlayerMobile pm) { return; }
        if (!pm.InRange(Location, 3)) { pm.SendLocalizedMessage(500446); return; } // That is too far away.
        pm.SendGump(new LeagueRegistrarGump(pm));
    }
}

// cc-P480 Part 3: the walking lesson's two marks''')
c.save()

t = F('TutorialCoreTrials.cs')
t.rep('''        "core.loop" => "Follow the arrow up the knoll to the standing stones and double-click the bright blue rune stone. Watch the vision; it lasts under a minute, holds you still, and will not change your character.",''',
      '''        "core.loop" => "Follow the arrow up the knoll to the standing stones and double-click the lesson's signpost there. Watch the vision; it lasts under a minute, holds you still, and will not change your character.",''')
t.rep('''        "core.death" => t.Progress.Step == 0 ? TutorialCorePlacement.DeathSpot : TutorialCorePlacement.HealerSpot,
        _ => TutorialCorePlacement.Spot(t.Station.Key)''',
      '''        "core.death" => t.Progress.Step == 0 ? TutorialCorePlacement.DeathSpot : TutorialCorePlacement.HealerSpot,
        // cc-P720 item 4: the bank's door until the trainee is inside, then Merrin
        "core.banking" when !TutorialCorePlacement.InBank(t.Player.Location) => TutorialWorld.Ground(TutorialWorld.MapOf(t.Player) ?? TutorialWorld.Isle, TutorialWorld.BankDoor),
        _ => TutorialCorePlacement.Spot(t.Station.Key)''')
t.rep('''        Point(pm, Destination(trial), trial.Station.Title);''',
      '''        Point(pm, Destination(trial), ArrowLabel(trial));
        trial.ArrowAt = Destination(trial);''')
t.rep('''    private static Point3D Destination(Trial t) => t.Station.Key switch''',
      '''    // cc-P720 item 4: what the arrow is pointing at, named.
    private static string ArrowLabel(Trial t) => t.Station.Key == "core.banking"
        ? TutorialCorePlacement.InBank(t.Player.Location) ? "Merrin the banker" : "the practice bank's door"
        : t.Station.Title;

    private static Point3D Destination(Trial t) => t.Station.Key switch''')
t.rep('''        public int Ticks;
    }''', '''        public int Ticks;
        public Point3D ArrowAt; // cc-P720: where the arrow points now (the bank lesson moves it)
    }''')
t.rep('''            case "core.banking" when pm.Alive && trial.Supply?.IsChildOf(pm.FindBankNoCreate()) == true:
                Observe(pm, TutorialAction.Deposited);
                break;''', '''            case "core.banking" when pm.Alive && trial.Supply?.IsChildOf(pm.FindBankNoCreate()) == true:
                Observe(pm, TutorialAction.Deposited);
                break;
            case "core.banking" when Destination(trial) != trial.ArrowAt:
                // cc-P720 item 4: through the door, the arrow turns to Merrin (and back to the door on leaving)
                Point(pm, Destination(trial), ArrowLabel(trial));
                trial.ArrowAt = Destination(trial);
                break;''')
t.save()

v = F('TutorialVisionScene.cs')
v.rep('''"The vision fades. Double-click the bright blue rune stone to see it again."''',
      '''"The vision fades. Double-click the lesson's signpost by the stones to see it again."''')
v.save()
