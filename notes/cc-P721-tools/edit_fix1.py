def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:80], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


C = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/"
T = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/"

# The vision's light wins over the waking light; a vision ends any wake.
edit(C + "Fold/FoldRegions.cs", [
("""        Server.Tutorial.TutorialVisionScene.AlterLight(m, ref global, ref personal); // cc-P665: the vision's light, per player
        Server.Tutorial.TutorialWake.AlterLight(m, ref global, ref personal); // cc-P721: waking on the beach""",
 """        Server.Tutorial.TutorialWake.AlterLight(m, ref global, ref personal); // cc-P721: waking on the beach
        Server.Tutorial.TutorialVisionScene.AlterLight(m, ref global, ref personal); // cc-P665: the vision's light, per player"""),
])
edit(C + "Tutorial/TutorialVisionScene.cs", [
("""        var scene = new Scene(pm, pm.Map, finished, ended) { Origin = pm.Location };""",
 """        TutorialWake.Stand(pm); // cc-P721: never both at once
        var scene = new Scene(pm, pm.Map, finished, ended) { Origin = pm.Location };"""),
])
# Pip counts in a dry run too.
edit(C + "Tutorial/TutorialFarm.cs", [
("""            else if (!dryRun && TutorialCorePlacement.FitsOn(TutorialWorld.Ground(map, PipSpot), map))
            {
                var spot = TutorialWorld.Ground(map, PipSpot);
                new TutorialWoundedHelper { Direction = Direction.West, Home = spot, RangeHome = 0 }.MoveToWorld(spot, map);
                hands++;
            }""", """            else if (TutorialCorePlacement.FitsOn(TutorialWorld.Ground(map, PipSpot), map))
            {
                if (!dryRun)
                {
                    var spot = TutorialWorld.Ground(map, PipSpot);
                    new TutorialWoundedHelper { Direction = Direction.West, Home = spot, RangeHome = 0 }.MoveToWorld(spot, map);
                }

                hands++;
            }"""),
])

# -- tests: the weapon and war mode before the pests
W = T + "Tutorial/TutorialIsleWalkFixesVerification.cs"
edit(W, [
("""        // The commands done: the pests fight, and Wren opened the gate.
        p.Record.StationsDone.UnionWith([TutorialFarm.FollowKey]);
        pet.ControlOrder = OrderType.Guard;
        Assert.True(TutorialFarm.CheckCommands(p.Pm));""", """        // The commands done (and, since cc-P721, the pitchfork in hand and war mode): the pests fight, and Wren opened the gate.
        p.Record.StationsDone.UnionWith([TutorialFarm.FollowKey]);
        pet.ControlOrder = OrderType.Guard;
        Assert.False(TutorialFarm.CheckCommands(p.Pm));
        Hold(p.Pm);
        Assert.False(TutorialFarm.CheckCommands(p.Pm));
        p.Pm.Warmode = true;
        Assert.True(TutorialFarm.CheckCommands(p.Pm));"""),
("""        pet.ControlOrder = OrderType.Guard;
        Assert.True(TutorialFarm.CheckCommands(p.Pm));
        Assert.True(TutorialFarm.PestPartOn(p.Pm));
        Assert.Contains("all follow me", TutorialFarm.CommandsLine);""", """        pet.ControlOrder = OrderType.Guard;
        Assert.False(TutorialFarm.CheckCommands(p.Pm)); // cc-P721: then the weapon and war mode
        Hold(p.Pm);
        Assert.False(TutorialFarm.CheckCommands(p.Pm));
        p.Pm.Warmode = true;
        Assert.True(TutorialFarm.CheckCommands(p.Pm));
        Assert.True(TutorialFarm.PestPartOn(p.Pm));
        Assert.Contains("all follow me", TutorialFarm.CommandsLine);"""),
("""    private static Point3D Beside(IEntity m, int dx) => new(m.X + dx, m.Y, m.Z);""",
 """    private static Point3D Beside(IEntity m, int dx) => new(m.X + dx, m.Y, m.Z);

    /// <summary>cc-P721: the trainee takes Wren's pitchfork in hand (the host has no tiledata: its layer is set).</summary>
    private static void Hold(PlayerMobile pm)
    {
        var fork = pm.Backpack!.FindItemByType<TutorialPitchfork>()!;
        fork.Layer = Layer.TwoHanded;
        Assert.True(pm.EquipItem(fork));
    }"""),
("""        p.Record.StationsDone.UnionWith([TutorialFarm.FollowKey, TutorialFarm.GuardKey, TutorialFarm.PestsKey]);""",
 """        p.Record.StationsDone.UnionWith([TutorialFarm.FollowKey, TutorialFarm.GuardKey, TutorialFarm.WeaponKey, TutorialFarm.WarKey, TutorialFarm.PestsKey]);"""),
])

F = T + "Tutorial/TutorialFarmVerification.cs"
edit(F, [
("""            pet.ControlOrder = OrderType.Guard;
            Assert.True(TutorialFarm.CheckCommands(p.Pm));
            pet.ControlOrder = OrderType.Attack;""", """            pet.ControlOrder = OrderType.Guard;
            TutorialFarm.CheckCommands(p.Pm);
            var fork = p.Pm.Backpack.FindItemByType<TutorialPitchfork>()!; // cc-P721: the weapon, then war mode
            fork.Layer = Layer.TwoHanded;
            Assert.True(p.Pm.EquipItem(fork));
            TutorialFarm.CheckCommands(p.Pm);
            p.Pm.Warmode = true;
            Assert.True(TutorialFarm.CheckCommands(p.Pm));
            pet.ControlOrder = OrderType.Attack;"""),
("""        TutorialFarm.FindFieldFence(map)?.Delete();""", """        TutorialFarm.FindFieldFence(map)?.Delete();
        TutorialFarm.FindPip(map)?.Delete(); // cc-P721"""),
("""            Assert.Equal((false, 1, 3, 1, 2, 0), (dry.Refused, dry.Addons, dry.Doors, dry.Farmhands, dry.Spawners, dry.Present));""",
 """            // cc-P721: Wren and Pip.
            Assert.Equal((false, 1, 3, 2, 2, 0), (dry.Refused, dry.Addons, dry.Doors, dry.Farmhands, dry.Spawners, dry.Present));"""),
("""            Assert.Equal((false, 1, 3, 1, 2, 0), (first.Refused, first.Addons, first.Doors, first.Farmhands, first.Spawners, first.Present));""",
 """            Assert.Equal((false, 1, 3, 2, 2, 0), (first.Refused, first.Addons, first.Doors, first.Farmhands, first.Spawners, first.Present));"""),
("""            Assert.Equal((0, 0, 0, 0, 7), (again.Addons, again.Doors, again.Farmhands, again.Spawners, again.Present));""",
 """            Assert.Equal((0, 0, 0, 0, 8), (again.Addons, again.Doors, again.Farmhands, again.Spawners, again.Present));"""),
("""            Assert.Equal((0, 7), (again.Doors, again.Present)); // cc-P718: and the field gate and its fence piece""",
 """            Assert.Equal((0, 8), (again.Doors, again.Present)); // cc-P718: and the field gate and its fence piece; cc-P721: Pip"""),
])

edit(T + "Tutorial/TutorialCopiesVerification.cs", [
("""        RecordOf(a).StationsDone.UnionWith([TutorialFarm.FollowKey, TutorialFarm.GuardKey]);
        RecordOf(b).StationsDone.UnionWith([TutorialFarm.FollowKey, TutorialFarm.GuardKey]);""",
 """        RecordOf(a).StationsDone.UnionWith([TutorialFarm.FollowKey, TutorialFarm.GuardKey, TutorialFarm.WeaponKey, TutorialFarm.WarKey]);
        RecordOf(b).StationsDone.UnionWith([TutorialFarm.FollowKey, TutorialFarm.GuardKey, TutorialFarm.WeaponKey, TutorialFarm.WarKey]);"""),
])

# -- the vision's timings (cc-P721: 61 s, named beats)
V = T + "Tutorial/TutorialVisionSceneVerification.cs"
edit(V, [
("""        ShardTestClock.Advance(TimeSpan.FromSeconds(4)); // the Gem and the Stranger
        Assert.Equal(TutorialVisionScene.Dim, GlobalLight(p.Pm));""", """        ShardTestClock.Advance(TimeSpan.FromSeconds(4)); // the Gem and the Stranger, lit (cc-P721)
        Assert.Equal(TutorialVisionScene.Lit, GlobalLight(p.Pm));"""),
("""        ShardTestClock.Advance(TimeSpan.FromSeconds(19)); // 23 s: the echo has spoken""",
 """        ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Beats.EchoSays + 1 - 4)); // the echo has spoken"""),
("""        ShardTestClock.Advance(TimeSpan.FromSeconds(23)); // 46 s: over""",
 """        ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Length - TutorialVisionScene.Beats.EchoSays)); // over"""),
])
s = open(V, encoding="utf-8").read()
n = s.count("ShardTestClock.Advance(TimeSpan.FromSeconds(46));")
s = s.replace("ShardTestClock.Advance(TimeSpan.FromSeconds(46));", "ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Length + 1));")
old_panels = """            ShardTestClock.Advance(TimeSpan.FromSeconds(17.5));
            Assert.False(off.Pm.HasGump<TutorialVisionPanelGump>());
            ShardTestClock.Advance(TimeSpan.FromSeconds(29));"""
assert s.count(old_panels) == 1
s = s.replace(old_panels, """            ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Beats.Flash + 0.5));
            Assert.False(off.Pm.HasGump<TutorialVisionPanelGump>());
            ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Length - TutorialVisionScene.Beats.Flash));""")
old_on = """            ShardTestClock.Advance(TimeSpan.FromSeconds(17.5));
            Assert.Equal(TutorialVisionScene.PanelBrokenSword, on.Pm.FindGump<TutorialVisionPanelGump>()!.GumpId);
            ShardTestClock.Advance(TimeSpan.FromSeconds(13)); // 30.5 s
            Assert.Equal(TutorialVisionScene.PanelCrest, on.Pm.FindGump<TutorialVisionPanelGump>()!.GumpId);
            ShardTestClock.Advance(TimeSpan.FromSeconds(16));"""
assert s.count(old_on) == 1
s = s.replace(old_on, """            ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Beats.Flash + 0.5));
            Assert.Equal(TutorialVisionScene.PanelBrokenSword, on.Pm.FindGump<TutorialVisionPanelGump>()!.GumpId);
            ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Beats.Hooded - TutorialVisionScene.Beats.Flash)); // the crest
            Assert.Equal(TutorialVisionScene.PanelCrest, on.Pm.FindGump<TutorialVisionPanelGump>()!.GumpId);
            ShardTestClock.Advance(TimeSpan.FromSeconds(TutorialVisionScene.Length - TutorialVisionScene.Beats.Hooded));""")
open(V, "w", encoding="utf-8", newline="").write(s)
print("ok", n)
