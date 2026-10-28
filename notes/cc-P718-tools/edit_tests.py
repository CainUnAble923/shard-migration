import os
os.chdir(r"D:\UO\golems\Iron\ShatteredLegacy\server\tests")


def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) >= 1, (p, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


BAG_OLD = '"core.backpack" => [TutorialAction.OpenedBag],'
BAG_NEW = '"core.backpack" => [TutorialAction.OpenedPaperdoll, TutorialAction.OpenedBag], // cc-P718: the character window first'
for f in [r"Tutorial\TutorialIsleVerification.cs", r"Tutorial\TutorialFirstPlayVerification.cs", r"Misc\TutorialVerification.cs"]:
    edit(f, [(BAG_OLD, BAG_NEW)])

edit(r"Tutorial\TutorialTrialProgressVerification.cs", [
('[InlineData("core.backpack", TutorialAction.OpenedBag, TutorialAction.OpenedBag)]',
 '[InlineData("core.backpack", TutorialAction.OpenedPaperdoll, TutorialAction.OpenedBag)] // cc-P718'),
])

edit(r"Tutorial\TutorialTradeTrialVerification.cs", [
("""            if (!station.IsCore)
            {
                Assert.True(TutorialWingTrials.IsWingTrial(station.Key), $"{station.Key} is not a wing trial");""",
 """            if (!station.IsCore && !TutorialStations.IsAnytime(station.Key)) // cc-P718: the client tips are not a wing
            {
                Assert.True(TutorialWingTrials.IsWingTrial(station.Key), $"{station.Key} is not a wing trial");"""),
])

edit(r"Tutorial\TutorialFirstPlayVerification.cs", [
("""        foreach (var s in TutorialStations.All)
        {
            if (s.IsCore)
            {
                Assert.Contains(StationButton(s.Key), buttons);
            }""", """        foreach (var s in TutorialStations.All)
        {
            if (s.IsCore || TutorialStations.IsAnytime(s.Key)) // cc-P718: the client tips are offered at any time
            {
                Assert.Contains(StationButton(s.Key), buttons);
            }"""),
# cc-P718: the cloak is not a backpack supply any more (it waits on the table: TutorialIsleVerification's cc-P718 facts).
("""        foreach (var key in new[] { "core.backpack", "core.paperdoll", "core.banking" })""",
 """        foreach (var key in new[] { "core.backpack", "core.banking" }) // cc-P718: the cloak waits on the table instead"""),
])

edit(r"Misc\TutorialVerification.cs", [
("""        bag.OnDoubleClick(stranger.Pm);
        Assert.DoesNotContain("core.backpack", p.Record.StationsDone);
        bag.OnDoubleClick(p.Pm);""", """        bag.OnDoubleClick(stranger.Pm);
        Assert.DoesNotContain("core.backpack", p.Record.StationsDone);
        bag.OnDoubleClick(p.Pm); // cc-P718: before the character window, the bag does not finish the lesson
        Assert.DoesNotContain("core.backpack", p.Record.StationsDone);
        p.Pm.DisplayPaperdollTo(p.Pm); // the real hook: EventSink.PaperdollRequest
        bag.OnDoubleClick(p.Pm);"""),
("""        // The fake host has no tiledata; give this practice item's fake its real equipment layer.
        var cloak = TutorialCoreTrials.Current(p.Pm)!.Supply!;""", """        // The fake host has no tiledata; give this practice item's fake its real equipment layer.
        // cc-P718: the cloak waits on the clothes table.
        var cloak = WakeningIsleCloak.OnTable(p.Pm, TutorialWorld.MapOf(p.Pm))!;"""),
('"thieving.trial", "housing.basics", "travel.wing", "reputation.wing", "shard.systems"',
 '"thieving.trial", "housing.basics", "travel.wing", "reputation.wing", "shard.systems", "client.tips"'),
])

edit(r"Tutorial\TutorialFarmVerification.cs", [
("""        TutorialFarm.FindDoor(map)?.Delete();
        TutorialFarmhand.Find(map)?.Delete();""", """        TutorialFarm.FindDoor(map)?.Delete();
        foreach (var gate in TutorialFarm.FieldGates(map)) { gate.Delete(); } // cc-P718
        TutorialFarmhand.Find(map)?.Delete();"""),
("""            Assert.Equal((false, 1, 1, 1, 2, 0), (dry.Refused, dry.Addons, dry.Doors, dry.Farmhands, dry.Spawners, dry.Present));""",
 """            // cc-P718: the farmhouse door and the field gate's two halves.
            Assert.Equal((false, 1, 3, 1, 2, 0), (dry.Refused, dry.Addons, dry.Doors, dry.Farmhands, dry.Spawners, dry.Present));"""),
("""            Assert.Equal((false, 1, 1, 1, 2, 0), (first.Refused, first.Addons, first.Doors, first.Farmhands, first.Spawners, first.Present));""",
 """            Assert.Equal((false, 1, 3, 1, 2, 0), (first.Refused, first.Addons, first.Doors, first.Farmhands, first.Spawners, first.Present));"""),
("""            Assert.Equal(TutorialFarmLayout.Pieces.Length, addon.Components.Count);
            var placed = addon.Components.Select(c => (c.ItemID, c.X, c.Y, c.Z)).OrderBy(t => t).ToArray();
            var wanted = TutorialIsleFarmLayout.Pieces.Select(p => (p.Id, p.X, p.Y, p.Z)).OrderBy(t => t).ToArray();""",
 """            // cc-P718: the gate's wall-arm sign is the standing post, and its hung board is left out.
            Assert.Equal(TutorialFarmLayout.Pieces.Length - 1, addon.Components.Count);
            var placed = addon.Components.Select(c => (c.ItemID, c.X, c.Y, c.Z)).OrderBy(t => t).ToArray();
            var wanted = TutorialIsleFarmLayout.Pieces.Where(p => TutorialFarm.IsleArt(p.Id) != null)
                .Select(p => (TutorialFarm.IsleArt(p.Id)!.Value, p.X, p.Y, p.Z)).OrderBy(t => t).ToArray();"""),
("""            Assert.Equal((0, 0, 0, 0, 5), (again.Addons, again.Doors, again.Farmhands, again.Spawners, again.Present));""",
 """            Assert.Equal((0, 0, 0, 0, 7), (again.Addons, again.Doors, again.Farmhands, again.Spawners, again.Present));"""),
("""            Assert.Equal((0, 5), (again.Doors, again.Present));""", """            Assert.Equal((0, 7), (again.Doors, again.Present)); // cc-P718: and the field gate's halves"""),
("""            Assert.Null(TutorialFarm.ChoosePet(p.Pm, "cat")); // one pet
            Assert.Equal(2, TutorialFarm.StepOf(p.Pm));
""", """            Assert.Null(TutorialFarm.ChoosePet(p.Pm, "cat")); // one pet
            Assert.Equal(2, TutorialFarm.StepOf(p.Pm));

            // cc-P718: the commands first (the pet's order is the evidence), then the pests fight, and the pet attacks.
            Assert.Equal(OrderType.Stay, pet.ControlOrder);
            pet.ControlTarget = p.Pm;
            pet.ControlOrder = OrderType.Follow;
            TutorialFarm.CheckCommands(p.Pm);
            pet.ControlOrder = OrderType.Guard;
            Assert.True(TutorialFarm.CheckCommands(p.Pm));
            pet.ControlOrder = OrderType.Attack;
"""),
])

edit(r"Tutorial\TutorialCopiesVerification.cs", [
("""        RecordOf(a).PetClaimed = true;
        RecordOf(b).PetClaimed = true;""", """        RecordOf(a).PetClaimed = true;
        RecordOf(b).PetClaimed = true;
        // cc-P718: past the pet commands, so the pests fight them.
        RecordOf(a).StationsDone.UnionWith([TutorialFarm.FollowKey, TutorialFarm.GuardKey]);
        RecordOf(b).StationsDone.UnionWith([TutorialFarm.FollowKey, TutorialFarm.GuardKey]);"""),
])
print("ok")
