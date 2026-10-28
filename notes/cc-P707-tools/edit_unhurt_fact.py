"""cc-P707 run 4: fact 15, a bandage on the heal step that finds nobody hurt gives the trainee a scratch.

    python -P edit_unhurt_fact.py <code repo>
"""
import os
import sys

repo = sys.argv[1]
path = os.path.join(repo, 'server', 'tests', 'Tutorial', 'TutorialFarmVerification.cs')
text = open(path, 'rb').read().decode('utf-8')
nl = '\r\n' if '\r\n' in text else '\n'

anchor = '''    // ---------------------------------------------------------------- 8 (P420 #4 = P421 #1)
'''
fact = '''    // ---------------------------------------------------------------- 15 (cc-P707 run 4)

    [Fact]
    public void ABandageThatFindsNobodyHurtOnTheHealStepGivesAScratch()
    {
        using var p = new Player(true);
        p.Record.PetClaimed = true;
        p.Record.StationsDone.Add(TutorialFarm.PestsKey);
        Assert.Equal(3, TutorialFarm.StepOf(p.Pm));

        // As it ends: the trainee's hits came back during the bandage's delay (the play-through's run 4).
        p.Pm.Hits = p.Pm.HitsMax;
        new Bandaging(p.Pm, p.Pm, 0).Finish();
        Assert.True(p.Pm.Hits < p.Pm.HitsMax, $"hits {p.Pm.Hits} of {p.Pm.HitsMax}");
        Assert.Equal(3, TutorialFarm.StepOf(p.Pm)); // not finished: only a real heal does that

        // The next bandage treats the scratch and finishes the step.
        new Bandaging(p.Pm, p.Pm, 0).Finish();
        Assert.Equal(4, TutorialFarm.StepOf(p.Pm));

        // As it begins, back on the step: "That being is not damaged!" becomes a scratch.
        p.Record.StationsDone.Remove(TutorialFarm.HealKey);
        p.Pm.Hits = p.Pm.HitsMax;
        Assert.Null(BandageContext.BeginHeal(p.Pm, p.Pm));
        Assert.True(p.Pm.Hits < p.Pm.HitsMax, $"hits {p.Pm.Hits} of {p.Pm.HitsMax}");

        // Off the step, an unhurt patient is left alone.
        p.Record.StationsDone.Add(TutorialFarm.HealKey);
        p.Pm.Hits = p.Pm.HitsMax;
        Assert.False(TutorialFarm.OnUnhurt(p.Pm, p.Pm));
        Assert.Null(BandageContext.BeginHeal(p.Pm, p.Pm));
        Assert.Equal(p.Pm.HitsMax, p.Pm.Hits);
    }

'''
assert text.count(anchor.replace('\n', nl)) == 1
text = text.replace(anchor.replace('\n', nl), (fact + anchor).replace('\n', nl))
open(path, 'wb').write(text.encode('utf-8'))
print('edited', path)
