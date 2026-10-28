"""cc-P722: resolve SOURCE.txt for the stock-land release: no cc-P675 (SoS re-base) lines; the isle notes in
stock-land words."""
import re
import sys

p = sys.argv[1] + "/player-package/vendor/shattered-legacy-map/SOURCE.txt"
s = open(p, encoding="utf-8", newline="").read()
pat = re.compile(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)
assert len(pat.findall(s)) == 1
I = " " * 17
text = (
    I + "cc-P662, 2026-10-26: the Wakening Isle (x 6594-6865, y 3905-4049, site A of cc-P673), on void.\n"
    + I + "cc-P720, 2026-10-28 (Chase's isle walk, round 2): the isle rebuilt in place by the same driver\n"
    + I + "(notes/cc-P662-tools/build_isle.py): the bank and the lodge as OSI's stone shop (windows, pitched\n"
    + I + "shingle roof, gable) and furnished; no meadow fence; no flowers by the road; the sand under the dock's\n"
    + I + "shore end at the beach's height, so the planks are one step up. P720 built it on the SoS copy; this\n"
    + I + "stock-land file (release/isle-20261028, cc-P722) takes the same lines for its 44 changed blocks, which\n"
    + I + "sit on void in both maps (their B fingerprints are the same on both).\n"
)
s = pat.sub(lambda m: m.group(1) + text, s)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
