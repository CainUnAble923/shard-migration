"""Bug reports inbox (cc-P97): the store and the rules, beside ideas.py and handled exactly like it.

Chase reports a bug from the play-test page while testing, from scratch or from a play test ("Bug from this", or the
offer after marking one Fail). The overseer reads them ("Copy new bugs") and gives the real ones a D-number in
docs/bug-list.md. This is the inbox that feeds the bug list, not a second bug list: nothing here edits docs/.

  testing/bug-reports.json          the reports. Ids B-001, B-002 ... from a stored counter (nextId), so an id is never
                                    reused, even after a delete. Pretty-printed, fixed key order, written atomically
                                    (temp file + rename) under its own lock file, exactly like feature-ideas.json.
  testing/bug-reports/files/        screenshots, B-001-1.png and on: PNG or JPG only, 2 MB at most, 3 per report.
                                    The page re-encodes a larger picture before it sends it; the server checks the
                                    bytes and refuses anything else (standard library only: it cannot re-encode).

docker/test-queue/server.py (D:\\ShatteredLegacy) imports this file. Standard library only. ASCII only.
"""
import base64
import binascii
import json
import os
import re

import ideas
import playtests as pt

SCHEMA = 1
DATA_REL = os.path.join("testing", "bug-reports.json")
FILES_REL = os.path.join("testing", "bug-reports", "files")

SEVERITIES = ("blocks play", "wrong", "annoying", "looks wrong")
AREAS = ideas.AREAS
# Status keys and the words the page shows for them.
STATUSES = {"new": "new", "taken": "taken by the overseer", "duplicate": "duplicate", "notbug": "not a bug",
            "fixed": "fixed"}
DNUM_RE = re.compile(r"^D\d+$")
DUP_RE = re.compile(r"^(D\d+|B-\d{3,})$")
ID_RE = re.compile(r"^B-(\d{3,})$")

LIMITS = {"title": 140, "text": 2000, "short": 140, "reason": 300}
MAX_SHOTS = 3
MAX_SHOT_BYTES = 2 * 1024 * 1024
SHOT_TYPES = {"png": b"\x89PNG\r\n\x1a\n", "jpg": b"\xff\xd8\xff"}
SHOT_NAME_RE = re.compile(r"^B-\d{3,}-\d+\.(png|jpg)$")


# --- the store ----------------------------------------------------------------------------------

def new_doc():
    return {"schema": SCHEMA, "nextId": 1, "copiedAt": "", "bugs": [], "deleted": []}


def new_bug(**kw):
    bug = {"id": "", "title": "", "happened": "", "expected": "", "steps": "", "severity": "", "area": "",
           "playtest": "", "character": "", "location": "", "version": "", "shots": [], "status": "new", "dnum": "",
           "duplicateOf": "", "reason": "", "by": "", "createdAt": "", "updatedAt": "", "statusAt": ""}
    bug.update(kw)
    return bug


def ordered_bug(b):
    base = new_bug()
    out = {k: b.get(k, base[k]) for k in base}
    out["shots"] = list(out["shots"] or [])
    return out


def ordered_deleted(d):
    return {k: d.get(k, "") for k in ("id", "title", "reason", "by", "deletedAt")}


def num(bug_id):
    return int(ID_RE.match(bug_id).group(1))


def ordered_doc(doc):
    bugs = sorted((ordered_bug(b) for b in doc.get("bugs", [])), key=lambda b: num(b["id"]))
    gone = sorted((ordered_deleted(d) for d in doc.get("deleted", [])), key=lambda d: num(d["id"]))
    return {"schema": SCHEMA, "nextId": int(doc.get("nextId") or 1), "copiedAt": doc.get("copiedAt", ""),
            "bugs": bugs, "deleted": gone}


def path_of(root):
    return os.path.join(root, DATA_REL)


def files_dir(root):
    return os.path.join(root, FILES_REL)


def load(root):
    path = path_of(root)
    if not os.path.exists(path):
        return new_doc()
    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("schema") != SCHEMA:
        raise RuntimeError("bug-reports.json schema %r is not %d" % (doc.get("schema"), SCHEMA))
    for k, v in new_doc().items():
        doc.setdefault(k, v)
    # The counter can never fall behind an id that exists or was deleted (a hand-edited file, say).
    used = [num(x["id"]) for x in doc["bugs"] + doc["deleted"] if ID_RE.match(x.get("id", ""))]
    doc["nextId"] = max([int(doc["nextId"] or 1)] + [u + 1 for u in used])
    return doc


def save(root, doc):
    path = path_of(root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    final = ordered_doc(doc)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="ascii", newline="\n") as f:
        f.write(json.dumps(final, indent=2, ensure_ascii=True) + "\n")
    os.replace(tmp, path)
    return final


def update(root, fn):
    """Read, change one thing, write, all under the lock (playtests.Lock, its own lock file)."""
    with pt.Lock(path_of(root)):
        doc = load(root)
        value = fn(doc)
        save(root, doc)
    return value


def find(doc, bug_id):
    for b in doc["bugs"]:
        if b["id"] == bug_id:
            return b
    raise KeyError(bug_id)


def summary(doc):
    count = {k: 0 for k in STATUSES}
    for b in doc["bugs"]:
        count[b["status"]] = count.get(b["status"], 0) + 1
    out = dict(count)
    out["pending"] = sum(1 for b in doc["bugs"] if b["status"] == "taken" and not b["dnum"])
    out["total"] = len(doc["bugs"])
    return out


# --- checks ---------------------------------------------------------------------------------------

def _text(value, limit):
    # Line breaks are kept (steps are a list); runs of spaces inside a line are not.
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in str(value).replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip()[:limit]


def clean_fields(title=None, happened=None, expected=None, steps=None, severity=None, area=None, playtest=None,
                 character=None, location=None):
    out = {}
    if title is not None:
        t = pt.norm(title)[:LIMITS["title"]]
        if not t:
            raise ValueError("a bug report needs a title")
        out["title"] = t
    for k, v in (("happened", happened), ("expected", expected), ("steps", steps)):
        if v is not None:
            out[k] = _text(v, LIMITS["text"])
    for k, v in (("character", character), ("location", location)):
        if v is not None:
            out[k] = pt.norm(v)[:LIMITS["short"]]
    if severity is not None:
        s = pt.norm(severity)
        if s and s not in SEVERITIES:
            raise ValueError("severity must be one of: " + ", ".join(SEVERITIES))
        out["severity"] = s
    if area is not None:
        a = pt.norm(area)
        if a and a not in AREAS:
            raise ValueError("area must be one of: " + ", ".join(AREAS))
        out["area"] = a
    if playtest is not None:
        p = pt.norm(playtest)
        if p and not ideas.PLAYTEST_RE.match(p):
            raise ValueError("a linked play test looks like P71-3, T-012 or M-001")
        out["playtest"] = p
    return out


def reason_of(reason, what):
    r = pt.norm(reason)[:LIMITS["reason"]]
    if not r:
        raise ValueError(what + " needs a one-line reason")
    return r


# --- the actions ------------------------------------------------------------------------------------

def add(root, title, happened="", expected="", steps="", severity="", area="", playtest="", character="",
        location="", version="", by=""):
    fields = clean_fields(title, happened, expected, steps, severity, area, playtest, character, location)

    def fn(doc):
        bid = "B-%03d" % doc["nextId"]
        doc["nextId"] += 1
        stamp = pt.now_iso()
        doc["bugs"].append(new_bug(id=bid, createdAt=stamp, updatedAt=stamp, version=pt.norm(version)[:60],
                                   by=pt.norm(by)[:60], **fields))
        return dict(doc["bugs"][-1])
    return update(root, fn)


def edit(root, bug_id, **kw):
    fields = clean_fields(**kw)

    def fn(doc):
        b = find(doc, bug_id)
        b.update(fields)
        b["updatedAt"] = pt.now_iso()
        return dict(b)
    return update(root, fn)


def set_status(root, bug_id, status, dnum="", duplicate_of="", reason=""):
    """new; taken (the overseer has it: with a D-number it 'became D-NN', without one it is pending a number);
    duplicate (of a D-number or another report, required); notbug (a reason, required); fixed."""
    if status not in STATUSES:
        raise ValueError("status must be one of: " + ", ".join(STATUSES))
    dnum = pt.norm(dnum).upper()
    dup = pt.norm(duplicate_of).upper()
    if dnum and not DNUM_RE.match(dnum):
        raise ValueError("a bug-list number looks like D89")
    if status == "duplicate":
        if not DUP_RE.match(dup):
            raise ValueError("a duplicate needs what it duplicates: a D-number (D89) or a report (B-003)")
        if dup == bug_id:
            raise ValueError("a report cannot duplicate itself")
    if status == "notbug":
        reason = reason_of(reason, "'not a bug'")
    else:
        reason = ""

    def fn(doc):
        b = find(doc, bug_id)
        stamp = pt.now_iso()
        # taken: the D-number given, or none yet (pending). fixed: the one given, else the one it had (the row that
        # closed). Every other status clears it.
        d = ""
        if status == "taken":
            d = dnum
        elif status == "fixed":
            d = dnum or b["dnum"]
        b.update(status=status, dnum=d, duplicateOf=dup if status == "duplicate" else "", reason=reason,
                 statusAt=stamp, updatedAt=stamp)
        return dict(b)
    return update(root, fn)


def mark_taken(root, ids):
    """The reports copied for the overseer: each one still 'new' becomes 'taken', pending its D-number."""
    ids = [pt.norm(i) for i in ids]

    def fn(doc):
        stamp = pt.now_iso()
        done = []
        for b in doc["bugs"]:
            if b["id"] in ids and b["status"] == "new":
                b.update(status="taken", statusAt=stamp, updatedAt=stamp)
                done.append(b["id"])
        doc["copiedAt"] = stamp
        return done
    return update(root, fn)


def delete(root, bug_id, reason, by=""):
    """Removes the report and its screenshots. The id, title and reason are kept under 'deleted', and nextId is
    untouched, so the id is never handed out again and why it went is not forgotten."""
    reason = reason_of(reason, "deleting a report")

    def fn(doc):
        b = find(doc, bug_id)
        doc["bugs"].remove(b)
        doc["deleted"].append({"id": b["id"], "title": b["title"], "reason": reason, "by": pt.norm(by)[:60],
                               "deletedAt": pt.now_iso()})
        for name in b["shots"]:
            try:
                os.remove(os.path.join(files_dir(root), name))
            except OSError:
                pass
        return b["id"]
    return update(root, fn)


# --- screenshots ------------------------------------------------------------------------------------

def shot_type(data):
    for ext, magic in SHOT_TYPES.items():
        if data[:len(magic)] == magic:
            return ext
    return None


def decode_shot(b64):
    """The page sends a data URL or bare base64. Returns the bytes, or raises ValueError."""
    s = str(b64 or "")
    if s.startswith("data:"):
        s = s.split(",", 1)[-1]
    try:
        return base64.b64decode(s, validate=True)
    except (binascii.Error, ValueError):
        raise ValueError("the screenshot is not valid base64")


def add_shot(root, bug_id, data):
    """Stores one screenshot for a report: PNG or JPG by its bytes (never by a name), at most MAX_SHOT_BYTES, at most
    MAX_SHOTS per report. Returns the file name."""
    if not data:
        raise ValueError("the screenshot is empty")
    ext = shot_type(data)
    if not ext:
        raise ValueError("a screenshot must be a PNG or JPG picture")
    if len(data) > MAX_SHOT_BYTES:
        raise ValueError("a screenshot can be at most 2 MB (this one is %.1f MB)" % (len(data) / 1048576.0))

    def fn(doc):
        b = find(doc, bug_id)
        if len(b["shots"]) >= MAX_SHOTS:
            raise ValueError("a report holds at most %d screenshots" % MAX_SHOTS)
        used = [int(re.match(r"^B-\d+-(\d+)\.", n).group(1)) for n in b["shots"]]
        name = "%s-%d.%s" % (bug_id, max(used + [0]) + 1, ext)
        os.makedirs(files_dir(root), exist_ok=True)
        path = os.path.join(files_dir(root), name)
        tmp = path + ".tmp"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
        b["shots"].append(name)
        b["updatedAt"] = pt.now_iso()
        return name
    return update(root, fn)


def shot_path(root, name):
    if not SHOT_NAME_RE.match(name or ""):
        raise KeyError(name)
    return os.path.join(files_dir(root), name)


# --- for the overseer ---------------------------------------------------------------------------------

def copy_text(doc, playtests=None, files_root="D:\\UO\\shard-migration"):
    """Every 'new' report as plain text, oldest first, one block per report with every field, ready to paste into the
    overseer chat. A linked play test gives its id and title; screenshots give their full paths on this PC."""
    titles = {}
    for it in (playtests or {}).get("items", []):
        titles[it["id"]] = it.get("label") or it.get("what") or it.get("text") or ""
    blocks = []
    for b in sorted((x for x in doc["bugs"] if x["status"] == "new"), key=lambda x: num(x["id"])):
        pl = b["playtest"] or "(none)"
        if b["playtest"] and titles.get(b["playtest"]):
            pl += " (" + pt.norm(titles[b["playtest"]])[:100] + ")"
        lines = ["%s: %s" % (b["id"], b["title"]),
                 "Severity: " + (b["severity"] or "(none)"),
                 "Area: " + (b["area"] or "(none)"),
                 "Linked play test: " + pl,
                 "Shard version: " + (b["version"] or "(unknown)"),
                 "Character: " + (b["character"] or "(none)"),
                 "Location: " + (b["location"] or "(none)"),
                 "Reported: " + b["createdAt"]]
        for label, key in (("What happened", "happened"), ("Expected", "expected"), ("Steps", "steps")):
            if b[key]:
                lines.append(label + ":")
                lines += ["  " + l for l in b[key].split("\n")]
            else:
                lines.append(label + ": (none)")
        if b["shots"]:
            lines.append("Screenshots:")
            lines += ["  " + files_root.rstrip("\\") + "\\" + FILES_REL.replace("/", "\\") + "\\" + n for n in b["shots"]]
        else:
            lines.append("Screenshots: (none)")
        blocks.append("\n".join(lines))
    if not blocks:
        return ""
    head = "New bug reports from the play-test page (%d), for D-numbers in docs/bug-list.md:" % len(blocks)
    return head + "\n\n" + "\n\n".join(blocks) + "\n"
