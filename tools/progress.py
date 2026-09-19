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

def check_inputs():
    """Refuse to write a degraded README. If the shard or ServUO tree is not where
    this expects, the content section and the counted-from-the-trees line silently
    become empty and the commit looks like real progress data. That is the same
    failure mode as the patch runner that exited 0 on a failed patch, so this
    aborts instead. Use SL_SHARD / SL_SERVUO to point it at another checkout."""
    missing = []
    if not (SHARD / "server" / "customizations").is_dir():
        missing.append(f"shard customizations at {SHARD}  (set SL_SHARD)")
    if not (SERVUO / "Scripts").is_dir():
        missing.append(f"ServUO scripts at {SERVUO}  (set SL_SERVUO)")
    if missing:
        print("  refusing to write: cannot see " + "; ".join(missing), file=sys.stderr)
        print("  (--dry-run prints what it can without writing)", file=sys.stderr)
        sys.exit(2)

def load():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  cannot read progress-state.json: {e}", file=sys.stderr)
        sys.exit(1)

def _emit(text):
    """Print to a console that may be cp1252. The block characters used by bar()
    are correct in the files we write; only the console needs a fallback. A
    progress tool that crashes on its own progress bar is worse than an ugly bar."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.replace("\u2588", "#").replace("\u2591", "."))

def bar(done, total, w=22):
    """Block bar. A nonzero value always shows at least one block, so "barely
    started" never renders identically to "not started"."""
    if total <= 0: return "\u2591" * w
    f = round(w * done / total)
    if done > 0 and f == 0: f = 1
    if done < total and f == w: f = w - 1
    return "\u2588" * f + "\u2591" * (w - f)

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
    cust = {p.stem.lower() for p in (SHARD/"server"/"customizations").rglob("*.cs")} \
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
    out["customization_files"] = len(list(c.rglob("*.cs"))) if c.is_dir() else None
    out["patch_files"] = (len(list(p.glob("*.patch"))) + len(list(p.glob("*.cs")))) if p.is_dir() else None
    out["stale_migrations_present"] = (c / "migrations").is_dir() if c.is_dir() else None
    t = shard / "server" / "tests"
    if t.is_dir():
        files = list(t.rglob("*.cs"))
        out["test_files"] = len(files)
        out["test_cases"] = sum(f.read_text(encoding="utf-8", errors="replace").count("[Fact]")
                                for f in files)
    else:
        out["test_files"] = out["test_cases"] = None
    return out

def build():
    st = load(); cnt = counted(SHARD)
    d = st["setup_defects"]
    done, total = sum(1 for v in d.values() if v), len(d)

    L = []
    L.append("**Direction: staying on ModernUO.** ServUO content is pulled in piece by piece.")
    L.append("")

    # Overall headline. This used to say a single percentage was impossible by design,
    # which was true when written: ported content had no denominator. S3 and S9 built one
    # by filtering ServUO against what ModernUO already ships, so the number exists now.
    # It is still SOFT and the caveat travels with it - see below.
    cp = content_progress()
    if cp:
        ctot = sum(r["done"] for r in cp)
        call = sum(r["total"] for r in cp)
        pct = (100.0 * ctot / call) if call else 0.0
        L.append(f"## Overall: {pct:.0f}% of candidate content ported")
        L.append("")
        L.append("```")
        L.append(f"Content   {bar(ctot, call)}  {ctot}/{call}   {pct:.1f}%")
        L.append(f"Setup     {bar(done, total)}  {done}/{total}     blocking defects resolved")
        L.append("```")
        L.append("")
        L.append("**Read that denominator with suspicion.** 'Candidate files' is ServUO's tree "
                 "filtered against the names ModernUO already declares, and **every count on this "
                 "project has moved when someone actually read the files**: CC9's row went 455 -> "
                 "437, its buckets moved twice more, CC4 Despise was '4 files' and was 14, and the "
                 "brief's 120/29 were 107/30. The percentage is a useful direction of travel and a "
                 "poor promise. Setup health is the only figure here with a denominator that cannot "
                 "move.")
        L.append("")
    else:
        # No content denominator available; fall back to the setup bar alone.
        L.append("```")
        L.append(f"Setup health   {bar(done,total)}  {done}/{total}   blocking defects resolved")
        L.append("```")
        L.append("")
    pg = st.get("playable_gates")
    if pg:
        gates = pg.get("gates", [])
        met = sum(1 for g in gates if g.get("done"))
        blockers = [g for g in gates if not g.get("done")]
        if blockers:
            L.append(f"### Playable? **Not yet: {met} of {len(gates)} gates met.** "
                     f"The next one to fall is *{blockers[0]['name']}*.")
        else:
            L.append(f"### Playable? **Yes, all {len(gates)} gates met.**")
        L.append("")
        L.append(pg.get("note", ""))
        L.append("")
        L.append("| | Gate | Where it stands |")
        L.append("|---|---|---|")
        for g in gates:
            mark = "**yes**" if g.get("done") else "no"
            L.append(f"| {mark} | {g['name']} | {g.get('detail','')} |")
        L.append("")

    L.append("| Setup defect | Resolved |")
    L.append("|---|---|")
    for k, v in d.items():
        L.append(f"| {k} | {'yes' if v else '**no**'} |")
    L.append("")

    p = st["patches"]
    gated = d.get("apply-patches.sh fails on failed patch", False)
    L.append(f"**Patches:** {p['total']} total, **{p['failing']} currently failing to apply**, "
             f"{p['triaged']} triaged, {p['obsolete']} found obsolete. "
             + ("`apply-patches.sh` fails the build on a failed patch, so a green build means "
                "every patch applied."
                if gated else
                "`apply-patches.sh` still exits 0 on failure, so a green build proves nothing."))
    L.append("")

    cp = content_progress()
    if cp:
        tot_d = sum(r["done"] for r in cp); tot_t = sum(r["total"] for r in cp)
        L.append(f"### Content moved over: {tot_d:,} of {tot_t:,} candidate files "
                 f"({100*tot_d/tot_t if tot_t else 0:.1f}%)")
        L.append("")
        L.append("```")
        L.append(f"{'TOTAL':<31}{bar(tot_d,tot_t,18)} {tot_d:>4}/{tot_t:<5}"
                 f"{100*tot_d/tot_t if tot_t else 0:>6.1f}%")
        L.append("")
        for r in cp:
            L.append(f"{r['area'][:30]:<31}{bar(r['done'],r['total'],18)} {r['done']:>4}/{r['total']:<5}{r['pct']:>6.1f}%")
        L.append("```")
        L.append("")
        L.append("_Counted by matching ServUO file stems (excluding those stock ModernUO already has) "
                 "against `server/customizations`. Auto-counted, never hand-edited._")
        L.append("")

    # De-duplicate by name. Two agents logging the same port in one day already
    # happened once; the first entry wins and the duplicate is dropped silently.
    pc, _seen = [], set()
    for _e in st["ported_content"]:
        _n = _e.get("name")
        if _n in _seen: continue
        _seen.add(_n); pc.append(_e)
    if len(pc) != len(st["ported_content"]):
        print(f"  note: dropped {len(st['ported_content'])-len(pc)} duplicate ported_content "
              "entries; fix tools/progress-state.json", file=sys.stderr)
    L.append(f"**Ported systems logged: {len(pc)}**")
    if pc:
        L.append("")
        L.append("| Content | Task | Notes |")
        L.append("|---|---|---|")
        for i in pc:
            L.append(f"| {i.get('name','?')} | {i.get('task','-')} | {i.get('note', i.get('notes',''))} |")
    else:
        L.append("")
        L.append("_None yet. Blocked until the setup defects above are resolved._")
    L.append("")

    tk = st.get("tasks", [])
    if tk:
        SYM = {"done":"x", "in-progress":"~", "blocked":"!", "todo":" "}
        nd = sum(1 for t in tk if t["status"]=="done")
        L.append(f"### Task list ({nd} of {len(tk)} done)")
        L.append("")
        L.append("```")
        L.append(f"Tasks          {bar(nd,len(tk))}  {nd}/{len(tk)}   "
                 "Foundation and the port pipeline")
        L.append("```")
        L.append("")
        L.append("| | Task | Status | Notes |")
        L.append("|---|---|---|---|")
        for t in tk:
            mark = {"done":"done","in-progress":"**in progress**","blocked":"**blocked**","todo":"todo"}[t["status"]]
            L.append(f"| `{t['id']}` | {t['title']} | {mark} | {t.get('note','')} |")
        L.append("")
        L.append("_Detail and acceptance criteria in `docs/tasks.md`. Status lives in "
                 "`tools/progress-state.json`._")
        L.append("")

    up = st.get("upstream_patches") or {}
    if up:
        ps = up.get("patches", []); rp = up.get("replacements", [])
        hi = sum(1 for x in ps if x.get("risk") == "high")
        L.append(f"### Needs reconciling on a `MODERNUO_COMMIT` bump: {len(ps)} patches, {len(rp)} replacements")
        L.append("")
        L.append(up.get("note", ""))
        L.append("")
        L.append("| Upstream file | Patch | Diff | Risk | Breaks when |")
        L.append("|---|---|---|---|---|")
        order = {"high": 0, "medium": 1, "low": 2}
        for x in sorted(ps, key=lambda v: order.get(v.get("risk"), 3)):
            L.append(f"| `{x['file']}` | {x['patch']} | {x['d']} | **{x['risk']}** | {x['breaks']} |")
        L.append("")
        L.append(f"**{len(rp)} full-file replacements fail silently on a bump** and must be diffed by hand: "
                 + ", ".join(f"`{x['file']}`" for x in rp) + ".")
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
             (f"{cnt['test_cases']} tests in {cnt['test_files']} files"
              if cnt.get('test_cases') else None),
             "stale migrations subfolder still present" if cnt['stale_migrations_present'] else None]
    L.append("Counted from the trees: " + ", ".join(f for f in facts if f) + ".")
    L.append(f"Shard status: {st.get('shard_status','unknown')}.")

    snap = {"generated": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds"),
            "direction": "stay on ModernUO; pull ServUO content selectively",
            "setup_defects": d, "setup_done": done, "setup_total": total,
            "patches": p, "ported_content": pc, "declined_content": dc,
            "upstream_patches": st.get("upstream_patches"), "counted": cnt, "content_progress": content_progress(), "tasks": st.get("tasks", []),
            "playable_gates": st.get("playable_gates"),
            "shard_status": st.get("shard_status")}
    try:
        (MIGRATE / "tools" / "progress.json").write_text(json.dumps(snap, indent=2) + "\n", encoding="utf-8", newline="\n")
    except Exception as e:
        print(f"  warning: progress.json not written ({e})", file=sys.stderr)
    return "\n".join(L)

START, END = "<!-- PROGRESS:START -->", "<!-- PROGRESS:END -->"

def main():
    if "--dry-run" not in sys.argv: check_inputs()
    rep = build(); _emit(rep)
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
