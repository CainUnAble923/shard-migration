# cc-P804: the release branch's two conflicts, and its own New Haven (before the SoS move: the Order's hall, the trades yard).
import re
R = 'D:/UO/golems/Iron/p804-isle/'
p = R + 'server/customizations/Tutorial/TutorialStations.cs'
s = open(p, encoding='utf-8', newline='').read()
m = re.search(r'<<<<<<< ours\r?\n(.*?)=======\r?\n.*?>>>>>>> theirs\r?\n', s, re.S)
if m:
    s = s[:m.start()] + m.group(1).replace('Herbalism (not available yet)', 'Herbalism (the wild garlic in the yard)') + s[m.end():]
    open(p, 'w', encoding='utf-8', newline='').write(s)
p = R + 'docker/uo/apply-patches.sh'
s = open(p, encoding='utf-8', newline='').read()
m = re.search(r'<<<<<<< ours\r?\n(.*?)=======\r?\n.*?>>>>>>> theirs\r?\n', s, re.S)
if m:
    add = '''
# cc-P804 (F-51): the Herbalism skill and the reagent lane. Last: the lane's context includes the raised bed hooks above.
apply_patch "$PATCHES/Skills-herbalism.patch"
apply_patch "$PATCHES/skills-json-herbalism.patch"
apply_patch "$PATCHES/FeatureFlagManager-skill-count.patch"
apply_patch "$PATCHES/Plants-herbalism-lane.patch"
'''
    s = s[:m.start()] + m.group(1) + add + s[m.end():]
    open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
