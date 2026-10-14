"""cc-P97: the bug-reports inbox (tools/bugs.py), its routes in the play-test service, its page, and the reason now
required to decline or delete an idea (tools/ideas.py).

    python -m unittest tools/tests/test_bug_reports.py

Every fact works in a temporary folder. The service facts start D:\\ShatteredLegacy\\docker\\test-queue\\server.py on a
free local port against a temporary root and stop it afterwards; they are skipped if that file is not there. The
page facts read docker/test-queue/html/index.html as text: what the buttons are wired to, not how they look (that
was checked in a browser, see the P97 notes). Standard library only. ASCII only.
"""
import base64
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

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import bugs  # noqa: E402
import ideas  # noqa: E402

SHARD = Path(os.environ.get("SL_SHARD", r"D:\ShatteredLegacy"))
SERVER = SHARD / "docker" / "test-queue" / "server.py"
PAGE = SHARD / "docker" / "test-queue" / "html" / "index.html"

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64
JPG = b"\xff\xd8\xff\xe0" + b"\x00" * 64


class BugStore(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="bugs-")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def doc_text(self):
        with open(os.path.join(self.root, "testing", "bug-reports.json"), "r", encoding="ascii") as f:
            return f.read()

    def test_add_fills_every_field_with_stable_pretty_json(self):
        a = bugs.add(self.root, "  Smelting   eats the ore ", happened="Ore gone\n  no ingots  ", expected="Ingots",
                     steps="1. Mine\n2. Smelt", severity="wrong", area="crafting", playtest="P71-3",
                     character="Tester", location="Minoc forge", version="2026.10.14.3 (test shard, 61db33c)")
        b = bugs.add(self.root, "Second")
        self.assertEqual(("B-001", "B-002"), (a["id"], b["id"]))
        self.assertEqual("Smelting eats the ore", a["title"])
        self.assertEqual("Ore gone\nno ingots", a["happened"])
        self.assertEqual(("wrong", "crafting", "P71-3", "new", ""), (a["severity"], a["area"], a["playtest"], a["status"], a["by"]))
        self.assertEqual("2026.10.14.3 (test shard, 61db33c)", a["version"])
        doc = json.loads(self.doc_text())
        self.assertEqual(["schema", "nextId", "copiedAt", "bugs", "deleted"], list(doc))
        self.assertEqual(list(bugs.new_bug()), list(doc["bugs"][0]), "fixed key order")
        self.assertTrue(self.doc_text().endswith("}\n"))
        left = os.listdir(os.path.join(self.root, "testing"))
        self.assertEqual(["bug-reports.json"], left, "no temp or lock file is left")

    def test_bad_input_is_refused_and_nothing_is_written(self):
        for kw in ({"title": " "}, {"title": "x", "severity": "fatal"}, {"title": "x", "area": "pvp"},
                   {"title": "x", "playtest": "P71"}):
            with self.assertRaises(ValueError, msg=str(kw)):
                bugs.add(self.root, **kw)
        self.assertFalse(os.path.exists(os.path.join(self.root, "testing", "bug-reports.json")))

    def test_edit_changes_only_what_is_given(self):
        a = bugs.add(self.root, "Door", happened="Will not open", severity="annoying")
        e = bugs.edit(self.root, a["id"], title="Door in Britain", steps="Double-click it")
        self.assertEqual(("Door in Britain", "Will not open", "Double-click it", "annoying"),
                         (e["title"], e["happened"], e["steps"], e["severity"]))
        with self.assertRaises(KeyError):
            bugs.edit(self.root, "B-404", title="x")

    def test_each_status_needs_what_it_says(self):
        a = bugs.add(self.root, "Crash on cast")
        t = bugs.set_status(self.root, a["id"], "taken")
        self.assertEqual(("taken", ""), (t["status"], t["dnum"]), "taken, pending its number")
        t = bugs.set_status(self.root, a["id"], "taken", dnum="d91")
        self.assertEqual(("taken", "D91"), (t["status"], t["dnum"]), "became D91")
        with self.assertRaises(ValueError):
            bugs.set_status(self.root, a["id"], "taken", dnum="91")             # not a D-number
        f = bugs.set_status(self.root, a["id"], "fixed")
        self.assertEqual(("fixed", "D91"), (f["status"], f["dnum"]), "fixed keeps the D-number it had")
        with self.assertRaises(ValueError):
            bugs.set_status(self.root, a["id"], "duplicate")                    # of what?
        with self.assertRaises(ValueError):
            bugs.set_status(self.root, a["id"], "duplicate", duplicate_of="B-001")   # itself
        d = bugs.set_status(self.root, a["id"], "duplicate", duplicate_of="d89")
        self.assertEqual(("duplicate", "D89", ""), (d["status"], d["duplicateOf"], d["dnum"]))
        self.assertEqual("B-007", bugs.set_status(self.root, a["id"], "duplicate", duplicate_of="b-007")["duplicateOf"])
        with self.assertRaises(ValueError):
            bugs.set_status(self.root, a["id"], "notbug")                       # no reason
        with self.assertRaises(ValueError):
            bugs.set_status(self.root, a["id"], "notbug", reason="   ")         # only spaces
        n = bugs.set_status(self.root, a["id"], "notbug", reason="OSI does this")
        self.assertEqual(("notbug", "OSI does this", ""), (n["status"], n["reason"], n["duplicateOf"]))
        with self.assertRaises(ValueError):
            bugs.set_status(self.root, a["id"], "closed")                       # not a status
        back = bugs.set_status(self.root, a["id"], "new")
        self.assertEqual(("new", "", "", ""), (back["status"], back["dnum"], back["duplicateOf"], back["reason"]))

    def test_delete_needs_a_reason_keeps_it_and_retires_the_id(self):
        bugs.add(self.root, "One")
        two = bugs.add(self.root, "Two")
        bugs.add_shot(self.root, two["id"], PNG)
        with self.assertRaises(ValueError):
            bugs.delete(self.root, two["id"], "  ")
        self.assertEqual("B-002", bugs.delete(self.root, two["id"], "Reported twice"))
        self.assertFalse(os.path.exists(os.path.join(self.root, "testing", "bug-reports", "files", "B-002-1.png")),
                         "its screenshots go with it")
        doc = bugs.load(self.root)
        self.assertEqual([{"id": "B-002", "title": "Two", "reason": "Reported twice"}],
                         [{k: d[k] for k in ("id", "title", "reason")} for d in doc["deleted"]])
        self.assertEqual("B-003", bugs.add(self.root, "Three")["id"], "the deleted B-002 is not handed out again")
        with self.assertRaises(KeyError):
            bugs.delete(self.root, "B-002", "again")
        # A counter edited back by hand still never reuses an id, deleted ones included.
        path = os.path.join(self.root, "testing", "bug-reports.json")
        raw = json.loads(self.doc_text())
        raw["nextId"] = 1
        raw["bugs"] = [b for b in raw["bugs"] if b["id"] != "B-003"]
        with open(path, "w", encoding="ascii") as f:
            json.dump(raw, f)
        self.assertEqual("B-003", bugs.add(self.root, "Again")["id"], "the highest existing id is B-002, deleted")

    def test_screenshots_png_and_jpg_only_2mb_at_most_three_per_report(self):
        a = bugs.add(self.root, "Gump overlaps")
        self.assertEqual("B-001-1.png", bugs.add_shot(self.root, a["id"], PNG))
        self.assertEqual("B-001-2.jpg", bugs.add_shot(self.root, a["id"], JPG))
        for bad, why in ((b"GIF89a" + b"\x00" * 64, "a GIF"), (b"<svg></svg>", "text"), (b"", "empty")):
            with self.assertRaises(ValueError, msg=why):
                bugs.add_shot(self.root, a["id"], bad)
        big = b"\x89PNG\r\n\x1a\n" + b"\x00" * (2 * 1024 * 1024)
        with self.assertRaises(ValueError):
            bugs.add_shot(self.root, a["id"], big)
        self.assertEqual("B-001-3.png", bugs.add_shot(self.root, a["id"], PNG))
        with self.assertRaises(ValueError):
            bugs.add_shot(self.root, a["id"], PNG)                              # a fourth
        files = sorted(os.listdir(os.path.join(self.root, "testing", "bug-reports", "files")))
        self.assertEqual(["B-001-1.png", "B-001-2.jpg", "B-001-3.png"], files, "nothing refused was written")
        self.assertEqual(files, bugs.load(self.root)["bugs"][0]["shots"])
        self.assertEqual(PNG, bugs.decode_shot("data:image/png;base64," + base64.b64encode(PNG).decode("ascii")))
        with self.assertRaises(ValueError):
            bugs.decode_shot("not base64 at all!")
        with self.assertRaises(KeyError):
            bugs.shot_path(self.root, "../bug-reports.json")

    def test_mark_taken_moves_only_new_reports(self):
        a = bugs.add(self.root, "One")
        b = bugs.add(self.root, "Two")
        bugs.set_status(self.root, b["id"], "notbug", reason="By design")
        self.assertEqual([a["id"]], bugs.mark_taken(self.root, [a["id"], b["id"], "B-777"]))
        doc = bugs.load(self.root)
        self.assertEqual(["taken", "notbug"], [x["status"] for x in doc["bugs"]])
        self.assertEqual(1, bugs.summary(doc)["pending"], "taken with no D-number yet")
        self.assertTrue(doc["copiedAt"])


class BugCopyText(unittest.TestCase):
    def test_the_format_for_the_overseer(self):
        doc = bugs.new_doc()
        doc["bugs"] = [bugs.new_bug(id="B-001", title="Bare report", createdAt="2026-10-14T15:00:00Z"),
                       bugs.new_bug(id="B-002", title="Smelt eats ore", happened="Ore gone\nno ingots", expected="Ingots",
                                    steps="1. Mine\n2. Smelt", severity="wrong", area="crafting", playtest="P71-3",
                                    character="Tester", location="Minoc", version="2026.10.14.3 (test shard, 61db33c)",
                                    shots=["B-002-1.png"], createdAt="2026-10-14T15:01:00Z"),
                       bugs.new_bug(id="B-003", title="Not new", status="taken")]
        pts = {"items": [{"id": "P71-3", "label": "Fill a BOD from the backpack"}]}
        want = (
            "New bug reports from the play-test page (2), for D-numbers in docs/bug-list.md:\n"
            "\n"
            "B-001: Bare report\n"
            "Severity: (none)\n"
            "Area: (none)\n"
            "Linked play test: (none)\n"
            "Shard version: (unknown)\n"
            "Character: (none)\n"
            "Location: (none)\n"
            "Reported: 2026-10-14T15:00:00Z\n"
            "What happened: (none)\n"
            "Expected: (none)\n"
            "Steps: (none)\n"
            "Screenshots: (none)\n"
            "\n"
            "B-002: Smelt eats ore\n"
            "Severity: wrong\n"
            "Area: crafting\n"
            "Linked play test: P71-3 (Fill a BOD from the backpack)\n"
            "Shard version: 2026.10.14.3 (test shard, 61db33c)\n"
            "Character: Tester\n"
            "Location: Minoc\n"
            "Reported: 2026-10-14T15:01:00Z\n"
            "What happened:\n"
            "  Ore gone\n"
            "  no ingots\n"
            "Expected:\n"
            "  Ingots\n"
            "Steps:\n"
            "  1. Mine\n"
            "  2. Smelt\n"
            "Screenshots:\n"
            "  D:\\UO\\shard-migration\\testing\\bug-reports\\files\\B-002-1.png\n")
        self.assertEqual(want, bugs.copy_text(doc, pts, "D:\\UO\\shard-migration"))
        self.assertEqual("", bugs.copy_text(bugs.new_doc()))


class IdeaReasons(unittest.TestCase):
    """Part B: declining or deleting an idea needs a reason (Chase, Q17), and old declined ideas still load."""

    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="ideas-p97-")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_declining_and_deleting_need_a_reason_that_is_not_only_spaces(self):
        a = ideas.add(self.root, "Climbing gear")
        b = ideas.add(self.root, "Fishing nets")
        for r in ("", "   "):
            with self.assertRaises(ValueError):
                ideas.set_status(self.root, a["id"], "declined", reason=r)
            with self.assertRaises(ValueError):
                ideas.delete(self.root, b["id"], r)
        self.assertEqual("Covered by F-36", ideas.set_status(self.root, a["id"], "declined", reason="Covered by F-36")["reason"])
        self.assertEqual("I-002", ideas.delete(self.root, b["id"], "Same as I-001"))
        doc = ideas.load(self.root)
        self.assertEqual([("I-002", "Fishing nets", "Same as I-001")], [(d["id"], d["title"], d["reason"]) for d in doc["deleted"]])
        self.assertEqual("I-003", ideas.add(self.root, "Next")["id"], "a deleted id stays retired")

    def test_the_copy_lists_what_was_declined_or_deleted_since_with_its_reason(self):
        ideas.add(self.root, "Kept new")
        old = ideas.add(self.root, "Old decline")
        gone = ideas.add(self.root, "Gone")
        # An idea declined before reasons were required: no reason on file.
        path = os.path.join(self.root, "testing", "feature-ideas.json")
        raw = json.load(open(path, encoding="ascii"))
        for it in raw["ideas"]:
            if it["id"] == old["id"]:
                it.update(status="declined", reason="", statusAt="2026-10-13T10:00:00Z")
        raw.pop("deleted", None)
        raw.pop("copiedAt", None)
        with open(path, "w", encoding="ascii") as f:
            json.dump(raw, f)
        doc = ideas.load(self.root)                                   # the old file still loads
        self.assertEqual([], doc["deleted"])
        ideas.delete(self.root, gone["id"], "Not for this shard")
        text = ideas.copy_text(ideas.load(self.root))
        self.assertIn("I-001: Kept new\n", text)
        self.assertIn("Declined or deleted since the last copy (2):\n"
                      "I-002 (declined): Old decline\n  Reason: no reason recorded\n"
                      "I-003 (deleted): Gone\n  Reason: Not for this shard\n", text)
        ideas.mark_taken(self.root, ["I-001"])
        self.assertEqual("", ideas.copy_text(ideas.load(self.root)), "after the copy is marked, nothing repeats")


class Page(unittest.TestCase):
    """What the page's controls are wired to. The look was checked in a browser at 375 px, light and dark."""

    @classmethod
    def setUpClass(cls):
        if not PAGE.exists():
            raise unittest.SkipTest("no " + str(PAGE))
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_ascii_only(self):
        self.html.encode("ascii")

    def test_bug_from_this_on_every_play_test_card(self):
        card = self.html[self.html.index("function card(it)"):self.html.index("function api(")]
        self.assertIn('data-bug-from="', card, "the card builds a Bug from this button")
        self.assertLess(card.index("data-idea-from"), card.index("data-bug-from"), "next to Idea from this")
        self.assertIn("bugFrom(", self.html)

    def test_marking_a_fail_offers_a_bug_report_prefilled(self):
        self.assertIn("Report a bug for this?", self.html)
        i = self.html.index("Report a bug for this?")
        self.assertIn("bugFrom(", self.html[i:i + 400], "the offer opens quick add with the play test linked")

    def test_the_bugs_tab_and_its_parts(self):
        for want in ('data-f="bugs"', 'id="bugs-n"', 'id="bug-form"', 'id="b-sev"', 'id="b-area"', 'id="b-pt"',
                     'id="b-shots"', 'id="copy-bugs"', "/api/bugs/shot", "'paste'"):
            self.assertIn(want, self.html, want)


class ServiceRoutes(unittest.TestCase):
    def setUp(self):
        if not SERVER.exists():
            self.skipTest("no " + str(SERVER))
        self.root = tempfile.mkdtemp(prefix="bugs-svc-")
        for d in ("notes", "docs", "testing"):
            os.makedirs(os.path.join(self.root, d))
        shutil.copy(ROOT / "docs" / "feature-queue.md", os.path.join(self.root, "docs", "feature-queue.md"))
        self.deployed = os.path.join(self.root, "shard-commit.json")
        with open(self.deployed, "w", encoding="ascii") as f:
            json.dump({"commit": "61db33c5e52759eb19c371c3e0145918bd1694c5", "version": "2026.10.14.3"}, f)
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        self.port = s.getsockname()[1]
        s.close()
        self.proc = subprocess.Popen([sys.executable, "-B", str(SERVER), "--root", self.root, "--lib", str(TOOLS),
                                      "--bind", "127.0.0.1", "--port", str(self.port), "--status-page", os.devnull,
                                      "--deployed", self.deployed, "--host-root", "D:\\UO\\shard-migration"],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                self.get("/api/summary")
                return
            except OSError:
                time.sleep(0.1)
        self.fail("the service did not start")

    def tearDown(self):
        self.proc.terminate()
        self.proc.wait(10)
        shutil.rmtree(self.root, ignore_errors=True)

    def raw(self, path):
        with urllib.request.urlopen("http://127.0.0.1:%d%s" % (self.port, path), timeout=5) as r:
            return r.status, r.headers.get("Content-Type"), r.read()

    def get(self, path):
        return json.loads(self.raw(path)[2].decode("utf-8"))

    def post(self, path, body):
        req = urllib.request.Request("http://127.0.0.1:%d%s" % (self.port, path), data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode("utf-8"))

    def test_add_screenshot_copy_status_delete_and_count(self):
        self.assertEqual(0, self.get("/api/summary")["bugs_new"])
        code, j = self.post("/api/bugs/add", {"title": "Smelt eats ore", "severity": "wrong", "area": "crafting",
                                              "playtest": "P71-3", "version": "typed by hand"})
        self.assertEqual((200, "B-001"), (code, j["bug"]["id"]))
        self.assertEqual("2026.10.14.3 (test shard, 61db33c)", j["bug"]["version"], "the server fills it, never the page")
        self.assertEqual(400, self.post("/api/bugs/add", {"title": ""})[0])
        self.assertEqual(1, self.get("/api/summary")["bugs_new"])
        png = "data:image/png;base64," + base64.b64encode(PNG).decode("ascii")
        self.assertEqual((200, {"shot": "B-001-1.png"}), self.post("/api/bugs/shot", {"id": "B-001", "data": png}))
        gif = base64.b64encode(b"GIF89a" + b"\x00" * 10).decode("ascii")
        self.assertEqual(400, self.post("/api/bugs/shot", {"id": "B-001", "data": gif})[0], "wrong type")
        big = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"\x00" * (2 * 1024 * 1024 + 1)).decode("ascii")
        self.assertEqual(400, self.post("/api/bugs/shot", {"id": "B-001", "data": big})[0], "over 2 MB")
        status, ctype, body = self.raw("/api/bugs/file/B-001-1.png")
        self.assertEqual((200, "image/png", PNG), (status, ctype, body))
        with self.assertRaises(urllib.error.HTTPError):
            self.raw("/api/bugs/file/..%2Fbug-reports.json")
        doc = self.get("/api/bugs")
        self.assertEqual(["blocks play", "wrong", "annoying", "looks wrong"], doc["severities"])
        self.assertEqual(["B-001-1.png"], doc["bugs"][0]["shots"])
        cp = self.get("/api/bugs/copy")
        self.assertEqual(["B-001"], cp["ids"])
        self.assertIn("  D:\\UO\\shard-migration\\testing\\bug-reports\\files\\B-001-1.png\n", cp["text"])
        self.assertEqual((200, {"taken": ["B-001"]}), self.post("/api/bugs/taken", {"ids": cp["ids"]}))
        self.assertEqual(0, self.get("/api/summary")["bugs_new"])
        self.assertEqual(400, self.post("/api/bugs/status", {"id": "B-001", "status": "notbug"})[0], "no reason")
        self.assertEqual("D92", self.post("/api/bugs/status", {"id": "B-001", "status": "taken", "dnum": "D92"})[1]["bug"]["dnum"])
        self.assertEqual(400, self.post("/api/bugs/delete", {"id": "B-001"})[0], "a delete needs a reason")
        self.assertEqual((200, {"deleted": "B-001"}), self.post("/api/bugs/delete", {"id": "B-001", "reason": "test"}))
        self.assertEqual("B-002", self.post("/api/bugs/add", {"title": "Next"})[1]["bug"]["id"])

    def test_an_idea_delete_needs_a_reason_over_the_api(self):
        self.post("/api/ideas/add", {"title": "Climbing gear"})
        self.assertEqual(400, self.post("/api/ideas/delete", {"id": "I-001"})[0])
        self.assertEqual(200, self.post("/api/ideas/delete", {"id": "I-001", "reason": "Covered by F-36"})[0])


if __name__ == "__main__":
    unittest.main()
