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
# cc-P99: the autopilot became the Golem. Its folder is read once Move-ToGolem.ps1 has written ACTIVE there.
GOLEM     = Path(os.environ.get("SL_GOLEM", r"D:\UO\golem"))
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
             "why": s.get("why", ""), "covers": list(s.get("covers") or []), "candidates": 0, "done": 0}
            for s in systems]
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

def runner_folder(golem=None, autopilot=None):
    """cc-P99: the folder the queue runner keeps its state in. The Golem's once it is active (ACTIVE and
    Start-Golem.ps1 both there, as the Shard Console decides), else cc-autopilot's."""
    golem = Path(golem or GOLEM)
    if (golem / "ACTIVE").exists() and (golem / "Start-Golem.ps1").exists():
        return golem
    return Path(autopilot or AUTOPILOT)

def queue_state(notes_dir=None, prompts=None, autopilot=None):
    """The CC prompt queue: queued (cc-prompts/queue), running (the Golem's state.json; cc-autopilot's before the
    cutover), and the latest finished (each prompt's notes ends DONE or STOPPED). Read only; the Golem and the
    overseer own these files. The "autopilot" key (on or off) keeps its name so older readers still work."""
    notes_dir = Path(notes_dir or MIGRATE / "notes")
    prompts = Path(prompts or PROMPTS)
    autopilot = Path(autopilot) if autopilot else runner_folder()
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
            # cc-P136: a STOPPED prompt is never progress; done_total is what the page counts.
            "done_total": sum(1 for r in fin if r["state"] == "done"),
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

# --- cc-P136: judgments derived every run, and the ones still owed by the overseer ----------------------------------
# The rules, each computed here and never stored in progress-state.json:
#   1. a port-list system whose candidate files are all ported is "in" (port_list(), "complete");
#   2. a task whose id a port-list system lists under "covers" is that system's work: shown as covered by it, with the
#      system's counts, and left out of the task totals (split_tasks());
#   3. a prompt whose notes end STOPPED is never progress: it is not in done_total, not the latest done, and never
#      makes a task row owe a review (queue_state(), review_owed());
#   4. "next to land" is the first Port row, in port-list order, that is not in (port_list(), "next").
# What cannot be derived goes in the "Needs overseer review" box (review_owed()), one line per item with the judge.py
# command that settles it. Nothing here writes progress-state.json: a needs_confirm mark stays until a person clears it.
REVIEW_DAYS = STALE_DAYS
_PREFS = re.compile(r"\bP(\d+)(?:\s*-\s*P?(\d+))?\b")
_DATE_IN_NAME = re.compile(r"(\d{4}-\d{2}-\d{2})")


def safely(what, fn, fallback):
    """Run one derived step; on any error say so in one line and carry on, so a refresh never blocks a commit."""
    try:
        return fn()
    except Exception as e:
        print(f"  {what} not worked out ({type(e).__name__}: {e}); the rest of the page is refreshed", file=sys.stderr)
        return fallback


def split_tasks(tasks, pl):
    """Rule 2: (own, covered). own keeps the order of tasks; covered rows carry the covering systems' titles, their
    summed done and files, and "in" when every covering system is in. Ids match case-insensitively."""
    by = {}
    for r in (pl or {}).get("systems", []):
        for tid in r.get("covers") or []:
            by.setdefault(str(tid).lower(), []).append(r)
    own, covered = [], []
    for t in tasks:
        rs = by.get(str(t.get("id", "")).lower())
        if not rs:
            own.append(t)
            continue
        covered.append({"id": t.get("id"), "title": t.get("title", ""), "by": [r["title"] for r in rs],
                        "done": sum(r["done"] for r in rs), "files": sum(r["candidates"] for r in rs),
                        "in": all(r["complete"] for r in rs)})
    return own, covered


def prompt_refs(text):
    """The prompt numbers a task names: "P80", "P65-P84" and "P65-84" (a range of at most 200)."""
    out = set()
    for a, b in _PREFS.findall(text or ""):
        lo = int(a); hi = int(b) if b else lo
        out.update(range(lo, hi + 1) if lo <= hi <= lo + 200 else (lo,))
    return out


def newest_decisions_note(notes_dir):
    """(date, "notes/<name>") of the newest notes/*decision*.md, dated by the YYYY-MM-DD in its name, else its mtime."""
    best = ("", "")
    for f in Path(notes_dir).glob("*decision*.md"):
        m = _DATE_IN_NAME.search(f.name)
        best = max(best, (m.group(1) if m else _mdate(f), "notes/" + f.name))
    return best


def review_label(x):
    """"gate Things to fight", "task DEPLOY"; "shard status" and "direction" once, not twice."""
    return x["item"] if x["kind"] in x["item"] else f"{x['kind']} {x['item']}"


def review_owed(st, finished, notes_dir=None, today=None, days=REVIEW_DAYS):
    """The "Needs overseer review" box: [{kind, item, check, cmd: [judge.py lines]}], gates first, then tasks, the
    shard status and the direction. Owed: a gate or task judge.py marked needs_confirm (Chase's or the overseer's call;
    never settled here); a gate or the status confirmed more than `days` ago; a task row confirmed more than `days` ago
    while a prompt it names finished DONE after that date; the direction confirmed before the newest decisions note.
    An empty list means nothing is owed."""
    from datetime import date as _date
    today = today or _date.today()
    notes_dir = Path(notes_dir or MIGRATE / "notes")

    def age(d):
        try:
            return (today - _date.fromisoformat(d)).days
        except (TypeError, ValueError):
            return None

    def old(d):
        a = age(d)
        return a is None or a > days

    out = []
    for g in (st.get("playable_gates") or {}).get("gates", []):
        name, c = g["name"], g.get("confirmed", "")
        settle = [f'python tools/judge.py gate "{name}" --done {"no" if g.get("done") else "yes"} --detail "..."',
                  f'python tools/judge.py confirm gate "{name}"']
        if g.get("needs_confirm"):
            out.append({"kind": "gate", "item": name, "check": f"Waits on a confirmation: {g['needs_confirm']} "
                        "Settle it with whoever was asked, then record the answer (or re-confirm as it stands).",
                        "cmd": settle})
        elif old(c):
            out.append({"kind": "gate", "item": name, "check": f"Last confirmed {c or 'never'}"
                        + (f" ({age(c)} days ago)" if age(c) is not None else "")
                        + ". Re-read its sources; still " + ("met" if g.get("done") else "not met") + "?",
                        "cmd": [settle[1], settle[0]]})
    done_prompts = [r for r in finished if r.get("state") == "done"]
    for t in st.get("tasks", []):
        tid, c = t["id"], t.get("confirmed", "")
        settle = [f'python tools/judge.py task {tid} --status todo|in-progress|blocked|done --note "..."',
                  f"python tools/judge.py confirm task {tid}"]
        if t.get("needs_confirm"):
            out.append({"kind": "task", "item": tid, "check": f"{t.get('title', '')}: waits on a confirmation: "
                        f"{t['needs_confirm']}", "cmd": settle})
            continue
        if t.get("status") == "done" or not old(c):
            continue
        refs = prompt_refs(f"{t.get('title', '')} {t.get('note', '')}") | {int(x) for x in t.get("prompts", [])}
        since = sorted(r["n"] for r in done_prompts if r["n"] in refs and r.get("date", "") > c)
        if since:
            out.append({"kind": "task", "item": tid, "check": f"{t.get('title', '')}: untouched since {c} while "
                        + ", ".join(f"P{n}" for n in since) + " finished. Does its status or note change?",
                        "cmd": settle})
    ss = st.get("shard_status")
    if isinstance(ss, dict) and old(ss.get("confirmed", "")):
        out.append({"kind": "status", "item": "shard status", "check": f"Last confirmed {ss.get('confirmed') or 'never'}:"
                    f" \"{ss.get('text', '')}\". Still what runs?",
                    "cmd": ['python tools/judge.py status "..."', "python tools/judge.py confirm status"]})
    dr = st.get("direction")
    if isinstance(dr, dict):
        nd, nf = newest_decisions_note(notes_dir)
        if nd and nd > dr.get("confirmed", ""):
            out.append({"kind": "direction", "item": "direction", "check": f"Confirmed {dr.get('confirmed') or 'never'};"
                        f" {nf} ({nd}) is newer. Read it; if the direction moved, edit \"direction\" in "
                        "tools/progress-state.json.", "cmd": ["python tools/judge.py confirm direction"]})
    return out


def review_playtests(root=None):
    """cc-P137: open play-test items with no Who, and triage rows naming a bucket the page does not know, owe the
    overseer a sort (testing/bot-triage.md says where each new prompt's items go). One review line, or none."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import playtests as pt
    import playwho
    root = Path(root or MIGRATE)
    triage, steps = playwho.load_sources([str(root)])
    if triage is None:
        return []
    doc = playwho.annotate(pt.ordered_doc(pt.load(str(root / pt.DATA_REL))), triage, steps)
    unsorted = doc["who"]["unsorted"]
    bad = playwho.malformed_rows((root / "testing" / "bot-triage.md").read_text(encoding="utf-8"))
    if not unsorted and not bad:
        return []
    parts = []
    if unsorted:
        parts.append(f"{len(unsorted)} open play-test item(s) have no Who: {', '.join(unsorted[:20])}"
                     + (" ..." if len(unsorted) > 20 else ""))
    if bad:
        parts.append(f"{len(bad)} triage row(s) name an unknown bucket: {', '.join(bad)}")
    return [{"kind": "play tests", "item": "not sorted", "check": "; ".join(parts) + ". Sort each into "
             "testing/bot-triage.md with its steps in testing/playtest-steps.json (that file's 'Where a new prompt's "
             "items are sorted'), then run the check.", "cmd": ["python -m unittest tools/tests/test_play_who.py"]}]


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
             f"Golem {q['autopilot']}"
             + (f", running P{run['n']} ({run['slug']})" if run else "")
             + f", {len(q['queued'])} queued"
             + (f", latest done P{q['latest_done']['n']}" if q.get('latest_done') else "") + ". "
             + (f"Play tests: {pt.get('open')} open, {pt.get('failed')} failed, {pt.get('passed')} passed."
                if pt else "Play tests: no data."))
    L.append("")

    # cc-P92: the headline is the ServUO port list (tools/port-list.json), not every ServUO file ModernUO lacks.
    # That pool still has its own section lower down; it was never a target and the page always said so.
    pl = port_list()
    # cc-P136: the derived judgments and the review box. Each step that fails says so in one line and the rest goes on.
    own_tasks, covered_tasks = safely("covered tasks", lambda: split_tasks(st.get("tasks", []), pl),
                                      (st.get("tasks", []), []))
    review = safely("review box", lambda: review_owed(st, finished_prompts(MIGRATE / "notes")), None)
    if review is not None:
        review += safely("play-test sort check", review_playtests, [])
    if review is None:
        L.append("### Needs overseer review: **could not be worked out this run** (see the progress.py output).")
    elif review:
        L.append(f"### Needs overseer review ({len(review)})")
        L.append("")
        for x in review:
            L.append(f"- **{review_label(x)}**: {x['check']} " + " or ".join(f"`{c}`" for c in x["cmd"]))
    else:
        L.append("### Needs overseer review: nothing owed.")
    L.append("")
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

    tk = own_tasks
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
    if covered_tasks:
        L.append("Covered by the port list (not counted above): "
                 + "; ".join(f"`{c['id']}` {c['title']}: {', '.join(c['by'])}, {c['done']}/{c['files']} files"
                             + (" (in)" if c["in"] else "") for c in covered_tasks) + ".")
        L.append("")

    # cc-P85: the CC prompt queue, derived each run (never hand-kept).
    q = dv["queue"]
    L.append(f"### Queue (Golem {q['autopilot']}; {q['done_total']} prompts done, "
             f"{q['stopped_total']} more stopped early and not counted)")
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
            "upstream_patches": st.get("upstream_patches"), "counted": cnt, "content_progress": content_progress(),
            # cc-P136: tasks a port-list system covers are listed apart and left out of the task totals; review is
            # the "Needs overseer review" box (None when it could not be worked out, [] when nothing is owed).
            "tasks": own_tasks, "tasks_covered": covered_tasks, "review": review,
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
    try:
        rep = build()
    except Exception as e:   # cc-P136: one line, so the commit script can say why and commit anyway
        print(f"  progress.py failed: {type(e).__name__}: {e}; the page was left as it was", file=sys.stderr)
        sys.exit(1)
    _emit(rep)
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
