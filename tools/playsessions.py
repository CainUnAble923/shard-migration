"""cc-P164: the play-test page's "Up next": Chase's open items in short themed sessions instead of one long list.

Chase, 2026-10-18 11:18: "the play test page is still intimidating, it would be nice for it to show what i need to test
in a similar fashion on how you give it to me in digestible chunks".

    annotate(doc, spec, deployed) -> doc, with doc["sessions"] = {available, list, upNext, owed, ...}

after playwho, decisions and playwhere have annotated the document (it needs each item's who and where).

A session is a short, ordered list of Chase's own items that belong together in one sitting:
    seeded   testing/sessions.json, the overseer's file (like testing/decisions-overlay.json): a title, a one-line why,
             a "before you start" list and item ids in order. Nothing here writes it.
    auto     every open item of Chase's that is in no seeded session and not probably stale, grouped by Where (and,
             for Player items, the character the steps name), then by prompt, newest prompts first, at most MAX items
             a session (a prompt is split only when it alone has more), so nothing is lost
    stale    "Probably stale": items the page can flag (below), each with its reason; one tap marks it Later
Chase's items are Who You or Bot then you, Where In game: Admin, In game: Player or Outside the game. Bot and CC
items never show; owed counts them. Questions (decisions) have their own cards and filter, so they are not here.

Each item in a session carries the words the card shows (line: what to do, pass: what should happen, place: where),
done (it has a result: pass, fail or later) and needs: "rebuild test shard" when its prompt was imported after the test
shard was last deployed (an in-game item only; the import is minutes after the prompt's DONE, so it stands in for the
prompt's commit, which the service cannot ask git for), and "newest player package" when it names the package or our
client and no package record says one was published after the prompt (there is no such record yet: see
PACKAGE_REL).

Probably stale (only items not in a seeded session):
    superseded   the item's prompt is in the spec's "superseded" map (prompt -> why), e.g. P62's kitsune frames by P138
    unparsed     a "checklist not parsed, read the notes" placeholder
    old address  its text or steps name the game PC's old page addresses (192.168.1.58:8093 or :3000) after the Haven move
    listed       the spec's own stale list, each with a reason
A session is finished when every item in it has a result; it then collapses to one line with the date of the last.
Up next is the first unfinished seeded session, else the first unfinished automatic one, else the stale group.
Pure functions apart from load(); ASCII only.
"""
import json
import os
import re

SPEC_REL = os.path.join("testing", "sessions.json")
PACKAGE_REL = os.path.join("testing", "package-published.json")
MAX = 12
STEPS_FIT = 0.15
STALE_NOTE = "probably stale"
OPEN = ("open", "blocked")           # still to do in a session; later, pass and fail count as done here
CHASE_WHO = ("you", "botyou")
CHASE_WHERE = ("admin", "player", "outside")
IN_GAME = ("admin", "player")
UNPARSED = re.compile(r"(?i)checklist not parsed")
OLD_ADDR = re.compile(r"192\.168\.1\.58:(8093|3000)\b")
PACKAGE = re.compile(r"(?i)player package|newest package|build package")
STOP = {"then", "with", "your", "that", "this", "from", "each", "when", "into", "they", "them", "have", "test", "shard"}
CHAR_WORDS = {"human": "Human (Ringo)", "gargoyle": "Gargoyle", "elf": "Elf"}


def load(roots):
    """The overseer's sessions.json, from the first root that has it (the notes clone first, like the triage): the
    spec dict, or None when there is none or it does not parse."""
    for r in roots:
        p = os.path.join(r, SPEC_REL)
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8-sig") as f:
                    spec = json.load(f)
                return spec if isinstance(spec, dict) else None
            except (OSError, ValueError):
                return None
    return None


def load_package(roots):
    """{version, at} of the last player package published, when something has written PACKAGE_REL; else None."""
    for r in roots:
        p = os.path.join(r, PACKAGE_REL)
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8-sig") as f:
                    return json.load(f)
            except (OSError, ValueError):
                return None
    return None


def prompt_num(pid):
    m = re.match(r"^P(\d+)$", pid or "")
    return int(m.group(1)) if m else -1


def is_chase(it):
    """An item for Chase's sessions: not replaced by decisions, Who You or Bot then you, Where in game or outside."""
    if it.get("replacedBy") or it.get("kind") == "decision":
        return False
    return (it.get("who") or {}).get("key") in CHASE_WHO and (it.get("where") or {}).get("key") in CHASE_WHERE


def plain(s):
    """Markdown bold off; backticks kept (the page shows them as code)."""
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", (s or "").strip())


def tokens(s):
    return set(w for w in re.findall(r"[a-z][a-z0-9]{3,}", (s or "").lower()) if w not in STOP)


def steps_fit(it):
    """The hand-written steps (testing/playtest-steps.json) belong to this item: a "checklist not parsed" placeholder
    (the steps are its only words), or they share at least STEPS_FIT of their words with the notes' own lines. P140's
    steps follow the notes' numbering, one off from the importer's, and this keeps them off the wrong card."""
    s = it.get("steps") or {}
    if not (s.get("do") or s.get("pass")):
        return False
    if UNPARSED.search(own_text(it)):
        return True
    a = tokens(" ".join([it.get("label") or "", it.get("what") or "", it.get("expect") or ""]))
    b = tokens(" ".join(s.get("do") or []) + " " + (s.get("pass") or ""))
    return bool(a and b) and len(a & b) / float(min(len(a), len(b))) >= STEPS_FIT


def words(it):
    """(line, pass, place) the card shows: the hand-written steps when they fit the item, else the notes' own lines."""
    s = (it.get("steps") or {}) if steps_fit(it) else {}
    do = [plain(d) for d in (s.get("do") or []) if d]
    line = "; then ".join(do) if do else plain(it.get("what") or it.get("text"))
    if not do and it.get("label"):
        line = plain(it["label"]) + ": " + line
    line = re.sub(r"\.\s*Pass$", ".", line)
    return line, plain(s.get("pass") or it.get("expect")), plain(s.get("where"))


def own_text(it):
    return (it.get("text") or "") + " " + (it.get("what") or "")


def item_text(it):
    s = it.get("steps") or {}
    return " ".join([it.get("text") or "", it.get("what") or "", it.get("expect") or "", s.get("where") or ""] +
                    list(s.get("do") or []) + [s.get("pass") or ""])


def task_text(it):
    """What the item asks for (not where it is done: every in-game line names our client build)."""
    s = it.get("steps") or {}
    return " ".join([own_text(it), it.get("expect") or ""] + list(s.get("do") or []) + [s.get("pass") or ""])


def needs(it, prompts, deployed, package):
    out = []
    p = (prompts or {}).get(it.get("prompt") or "") or {}
    when = p.get("importedAt") or ""
    where = (it.get("where") or {}).get("key")
    if where in IN_GAME and when and (deployed or {}).get("at") and when > deployed["at"]:
        out.append("rebuild test shard")
    if PACKAGE.search(task_text(it)) and not (package and when and (package.get("at") or "") > when):
        out.append("newest player package")
    return out


def stale_reason(it, spec):
    sup = (spec or {}).get("superseded") or {}
    if it.get("prompt") in sup:
        return "replaced by a later prompt: " + str(sup[it["prompt"]])
    if UNPARSED.search(own_text(it)):
        return "a 'checklist not parsed' placeholder: read the notes, then mark it"
    if OLD_ADDR.search(item_text(it)):
        return "its steps name the game PC's old page address; the pages are on Haven since 2026-10-16"
    return ""


def session_item(it, prompts, deployed, package, reason=""):
    """One card. A probably stale item carries its reason and no deploy tags: it is to be checked, not tested."""
    line, pas, place = words(it)
    d = {"id": it["id"], "prompt": it.get("prompt") or "", "status": it.get("status") or "open",
         "done": (it.get("status") or "open") not in OPEN, "resultAt": it.get("resultAt") or "",
         "line": line, "pass": pas, "place": place,
         "who": (it.get("who") or {}).get("key", ""), "where": (it.get("where") or {}).get("key", ""),
         "needs": needs(it, prompts, deployed, package) if (it.get("status") or "open") in OPEN and not reason else []}
    if reason:
        d["reason"] = reason
    return d


def finish(s):
    s["total"] = len(s["items"])
    s["doneCount"] = sum(1 for x in s["items"] if x["done"])
    s["finished"] = bool(s["items"]) and s["doneCount"] == s["total"]
    s["finishedAt"] = max([x["resultAt"] for x in s["items"]] or [""])[:10] if s["finished"] else ""
    needs_all = []
    for x in s["items"]:
        for n in x["needs"]:
            if n not in needs_all:
                needs_all.append(n)
    s["needs"] = needs_all
    return s


def auto_before(where, chars, labels):
    if where == "admin":
        return ["Start the test shard and log in as Admin (Eve)"]
    if where == "player":
        who = " or ".join(CHAR_WORDS[c] for c in chars) if chars else "any character"
        return ["Start the test shard and log in as a player: " + who]
    return ["At the game PC or a browser; no game needed"]


def auto_sessions(items, prompts, deployed, package, labels):
    """Automatic sessions from the items no seeded session holds: by Where (and character), then whole prompts,
    newest first, at most MAX items each."""
    groups = {}
    for it in items:
        w = it["where"]["key"]
        chars = tuple(sorted(it["where"].get("chars") or [])) if w == "player" else ()
        groups.setdefault((w, chars), []).append(it)
    order = {"admin": 0, "player": 1, "outside": 2}
    out = []
    for (w, chars) in sorted(groups, key=lambda k: (order.get(k[0], 9), k[1])):
        its = sorted(groups[(w, chars)], key=lambda i: (-prompt_num(i.get("prompt")), i.get("prompt") or "~", i.get("position", 0), i["id"]))
        chunks, cur = [], []
        by_prompt = []
        for it in its:
            if by_prompt and by_prompt[-1][0] == (it.get("prompt") or it["id"]):
                by_prompt[-1][1].append(it)
            else:
                by_prompt.append([it.get("prompt") or it["id"], [it]])
        for _, block in by_prompt:
            while len(block) > MAX:              # one prompt with more than MAX: split it
                if cur:
                    chunks.append(cur)
                    cur = []
                chunks.append(block[:MAX])
                block = block[MAX:]
            if cur and len(cur) + len(block) > MAX:
                chunks.append(cur)
                cur = []
            cur = cur + block
        if cur:
            chunks.append(cur)
        label = labels.get(w, w)
        if w == "player":
            label += ": " + (", ".join(CHAR_WORDS[c].split(" ")[0] for c in chars) if chars else "any character")
        for n, ch in enumerate(chunks):
            ps = []
            for it in ch:
                p = it.get("prompt") or ""
                if p and p not in ps:
                    ps.append(p)
            names = [re.sub(r"^cc-P\S*:?\s*", "", (prompts.get(p) or {}).get("title") or p) for p in ps]
            title = label + ": " + (names[0] if names else "older items") + (" and %d more" % (len(names) - 1) if len(names) > 1 else "")
            out.append(finish({
                "id": "auto-%s%s-%d" % (w, "-" + "-".join(chars) if chars else "", n + 1), "kind": "auto",
                "title": title, "why": "Not in a planned session yet: " + label + ", newest prompts first.",
                "before": auto_before(w, list(chars), labels),
                "items": [session_item(it, prompts, deployed, package) for it in ch]}))
    return out


def annotate(doc, spec, deployed=None, package=None):
    items = doc.get("items", [])
    by_id = {it["id"]: it for it in items}
    prompts = doc.get("prompts") or {}
    labels = (doc.get("where") or {}).get("labels") or {}
    available = spec is not None
    spec = spec or {}
    sessions, placed = [], set()
    for s in spec.get("sessions") or []:
        rows = []
        for i in s.get("items") or []:
            it = by_id.get(i)
            if not it or i in placed or it.get("replacedBy"):
                continue
            if (it.get("who") or {}).get("key") in ("bot", "cc"):
                continue                          # never Bot or CC, whatever the file says
            placed.add(i)
            rows.append(session_item(it, prompts, deployed, package))
        sessions.append(finish({"id": str(s.get("id") or "s%d" % (len(sessions) + 1)), "kind": "seeded",
                                "title": str(s.get("title") or ""), "why": str(s.get("why") or ""),
                                "before": [str(b) for b in (s.get("before") or [])], "items": rows}))
    # Probably stale: the spec's list first, in its order, then what the rules find, oldest prompts first. An item marked
    # Later from this group (its note starts "probably stale") stays in it, done, so the group can finish and collapse.
    def stale_ok(it):
        st_ = it.get("status") or "open"
        return st_ in OPEN or (st_ == "later" and (it.get("note") or "").lower().startswith(STALE_NOTE))
    stale_rows = []
    st = spec.get("stale") or {}
    for e in st.get("items") or []:
        i = e.get("id") if isinstance(e, dict) else e
        it = by_id.get(i)
        if not it or i in placed or not stale_ok(it) or not (is_chase(it) or (it.get("status") or "open") == "later"):
            continue
        placed.add(i)
        stale_rows.append(session_item(it, prompts, deployed, package, (e.get("reason") if isinstance(e, dict) else "") or stale_reason(it, spec) or "the overseer thinks so"))
    found = []
    for it in items:
        if it["id"] in placed or not stale_ok(it) or ((it.get("status") or "open") in OPEN and not is_chase(it)):
            continue
        if it.get("status") == "later" and it.get("replacedBy"):
            continue
        r = stale_reason(it, spec)
        if r:
            found.append((it, r))
    for it, r in sorted(found, key=lambda x: (prompt_num(x[0].get("prompt")), x[0].get("position", 0), x[0]["id"])):
        placed.add(it["id"])
        stale_rows.append(session_item(it, prompts, deployed, package, r))
    rest = [it for it in items if it["id"] not in placed and is_chase(it) and (it.get("status") or "open") in OPEN]
    sessions += auto_sessions(rest, prompts, deployed, package, labels)
    stale = finish({"id": "stale", "kind": "stale", "title": str(st.get("title") or "Probably stale"),
                    "why": str(st.get("why") or "Replaced, unparsed or pointing at the old game PC pages: check each, then mark it Later with the reason."),
                    "before": [str(b) for b in (st.get("before") or [])], "items": stale_rows})
    if stale_rows:
        sessions.append(stale)
    up = next((s["id"] for s in sessions if s["kind"] != "stale" and not s["finished"]), "")
    if not up and stale_rows and not stale["finished"]:
        up = "stale"
    owed = {"bot": 0, "cc": 0}
    for it in items:
        k = (it.get("who") or {}).get("key")
        if k in owed and (it.get("status") or "open") in ("open", "later", "blocked") and not it.get("replacedBy"):
            owed[k] += 1
    doc["sessions"] = {"available": available, "list": sessions, "upNext": up, "owed": owed,
                       "deployed": {k: (deployed or {}).get(k, "") for k in ("version", "commit", "at")},
                       "package": package or None, "max": MAX}
    return doc
