def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


F = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/TutorialFarm.cs"
edit(F, [
("""        /// <summary>cc-P718: the two tiles of the field's gate in its east fence (the layout leaves them open).</summary>
        public static readonly Point2D[] FieldGateSpots = [new(6713, 3978), new(6713, 3979)];""",
 """        /// <summary>
        /// cc-P718: the field's gate, in the two-tile gap of its east fence (6713, 3978-3979; the layout leaves it open).
        /// Every wooden gate's art is impassable open or shut, and pinned swings a gate in a north-south fence east by one
        /// tile (BaseDoor offsets), so two halves would stand on both tiles outside the gap (Wren's and the one below it)
        /// and shut the field: the P718 bot run could not get in. So one gate, on the gap's south tile, swinging north-east
        /// onto Wren's own tile (NorthCCW, offset +1,-1), and a fence piece closing the gap's north tile. A player walks in
        /// from the tile below Wren.
        /// </summary>
        public static readonly Point2D[] FieldGateSpots = [new(6713, 3979)];

        public static readonly Point2D FieldFenceSpot = new(6713, 3978);
        public const int FieldFenceId = 0x0837; // the layout's own wooden fence, north-south"""),
("""        /// <summary>The gate's halves: the north one swings north, the south one south.</summary>
        public static TutorialPestGate[] MakeFieldGates() => [new(DoorFacing.SouthCW), new(DoorFacing.NorthCCW)];""",
 """        /// <summary>The field gate (one, see FieldGateSpots).</summary>
        public static TutorialPestGate[] MakeFieldGates() => [new(DoorFacing.NorthCCW)];

        /// <summary>The fence piece closing the gap's north tile on <paramref name="map"/>, or null.</summary>
        public static Item? FindFieldFence(Map map)
        {
            foreach (var item in map.GetItemsInRange<Static>(TutorialWorld.Ground(map, FieldFenceSpot), 0))
            {
                if (!item.Deleted && item.ItemID == FieldFenceId)
                {
                    return item;
                }
            }

            return null;
        }"""),
("""            // cc-P718 item 7: the field gate, closed, in the gap of the east fence.
            var gates = MakeFieldGates();""", """            // cc-P718 item 7: the field gate, closed, in the gap of the east fence, and a fence piece beside it (both
            // counted with the doors).
            if (FindFieldFence(map) != null) { present++; }
            else
            {
                if (!dryRun) { new Static(FieldFenceId) { Name = "wooden fence" }.MoveToWorld(TutorialWorld.Ground(map, FieldFenceSpot), map); }
                doors++;
            }

            var gates = MakeFieldGates();"""),
])

T = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Tutorial/TutorialFarmVerification.cs"
edit(T, [
("""        foreach (var gate in TutorialFarm.FieldGates(map)) { gate.Delete(); } // cc-P718""",
 """        foreach (var gate in TutorialFarm.FieldGates(map)) { gate.Delete(); } // cc-P718
        TutorialFarm.FindFieldFence(map)?.Delete();"""),
("""            // cc-P718: the farmhouse door and the field gate's two halves.""", """            // cc-P718: the farmhouse door, the field gate and the fence piece beside it."""),
("""            Assert.Equal((0, 7), (again.Doors, again.Present)); // cc-P718: and the field gate's halves""",
 """            Assert.Equal((0, 7), (again.Doors, again.Present)); // cc-P718: and the field gate and its fence piece"""),
])

B = "D:/UO/golems/Iron/shard-migration/notes/cc-P718-tools/isle.py"
edit(B, [
("""FIELD_GATE = ((6713, 3978), (6713, 3979))  # cc-P718: TutorialFarm.FieldGateSpots
GATE_CLOSED = (0x0841, 0x0843)             # LightWoodGate SouthCW and NorthCCW, closed""",
 """FIELD_GATE = ((6713, 3979),)               # cc-P718: TutorialFarm.FieldGateSpots
BELOW_WREN = (6714, 3979)                  # the tile a player enters the field gate from
GATE_CLOSED = (0x0843,)                    # LightWoodGate NorthCCW, closed"""),
("""            if g:
                pl.go(spot, 1)""", """            if g:
                pl.go(BELOW_WREN, 0)"""),
("""    walk_to(pl, log, WREN, 2, "the field gate")""", """    walk_to(pl, log, BELOW_WREN, 0, "the field gate")"""),
])
print("ok")
