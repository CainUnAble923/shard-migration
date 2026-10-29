"""Resolve CHANGELOG/VERSION conflicts on the release branch: keep the picked task's own
section (main's number), drop sections already on the branch or left out (P727's .6)."""
import re, sys
root = sys.argv[1]
drop = set(sys.argv[2:])  # section versions to drop, e.g. 2026.10.28.6
p = root + "/CHANGELOG.md"
s = open(p, encoding="utf-8").read()
def fix(m):
    theirs = m.group(2)
    parts = re.split(r"(?m)^(?=## )", theirs)
    keep = [x for x in parts if not any(x.startswith("## " + d + "\n") for d in drop)]
    return m.group(1) + "".join(keep)
s2, n = re.subn(r"(?ms)^<<<<<<< [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n", fix, s)
open(p, "w", encoding="utf-8", newline="").write(s2)
v = re.findall(r"(?m)^## (\d{4}\.\d\d\.\d\d(?:\.\d+)?)$", s2.split("-->", 1)[1])[0]
open(root + "/VERSION", "w", newline="").write(v + "\n")
print("hunks", n, "VERSION", v)
