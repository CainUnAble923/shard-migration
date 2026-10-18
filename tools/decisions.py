"""cc-P146: Chase's decisions as items on the play-test page, answered there.

Every notes file's "Deviations and decisions for Chase" (or "Decisions for Chase", "Open questions") section is read
into one item per numbered (or, with no numbers, bulleted) entry: P77-D3 is the third decision in P77's notes. Three
sources are merged each time the page asks (/api/items), like tools/playwho.py, so a new prompt's decisions appear with
no one doing anything:

  notes/cc-P<nn>-*.md              the sections, parsed here (parse_notes). A prompt imports once its notes end DONE.
  testing/decisions-overlay.json   hand-written, checked in: which older prompts are only "noted" (their deviations
                                   were never asked as questions), the wording, options and default for a decision where
                                   the parse is not enough, sections that are prose and were split by hand, answers given
                                   elsewhere (with the source), moot ones (with the reason), and the play-test items each
                                   prompt's decisions replace on the page. The importer never writes it.
  testing/decisions.json           the answers given on the page, with who and when, and the overseer's "taken into
                                   P<nn>". Written only here (atomically, under its own lock), exported with the other
                                   marks (tools/opsdata.py), so the next commit carries them into the repo.

A decision's state: open (asked, no answer), later ("ask me later"), answered (on the page; changeable until taken),
taken (the overseer took the answer into a prompt), elsewhere (answered outside the page: the source says where),
moot (the reason says why), noted (an older deviation that was never put as a question).

Standard library only (python:3-alpine runs it). ASCII only.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import playtests as pt  # noqa: E402

SCHEMA = 1
DATA_REL = os.path.join("testing", "decisions.json")
OVERLAY_REL = os.path.join("testing", "decisions-overlay.json")
NOTES_URL = "https://github.com/CainUnAble923/shard-migration/blob/main/"

STATES = ("open", "later", "answered", "taken", "elsewhere", "moot", "noted")
ACTIVE = ("open", "later", "answered")      # the default view (Open) shows these
ASKING = ("open", "later")                  # these need Chase: You decide, and Mine
LABELS = {"open": "open", "later": "ask me later", "answered": "answered", "taken": "taken", "elsewhere": "answered elsewhere",
          "moot": "moot", "noted": "noted, not asked"}
TAKEN_RE = re.compile(r"^P\d+$")
LIMITS = {"text": 2000, "question": 600}

SECTION = re.compile(r"(?i)\b(deviations and decisions for chase|decisions for chase|open questions)\b")
NUMBERED = re.compile(r"^(\d+)[.)]\s+(.*)$")
BULLET = re.compile(r"^[-*]\s+(.*)$")
SUB = re.compile(r"^\s+(?:[-*]|\d+[.)])\s+(.*)$")
OPTIONS_LEAD = re.compile(r"(?i)\boptions?\b|\bpick\b|\bchoose\b|\beither\b|:\s*$")
RECOMMEND = re.compile(r"(?i)\brecommended\b\s*(?:is|:)?\s*([^.;]*)|\bI recommend\s+([^.;]*)")
BUILT_WORDS = re.compile(r"(?i)\bplaceholders?\b|\buntil then\b|\bfor now\b|\bdefaults? taken\b|\bas built\b|\bkept the\b")
DEFAULT_RE = re.compile(r"(?i)\b(?:the )?default(?: is|:)\s*([^.;]*)")


# --- reading the notes -------------------------------------------------------------------------------

def slug(heading):
    """GitHub's anchor for a heading: lower case, punctuation dropped, spaces to hyphens."""
    s = re.sub(r"[^a-z0-9 _-]", "", heading.strip().lower())
    return s.replace(" ", "-")


def sentences(text, n):
    """The first n sentences of text, and the rest."""
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z*`\"(])", text.strip())
    return " ".join(parts[:n]).strip(), " ".join(parts[n:]).strip()


def first_sentence(text):
    return sentences(text, 1)[0].rstrip(";.,")


def parse_notes(text, num):
    """The decisions in one notes file, in file order: [{id, prompt, number, section, anchor, question, detail,
    options, built, recommended, default}]. A file with no such section gives []."""
    lines = text.splitlines()
    out = []
    nxt = 1
    i = 0
    while i < len(lines):
        h = pt.HEADING.match(lines[i])
        if not (h and SECTION.search(h.group(2))):
            i += 1
            continue
        level, heading = len(h.group(1)), h.group(2).strip()
        body = []
        i += 1
        while i < len(lines):
            h2 = pt.HEADING.match(lines[i])
            if (h2 and len(h2.group(1)) <= level) or lines[i].strip() == "P%d DONE" % num:
                break
            body.append(lines[i])
            i += 1
        built_section = bool(re.search(r"(?i)deviations|defaults taken", heading))
        for entry in split_entries(body):
            n = entry["own"] if entry["own"] and entry["own"] >= nxt else nxt
            nxt = n + 1
            out.append(shape(entry, "P%d" % num, n, heading, built_section))
    return out


def split_entries(body):
    """Top-level numbered entries, or top-level bullets when the section has no numbers. Each: {own, main, subs,
    extra}: main is the entry's own paragraph, subs its nested list items, extra any later paragraph or code."""
    numbered = any(NUMBERED.match(l) for l in body)
    top = NUMBERED if numbered else BULLET
    entries, cur, fence, gap = [], None, False, False
    for l in body:
        s = l.strip()
        if s.startswith("```"):
            fence = not fence
            if cur is not None:
                cur["extra"].append(l)
            continue
        if fence:
            if cur is not None:
                cur["extra"].append(l)
            continue
        if not s:
            gap = True
            continue
        m = top.match(l)
        if m:
            cur = {"own": int(m.group(1)) if numbered else 0, "main": m.group(2 if numbered else 1).strip(), "subs": [],
                   "extra": []}
            entries.append(cur)
            gap = False
            continue
        if cur is None:
            continue                    # an introduction before the first entry
        sm = SUB.match(l)
        if sm:
            cur["subs"].append(sm.group(1).strip())
        elif l[:1] in (" ", "\t") and cur["subs"] and not gap:
            cur["subs"][-1] += " " + s  # a nested item's continuation
        elif l[:1] in (" ", "\t") and not gap and not cur["extra"]:
            cur["main"] += " " + s
        else:
            cur["extra"].append(s)
        gap = False
    return entries


def shape(entry, prompt, number, heading, built_section):
    main = pt.norm(entry["main"])
    # A bold lead-in ("**Currency name:**") is a label, not one of the two sentences.
    lead = re.match(r"^(\*\*[^*]+\*\*:?)\s*(.*)$", main)
    label, body = (lead.group(1), lead.group(2)) if lead else ("", main)
    question, rest = sentences(body, 2)
    if len(question) > 320:
        question, rest = sentences(body, 1)[0], body[len(sentences(body, 1)[0]):].strip()
    question = (label + ("" if question[:1] in ",.;:)" else " ") + question).strip()
    options = []
    if len(entry["subs"]) >= 2 and OPTIONS_LEAD.search(main):
        for s in entry["subs"]:
            label = re.sub(r"(?i)^or\s+", "", first_sentence(pt.norm(s)))[:160]
            mark = "recommended" if re.search(r"(?i)\brecommended\b", s) else ("built" if re.search(r"(?i)\b(built|today|current)\b", s) else "")
            options.append({"label": label, "mark": mark})
        subs_detail = []
    else:
        subs_detail = ["- " + pt.norm(s) for s in entry["subs"]]
    alltext = " ".join([main] + entry["subs"] + entry["extra"])
    rec = RECOMMEND.search(alltext)
    recommended = pt.norm((rec.group(1) or rec.group(2) or "")) if rec else ""
    d = DEFAULT_RE.search(alltext)
    detail = "\n".join([x for x in [rest] if x] + subs_detail + [pt.norm(x) for x in entry["extra"] if x.strip()])
    return {"id": "%s-D%d" % (prompt, number), "prompt": prompt, "number": number, "section": heading,
            "anchor": slug(heading), "question": question, "detail": detail.strip(), "options": options,
            "built": built_section or bool(BUILT_WORDS.search(alltext)), "recommended": recommended,
            "default": pt.norm(d.group(1)) if d else ""}


def read_all_notes(root, first=pt.FIRST_PROMPT):
    """{prompt: (notes file name, [decisions])} for every DONE notes file from P<first> on. Parsed files are cached by
    modification time and size."""
    out = {}
    try:
        names = pt.notes_files(root)
    except OSError:
        return out
    for num, name in names:
        if num < first:
            continue
        path = os.path.join(root, pt.NOTES_REL, name)
        parsed = _cached(path, lambda text, num=num: parse_notes(text, num) if pt.is_done(text, num) else None)
        if parsed is not None:
            out["P%d" % num] = (name, parsed)
    return out


_CACHE = {}


def _cached(path, parse):
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


def load_overlay(roots):
    """The overlay from the first root that has it (on Haven the notes clone comes first, as for the triage)."""
    for r in roots:
        if not r:
            continue
        v = _cached(os.path.join(r, OVERLAY_REL), json.loads)
        if isinstance(v, dict):
            return v
    return None


# --- building the list -------------------------------------------------------------------------------

def build(notes, overlay, store):
    """Every decision item, with its state. notes: read_all_notes(); overlay: load_overlay() or None; store: load()."""
    ov = overlay or {}
    over = ov.get("decisions") or {}
    noted = set(ov.get("notAsked") or [])
    base = ov.get("notesUrl") or NOTES_URL
    answers = (store or {}).get("answers") or {}
    out, seen = [], set()

    def finish(d, name):
        o = over.get(d["id"]) or {}
        for k in ("question", "detail", "options", "built", "recommended", "default", "section", "anchor"):
            if k in o:
                d[k] = o[k]
        if name and not d.get("link"):
            d["link"] = base + "notes/" + name + ("#" + d["anchor"] if d.get("anchor") else "")
        d["notesFile"] = "notes/" + name if name else d.get("notesFile", "")
        state = o.get("status") or ("noted" if d["prompt"] in noted else "open")
        d.update(source=o.get("source", ""), reason=o.get("reason", ""), elsewhere=o.get("answer", ""))
        a = answers.get(d["id"])
        if a and state != "moot":
            state = a["status"]
            d["answer"] = {k: a.get(k, "") for k in ("choice", "text", "by", "at", "takenInto", "takenAt", "takenBy")}
        d["state"] = state if state in STATES else "open"
        d["stateLabel"] = LABELS[d["state"]]
        d["kind"] = "decision"
        out.append(d)
        seen.add(d["id"])

    for prompt in sorted(notes, key=lambda p: int(p[1:])):
        name, items = notes[prompt]
        for d in items:
            finish(dict(d), name)
    # Hand-split items: prose sections, and decisions that live somewhere other than a notes section.
    for did, o in sorted(over.items(), key=lambda kv: natural(kv[0])):
        if did in seen or not o.get("question"):
            continue
        prompt = o.get("prompt") or did.rsplit("-D", 1)[0]
        name = o.get("notesFile", "").replace("notes/", "", 1) if o.get("notesFile", "").startswith("notes/") else ""
        if not name and prompt in notes:
            name = notes[prompt][0]
        d = {"id": did, "prompt": prompt, "number": int(re.sub(r"\D", "", did.rsplit("-D", 1)[-1]) or 0),
             "section": o.get("section", ""), "anchor": o.get("anchor", slug(o.get("section", ""))), "question": "",
             "detail": "", "options": [], "built": False, "recommended": "", "default": "", "split": True,
             "link": o.get("link", ""), "notesFile": o.get("notesFile", "")}
        finish(d, name)
    for d in out:
        d.setdefault("split", False)
        d["who"] = {"key": "decide", "label": "You decide", "kind": "a choice for you", "bucket": "DECISION", "reason": ""}
        d["where"] = {"key": "questions", "label": WHERE_QUESTIONS, "chars": []}
        d["status"] = d["state"]
        d["group"] = d["prompt"]
    return out


WHERE_QUESTIONS = "Questions"


def natural(did):
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", did)]


def replaced_items(overlay, decisions):
    """{play-test item id: [decision ids]} from the overlay's 'replaces': a prompt ("P77") means all of its decisions
    that are not 'noted'; a list names them."""
    by_prompt = {}
    for d in decisions:
        if d["state"] != "noted":
            by_prompt.setdefault(d["prompt"], []).append(d["id"])
    out = {}
    for iid, what in ((overlay or {}).get("replaces") or {}).items():
        out[iid] = list(what) if isinstance(what, list) else by_prompt.get(what, [])
    return out


def annotate(doc, decisions, overlay):
    """After playwho.annotate: the decisions go in doc["decisions"]; each play-test item they replace gets replacedBy
    and leaves the Who counts and the open count; You decide counts the decisions still asking; doc["answers"]
    counts the answers given on the page and not yet taken."""
    doc["decisions"] = decisions
    rep = replaced_items(overlay, decisions)
    who = doc.get("who") or {}
    counts = who.get("counts")
    gone = 0
    for it in doc.get("items", []):
        r = rep.get(it["id"])
        if r is None or it.get("status") not in pt.OPEN_STATUSES:
            continue
        it["replacedBy"] = r
        gone += 1
        if counts is not None and it.get("who"):
            counts[it["who"]["key"]] -= 1
    asking = sum(1 for d in decisions if d["state"] in ASKING)
    if counts is not None:
        counts["decide"] = counts.get("decide", 0) + asking
        who["mine"] = sum(counts[k] for k in ("you", "botyou", "decide"))
    if "summary" in doc:
        doc["summary"] = dict(doc["summary"], replaced=gone)
    tally = dict.fromkeys(STATES, 0)
    for d in decisions:
        tally[d["state"]] += 1
    doc["answers"] = {"new": tally["answered"], "states": tally, "total": len(decisions),
                      "replaced": sorted(i for i in rep if any(x["id"] == i for x in doc.get("items", [])))}
    return doc


# --- the answers store ---------------------------------------------------------------------------------

def new_doc():
    return {"schema": SCHEMA, "answers": {}}


def ordered_answer(a):
    keys = ("id", "prompt", "question", "choice", "text", "status", "by", "at", "takenInto", "takenAt", "takenBy",
            "history")
    out = {k: a.get(k, [] if k == "history" else "") for k in keys}
    out["history"] = [{k: h.get(k, "") for k in ("choice", "text", "status", "by", "at")} for h in out["history"]]
    return out


def ordered_doc(doc):
    return {"schema": SCHEMA,
            "answers": {k: ordered_answer(doc["answers"][k]) for k in sorted(doc.get("answers", {}), key=natural)}}


def path_of(data):
    return os.path.join(data, DATA_REL)


def load(data):
    path = path_of(data)
    if not os.path.exists(path):
        return new_doc()
    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("schema") != SCHEMA:
        raise RuntimeError("decisions.json schema %r is not %d" % (doc.get("schema"), SCHEMA))
    doc.setdefault("answers", {})
    return doc


def save(data, doc):
    path = path_of(data)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    final = ordered_doc(doc)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="ascii", newline="\n") as f:
        f.write(json.dumps(final, indent=2, ensure_ascii=True) + "\n")
    os.replace(tmp, path)
    return final


def update(data, fn):
    with pt.Lock(path_of(data)):
        doc = load(data)
        value = fn(doc)
        save(data, doc)
    return value


def _record(doc, decision):
    a = doc["answers"].get(decision["id"])
    if a is None:
        a = doc["answers"][decision["id"]] = {"id": decision["id"], "prompt": decision["prompt"], "history": []}
    elif a.get("status") == "taken":
        raise ValueError("%s was taken into %s; it can no longer be changed here" % (decision["id"], a.get("takenInto")))
    if a.get("status"):
        a["history"].append({k: a.get(k, "") for k in ("choice", "text", "status", "by", "at")})
    a["question"] = pt.norm(decision.get("question", ""))[:LIMITS["question"]]
    return a


def answer(data, decision, choice="", text="", by=""):
    """Save an answer: one of the decision's option labels, "built" (keep what's built), and/or free text."""
    choice = pt.norm(choice)
    text = str(text or "").replace("\r\n", "\n").strip()[:LIMITS["text"]]
    allowed = [o["label"] for o in decision.get("options") or []] + (["built"] if decision.get("built") else [])
    if choice and choice not in allowed:
        raise ValueError("choose one of the options shown" + (" or keep what's built" if decision.get("built") else ""))
    if not choice and not text:
        raise ValueError("pick an option or write an answer")
    if decision.get("state") == "moot":
        raise ValueError("%s is moot: %s" % (decision["id"], decision.get("reason", "")))

    def fn(doc):
        a = _record(doc, decision)
        a.update(choice=choice, text=text, status="answered", by=pt.norm(by)[:60], at=pt.now_iso())
        return ordered_answer(a)
    return update(data, fn)


def later(data, decision, by=""):
    """"Ask me later": no answer, and the card says so."""
    def fn(doc):
        a = _record(doc, decision)
        a.update(choice="", text="", status="later", by=pt.norm(by)[:60], at=pt.now_iso())
        return ordered_answer(a)
    return update(data, fn)


def mark_taken(data, ids, prompt, by="", undo=False):
    """The overseer took these answers into prompt P<nn> (each 'answered' one becomes 'taken'); undo puts a taken one
    back to 'answered'. Others are left alone. Returns the ids changed."""
    prompt = pt.norm(prompt).upper()
    if not undo and not TAKEN_RE.match(prompt):
        raise ValueError("say which prompt took them, for example P150")
    ids = [pt.norm(i) for i in ids]

    def fn(doc):
        done = []
        for i in ids:
            a = doc["answers"].get(i)
            if a is None:
                continue
            if not undo and a.get("status") == "answered":
                a.update(status="taken", takenInto=prompt, takenAt=pt.now_iso(), takenBy=pt.norm(by)[:60])
                done.append(i)
            elif undo and a.get("status") == "taken":
                a.update(status="answered", takenInto="", takenAt="", takenBy="")
                done.append(i)
        return done
    return update(data, fn)


def find(decisions, did):
    for d in decisions:
        if d["id"] == did:
            return d
    raise KeyError(did)


def copy_text(decisions):
    """The answers given on the page and not yet taken, as plain text for the overseer, oldest prompt first."""
    rows = [d for d in decisions if d["state"] == "answered"]
    if not rows:
        return ""
    out = ["New answers from the play-test page (%d), for the next prompt:" % len(rows), ""]
    for d in rows:
        a = d.get("answer") or {}
        pick = "Keep what's built" if a.get("choice") == "built" else a.get("choice", "")
        out.append("%s: %s" % (d["id"], d["question"]))
        if pick:
            out.append("  Choice: " + pick)
        if a.get("text"):
            out += ["  Answer: " + l for l in a["text"].split("\n")]
        out.append("  By %s at %s. Detail: %s" % (a.get("by") or "(no sign-in)", a.get("at", ""), d.get("link", "")))
        out.append("")
    return "\n".join(out)


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="cc-P146: the decision items and their answers")
    ap.add_argument("cmd", choices=("list", "answers"))
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--prompt", default="")
    a = ap.parse_args(argv)
    ds = build(read_all_notes(a.root), load_overlay([a.root]), load(a.root))
    if a.cmd == "answers":
        print(copy_text(ds) or "No new answers.")
        return 0
    for d in ds:
        if a.prompt and d["prompt"] != a.prompt:
            continue
        print("%-10s %-10s %s" % (d["id"], d["state"], d["question"][:110]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
