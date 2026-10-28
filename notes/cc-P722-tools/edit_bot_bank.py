"""cc-P722 run 3: the bot's planner found no path from the square into P720's bank (6761,3982 to the floor), while a
real TazUO character walked it both ways (runs/walks/walk-bank2.txt). The bot now takes the real character's way:
round the lesson's signpost (6762,3982) to 6763,3981, onto the door's line at 6762,3981, then through the door."""
import sys

p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
a = '    walk_to(pl, log, BANK_FLOOR, 1, "the bank floor in front of Merrin\'s counter")\n'
b = ('    for step in ((6763, 3981), (6762, 3981)):  # cc-P722: round the lesson\'s signpost, onto the door\'s line\n'
     '        walk_to(pl, log, step, 0, "the bank\'s doorstep %s" % (step,))\n'
     '    walk_to(pl, log, BANK_FLOOR, 1, "the bank floor in front of Merrin\'s counter")\n')
assert s.count(a) == 1
s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
