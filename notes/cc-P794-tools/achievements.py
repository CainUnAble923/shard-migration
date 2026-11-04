r"""cc-P794: every achievement of 75 AP or more with no reward item, from ClusterFAchievements.cs, for the route proposal. Read only."""
import re

s = open("D:/UO/golems/Iron/ShatteredLegacy/server/customizations/ClusterFAchievements.cs", encoding="utf-8").read()
parts = re.split(r'(?=\n\s+Reg\(")', s)
rows = []
for p in parts:
    m = re.match(r'\n\s+Reg\("([^"]+)",\s*"([^"]+)",\s*"([^"]*)"', p)
    ap = re.search(r"ap:\s*(\d+)", p)
    if not m or not ap:
        continue
    rows.append((int(ap.group(1)), m.group(1), m.group(2), m.group(3)[:90], "rewardItems" in p, "hidden: true" in p, "retired:" in p and "retired:          true" in p))
print(len(rows), "achievements;", sum(1 for r in rows if r[4]), "with a reward item")
for r in sorted(rows, reverse=True):
    if r[0] >= 50 and not r[4] and not r[6]:
        print(r[0], r[1], "|", r[2], "|", r[3], "| hidden" if r[5] else "")
print("retired:", sum(1 for r in rows if r[6]))
