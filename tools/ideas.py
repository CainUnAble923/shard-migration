"""Feature ideas inbox (cc-P90): the store and the rules, beside playtests.py and handled exactly like it.

Chase jots an idea on the play-test page while testing; the features chat later turns it into an F-NN in
docs/feature-queue.md, or declines it. This is an inbox, not a second feature list: nothing here edits docs/.

  testing/feature-ideas.json   the ideas. Ids I-001, I-002 ... from a stored counter (nextId), so an id is never
                               reused, even after a delete. Pretty-printed, fixed key order, written atomically
                               (temp file + rename) under its own lock file, exactly like play-tests.json.
  docs/feature-queue.md        read only: its F-NN entries, for the read-only list and the duplicate hint.

docker/test-queue/server.py (D:\\ShatteredLegacy) imports this file. Standard library only. ASCII only.
"""
import json
import os
import re

import playtests as pt

SCHEMA = 1
DATA_REL = os.path.join("testing", "feature-ideas.json")
QUEUE_REL = os.path.join("docs", "feature-queue.md")

AREAS = ("crafting", "combat", "skills", "guilds", "League", "companions", "world", "client/UI", "staff tools", "other")
# Status keys and the words the page shows for them.
STATUSES = {"new": "new", "taken": "taken to features chat", "became": "became F-NN", "declined": "declined"}
FEATURE_RE = re.compile(r"^F-\d+$")
PLAYTEST_RE = re.compile(r"^(P\d+-\d+|T-\d{3}|M-\d{3,})$")

LIMITS = {"title": 140, "description": 2000, "reason": 300}


# --- the store ----------------------------------------------------------------------------------

def new_doc():
    # cc-P97: 'deleted' keeps each deleted idea's id, title and reason (a delete needs one), and 'copiedAt' is when the
    # copied ideas were last marked taken, so "Copy new ideas" can list what was declined or deleted since.
    return {"schema": SCHEMA, "nextId": 1, "copiedAt": "", "ideas": [], "deleted": []}


def new_idea(**kw):
    idea = {"id": "", "title": "", "description": "", "area": "", "playtest": "", "status": "new", "feature": "",
            "reason": "", "by": "", "createdAt": "", "updatedAt": "", "statusAt": ""}
    idea.update(kw)
    return idea


def ordered_idea(it):
    base = new_idea()
    return {k: it.get(k, base[k]) for k in base}


def ordered_deleted(d):
    return {k: d.get(k, "") for k in ("id", "title", "reason", "by", "deletedAt")}


def ordered_doc(doc):
    ideas = sorted((ordered_idea(i) for i in doc.get("ideas", [])), key=lambda i: int(i["id"][2:]))
    gone = sorted((ordered_deleted(d) for d in doc.get("deleted", [])), key=lambda d: int(d["id"][2:]))
    return {"schema": SCHEMA, "nextId": int(doc.get("nextId") or 1), "copiedAt": doc.get("copiedAt", ""),
            "ideas": ideas, "deleted": gone}


def path_of(root):
    return os.path.join(root, DATA_REL)


def load(root):
    path = path_of(root)
    if not os.path.exists(path):
        return new_doc()
    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("schema") != SCHEMA:
        raise RuntimeError("feature-ideas.json schema %r is not %d" % (doc.get("schema"), SCHEMA))
    for k, v in new_doc().items():
        doc.setdefault(k, v)
    # The counter can never fall behind an id that exists (a hand-edited file, say).
    used = [int(i["id"][2:]) for i in doc["ideas"] + doc["deleted"] if re.match(r"^I-\d+$", i.get("id", ""))]
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


def find(doc, idea_id):
    for it in doc["ideas"]:
        if it["id"] == idea_id:
            return it
    raise KeyError(idea_id)


def summary(doc):
    count = {k: 0 for k in STATUSES}
    for it in doc["ideas"]:
        count[it["status"]] = count.get(it["status"], 0) + 1
    return {"new": count["new"], "taken": count["taken"], "became": count["became"], "declined": count["declined"],
            "total": len(doc["ideas"])}


# --- checks ---------------------------------------------------------------------------------------

def clean_fields(title=None, description=None, area=None, playtest=None):
    out = {}
    if title is not None:
        t = pt.norm(title)[:LIMITS["title"]]
        if not t:
            raise ValueError("an idea needs a title")
        out["title"] = t
    if description is not None:
        # Line breaks are kept (a description can be a short list); runs of spaces inside a line are not.
        lines = [re.sub(r"[ \t]+", " ", l).strip() for l in str(description).replace("\r\n", "\n").split("\n")]
        out["description"] = "\n".join(lines).strip()[:LIMITS["description"]]
    if area is not None:
        a = pt.norm(area)
        if a and a not in AREAS:
            raise ValueError("area must be one of: " + ", ".join(AREAS))
        out["area"] = a
    if playtest is not None:
        p = pt.norm(playtest)
        if p and not PLAYTEST_RE.match(p):
            raise ValueError("a linked play test looks like P71-3, T-012 or M-001")
        out["playtest"] = p
    return out


# --- the actions ------------------------------------------------------------------------------------

def add(root, title, description="", area="", playtest="", by=""):
    fields = clean_fields(title, description, area, playtest)

    def fn(doc):
        iid = "I-%03d" % doc["nextId"]
        doc["nextId"] += 1
        stamp = pt.now_iso()
        # cc-P105: by is the writer identity (Cloudflare Access when on), empty otherwise.
        doc["ideas"].append(new_idea(id=iid, createdAt=stamp, updatedAt=stamp, by=pt.norm(by)[:60], **fields))
        return dict(doc["ideas"][-1])
    return update(root, fn)


def edit(root, idea_id, title=None, description=None, area=None, playtest=None):
    fields = clean_fields(title, description, area, playtest)

    def fn(doc):
        it = find(doc, idea_id)
        it.update(fields)
        it["updatedAt"] = pt.now_iso()
        return dict(it)
    return update(root, fn)


def set_status(root, idea_id, status, feature="", reason=""):
    if status not in STATUSES:
        raise ValueError("status must be one of: " + ", ".join(STATUSES))
    feature = pt.norm(feature).upper()
    reason = pt.norm(reason)[:LIMITS["reason"]]
    if status == "became" and not FEATURE_RE.match(feature):
        raise ValueError("'became F-NN' needs the F-number, for example F-44")
    if status == "declined" and not reason:
        raise ValueError("a declined idea needs a one-line reason")

    def fn(doc):
        it = find(doc, idea_id)
        stamp = pt.now_iso()
        it.update(status=status, feature=feature if status == "became" else "", reason=reason if status == "declined" else "",
                  statusAt=stamp, updatedAt=stamp)
        return dict(it)
    return update(root, fn)


def mark_taken(root, ids):
    """The ideas copied for the features chat: each one still 'new' becomes 'taken'. Others are left alone."""
    ids = [pt.norm(i) for i in ids]

    def fn(doc):
        stamp = pt.now_iso()
        done = []
        for it in doc["ideas"]:
            if it["id"] in ids and it["status"] == "new":
                it.update(status="taken", statusAt=stamp, updatedAt=stamp)
                done.append(it["id"])
        doc["copiedAt"] = stamp
        return done
    return update(root, fn)


def delete(root, idea_id, reason, by=""):
    """Removes the idea. cc-P97: only with a one-line reason, kept with its id and title under 'deleted' ("otherwise
    someone (me) will forget why we didn't go with that idea", Chase, Q17). nextId is untouched, so the id is never
    handed out again."""
    reason = pt.norm(reason)[:LIMITS["reason"]]
    if not reason:
        raise ValueError("deleting an idea needs a one-line reason")

    def fn(doc):
        it = find(doc, idea_id)
        doc["ideas"].remove(it)
        doc["deleted"].append({"id": it["id"], "title": it["title"], "reason": reason, "by": pt.norm(by)[:60],
                               "deletedAt": pt.now_iso()})
        return it["id"]
    return update(root, fn)


# --- for the features chat ----------------------------------------------------------------------------

def copy_text(doc, playtests=None):
    """Every 'new' idea as plain text, oldest first, one block per idea, ready to paste into the features chat.

        I-003: Bank deposit from the pack
        Area: crafting
        Linked play test: P71-3 (Fill a BOD from the backpack)
        Description:
          Two lines
          of text
    A missing area or play test says "(none)"; a missing description says "(none)" on the Description line."""
    titles = {}
    for it in (playtests or {}).get("items", []):
        titles[it["id"]] = it.get("label") or it.get("what") or it.get("text") or ""
    blocks = []
    for it in sorted((i for i in doc["ideas"] if i["status"] == "new"), key=lambda i: int(i["id"][2:])):
        pl = it["playtest"] or "(none)"
        if it["playtest"] and titles.get(it["playtest"]):
            pl += " (" + pt.norm(titles[it["playtest"]])[:100] + ")"
        lines = ["%s: %s" % (it["id"], it["title"]), "Area: " + (it["area"] or "(none)"), "Linked play test: " + pl]
        if it["description"]:
            lines.append("Description:")
            lines += ["  " + l for l in it["description"].split("\n")]
        else:
            lines.append("Description: (none)")
        blocks.append("\n".join(lines))
    # cc-P97: what was declined or deleted since the copied ideas were last marked taken, each with its reason. An
    # idea declined before reasons were required says so rather than nothing.
    since = doc.get("copiedAt", "")
    closed = []
    for it in doc["ideas"]:
        if it["status"] == "declined" and it.get("statusAt", "") > since:
            closed.append((it["id"], "declined", it["title"], it.get("reason", "")))
    for d in doc.get("deleted", []):
        if d.get("deletedAt", "") > since:
            closed.append((d["id"], "deleted", d.get("title", ""), d.get("reason", "")))
    closed.sort(key=lambda c: int(c[0][2:]))
    if not blocks and not closed:
        return ""
    out = ""
    if blocks:
        head = "New feature ideas from the play-test page (%d), for F-numbers or a decline:" % len(blocks)
        out = head + "\n\n" + "\n\n".join(blocks) + "\n"
    if closed:
        out += ("\n" if out else "") + "Declined or deleted since the last copy (%d):\n" % len(closed)
        out += "".join("%s (%s): %s\n  Reason: %s\n" % (c[0], c[1], c[2], c[3] or "no reason recorded") for c in closed)
    return out


# --- the real feature queue, read only ------------------------------------------------------------------

F_HEAD = re.compile(r"^###\s+(F-\d+):\s*(.*?)\s*$")
ADDED = re.compile(r"\s*\(([^()]*?\badded\s+(\d{4}-\d{2}-\d{2})[^()]*)\)\s*$")
TABLE_ROW = re.compile(r"^\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")


def parse_feature_queue(text):
    """docs/feature-queue.md's F-NN entries, each with the section it sits under.

    - '### F-NN: title (added YYYY-MM-DD)' headings, under whichever '## ' heading holds them (today only 'Open').
      The parenthesis is dropped from the title; its date is 'added'. '(planned, added ...)' and
      '(added ..., was: ...)' are read the same way.
    - The 'Batched' table: every F-NN in a row's first cell is marked batched, with the prompt from the second cell.
      An entry can be under Open and batched at once (the file keeps some under Open while questions stand).
    - The 'Dropped' table: an F-NN with no heading of its own becomes an entry in section 'Dropped', titled with the
      first sentence of its reason.
    Returns a list sorted by number."""
    entries = {}
    section = ""
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        h = F_HEAD.match(line)
        if h:
            fid, title = h.group(1), h.group(2)
            added = ""
            m = ADDED.search(title)
            if m:
                added = m.group(2)
                title = title[:m.start()].rstrip()
            entries[fid] = {"id": fid, "title": title, "added": added, "section": section, "batched": []}
            continue
        r = TABLE_ROW.match(line)
        if not r or section not in ("Batched", "Dropped") or r.group(1) in ("ID", "") or set(r.group(1)) <= set("-: "):
            continue
        ids = re.findall(r"\bF-\d+\b", r.group(1))
        for fid in ids:
            e = entries.get(fid)
            if section == "Batched":
                if e is None:
                    e = entries[fid] = {"id": fid, "title": "", "added": "", "section": "Batched", "batched": []}
                prompt = r.group(2)
                if prompt and prompt not in e["batched"]:
                    e["batched"].append(prompt)
            elif e is None:
                why = re.split(r"(?<=[.!?])\s", r.group(2), maxsplit=1)[0].rstrip(".")
                entries[fid] = {"id": fid, "title": why, "added": "", "section": "Dropped", "batched": []}
            else:
                e["section"] = "Dropped"
    return sorted(entries.values(), key=lambda e: int(e["id"][2:]))


def read_feature_queue(root):
    path = os.path.join(root, QUEUE_REL)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return parse_feature_queue(f.read())
    except OSError:
        return []


def section_counts(features):
    out = {}
    for e in features:
        out[e["section"]] = out.get(e["section"], 0) + 1
    return out
