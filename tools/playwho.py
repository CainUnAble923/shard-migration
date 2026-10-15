"""cc-P115: who tests each play-test item, and how.

Who comes from testing/bot-triage.md, the single source (its '| id | BUCKET | reason |' rows; the overnight bot's plan
reads the same rows). The steps come from testing/playtest-steps.json, a hand-written overlay keyed by item id. Neither
file is ever written by the importer (tools/playtests.py writes only play-tests.json and SUMMARY.md) nor by this module:
the service merges both into the document each time /api/items is read.

    annotate(doc, triage, steps) -> doc, with "who" and "steps" on each open, later or blocked item, and doc["who"]
    = {available, counts {you, botyou, decide, bot, cc, unsorted}, mine, unsorted [ids], buckets {BUCKET: n}}

Buckets and what the page calls them:
    BOT -> Bot; BOT-PARTIAL -> Bot, then you; EYES and DEPLOY -> You; DECISION -> You decide; CC -> CC.
An open item missing from the triage is "Not sorted yet" until someone adds it there.
"""
import json
import os
import re

TRIAGE_REL = os.path.join("testing", "bot-triage.md")
STEPS_REL = os.path.join("testing", "playtest-steps.json")
OPEN = ("open", "later", "blocked")

BUCKETS = {
    "BOT": {"key": "bot", "label": "Bot", "kind": "the overnight bot"},
    "BOT-PARTIAL": {"key": "botyou", "label": "Bot, then you", "kind": "the bot does the mechanics, you check the look"},
    "EYES": {"key": "you", "label": "You", "kind": "in the game or on screen"},
    "DEPLOY": {"key": "you", "label": "You", "kind": "a deploy, the console or a web page"},
    "DECISION": {"key": "decide", "label": "You decide", "kind": "a choice for you"},
    "CC": {"key": "cc", "label": "CC", "kind": "Claude Code, from files, logs or tests"},
}
UNSORTED = {"key": "unsorted", "label": "Not sorted yet", "kind": "", "bucket": "",
            "reason": "not in testing/bot-triage.md yet"}
KEYS = ("you", "botyou", "decide", "bot", "cc", "unsorted")
MINE = ("you", "botyou", "decide")

ROW = re.compile(r"^\|\s*([A-Za-z0-9]+-[A-Za-z0-9-]+)\s*\|\s*(BOT-PARTIAL|BOT|EYES|DEPLOY|DECISION|CC)\s*\|\s*(.*?)\s*\|\s*$")


def who_of(bucket):
    return dict(BUCKETS[bucket], bucket=bucket)


def parse_triage(text):
    """{id: {bucket, reason}} from the triage's item rows. The first row of an id wins."""
    out = {}
    for line in (text or "").splitlines():
        m = ROW.match(line)
        if m and m.group(1) not in out:
            out[m.group(1)] = {"bucket": m.group(2), "reason": m.group(3)}
    return out


_CACHE = {}


def _read(path, parse):
    """A file's parsed contents, re-read only when its modification time or size changes."""
    try:
        st = os.stat(path)
    except OSError:
        return None
    key = (st.st_mtime_ns, st.st_size)
    hit = _CACHE.get(path)
    if hit and hit[0] == key:
        return hit[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            value = parse(f.read())
    except (OSError, ValueError):
        value = None
    _CACHE[path] = (key, value)
    return value


def _steps(text):
    doc = json.loads(text)
    items = doc.get("items") if isinstance(doc, dict) else None
    return items if isinstance(items, dict) else {}


def load_sources(roots):
    """(triage, steps) from the first root that has each file. On Haven the notes clone comes first: the triage and
    the steps are committed files, and testing/ there is a separate data volume."""
    triage = steps = None
    for r in roots:
        if r and triage is None:
            triage = _read(os.path.join(r, TRIAGE_REL), parse_triage)
        if r and steps is None:
            steps = _read(os.path.join(r, STEPS_REL), _steps)
    return triage, steps


def annotate(doc, triage, steps):
    counts = dict.fromkeys(KEYS, 0)
    unsorted, buckets = [], {}
    available = triage is not None
    for it in doc.get("items", []):
        if not available or it.get("status") not in OPEN:
            continue
        t = triage.get(it["id"])
        if t:
            w = dict(who_of(t["bucket"]), reason=t["reason"])
            buckets[t["bucket"]] = buckets.get(t["bucket"], 0) + 1
        else:
            w = dict(UNSORTED)
            unsorted.append(it["id"])
        it["who"] = w
        it["steps"] = (steps or {}).get(it["id"]) or None
        counts[w["key"]] += 1
    doc["who"] = {"available": available, "counts": counts, "mine": sum(counts[k] for k in MINE),
                  "unsorted": unsorted, "buckets": buckets,
                  "labels": {v["key"]: v["label"] for v in list(BUCKETS.values()) + [UNSORTED]}}
    return doc
