"""cc-P112: the robot icons on the play-test page.

    python -m unittest discover -s tools\\tests -p "test_bot_tonight.py"

Shaping (tools/bottonight.py), the service's GET /api/bot-tonight and report view (docker/test-queue/server.py, started
on a free port with a scratch root, as test_haven_h1 does), and the page (html/index.html, read as text: what it is wired
to, not how it looks). The plan files here are made up; the real plan is checked against the runner in the notes.
"""
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
import bottonight  # noqa: E402

PLAN = {"schema": 1, "generatedAt": "2026-10-14T22:49:32Z", "available": True, "commit": "b58ef94" + "0" * 33,
        "short": "b58ef94", "run": True, "minutes": 166,
        "tonight": {"P64-1": {"reason": "code changed since 10f4088", "minutes": 2}},
        "checkable": ["T-047", "C-7", "P64-1"],
        "last": {"P64-1": {"result": "PASS", "run": "2026-10-13-1428", "at": "2026-10-13T19:28:00Z"},
                 "T-047": {"result": "ERROR", "run": "2026-10-14-0817", "at": "2026-10-14T13:17:00Z"}}}


class Shape(unittest.TestCase):
    def test_tonight_gets_the_robot_checkable_the_dim_robot_the_rest_nothing(self):
        s = bottonight.shape(PLAN, "file", lambda stamp: stamp == "2026-10-14-0817")
        self.assertTrue(s["available"])
        self.assertEqual(1, s["count"], "the header count is tonight's items only")
        self.assertEqual("tonight", s["items"]["P64-1"]["state"])
        self.assertEqual("checkable", s["items"]["T-047"]["state"])
        self.assertEqual("checkable", s["items"]["C-7"]["state"])
        self.assertNotIn("E-1", s["items"], "no icon for an item the bot cannot check")
        self.assertEqual("The overnight bot tries this tonight (about 2 min). Plan as of 2026-10-14 22:49 UTC.",
                         s["items"]["P64-1"]["title"])
        self.assertTrue(s["items"]["T-047"]["title"].startswith("Bot-checkable; already checked on this code. Last bot result: could not run, 2026-10-14"))
        self.assertIn("no bot check is built", s["items"]["C-7"]["title"])

    def test_the_newest_result_shows_with_a_report_link_only_when_that_report_exists(self):
        s = bottonight.shape(PLAN, "file", lambda stamp: stamp == "2026-10-14-0817")
        self.assertEqual({"result": "ERROR", "label": "could not run", "run": "2026-10-14-0817", "at": "2026-10-14T13:17:00Z",
                          "report": "/bot-runs/2026-10-14-0817/report?item=T-047#item-T-047"}, s["items"]["T-047"]["last"])
        self.assertNotIn("report", s["items"]["P64-1"]["last"], "no report file, no link")
        self.assertEqual("pass", s["items"]["P64-1"]["last"]["label"])
        self.assertIsNone(s["items"]["C-7"]["last"])
        for result, label in (("FAIL", "fail"), ("FLAKY", "flaky")):
            p = dict(PLAN, last={"C-7": {"result": result, "run": "2026-10-14-0817", "at": ""}})
            self.assertEqual(label, bottonight.shape(p, "file")["items"]["C-7"]["last"]["label"])

    def test_anything_wrong_is_unavailable_never_an_error(self):
        for bad, why in ((None, "no bot plan"), ({"schema": 2}, "no bot plan"), ("text", "no bot plan"),
                         ({"schema": 1, "available": False, "error": "not a commit in D:\\x: HEAD"}, "not a commit")):
            s = bottonight.shape(bad, "file")
            self.assertFalse(s["available"])
            self.assertIn(why, s["reason"])
            self.assertEqual({}, s["items"])
        self.assertIn("snapshot", bottonight.shape(None, "snapshot")["reason"])

    def test_the_report_page_anchors_every_item_row_and_marks_the_asked_one(self):
        md = "# Overnight\n\n| Id | Result |\n|---|---|\n| T-047 | PASS | <b> |\n| P64-1 | FAIL |\n"
        h = bottonight.report_html(md, "P64-1")
        self.assertIn('<span id="item-T-047">| T-047 | PASS | &lt;b&gt; |</span>', h)
        self.assertIn('<span id="item-P64-1" class="hit">', h)
        self.assertNotIn('id="item-Id"', h)


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class Service(unittest.TestCase):
    def start(self, extra=()):
        self.root = tempfile.mkdtemp(prefix="p112-root-")
        for d in ("notes", "docs", "testing"):
            os.makedirs(os.path.join(self.root, d))
        shutil.copy(ROOT / "docs" / "feature-queue.md", os.path.join(self.root, "docs", "feature-queue.md"))
        self.port = free_port()
        e = {k: v for k, v in os.environ.items() if not k.startswith(("PLAYTESTS_", "ACCESS_", "REPO_STAMP"))}
        self.proc = subprocess.Popen([sys.executable, "-B", str(SERVER), "--root", self.root, "--lib", str(TOOLS),
                                      "--bind", "127.0.0.1", "--port", str(self.port), "--status-page", os.devnull,
                                      "--deployed", os.devnull] + list(extra),
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

    def bot(self):
        code, raw = self.get("/api/bot-tonight")
        self.assertEqual(200, code)
        return json.loads(raw.decode("utf-8"))

    def write(self, base, rel, obj):
        p = os.path.join(base, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(obj if isinstance(obj, str) else json.dumps(obj))

    def test_the_game_pc_file_gives_the_items_and_is_cached_five_minutes(self):
        self.start()
        self.write(self.root, "testing/bot-tonight.json", PLAN)
        self.write(self.root, "testing/bot-runs/2026-10-14-0817/report.md", "| T-047 | ERROR |\n")
        b = self.bot()
        self.assertEqual(("file", 1, "tonight"), (b["source"], b["count"], b["items"]["P64-1"]["state"]))
        self.assertEqual("/bot-runs/2026-10-14-0817/report?item=T-047#item-T-047", b["items"]["T-047"]["last"]["report"])
        self.write(self.root, "testing/bot-tonight.json", dict(PLAN, tonight={}))
        self.assertEqual(1, self.bot()["count"], "within 5 minutes the cached plan is served")
        code, raw = self.get("/bot-runs/2026-10-14-0817/report?item=T-047")
        self.assertEqual(200, code)
        self.assertIn(b'<span id="item-T-047" class="hit">', raw)
        self.assertEqual(404, self.get("/bot-runs/..%2F..%2Fnotes/report")[0])
        self.assertEqual(404, self.get("/bot-runs/2026-01-01-0000/report")[0])

    def test_no_plan_is_a_quiet_unavailable_not_an_error(self):
        self.start()
        b = self.bot()
        self.assertFalse(b["available"])
        self.assertEqual({}, b["items"])

    def test_haven_mode_reads_the_plan_from_the_game_pc_snapshot(self):
        self.data = tempfile.mkdtemp(prefix="p112-data-")
        self.start(extra=["--data", self.data])
        self.write(self.data, os.path.join("ops", "gamepc.json"),
                   {"receivedAt": "2026-10-14T22:50:00Z", "snapshot": {"schema": 1, "botTonight": PLAN}})
        self.write(self.root, "testing/bot-runs/2026-10-14-0817/report.md", "| T-047 | ERROR |\n")
        b = self.bot()
        self.assertTrue(b["available"], b)
        self.assertEqual(("snapshot", "2026-10-14 22:49 UTC"), (b["source"], b["asOf"]))
        self.assertIn("Plan as of 2026-10-14 22:49 UTC", b["items"]["P64-1"]["title"])
        self.assertIn("report", b["items"]["T-047"]["last"], "on Haven the runs are in the notes clone")


class Page(unittest.TestCase):
    def setUp(self):
        self.t = PAGE.read_text(encoding="utf-8")

    def test_the_robots_come_from_the_service_and_only_mark_items(self):
        self.assertIn("api('/api/bot-tonight')", self.t)
        self.assertIn("Promise.all([a, b, c, d])", self.t)
        self.assertIn("'<span class=\"robot\" data-bot=\"tonight\" title=\"' + esc(b.title) + '\">&#129302;</span>'", self.t)
        self.assertIn("'<span class=\"robot dim\" data-bot=\"checkable\" title=\"' + esc(b.title) + '\">&#129302;</span>'", self.t)
        self.assertIn("var rb = robot(it);", self.t)
        self.assertIn(".robot.dim { opacity: .38;", self.t)

    def test_the_filter_is_an_extra_and_open_stays_the_default(self):
        self.assertIn('<button data-f="bot" aria-pressed="false"', self.t)
        self.assertIn("if (filter === 'bot') return botInfo(it.id).state === 'tonight';", self.t)
        self.assertIn("var filter = 'open';", self.t)
        self.assertIn('<button data-f="open" aria-pressed="true">Open</button>', self.t)

    def test_the_header_count_and_the_quiet_line(self):
        self.assertIn("'\">Bot tonight: ' + bot.count + '</span>'", self.t)
        self.assertIn("Bot plan unavailable", self.t)
        self.assertIn("botCount();", self.t)
        self.assertIn("[data-go=\"bot\"]", self.t)

    def test_a_result_chip_links_to_the_runs_report(self):
        self.assertIn("'bot: ' + b.last.label", self.t)
        self.assertIn("'<a class=\"chip bot bot-' + esc(b.last.result) + '\" href=\"' + esc(b.last.report) + '\"", self.t)
        self.assertNotIn("data-s=\"pass\"' + b", self.t, "the bot never marks a result")

    def test_the_source_stays_ascii(self):
        self.assertNotIn("\U0001F916", self.t)


if __name__ == "__main__":
    unittest.main()
