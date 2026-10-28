"""cc-P707: the farm's heal step needs someone hurt. On the isle the pests die to the pet before they bite (the bot's run:
pet 100/100, the trainee unhurt, "That being is not damaged!" on both, and the step can never finish). Wren now gives
an unhurt trainee a small scratch when she hands the bandages, and says so.

    python -P edit_scratch.py <code repo>
"""
import os
import sys

repo = sys.argv[1]
farm = os.path.join(repo, 'server', 'customizations', 'Tutorial', 'TutorialFarm.cs')
tests = os.path.join(repo, 'server', 'tests', 'Tutorial', 'TutorialFarmVerification.cs')


def edit(path, pairs):
    s = open(path, 'rb').read().decode('utf-8')
    crlf = '\r\n' in s
    for old, new in pairs:
        if crlf:
            old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
        assert s.count(old) == 1, (path, old[:70])
        s = s.replace(old, new)
    open(path, 'wb').write(s.encode('utf-8'))


edit(farm, [
    ('''        public const string HealLine = "Double-click a bandage in your backpack, then click yourself or an injured pet. A successful heal finishes this step.";
''', '''        public const string HealLine = "Double-click a bandage in your backpack, then click yourself or an injured pet. A successful heal finishes this step.";
        // cc-P707: the pests die to the pet before they bite, so nobody is hurt and a bandage only says "That being is not
        // damaged!". Wren gives an unhurt trainee a scratch to practise on.
        public const string ScratchLine = "A rat nipped your ankle in the rows. Double-click a bandage in your backpack, then click yourself to treat it. A successful heal finishes this step.";
'''),
    ('''                case 3:
                    hand.SayTo(pm, GiveBandages(pm) switch
                    {
                        BandageGift.NoneLeft => NoMoreBandagesLine,
                        BandageGift.NoRoom => NoRoomForBandagesLine,
                        _ => HealLine
                    });
                    break;
''', '''                case 3:
                    var gift = GiveBandages(pm);
                    hand.SayTo(pm, gift switch
                    {
                        BandageGift.NoneLeft => NoMoreBandagesLine,
                        BandageGift.NoRoom => NoRoomForBandagesLine,
                        _ => Scratch(pm) ? ScratchLine : HealLine
                    });
                    break;
'''),
    ('''        public enum BandageGift { Given, HasSome, NoneLeft, NoRoom }
''', '''        public enum BandageGift { Given, HasSome, NoneLeft, NoRoom }

        /// <summary>
        /// cc-P707: step 3 needs a bandage that really heals. When neither the trainee nor a pet of theirs within 12 tiles is
        /// hurt, takes a fifth of the trainee's hits (at least 5, never the last one). True when it did.
        /// </summary>
        public static bool Scratch(PlayerMobile pm)
        {
            if (!pm.Alive || pm.Hits < pm.HitsMax)
            {
                return false;
            }

            foreach (var f in pm.AllFollowers)
            {
                if (f is BaseCreature { Alive: true, Deleted: false } pet && pet.Map == pm.Map && pet.InRange(pm, 12) &&
                    pet.Hits < pet.HitsMax)
                {
                    return false;
                }
            }

            pm.Hits = Math.Max(1, pm.HitsMax - Math.Max(5, pm.HitsMax / 5));
            return pm.Hits < pm.HitsMax;
        }
'''),
])

edit(tests, [
    ('''//  12. The pen and the pests are replaced after a death and a taming.
''', '''//  12. The pen and the pests are replaced after a death and a taming.
// cc-P707 (the isle play-through, notes/cc-P707-isle-playthrough.md):
//  13. On the heal step an unhurt trainee with an unhurt pet gets a scratch to bandage, and Wren says so; a trainee or
//      pet already hurt gets none.
'''),
    ('''    // ---------------------------------------------------------------- 8 (P420 #4 = P421 #1)
''', '''    // ---------------------------------------------------------------- 13 (cc-P707)

    [Fact]
    public void AnUnhurtTraineeOnTheHealStepGetsAScratchToBandage()
    {
        var hand = new TutorialFarmhand();
        hand.MoveToWorld(new Point3D(3396, 2614, 0), Map.Trammel);
        using var p = new Player(true);
        p.Litter.Add(hand);
        Assert.Equal(1, TutorialFarm.Talk(p.Pm, hand));
        var pet = TutorialFarm.ChoosePet(p.Pm, "dog")!;
        p.Litter.Add(pet);
        pet.MoveToWorld(p.Pm.Location, p.Pm.Map);
        p.Record.StationsDone.Add(TutorialFarm.PestsKey);
        Assert.Equal(3, TutorialFarm.StepOf(p.Pm));

        // Nobody hurt: a scratch, and the line says what to do with it.
        pet.Hits = pet.HitsMax;
        p.Pm.Hits = p.Pm.HitsMax;
        var full = p.Pm.HitsMax;
        Assert.Equal(3, TutorialFarm.Talk(p.Pm, hand));
        Assert.True(p.Pm.Hits < full, $"hits {p.Pm.Hits} of {full}");
        Assert.True(p.Pm.Hits >= 1);
        Assert.False(TutorialFarm.Scratch(p.Pm)); // hurt now: no second scratch

        // The pet already hurt: the trainee is left alone.
        p.Pm.Hits = p.Pm.HitsMax;
        pet.Hits = pet.HitsMax / 2;
        Assert.False(TutorialFarm.Scratch(p.Pm));
        Assert.Equal(p.Pm.HitsMax, p.Pm.Hits);
    }

    // ---------------------------------------------------------------- 8 (P420 #4 = P421 #1)
'''),
])
print('ok')
