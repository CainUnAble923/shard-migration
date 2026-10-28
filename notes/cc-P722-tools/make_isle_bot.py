"""cc-P722: P721's isle.py (from origin/golem/Iron/P723) as notes/cc-P722-tools/isle.py, with Rook's and the New Haven
start's spots back on the stock land's New Haven (release/isle-20261028 has no P678 move: HavenSpots.MoongateExit is
3501,2572,14, as in P707's isle.py)."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8", newline="").read()
subs = [
    ("ROOK_EXIT = (3632, 2584)     # HavenSpots.MoongateExit, beside Rook (3631,2584); cc-P718: P678 moved New Haven",
     "ROOK_EXIT = (3501, 2572)     # HavenSpots.MoongateExit, beside Rook (3500,2572); cc-P722: stock New Haven (no P678)"),
    ("HAVEN_START = (3634, 2586)   # HavenSpots.Start (cc-P718: P678 moved New Haven)",
     "HAVEN_START = (3503, 2574)   # HavenSpots.Start (cc-P722: stock New Haven, as P707)"),
    ('rook = pl.mobile_at((3631, 2584), 2, "Rook")', 'rook = pl.mobile_at((3500, 2572), 2, "Rook")'),
]
for a, b in subs:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
assert "3631" not in s and "3632" not in s and "3634" not in s
s = '"""cc-P722: P721\'s isle.py with New Haven on the stock land (release/isle-20261028).\n\n' + s[3:]
open(dst, "w", encoding="utf-8", newline="").write(s)
print("ok")
