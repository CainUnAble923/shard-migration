r"""cc-P678 WRITES: RegistrarOfficeVerification.cs helpers: the house box becomes two boxes (the old New Haven house,
where a cc-P19 world has its office, and SoS Haven's hall, where the current layout goes); the cc-P17 door helpers,
used only by the old fact 3, go."""
P = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Misc/RegistrarOfficeVerification.cs"
t = open(P, encoding="utf-8").read()

old_box = """    // Every AddonComponent on Trammel in the house box, whoever owns it: catches a component left behind.
    private static List<AddonComponent> OfficeComponentsInTheHouseBox() =>
        World.Items.Values.OfType<AddonComponent>()
            .Where(c => !c.Deleted && c.Map == Map.Trammel && c.X is >= 3448 and <= 3468 && c.Y is >= 2590 and <= 2608).ToList();
"""
new_box = """    // The two places an office can be: the old New Haven house (a world seeded by cc-P19 or cc-P31) and, since cc-P678,
    // SoS Haven's hall with the outside group south of it.
    private static readonly (int X1, int Y1, int X2, int Y2) OldHouse = (3448, 2590, 3468, 2608);
    private static readonly (int X1, int Y1, int X2, int Y2) NewHall = (3653, 2542, 3679, 2567);

    private static List<AddonComponent> OfficeComponentsIn((int X1, int Y1, int X2, int Y2) box) =>
        World.Items.Values.OfType<AddonComponent>()
            .Where(c => !c.Deleted && c.Map == Map.Trammel && c.X >= box.X1 && c.X <= box.X2 && c.Y >= box.Y1 && c.Y <= box.Y2)
            .ToList();

    // Every AddonComponent on Trammel in either box, whoever owns it: catches a component left behind.
    private static List<AddonComponent> OfficeComponentsInTheHouseBox() =>
        OfficeComponentsIn(OldHouse).Concat(OfficeComponentsIn(NewHall)).ToList();
"""
assert t.count(old_box) == 1
t = t.replace(old_box, new_box)

a = t.index("\n    private static Point2D Swing(Point3D closed, DoorFacing facing)")
b = t.index("    private static void Place(BaseCreature npc, Point3D at, Direction facing)")
t = t[:a] + "\n" + t[b:]

old_assert = """        var placed = OfficeComponentsInTheHouseBox();
        Assert.Equal(14, placed.Count);
"""
new_assert = """        var placed = OfficeComponentsInTheHouseBox();
        Assert.Equal(14, placed.Count);
        Assert.Empty(OfficeComponentsIn(OldHouse));
"""
assert t.count(old_assert) == 1
t = t.replace(old_assert, new_assert)
open(P, "w", encoding="utf-8", newline="").write(t)
print("ok")
