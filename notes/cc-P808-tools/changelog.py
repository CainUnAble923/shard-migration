# cc-P808: the CHANGELOG section and VERSION. python -P changelog.py <repo> <old version> <new version>
import sys
repo, old, new = sys.argv[1:4]
sec = f'''## {new}

### Added
- The Clockwork Scavenger: reach Journeyman in the Tinkers' Union and ask a Tinker guildmaster about the "scavenger". Gather the parts (gears, springs, clock parts, an axle with gears and iron ingots), use the frame, and a little brass crawler follows you and picks gold, gems and reagents from the monsters you kill. Choose what it collects in its Options. It takes only what you could loot yourself, never from players. With a Clockwork Load Harness III on your mule, it carries the loot to the mule instead. One per character.

### Staff
- The Scavenger's parts, look, reach and pace are in Configuration/clockwork-scavenger.json, written with the defaults on first start.

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
