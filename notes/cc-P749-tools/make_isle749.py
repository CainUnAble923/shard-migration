"""cc-P749: the release's bot route. P733's isle.py (the release's stock New Haven), with P740's two wake-timing edits;
then run main's notes/cc-P741-tools/make_isle741.py on the result for the turned-round farm.
Usage: python -P make_isle749.py <P733 isle.py> <out step-1 isle.py>
"""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8", newline="").read()
for a, b in [
    ('        # cc-P728: down until the first move; "Move to get up." after 8 s; no window while lying',
     '        # cc-P728: down until the first move; "Move to get up." (cc-P740: after 4 s); no window while lying'),
    ("(refused: %d)\" % took)\n        pc.sleep(3.0)\n",
     "(refused: %d)\" % took)\n        pc.sleep(5.0)  # cc-P740: the slow get-up (about 3 s), then the dawn (2 s), then the first lines\n"),
]:
    assert s.count(a) == 1, (s.count(a), a)
    s = s.replace(a, b)
open(dst, "w", encoding="utf-8", newline="").write(s)
print("wrote", dst)
