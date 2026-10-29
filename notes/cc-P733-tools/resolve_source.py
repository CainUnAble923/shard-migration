"""cc-P733: resolve SOURCE.txt for the stock-land release: keep the branch's P720 lines (stock-land words) and add
P725's line in stock-land words (no SoS copy, no SoS block count)."""
import re
import sys

p = sys.argv[1] + "/player-package/vendor/shattered-legacy-map/SOURCE.txt"
s = open(p, encoding="utf-8", newline="").read()
pat = re.compile(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)
assert len(pat.findall(s)) == 1
I = " " * 17
text = (
    I + "cc-P725, 2026-10-29 (Chase 10-28: shore tiles, a tropical island): the isle rebuilt in place\n"
    + I + "by the same driver: the coast laid with OSI's surf pieces (0x179D-0x17B2) by a rule learned from\n"
    + I + "stock Trammel's sandy beaches (notes/cc-P725-tools/survey_rule.py, shore-rule.json), the first sand\n"
    + I + "ring at -4 in place of P662's plain water diamond, and the island planted with stock tropical art\n"
    + I + "(palms, banana, o'hii, OSI's jungle trees whole, ferns, pampas). P725 built it on both bases; this\n"
    + I + "stock-land file (release/isle-20261028, cc-P733) takes the same isle lines (they sit on void in both\n"
    + I + "maps), and is byte for byte P725's stock-base build (notes/cc-P725-tools/trammel-stock-base.mapops).\n"
)
s = pat.sub(lambda m: m.group(1) + text, s)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
