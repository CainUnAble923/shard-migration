"""cc-P722: TutorialCoreTrials.cs core.loop line: P720's signpost wording with P721's "about a minute"."""
import re
import sys

p = sys.argv[1] + "/server/customizations/Tutorial/TutorialCoreTrials.cs"
s = open(p, encoding="utf-8", newline="").read()
pat = re.compile(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)
blocks = pat.findall(s)
assert len(blocks) == 1
ours = blocks[0][0]
assert "lesson's signpost there" in ours and "under a minute" in ours
s = pat.sub(lambda m: m.group(1).replace("it lasts under a minute", "it lasts about a minute"), s)
assert "<<<<<<<" not in s
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
