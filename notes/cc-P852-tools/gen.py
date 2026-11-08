import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))
from verdicts import V
S = os.path.dirname(os.path.abspath(sys.argv[0]))
d = json.load(open(os.path.join(S, "survey.json")))
COST = {"D": "data", "C": "small code", "M": "medium code"}
GROUP = {"H": "holiday kit", "T": "town dressing", "F": "housing furniture", "S": "structures"}
assert set(V) == set(d), set(V) ^ set(d)

def author(src):
    first = src.splitlines()[0] if src else ""
    m = re.search(r", by (.+)$", first)
    return m.group(1).strip() if m else "?"

def dl(src):
    m = re.search(r"Downloaded 2026-(\d\d-\d\d)", src)
    return m.group(1) if m else "11-08"

notes, intake = [], []
for f in d:
    r = d[f]; g, what, fit, cost, terms, rec, why = V[f]
    a = author(r["source"])
    if f == "olorin-pond-bridge": a = "Celestial"
    size = f"{len(r['cs'])} .cs, {r['lines']} lines, {r['ser']} Ser"
    art = f"stock: {r['nids']} art IDs, all in our client" + (f" (up to 0x{r['maxid']:X})" if r["maxid"] >= 0x4000 else "")
    t = f"none stated; credit {a}" + (f"; {terms}" if terms else "")
    notes.append(f"| `{f}` | {a} | {GROUP[g]} | {what} | {fit} | {size}; {art} | {COST[cost]} | {t} | **{rec}**: {why} |")
    step = f"{rec}: {why} (notes/cc-P852-deco-addons-assessment.md)"
    intake.append(f"| {dl(r['source'])} | code/{f} | {what} ({a}) | {fit} | {t} | {size}; stock art only ({r['nids']} IDs, all in our client); port cost: {COST[cost]} | {step} | assess (P852): {rec} |")

open(os.path.join(S, "notes-table.md"), "w", encoding="utf-8").write("\n".join(notes) + "\n")
open(os.path.join(S, "intake-rows.md"), "w", encoding="utf-8").write("\n".join(intake) + "\n")
from collections import Counter
print(Counter(v[5] for v in V.values()))
print(Counter((v[0], v[5]) for v in V.values()))
print(sorted(set(dl(r["source"]) for r in d.values())))
