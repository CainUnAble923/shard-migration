"""cc-P733: check the release branch's merged trammel.mapops is the branch's stock-land file (c925c0f) with exactly
P725's changed blocks replaced by main's P725 lines; every other block, every fingerprint and the header stay the
branch's; and P725's changed blocks have the same fingerprints on both maps (void on both).
Usage: mapops_verify_merge.py <release worktree> <merged trammel.mapops>
"""
import subprocess
import sys
from collections import defaultdict

W, merged_path = sys.argv[1], sys.argv[2]
PATH = "player-package/vendor/shattered-legacy-map/trammel.mapops"


def parse(text):
    blocks = defaultdict(list)
    fp = {}
    head = []
    for line in text.splitlines():
        if not line or line.startswith("#") or line.startswith("F "):
            head.append(line)
            continue
        p = line.split()
        if p[0] == "B":
            fp[int(p[1])] = p[2]
            continue
        blocks[(int(p[1]) >> 3) * 512 + (int(p[2]) >> 3)].append(line)
    return head, blocks, fp


def at(rev):
    return parse(subprocess.run(["git", "-C", W, "show", f"{rev}:{PATH}"], capture_output=True, text=True,
                                encoding="utf-8", check=True).stdout)


stock = at("c925c0f")
par = at("92f6392^1")
new = at("92f6392")
got = parse(open(merged_path, encoding="utf-8").read())

changed = {b for b in set(par[1]) | set(new[1]) if par[1].get(b) != new[1].get(b)}
xs = sorted(((b // 512) * 8) for b in changed)
ys = sorted(((b % 512) * 8) for b in changed)
bad = []
for b in set(stock[1]) | set(got[1]) | set(new[1]):
    want = new[1].get(b, []) if b in changed else stock[1].get(b, [])
    if got[1].get(b, []) != want:
        bad.append(b)
fp_same = all(stock[2].get(b) == new[2].get(b) for b in changed)
par_same = all(stock[1].get(b, []) == par[1].get(b, []) for b in changed)
print("isle blocks taken from P725:", len(changed), "x", xs[0], "-", xs[-1] + 7, "y", ys[0], "-", ys[-1] + 7)
print("their fingerprints the same on stock (c925c0f) and SoS (main):", fp_same)
print("their lines on the branch equal P725's parent's:", par_same)
print("blocks not as expected:", len(bad), sorted(bad)[:10])
print("fingerprints equal the branch's:", got[2] == stock[2], "count", len(got[2]))
print("header equal the branch's:", got[0] == stock[0])
