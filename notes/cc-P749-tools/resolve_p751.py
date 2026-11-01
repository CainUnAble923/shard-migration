"""cc-P749: resolve the P741+P746+P751 pick's CHANGELOG/VERSION conflicts on release/isle-20261028.
Keep main's 2026.10.31.4 section (the isle round's ten lines); drop main's 2026.10.31.3 (P750) and 2026.10.31 (P708)
Staff sections, both the guild headquarters on the SoS land. VERSION takes main's number, 2026.10.31.4.
Usage: resolve_p751.py <release worktree>
"""
import re
import sys

W = sys.argv[1]
p = W + "/CHANGELOG.md"
t = open(p, encoding="utf-8").read()
m = re.search(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", t, re.S)
assert m and m.group(1) == "", m and m.group(1)
theirs = m.group(2)
keep, _, dropped = theirs.partition("## 2026.10.31.3\n")
assert keep.startswith("## 2026.10.31.4\n") and "\n## " not in keep, keep
assert "\n## 2026.10.31\n" in dropped and "### Changed" not in dropped and "### Added" not in dropped, dropped
t = t[:m.start()] + keep + t[m.end():]
assert "<<<<<<<" not in t and ">>>>>>>" not in t
open(p, "w", encoding="utf-8", newline="\n").write(t)
open(W + "/VERSION", "w", encoding="utf-8", newline="\n").write("2026.10.31.4\n")
print("resolved; kept", keep.count("\n- "), "lines")
