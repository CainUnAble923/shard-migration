"""cc-P707: the farm's practice bandage always works for a trainee on the heal step. Pinned's chance is (Healing + 10)%,
so a newcomer with no Healing heals one bandage in ten, while Wren's scratch heals itself back in about a minute; the
bot's run failed twice with Healing 30. The bandage still really heals (P453's rule: only a heal finishes the step).

    python -P edit_sureheal.py <code repo>
"""
import os
import sys

repo = sys.argv[1]
farm = os.path.join(repo, 'server', 'customizations', 'Tutorial', 'TutorialFarm.cs')
tests = os.path.join(repo, 'server', 'tests', 'Tutorial', 'TutorialFarmVerification.cs')
patch = os.path.join(repo, 'server', 'patches', 'Bandage-tutorial-real-heal.patch')


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
    ('''            BandageHealed = OnBandageHealed;
        }
''', '''            BandageHealed = OnBandageHealed;
            SureHeal = (healer, _) => healer is PlayerMobile pm && StepOf(pm) == 3; // cc-P707
        }
'''),
    ('''        public static Action<Mobile, Mobile>? BandageHealed { get; set; }
''', '''        public static Action<Mobile, Mobile>? BandageHealed { get; set; }

        /// <summary>
        /// cc-P707: asked by Bandage-tutorial-real-heal.patch before the healing roll (healer, patient). True makes the
        /// bandage heal: a trainee on the farm's heal step, whatever their Healing (pinned's chance is (Healing + 10)%, one
        /// in ten for a newcomer without it). The heal is still real, so BandageHealed still finishes the step.
        /// </summary>
        public static Func<Mobile, Mobile, bool>? SureHeal { get; set; }
'''),
])

edit(tests, [
    ('''//  13. On the heal step an unhurt trainee with an unhurt pet gets a scratch to bandage, and Wren says so; a trainee or
//      pet already hurt gets none.
''', '''//  13. On the heal step an unhurt trainee with an unhurt pet gets a scratch to bandage, and Wren says so; a trainee or
//      pet already hurt gets none.
//  14. On the heal step a trainee with no Healing heals with every bandage (the practice bandage works), and finishes the
//      step; off the step the stock chance stands.
'''),
    ('''    // ---------------------------------------------------------------- 8 (P420 #4 = P421 #1)
''', '''    // ---------------------------------------------------------------- 14 (cc-P707)

    [Fact]
    public void ATraineeWithNoHealingHealsWithEveryPracticeBandage()
    {
        using var p = new Player(true);
        p.Record.PetClaimed = true;
        p.Record.StationsDone.Add(TutorialFarm.PestsKey);
        p.Pm.Skills.Healing.Base = 0;
        p.Pm.Skills.Anatomy.Base = 0;
        Assert.Equal(3, TutorialFarm.StepOf(p.Pm));
        Assert.True(TutorialFarm.SureHeal?.Invoke(p.Pm, p.Pm));

        // Ten bandages at a one-in-ten chance would all heal once in ten billion runs; the practice bandage always does.
        for (var i = 0; i < 10; i++)
        {
            p.Pm.Hits = p.Pm.HitsMax - 20;
            var before = p.Pm.Hits;
            new Bandaging(p.Pm, p.Pm, 0).Finish();
            Assert.True(p.Pm.Hits > before, $"bandage {i + 1}: hits {p.Pm.Hits}, before {before}");
            if (i == 0)
            {
                Assert.Contains(TutorialFarm.HealKey, p.Record.StationsDone);
                Assert.Equal(4, TutorialFarm.StepOf(p.Pm));
                Assert.False(TutorialFarm.SureHeal?.Invoke(p.Pm, p.Pm)); // off the step: the stock chance again
                p.Record.StationsDone.Remove(TutorialFarm.HealKey); // back on the step for the other nine
            }
        }
    }

    // ---------------------------------------------------------------- 8 (P420 #4 = P421 #1)
'''),
])

# The patch: a second hunk before the healing roll; the heal hunk moves down two lines.
p = open(patch, 'rb').read().decode('utf-8')
assert '@@ -416,6 +416,8 @@' in p and 'SureHeal' not in p
head, rest = p.split('@@ -416,6 +416,8 @@', 1)
hunk1 = ('@@ -375,6 +375,8 @@\n'
         '             var healing = Healer.Skills[primarySkill].Value;\n'
         '             var anatomy = Healer.Skills[secondarySkill].Value;\n'
         '             var chance = (healing + 10.0) / 100.0 - Slips * 0.02;\n'
         '+            // Shattered Legacy (cc-P707): the tutorial farm\'s practice bandage works, whatever the trainee\'s Healing.\n'
         '+            if (Server.Tutorial.TutorialFarm.SureHeal?.Invoke(Healer, Patient) == true) { chance = 1.0; }\n'
         ' \n'
         '             if (chance > Utility.RandomDouble())\n'
         '             {\n')
open(patch, 'wb').write((head + hunk1 + '@@ -416,6 +418,8 @@' + rest).encode('utf-8'))
print('ok')
