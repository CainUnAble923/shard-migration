#!/usr/bin/env python3
"""
Progress reporter.

Direction: the shard STAYS on ModernUO; ServUO content is pulled in selectively.
There is no fixed total to reach, so this deliberately does not report a single
completion percentage. Setup health has a denominator. Ported content does not.

    python tools/progress.py             # print, rewrite README block, write progress.json
    python tools/progress.py --dry-run   # print only

Path overrides: SL_SHARD, SL_MIGRATE
"""
import json, os, re, sys
from pathlib import Path

SHARD   = Path(os.environ.get("SL_SHARD", r"D:\ShatteredLegacy"))
SERVUO  = Path(os.environ.get("SL_SERVUO", r"D:\UO\ServUO-pub57"))
MIGRATE = Path(os.environ.get("SL_MIGRATE", Path(__file__).resolve().parent.parent))
STATE   = MIGRATE / "tools" / "progress-state.json"

def load():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  cannot read progress-state.json: {e}", file=sys.stderr)
        sys.exit(1)

def bar(done, total, w=22):
    if total <= 0: return "-" * w
    f = round(w * done / total)
    return "#" * f + "." * (w - f)

AREAS = ["Items/Artifacts","Services/Revamped Dungeons","Mobiles/NPCs","Items/Addons",
         "Items/Equipment","Mobiles/Normal","Services/XmlSpawner","Items/Decorative",
         "Items/Quest","Items/Resource","Items/Consumables","Services/CleanUpBritannia",
         "Items/StoreBought","Items/Functional","Services/New Magincia","Quests",
         "Items/Containers","Services/BulkOrders","Services/Expansions"]

def content_progress():
    """Per-area: how many ServUO files (absent from stock ModernUO) now exist in ours."""
    stems_file = MIGRATE / "tools" / "modernuo-stems.txt"
    if not (SERVUO / "Scripts").is_dir() or not stems_file.exists():
        return None
    stock = {l.strip().lower() for l in stems_file.read_text(encoding="utf-8").splitlines() if l.strip()}
    cust = {p.stem.lower() for p in (SHARD/"server"/"customizations").glob("*.cs")} \
           if (SHARD/"server"/"customizations").is_dir() else set()
    out = []
    for area in AREAS:
        root = SERVUO / "Scripts" / area
        if not root.is_dir(): continue
        cand = {p.stem.lower() for p in root.rglob("*.cs")} - stock   # not already in ModernUO
        if not cand: continue
        done = cand & cust
        out.append({"area": area, "total": len(cand), "done": len(done),
                    "pct": round(100*len(done)/len(cand),1)})
    out.sort(key=lambda r: (-r["done"], -r["total"]))
    return out

def counted(shard):
    """Facts counted from the trees, never hand-edited."""
    out = {}
    c = shard / "server" / "customizations"
    p = shard / "server" / "patches"
    out["customization_files"] = len(list(c.glob("*.cs"))) if c.is_dir() else None
    out["patch_files"] = (len(list(p.glob("*.patch"))) + len(list(p.glob("*.cs")))) if p.is_dir() else None
    out["stale_migrations_present"] = (c / "migrations").is_dir() if c.is_dir() else None
    return out

def build():
    st = load(); cnt = counted(SHARD)
    d = st["setup_defects"]
    done, total = sum(1 for v in d.values() if v), len(d)

    L = []
    L.append("**Direction: staying on ModernUO.** ServUO content is pulled in piece by piece. "
             "There is no total to reach, so there is no single completion percentage here by design.")
    L.append("")
    L.append("```")
    L.append(f"Setup health   {bar(done,total)}  {done}/{total}   blocking defects resolved")
    L.append("```")
    L.append("")
    L.append("| Setup defect | Resolved |")
    L.append("|---|---|")
    for k, v in d.items():
        L.append(f"| {k} | {'yes' if v else '**no**'} |")
    L.append("")

    p = st["patches"]
    L.append(f"**Patches:** {p['total']} total, **{p['failing']} currently failing to apply**, "
             f"{p['triaged']} triaged, {p['obsolete']} found obsolete. "
             f"`apply-patches.sh` still exits 0 on failure, so a green build proves nothing.")
    L.append("")

    cp = content_progress()
    if cp:
        tot_d = sum(r["done"] for r in cp); tot_t = sum(r["total"] for r in cp)
        L.append(f"### Content moved over: {tot_d:,} of {tot_t:,} candidate files "
                 f"({100*tot_d/tot_t if tot_t else 0:.1f}%)")
        L.append("")
        L.append("```")
        for r in cp:
            L.append(f"{r['area'][:30]:<31}{bar(r['done'],r['total'],18)} {r['done']:>4}/{r['total']:<5}{r['pct']:>6.1f}%")
        L.append("```")
        L.append("")
        L.append("_Counted by matching ServUO file stems (excluding those stock ModernUO already has) "
                 "against `server/customizations`. Auto-counted, never hand-edited._")
        L.append("")

    pc = st["ported_content"]
    L.append(f"**Ported systems logged: {len(pc)}**")
    if pc:
        L.append("")
        L.append("| Content | Ported | Notes |")
        L.append("|---|---|---|")
        for i in pc:
            L.append(f"| {i.get('name','?')} | {i.get('date','-')} | {i.get('notes','')} |")
    else:
        L.append("")
        L.append("_None yet. Blocked until the setup defects above are resolved._")
    L.append("")

    dc = st.get("declined_content", [])
    if dc:
        L.append("**Deliberately declined:**")
        L.append("")
        for i in dc:
            L.append(f"- **{i['name']}** — {i['reason']}")
        L.append("")

    facts = [f"{cnt['customization_files']} customization files" if cnt['customization_files'] is not None else None,
             f"{cnt['patch_files']} patch files" if cnt['patch_files'] is not None else None,
             "stale migrations subfolder still present" if cnt['stale_migrations_present'] else None]
    L.append("Counted from the trees: " + ", ".join(f for f in facts if f) + ".")
    L.append(f"Shard status: {st.get('shard_status','unknown')}.")

    snap = {"generated": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds"),
            "direction": "stay on ModernUO; pull ServUO content selectively",
            "setup_defects": d, "setup_done": done, "setup_total": total,
            "patches": p, "ported_content": pc, "declined_content": dc,
            "counted": cnt, "content_progress": content_progress(),
            "shard_status": st.get("shard_status")}
    try:
        (MIGRATE / "tools" / "progress.json").write_text(json.dumps(snap, indent=2) + "\n", encoding="utf-8")
    except Exception as e:
        print(f"  warning: progress.json not written ({e})", file=sys.stderr)
    return "\n".join(L)

START, END = "<!-- PROGRESS:START -->", "<!-- PROGRESS:END -->"

def main():
    rep = build(); print(rep)
    if "--dry-run" in sys.argv: return
    rm = MIGRATE / "README.md"
    if not rm.exists(): return
    t = rm.read_text(encoding="utf-8")
    block = f"{START}\n{rep}\n{END}"
    if START in t and END in t:
        t = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, t, flags=re.S)
    else:
        t = t.rstrip() + "\n\n## Progress\n\n" + block + "\n"
    rm.write_text(t, encoding="utf-8", newline="\n")
    print("\n  README.md updated.")
    # keep the expansion block in step: one command does both
    try:
        import subprocess
        r = subprocess.run([sys.executable, str(MIGRATE/"tools"/"expansion_coverage.py")],
                           capture_output=True, text=True, timeout=600)
        if r.returncode == 0:
            print("  expansion coverage refreshed.")
        else:
            print(f"  expansion coverage skipped: {(r.stderr or '').strip()[:120]}")
    except Exception as e:
        print(f"  expansion coverage skipped: {e}")
    try:
        import subprocess
        r = subprocess.run([sys.executable, str(MIGRATE/"tools"/"render_dashboard.py")],
                           capture_output=True, text=True, timeout=300)
        print((r.stdout or r.stderr or "").rstrip() or "  dashboard step produced no output")
    except Exception as e:
        print(f"  dashboard skipped: {e}")

if __name__ == "__main__":
    main()
