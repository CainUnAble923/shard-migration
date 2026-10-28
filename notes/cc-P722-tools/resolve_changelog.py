"""cc-P722: resolve a cherry-pick's CHANGELOG.md / VERSION conflict on the release branch.

CHANGELOG.md: each conflict block is two new version sections (ours = the release branch's newest, theirs = the
pick's). Keep both, the pick's (newer) first, blank-line separated. VERSION: the pick's version.
Usage: resolve_changelog.py <worktree>
"""
import re
import sys

W = sys.argv[1]

def read(p):
    return open(p, encoding="utf-8", newline="").read()

def write(p, s):
    open(p, "w", encoding="utf-8", newline="").write(s)

pat = re.compile(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)

p = W + "/CHANGELOG.md"
s = read(p)
n = 0
def both(m):
    global n
    n += 1
    ours, theirs = m.group(1), m.group(2)
    return theirs.rstrip("\n") + "\n\n" + ours
s2 = pat.sub(both, s)
assert "<<<<<<<" not in s2 and ">>>>>>>" not in s2
write(p, s2)

v = W + "/VERSION"
vs = read(v)
if "<<<<<<<" in vs:
    m = pat.search(vs)
    write(v, m.group(2))
print("changelog blocks:", n, "VERSION:", read(v).strip())
