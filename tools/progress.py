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

    pc = st["ported_content"]
    L.append(f"**ServUO content pulled in: {len(pc)}**")
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
            "counted": cnt, "shard_status": st.get("shard_status")}
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

if __name__ == "__main__":
    main()
