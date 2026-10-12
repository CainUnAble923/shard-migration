"""Play-test queue: the one place the parsing and merging logic lives (cc-P83).

Used two ways, so the rules cannot drift:
  - tools/Import-PlayTests.ps1 runs `python playtests.py import --root D:\\UO\\shard-migration` on the host.
  - docker/test-queue/server.py (D:\\ShatteredLegacy) imports this file and calls import_all() on start and
    every 60 s, so a prompt whose notes end "Pnn DONE" shows up on the page within a minute.

The data is testing/play-tests.json under the root (agents never edit docs/, so it is not there). It is
pretty-printed with a fixed key order so git diffs read, and written atomically (temp file + rename) under
a lock file that both the host importer and the container honour. testing/SUMMARY.md is rewritten with it.

Standard library only (python:3-alpine runs it). ASCII only.
"""
import datetime
import hashlib
import json
import os
import re
import sys
import time

SCHEMA = 1
FIRST_PROMPT = 56          # P56 is the first prompt of the backlog this queue starts from (cc-P83)
DATA_REL = os.path.join("testing", "play-tests.json")
SUMMARY_REL = os.path.join("testing", "SUMMARY.md")
QUEUE_DOC_REL = os.path.join("docs", "client-test-queue.md")
NOTES_REL = "notes"

STATUSES = ("open", "pass", "fail", "later", "blocked", "moot")
OPEN_STATUSES = ("open", "later", "blocked")
SET_STATUSES = ("open", "pass", "fail", "later")

# --- extraction rules ---------------------------------------------------------------------------
# A notes file imports only when its last non-blank line is exactly "Pnn DONE".
# Its checklist is the list under the "For Chase" heading (exactly that heading; "Decisions for
# Chase" and "Deviations and decisions for Chase" are not checklists). Inside it, a line that is not
# a list item (a "marker", e.g. "In game on the test shard:" or "**Deploy:**") sets what the items
# after it are:
MARKER_TEST = re.compile(r"(?i)\bin[- ]game\b|\bchecklist\b|\bto try it\b|\bto run\b|\bhow to use\b|\bin the client\b")
MARKER_DEPLOY = re.compile(r"(?i)\bdeploy\b|\bpackage first\b|\bcommit\b|\bbuild\b|\bpublish\b|\brestart the test shard\b")
# Any other marker ("**If it goes wrong:**", "**Promote to docs:**", "**Bugs in ...**") ends the test
# items until the next test marker. Before any marker, items count as tests but are flagged
# "unmarked" (P60, P63, P68 list console checks with no heading).
# And whatever the marker said, an item that is a deploy, commit or docs step is never a play-test:
NOT_A_TEST = re.compile(
    r"(?i)^\s*(\*\*)?(commit|push|promote|deploy|build the package|publish|get it onto|put `?sl-modernuo|package first|"
    r"decide|before you leave|to undo)\b"
    r"|docker tag |Start-TestShard\.ps1|Build-PlayerPackage\.ps1|Publish-PlayerPackage\.ps1|Commit-ShardWork\.ps1"
    r"|\bpromote to `?docs")

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
FOR_CHASE = re.compile(r"(?i)^(\d+\.\s+)?for chase$")
LIST_ITEM = re.compile(r"^(\s*)(\d+[.)]|[-*])\s+(\[[ xX]\]\s+)?(.*)$")
VERSION_RE = (re.compile(r"`?\[version`?\s+(?:shows|says)\s+\"?(?:Shattered Legacy\s+)?(\d{4}\.\d{2}\.\d{2}(?:\.\d+)?)"),
              re.compile(r"\[ShardVersion\]\s+Shattered Legacy\s+(\d{4}\.\d{2}\.\d{2}(?:\.\d+)?)"))
TITLE_RE = re.compile(r"^#\s+(.*)$", re.M)


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm(text):
    return re.sub(r"\s+", " ", text or "").strip()


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def is_done(text, num):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return bool(lines) and lines[-1] == "P%d DONE" % num


def split_what_expect(text):
    """'**Label (D77):** do this: see that' -> (label, do this, see that). The split is the first ': '
    outside backticks and quotes after the label; with none, the whole step is what to do."""
    label = ""
    m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", text)
    if m and m.group(1).rstrip().endswith(":"):
        label = m.group(1).rstrip().rstrip(":").strip()
        text = m.group(2)
    elif m and m.group(2).startswith(":"):
        label = m.group(1).strip()
        text = m.group(2)[1:].strip()
    first = True
    while True:
        i = first_split(text)
        if i < 0:
            return label, text.strip(), ""
        what, rest = text[:i].strip(), text[i + 1:].strip()
        # "Hiding: set Hiding 150, ...: expected" -- a short lead-in with no command in it is a label. With no
        # second split after it ("Stable slots: Taming 200, then stable pets..."), the rest is the step, unsplit.
        if first and not label and len(what.split()) <= 4 and "`" not in what and "[" not in what:
            if first_split(rest) >= 0:
                label, text, first = what, rest, False
                continue
            return what, rest, ""
        return label, what, rest


def first_split(text):
    """Index of the first ': ' outside backticks, double quotes and parentheses, or -1."""
    tick = quote = False
    depth = 0
    for i, ch in enumerate(text):
        if ch == "`":
            tick = not tick
        elif tick:
            continue
        elif ch == '"':
            quote = not quote
        elif quote:
            continue
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif ch == ":" and depth == 0 and text[i + 1:i + 2] == " " and len(text[:i].strip()) >= 3:
            return i
    return -1


def parse_notes(text, num):
    """The checklist of one notes file. Returns a dict; items are play-test steps only."""
    out = {"prompt": "P%d" % num, "done": is_done(text, num), "title": "", "version": "", "items": [],
           "parsed": False, "skipped": [], "section": ""}
    t = TITLE_RE.search(text)
    if t:
        out["title"] = norm(t.group(1))
    for rx in VERSION_RE:
        v = rx.search(text)
        if v:
            out["version"] = v.group(1)
            break
    lines = text.splitlines()
    start = None
    level = 0
    for i, l in enumerate(lines):
        h = HEADING.match(l)
        if h and FOR_CHASE.match(h.group(2).strip()):
            start, level = i + 1, len(h.group(1))
            out["section"] = h.group(2).strip()
            break
    if start is None:
        return out
    body = []
    for l in lines[start:]:
        h = HEADING.match(l)
        if h and len(h.group(1)) <= level:
            break
        if l.strip() == "P%d DONE" % num:
            break
        body.append(l)

    mode = "unmarked"            # test (marked), unmarked (test, no heading seen), deploy, other
    fence = False
    cur = None
    raw = []                     # (mode, text)

    def close():
        if cur is not None:
            raw.append(cur)

    for l in body:
        s = l.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if not s:
            continue
        m = LIST_ITEM.match(l)
        if m and len(m.group(1)) == 0:
            close()
            cur = [mode, m.group(4).strip()]
            continue
        if l[:1] in (" ", "\t") and cur is not None:
            cur[1] += " " + s     # a continuation line or a nested item belongs to its parent step
            continue
        # a marker paragraph
        close()
        cur = None
        marker = s.replace("**", "")
        if MARKER_TEST.search(marker):
            mode = "test"
        elif MARKER_DEPLOY.search(marker):
            mode = "deploy"
        else:
            mode = "other"
    close()

    pos = 0
    for m, txt in raw:
        txt = norm(txt)
        if m in ("deploy", "other") or NOT_A_TEST.search(txt):
            out["skipped"].append({"why": "not a play-test (%s)" % ("deploy or docs step" if m == "deploy" or NOT_A_TEST.search(txt) else "under '%s'" % m), "text": txt})
            continue
        pos += 1
        label, what, expect = split_what_expect(txt)
        out["items"].append({"position": pos, "text": txt, "label": label, "what": what, "expect": expect,
                             "unmarked": m == "unmarked"})
    out["parsed"] = pos > 0
    return out


# --- the store ----------------------------------------------------------------------------------

def new_doc():
    return {"schema": SCHEMA, "summary": {}, "prompts": {}, "imports": {}, "items": []}


def new_item(**kw):
    item = {
        "id": "", "source": "", "prompt": "", "position": 0, "label": "", "what": "", "expect": "",
        "text": "", "version": "", "unmarked": False, "status": "open", "note": "", "resultAt": "",
        "bug": "", "textChanged": False, "previousText": "", "removedFromNotes": False, "addedAt": "",
    }
    item.update(kw)
    return item


def ordered_item(it):
    base = new_item()
    for k in list(base.keys()):
        if k in it:
            base[k] = it[k]
    return base


def compute_summary(doc):
    items = doc["items"]
    count = {s: 0 for s in STATUSES}
    for it in items:
        count[it["status"]] = count.get(it["status"], 0) + 1
    fails = [it for it in items if it["status"] == "fail"]
    return {
        "generatedAt": now_iso(),
        "open": sum(count[s] for s in OPEN_STATUSES),
        "failed": count["fail"],
        "passed": count["pass"],
        "later": count["later"],
        "blocked": count["blocked"],
        "moot": count["moot"],
        "total": len(items),
        "unloggedFails": sum(1 for it in fails if not it["bug"]),
        "failures": [{"id": it["id"], "prompt": it["prompt"], "source": it["source"], "what": it["what"] or it["text"], "note": it["note"],
                      "at": it["resultAt"], "bug": it["bug"]} for it in fails],
    }


def ordered_doc(doc):
    prompts = {}
    for k in sorted(doc.get("prompts", {}), key=lambda p: int(p[1:])):
        p = doc["prompts"][k]
        prompts[k] = {key: p.get(key, d) for key, d in (("notesFile", ""), ("title", ""), ("version", ""), ("sourceHash", ""),
                                                       ("importedAt", ""), ("updatedAt", ""), ("parsed", False), ("items", 0), ("skipped", 0))}
    return {"schema": SCHEMA, "summary": compute_summary(doc), "prompts": prompts,
            "imports": doc.get("imports", {}), "items": [ordered_item(i) for i in doc["items"]]}


class Lock(object):
    """A lock file beside the data. Both the host importer and the container use it, so two writers
    never interleave a read and a write. A lock older than STALE seconds is taken over."""
    STALE = 30.0

    def __init__(self, path, timeout=20.0):
        self.path = path + ".lock"
        self.timeout = timeout

    def __enter__(self):
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        end = time.time() + self.timeout
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode("ascii"))
                os.close(fd)
                return self
            except FileExistsError:
                try:
                    if time.time() - os.path.getmtime(self.path) > self.STALE:
                        os.remove(self.path)
                        continue
                except OSError:
                    pass
                if time.time() > end:
                    raise RuntimeError("play-tests.json is locked by another writer: " + self.path)
                time.sleep(0.05)

    def __exit__(self, *a):
        try:
            os.remove(self.path)
        except OSError:
            pass


def load(path):
    if not os.path.exists(path):
        return new_doc()
    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("schema") != SCHEMA:
        raise RuntimeError("play-tests.json schema %r is not %d" % (doc.get("schema"), SCHEMA))
    for k, v in new_doc().items():
        doc.setdefault(k, v)
    return doc


def render_summary_md(doc):
    s = doc["summary"]
    out = ["# Play tests: summary", "",
           "Regenerated on every write of `play-tests.json` (cc-P83). Do not edit; the page and the importer rewrite it.", "",
           "Generated %s: **%d open**, **%d failed** (%d not yet logged as a bug), **%d passed**, %d later, %d blocked, %d moot, %d in all." % (
               s["generatedAt"], s["open"], s["failed"], s["unloggedFails"], s["passed"], s["later"], s["blocked"], s["moot"], s["total"]),
           "", "## Failures", ""]
    if not s["failures"]:
        out.append("None.")
    for f in s["failures"]:
        out.append("- **%s** (%s, %s)%s: %s. Note: %s" % (f["id"], f["prompt"] or f.get("source", ""), f["at"] or "no time",
                                                     (" bug " + f["bug"]) if f["bug"] else " NOT LOGGED", f["what"], f["note"] or "(none)"))
    out += ["", "## Open, by prompt", ""]
    by = {}
    for it in doc["items"]:
        if it["status"] in OPEN_STATUSES:
            by.setdefault(it["prompt"] or it["source"], 0)
            by[it["prompt"] or it["source"]] += 1
    if not by:
        out.append("Nothing open.")
    for k in sorted(by, key=sort_key, reverse=True):
        out.append("- %s: %d" % (k, by[k]))
    return "\n".join(out) + "\n"


def sort_key(k):
    m = re.match(r"^P(\d+)$", k or "")
    if m:
        return (2, int(m.group(1)))
    return (1 if k == "manual" else 0, 0)


def save(root, doc):
    path = os.path.join(root, DATA_REL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    final = ordered_doc(doc)
    text = json.dumps(final, indent=2, ensure_ascii=True) + "\n"
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="ascii", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)
    md = os.path.join(root, SUMMARY_REL)
    with open(md + ".tmp", "w", encoding="ascii", newline="\n") as f:
        f.write(render_summary_md(final))
    os.replace(md + ".tmp", md)
    return final


def find_item(doc, item_id):
    for it in doc["items"]:
        if it["id"] == item_id:
            return it
    return None


# --- importing ------------------------------------------------------------------------------------

def notes_files(root):
    d = os.path.join(root, NOTES_REL)
    found = []
    for name in os.listdir(d):
        m = re.match(r"^cc-P(\d+)-.*\.md$", name)
        if m:
            found.append((int(m.group(1)), name))
    found.sort()
    return found


def merge_prompt(doc, parsed, notes_name, text_hash, log):
    p = parsed["prompt"]
    num = int(p[1:])
    stamp = now_iso()
    known = doc["prompts"].get(p)
    if known and known.get("sourceHash") == text_hash:
        return False
    items = parsed["items"]
    if not parsed["parsed"]:
        items = [{"position": 0, "text": "%s: checklist not parsed, read the notes (notes/%s)" % (p, notes_name), "label": "",
                  "what": "%s: checklist not parsed, read the notes" % p, "expect": "notes/" + notes_name, "unmarked": False}]
    existing = {it["id"]: it for it in doc["items"] if it["prompt"] == p and it["source"] == "notes"}
    seen = set()
    for st in items:
        iid = "%s-%d" % (p, st["position"])
        seen.add(iid)
        old = existing.get(iid)
        if old is None:
            doc["items"].append(new_item(id=iid, source="notes", prompt=p, position=st["position"], label=st["label"],
                                         what=st["what"], expect=st["expect"], text=st["text"], version=parsed["version"],
                                         unmarked=st["unmarked"], addedAt=stamp))
            log("added %s: %s" % (iid, st["what"][:90]))
        elif norm(old["text"]) != norm(st["text"]):
            # The checklist changed after import: the result is kept and the item is flagged.
            old["previousText"] = old["text"]
            old.update(text=st["text"], label=st["label"], what=st["what"], expect=st["expect"], textChanged=True,
                       removedFromNotes=False)
            log("text changed %s (result kept: %s)" % (iid, old["status"]))
        elif old.get("removedFromNotes"):
            old["removedFromNotes"] = False
        if old is not None and old.get("version") != parsed["version"] and parsed["version"]:
            old["version"] = parsed["version"]
    for iid, old in existing.items():
        if iid not in seen and not old.get("removedFromNotes"):
            old["removedFromNotes"] = True
            log("no longer in the notes %s (kept: %s)" % (iid, old["status"]))
    doc["prompts"][p] = {"notesFile": "notes/" + notes_name, "title": parsed["title"], "version": parsed["version"],
                         "sourceHash": text_hash, "importedAt": (known or {}).get("importedAt") or stamp,
                         "updatedAt": stamp, "parsed": parsed["parsed"], "items": len(parsed["items"]),
                         "skipped": len(parsed["skipped"])}
    return True


T_ROW = re.compile(r"^\|\s*(T-\d{3})\s*\|\s*([^|]*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")


def strip_md(s):
    return norm(s.replace("**", ""))


def import_client_queue(doc, root, log):
    """The T-rows of docs/client-test-queue.md, once. The .md file is never written."""
    if "clientTestQueue" in doc["imports"]:
        return False
    path = os.path.join(root, QUEUE_DOC_REL)
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    results = {}
    if "## Results" in text:
        last = None
        for l in text.split("## Results", 1)[1].splitlines():
            m = re.match(r"^- (T-\d{3}), (\d{4}-\d{2}-\d{2}):\s*(.*)$", l)
            if m:
                last = [m.group(2), m.group(3)]
                results.setdefault(m.group(1), []).append(last)
            elif last is not None and l[:1] == " " and l.strip():
                last[1] += " " + l.strip()      # a result line wrapped onto the next line
            else:
                last = None
    section = ""
    n = 0
    stamp = now_iso()
    have = {it["id"] for it in doc["items"]}
    for l in text.splitlines():
        if l.startswith("## "):
            section = l[3:].strip()
        m = T_ROW.match(l)
        if not m:
            continue
        tid, status_cell, check, how, ok, source = m.groups()
        word = re.sub(r"[^A-Z]", " ", status_cell.upper()).split()
        word = word[0] if word else "OPEN"
        status = {"OPEN": "open", "PASS": "pass", "PASSED": "pass", "FAIL": "fail", "BLOCKED": "blocked", "MOOT": "moot"}.get(word, "open")
        res = results.get(tid, [])
        note = ""
        bug = ""
        at = ""
        if res:
            at = res[0][0]
            if status == "fail":
                note = strip_md(res[0][1])[:300]
                b = re.search(r"\bD\d+\b", " ".join(r[1] for r in res))
                bug = b.group(0) if b else ""
        if tid in have:
            continue
        doc["items"].append(new_item(id=tid, source="client-test-queue", prompt="", label=strip_md(check), what=strip_md(how),
                                     expect=strip_md(ok), text=strip_md(" | ".join((check, how, ok, source))), status=status,
                                     note=note or ("" if status == "open" else "imported as %s from docs/client-test-queue.md" % word),
                                     resultAt=at, bug=bug, addedAt=stamp))
        n += 1
    doc["imports"]["clientTestQueue"] = {"file": "docs/client-test-queue.md", "importedAt": stamp, "rows": n}
    log("imported %d T-rows from docs/client-test-queue.md (once; the file itself is unchanged)" % n)
    return n > 0


def import_all(root, write=True, log=print, first=FIRST_PROMPT):
    """Scan notes, merge DONE checklists and the T-rows. Returns (changed, doc). Idempotent."""
    path = os.path.join(root, DATA_REL)

    def run():
        doc = load(path)
        changed = import_client_queue(doc, root, log)
        for num, name in notes_files(root):
            if num < first:
                continue
            with open(os.path.join(root, NOTES_REL, name), "r", encoding="utf-8") as f:
                text = f.read()
            parsed = parse_notes(text, num)
            if not parsed["done"]:
                if "P%d" % num not in doc["prompts"]:
                    log("skip P%d: notes do not end 'P%d DONE' (%s)" % (num, num, name))
                continue
            if merge_prompt(doc, parsed, name, sha(text), log):
                changed = True
        return changed, doc

    if not write:
        changed, doc = run()
        return changed, ordered_doc(doc)
    with Lock(path):
        changed, doc = run()
        if changed or not os.path.exists(path):
            doc = save(root, doc)
        else:
            doc = ordered_doc(doc)
    return changed, doc


def update(root, fn):
    """Read, change one thing, write, all under the lock. fn(doc) returns the value to hand back."""
    path = os.path.join(root, DATA_REL)
    with Lock(path):
        doc = load(path)
        value = fn(doc)
        save(root, doc)
    return value


def set_result(root, item_id, status, note=""):
    if status not in SET_STATUSES:
        raise ValueError("status must be one of " + ", ".join(SET_STATUSES))
    note = norm(note)[:500]
    if status == "fail" and not note:
        raise ValueError("a Fail needs a one-line note")

    def fn(doc):
        it = find_item(doc, item_id)
        if it is None:
            raise KeyError(item_id)
        it["status"] = status
        it["note"] = note if status in ("fail", "later", "pass") else ""
        it["resultAt"] = now_iso() if status != "open" else ""
        if status != "fail":
            it["bug"] = ""
        return dict(it)
    return update(root, fn)


def set_bug(root, item_id, bug):
    bug = norm(bug)[:40]

    def fn(doc):
        it = find_item(doc, item_id)
        if it is None:
            raise KeyError(item_id)
        it["bug"] = bug
        return dict(it)
    return update(root, fn)


def add_manual(root, what, expect=""):
    what = norm(what)[:500]
    if not what:
        raise ValueError("say what to test")

    def fn(doc):
        nums = [int(i["id"][2:]) for i in doc["items"] if re.match(r"^M-\d+$", i["id"])]
        iid = "M-%03d" % ((max(nums) if nums else 0) + 1)
        doc["items"].append(new_item(id=iid, source="manual", prompt="", what=what, expect=norm(expect)[:500],
                                     text=what, addedAt=now_iso()))
        return dict(doc["items"][-1])
    return update(root, fn)


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="Play-test queue importer (cc-P83)")
    sub = ap.add_subparsers(dest="cmd")
    imp = sub.add_parser("import")
    imp.add_argument("--root", required=True)
    imp.add_argument("--dry-run", action="store_true")
    imp.add_argument("--first", type=int, default=FIRST_PROMPT)
    pp = sub.add_parser("parse")
    pp.add_argument("file")
    a = ap.parse_args(argv)
    if a.cmd == "import":
        lines = []
        changed, doc = import_all(a.root, write=not a.dry_run, log=lines.append, first=a.first)
        for l in lines:
            print(("(dry run) " if a.dry_run else "") + l)
        s = doc["summary"]
        print("%s: %d items, %d open, %d failed (%d not logged), %d passed%s" % (
            "dry run" if a.dry_run else ("written" if changed else "no change"), s["total"], s["open"], s["failed"],
            s["unloggedFails"], s["passed"], "" if not a.dry_run else ". Nothing was written."))
        return 0
    if a.cmd == "parse":
        num = int(re.search(r"cc-P(\d+)-", os.path.basename(a.file)).group(1))
        with open(a.file, "r", encoding="utf-8") as f:
            print(json.dumps(parse_notes(f.read(), num), indent=2))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
