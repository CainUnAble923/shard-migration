"""cc-P856: one-off. The CHANGELOG section and VERSION, on main (2026.11.10.2: P855, not merged yet, takes 2026.11.10) and
on the release copy (2026.11.10, after its 2026.11.08.3). python -P changelog.py <code copy folder> <version>"""
import os
import sys

root, version = sys.argv[1], sys.argv[2]
p = os.path.join(root, "CHANGELOG.md")
s = open(p, encoding="utf-8").read()
section = """## %s

### Added
- New Haven dresses up for winter from December 1: a Christmas train with turning wheels, smoke and lights, a big walk-round snow globe with falling snow, a Santa bench and a snowman bench. They go when the winter decorations come down after January 6.
- The Festival's winter stock has a Santa bench, a snowman bench and a holiday fireplace with stockings and a bear rug, for your house. Each piece names the player who designed it.

""" % version
i = s.index("-->\n") + len("-->\n")
rest = s[i:].lstrip("\n")
s = s[:i] + "\n" + section + rest
open(p, "w", encoding="utf-8", newline="\n").write(s)
open(os.path.join(root, "VERSION"), "w", newline="\n").write(version + "\n")
print("ok", root, version)
