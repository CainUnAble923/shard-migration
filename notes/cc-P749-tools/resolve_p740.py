"""cc-P749: resolve P740's CHANGELOG/VERSION conflicts on release/isle-20261028.
Keep main's 2026.10.30.3 section (P740's two lines); drop main's 2026.10.30 Staff section (the SoS swap's credits).
VERSION takes main's number for the section, 2026.10.30.3.
Usage: resolve_p740.py <release worktree>
"""
import re
import sys

W = sys.argv[1]
p = W + "/CHANGELOG.md"
t = open(p, encoding="utf-8").read()
m = re.search(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", t, re.S)
assert m and m.group(1) == "", m and m.group(1)
theirs = m.group(2)
keep, _, dropped = theirs.partition("## 2026.10.30\n")
assert keep.startswith("## 2026.10.30.3\n") and "Siege of Sosaria" in dropped and "\n## " not in dropped, theirs
t = t[:m.start()] + keep + t[m.end():]
assert "<<<<<<<" not in t and ">>>>>>>" not in t
open(p, "w", encoding="utf-8", newline="\n").write(t)
open(W + "/VERSION", "w", encoding="utf-8", newline="\n").write("2026.10.30.3\n")
print("resolved; kept", keep.count("\n- "), "lines")
