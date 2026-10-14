"""cc-P112: the play-test page's robot icons, from tonight's bot plan.

The plan is written on the game PC by the bot's own work check (D:\\ShatteredLegacy\\tools\\playtest-bot\\uobot\\tonight.py,
which calls uobot.work.find_work, the runner's rule), into testing/bot-tonight.json. On Haven the same plan arrives inside
the game PC snapshot (botTonight). This module only shapes it for the page: no rule, no git, no subprocess.

    shape(plan, source, report_exists) -> {available, source, asOf, commit, short, minutes, count, items: {id: {...}}}

Each item is "tonight" (the robot: the overnight bot tries it tonight) or "checkable" (the dim robot: the bot can check
it, but tonight has no work for it), with a tooltip and, when the bot has a result for it, that result, its run and a
link to the run's report. Items in neither get no icon.
"""
import json
import os
import re

PLAN_REL = os.path.join("testing", "bot-tonight.json")
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}$")
LABELS = {"PASS": "pass", "FAIL": "fail", "FLAKY": "flaky", "ERROR": "could not run"}


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def as_of_text(iso):
    """'2026-10-14T22:49:32Z' -> '2026-10-14 22:49 UTC'; '' if there is none."""
    return (iso[:10] + " " + iso[11:16] + " UTC") if iso and len(iso) >= 16 else ""


def unavailable(why):
    return {"available": False, "reason": why, "count": 0, "items": {}}


def shape(plan, source, report_exists=lambda stamp: False):
    if not isinstance(plan, dict) or plan.get("schema") != 1:
        return unavailable("no bot plan" + (" in the game PC snapshot" if source == "snapshot" else ""))
    if not plan.get("available"):
        return unavailable(str(plan.get("error") or "the work check could not run"))
    as_of = as_of_text(plan.get("generatedAt", ""))
    tail = (" Plan as of %s." % as_of) if as_of else ""
    last = plan.get("last") or {}
    items = {}

    def result_of(iid):
        r = last.get(iid)
        if not isinstance(r, dict) or r.get("result") not in LABELS:
            return None
        run = str(r.get("run") or "")
        out = {"result": r["result"], "label": LABELS[r["result"]], "run": run, "at": str(r.get("at") or "")}
        if STAMP.match(run) and report_exists(run):
            out["report"] = "/bot-runs/%s/report?item=%s#item-%s" % (run, iid, iid)
        return out

    for iid, t in (plan.get("tonight") or {}).items():
        minutes = int((t or {}).get("minutes") or 0)
        items[iid] = {"state": "tonight", "minutes": minutes, "reason": str((t or {}).get("reason") or ""),
                      "title": "The overnight bot tries this tonight (about %d min).%s" % (max(1, minutes), tail),
                      "last": result_of(iid)}
    for iid in plan.get("checkable") or []:
        if iid in items:
            continue
        r = result_of(iid)
        if r:
            title = "Bot-checkable; already checked on this code. Last bot result: %s, %s.%s" % (r["label"], r["at"][:10] or r["run"], tail)
        else:
            title = "Bot-checkable; no bot check is built for it yet, so tonight's run does not try it.%s" % tail
        items[iid] = {"state": "checkable", "title": title, "last": r}
    return {"available": True, "source": source, "asOf": as_of, "commit": str(plan.get("commit") or ""),
            "short": str(plan.get("short") or ""), "minutes": int(plan.get("minutes") or 0),
            "count": sum(1 for v in items.values() if v["state"] == "tonight"), "items": items}


def report_html(markdown, item=""):
    """A run's report.md as a page: the text as it is, each table row of an item with an anchor (#item-<id>), and the
    asked-for item's row marked. Read only; no markdown rendering beyond that."""
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    rows = []
    for line in markdown.splitlines():
        m = re.match(r"^\|\s*([A-Za-z0-9-]+)\s*\|", line)
        if m and m.group(1) not in ("Id", "---"):
            mark = ' class="hit"' if m.group(1) == item else ""
            rows.append('<span id="item-%s"%s>%s</span>' % (esc(m.group(1)), mark, esc(line)))
        else:
            rows.append(esc(line))
    return ("<!doctype html><meta charset=utf-8><title>Bot report</title>"
            "<style>body{font:14px ui-monospace,Consolas,monospace;margin:16px;white-space:pre-wrap}"
            ".hit{background:#ffe9a8;color:#000}</style>" + "\n".join(rows))
