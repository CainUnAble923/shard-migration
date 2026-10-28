def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


C = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/TutorialCopies.cs"
T = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Tutorial/TutorialCopiesVerification.cs"

edit(C, [
("""            if (!free.Seeded)
            {
                Seed(free);
            }""", """            // cc-P718: a copy whose seeding placed nothing (refused: the isle's land was not on the map then) is seeded again.
            if (!free.Seeded || free.Placed.Count == 0)
            {
                Seed(free);
            }"""),
("""        slot.Seeded = true;
        logger.Information("Tutorial copy {N} seeded ({Count} pieces): {Result}", slot.N, slot.Placed.Count, result);""",
 """        // cc-P718: a refused seeding (nothing placed) leaves the copy unseeded, so its next claim tries again. The overnight
        // bot's world held six copies "seeded (0 pieces)" from nights without the isle's map overlay, and trainees woke on
        // an empty copy.
        slot.Seeded = slot.Placed.Count > 0;
        logger.Information("Tutorial copy {N} seeded ({Count} pieces): {Result}", slot.N, slot.Placed.Count, result);"""),
])

s = open(T, encoding="utf-8").read()
anchor = "    private static List<BaseCreature> Pests(Map map) =>"
assert s.count(anchor) == 1
fact = """    // cc-P718: a copy whose seeding placed nothing (the isle's land was missing then) is not left "seeded" and empty: the
    // next claim seeds it again. The overnight bot's world had six such copies, and the P718 bot run woke on an empty one.
    [Fact]
    public void ACopyWhoseSeedingPlacedNothingIsSeededAgainAtTheNextClaim()
    {
        var seed = TutorialCopies.SeedCopy;
        try
        {
            TutorialCopies.SeedCopy = _ => "Tutorial: refused. (the isle's land is missing)";
            var first = Trainee("CopyEmpty");
            var slot = TutorialCopies.SlotOf(first.Map);
            Assert.Empty(slot.Placed);
            Assert.False(slot.Seeded);

            TutorialStart.SendHome(first);
            TutorialCopies.Tick(Core.Now + TimeSpan.FromMinutes(31));
            Assert.False(slot.InUse);

            // An old save's state: seeded, with nothing placed.
            foreach (var s in TutorialCopies.Slots)
            {
                s.Seeded = true;
                s.Placed.Clear();
            }

            TutorialCopies.SeedCopy = seed;
            var next = Trainee("CopyRetry");
            var again = TutorialCopies.SlotOf(next.Map);
            Assert.True(again.Seeded);
            Assert.NotEmpty(again.Placed);
        }
        finally
        {
            TutorialCopies.SeedCopy = seed;
        }
    }

"""
s = s.replace(anchor, fact + anchor)
open(T, "w", encoding="utf-8", newline="").write(s)
print("ok")
