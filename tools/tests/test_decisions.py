"""cc-P146: Chase's decisions as items he answers on the play-test page, and the Where filters.

    python -m unittest discover -s tools\\tests -p "test_decisions.py"

tools/decisions.py reads each notes file's decisions section into items (P77-D3), merges the hand-written overlay
(testing/decisions-overlay.json) and the answers given on the page (testing/decisions.json, exported with the other
marks). tools/playwhere.py gives every open item one Where. The service (docker/test-queue/server.py) serves both on
/api/items and takes answers; the page (html/index.html) is read as text. The last class checks the real files.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
SHARD = Path(r"D:\ShatteredLegacy")
SERVER = SHARD / "docker" / "test-queue" / "server.py"
PAGE = SHARD / "docker" / "test-queue" / "html" / "index.html"
sys.path.insert(0, str(TOOLS))
import opsdata  # noqa: E402
import playtests as pt  # noqa: E402
import playwho  # noqa: E402

try:
    import decisions  # noqa: E402
    import playwhere  # noqa: E402
except ImportError:  # before cc-P146: every fact below fails on it, none errors out of the run
    decisions = playwhere = None

NOTES = """# cc-P900: a sample

## What changed

1. Not a decision: this list is outside the section.

## Deviations and decisions for Chase

Some introduction.

1. **The stack lives in /home/chase.** Nothing needs sudo. It is apart. More words here.
2. **A mule module?** P70 built 17 modules. Options:
   - a module for the Order;
   - or leave it, and reword the note.
3. **Prices are placeholders:** books 100/200,
   continued on a second line. Recommended: the pillar lamp first.

## Open questions

- **First bullet in a second section.** Say if you want it.

## For Chase

1. Not a decision either.

P900 DONE
"""


def need():
    if decisions is None:
        raise AssertionError("tools/decisions.py or tools/playwhere.py does not exist")


def real_notes(prompt):
    for num, name in pt.notes_files(str(ROOT)):
        if "P%d" % num == prompt:
            return (ROOT / "notes" / name).read_text(encoding="utf-8"), num
    raise AssertionError(prompt)


class Extraction(unittest.TestCase):
    def test_a_sample_section_gives_one_item_per_entry(self):
        need()
        ds = decisions.parse_notes(NOTES, 900)
        self.assertEqual(["P900-D1", "P900-D2", "P900-D3", "P900-D4"], [d["id"] for d in ds],
                         "numbered entries keep their numbers; a second section continues after them")
        self.assertEqual("**The stack lives in /home/chase.** Nothing needs sudo. It is apart.", ds[0]["question"],
                         "the bold label is not one of the two sentences")
        self.assertEqual("More words here.", ds[0]["detail"])
        self.assertTrue(ds[0]["built"], "a deviation is something built")
        self.assertEqual(["a module for the Order", "leave it, and reword the note"], [o["label"] for o in ds[1]["options"]])
        self.assertIn("continued on a second line", ds[2]["question"] + " " + ds[2]["detail"])
        self.assertEqual("the pillar lamp first", ds[2]["recommended"])
        self.assertEqual("deviations-and-decisions-for-chase", ds[0]["anchor"])
        self.assertEqual(("Open questions", "open-questions"), (ds[3]["section"], ds[3]["anchor"]))

    def test_p77_gives_its_eight_decisions_in_its_own_words(self):
        need()
        text, num = real_notes("P77")
        ds = decisions.parse_notes(text, num)
        self.assertEqual(["P77-D%d" % i for i in range(1, 9)], [d["id"] for d in ds])
        self.assertEqual('**Currency name:** "Alembic Drams" is a placeholder. Others: "Still Marks", "Vial Tokens".',
                         ds[1]["question"])
        self.assertTrue(ds[1]["built"], "a placeholder is built")
        self.assertEqual(["a module for the Order (a tonic drip, or a reagent rack that weighs less)",
                          'leave it, and reword "one from each guild" in a later note'],
                         [o["label"] for o in ds[5]["options"]])
        self.assertIn("the pillar lamp (on disk), then the bubble vat", ds[7]["recommended"])
        self.assertEqual({"Decisions for Chase"}, {d["section"] for d in ds})

    def test_p78_gives_its_twelve_defaults_taken(self):
        need()
        text, num = real_notes("P78")
        ds = decisions.parse_notes(text, num)
        self.assertEqual(12, len(ds))
        self.assertEqual("**Merge rule results:** Fletching has only a \"Band IV\" book holding Bands I to III; Alchemy, "
                         "Inscription and Cooking each have a \"Band IV\" book holding Band II or III items. Keep the literal "
                         "rule, or fold a leftover backward into the previous book?", ds[2]["question"])
        self.assertEqual("**Reading a book or scroll needs no skill.** Pinned's RecipeScroll needs the item's min skill. Add a floor?",
                         ds[4]["question"])
        self.assertTrue(all(d["built"] for d in ds), "defaults taken: every one is built")
        self.assertEqual("decisions-for-chase-defaults-taken", ds[0]["anchor"])

    def test_a_new_prompts_decisions_are_open_with_no_one_editing_anything(self):
        need()
        tmp = tempfile.mkdtemp(prefix="p146-notes-")
        try:
            os.makedirs(os.path.join(tmp, "notes"))
            Path(tmp, "notes", "cc-P900-sample.md").write_text(NOTES, encoding="utf-8")
            Path(tmp, "notes", "cc-P901-unfinished.md").write_text(NOTES.replace("P900 DONE", "still going"), encoding="utf-8")
            ds = decisions.build(decisions.read_all_notes(tmp), {"notAsked": ["P56"]}, decisions.new_doc())
            self.assertEqual(["open"] * 4, [d["state"] for d in ds], "a prompt that is not DONE gives nothing")
            self.assertTrue(ds[0]["link"].endswith("notes/cc-P900-sample.md#deviations-and-decisions-for-chase"))
            self.assertEqual("decide", ds[0]["who"]["key"])
            self.assertEqual("questions", ds[0]["where"]["key"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


def overlay():
    return {"notAsked": ["P900"], "replaces": {"P900-0": "P901", "T-1": ["P901-D9"]}, "decisions": {
        "P901-D1": {"question": "Hand words?", "options": [{"label": "Yes", "mark": "recommended"}, {"label": "No", "mark": ""}],
                    "built": False},
        "P901-D2": {"question": "Asked before?", "status": "elsewhere", "answer": "yes", "source": "notes/x.md"},
        "P901-D3": {"question": "Gone?", "status": "moot", "reason": "live is retired"},
        "P901-D9": {"prompt": "P901", "section": "6. Prose", "question": "Split by hand?", "built": True,
                    "notesFile": "notes/cc-P901-b.md"}}}


def notes_two():
    a = decisions.parse_notes(NOTES, 900)
    b = decisions.parse_notes(NOTES.replace("P900", "P901"), 901)
    return {"P900": ("cc-P900-a.md", a), "P901": ("cc-P901-b.md", b)}


class Overlay(unittest.TestCase):
    def test_the_overlay_words_notes_answers_elsewhere_moot_and_splits(self):
        need()
        ds = {d["id"]: d for d in decisions.build(notes_two(), overlay(), decisions.new_doc())}
        self.assertEqual("noted", ds["P900-D1"]["state"], "an older prompt in notAsked is only noted")
        self.assertEqual(("Hand words?", "open"), (ds["P901-D1"]["question"], ds["P901-D1"]["state"]))
        self.assertEqual(("elsewhere", "yes", "notes/x.md"), (ds["P901-D2"]["state"], ds["P901-D2"]["elsewhere"], ds["P901-D2"]["source"]))
        self.assertEqual(("moot", "live is retired"), (ds["P901-D3"]["state"], ds["P901-D3"]["reason"]))
        self.assertTrue(ds["P901-D9"]["split"])
        self.assertTrue(ds["P901-D9"]["link"].endswith("notes/cc-P901-b.md#6-prose"))
        self.assertEqual("open", ds["P901-D4"]["state"], "not in the overlay: parsed and asked")

    def test_replaced_items_leave_the_counts_and_you_decide_counts_the_questions(self):
        need()
        doc = pt.new_doc()
        for iid, p in (("P900-0", "P900"), ("T-1", ""), ("P900-1", "P900")):
            doc["items"].append(pt.new_item(id=iid, prompt=p, source="notes", what="w"))
        doc["summary"] = pt.compute_summary(doc)
        triage = {"P900-0": {"bucket": "DECISION", "reason": ""}, "T-1": {"bucket": "DECISION", "reason": ""},
                  "P900-1": {"bucket": "EYES", "reason": ""}}
        playwho.annotate(doc, triage, {})
        ds = decisions.build(notes_two(), overlay(), decisions.new_doc())
        decisions.annotate(doc, ds, overlay())
        it = {i["id"]: i for i in doc["items"]}
        self.assertEqual(["P901-D1", "P901-D2", "P901-D3", "P901-D4", "P901-D9"], it["P900-0"]["replacedBy"],
                         "a prompt replaces with all its decisions that are not noted")
        self.assertEqual(["P901-D9"], it["T-1"]["replacedBy"])
        self.assertNotIn("replacedBy", it["P900-1"])
        # You decide: the two replaced items leave; the asking decisions (P901-D1, D4, D9) come in.
        self.assertEqual(3, doc["who"]["counts"]["decide"])
        self.assertEqual(4, doc["who"]["mine"])
        self.assertEqual(2, doc["summary"]["replaced"])
        self.assertEqual(0, doc["answers"]["new"])


class Answers(unittest.TestCase):
    def setUp(self):
        need()
        self.data = tempfile.mkdtemp(prefix="p146-data-")

    def tearDown(self):
        shutil.rmtree(self.data, ignore_errors=True)

    def ds(self):
        return {d["id"]: d for d in decisions.build(notes_two(), overlay(), decisions.load(self.data))}

    def test_an_answer_is_saved_with_who_and_when_and_can_be_changed(self):
        a = decisions.answer(self.data, self.ds()["P901-D1"], "Yes", "and soon", by="chase@example.com")
        self.assertEqual(("answered", "Yes", "and soon", "chase@example.com"), (a["status"], a["choice"], a["text"], a["by"]))
        self.assertRegex(a["at"], r"^\d{4}-\d\d-\d\dT")
        d = self.ds()["P901-D1"]
        self.assertEqual(("answered", "Yes"), (d["state"], d["answer"]["choice"]))
        b = decisions.answer(self.data, d, "", "changed my mind", by="daughter@example.com")
        self.assertEqual(("", "changed my mind"), (b["choice"], b["text"]))
        self.assertEqual("Yes", b["history"][0]["choice"], "the earlier answer is kept in history")
        raw = Path(self.data, decisions.DATA_REL).read_text(encoding="ascii")
        self.assertIn('"question": "Hand words?"', raw, "the store holds the question, so the export reads on its own")

    def test_bad_answers_are_refused(self):
        ds = self.ds()
        with self.assertRaises(ValueError):
            decisions.answer(self.data, ds["P901-D1"], "Maybe")
        with self.assertRaises(ValueError):
            decisions.answer(self.data, ds["P901-D1"], "", "  ")
        with self.assertRaises(ValueError):
            decisions.answer(self.data, ds["P901-D1"], "built", "", )
        decisions.answer(self.data, ds["P901-D9"], "built")
        with self.assertRaises(ValueError):
            decisions.answer(self.data, ds["P901-D3"], "", "moot ones are not answered")

    def test_taken_locks_the_answer_and_leaves_the_default_view(self):
        decisions.answer(self.data, self.ds()["P901-D1"], "No")
        decisions.later(self.data, self.ds()["P901-D4"])
        self.assertEqual("later", self.ds()["P901-D4"]["state"])
        with self.assertRaises(ValueError):
            decisions.mark_taken(self.data, ["P901-D1"], "soon")
        self.assertEqual(["P901-D1"], decisions.mark_taken(self.data, ["P901-D1", "P901-D4"], "p150", by="overseer"))
        d = self.ds()["P901-D1"]
        self.assertEqual(("taken", "P150"), (d["state"], d["answer"]["takenInto"]))
        with self.assertRaises(ValueError):
            decisions.answer(self.data, d, "Yes")
        doc = {"items": [], "decisions": list(self.ds().values())}
        self.assertNotIn("P901-D1", [x["id"] for x in playwhere.shown_items(doc, "open")], "taken leaves the default view")
        self.assertIn("P901-D1", [x["id"] for x in playwhere.shown_items(doc, "all")])
        self.assertEqual(["P901-D1"], decisions.mark_taken(self.data, ["P901-D1"], "", undo=True))
        self.assertEqual("answered", self.ds()["P901-D1"]["state"])

    def test_answers_are_exported_with_the_other_marks(self):
        decisions.answer(self.data, self.ds()["P901-D1"], "Yes")
        b = opsdata.export_bundle(self.data)
        self.assertIn("testing/decisions.json", b["files"])
        mirror = tempfile.mkdtemp(prefix="p146-mirror-")
        try:
            opsdata.write_bundle(b, mirror)
            self.assertEqual("answered", decisions.load(mirror)["answers"]["P901-D1"]["status"])
        finally:
            shutil.rmtree(mirror, ignore_errors=True)
        text = decisions.copy_text(list(self.ds().values()))
        self.assertIn("P901-D1: Hand words?", text)
        self.assertIn("  Choice: Yes", text)


def where_doc():
    """Six open items and three decisions, with their Who and steps."""
    doc = pt.new_doc()
    rows = [("A-1", "EYES", {"where": "Test shard, SL TEST - Admin (Eve)"}),
            ("A-2", "EYES", {"where": "Test shard, SL TEST - Human (Ringo)"}),
            ("A-3", "BOT-PARTIAL", {"where": "Test shard, SL TEST - Elf (Elf Female)", "check": "c"}),
            ("A-4", "DEPLOY", {"where": "Shard Console (desktop), Websites tab"}),
            ("A-5", "BOT", {"check": "c"}),
            ("A-6", "EYES", {"where": "Test shard, a fresh tutorial character"}),
            ("A-7", "CC", {"check": "c"}),
            ("A-8", "DEPLOY", {"where": "Tailscale admin console"}),
            ("A-9", "EYES", {"where": "Somewhere odd", "place": "player", "chars": ["gargoyle"]})]
    triage, steps = {}, {}
    for iid, b, s in rows:
        doc["items"].append(pt.new_item(id=iid, prompt="P1", source="notes", what="w"))
        triage[iid] = {"bucket": b, "reason": ""}
        steps[iid] = s
    doc["items"].append(pt.new_item(id="A-10", prompt="P1", source="notes", what="w", status="pass"))
    playwho.annotate(doc, triage, steps)
    ds = decisions.build(notes_two(), overlay(), decisions.new_doc())
    decisions.annotate(doc, [d for d in ds if d["prompt"] == "P901" and d["id"] in ("P901-D1", "P901-D4", "P901-D2")], {})
    playwhere.annotate(doc)
    return doc


class Where(unittest.TestCase):
    def test_every_open_item_gets_one_where_from_its_who_and_steps(self):
        need()
        doc = where_doc()
        got = {i["id"]: (i["where"]["key"], i["where"]["chars"]) for i in doc["items"] if "where" in i}
        self.assertEqual({"A-1": ("admin", []), "A-2": ("player", ["human"]), "A-3": ("player", ["elf"]),
                          "A-4": ("outside", []), "A-5": ("bot", []), "A-6": ("player", []), "A-7": ("cc", []),
                          "A-8": ("outside", []), "A-9": ("player", ["gargoyle"])}, got,
                         "a hand-set place wins; 'admin console' is not in game; a passed item has none")
        self.assertEqual([], doc["where"]["missing"])

    def test_each_chip_counts_what_it_shows(self):
        need()
        c = where_doc()["where"]["counts"]
        self.assertEqual({"questions": 2, "outside": 2, "admin": 1, "player": 4, "bot": 1, "cc": 1}, {k: c[k] for k in playwhere.KEYS},
                         "Open: the answered-elsewhere decision is not in the default view")
        self.assertEqual({"human": 1, "gargoyle": 1, "elf": 1, "any": 1}, c["chars"])

    def test_chips_combine_with_mine(self):
        need()
        doc = where_doc()
        ids = lambda *a: sorted(i["id"] for i in playwhere.shown_items(doc, *a))  # noqa: E731
        self.assertEqual(["A-1", "A-2", "A-3", "A-4", "A-6", "A-8", "A-9", "P901-D1", "P901-D4"], ids("mine"))
        self.assertEqual(["A-2", "A-3", "A-6", "A-9"], ids("mine", "player"))
        self.assertEqual(["A-2"], ids("mine", "player", "human"))
        self.assertEqual(["A-6"], ids("mine", "player", "any"))
        self.assertEqual(["P901-D1", "P901-D4"], ids("mine", "questions"))
        self.assertEqual([], ids("whobot", "player"), "Bot + In game: Player: the bot items have Where bot")
        self.assertEqual(["A-5"], ids("whobot"))
        self.assertEqual(4, playwhere.counts(playwhere.shown_items(doc, "mine"))["player"])


def free_port():
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class Service(unittest.TestCase):
    def setUp(self):
        need()
        self.root = tempfile.mkdtemp(prefix="p146-root-")
        for d in ("notes", "docs", "testing"):
            os.makedirs(os.path.join(self.root, d))
        Path(self.root, "notes", "cc-P901-sample.md").write_text(NOTES.replace("P900", "P901"), encoding="utf-8")
        ov = overlay()
        ov["replaces"] = {"P901-0": "P901"}
        Path(self.root, decisions.OVERLAY_REL).write_text(json.dumps(ov), encoding="utf-8")
        Path(self.root, "testing", "bot-triage.md").write_text("| P901-0 | DECISION | read the notes |\n", encoding="utf-8")
        doc = pt.new_doc()
        doc["items"].append(pt.new_item(id="P901-0", prompt="P901", source="notes", what="P901: checklist not parsed"))
        Path(self.root, pt.DATA_REL).write_text(json.dumps(pt.ordered_doc(doc)), encoding="utf-8")
        self.port = free_port()
        e = {k: v for k, v in os.environ.items() if not k.startswith(("PLAYTESTS_", "ACCESS_", "REPO_STAMP"))}
        self.proc = subprocess.Popen([sys.executable, "-B", str(SERVER), "--root", self.root, "--lib", str(TOOLS),
                                      "--bind", "127.0.0.1", "--port", str(self.port), "--status-page", os.devnull,
                                      "--deployed", os.devnull, "--import-seconds", "3600", "--reload-seconds", "0"],
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=e)
        for _ in range(100):
            if self.proc.poll() is not None:
                self.fail("the service exited: " + self.proc.stdout.read().decode("utf-8", "replace")[-600:])
            try:
                self.call("/nav.js")
                return
            except OSError:
                time.sleep(0.1)
        self.fail("the service did not start")

    def tearDown(self):
        self.proc.terminate()
        self.proc.wait(10)
        self.proc.stdout.close()
        shutil.rmtree(self.root, ignore_errors=True)

    def call(self, path, body=None):
        req = urllib.request.Request("http://127.0.0.1:%d%s" % (self.port, path),
                                     data=None if body is None else json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, json.loads(r.read().decode("utf-8") or "null") if path.startswith("/api/") else None
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read().decode("utf-8"))

    def test_the_page_gets_the_decisions_and_an_answer_round_trips(self):
        code, d = self.call("/api/items")
        self.assertEqual(200, code)
        ds = {x["id"]: x for x in d["decisions"]}
        self.assertEqual("open", ds["P901-D1"]["state"])
        self.assertEqual(["P901-D1", "P901-D2", "P901-D3", "P901-D4", "P901-D9"],
                         {i["id"]: i for i in d["items"]}["P901-0"]["replacedBy"])
        self.assertEqual("questions", ds["P901-D1"]["where"]["key"])
        self.assertEqual(0, d["answers"]["new"])
        code, r = self.call("/api/decisions/answer", {"id": "P901-D1", "choice": "Yes", "text": "go"})
        self.assertEqual((200, "answered"), (code, r["answer"]["status"]))
        self.assertEqual(400, self.call("/api/decisions/answer", {"id": "P901-D1", "choice": "Perhaps"})[0])
        self.assertEqual(404, self.call("/api/decisions/answer", {"id": "P901-D99", "text": "x"})[0])
        code, d = self.call("/api/items")
        self.assertEqual(1, d["answers"]["new"])
        self.assertEqual(1, self.call("/api/summary")[1]["answers_new"])
        self.assertIn("P901-D1: Hand words?", self.call("/api/decisions/copy")[1]["text"])
        self.assertTrue(os.path.isfile(os.path.join(self.root, decisions.DATA_REL)))
        self.assertEqual(200, self.call("/api/decisions/later", {"id": "P901-D4"})[0])
        code, r = self.call("/api/decisions/taken", {"ids": ["P901-D1"], "prompt": "P150"})
        self.assertEqual((200, ["P901-D1"]), (code, r["taken"]))
        code, d = self.call("/api/items")
        ds = {x["id"]: x for x in d["decisions"]}
        self.assertEqual(("taken", "later", 0), (ds["P901-D1"]["state"], ds["P901-D4"]["state"], d["answers"]["new"]))
        self.assertEqual(400, self.call("/api/decisions/answer", {"id": "P901-D1", "text": "too late"})[0])


class Page(unittest.TestCase):
    def setUp(self):
        self.t = PAGE.read_text(encoding="utf-8")

    def test_the_where_chips_combine_with_the_buttons(self):
        self.assertIn('<div class="wherebar" id="where-chips" role="group" aria-label="Where"></div>', self.t)
        self.assertIn("function shown(it) { return shownPrimary(it) && whereMatch(it, where, chr); }", self.t)
        for key, label in (("questions", "Questions"), ("outside", "Outside the game"), ("admin", "In game: Admin"),
                           ("player", "In game: Player")):
            self.assertIn("['%s', '%s']" % (key, label), self.t)
        for key, label in (("human", "Human"), ("gargoyle", "Gargoyle"), ("elf", "Elf"), ("any", "Any character")):
            self.assertIn("['%s', '%s']" % (key, label), self.t)
        self.assertIn("return shownPrimary(it) && whereMatch(it, w, c);", self.t, "each chip counts what it would show")
        self.assertIn("'<span class=\"n\">' + whereCount(w[0], '') + '</span>", self.t)

    def test_the_decision_card_answers_on_the_page(self):
        for s in ("Keep what\\'s built", "Ask me later", "Save answer", "Taken into P...", "/api/decisions/answer",
                  "/api/decisions/later", "/api/decisions/taken", "data-d=\"opt\""):
            self.assertIn(s, self.t)
        self.assertIn("You can change it until the overseer takes it.", self.t)
        self.assertIn("Answered elsewhere: ", self.t)
        self.assertIn("Moot: ", self.t)

    def test_the_answered_filter_and_the_new_answers_count(self):
        self.assertIn('<button data-f="answered" aria-pressed="false"', self.t)
        self.assertIn(">Answered, not yet taken</button>", self.t)
        self.assertIn("if (filter === 'answered') return it.state === 'answered';", self.t)
        self.assertIn("' new answer' + (na === 1 ? '' : 's')", self.t)
        self.assertIn("var DEC_OPEN = { open: 1, later: 1, answered: 1 }, DEC_ASK = { open: 1, later: 1 };", self.t)
        self.assertIn("if (it.replacedBy && filter !== 'all') return false;", self.t)
        self.assertIn("var filter = 'open';", self.t, "the default view is still Open")
        self.assertIn("(s.open - (s.replaced || 0)) + ' open</span>'", self.t, "the open count leaves out replaced items")

    def test_the_source_stays_ascii(self):
        self.assertTrue(all(ord(c) < 128 for c in self.t))


class RealFiles(unittest.TestCase):
    """The real check: the overlay against the real notes and the real play tests."""

    def setUp(self):
        need()
        self.ov = decisions.load_overlay([str(ROOT)])
        self.assertIsNotNone(self.ov, "testing/decisions-overlay.json is missing or broken")
        self.ds = decisions.build(decisions.read_all_notes(str(ROOT)), self.ov, decisions.new_doc())

    def test_every_overlay_entry_is_an_item_with_a_question(self):
        ids = {d["id"] for d in self.ds}
        self.assertEqual([], [k for k in self.ov["decisions"] if k not in ids])
        for d in self.ds:
            if d["state"] != "noted":
                self.assertTrue(d["question"].strip(), d["id"])
                self.assertTrue(d["link"], d["id"])
            if d["state"] == "elsewhere":
                self.assertTrue(d["elsewhere"] and d["source"], d["id"])
            if d["state"] == "moot":
                self.assertTrue(d["reason"], d["id"])

    def test_every_you_decide_item_is_replaced_by_its_decisions(self):
        triage, _ = playwho.load_sources([str(ROOT)])
        doc = pt.ordered_doc(pt.load(str(ROOT / pt.DATA_REL)))
        rep = decisions.replaced_items(self.ov, self.ds)
        open_decide = [i["id"] for i in doc["items"] if i["status"] in ("open", "later", "blocked")
                       and (triage.get(i["id"]) or {}).get("bucket") == "DECISION"]
        self.assertEqual([], [i for i in open_decide if not rep.get(i)], "an open You decide item with no decisions")
        ids = {d["id"] for d in self.ds}
        self.assertEqual([], [x for r in rep.values() for x in r if x not in ids])

    def test_the_named_moot_ones_are_moot(self):
        st = {d["id"]: d["state"] for d in self.ds}
        self.assertEqual("moot", st["P89-D10"], "the intranet is Tailscale only")
        self.assertEqual("moot", st["P106-D10"], "live's D94 question: live is retired")
        self.assertEqual(["elsewhere"] * 8, [st["P59-D%d" % i] for i in range(1, 9)])
        self.assertEqual(["elsewhere"] * 8, [st["P80-D%d" % i] for i in range(1, 9)])


if __name__ == "__main__":
    unittest.main()
