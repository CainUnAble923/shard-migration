# cc-P804: copies the new files to the isle copy and sets the release's own New Haven (before the SoS move) in its defaults.
import shutil, os
M = 'D:/UO/golems/Iron/ShatteredLegacy/'
I = 'D:/UO/golems/Iron/p804-isle/'
os.makedirs(I + 'server/customizations/Herbalism', exist_ok=True)
for f in os.listdir(M + 'server/customizations/Herbalism'):
    shutil.copy(M + 'server/customizations/Herbalism/' + f, I + 'server/customizations/Herbalism/' + f)
for f in ['server/tests/Misc/HerbalismVerification.cs', 'client/patches/0011-unplaced-skills.patch', 'server/patches/Skills-herbalism.patch',
          'server/patches/skills-json-herbalism.patch', 'server/patches/FeatureFlagManager-skill-count.patch', 'server/patches/Plants-herbalism-lane.patch',
          'server/customizations/Tutorial/TutorialTradeTrials.cs'][:6]:
    shutil.copy(M + f, I + f)
p = I + 'server/customizations/Herbalism/HerbalismSettings.cs'
s = open(p, encoding='utf-8', newline='').read()
for a, b in [('TableX { get; set; } = 3606', 'TableX { get; set; } = 3458'), ('TableY { get; set; } = 2500', 'TableY { get; set; } = 2566'),
             ('public int TableZ { get; set; }', 'public int TableZ { get; set; } = 35;'),
             ('S("Garlic", 3625, 2558), S("Ginseng", 3628, 2562), S("Garlic", 3610, 2565), S("Ginseng", 3604, 2570)',
              'S("Garlic", 3432, 2630), S("Ginseng", 3436, 2634), S("Garlic", 3420, 2640), S("Ginseng", 3414, 2646)')]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
