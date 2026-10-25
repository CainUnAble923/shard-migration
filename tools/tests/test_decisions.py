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
# cc-P610: SL_SHARD points the facts at another work copy of the shard repo (a Golem's own).
SHARD = Path(os.environ.get("SL_SHARD", r"D:\ShatteredLegacy"))
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
        rev = self.ds()["P901-D1"]["answer"]["rev"]
        with self.assertRaises(ValueError):
            decisions.mark_taken(self.data, ["P901-D1"], "soon", expect={"P901-D1": {"rev": rev}})
        with self.assertRaises(ValueError, msg="a later one is not an answer to take"):
            decisions.mark_taken(self.data, ["P901-D1", "P901-D4"], "p150", by="overseer",
                                 expect={"P901-D1": {"rev": rev}, "P901-D4": {"rev": 1}})
        self.assertEqual(["P901-D1"], decisions.mark_taken(self.data, ["P901-D1"], "p150", by="overseer",
                                                           expect={"P901-D1": {"rev": rev}}))
        d = self.ds()["P901-D1"]
        self.assertEqual(("taken", "P150"), (d["state"], d["answer"]["takenInto"]))
        with self.assertRaises(ValueError):
            decisions.answer(self.data, d, "Yes")
        doc = {"items": [], "decisions": list(self.ds().values())}
        self.assertNotIn("P901-D1", [x["id"] for x in playwhere.shown_items(doc, "open")], "taken leaves the default view")
        self.assertIn("P901-D1", [x["id"] for x in playwhere.shown_items(doc, "all")])
        self.assertEqual(["P901-D1"], decisions.mark_taken(self.data, ["P901-D1"], "", undo=True,
                                                           expect={"P901-D1": {"rev": d["answer"]["rev"], "takenInto": "P150"}}))
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
        self.assertEqual(400, self.call("/api/decisions/taken", {"ids": ["P901-D1"], "prompt": "P150"})[0],
                         "cc-P610: a take that does not say which answer it took is refused")
        expect = self.call("/api/decisions/copy")[1]["expect"]
        code, r = self.call("/api/decisions/taken", {"ids": ["P901-D1"], "prompt": "P150", "expect": expect})
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
        self.assertIn("if (filter === 'answered') return it.state === 'answered' || (it.state === 'archived' && it.answerStatus === 'answered');", self.t)
        self.assertIn("' new answer' + (na === 1 ? '' : 's')", self.t)
        self.assertIn("var DEC_OPEN = { open: 1, later: 1, answered: 1, archived: 1 }, DEC_ASK = { open: 1, later: 1 };", self.t)
        self.assertIn("if (it.replacedBy && filter !== 'all') return false;", self.t)
        self.assertIn("var listFilter = 'open';", self.t, "the full list's default is still Open (cc-P164: the page opens on Up next)")
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


# --- cc-P610 (P533 U8, P509 #1-#5): identity, archived answers, safe take and undo, drafts ---------------

def doors(*questions, num=902):
    """A DONE notes file whose decisions are these questions, in this order."""
    rows = "\n".join("%d. **%s** Say which." % (i + 1, q) for i, q in enumerate(questions))
    return {"P%d" % num: ("cc-P%d-doors.md" % num, decisions.parse_notes(
        "# cc-P%d\n\n## Decisions for Chase\n\n%s\n\nP%d DONE\n" % (num, rows, num), num))}


class Identity(unittest.TestCase):
    """P509 #1 and #2: an answer stays with its question when the notes change around it."""

    def setUp(self):
        need()
        self.data = tempfile.mkdtemp(prefix="p610-data-")

    def tearDown(self):
        shutil.rmtree(self.data, ignore_errors=True)

    def ds(self, notes):
        return decisions.build(notes, {}, decisions.load(self.data))

    def by_q(self, notes):
        return {d["question"]: d for d in self.ds(notes)}

    def test_an_inserted_question_does_not_take_another_ones_answer(self):
        v1 = doors("Use oak for the door?")
        decisions.answer(self.data, self.ds(v1)[0], "", "oak, please")
        v2 = doors("Add a lamp?", "Use oak for the door?")      # a bullet inserted above it
        q = self.by_q(v2)
        self.assertEqual(("P902-D1", "open"), (q["**Add a lamp?** Say which."]["id"], q["**Add a lamp?** Say which."]["state"]),
                         "the new question at D1 is open: the scratch example attached oak to it")
        oak = q["**Use oak for the door?** Say which."]
        self.assertEqual(("P902-D2", "answered", "oak, please"), (oak["id"], oak["state"], oak["answer"]["text"]))
        # Answering the new D1 leaves the oak answer alone.
        decisions.answer(self.data, q["**Add a lamp?** Say which."], "", "a lamp")
        q = self.by_q(v2)
        self.assertEqual("a lamp", q["**Add a lamp?** Say which."]["answer"]["text"])
        self.assertEqual("oak, please", q["**Use oak for the door?** Say which."]["answer"]["text"])
        self.assertEqual([], [d for d in self.ds(v2) if d["state"] == "archived"])

    def test_reordered_and_renumbered_questions_keep_their_answers(self):
        v1 = doors("Use oak for the door?", "Add a lamp?", "Paint it red?")
        ds = self.ds(v1)
        decisions.answer(self.data, ds[0], "", "oak")
        decisions.answer(self.data, ds[2], "", "red")
        q = self.by_q(doors("Paint it red?", "Use oak for the door?"))
        self.assertEqual(("P902-D1", "red"), (q["**Paint it red?** Say which."]["id"], q["**Paint it red?** Say which."]["answer"]["text"]))
        self.assertEqual(("P902-D2", "oak"), (q["**Use oak for the door?** Say which."]["id"], q["**Use oak for the door?** Say which."]["answer"]["text"]))

    def test_a_reworded_question_keeps_its_old_answer_visible_and_unattached(self):
        decisions.answer(self.data, self.ds(doors("Use oak for the door?"))[0], "", "oak")
        ds = self.ds(doors("Use pine for the door?"))
        live = [d for d in ds if d["state"] != "archived"]
        self.assertEqual(["open"], [d["state"] for d in live], "never silently attached to a different question")
        old = [d for d in ds if d["state"] == "archived"]
        self.assertEqual(1, len(old), "the saved answer stays on the page for review")
        self.assertEqual(("**Use oak for the door?** Say which.", "oak"), (old[0]["question"], old[0]["answer"]["text"]))
        self.assertNotEqual(live[0]["id"], old[0]["id"], "each card has its own id on the page")
        doc = {"items": [], "summary": {}}
        decisions.annotate(doc, ds, {})
        self.assertEqual(1, doc["answers"]["new"], "it still counts as an answer not yet taken")
        self.assertEqual(0, sum(1 for d in ds if d["state"] in decisions.ASKING and d["state"] == "archived"))
        self.assertIn("Use oak for the door?", decisions.copy_text(ds))
        with self.assertRaises(ValueError):
            decisions.answer(self.data, old[0], "", "changed")

    def test_a_removed_question_keeps_its_answer_and_gets_it_back_when_it_returns(self):
        v1 = doors("Use oak for the door?", "Add a lamp?")
        decisions.answer(self.data, self.ds(v1)[1], "", "a lamp")
        gone = self.ds(doors("Use oak for the door?"))
        old = [d for d in gone if d["state"] == "archived"]
        self.assertEqual(["**Add a lamp?** Say which."], [d["question"] for d in old])
        self.assertIn("Add a lamp?", decisions.copy_text(gone))
        back = self.by_q(v1)
        self.assertEqual(("answered", "a lamp"), (back["**Add a lamp?** Say which."]["state"], back["**Add a lamp?** Say which."]["answer"]["text"]))
        self.assertEqual([], [d for d in self.ds(v1) if d["state"] == "archived"])
        # Notes that cannot be read for a while (no notes at all) lose no answer either.
        self.assertEqual(["archived"], [d["state"] for d in self.ds({})])

    def test_an_answer_saved_before_questions_were_stored_still_joins_by_place(self):
        Path(self.data, "testing").mkdir()
        Path(self.data, decisions.DATA_REL).write_text(json.dumps({"schema": 1, "answers": {"P902-D1": {
            "id": "P902-D1", "prompt": "P902", "question": "", "choice": "", "text": "old", "status": "answered",
            "by": "", "at": "2026-10-01T00:00:00Z", "history": []}}}), encoding="ascii")
        d = self.ds(doors("Use oak for the door?"))[0]
        self.assertEqual(("answered", "old"), (d["state"], d["answer"]["text"]))


class Revisions(unittest.TestCase):
    """P509 #3: a take or an undo says which answer it saw; a stale one is refused."""

    def setUp(self):
        need()
        self.data = tempfile.mkdtemp(prefix="p610-rev-")
        self.notes = doors("Use oak for the door?")

    def tearDown(self):
        shutil.rmtree(self.data, ignore_errors=True)

    def d(self):
        return decisions.build(self.notes, {}, decisions.load(self.data))[0]

    def test_a_take_of_an_answer_that_changed_since_is_refused(self):
        decisions.answer(self.data, self.d(), "", "A: oak")
        seen = self.d()["answer"]["rev"]                         # the overseer copies answer A
        decisions.answer(self.data, self.d(), "", "B: pine")     # Chase changes it
        with self.assertRaises(ValueError):
            decisions.mark_taken(self.data, ["P902-D1"], "P150", expect={"P902-D1": {"rev": seen}})
        self.assertEqual("answered", self.d()["state"], "B is not marked taken on the strength of A")
        with self.assertRaises(ValueError):
            decisions.mark_taken(self.data, ["P902-D1"], "P150")
        decisions.mark_taken(self.data, ["P902-D1"], "P150", expect={"P902-D1": {"rev": self.d()["answer"]["rev"]}})
        self.assertEqual(("taken", "B: pine"), (self.d()["state"], self.d()["answer"]["text"]))

    def test_a_delayed_or_repeated_undo_cannot_reopen_a_later_take(self):
        decisions.answer(self.data, self.d(), "", "oak")
        decisions.mark_taken(self.data, ["P902-D1"], "P150", expect={"P902-D1": {"rev": self.d()["answer"]["rev"]}})
        undo = {"P902-D1": {"rev": self.d()["answer"]["rev"], "takenInto": "P150"}}
        self.assertEqual(["P902-D1"], decisions.mark_taken(self.data, ["P902-D1"], "", undo=True, expect=undo))
        with self.assertRaises(ValueError, msg="the same undo again"):
            decisions.mark_taken(self.data, ["P902-D1"], "", undo=True, expect=undo)
        decisions.mark_taken(self.data, ["P902-D1"], "P160", expect={"P902-D1": {"rev": self.d()["answer"]["rev"]}})
        decisions.mark_taken(self.data, ["P902-D1"], "", undo=True,
                             expect={"P902-D1": {"rev": self.d()["answer"]["rev"], "takenInto": "P160"}})
        decisions.mark_taken(self.data, ["P902-D1"], "P150", expect={"P902-D1": {"rev": self.d()["answer"]["rev"]}})
        with self.assertRaises(ValueError, msg="the first undo, arriving late"):
            decisions.mark_taken(self.data, ["P902-D1"], "", undo=True, expect=undo)
        self.assertEqual(("taken", "P150"), (self.d()["state"], self.d()["answer"]["takenInto"]))

    def test_the_copy_gives_what_a_take_must_carry(self):
        decisions.answer(self.data, self.d(), "", "oak")
        ds = decisions.build(self.notes, {}, decisions.load(self.data))
        expect = decisions.expectations(ds)
        self.assertEqual({"P902-D1": {"rev": self.d()["answer"]["rev"]}}, expect)
        self.assertEqual(["P902-D1"], decisions.mark_taken(self.data, ["P902-D1"], "P150", expect=expect))


HOSTILE = '"><img src=x onerror="window.__pwned=1"></textarea><script>window.__pwned=2</script> \'q\' <b>tag</b> & done'
HOSTILE_BY = '<img src=y onerror="window.__pwned=4">"quoted"'
SCENARIO = r"""
<script>
(function () {
  var out = { steps: [] };
  function done(e) {
    if (e) out.error = String(e && e.stack || e);
    var pre = document.createElement('pre'); pre.id = 'p610-result';
    pre.textContent = JSON.stringify(out); document.body.appendChild(pre);
  }
  function box(id) { return document.querySelector('textarea[data-t="' + id + '"]'); }
  function until(test, then, n) {
    n = n || 0;
    if (test()) return then();
    if (n > 400) return done('timed out at step ' + out.steps.length);
    setTimeout(function () { until(test, then, n + 1); }, 25);
  }
  function type(id, text) { var b = box(id); b.focus(); b.value = text; b.dispatchEvent(new Event('input', { bubbles: true })); }
  try { localStorage.clear(); } catch (x) {}
  until(function () { return typeof data !== 'undefined' && data && data.decisions; }, function () {
    document.querySelector('.filters button[data-f="open"]').click();
    until(function () { return box('P903-D1') && box('P903-D2'); }, function () {
      type('P903-D1', 'draft one');
      document.querySelector('#where-chips button[data-w="questions"]').click();      // a Where chip
      out.steps.push(['chip', box('P903-D1').value]);
      type('P903-D2', 'two, saved');
      document.querySelector('button[data-d="text"][data-i="P903-D2"]').click();       // another card saves
      until(function () { return document.querySelector('#i-P903-D2.answered'); }, function () {
        out.steps.push(['other save', box('P903-D1').value, box('P903-D2').value]);
        load().then(function () {                                                        // a data refresh
          out.steps.push(['reload', box('P903-D1').value]);
          var discard = document.querySelector('button[data-d="discard"][data-i="P903-D1"]');
          out.steps.push(['discard button', !!discard]);
          if (discard) discard.click();
          render();
          out.steps.push(['after discard', box('P903-D1').value]);
          var h = document.getElementById('i-P903-D3');
          out.hostile = {
            box: box('P903-D3') ? box('P903-D3').value : null,
            answer: h && h.querySelector('.answer') ? h.querySelector('.answer').textContent : null,
            label: h && h.querySelector('.label') ? h.querySelector('.label').textContent : null,
            injected: document.querySelectorAll('#list img, #list script').length,
            pwned: window.__pwned || 0
          };
          done();
        }).catch(done);
      });
    });
  });
})();
</script>
"""


def chrome():
    for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if os.path.isfile(p):
            return p
    return None


class PageDom(unittest.TestCase):
    """P509 #4 and #5, in a real browser (headless Chrome or Edge) on a throwaway loopback copy of the service: a draft
    survives a Where chip, another card's save and a data refresh, and goes only on its own save or Discard; hostile
    answer, writer and question text render as literal text."""

    def setUp(self):
        need()
        self.browser = chrome()
        if not self.browser:
            self.skipTest("UNVERIFIED: no Chrome or Edge on this machine")
        self.tmp = tempfile.mkdtemp(prefix="p610-dom-")
        svc = os.path.join(self.tmp, "svc")
        shutil.copytree(str(SHARD / "docker" / "test-queue"), svc)
        page = Path(svc, "html", "index.html")
        t = page.read_text(encoding="utf-8")
        page.write_text(t.replace("</body>", SCENARIO + "</body>", 1), encoding="utf-8")
        self.root = os.path.join(self.tmp, "root")
        for d in ("notes", "docs", "testing"):
            os.makedirs(os.path.join(self.root, d))
        Path(self.root, "notes", "cc-P903-page.md").write_text(
            "# cc-P903\n\n## Decisions for Chase\n\n1. **Use oak for the door?** Say which.\n"
            "2. **Add a lamp?** Say which.\n3. **<img src=z onerror=\"window.__pwned=3\"> Paint it?** Say which.\n\nP903 DONE\n",
            encoding="utf-8")
        Path(self.root, decisions.OVERLAY_REL).write_text("{}", encoding="utf-8")
        Path(self.root, pt.DATA_REL).write_text(json.dumps(pt.ordered_doc(pt.new_doc())), encoding="utf-8")
        q3 = decisions.parse_notes(Path(self.root, "notes", "cc-P903-page.md").read_text(encoding="utf-8"), 903)[2]["question"]
        Path(self.root, decisions.DATA_REL).write_text(json.dumps({"schema": 1, "answers": {"P903-D3": {
            "id": "P903-D3", "prompt": "P903", "question": q3, "choice": "", "text": HOSTILE, "status": "answered",
            "by": HOSTILE_BY, "at": "2026-10-25T00:00:00Z", "history": []}}}), encoding="ascii")
        self.port = free_port()
        e = {k: v for k, v in os.environ.items() if not k.startswith(("PLAYTESTS_", "ACCESS_", "REPO_STAMP"))}
        self.proc = subprocess.Popen([sys.executable, "-B", os.path.join(svc, "server.py"), "--root", self.root, "--lib",
                                      str(TOOLS), "--bind", "127.0.0.1", "--port", str(self.port), "--status-page",
                                      os.devnull, "--deployed", os.devnull, "--import-seconds", "3600",
                                      "--reload-seconds", "0"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=e)
        for _ in range(100):
            try:
                urllib.request.urlopen("http://127.0.0.1:%d/nav.js" % self.port, timeout=2).close()
                return
            except OSError:
                time.sleep(0.1)
        self.fail("the service did not start")

    def tearDown(self):
        if getattr(self, "proc", None):
            self.proc.terminate()
            self.proc.wait(10)
            self.proc.stdout.close()
        if getattr(self, "tmp", None):
            shutil.rmtree(self.tmp, ignore_errors=True)

    def run_page(self):
        r = subprocess.run([self.browser, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
                            "--user-data-dir=" + os.path.join(self.tmp, "profile"), "--virtual-time-budget=30000",
                            "--dump-dom", "http://127.0.0.1:%d/" % self.port],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=120)
        dom = r.stdout.decode("utf-8", "replace")
        start = dom.find('<pre id="p610-result">')
        if start < 0:
            self.fail("UNVERIFIED: the browser gave no result (exit %d, %d bytes of DOM)" % (r.returncode, len(dom)))
        import html
        body = dom[start + len('<pre id="p610-result">'):dom.index("</pre>", start)]
        return json.loads(html.unescape(body))

    def test_drafts_survive_and_hostile_text_stays_text(self):
        res = self.run_page()
        self.assertNotIn("error", res, res.get("error"))
        steps = {s[0]: s[1:] for s in res["steps"]}
        self.assertEqual(["draft one"], steps["chip"], "a Where chip keeps the draft")
        self.assertEqual(["draft one", "two, saved"], steps["other save"], "another card's save keeps it")
        self.assertEqual(["draft one"], steps["reload"], "a data refresh keeps it")
        self.assertEqual([True], steps["discard button"])
        self.assertEqual([""], steps["after discard"], "Discard puts the saved answer (none) back")
        h = res["hostile"]
        self.assertEqual(HOSTILE, h["box"], "the answer reads back literally in its box")
        self.assertIn("<b>tag</b>", h["answer"])
        self.assertIn(HOSTILE_BY, h["answer"], "the writer's name is text")
        self.assertIn("<img src=z", h["label"], "the question is text")
        self.assertEqual((0, 0), (h["injected"], h["pwned"]), "no element or handler from the data")


if __name__ == "__main__":
    unittest.main()
