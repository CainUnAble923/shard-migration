#!/usr/bin/env python3
"""
Expansion progression: how much of each UO expansion's content ServUO has, how much
ModernUO already ships, and how much our shard has picked up.

    python tools/expansion_coverage.py

METHOD AND ITS LIMITS. Files are classified by, in priority order: directory
(Services/Expansions/...), an explicit runtime gate (Core.HS, Expansion.TOL, ...), then
landmark keywords (Ter Mur, Eodon, Galleon, Tokuno...). Coverage is measured by FILENAME
STEM match, which is a proxy: a matching name means a file of that name exists, not that
behaviour matches. Treat these as directional, not precise. Unclassified files fall to
Pre-AoS, which inflates that bucket.

Paths: SL_SERVUO, SL_SHARD, SL_MIGRATE
"""
import os, re, sys, json
from pathlib import Path
from collections import defaultdict

SERVUO  = Path(os.environ.get("SL_SERVUO", r"D:\UO\ServUO-pub57"))
SHARD   = Path(os.environ.get("SL_SHARD",  r"D:\ShatteredLegacy"))
MIGRATE = Path(os.environ.get("SL_MIGRATE", Path(__file__).resolve().parent.parent))

ORDER = ["Pre-AoS","AOS","SE","ML","SA","HS","TOL","EJ"]
LABEL = {"Pre-AoS":"Pre-AoS (T2A/UOR/LBR)","AOS":"Age of Shadows","SE":"Samurai Empire",
         "ML":"Mondain's Legacy","SA":"Stygian Abyss (Ter Mur)","HS":"High Seas",
         "TOL":"Time of Legends (Eodon)","EJ":"Endless Journey"}
GATE = {g: re.compile(r"\bCore\." + g + r"\b|\bExpansion\." + g + r"\b") for g in ["AOS","SE","ML","SA","HS","TOL","EJ"]}
DIRS = [("Services/Expansions/High Seas","HS"), ("Services/Expansions/Time Of Legends","TOL")]
KEY = {k: re.compile(v, re.I) for k, v in {
 "AOS": r"\bMalas\b|\bLuna\b|\bUmbra\b|Necromanc|Chivalry|\bDoom\b|Gauntlet|Paladin",
 "SE":  r"\bTokuno\b|Ninjitsu|Bushido|\bZento\b|Samurai|Homare|Isamu|Makoto",
 "ML":  r"Heartwood|Blighted Grove|Painted Cave|Twisted Weald|\bBedlam\b|Labyrinth|Prism of Light|Sanctuary|\bElf\b|Mondain",
 "SA":  r"Ter ?Mur|Gargoyle|Stygian|Underworld|Royal City|Holy City|Imbuing|Mysticism|Throwing|Abyss",
 "HS":  r"Galleon|Cannon|Charybdis|Corgul|Scalis|Bounty|Fishmonger|Dockmaster|Ship",
 "TOL": r"\bEodon\b|Myrmidex|Shadowguard|Barrab|Jukari|Kurak|Sakkhra|Urali|Zipactriotl",
 "EJ":  r"Endless Journey|Blackthorn.?s? Dungeon|Khaldun",
}.items()}

def classify(rel, src):
    r = str(rel).replace("\\", "/")
    for d, e in DIRS:
        if r.startswith(d): return e
    for e in ["EJ","TOL","HS","SA","ML","SE","AOS"]:
        if GATE[e].search(src): return e
    for e in ["TOL","HS","SA","ML","SE","AOS"]:
        if KEY[e].search(src): return e
    return "Pre-AoS"

def bar(d, t, w=20):
    if t <= 0: return "-"*w
    f = round(w*d/t)
    return "#"*f + "."*(w-f)

def main():
    root = SERVUO / "Scripts"
    stems_file = MIGRATE / "tools" / "modernuo-stems.txt"
    if not root.is_dir():
        print("ServUO not found at " + str(root), file=sys.stderr); return 1
    if not stems_file.exists():
        print("missing " + str(stems_file), file=sys.stderr); return 1
    stock = {l.strip().lower() for l in stems_file.read_text(encoding="utf-8").splitlines() if l.strip()}
    cdir = SHARD/"server"/"customizations"
    cust  = {p.stem.lower() for p in cdir.rglob("*.cs")} if cdir.is_dir() else set()

    b = defaultdict(lambda: {"tot":0, "stock":0, "ours":0})
    for p in root.rglob("*.cs"):
        try: s = p.read_text(errors="replace")
        except OSError: continue
        e = classify(p.relative_to(root), s); st = p.stem.lower()
        b[e]["tot"] += 1
        if st in stock: b[e]["stock"] += 1
        elif st in cust: b[e]["ours"] += 1

    rows = []
    print("%-26s%-22s%7s%7s%6s   (ours)" % ("expansion","progress","have","of","%"))
    print("-"*76)
    for e in ORDER:
        v = b[e]
        if not v["tot"]: continue
        have = v["stock"] + v["ours"]; pct = 100*have/v["tot"]
        print("%-26s%s  %5d%7d%5.0f%%   +%d" % (LABEL[e], bar(have,v["tot"]), have, v["tot"], pct, v["ours"]))
        rows.append({"expansion":e,"label":LABEL[e],"servuo_files":v["tot"],
                     "modernuo_stock":v["stock"],"ported_by_us":v["ours"],
                     "have":have,"pct":round(pct,1)})
    t = sum(r["servuo_files"] for r in rows); h = sum(r["have"] for r in rows)
    o = sum(r["ported_by_us"] for r in rows)
    print("-"*76)
    print("%-26s%s  %5d%7d%5.0f%%   +%d" % ("TOTAL", bar(h,t), h, t, 100*h/t, o))
    print("\nCoverage is filename-stem matching: a proxy for presence, not behaviour.")
    print("Unclassified files fall to Pre-AoS, inflating that bucket. Directional only.")
    (MIGRATE/"tools"/"expansion-coverage.json").write_text(
        json.dumps({"rows":rows,"total_files":t,"total_have":h,"ported_by_us":o}, indent=2)+"\n",
        encoding="utf-8", newline="\n")

    if "--dry-run" not in sys.argv:
        write_readme(rows, t, h, o)
    return 0

START, END = "<!-- EXPANSION:START -->", "<!-- EXPANSION:END -->"

def write_readme(rows, t, h, o):
    L = ["### Content by expansion", ""]
    L.append(f"**{h:,} of {t:,} ServUO files present** ({100*h/t:.0f}%), of which **{o:,} ported by us**.")
    L.append("")
    L.append("```")
    for r in rows:
        L.append("%-26s%s %5d/%-6d%4.0f%%%s" % (
            r["label"], bar(r["have"], r["servuo_files"]), r["have"], r["servuo_files"],
            r["pct"], f"   +{r['ported_by_us']}" if r["ported_by_us"] else ""))
    L.append("%-26s%s %5d/%-6d%4.0f%%   +%d" % ("TOTAL", bar(h,t), h, t, 100*h/t, o))
    L.append("```")
    L.append("")
    L.append("_Filename-stem matching: a proxy for presence, not behaviour. Unclassified files "
             "fall into Pre-AoS, inflating it. Directional, not a completion percentage._")
    block = START + "\n" + "\n".join(L) + "\n" + END
    rm = MIGRATE / "README.md"
    if not rm.exists(): return
    txt = rm.read_text(encoding="utf-8")
    if START in txt and END in txt:
        txt = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, txt, flags=re.S)
    else:
        txt = txt.rstrip() + "\n\n## Expansion coverage\n\n" + block + "\n"
    rm.write_text(txt, encoding="utf-8", newline="\n")
    print("\n  README.md expansion block updated.")

if __name__ == "__main__":
    sys.exit(main())
