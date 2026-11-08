r"""cc-P817: the map SOURCE.txt entry, and CHANGELOG/VERSION, in a code copy.

    python -P source_and_changelog.py <code copy> <version>
"""
import sys

root, version = sys.argv[1], sys.argv[2]

p = root + '/player-package/vendor/shattered-legacy-map/SOURCE.txt'
s = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
anchor = ("                 the isle's stock art, these are tile numbers and places, not EA's files." + nl)
assert s.count(anchor) == 1, s.count(anchor)
entry = (
    "                 cc-P817, 2026-11-07 (Chase 11-07: the isle bank's \"sign and deco are not optimized\"): two\n"
    "                 of the bank's statics, by hand in this file and in the driver's isle-sets.json (so a rebuild\n"
    "                 lays the same): the strongbox 0x09A8 from 6766,3974 to 6762,3973 on the back wall, and the\n"
    "                 potted plant 0x11CA inside at 6766,3978 removed. One S+ line moved, one gone; no B line changed\n"
    "                 (they fingerprint EA's base). notes/cc-P817-tools/bank_statics.py.\n"
).replace('\n', nl)
s = s.replace(anchor, anchor + entry)
open(p, 'w', encoding='utf-8', newline='').write(s)

p = root + '/CHANGELOG.md'
s = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
v = open(root + '/VERSION', encoding='utf-8').read().strip()
anchor = '## ' + v
assert s.count(anchor) == 1, (anchor, s.count(anchor))
section = (
    '## ' + version + '\n\n'
    '### Changed\n'
    '- Character creation: humans only, Tutorial Island start, a brighter wake, and your pet waits at the end of the isle.\n'
    '- The trade (Blacksmith) starting choice is gone; you can still pick Blacksmithy, Mining, Tailoring and Tinkering with "Choose my own skills".\n'
    '- On the Wakening Isle, Merrin the banker faces his counter and tells you what to do as you walk in, and the island bank is tidier: its lesson sign stands by the path instead of before the door.\n\n'
    '### Staff\n'
    '- The creation screen\'s race row and profession list need the new player package; the server already makes any other race Human and refuses the Blacksmith choice.\n\n'
).replace('\n', nl)
s = s.replace(anchor, section + anchor, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
open(root + '/VERSION', 'w', encoding='utf-8', newline='').write(version + '\n')
print('ok', v, '->', version)
