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
# cc-P85: what progress.py now derives instead of a person writing it down. Read only.
AUTOPILOT = Path(os.environ.get("SL_AUTOPILOT", r"D:\UO\cc-autopilot"))
PROMPTS   = Path(os.environ.get("SL_PROMPTS", r"D:\UO\cc-prompts"))
STALE_DAYS = 7   # the judgment turns amber on the page when its newest confirmed date is older than this

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

# --- cc-P92: the ServUO port list ----------------------------------------------------------------------------------
# tools/port-list.json is hand-kept judgment, like progress-state.json: the overseer edits it (moves a system between
# tiers, reorders the Port rows for "next to land"), and this only reads it.
PORT_LIST = MIGRATE / "tools" / "port-list.json"
PORT_ROOTS = ("Services", "Items", "Mobiles")
COUNTED_TIERS = ("port",)          # every other tier is shown, never counted
TIER_ORDER = ("port", "decide", "ride", "reward", "source", "later", "drop")


def port_list(path=None, servuo=None, shard=None, stems=None):
    """Every ServUO file under Scripts/Services, Items and Mobiles that stock ModernUO lacks (its lowercased stem is not
    in modernuo-stems.txt) is a candidate; it is done when the stem exists anywhere under server/customizations, the
    same proxy as content_progress() (filename stems, not behavior). Each candidate goes to the FIRST system in file
    order whose prefix matches its path under Scripts/ (forward slashes) and whose exclude regex, if any, does not.
    Candidates no system claims are reported, count and the first 20 paths, so a new ServUO file shows up rather than
    vanishing. Returns None when the list, the ServUO tree or the stems file is missing."""
    pl = _read_json(path or PORT_LIST)
    root = Path(servuo or SERVUO) / "Scripts"
    stems_file = Path(stems or MIGRATE / "tools" / "modernuo-stems.txt")
    if not pl or not root.is_dir() or not stems_file.exists():
        return None
    stock = {l.strip().lower() for l in stems_file.read_text(encoding="utf-8").splitlines() if l.strip()}
    cdir = Path(shard or SHARD) / "server" / "customizations"
    cust = {p.stem.lower() for p in cdir.rglob("*.cs")} if cdir.is_dir() else set()
    systems = pl.get("systems", [])
    rx = [re.compile(s["exclude"]) if s.get("exclude") else None for s in systems]
    rows = [{"id": s.get("id"), "tier": s.get("tier"), "title": s.get("title"), "feeds": s.get("feeds", ""),
             "why": s.get("why", ""), "candidates": 0, "done": 0} for s in systems]
    unassigned = []
    total = 0
    for top in PORT_ROOTS:
        base = root / top
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.cs")):
            stem = p.stem.lower()
            if stem in stock:
                continue
            total += 1
            rel = p.relative_to(root).as_posix()
            for i, s in enumerate(systems):
                if any(rel.startswith(x) for x in s.get("prefixes", [])) and not (rx[i] and rx[i].search(rel)):
                    rows[i]["candidates"] += 1
                    rows[i]["done"] += stem in cust
                    break
            else:
                unassigned.append(rel)
    for r in rows:
        r["complete"] = r["candidates"] > 0 and r["done"] == r["candidates"]
        r["pct"] = round(100.0 * r["done"] / r["candidates"], 1) if r["candidates"] else 0.0
    counted_rows = [r for r in rows if r["tier"] in COUNTED_TIERS]
    c_done = sum(r["done"] for r in counted_rows)
    c_total = sum(r["candidates"] for r in counted_rows)
    nxt = next((r for r in counted_rows if not r["complete"]), None)
    tiers = {}
    for t in TIER_ORDER + tuple(sorted({r["tier"] for r in rows} - set(TIER_ORDER))):
        rs = [r for r in rows if r["tier"] == t]
        if rs:
            tiers[t] = {"systems": len(rs), "files": sum(r["candidates"] for r in rs), "done": sum(r["done"] for r in rs),
                        "titles": [r["title"] for r in rs], "counted": t in COUNTED_TIERS,
                        "meaning": (pl.get("tiers") or {}).get(t, "")}
    return {"systems": rows, "tiers": tiers, "candidates": total, "unassigned": len(unassigned),
            "unassigned_first": unassigned[:20],
            "counted": {"systems": len(counted_rows), "in": sum(1 for r in counted_rows if r["complete"]),
                        "done": c_done, "total": c_total,
                        "pct": round(100.0 * c_done / c_total, 1) if c_total else 0.0},
            "next": nxt["title"] if nxt else None, "decided": pl.get("decided", [])}


def port_list_headline(pl):
    """"Port list: n of N systems in. done of total files (pct%)." The one sentence the page and README lead with."""
    c = pl["counted"]
    return (f"Port list: {c['in']} of {c['systems']} systems in. {c['done']:,} of {c['total']:,} files "
            f"({c['pct']:.0f}%).")


DIRECTION_LINE = ("A faithful port comes first, our feature customizations after it; work already started or already "
                  "requested is still finished (Chase, 2026-10-13).")


def counted(shard):
    """Facts counted from the trees, never hand-edited."""
    out = {}
    c = shard / "server" / "customizations"
    p = shard / "server" / "patches"
    out["customization_files"] = len(list(c.rglob("*.cs"))) if c.is_dir() else None
    out["patch_files"] = (len(list(p.glob("*.patch"))) + len(list(p.glob("*.cs")))) if p.is_dir() else None
    out["stale_migrations_present"] = (c / "migrations").is_dir() if c.is_dir() else None
    # cc-P38: what a bump must reconcile, counted from the build route rather than the hand-kept table in
    # progress-state.json (which said 17 and 5 while the tree held 36 and 10). A .patch fails loudly on a bump; a
    # replace_file line in apply-patches.sh routes a full-file replacement, which fails silently.
    ap = shard / "docker" / "uo" / "apply-patches.sh"
    out["upstream_patch_files"] = len(list(p.glob("*.patch"))) if p.is_dir() else None
    out["upstream_replacements"] = (sorted(re.findall(r'^replace_file\s+"\$\w+/([^"]+)"',
                                                      ap.read_text(encoding="utf-8"), re.M))
                                    if ap.is_file() else None)
    t = shard / "server" / "tests"
    if t.is_dir():
        files = list(t.rglob("*.cs"))
        out["test_files"] = len(files)
        # Attribute lines only: a bare substring count also counted "[Fact]" inside a comment
        # (AthenaeumIsleQuestVerification.cs:7) and reported one more test than the gate runs.
        out["test_cases"] = sum(len(re.findall(r"^\s*\[(?:Fact|Theory)\b",
                                               f.read_text(encoding="utf-8", errors="replace"), re.M))
                                for f in files)
    else:
        out["test_files"] = out["test_cases"] = None
    return out

# --- cc-P85: derived facts (no person keeps these) -----------------------------------------------------------------

_NOTE_END = re.compile(r"^P(\d+) (DONE|STOPPED)(?::\s*(.*))?$")
_PROMPT = re.compile(r"^cc-P(\d+)-(.+)\.md$")

def _read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None

def _mdate(path):
    from datetime import datetime
    try:
        return datetime.fromtimestamp(Path(path).stat().st_mtime).strftime("%Y-%m-%d")
    except OSError:
        return ""

def finished_prompts(notes_dir):
    """Every notes/cc-Pnn-*.md whose last line is "Pnn DONE" or "Pnn STOPPED: why", newest number first."""
    out = []
    for f in Path(notes_dir).glob("cc-P*.md"):
        m = _PROMPT.match(f.name)
        if not m: continue
        try:
            lines = [l.strip() for l in f.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
        except OSError:
            continue
        e = _NOTE_END.match(lines[-1]) if lines else None
        if not e or e.group(1) != m.group(1): continue
        out.append({"n": int(m.group(1)), "slug": m.group(2), "state": e.group(2).lower(),
                    "why": (e.group(3) or "").strip(), "date": _mdate(f), "notes": "notes/" + f.name})
    out.sort(key=lambda r: -r["n"])
    return out

def queue_state(notes_dir=None, prompts=None, autopilot=None):
    """The CC prompt queue: queued (cc-prompts/queue), running (the autopilot's state.json), and the latest finished
    (each prompt's notes ends DONE or STOPPED). Read only; the autopilot and the overseer own these files."""
    notes_dir = Path(notes_dir or MIGRATE / "notes")
    prompts = Path(prompts or PROMPTS)
    autopilot = Path(autopilot or AUTOPILOT)
    fin = finished_prompts(notes_dir)
    done_n = {r["n"] for r in fin}
    st = _read_json(autopilot / "state.json") or {}
    enabled = (autopilot / "ENABLED").exists()
    running = None
    m = re.match(r"^P(\d+)$", str(st.get("current") or ""))
    if m and int(m.group(1)) not in done_n:
        f = _PROMPT.match(str(st.get("currentFile") or ""))
        running = {"n": int(m.group(1)), "slug": f.group(2) if f else "", "state": "running",
                   "since": str(st.get("startedAt") or "")}
    queued = []
    qdir = prompts / "queue"
    if qdir.is_dir():
        for f in qdir.glob("cc-P*.md"):
            q = _PROMPT.match(f.name)
            if q and int(q.group(1)) not in done_n and not (running and running["n"] == int(q.group(1))):
                queued.append({"n": int(q.group(1)), "slug": q.group(2), "state": "queued"})
    queued.sort(key=lambda r: r["n"])
    return {"autopilot": "on" if enabled else "off", "running": running, "queued": queued,
            "finished": fin[:10], "finished_total": len(fin),
            "stopped_total": sum(1 for r in fin if r["state"] == "stopped"),
            "latest_done": next((r for r in fin if r["state"] == "done"), None)}

def playtest_counts(path=None):
    """Open, failed and passed play tests from testing/play-tests.json (cc-P83), as its own summary counts them."""
    doc = _read_json(path or MIGRATE / "testing" / "play-tests.json")
    if not doc or not isinstance(doc.get("summary"), dict): return None
    s = doc["summary"]
    return {k: s.get(k) for k in ("open", "failed", "passed", "later", "blocked", "total", "unloggedFails", "generatedAt")}

def newest_confirmed(obj):
    """The newest "confirmed" date anywhere in the hand-written state: when the judgment was last reviewed."""
    best = ""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "confirmed" and isinstance(v, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", v):
                best = max(best, v)
            else:
                best = max(best, newest_confirmed(v))
    elif isinstance(obj, list):
        for v in obj:
            best = max(best, newest_confirmed(v))
    return best

def derived(st):
    ver = None
    try:
        ver = (SHARD / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        pass
    return {"version": ver, "playtests": playtest_counts(), "queue": queue_state(),
            "reviewed": newest_confirmed(st), "stale_days": STALE_DAYS}

def build():
    st = load(); cnt = counted(SHARD); dv = derived(st)
    d = st["setup_defects"]
    done, total = sum(1 for v in d.values() if v), len(d)

    L = []
    L.append("**Direction: staying on ModernUO.** ServUO content is pulled in piece by piece.")
    L.append("")
    # cc-P85: how old the hand-written judgment is, and the facts derived each run.
    q = dv["queue"]; pt = dv["playtests"] or {}
    run = q["running"]
    L.append(f"Judgment reviewed {dv['reviewed'] or 'never'}. Shard version {dv['version'] or 'unknown'}. "
             f"Autopilot {q['autopilot']}"
             + (f", running P{run['n']} ({run['slug']})" if run else "")
             + f", {len(q['queued'])} queued"
             + (f", latest done P{q['latest_done']['n']}" if q.get('latest_done') else "") + ". "
             + (f"Play tests: {pt.get('open')} open, {pt.get('failed')} failed, {pt.get('passed')} passed."
                if pt else "Play tests: no data."))
    L.append("")

    # cc-P92: the headline is the ServUO port list (tools/port-list.json), not every ServUO file ModernUO lacks.
    # That pool still has its own section lower down; it was never a target and the page always said so.
    pl = port_list()
    if pl:
        c = pl["counted"]
        L.append("## " + port_list_headline(pl))
        L.append("")
        if pl["next"]:
            L.append(f"**Next to land: {pl['next']}.** {DIRECTION_LINE}")
        else:
            L.append(f"**Every Port system is in.** {DIRECTION_LINE}")
        L.append("")
        L.append("```")
        L.append(f"Port list {bar(c['done'], c['total'])}  {c['done']}/{c['total']}   {c['pct']:.1f}%")
        L.append(f"Setup     {bar(done, total)}  {done}/{total}     blocking defects resolved")
        L.append("```")
        L.append("")
        L.append("| System | Done / files | | Feeds |")
        L.append("|---|---|---|---|")
        for r in pl["systems"]:
            if r["tier"] not in COUNTED_TIERS:
                continue
            L.append(f"| {r['title']}{' (in)' if r['complete'] else ''} | {r['done']} / {r['candidates']} | "
                     f"`{bar(r['done'], r['candidates'], 12)}` | {r['feeds']} |")
        for r in pl["systems"]:
            if r["tier"] == "decide":
                L.append(f"| {r['title']} (**waiting on Chase**) | {r['done']} / {r['candidates']} | | {r['feeds']} |")
        L.append("")
        others = [f"{t} {v['files']:,} files ({v['done']:,} in)" for t, v in pl["tiers"].items()
                  if t not in COUNTED_TIERS and t != "decide"]
        L.append("Not counted: " + "; ".join(others) + ". "
                 + (f"**{pl['unassigned']} candidate files belong to no system**: "
                    + ", ".join(f"`{x}`" for x in pl["unassigned_first"]) + ". "
                    if pl["unassigned"] else "Every candidate belongs to a system. ")
                 + "_Counted by filename stem (not behavior) against `server/customizations`; the list itself is "
                   "`tools/port-list.json`, kept by hand._")
        L.append("")
    else:
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
            src = "; ".join(g.get("sources", []))
            L.append(f"| {mark} | {g['name']} | {g.get('detail','')}"
                     + (f" _Sources: {src}._" if src else "")
                     + (f" _Confirmed {g['confirmed']}._" if g.get("confirmed") else "") + " |")
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
        L.append(f"### Every ServUO file ModernUO lacks, by area (not a target): {tot_d:,} of {tot_t:,} "
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
                 "Open work the overseer tracks")
        L.append("```")
        L.append("")
        L.append("| | Task | Status | Notes | Confirmed |")
        L.append("|---|---|---|---|---|")
        for t in tk:
            mark = {"done":"done","in-progress":"**in progress**","blocked":"**blocked**","todo":"todo"}[t["status"]]
            L.append(f"| `{t['id']}` | {t['title']} | {mark} | {t.get('note','')} | {t.get('confirmed','')} |")
        L.append("")
        L.append("_Status lives in `tools/progress-state.json`; `python tools/judge.py` updates one row and its date._")
        L.append("")

    # cc-P85: the CC prompt queue, derived each run (never hand-kept).
    q = dv["queue"]
    L.append(f"### Queue (autopilot {q['autopilot']}; {q['finished_total']} prompts finished, "
             f"{q['stopped_total']} of them stopped early)")
    L.append("")
    L.append("| Prompt | State | When |")
    L.append("|---|---|---|")
    rows = ([q["running"]] if q["running"] else []) + q["queued"] + q["finished"]
    for r in rows:
        when = r.get("since") or r.get("date") or ""
        state = r["state"] + (f": {r['why']}" if r.get("why") else "")
        L.append(f"| P{r['n']} {r['slug']} | {state} | {when} |")
    L.append("")

    up = st.get("upstream_patches") or {}
    if up:
        ps = up.get("patches", []); rp = up.get("replacements", [])
        hi = sum(1 for x in ps if x.get("risk") == "high")
        n_ps = cnt.get("upstream_patch_files"); rp_counted = cnt.get("upstream_replacements")
        n_rp = len(rp_counted) if rp_counted is not None else None
        L.append(f"### Needs reconciling on a `MODERNUO_COMMIT` bump: {n_ps} patches, {n_rp} replacements")
        L.append("")
        L.append(f"_Counted from `server/patches/` and `apply-patches.sh`. The table below is hand-kept in "
                 f"`progress-state.json` and lists {len(ps)} rows; it is a partial risk register, not the count._")
        L.append("")
        L.append(up.get("note", ""))
        L.append("")
        L.append("| Upstream file | Patch | Diff | Risk | Breaks when |")
        L.append("|---|---|---|---|---|")
        order = {"high": 0, "medium": 1, "low": 2}
        for x in sorted(ps, key=lambda v: order.get(v.get("risk"), 3)):
            L.append(f"| `{x['file']}` | {x['patch']} | {x['d']} | **{x['risk']}** | {x['breaks']} |")
        L.append("")
        rp_names = rp_counted if rp_counted is not None else [x['file'] for x in rp]
        L.append(f"**{len(rp_names)} full-file replacements fail silently on a bump** and must be diffed by hand: "
                 + ", ".join(f"`{x}`" for x in rp_names) + ".")
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
    ss = st.get("shard_status", "unknown")
    if isinstance(ss, dict):
        ss = ss.get("text", "unknown") + (f" (confirmed {ss['confirmed']})" if ss.get("confirmed") else "")
    L.append(f"Shard status: {ss}.")

    snap = {"generated": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds"),
            "direction": "stay on ModernUO; pull ServUO content selectively",
            "setup_defects": d, "setup_done": done, "setup_total": total,
            "patches": p, "ported_content": pc, "declined_content": dc,
            "upstream_patches": st.get("upstream_patches"), "counted": cnt, "content_progress": content_progress(), "tasks": st.get("tasks", []),
            # cc-P92: the port list, counted from the trees against tools/port-list.json.
            "port_list": pl,
            "playable_gates": st.get("playable_gates"),
            "shard_status": st.get("shard_status"),
            # cc-P85: the direction note, the as-of dates of the page's hand-written sections, and the derived facts.
            "direction": st.get("direction"), "sections": st.get("sections"), "derived": dv}
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
