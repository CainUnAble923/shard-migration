#!/usr/bin/env python3
"""
Port triage: classify each file in server/customizations by how hard it will be to
port from ModernUO to ServUO. Read-only. Emits JSON + a markdown table.

Signals are counted from source, not guessed. Difficulty is derived from those counts
by an explicit rule, so the ranking is reproducible and arguable.
"""
import json, os, re, sys
from pathlib import Path

SHARD = Path(os.environ.get("SL_SHARD", r"D:\ShatteredLegacy"))
SERVUO = Path(os.environ.get("SL_SERVUO", r"D:\UO\ServUO-pub57"))
OUT    = Path(os.environ.get("SL_MIGRATE", Path(__file__).resolve().parent.parent))

CUST = SHARD / "server" / "customizations"
REPLACEMENTS = {"CharacterCreation","CraftItem","HammerOfHephaestus","Meditation","RegenRates"}

# ModernUO-only constructs. Each needs a hand rewrite in ServUO.
PATTERNS = {
    "sergen":      r"\[SerializationGenerator\(",
    "serfield":    r"\[SerializableField\(",
    "sercmdprop":  r"\[SerializedCommandProperty\(",
    "igeneric":    r"\bIGeneric(?:Reader|Writer)\b",
    "serial_math": r"\bSerial\s*[-+]|\.Serial\s*[-+]|Serial\s*==\s*-1|Serial\s*!=\s*-1",
    "packets":     r"\bPacket(?:Writer|Reader)?\b|\bNetState\b\.\w*Send|\bOutgoingPackets\b",
    "lambdatimer": r"Timer\.(?:StartTimer|DelayCall)\s*\(",
    "pooled":      r"\bPooledRef(?:Queue|List)\b",
    "valuesb":     r"\bValueStringBuilder\b|\bSpanFormattable\b",
    "textdef":     r"\bTextDefinition\b",
    "gump":        r":\s*Gump\b|\bnew\s+\w*Gump\s*\(",
    "linq":        r"^using System\.Linq",
    "async":       r"\basync\s+(?:Task|ValueTask)\b",
}

def servuo_index():
    idx = {}
    root = SERVUO / "Scripts"
    if not root.is_dir():
        return idx
    for p in root.rglob("*.cs"):
        idx.setdefault(p.stem, []).append(str(p.relative_to(SERVUO)))
    return idx

def analyse(path, sidx):
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return None
    lines = src.count("\n") + 1
    counts = {k: len(re.findall(v, src, re.M)) for k, v in PATTERNS.items()}
    types = re.findall(r"\b(?:public|internal)\s+(?:sealed\s+|abstract\s+|static\s+|partial\s+)*"
                       r"(class|struct|enum|interface)\s+(\w+)", src)
    bases = re.findall(r"\bclass\s+\w+\s*:\s*([\w<>, ]+)", src)
    base = bases[0].split(",")[0].strip() if bases else ""

    # score
    s = 0
    s += counts["sergen"] * 3 + counts["serfield"] * 1 + counts["sercmdprop"]
    s += counts["igeneric"] * 2
    s += counts["serial_math"] * 5
    s += counts["packets"] * 6
    s += counts["pooled"] * 4 + counts["valuesb"] * 4
    s += counts["lambdatimer"] * 2
    s += counts["async"] * 5
    s += lines // 250
    if path.stem in REPLACEMENTS:
        s += 12

    if   s >= 25: band = "needs-judgment"
    elif s >= 8:  band = "mechanical"
    else:         band = "trivial"

    collision = sidx.get(path.stem, [])
    return {
        "file": path.name, "lines": lines, "score": s, "band": band,
        "base": base, "types": [t[1] for t in types][:4],
        "replacement": path.stem in REPLACEMENTS,
        "servuo_same_name": collision[:2],
        "signals": {k: v for k, v in counts.items() if v},
    }

def main():
    if not CUST.is_dir():
        print(f"customizations not found at {CUST}", file=sys.stderr); return 1
    sidx = servuo_index()
    rows = [r for r in (analyse(p, sidx) for p in sorted(CUST.glob("*.cs"))) if r]
    rows.sort(key=lambda r: (-r["score"], r["file"]))

    tally = {}
    for r in rows: tally[r["band"]] = tally.get(r["band"], 0) + 1
    total_lines = sum(r["lines"] for r in rows)

    (OUT / "tools" / "obsolete" / "port-triage.json").write_text(
        json.dumps({"files": rows, "tally": tally, "total_lines": total_lines}, indent=2) + "\n",
        encoding="utf-8")

    print(f"{len(rows)} files, {total_lines:,} lines")
    print("bands:", ", ".join(f"{k} {v}" for k, v in sorted(tally.items())))
    print(f"servuo index: {len(sidx)} type names")
    print()
    print(f"{'file':<42} {'lines':>6} {'score':>5}  {'band':<15} signals")
    for r in rows[:30]:
        sig = " ".join(f"{k}:{v}" for k, v in sorted(r["signals"].items()))[:64]
        print(f"{r['file']:<42} {r['lines']:>6} {r['score']:>5}  {r['band']:<15} {sig}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
