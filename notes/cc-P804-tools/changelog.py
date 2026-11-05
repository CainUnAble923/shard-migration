# cc-P804: the CHANGELOG section and VERSION. python -P changelog.py <repo> <old version> <new version>
import sys
repo, old, new = sys.argv[1:4]
sec = f'''## {new}

### Added
- Herbalism arrives: forage wild herbs and grow your own reagents. It's a new skill to 200 with the Order of the Alembic. Wild garlic, ginseng, mandrake, nightshade, blood moss and rarer herbs grow around the land and regrow after picking, and [herbalism keeps your ledger of finds. The Order's herb table in New Haven gives each character a bowl and seeds, and sells a raised bed deed. Plants in bowls grow at the usual pace, a bed is tended as one, and crossing plants of the same strain can breed a better one, up the metal ladder to Celestial. Harvest herbs, double-click them to work them into bundles, and open a bundle for reagents. Plants forgive a few days away, more as your skill rises. Green Thumb is yours for your first harvest. Vendors still sell reagents.

### Changed
- The Camping lesson now has you pick wild garlic with Herbalism.

### Staff
- Every Herbalism number and the wild patch list are in Configuration/herbalism.json, written with the defaults on first start. [Herbalism reload reads it again.
- Herbalism needs the new player package: the skill's name is written into each player's skill files, and the client shows a skill no saved group lists.

'''
p = repo + '/CHANGELOG.md'
s = open(p, encoding='utf-8', newline='').read()
if '\r\n' in s:
    sec = sec.replace('\n', '\r\n')
i = s.index('-->')
j = s.index(f'## {old}', i)
open(p, 'w', encoding='utf-8', newline='').write(s[:j] + sec + s[j:])
v = repo + '/VERSION'
t = open(v, encoding='utf-8', newline='').read()
assert old in t
open(v, 'w', encoding='utf-8', newline='').write(t.replace(old, new))
print('ok')
