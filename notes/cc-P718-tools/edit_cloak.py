import os
os.chdir(r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations\Tutorial")


def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


edit("TutorialTrialProgress.cs", [
("""    FarmDone // cc-P663: Wren's three steps (TutorialFarm.StepOf reaches 4)
}""", """    FarmDone, // cc-P663: Wren's three steps (TutorialFarm.StepOf reaches 4)
    OpenedPaperdoll // cc-P718: the trainee opened their own character window (EventSink.PaperdollRequest)
}"""),
("""            "core.backpack" => [TutorialAction.OpenedBag],""", """            // cc-P718 item 4: new clients start with the character window closed, and the backpack lesson is the first
            // that needs it, so it is opened first.
            "core.backpack" => [TutorialAction.OpenedPaperdoll, TutorialAction.OpenedBag],"""),
])

edit("TutorialCorePlacement.cs", [
("""        "core.paperdoll" => Ground(TutorialWorld.Rack),
        "core.chat" => Ground(TutorialWorld.Signpost),""", """        "core.paperdoll" => Ground(ClothesTable), // cc-P718: the table the cloak lies on
        "core.chat" => Ground(ChatSignpost), // cc-P718: the post itself, not the stop in front of it"""),
("""        "core.movement" => Ground(new Point2D(TutorialWorld.BlueTile.X, TutorialWorld.BlueTile.Y + 1)),""", """        "core.movement" => Ground(new Point2D(TutorialWorld.BlueTile.X, TutorialWorld.BlueTile.Y + 1)),
        "core.paperdoll" => Ground(TutorialWorld.Rack),
        "core.chat" => Ground(TutorialWorld.Signpost),"""),
("""    // The stops' props (all stock art, server items so P662's statics stay the map's own): id, spot, name.
    public static readonly (int Id, Point2D At, string Name)[] Props =
    [
        (0x0DE3, new Point2D(TutorialWorld.Camp.X - 1, TutorialWorld.Camp.Y - 2), "campfire"),
        (0x0A55, new Point2D(TutorialWorld.Camp.X + 1, TutorialWorld.Camp.Y - 2), "bedroll"),
        (0x0A55, new Point2D(TutorialWorld.Camp.X + 2, TutorialWorld.Camp.Y - 2), "bedroll"),
        (0x0EC6, new Point2D(TutorialWorld.Rack.X, TutorialWorld.Rack.Y - 2), "clothes rack"),
        (0x0B97, new Point2D(TutorialWorld.Signpost.X, TutorialWorld.Signpost.Y - 2), "signpost: the farm, east"),
        (0x0E7C, TutorialWorld.BankBox, "practice bank box")
    ];""", """    // cc-P718 item 5: the clothes stop's table, beside the rack, where each trainee's cloak waits.
    public static readonly Point2D ClothesTable = new(TutorialWorld.Rack.X - 1, TutorialWorld.Rack.Y - 2);
    public const int TableId = 0x0B8F; // "table": a surface 6 high
    public const int TableHeight = 6;

    // cc-P718 item 6: a standing post with its sign board (0xA854, "sign_post"), where the chat lesson's post stood. The
    // old art, 0x0B97, is the arm that hangs a shop sign from a wall: on the ground it read as debris (Chase, 10-28).
    public static readonly Point2D ChatSignpost = new(TutorialWorld.Signpost.X, TutorialWorld.Signpost.Y - 2);
    public const int SignpostId = 0xA854;
    public const string ChatSignpostName = "Farm signpost: say 'I am ready to learn'";
    public const int OldSignpostId = 0x0B97;
    public const string OldChatSignpostName = "signpost: the farm, east";

    // The stops' props (all stock art, server items so P662's statics stay the map's own): id, spot, name.
    public static readonly (int Id, Point2D At, string Name)[] Props =
    [
        (0x0DE3, new Point2D(TutorialWorld.Camp.X - 1, TutorialWorld.Camp.Y - 2), "campfire"),
        (0x0A55, new Point2D(TutorialWorld.Camp.X + 1, TutorialWorld.Camp.Y - 2), "bedroll"),
        (0x0A55, new Point2D(TutorialWorld.Camp.X + 2, TutorialWorld.Camp.Y - 2), "bedroll"),
        (0x0EC6, new Point2D(TutorialWorld.Rack.X, TutorialWorld.Rack.Y - 2), "clothes rack"),
        (TableId, ClothesTable, "table"),
        (SignpostId, ChatSignpost, ChatSignpostName),
        (0x0E7C, TutorialWorld.BankBox, "practice bank box")
    ];"""),
("""        var props = Props.Where(p => !HasItem<Item>(map, Ground(p.At), i => i.ItemID == p.Id && i.Name == p.Name)).ToArray();
""", """        var props = Props.Where(p => !HasItem<Item>(map, Ground(p.At), i => i.ItemID == p.Id && i.Name == p.Name)).ToArray();
        // cc-P718: the old wall-arm signpost a seeded world still has makes way for the standing one.
        var oldSignposts = new List<Item>();
        foreach (var i in map.GetItemsInRange<Static>(Ground(ChatSignpost), 0))
        { if (!i.Deleted && i.ItemID == OldSignpostId && i.Name == OldChatSignpostName) { oldSignposts.Add(i); } }
"""),
("""            foreach (var (id, at, name) in props) { new Static(id) { Name = name }.MoveToWorld(Ground(at), map); }""",
 """            foreach (var old in oldSignposts) { old.Delete(); }
            foreach (var (id, at, name) in props) { new Static(id) { Name = name }.MoveToWorld(Ground(at), map); }"""),
("""[SerializationGenerator(0, false)]
public partial class TutorialBankToken : Item""", """/// <summary>
/// cc-P718 items 2 and 5: the clothes lesson's cloak. It waits on the table at the clothes stop, for its trainee alone, and
/// is theirs to keep: blessed (kept on death), and Nontransferable, so it cannot be sold, traded, banked, handed over or
/// dropped (pinned Item: OnDroppedToWorld, OnDroppedInto anything but the backpack, OnDroppedToMobile; GenericSellInfo
/// .IsSellable). Nothing takes it back at graduation, the skip or leaving the isle. No bonus (the notes propose one).
/// </summary>
[SerializationGenerator(0, false)]
public partial class WakeningIsleCloak : Cloak
{
    public const string CloakName = "cloak of the Wakening Isle";

    [SerializableField(0)]
    [SerializedCommandProperty(AccessLevel.GameMaster)]
    private Mobile? _owner;

    [Constructible]
    public WakeningIsleCloak() : this(null) { }

    public WakeningIsleCloak(Mobile? owner)
    {
        _owner = owner;
        Name = CloakName;
        Hue = TutorialStyle.SupplyHue;
        LootType = LootType.Blessed;
    }

    public override bool Nontransferable => true;

    public override void HandleInvalidTransfer(Mobile from) =>
        from.SendMessage(0x3B2, "Your cloak of the Wakening Isle is yours alone. Keep it in your backpack or wear it.");

    // Lying on the table, only its trainee (and staff) can pick it up.
    public override bool CheckLift(Mobile from, Item item, ref LRReason reject)
    {
        if (Parent == null && Owner != null && from != Owner && from.AccessLevel == AccessLevel.Player)
        {
            from.SendMessage(0x3B2, "That cloak is waiting for another trainee.");
            reject = LRReason.Inspecific;
            return false;
        }

        return base.CheckLift(from, item, ref reject);
    }

    /// <summary>The isle cloak <paramref name="pm"/> has on them (worn or anywhere in the backpack), or null.</summary>
    public static WakeningIsleCloak? On(PlayerMobile pm) =>
        pm.FindItemOnLayer(Layer.Cloak) as WakeningIsleCloak ?? pm.Backpack?.FindItemByType<WakeningIsleCloak>();

    /// <summary>The cloak waiting on the clothes table for <paramref name="pm"/> on <paramref name="map"/>, or null.</summary>
    public static WakeningIsleCloak? OnTable(PlayerMobile pm, Map map)
    {
        foreach (var c in map.GetItemsInRange<WakeningIsleCloak>(TutorialWorld.Ground(map, TutorialCorePlacement.ClothesTable), 0))
        {
            if (!c.Deleted && c.Parent == null && c.Owner == pm) { return c; }
        }
        return null;
    }

    /// <summary>
    /// One cloak per character: when <paramref name="pm"/> has none on them and none waits on the table, a new one is set
    /// on the table. Returns the cloak waiting on the table (new or old), or null when they already have theirs.
    /// </summary>
    public static WakeningIsleCloak? EnsureOnTable(PlayerMobile pm)
    {
        if (On(pm) != null) { return null; }
        var map = TutorialWorld.MapOf(pm);
        if (map == null) { return null; }
        if (OnTable(pm, map) is { } waiting) { return waiting; }
        var cloak = new WakeningIsleCloak(pm);
        var table = TutorialWorld.Ground(map, TutorialCorePlacement.ClothesTable);
        cloak.MoveToWorld(new Point3D(table.X, table.Y, table.Z + TutorialCorePlacement.TableHeight), map);
        return cloak;
    }
}

[SerializationGenerator(0, false)]
public partial class TutorialBankToken : Item"""),
])

# The lessons: the cloak is no longer a backpack supply; the paperdoll comes first in the backpack lesson.
edit("TutorialCoreTrials.cs", [
("""        "core.backpack" => "Follow the arrow to the camp beside the road. Double-click your character to open the character window, then double-click its backpack picture. Inside your backpack, double-click the blue practice bag.",
        "core.paperdoll" => "Follow the arrow to the clothes rack. Double-click your character to open the character window, then drag the blue practice cloak from your backpack onto your character's picture. If you already wear a cloak, drag it into your backpack first.",""",
 """        "core.backpack" => "Follow the arrow to the camp beside the road. First open your character window: double-click your own character (two quick left clicks on yourself), or click the paperdoll button. Then double-click the backpack picture in that window, and inside your backpack double-click the blue practice bag.",
        "core.paperdoll" => "Follow the arrow to the table by the clothes rack: your blue cloak of the Wakening Isle lies on it. To move a thing, click it, hold the left mouse button down, move the mouse, and let go: that is drag and drop. Drag the cloak onto your character's picture in the character window to wear it, or into your backpack first and double-click it there. If you already wear a cloak, drag it into your backpack first. The cloak is yours to keep.","""),
("""        "core.paperdoll" => new TutorialPracticeCloak(),
""", ""),
("""        Timer.StartTimer(TimeSpan.FromMilliseconds(250), TimeSpan.FromMilliseconds(250), () => Tick(trial), out trial.Timer);""",
 """        if (station.Key == "core.paperdoll") { WakeningIsleCloak.EnsureOnTable(pm); } // cc-P718: on the table, not in the bag
        Timer.StartTimer(TimeSpan.FromMilliseconds(250), TimeSpan.FromMilliseconds(250), () => Tick(trial), out trial.Timer);"""),
("""    private static void Show(PlayerMobile pm, Trial trial)
    {
        Resupply(pm, trial);""", """    private static void Show(PlayerMobile pm, Trial trial)
    {
        Resupply(pm, trial);
        if (trial.Station.Key == "core.paperdoll") { WakeningIsleCloak.EnsureOnTable(pm); } // cc-P718: a lost cloak comes back"""),
("""            case "core.paperdoll" when pm.Alive && trial.Supply?.Parent == pm:
                Observe(pm, TutorialAction.Equipped);
                break;""", """            case "core.paperdoll" when pm.Alive && pm.FindItemOnLayer(Layer.Cloak) is WakeningIsleCloak:
                Observe(pm, TutorialAction.Equipped);
                break;"""),
("""        _hooked = true;
        EventSink.Speech += OnSpeech;
    }""", """        _hooked = true;
        EventSink.Speech += OnSpeech;
        EventSink.PaperdollRequest += OnPaperdollRequest; // cc-P718 item 4
    }

    // cc-P718 item 4: the trainee opened their own character window (a double-click on themselves, or the client's
    // paperdoll button: both reach Mobile.DisplayPaperdollTo, which raises PaperdollRequest).
    private static void OnPaperdollRequest(Mobile beholder, Mobile beheld)
    {
        if (beholder == beheld && beholder is PlayerMobile { Alive: true } pm && IsDoing(pm, "core.backpack") &&
            Current(pm)!.Progress.Step == 0)
        {
            Observe(pm, TutorialAction.OpenedPaperdoll);
            ClusterFTutorial.SystemLine(pm, "That is your character window. Now double-click the backpack picture in it, then double-click the blue practice bag inside your backpack.");
        }
    }"""),
])
print("ok")
