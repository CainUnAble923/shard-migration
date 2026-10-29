"""cc-P686: a mutant regions-felucca.json for fact 5's red run: Britain's guard zone gets one more rect, over the first
champion altar in notes/cc-P685-tools/out/champs.csv. Usage: python -I mutate_champ.py <regions-felucca.json> <out>"""
import csv, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
row = next(csv.DictReader(open(os.path.join(here, "..", "cc-P685-tools", "out", "champs.csv"))))
x, y = int(row["x"]), int(row["y"])
f = json.load(open(sys.argv[1], encoding="utf-8"))
next(r for r in f if r.get("Name") == "Britain")["Area"].append({"x1": x - 2, "y1": y - 2, "x2": x + 2, "y2": y + 2})
open(sys.argv[2], "w", encoding="ascii").write(json.dumps(f))
print("wrote", sys.argv[2], "with a guard rect over", row["id"], x, y)
