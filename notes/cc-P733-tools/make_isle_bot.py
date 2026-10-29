"""cc-P731: P726's isle.py (main's New Haven, after P678) with Rook's and the New Haven start's spots back on the
stock land, as P722 did for the release branch. Usage: python -P make_isle_bot.py <P726 isle.py> <out isle.py>."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8", newline="").read()
for a, b, n in [
    ("ROOK_EXIT = (3632, 2584)     # HavenSpots.MoongateExit, beside Rook (3631,2584); cc-P727: main's New Haven (P678)",
     "ROOK_EXIT = (3501, 2572)     # HavenSpots.MoongateExit, beside Rook (3500,2572); cc-P731: stock New Haven (no P678)", 1),
    ("HAVEN_START = (3634, 2586)   # HavenSpots.Start (cc-P727: main's New Haven, P678)",
     "HAVEN_START = (3503, 2574)   # HavenSpots.Start (cc-P731: stock New Haven, as P722)", 1),
    ("(3631, 2584)", "(3500, 2572)", 2),
]:
    assert s.count(a) == n, (s.count(a), a)
    s = s.replace(a, b)
open(dst, "w", encoding="utf-8", newline="").write(s)
print("wrote", dst)
