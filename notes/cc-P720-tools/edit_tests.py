"""cc-P720: the farm facts for the new layout (TutorialFarmVerification.cs)."""
import sys

p = sys.argv[1] + '/server/tests/Tutorial/TutorialFarmVerification.cs'
s = open(p, encoding='utf-8').read()


def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:90], s.count(old))
    s = s.replace(old, new)


rep('''            // cc-P663: the isle's farm: the same 330 pieces moved by (+3314, +1364), each at its height above the old ground.''',
    '''            // cc-P663: the isle's farm. cc-P720: its own design now (the cottage laid whole on the flat meadow, one fence
            // ring), so it is no longer New Haven's 330 pieces moved by (+3314, +1364).''')
rep('''            Assert.Equal(TutorialFarmLayout.Pieces.Length - 1, addon.Components.Count);''',
    '''            Assert.Equal(TutorialIsleFarmLayout.Pieces.Count(p => TutorialFarm.IsleArt(p.Id) != null), addon.Components.Count);''')
rep('''            var moved = TutorialFarmLayout.Pieces.Select(p => (p.Id, p.X + 3314, p.Y + 1364)).OrderBy(t => t).ToArray();
            Assert.Equal(moved, TutorialIsleFarmLayout.Pieces.Select(p => (p.Id, p.X, p.Y)).OrderBy(t => t).ToArray());
''', '''            Assert.True(TutorialFarm.IsCurrent(addon));
''')
rep('''            Assert.Equal(0x06AD, door!.ItemID);''',
    '''            Assert.Equal(0x06A5, door!.ItemID); // cc-P720: the cottage's door, in its south wall (WestCW)''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('edited', p)
