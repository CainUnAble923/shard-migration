"""cc-P722: compare trammel.mapops at 9ee74b6 (stock land), P720's parent and P720 (both on the SoS copy).

Splits each file by 8x8 block (block = (x >> 3) * 512 + (y >> 3), facet 1 is 7168 x 4096) and reports, for the blocks
P720 changed: whether the base fingerprints (B lines) agree between stock and SoS, and how the lines differ.
Usage: mapops_compare.py <dir with mapops-9ee74b6.txt, mapops-p720parent.txt, mapops-41fe8c1.txt>
"""
import sys
from collections import defaultdict

D = sys.argv[1]

def load(name):
    blocks = defaultdict(list)   # block -> op lines (L/S+/S-)
    fp = {}                      # block -> fingerprint
    head = []
    for line in open(D + "/" + name, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#") or line.startswith("F "):
            head.append(line)
            continue
        parts = line.split()
        if parts[0] == "B":
            fp[int(parts[1])] = parts[2]
            continue
        x, y = int(parts[1]), int(parts[2])
        blocks[(x >> 3) * 512 + (y >> 3)].append(line)
    return head, blocks, fp

stock = load("mapops-9ee74b6.txt")
par = load("mapops-p720parent.txt")
new = load("mapops-41fe8c1.txt")

def bxy(b):
    return (b // 512) * 8, (b % 512) * 8

changed = sorted(b for b in set(par[1]) | set(new[1]) | set(par[2]) | set(new[2])
                 if par[1].get(b) != new[1].get(b) or par[2].get(b) != new[2].get(b))
print("blocks P720 changed:", len(changed))
xs = [bxy(b) for b in changed]
print("their x range", min(x for x, _ in xs), max(x for x, _ in xs) + 7, "y range", min(y for _, y in xs), max(y for _, y in xs) + 7)

fp_same = fp_diff = fp_missing = 0
for b in changed:
    s, n = stock[2].get(b), new[2].get(b)
    if s is None or n is None:
        fp_missing += 1
    elif s == n:
        fp_same += 1
    else:
        fp_diff += 1
print("fingerprints stock vs P720: same", fp_same, "differ", fp_diff, "missing on one side", fp_missing)

same_lines = sum(1 for b in changed if stock[1].get(b) == par[1].get(b))
print("changed blocks whose lines at 9ee74b6 equal P720's parent:", same_lines, "of", len(changed))

# Blocks that differ between stock and P720's parent outside the changed set (the swap's own differences).
other = sorted(b for b in set(stock[1]) | set(par[1]) | set(stock[2]) | set(par[2])
               if b not in set(changed) and (stock[1].get(b) != par[1].get(b) or stock[2].get(b) != par[2].get(b)))
print("blocks stock vs parent differ elsewhere (the swap):", len(other))
for b in other[:12]:
    x, y = bxy(b)
    print("  block", b, "x", x, "y", y, "stock lines", len(stock[1].get(b, [])), "parent lines", len(par[1].get(b, [])),
          "fp", stock[2].get(b), par[2].get(b))
