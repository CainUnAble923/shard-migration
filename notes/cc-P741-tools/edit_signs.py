"""cc-P741 item 3: the lesson signs north of their paths, in TutorialCorePlacement.cs (run once)."""
import re
p = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/TutorialCorePlacement.cs'
s = open(p, encoding='utf-8').read()


def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)


rep('''    /// <summary>
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
        "core.healing" => HealingSign,
        "core.death" => new Point2D(6736, 3996),
        "core.banking" => new Point2D(6762, 3982),
        "core.league" => new Point2D(6780, 3994),
        "core.loop" => new Point2D(6794, 3981),
        "core.travel" => new Point2D(6831, 3992),''',
    '''    /// <summary>
    /// cc-P720 item 3: where each lesson's signpost stands, beside its stop. The standing signpost is impassable, so it
    /// cannot stand on the stop (the road runs through it). Each is the nearest tile to the stop that is off the walked
    /// route and the road, outside every building, clear of every spot, door and gate, fits a person, and leaves the stop
    /// reachable. cc-P741 (Chase 10-30: "all signs should be north of path"): and north of its path, beside it, so its
    /// board (0xA854 reads from the south) faces the path as a trainee walks up; the travel lesson's sign stands where
    /// the road meets the dock, clear of the moongate frame's glow, where it is seen before the dock (Chase: "sign next
    /// to moongate at end is hard to see"). shard-migration notes/cc-P741-tools/sign_spots741.py, on the built isle.
    /// </summary>
    public static Point2D SignPoint(string key) => key switch
    {
        "core.movement" => new Point2D(6646, 3990),
        "core.backpack" => new Point2D(6656, 3988),
        "core.paperdoll" => new Point2D(6665, 3989),
        "core.chat" => new Point2D(6691, 3987),
        "core.farm" => new Point2D(6698, 3978),
        "core.healing" => HealingSign,
        "core.death" => new Point2D(6736, 3989),
        "core.banking" => new Point2D(6766, 3981),
        "core.league" => new Point2D(6782, 3989),
        "core.loop" => new Point2D(6794, 3981),
        "core.travel" => new Point2D(6811, 3988),''')
rep('''    /// <summary>
    /// cc-P726: the healing lesson's signpost, outside the farmhouse door (6690,3978) to the south-west, clear of its steps
    /// (6689-6691,3979) and its own sign (6692,3979). The seeder's fit check refuses the isle if it is blocked.
    /// </summary>
    public static readonly Point2D HealingSign = new(6688, 3980);''',
    '''    /// <summary>
    /// cc-P726: the healing lesson's signpost, outside the farmhouse door. cc-P741: the farmhouse moved east (door
    /// 6702,3978, steps 6701-6703,3979): the sign stands south-west of the steps, north of the road, clear of the door's
    /// line. The seeder's fit check refuses the isle if it is blocked.
    /// </summary>
    public static readonly Point2D HealingSign = new(6701, 3980);''')
rep('''    public static readonly Point2D ChatSignpost = new(TutorialWorld.Signpost.X, TutorialWorld.Signpost.Y - 2);''',
    '''    // cc-P741: north of the road (it stood on the road's edge, 2 north of the stop), beside the chat lesson's own sign.
    public static readonly Point2D ChatSignpost = new(TutorialWorld.Signpost.X - 2, TutorialWorld.Signpost.Y - 4);
    public static readonly Point2D OldChatSignpostSpot = new(TutorialWorld.Signpost.X, TutorialWorld.Signpost.Y - 2);''')
rep('''        if (!dryRun) { TutorialFarm.MoveFromOldLayout(map); }''',
    '''        if (!dryRun) { MoveChatSignpost(map); } // cc-P741: before the props are counted, so it is moved, not doubled
        if (!dryRun) { TutorialFarm.MoveFromOldLayout(map); }''')
rep('''    private static void Place(Mobile m, Point3D spot, Map map)''',
    '''    /// <summary>cc-P741: moves the farm signpost from its spot before (on the road's edge) to north of the road.</summary>
    public static int MoveChatSignpost(Map map)
    {
        var old = new List<Item>();
        foreach (var i in map.GetItemsInRange<Static>(Ground(OldChatSignpostSpot), 0))
        { if (!i.Deleted && i.ItemID == SignpostId && i.Name == ChatSignpostName) { old.Add(i); } }
        if (HasItem<Static>(map, Ground(ChatSignpost), i => i.ItemID == SignpostId && i.Name == ChatSignpostName))
        {
            foreach (var i in old) { i.Delete(); }
            return old.Count;
        }
        foreach (var i in old.Take(1)) { i.MoveToWorld(Ground(ChatSignpost), map); }
        foreach (var i in old.Skip(1)) { i.Delete(); }
        return old.Count;
    }

    private static void Place(Mobile m, Point3D spot, Map map)''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
