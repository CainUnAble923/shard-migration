#!/usr/bin/env python3
"""
Migration progress reporter.

Counts real state from the working trees and rewrites the progress block in README.md
between the PROGRESS markers. Judgment items that cannot be counted live in
tools/progress-state.json.

Usage:
    python tools/progress.py            # print report and update README.md
    python tools/progress.py --dry-run  # print only

Paths default to the Windows layout and can be overridden with env vars:
    SL_SHARD    D:\\ShatteredLegacy
    SL_WORK     D:\\UO\\ServUO-work
    SL_MIGRATE  D:\\UO\\shard-migration
"""
import json, os, re, sys
from pathlib import Path

def env(name, default):
    return Path(os.environ.get(name, default))

SHARD   = env("SL_SHARD",   r"D:\ShatteredLegacy")
WORK    = env("SL_WORK",    r"D:\UO\ServUO-work")
MIGRATE = env("SL_MIGRATE", Path(__file__).resolve().parent.parent)

# Files in server/customizations that replace upstream sources rather than add to them.
REPLACEMENTS = {"CharacterCreation", "CraftItem", "HammerOfHephaestus", "Meditation", "RegenRates"}

STATE_PATH = Path(MIGRATE) / "tools" / "progress-state.json"
DEFAULT_STATE = {
    "baseline_gaps": {
        "CraftContext members (RepeatCount, RepeatItem, RepeatTypeRes)": False,
        "ResourceInfo extended wood enum members (8)": False,
        "OutridersGuildmaster": False,
    },
    "phases": {
        "0 Freeze and inventory": "in-progress",
        "1 Stock ServUO reference": "done",
        "2 Rewrite custom scripts": "in-progress",
        "3 Move accounts and spawners": "not-started",
        "4 Spawns and maps": "not-started",
        "5 Runtime and hosting": "not-started",
        "6 Verify and cut over": "not-started",
    },
    "patches_triaged": 0,
    "patches_obsolete": 0,
    "notes": "Edit this file for items that cannot be counted from the trees.",
}

def load_state():
    if STATE_PATH.exists():
        try:
            s = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            for k, v in DEFAULT_STATE.items():
                s.setdefault(k, v)
            return s
        except Exception as e:
            print(f"  warning: could not read {STATE_PATH.name} ({e}); using defaults", file=sys.stderr)
    return dict(DEFAULT_STATE)

def bar(done, total, width=22):
    if total <= 0:
        return "─" * width
    filled = round(width * done / total)
    return "█" * filled + "░" * (width - filled)

def pct(done, total):
    return 0.0 if total <= 0 else 100.0 * done / total

def count_customizations():
    d = SHARD / "server" / "customizations"
    if not d.is_dir():
        return None
    files = [p for p in d.glob("*.cs")]
    additive = [p for p in files if p.stem not in REPLACEMENTS]
    repl = [p for p in files if p.stem in REPLACEMENTS]
    return {"total": len(files), "additive": len(additive), "replacements": len(repl)}

def count_ported():
    d = WORK / "Scripts" / "Custom" / "ShatteredLegacy"
    if not d.is_dir():
        return 0
    return len(list(d.rglob("*.cs")))

def count_patches():
    d = SHARD / "server" / "patches"
    if not d.is_dir():
        return None
    return {"patch": len(list(d.glob("*.patch"))), "replacement_cs": len(list(d.glob("*.cs")))}

def build_report():
    st = load_state()
    cust = count_customizations()
    patches = count_patches()
    ported = count_ported()

    rows = []
    warnings = []

    gaps = st["baseline_gaps"]
    g_done = sum(1 for v in gaps.values() if v)
    rows.append(("Baseline recovery", g_done, len(gaps), "canonical tree compiles"))

    if cust:
        rows.append(("Content ports", min(ported, cust["total"]), cust["total"],
                     f"{cust['additive']} additive + {cust['replacements']} replacements"))
    else:
        warnings.append(f"customizations not found at {SHARD / 'server' / 'customizations'}")
        rows.append(("Content ports", ported, 0, "source tree not found"))

    if patches:
        p_total = patches["patch"] + patches["replacement_cs"]
        p_done = min(st["patches_triaged"], p_total)
        rows.append(("Patch triage", p_done, p_total,
                     f"{patches['patch']} .patch + {patches['replacement_cs']} replacements, "
                     f"{st['patches_obsolete']} found obsolete"))
    else:
        warnings.append(f"patches not found at {SHARD / 'server' / 'patches'}")

    ph = st["phases"]
    ph_done = sum(1 for v in ph.values() if v == "done")
    rows.append(("Phase gates", ph_done, len(ph), "of 7 phases complete"))

    width = max(len(r[0]) for r in rows)
    lines = ["```", ]
    for name, done, total, note in rows:
        lines.append(f"{name:<{width}}  {bar(done,total)}  {done:>3}/{total:<3} {pct(done,total):5.1f}%   {note}")
    lines.append("```")
    lines.append("")

    lines.append("| Phase | Status |")
    lines.append("|---|---|")
    sym = {"done": "done", "in-progress": "in progress", "not-started": "not started", "blocked": "**blocked**"}
    for k, v in ph.items():
        lines.append(f"| {k} | {sym.get(v, v)} |")
    lines.append("")

    open_gaps = [k for k, v in gaps.items() if not v]
    if open_gaps:
        lines.append("**Blocking Phase 2:** canonical tree does not compile. Missing:")
        for g in open_gaps:
            lines.append(f"- {g}")
        lines.append("")

    overall_done = sum(r[1] for r in rows)
    overall_total = sum(r[2] for r in rows)
    lines.insert(0, f"**Overall: {pct(overall_done, overall_total):.0f}%** "
                    f"({overall_done}/{overall_total} tracked items). "
                    f"Counted from the working trees, not hand-maintained.")
    lines.insert(1, "")

    for w in warnings:
        lines.append(f"> Path warning: {w}")
    return "\n".join(lines)

START, END = "<!-- PROGRESS:START -->", "<!-- PROGRESS:END -->"

def main():
    report = build_report()
    print(report)
    if "--dry-run" in sys.argv:
        return
    readme = Path(MIGRATE) / "README.md"
    if not readme.exists():
        print(f"\n  README.md not found at {readme}", file=sys.stderr); return
    text = readme.read_text(encoding="utf-8")
    block = f"{START}\n{report}\n{END}"
    if START in text and END in text:
        text = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n## Migration progress\n\n" + block + "\n"
    readme.write_text(text, encoding="utf-8", newline="\n")
    print(f"\n  README.md updated.")

if __name__ == "__main__":
    main()
