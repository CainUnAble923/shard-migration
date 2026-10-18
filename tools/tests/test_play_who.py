"""cc-P115: every play-test item says who tests it (You, Bot, Bot then you, You decide, CC) and how.

    python -m unittest discover -s tools\\tests -p "test_play_who.py"

Who comes from testing/bot-triage.md (the single source, also read by the overnight bot's plan); the steps from
testing/playtest-steps.json, keyed by item id. tools/playwho.py merges both into the document when /api/items is read
(docker/test-queue/server.py); nothing is written back, and the importer never writes either file. The page
(html/index.html) is read as text here: what it is wired to. The last class checks the real files.
"""
import hashlib
import json
import os
import shutil
import socket
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
import playtests as pt  # noqa: E402

try:
    import playwho  # noqa: E402
except ImportError:  # before cc-P115: every fact below fails on it, none errors out of the run
    playwho = None

TRIAGE = """# Open play tests

| Bucket | Items |
|---|---|
| BOT | 1 |

### P56

| id | bucket | reason |
|---|---|---|
| P56-1 | BOT | Seal message is server-sent |
| P56-7 | BOT-PARTIAL | Bot: cliloc ids; Chase: the labels read as words |
| P62-2 | EYES | Paperdoll placement |
| P63-1 | DEPLOY | Shard Console, Player package tab |
| P59-0 | DECISION | Evo pet bodies |
| P95-3 | CC | git shows the run folder committed |
"""
STEPS = {"schema": 1, "items": {
    "P62-2": {"where": "Test shard, SL TEST - Elf", "do": ["Equip the ears", "Open the paperdoll"], "pass": "Ears above the hair"},
    "P56-1": {"check": "Not built yet: hand in a deed; result in the nightly report once built."},
    "P63-1": {"unknown": "which zip to pick"}}}


def doc_with(*rows):
    d = pt.new_doc()
    for iid, status in rows:
        d["items"].append(pt.new_item(id=iid, source="notes", prompt=iid.split("-")[0], what="w " + iid, status=status))
    return d


class Who(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(playwho, "tools/playwho.py does not exist")

    def test_the_triage_gives_every_bucket_its_who(self):
        t = playwho.parse_triage(TRIAGE)
        self.assertEqual(6, len(t), "the counts table's '| BOT | 1 |' row is not an item")
        self.assertEqual({"bucket": "CC", "reason": "git shows the run folder committed"}, t["P95-3"])
        got = {i: playwho.who_of(t[i]["bucket"])["label"] for i in t}
        self.assertEqual({"P56-1": "Bot", "P56-7": "Bot, then you", "P62-2": "You", "P63-1": "You",
                          "P59-0": "You decide", "P95-3": "CC"}, got)
        self.assertEqual("in the game or on screen", playwho.who_of("EYES")["kind"])
        self.assertEqual("a deploy, the console or a web page", playwho.who_of("DEPLOY")["kind"])

    def test_open_and_blocked_items_get_who_and_steps_and_results_are_left_alone(self):
        d = doc_with(("P62-2", "open"), ("P56-1", "blocked"), ("P63-1", "open"), ("P56-7", "pass"), ("P99-9", "open"))
        before = json.dumps(d["items"][3], sort_keys=True)
        playwho.annotate(d, playwho.parse_triage(TRIAGE), STEPS["items"])
        it = {i["id"]: i for i in d["items"]}
        self.assertEqual(("you", "You", "EYES", "Paperdoll placement"),
                         tuple(it["P62-2"]["who"][k] for k in ("key", "label", "bucket", "reason")))
        self.assertEqual(STEPS["items"]["P62-2"], it["P62-2"]["steps"])
        self.assertEqual("bot", it["P56-1"]["who"]["key"], "blocked counts as open")
        self.assertIn("check", it["P56-1"]["steps"])
        self.assertEqual({"unknown": "which zip to pick"}, it["P63-1"]["steps"])
        self.assertEqual(before, json.dumps(it["P56-7"], sort_keys=True), "an item with a result is not touched")
        self.assertEqual("unsorted", it["P99-9"]["who"]["key"], "an open item missing from the triage says so")
        self.assertIsNone(it["P99-9"]["steps"])
        for i in d["items"]:
            self.assertEqual("w " + i["id"], i["what"], "what/expect/text are never written over")

    def test_the_counts_are_per_who_over_open_items(self):
        d = doc_with(("P62-2", "open"), ("P63-1", "open"), ("P56-7", "later"), ("P59-0", "open"), ("P56-1", "open"),
                     ("P95-3", "open"), ("P99-9", "open"), ("P61-1", "pass"))
        w = playwho.annotate(d, playwho.parse_triage(TRIAGE), {})["who"]
        self.assertTrue(w["available"])
        self.assertEqual({"you": 2, "botyou": 1, "decide": 1, "bot": 1, "cc": 1, "unsorted": 1}, w["counts"])
        self.assertEqual(["P99-9"], w["unsorted"])
        self.assertEqual(4, w["mine"], "Mine = You + Bot, then you + You decide")

    def test_no_triage_is_unavailable_and_items_get_no_who(self):
        d = doc_with(("P62-2", "open"))
        w = playwho.annotate(d, None, None)["who"]
        self.assertFalse(w["available"])
        self.assertNotIn("who", d["items"][0])


class SurvivesTheImporter(unittest.TestCase):
    def test_an_import_never_touches_the_triage_or_the_steps(self):
        self.assertIsNotNone(playwho, "tools/playwho.py does not exist")
        tmp = tempfile.mkdtemp(prefix="p115-import-")
        try:
            shutil.copytree(ROOT / "notes", os.path.join(tmp, "notes"))
            shutil.copytree(ROOT / "docs", os.path.join(tmp, "docs"))
            os.makedirs(os.path.join(tmp, "testing"))
            for f in ("play-tests.json", "bot-triage.md", "playtest-steps.json"):
                shutil.copy(ROOT / "testing" / f, os.path.join(tmp, "testing", f))
            # A prompt the importer has not seen yet, so the run really writes.
            with open(os.path.join(tmp, "notes", "cc-P999-probe.md"), "w", encoding="utf-8") as f:
                f.write("# cc-P999: probe\n\n## For Chase\n\n1. Look at the probe.\n\nP999 DONE\n")

            def h(name):
                return hashlib.sha256(Path(tmp, "testing", name).read_bytes()).hexdigest()
            before = {f: h(f) for f in ("bot-triage.md", "playtest-steps.json")}
            pt.import_all(tmp, write=True, log=lambda *a: None)
            pt.import_all(tmp, write=True, log=lambda *a: None)
            self.assertEqual(before, {f: h(f) for f in before}, "the importer wrote the triage or the steps")
            doc = pt.ordered_doc(pt.load(os.path.join(tmp, pt.DATA_REL)))
            self.assertTrue(any(i["id"].startswith("P999-") for i in doc["items"]), "the probe prompt was not imported")
            triage, steps = playwho.load_sources([tmp])
            playwho.annotate(doc, triage, steps)
            it = {i["id"]: i for i in doc["items"]}
            self.assertEqual("CC", it["P95-3"]["who"]["bucket"], "an existing Who is still served after the import")
            self.assertTrue(it["P95-3"]["steps"]["check"])
            self.assertEqual("unsorted", it["P999-1"]["who"]["key"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class Service(unittest.TestCase):
    def start(self, extra=()):
        self.root = tempfile.mkdtemp(prefix="p115-root-")
        for d in ("notes", "docs", "testing"):
            os.makedirs(os.path.join(self.root, d))
        shutil.copy(ROOT / "docs" / "feature-queue.md", os.path.join(self.root, "docs", "feature-queue.md"))
        self.write(self.root, "testing/bot-triage.md", TRIAGE)
        self.write(self.root, "testing/playtest-steps.json", STEPS)
        data = getattr(self, "data", None) or self.root
        self.write(data, pt.DATA_REL, doc_with(("P62-2", "open"), ("P56-1", "open"), ("P95-3", "open"),
                                              ("P56-7", "open"), ("P61-1", "pass"), ("P99-9", "open")))
        self.port = free_port()
        e = {k: v for k, v in os.environ.items() if not k.startswith(("PLAYTESTS_", "ACCESS_", "REPO_STAMP"))}
        self.proc = subprocess.Popen([sys.executable, "-B", str(SERVER), "--root", self.root, "--lib", str(TOOLS),
                                      "--bind", "127.0.0.1", "--port", str(self.port), "--status-page", os.devnull,
                                      "--deployed", os.devnull, "--import-seconds", "3600"] + list(extra),
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=e)
        for _ in range(100):
            if self.proc.poll() is not None:
                self.fail("the service exited: " + self.proc.stdout.read().decode("utf-8", "replace")[-600:])
            try:
                self.get("/nav.js")
                return
            except OSError:
                time.sleep(0.1)
        self.fail("the service did not start")

    def tearDown(self):
        if getattr(self, "proc", None):
            self.proc.terminate()
            self.proc.wait(10)
            self.proc.stdout.close()
        for d in (getattr(self, "root", None), getattr(self, "data", None)):
            if d:
                shutil.rmtree(d, ignore_errors=True)

    def get(self, path):
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d%s" % (self.port, path), timeout=10) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as err:
            return err.code, err.read()

    def items(self):
        code, raw = self.get("/api/items")
        self.assertEqual(200, code, raw[:300])
        return json.loads(raw.decode("utf-8"))

    def write(self, base, rel, obj):
        p = os.path.join(base, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(obj if isinstance(obj, str) else json.dumps(obj))

    def test_items_carry_who_and_steps_and_the_document_carries_the_counts(self):
        self.start()
        d = self.items()
        it = {i["id"]: i for i in d["items"]}
        self.assertEqual("You", it["P62-2"]["who"]["label"])
        self.assertEqual(["Equip the ears", "Open the paperdoll"], it["P62-2"]["steps"]["do"])
        self.assertEqual("Bot, then you", it["P56-7"]["who"]["label"])
        self.assertEqual("CC", it["P95-3"]["who"]["label"])
        self.assertNotIn("who", it["P61-1"], "a passed item gets no Who")
        self.assertEqual({"you": 1, "botyou": 1, "decide": 0, "bot": 1, "cc": 1, "unsorted": 1}, d["who"]["counts"])
        self.assertTrue(d["who"]["available"])
        with open(os.path.join(self.root, pt.DATA_REL), encoding="utf-8") as f:
            self.assertNotIn('"who"', f.read(), "the service never writes Who into play-tests.json")

    def test_an_edited_triage_is_served_without_a_restart(self):
        self.start()
        self.assertEqual("unsorted", {i["id"]: i for i in self.items()["items"]}["P99-9"]["who"]["key"])
        time.sleep(1.1)  # a new mtime, whatever the file system's resolution
        self.write(self.root, "testing/bot-triage.md", TRIAGE + "| P99-9 | DECISION | pick one |\n")
        self.assertEqual("You decide", {i["id"]: i for i in self.items()["items"]}["P99-9"]["who"]["label"])

    def test_haven_mode_reads_the_triage_from_the_notes_clone(self):
        self.data = tempfile.mkdtemp(prefix="p115-data-")
        self.start(extra=["--data", self.data])
        it = {i["id"]: i for i in self.items()["items"]}
        self.assertEqual("You", it["P62-2"]["who"]["label"], "on Haven testing/ is a data volume; the triage is in the clone")
        self.assertIn("pass", it["P62-2"]["steps"])


class Page(unittest.TestCase):
    def setUp(self):
        self.t = PAGE.read_text(encoding="utf-8")

    def test_every_card_has_the_who_badge_beside_the_id_and_robot(self):
        self.assertIn("var wb = whoBadge(it);", self.t)
        self.assertIn("if (wb) chips.push(wb);", self.t)
        self.assertIn("'<span class=\"who who-' + esc(w.key) + '\" title=\"' + esc(title) + '\">' + esc(w.label) + '</span>'", self.t)
        for cls in (".who-you", ".who-botyou", ".who-decide", ".who-bot", ".who-cc", ".who-unsorted"):
            self.assertIn(cls, self.t)

    def test_the_steps_are_one_click_away_with_where_showing(self):
        self.assertIn("h += stepsHtml(it);", self.t)
        self.assertIn("'<details class=\"steps\"><summary>How to test", self.t)
        for word in ("Where:", "Do:", "Pass looks like:", "Check:", "Steps unknown:"):
            self.assertIn(word, self.t)

    def test_the_three_filters_are_extras_and_open_stays_the_default(self):
        for f, label in (("mine", "Mine"), ("whobot", "Bot"), ("cc", "CC")):
            self.assertIn('<button data-f="%s" aria-pressed="false"' % f, self.t)
            self.assertIn('>%s</button>' % label, self.t)
        self.assertIn("if (filter === 'mine') return !!OPEN[it.status] && !!MINE[whoKey(it)];", self.t)
        self.assertIn("if (filter === 'whobot') return !!OPEN[it.status] && whoKey(it) === 'bot';", self.t)
        self.assertIn("if (filter === 'cc') return !!OPEN[it.status] && whoKey(it) === 'cc';", self.t)
        self.assertIn("var MINE = { you: 1, botyou: 1, decide: 1 };", self.t)
        self.assertIn("var filter = 'open';", self.t)
        self.assertIn('<button data-f="open" aria-pressed="true">Open</button>', self.t)
        self.assertIn('<button data-f="bot" aria-pressed="false"', self.t, "P112's Bot tonight is still there")
        self.assertIn("if (filter === 'open') return !!OPEN[it.status];", self.t, "Open still shows every open item")

    def test_the_header_counts_per_who(self):
        self.assertIn("whoCounts()", self.t)
        self.assertIn("'<span class=\"count who-count\" data-go=\"' + go + '\"", self.t)
        self.assertIn("[data-go=\"mine\"]", self.t)

    def test_the_source_stays_ascii(self):
        self.assertTrue(all(ord(c) < 128 for c in self.t))


class MalformedRows(unittest.TestCase):
    def test_a_row_with_an_unknown_bucket_is_reported_and_a_good_row_is_not(self):
        text = "\n".join(["| id | bucket | reason |", "|---|---|---|", "| P1-1 | BOT | fine |", "| P1-2 | CHASE | looks |",
                          "| P1-3 | bot | lower case |", "| Gate | Where it stands | not an item row |"])
        self.assertEqual(["P1-2 CHASE", "P1-3 bot"], playwho.malformed_rows(text))


class RealFiles(unittest.TestCase):
    """The real check: every open and blocked item has a Who, and every triage row names a bucket the page knows.
    cc-P137: the hand-kept Counts table is no longer compared with the page (every result and every new prompt's
    items changed it, so the check failed for no fault); the page's header counts them live."""

    def test_every_open_item_has_a_who(self):
        self.assertIsNotNone(playwho, "tools/playwho.py does not exist")
        triage, steps = playwho.load_sources([str(ROOT)])
        doc = pt.ordered_doc(pt.load(str(ROOT / pt.DATA_REL)))
        w = playwho.annotate(doc, triage, steps)["who"]
        self.assertEqual([], w["unsorted"], "open items with no Who: sort each into testing/bot-triage.md, with its "
                                            "steps in testing/playtest-steps.json")
        open_n = sum(1 for i in doc["items"] if i["status"] in ("open", "blocked", "later"))
        self.assertEqual(open_n, sum(w["counts"].values()))

    def test_every_open_item_and_decision_has_one_who_and_one_where(self):
        # cc-P146: the decisions count too (each is You decide, Where Questions), and every open item has exactly one
        # Where: from its Who, or its steps' Where line, or a "place" set by hand in testing/playtest-steps.json.
        import decisions
        import playwhere
        triage, steps = playwho.load_sources([str(ROOT)])
        doc = pt.ordered_doc(pt.load(str(ROOT / pt.DATA_REL)))
        playwho.annotate(doc, triage, steps)
        ov = decisions.load_overlay([str(ROOT)])
        decisions.annotate(doc, decisions.build(decisions.read_all_notes(str(ROOT)), ov, decisions.new_doc()), ov)
        playwhere.annotate(doc)
        self.assertEqual([], doc["where"]["missing"], "open items with no Where: give their steps a Where line or a place")
        live = [i for i in doc["items"] if i["status"] in ("open", "blocked", "later")] + \
               [d for d in doc["decisions"] if d["state"] in decisions.ACTIVE]
        for it in live:
            self.assertTrue(it.get("who", {}).get("key"), it["id"])
            self.assertIn(it.get("where", {}).get("key"), playwhere.KEYS, it["id"])
        self.assertEqual(sum(doc["where"]["counts"][k] for k in playwhere.KEYS),
                         len([i for i in live if not i.get("replacedBy")]), "each one counted under exactly one Where")

    def test_every_triage_row_names_a_known_bucket(self):
        # cc-P137: four rows said CHASE, which the row pattern does not read, so those items had no Who at all.
        text = (ROOT / "testing" / "bot-triage.md").read_text(encoding="utf-8")
        self.assertEqual([], playwho.malformed_rows(text))

    def test_every_item_has_steps_of_the_right_shape(self):
        self.assertIsNotNone(playwho, "tools/playwho.py does not exist")
        triage, steps = playwho.load_sources([str(ROOT)])
        for iid, t in triage.items():
            s = steps.get(iid)
            self.assertTrue(s, "%s has no steps" % iid)
            if s.get("unknown"):
                continue
            if t["bucket"] in ("BOT", "CC"):
                self.assertTrue(s.get("check"), "%s: a %s item needs its check line" % (iid, t["bucket"]))
            elif t["bucket"] == "BOT-PARTIAL":
                self.assertTrue(s.get("check") and s.get("do"), "%s: the bot half and Chase's half" % iid)
            else:
                self.assertTrue(s.get("where") and s.get("do") and s.get("pass"), "%s: where, do, pass" % iid)
                self.assertLessEqual(len(s["do"]), 5, iid)


if __name__ == "__main__":
    unittest.main()
