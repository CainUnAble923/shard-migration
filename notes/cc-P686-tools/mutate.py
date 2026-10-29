"""cc-P686: a mutant regions-felucca.json for a red run: Buccaneer's Den with its guards on, and Britain's first rect one
tile off Trammel's. Usage: python -I mutate.py <regions-felucca.json> <out>"""
import json, sys
f = json.load(open(sys.argv[1], encoding="utf-8"))
for r in f:
    if r.get("Name") == "Buccaneer's Den":
        r.pop("GuardsDisabled")
    if r.get("Name") == "Britain":
        r["Area"][0]["x2"] += 1
open(sys.argv[2], "w", encoding="ascii").write(json.dumps(f))
print("wrote", sys.argv[2])
