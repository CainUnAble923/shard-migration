"""cc-P727: P722's isle.py (P721's route taught P720's isle) with Rook's and the New Haven start's spots on main's New
Haven again (P678's move: HavenSpots.MoongateExit 3632,2584, Start 3634,2586, Rook 3631,2584, as P718's isle.py had)."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8', newline='').read()
subs = [
    ("ROOK_EXIT = (3501, 2572)     # HavenSpots.MoongateExit, beside Rook (3500,2572); cc-P722: stock New Haven (no P678)",
     "ROOK_EXIT = (3632, 2584)     # HavenSpots.MoongateExit, beside Rook (3631,2584); cc-P727: main's New Haven (P678)"),
    ("HAVEN_START = (3503, 2574)   # HavenSpots.Start (cc-P722: stock New Haven, as P707)",
     "HAVEN_START = (3634, 2586)   # HavenSpots.Start (cc-P727: main's New Haven, P678)"),
]
for a, b in subs:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
n = s.count('pl.mobile_at((3500, 2572)')
assert n == 2, n
s = s.replace('pl.mobile_at((3500, 2572)', 'pl.mobile_at((3631, 2584)')
assert '3500, 2572' not in s and '3501, 2572' not in s and '3503, 2574' not in s
s = s.replace('"""cc-P722: P721\'s isle.py with New Haven on the stock land (release/isle-20261028).',
              '"""cc-P727: P722\'s isle.py with New Haven on main\'s land again (P678).', 1)
open(dst, 'w', encoding='utf-8', newline='').write(s)
print('ok')
