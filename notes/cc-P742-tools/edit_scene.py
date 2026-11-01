"""cc-P742: the loop vision moves into the dungeon shrine (TutorialVisionChamber). Edits TutorialVisionScene.cs:
- Play takes a free chamber slot; the first beat builds the room, hides the player and moves them in (frozen, facing the
  pedestal), in the dark;
- the beats use the chamber's spots: the Stranger walks from the north-west corner to the Gem, faces it (south-east,
  toward the onlooker), strikes twice, and at Shards the Gem flashes and breaks into shards on and round the pedestal;
- End takes the room away and puts the player back exactly where they stood, unfrozen, hidden as they were;
- the save (TutorialVisionStore, version 1) keeps the spot and the hidden flag, so a restart puts them back there;
- a login that finds a player in the chamber strip outside a scene sends them to the stones.
Usage: python -P edit_scene.py <code copy>"""
import sys

p = sys.argv[1] + "/server/customizations/Tutorial/TutorialVisionScene.cs"
s = open(p, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


rep('''// It plays in place at the stones (P673 1.4 keeps a chamber optional, and a private copy is already private), so no
// chamber pool. What it does, and to whom:''',
'''// It plays in place at the stones (P673 1.4 keeps a chamber optional, and a private copy is already private), so no
// chamber pool. cc-P742 (Chase 10-30): it now plays in a chamber after all, a dungeon shrine with the Gem on a pedestal
// (TutorialVisionChamber), built per scene in a slot of the empty strip of site A on the player's own lesson map: the
// first beat hides the player and moves them in, the last puts them back exactly where they stood. What it does, and to
// whom:''')

rep('''        public Point3D Origin;
        public int Second;''', '''        public Point3D Origin;
        public bool WasHidden;       // cc-P742: restored at the end
        public int Slot = -1;        // cc-P742: the chamber slot on Map
        public readonly List<Item> Chamber = []; // cc-P742: the room's pieces, taken away at the end
        public Item? Pedestal;
        public int Second;''')

rep('''        var scene = new Scene(pm, pm.Map, finished, ended) { Origin = pm.Location };
        Active[pm.Serial] = scene;''', '''        // cc-P742: a chamber slot of its own on this map (a private copy always has slot 0 free)
        var slot = TutorialVisionChamber.FreeSlot(pm.Map, Active.Values.Where(a => a.Map == pm.Map).Select(a => a.Slot));
        if (slot < 0)
        {
            return false;
        }

        var scene = new Scene(pm, pm.Map, finished, ended) { Origin = pm.Location, WasHidden = pm.Hidden, Slot = slot };
        Active[pm.Serial] = scene;''')

rep('''        scene.Timer.Cancel();
        foreach (var e in scene.Placed)
        {
            if (e is Item { Deleted: false } item) { item.Delete(); }
            else if (e is Mobile { Deleted: false } m) { m.Delete(); }
        }

        scene.Placed.Clear();
        Restore(pm, scene.Map);''', '''        scene.Timer.Cancel();
        foreach (var e in scene.Placed)
        {
            if (e is Item { Deleted: false } item) { item.Delete(); }
            else if (e is Mobile { Deleted: false } m) { m.Delete(); }
        }

        scene.Placed.Clear();
        LeaveChamber(scene);
        Restore(pm, scene.Map, scene.Origin, scene.WasHidden);''')

rep('''    /// <summary>Unfrozen, light recomputed, subtitles closed, and back at the stones if they are on that map.</summary>
    public static void Restore(PlayerMobile pm, Map? map)
    {
        pm.Frozen = false;
        pm.CloseGump<TutorialVisionSubtitleGump>();
        pm.CloseGump<TutorialVisionPanelGump>();
        if (map != null && map != Map.Internal && pm.Map == map && !pm.Deleted)
        {
            var stones = Stones(map);
            if (!pm.InRange(stones, 4)) { pm.MoveToWorld(stones, map); }
        }
        else if (map != null && pm.LogoutMap == map)
        {
            pm.LogoutLocation = Stones(map);
        }
''', '''    /// <summary>
    /// Unfrozen, light recomputed, subtitles closed, and back where they stood (<paramref name="origin"/>, cc-P742) or, with
    /// no spot known (a save from before cc-P742), at the stones if they are on that map. A player logged out meanwhile gets
    /// the spot as their logout location.
    /// </summary>
    public static void Restore(PlayerMobile pm, Map? map, Point3D? origin = null, bool hidden = false)
    {
        pm.Frozen = false;
        if (origin != null)
        {
            pm.Hidden = hidden; // cc-P742: as they were before the chamber hid them
        }

        pm.CloseGump<TutorialVisionSubtitleGump>();
        pm.CloseGump<TutorialVisionPanelGump>();
        if (map != null && map != Map.Internal && pm.Map == map && !pm.Deleted)
        {
            if (origin is { } spot)
            {
                if (pm.Location != spot) { pm.MoveToWorld(spot, map); }
            }
            else
            {
                var stones = Stones(map);
                if (!pm.InRange(stones, 4)) { pm.MoveToWorld(stones, map); }
            }
        }
        else if (map != null && pm.LogoutMap == map)
        {
            pm.LogoutLocation = origin ?? Stones(map);
        }
''')

rep('''    /// <summary>Every serial the scenes have in the world now (figures and props), for the save.</summary>
    public static IEnumerable<(Serial Player, int MapIndex, Serial[] Placed)> Snapshot() =>
        Active.Values.Select(s => (s.Player.Serial, s.Map.MapIndex, s.Placed.Select(e => e.Serial).ToArray()));''',
'''    /// <summary>
    /// Every serial the scenes have in the world now (figures, props and the chamber's pieces), with where each player
    /// stood and whether they were hidden (cc-P742), for the save.
    /// </summary>
    public static IEnumerable<(Serial Player, int MapIndex, Serial[] Placed, Point3D Origin, bool Hidden)> Snapshot() =>
        Active.Values.Select(s => (s.Player.Serial, s.Map.MapIndex,
            s.Placed.Select(e => e.Serial).Concat(s.Chamber.Select(i => i.Serial)).ToArray(), s.Origin, s.WasHidden));

    // ---------------------------------------------------------------- the chamber (cc-P742)

    /// <summary>The room in the scene's slot, the player hidden and moved in, frozen, facing the pedestal.</summary>
    private static void EnterChamber(Scene s)
    {
        var pm = s.Player;
        s.Chamber.AddRange(TutorialVisionChamber.Build(s.Map, s.Slot));
        s.Pedestal = s.Chamber[^1];
        pm.Hidden = true;
        pm.MoveToWorld(C(s, TutorialVisionChamber.Onlooker), s.Map);
        pm.Direction = Direction.Up;
        pm.CheckLightLevels(true);
    }

    /// <summary>The room's pieces taken away.</summary>
    private static void LeaveChamber(Scene s)
    {
        foreach (var item in s.Chamber)
        {
            if (!item.Deleted) { item.Delete(); }
        }

        s.Chamber.Clear();
        s.Pedestal = null;
    }

    /// <summary>A spot in the scene's chamber.</summary>
    private static Point3D C(Scene s, Point2D p) => TutorialVisionChamber.At(s.Slot, p);''')

# ---- the beats
rep('''            case Beats.Start: // Touch the stones: frozen, fade to black.
                Screen(s, ScreenEffectType.FadeOut);
                SetLight(s, Black);
                TargetSparkle(s, pm, 0x376A);
                Sound(s, 0x1FE);
                Subtitle(s, 0);
                break;''', '''            case Beats.Start: // Touch the stones: frozen, fade to black; cc-P742: and into the shrine, hidden, in the dark.
                Screen(s, ScreenEffectType.FadeOut);
                SetLight(s, Black);
                TargetSparkle(s, pm, 0x376A);
                Sound(s, 0x1FE);
                EnterChamber(s);
                Subtitle(s, 0);
                break;''')

rep('''            case Beats.Lights: // Lit: the Gem on a plinth between two braziers, the Stranger at a distance with a longsword.
                Screen(s, ScreenEffectType.FadeIn);
                SetLight(s, Lit);
                var pedestal = Place(s, new TutorialVisionProp(PedestalId), At(s, 2, -2));
                s.Gem = Place(s, new TutorialVisionProp(GemId) { Hue = GemHue, Name = "the Gem of Immortality" },
                    new Point3D(pedestal.X, pedestal.Y, pedestal.Z + TileData.ItemTable[PedestalId].CalcHeight));
                Place(s, new TutorialVisionProp(BrazierId) { Name = "a brazier", Light = LightType.Circle300 }, At(s, 1, -3));
                Place(s, new TutorialVisionProp(BrazierId) { Name = "a brazier", Light = LightType.Circle300 }, At(s, 3, -3));
                s.Stranger = Figure(s, TutorialVisionFigure.Stranger(), At(s, 6, -1), Direction.West);
                Sparkle(s, s.Gem, 0x376A, GemHue);
                Sound(s, 0x20F);
                Subtitle(s, 1);
                break;
            case Beats.Walk:
            case Beats.Walk + 1:
            case Beats.Walk + 2: // the Stranger walks up to the Gem, a tile a second
                if (s.Stranger is { Deleted: false } walker)
                {
                    var to = At(s, 6 - (s.Second - Beats.Walk + 1), -1);
                    walker.Direction = Direction.West | Direction.Running;
                    walker.MoveToWorld(to, s.Map);
                }

                if (s.Gem != null && s.Second != Beats.Walk + 1) { Sparkle(s, s.Gem, 0x376A, GemHue); }
                break;
            case Beats.Face: // facing the Gem (up and to the left of it), the sword raised
                if (s.Stranger is { Deleted: false } facer) { facer.Direction = Direction.Up; }
                break;
            case Beats.Strike: // The strike: a real swing at the Gem, the hit, the bolt.
                if (s.Stranger is { Deleted: false } striker)
                {
                    striker.Direction = Direction.Up;
                    striker.Animate(SlashAnimation, 7, 1, true, false, 0);
                }''', '''            case Beats.Lights: // Lit: the shrine, the Gem on its pedestal between the braziers, the Stranger in the dark corner.
                Screen(s, ScreenEffectType.FadeIn);
                SetLight(s, Lit);
                var top = s.Pedestal is { } pedestal
                    ? new Point3D(pedestal.X, pedestal.Y, pedestal.Z + TileData.ItemTable[PedestalId].CalcHeight)
                    : C(s, TutorialVisionChamber.Pedestal);
                s.Gem = Place(s, new TutorialVisionProp(GemId) { Hue = GemHue, Name = "the Gem of Immortality" }, top);
                s.Stranger = Figure(s, TutorialVisionFigure.Stranger(), C(s, TutorialVisionChamber.StrangerWalk[0]), Direction.Down);
                Sparkle(s, s.Gem, 0x376A, GemHue);
                Sound(s, 0x20F);
                Subtitle(s, 1);
                break;
            case Beats.Walk:
            case Beats.Walk + 2: // cc-P742: the Stranger walks out of the corner to the Gem, a step every two seconds
                if (s.Stranger is { Deleted: false } walker)
                {
                    var step = s.Second == Beats.Walk ? 1 : 2;
                    walker.Direction = Direction.Down;
                    walker.MoveToWorld(C(s, TutorialVisionChamber.StrangerWalk[step]), s.Map);
                }

                if (s.Gem != null) { Sparkle(s, s.Gem, 0x376A, GemHue); }
                break;
            case Beats.Face: // facing the Gem (south-east of him, toward the onlooker), the sword raised
                if (s.Stranger is { Deleted: false } facer) { facer.Direction = Direction.Down; }
                break;
            case Beats.Strike: // The strike: a real swing at the Gem, the hit, the bolt.
                if (s.Stranger is { Deleted: false } striker)
                {
                    striker.Direction = Direction.Down;
                    striker.Animate(SlashAnimation, 7, 1, true, false, 0);
                }''')

rep('''            case Beats.Shards: // The shards and the broken sword.
                if (s.Gem is { } gem)
                {
                    foreach (var (dx, dy) in ShardOffsets)
                    {
                        var to = Place(s, new TutorialVisionProp(ShardsId) { Name = "a shard of the Gem" }, At(s, 2 + dx, -2 + dy));
                        Moving(s, gem, to, 0x3779, GemHue);
                    }

                    gem.Delete();
                    s.Gem = null;
                }

                if (s.Stranger?.FindItemOnLayer(Layer.OneHanded) is { } blade) { blade.Delete(); }
                s.Sword = Place(s, new TutorialVisionProp(SwordId) { Name = "the broken sword", Hue = DarkHue }, At(s, 3, 0));
                Place(s, new TutorialVisionProp(SwordTipId) { Name = "the sword's broken point", Hue = DarkHue }, At(s, 4, 1));
                Sound(s, 0x211);
                Subtitle(s, 3);
                break;''', '''            case Beats.Shards: // The Gem shatters: a flash, shards on the pedestal and across the floor, the broken sword.
                if (s.Gem is { } gem)
                {
                    Screen(s, ScreenEffectType.LightFlash); // cc-P742: the light of the breaking Gem
                    SetLight(s, Flash);
                    Sparkle(s, gem, 0x36BD, GemHue, 20);
                    Place(s, new TutorialVisionProp(ShardsId) { Name = "a shard of the Gem", Hue = GemHue }, gem.Location);
                    foreach (var spot in TutorialVisionChamber.Shards)
                    {
                        var to = Place(s, new TutorialVisionProp(ShardsId) { Name = "a shard of the Gem", Hue = GemHue }, C(s, spot));
                        Moving(s, gem, to, 0x3779, GemHue);
                    }

                    gem.Delete();
                    s.Gem = null;
                }

                if (s.Stranger?.FindItemOnLayer(Layer.OneHanded) is { } blade) { blade.Delete(); }
                s.Sword = Place(s, new TutorialVisionProp(SwordId) { Name = "the broken sword", Hue = DarkHue }, C(s, TutorialVisionChamber.BrokenSword));
                Place(s, new TutorialVisionProp(SwordTipId) { Name = "the sword's broken point", Hue = DarkHue }, C(s, TutorialVisionChamber.SwordTip));
                Sound(s, 0x211);
                Sound(s, 0x307);
                Subtitle(s, 3);
                break;
            case Beats.Shards + 1: // cc-P742: the flash fades back to the braziers' light
                SetLight(s, Lit);
                break;''')

rep('''                s.Echo = Figure(s, TutorialVisionFigure.EchoOf(pm), At(s, 1, 1), Direction.North);''',
    '''                s.Echo = Figure(s, TutorialVisionFigure.EchoOf(pm), C(s, TutorialVisionChamber.Echo), Direction.Down);''')
rep('''                s.Hooded = Figure(s, TutorialVisionFigure.Hooded(), At(s, -3, -3), Direction.Down);
                s.Sword = Place(s, new TutorialVisionProp(SwordId) { Name = "the broken sword", Hue = DarkHue }, At(s, -2, -1));''',
    '''                s.Hooded = Figure(s, TutorialVisionFigure.Hooded(), C(s, TutorialVisionChamber.Hooded), Direction.Down);
                s.Sword = Place(s, new TutorialVisionProp(SwordId) { Name = "the broken sword", Hue = DarkHue }, C(s, TutorialVisionChamber.BrokenSword));''')

rep('''    private static readonly (int Dx, int Dy)[] ShardOffsets = [(-2, -1), (2, -1), (-1, 2), (2, 2), (0, -3)];

    private static Point3D At(Scene s, int dx, int dy) =>
        TutorialWorld.Ground(s.Map, new Point2D(s.Origin.X + dx, s.Origin.Y + dy));

''', '')

# ---- login safety
rep('''    [OnEvent(nameof(PlayerMobile.PlayerLoginEvent))]
    public static void OnLogin(PlayerMobile pm)
    {
        End(pm, false);
        TutorialVisionStore.Recover(pm);
    }''', '''    [OnEvent(nameof(PlayerMobile.PlayerLoginEvent))]
    public static void OnLogin(PlayerMobile pm)
    {
        End(pm, false);
        TutorialVisionStore.Recover(pm);
        SendOutOfChamber(pm);
    }

    /// <summary>
    /// cc-P742: a player in the chamber strip with no scene playing (a crash between saves, a lost record) goes to the
    /// stones of that map, unfrozen and seen. Never staff, who may look at the room.
    /// </summary>
    public static bool SendOutOfChamber(PlayerMobile pm)
    {
        if (IsPlaying(pm) || pm.AccessLevel > AccessLevel.Player || pm.Map is not { } map || !TutorialVisionChamber.Contains(pm.Location, map))
        {
            return false;
        }

        pm.Frozen = false;
        pm.Hidden = false;
        pm.MoveToWorld(Stones(map), map);
        pm.CheckLightLevels(true);
        return true;
    }''')

# ---- the store: version 1 keeps the spot and the hidden flag
rep('''    public const int CurrentVersion = 0;''', '''    public const int CurrentVersion = 1; // cc-P742: 1 adds each player's spot and hidden flag''')
rep('''    /// <summary>Scenes read from the save and not yet recovered: player, map index, placed serials.</summary>
    private static readonly Dictionary<Serial, (int MapIndex, Serial[] Placed)> Pending = new();''',
    '''    /// <summary>Scenes read from the save and not yet recovered: player, map index, placed serials, their spot (version 1).</summary>
    private static readonly Dictionary<Serial, (int MapIndex, Serial[] Placed, Point3D? Origin, bool Hidden)> Pending = new();''')
rep('''        var all = new Dictionary<Serial, (int MapIndex, Serial[] Placed)>(Pending);
        foreach (var (player, mapIndex, placed) in TutorialVisionScene.Snapshot())
        {
            all[player] = (mapIndex, placed);
        }

        writer.WriteEncodedInt(all.Count);
        foreach (var (player, (mapIndex, placed)) in all)
        {
            writer.Write(player);
            writer.WriteEncodedInt(mapIndex);
            writer.WriteEncodedInt(placed.Length);
            foreach (var serial in placed)
            {
                writer.Write(serial);
            }
        }''', '''        var all = new Dictionary<Serial, (int MapIndex, Serial[] Placed, Point3D? Origin, bool Hidden)>(Pending);
        foreach (var (player, mapIndex, placed, origin, hidden) in TutorialVisionScene.Snapshot())
        {
            all[player] = (mapIndex, placed, origin, hidden);
        }

        writer.WriteEncodedInt(all.Count);
        foreach (var (player, (mapIndex, placed, origin, hidden)) in all)
        {
            writer.Write(player);
            writer.WriteEncodedInt(mapIndex);
            writer.WriteEncodedInt(placed.Length);
            foreach (var serial in placed)
            {
                writer.Write(serial);
            }

            writer.Write(origin != null); // version 1
            writer.Write(origin ?? Point3D.Zero);
            writer.Write(hidden);
        }''')
rep('''            var placed = new Serial[reader.ReadEncodedInt()];
            for (var k = 0; k < placed.Length; k++)
            {
                placed[k] = reader.ReadSerial();
            }

            Pending[player] = (mapIndex, placed);''', '''            var placed = new Serial[reader.ReadEncodedInt()];
            for (var k = 0; k < placed.Length; k++)
            {
                placed[k] = reader.ReadSerial();
            }

            Point3D? origin = null;
            var hidden = false;
            if (version >= 1)
            {
                var known = reader.ReadBool();
                var spot = reader.ReadPoint3D();
                hidden = reader.ReadBool();
                origin = known ? spot : null;
            }

            Pending[player] = (mapIndex, placed, origin, hidden);''')
rep('''    /// <summary>Puts <paramref name="pm"/> back at the stones, unfrozen, light restored, and removes what the scene placed.</summary>
    public static void Recover(PlayerMobile pm)
    {
        if (!Pending.ContainsKey(pm.Serial)) { return; }
        var map = Map.Maps[Pending[pm.Serial].MapIndex];
        Clean(pm.Serial);
        TutorialVisionScene.Restore(pm, map);
    }''', '''    /// <summary>
    /// Puts <paramref name="pm"/> back where they stood before the vision (cc-P742; a version 0 save: at the stones),
    /// unfrozen, light restored, and removes what the scene placed, the chamber included.
    /// </summary>
    public static void Recover(PlayerMobile pm)
    {
        if (!Pending.TryGetValue(pm.Serial, out var scene)) { return; }
        var map = Map.Maps[scene.MapIndex];
        Clean(pm.Serial);
        TutorialVisionScene.Restore(pm, map, scene.Origin, scene.Hidden);
    }''')

open(p, "w", encoding="utf-8", newline="").write(s)
print("edited", p)
