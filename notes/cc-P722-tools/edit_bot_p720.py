"""cc-P722: teach the isle route P720's isle, which P721's copy never ran on (P721 branched before P720):
- the vision lesson's marker is the lesson's signpost (TutorialCorePlacement.SignpostId 0xA854, at SignPoint
  core.loop 6794,3981), not the blue rune (0x1F14) P720 replaced;
- Wren stands at the field gate behind P720's whole-field fence, so the road reaches 4 tiles from her (she is
  double-clicked from there; the lesson already passed that way);
- Merrin stands behind P720's counter: the bot walks to the bank floor in front of it (inside the south door).
"""
import sys

p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
subs = [
    ('    mk = pl.item_at(STONES, 0x1F14, 2)\n'
     '    if not log.check(mk is not None, "the blue rune stone lies at %s" % (STONES,)):\n',
     '    mk = pl.item_at(LOOP_SIGN, 0xA854, 1)  # cc-P722: P720 made the marker the lesson\'s signpost\n'
     '    if not log.check(mk is not None, "the lesson\'s signpost stands at %s" % (LOOP_SIGN,)):\n'),
    ('    log("  -> double-clicked the rune stone: the vision")\n',
     '    log("  -> double-clicked the lesson\'s signpost: the vision")\n'),
    ('STONES = (6794, 3982)\n',
     'STONES = (6794, 3982)\nLOOP_SIGN = (6794, 3981)                   # cc-P722: TutorialCorePlacement.SignPoint("core.loop")\n'
     'BANK_FLOOR = (6762, 3978)                  # cc-P722: inside the south door, in front of P720\'s counter\n'),
    ('    walk_to(pl, log, MERRIN, 2, "Merrin inside the practice bank")\n',
     '    walk_to(pl, log, BANK_FLOOR, 1, "the bank floor in front of Merrin\'s counter")\n'),
]
for a, b in subs:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
# Wren: the field fence keeps the road 4 tiles from her
i = s.index('"Wren at the farm gate')
j = s.rindex("walk_to(", 0, i)
line = s[j:s.index("\n", j)]
assert ", 3, " in line, line
s = s[:j] + line.replace(", 3, ", ", 4, ") + s[s.index("\n", j):]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
