"""Resolve the CHANGELOG.md and VERSION conflicts of the P742 pick on release/isle-20261028.

Keeps main's 2026.10.31.7 section (P742's one line) and drops whatever main's side of the conflict
carries beyond it (2026.10.31.5, a section of a task not in the release). VERSION becomes 2026.10.31.7.
Usage: python resolve_p742.py <release worktree>
"""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])

(root / "VERSION").write_text("2026.10.31.7\n", encoding="utf-8", newline="\n")

cl = root / "CHANGELOG.md"
text = cl.read_text(encoding="utf-8")
m = re.search(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", text, re.S)
assert m, "no conflict block"
ours, theirs = m.group(1), m.group(2)
assert ours.strip() == "", "unexpected release-side lines: %r" % ours
sec = re.search(r"(## 2026\.10\.31\.7\n.*?)(?=^## )", theirs, re.S | re.M)
assert sec, "P742 section not found"
keep = sec.group(1)
assert "dungeon shrine" in keep
text = text[: m.start()] + keep + text[m.end():]
assert "<<<<<<<" not in text and ">>>>>>>" not in text
cl.write_text(text, encoding="utf-8", newline="\n")
print("resolved; kept:\n" + keep)
