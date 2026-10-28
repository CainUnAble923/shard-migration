"""cc-P722: check the release branch's merged trammel.mapops is 9ee74b6's stock-land file with exactly P720's isle
blocks replaced (lines per block equal P720's; every other block, fingerprint and header line equal 9ee74b6's).
Usage: mapops_verify_merge.py <dir with the three mapops-*.txt> <merged trammel.mapops>
"""
import sys
from collections import defaultdict

D, merged_path = sys.argv[1], sys.argv[2]

def load(path):
    blocks = defaultdict(list)
    fp = {}
    head = []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#") or line.startswith("F "):
            head.append(line)
            continue
        p = line.split()
        if p[0] == "B":
            fp[int(p[1])] = p[2]
            continue
        blocks[(int(p[1]) >> 3) * 512 + (int(p[2]) >> 3)].append(line)
    return head, blocks, fp

stock = load(D + "/mapops-9ee74b6.txt")
par = load(D + "/mapops-p720parent.txt")
new = load(D + "/mapops-41fe8c1.txt")
got = load(merged_path)

changed = {b for b in set(par[1]) | set(new[1]) if par[1].get(b) != new[1].get(b)}
bad = []
for b in set(stock[1]) | set(got[1]) | set(new[1]):
    want = new[1].get(b, []) if b in changed else stock[1].get(b, [])
    if got[1].get(b, []) != want:
        bad.append(b)
print("isle blocks taken from P720:", len(changed))
print("blocks not as expected:", len(bad), sorted(bad)[:10])
print("fingerprints equal 9ee74b6's:", got[2] == stock[2], "count", len(got[2]))
print("header equal 9ee74b6's:", got[0] == stock[0], got[0][:3])
ops = sum(len(v) for v in got[1].values())
print("op lines:", ops, "S+ lines:", sum(1 for v in got[1].values() for l in v if l.startswith("S+")))
sys.exit(1 if bad or got[2] != stock[2] or got[0] != stock[0] else 0)
