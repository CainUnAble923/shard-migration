#!/usr/bin/env python3
"""
Update one hand-written judgment in tools/progress-state.json and stamp it with today's date (cc-P85).

The dashboard (dashboard.html, README.md's progress block) shows how old the judgment is: "Judgment reviewed <date>"
is the newest "confirmed" date in progress-state.json, amber after 7 days, and each gate and task shows its own. This
script is the cheap way to keep those dates honest: change a row, or only re-confirm it, in one line.

    python tools/judge.py list                                     # every gate, task and section with its date
    python tools/judge.py gate "Things to fight" --done no --detail "..." --source "notes/cc-P76-extra-facets.md"
    python tools/judge.py task S7 --status in-progress --note "..."
    python tools/judge.py add-task F-50 --title "..." --status todo --note "..."
    python tools/judge.py retire-task C3                           # remove a finished or dropped task
    python tools/judge.py status "running on ModernUO; ..."        # the one-line shard status
    python tools/judge.py confirm gate "Things to fight"           # still true: only the date changes
    python tools/judge.py confirm all                              # every hand-written item re-read today

A gate is found by its exact name, else by the one name that starts with what you typed. Then run
python tools/progress.py to redraw the page (Commit-ShardWork.ps1 also runs it before every commit).
--state and --date are for tests. Standard library only. ASCII only.
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

DEFAULT_STATE = Path(__file__).resolve().parent / "progress-state.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, st):
    Path(path).write_text(json.dumps(st, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")


def find_gate(st, name):
    gates = (st.get("playable_gates") or {}).get("gates", [])
    exact = [g for g in gates if g["name"].lower() == name.lower()]
    if exact:
        return exact[0]
    starts = [g for g in gates if g["name"].lower().startswith(name.lower())]
    if len(starts) == 1:
        return starts[0]
    raise SystemExit(f"no single gate matches '{name}'" + (f": {', '.join(g['name'] for g in starts)}" if starts else ""))


def find_task(st, tid):
    for t in st.get("tasks", []):
        if t["id"].lower() == tid.lower():
            return t
    raise SystemExit(f"no task '{tid}'")


def run(argv, state=DEFAULT_STATE, today=None):
    ap = argparse.ArgumentParser(prog="judge.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("--state", default=str(state))
    ap.add_argument("--date", default=today)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    g = sub.add_parser("gate"); g.add_argument("name"); g.add_argument("--done", choices=["yes", "no"])
    g.add_argument("--detail"); g.add_argument("--source", action="append")
    t = sub.add_parser("task"); t.add_argument("id"); t.add_argument("--status", choices=["todo", "in-progress", "blocked", "done"])
    t.add_argument("--note"); t.add_argument("--title")
    a = sub.add_parser("add-task"); a.add_argument("id"); a.add_argument("--title", required=True)
    a.add_argument("--status", choices=["todo", "in-progress", "blocked", "done"], default="todo"); a.add_argument("--note", default="")
    r = sub.add_parser("retire-task"); r.add_argument("id")
    s = sub.add_parser("status"); s.add_argument("text")
    c = sub.add_parser("confirm"); c.add_argument("what", choices=["gate", "task", "status", "direction", "section", "all"])
    c.add_argument("key", nargs="?")
    args = ap.parse_args(argv)
    day = args.date or date.today().isoformat()
    st = load(args.state)
    said = []

    if args.cmd == "list":
        print(f"status    {st.get('shard_status', {}).get('confirmed', '?')}  {st.get('shard_status', {}).get('text', '')}")
        print(f"direction {st.get('direction', {}).get('confirmed', '?')}  {st.get('direction', {}).get('title', '')}")
        for x in (st.get("playable_gates") or {}).get("gates", []):
            print(f"gate      {x.get('confirmed', '?')}  {'yes' if x.get('done') else 'no '}  {x['name']}")
        for x in st.get("tasks", []):
            print(f"task      {x.get('confirmed', '?')}  {x['status']:<11}  {x['id']}  {x['title']}")
        for k, v in (st.get("sections") or {}).items():
            print(f"section   {v}  {k}")
        return 0

    if args.cmd == "gate":
        x = find_gate(st, args.name)
        if args.done: x["done"] = args.done == "yes"
        if args.detail is not None: x["detail"] = args.detail
        if args.source: x["sources"] = args.source
        x["confirmed"] = day; said.append(f"gate '{x['name']}' confirmed {day}")
    elif args.cmd == "task":
        x = find_task(st, args.id)
        for k in ("status", "note", "title"):
            if getattr(args, k) is not None: x[k] = getattr(args, k)
        x["confirmed"] = day; said.append(f"task {x['id']} confirmed {day}")
    elif args.cmd == "add-task":
        if any(t["id"].lower() == args.id.lower() for t in st.get("tasks", [])):
            raise SystemExit(f"task '{args.id}' exists; use task")
        st.setdefault("tasks", []).append({"id": args.id, "title": args.title, "status": args.status, "note": args.note, "confirmed": day})
        said.append(f"task {args.id} added")
    elif args.cmd == "retire-task":
        x = find_task(st, args.id)
        st["tasks"].remove(x); said.append(f"task {x['id']} retired")
        st.setdefault("sections", {})["tasks-reviewed"] = day
    elif args.cmd == "status":
        st["shard_status"] = {"text": args.text, "confirmed": day}; said.append("status set")
    elif args.cmd == "confirm":
        if args.what == "all":
            st["shard_status"]["confirmed"] = day; st["direction"]["confirmed"] = day
            for x in (st.get("playable_gates") or {}).get("gates", []): x["confirmed"] = day
            for x in st.get("tasks", []): x["confirmed"] = day
            said.append("everything confirmed " + day)
        elif args.what == "gate":
            find_gate(st, args.key or "")["confirmed"] = day; said.append("gate confirmed")
        elif args.what == "task":
            find_task(st, args.key or "")["confirmed"] = day; said.append("task confirmed")
        elif args.what == "status":
            st["shard_status"]["confirmed"] = day; said.append("status confirmed")
        elif args.what == "direction":
            st["direction"]["confirmed"] = day; said.append("direction confirmed")
        else:
            if not args.key or args.key not in (st.get("sections") or {}):
                raise SystemExit(f"sections are: {', '.join((st.get('sections') or {}).keys())}")
            st["sections"][args.key] = day; said.append(f"section {args.key} confirmed")
    save(args.state, st)
    for line in said:
        print(line)
    print("now run: python tools/progress.py")
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
