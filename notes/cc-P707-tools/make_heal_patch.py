"""cc-P707: writes server/patches/Bandage-tutorial-real-heal.patch from the Bandage.cs the build has when it applies it
(pinned's, after Bandage-pet-mimic-targeting, -heal-scaled-200, -searing-wounds and -unhurt-patient-achievement), so it
applies with --fuzz=0 and leaves Bandage-asclepius-bonus.patch's context (the healing, anatomy and chance lines) alone.

    python -P make_heal_patch.py <Bandage.cs before the tutorial patch> <code repo>

The changes: P453's heal hook after Patient.Heal (as before), P707's practice bandage on the roll's line, and P707's
unhurt-patient hook in BeginHeal and at the end of the heal.
"""
import difflib
import os
import sys

before_path, repo = sys.argv[1], sys.argv[2]
before = open(before_path, 'rb').read().decode('utf-8')
nl = '\r\n' if '\r\n' in before else '\n'
after = before


def sub(old, new):
    global after
    old, new = old.replace('\n', nl), new.replace('\n', nl)
    assert after.count(old) == 1, old[:60]
    after = after.replace(old, new)


sub('''
            if (chance > Utility.RandomDouble())
            {
                healerNumber = 500969; // You finish applying the bandages.''', '''
            // Shattered Legacy (cc-P707): the tutorial farm's practice bandage works whatever the trainee's Healing, when
            // nothing slipped (TutorialFarm.SureHeal; a slip still fails it, as cc-P453's fact wants).
            if (chance > Utility.RandomDouble() || Slips == 0 && Server.Tutorial.TutorialFarm.SureHeal?.Invoke(Healer, Patient) == true)
            {
                healerNumber = 500969; // You finish applying the bandages.''')
sub('''                Patient.Heal((int)toHeal, Healer, false);
''', '''                Patient.Heal((int)toHeal, Healer, false);
                // Shattered Legacy (cc-P453): a bandage that really healed; the tutorial farm's heal step listens.
                Server.Tutorial.TutorialFarm.BandageHealed?.Invoke(Healer, Patient);
''')

# cc-P707 run 4: a bandage that finds its patient unhurt, as it ends (the hits came back during the delay) and as it
# begins; the tutorial farm's heal step gives the trainee a scratch instead (TutorialFarm.Unhurt).
sub('''                Healer.SendLocalizedMessage(1010395); // You heal what little damage your patient had.
''', '''                // Shattered Legacy (cc-P707): on the tutorial farm's heal step, a scratch to bandage instead.
                if (Server.Tutorial.TutorialFarm.Unhurt?.Invoke(Healer, Patient) != true)
                {
                    Healer.SendLocalizedMessage(1010395); // You heal what little damage your patient had.
                }
''')
sub('''            healer.SendLocalizedMessage(500955); // That being is not damaged!
            ClusterFJokeAchievements.HealedUnhurt(healer); // Shattered Legacy (cc-P231): a joke achievement
''', '''            // Shattered Legacy (cc-P707): on the tutorial farm's heal step, a scratch to bandage instead.
            if (Server.Tutorial.TutorialFarm.Unhurt?.Invoke(healer, patient) != true)
            {
                healer.SendLocalizedMessage(500955); // That being is not damaged!
                ClusterFJokeAchievements.HealedUnhurt(healer); // Shattered Legacy (cc-P231): a joke achievement
            }
''')

name = 'Projects/UOContent/Items/Skill Items/Misc/Bandage.cs'
diff = difflib.unified_diff(before.split(nl), after.split(nl), '"a/%s"' % name, '"b/%s"' % name, n=3, lineterm='')
lines = list(diff)
lines[0] = '--- "a/%s"' % name
lines[1] = '+++ "b/%s"' % name
out = '\n'.join(lines) + '\n'
open(os.path.join(repo, 'server', 'patches', 'Bandage-tutorial-real-heal.patch'), 'wb').write(out.encode('utf-8'))
print(out)
