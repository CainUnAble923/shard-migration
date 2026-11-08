r"""cc-P817: CHANGELOG/VERSION only (the isle release copy; its map SOURCE entry comes with the diff).

    python -P changelog_isle.py <isle code copy> <version>
"""
import sys
root, version = sys.argv[1], sys.argv[2]
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
