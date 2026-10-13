"""cc-P85: the status dashboard's derived facts, its freshness, and judge.py.

    python -m unittest tools/tests/test_status_dashboard.py

Every fact works in a temporary folder with fixture files; nothing reads the real queue, autopilot or notes except
the last fact, which checks the real progress-state.json is well formed. Standard library only. ASCII only.
"""
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import progress  # noqa: E402
import render_dashboard as rd  # noqa: E402
import judge  # noqa: E402


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class QueueAndCounts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        notes, prompts, ap = self.root / "notes", self.root / "prompts", self.root / "autopilot"
        write(notes / "cc-P10-old-thing.md", "body\n\nP10 DONE\n")
        write(notes / "cc-P11-gave-up.md", "body\nP11 STOPPED: needs a decision\n")
        write(notes / "cc-P12-running.md", "half written\n")
        write(notes / "cc-P13-wrong-number.md", "body\nP99 DONE\n")       # a mismatched number is not finished
        write(notes / "passdown.md", "P1 DONE\n")                         # not a prompt note
        write(prompts / "queue" / "cc-P14-next-up.md", "x")
        write(prompts / "queue" / "cc-P12-running.md", "x")               # still in the queue folder while running
        write(ap / "state.json", json.dumps({"current": "P12", "currentFile": "cc-P12-running.md", "startedAt": "2026-10-13T01:00:00"}))
        write(ap / "ENABLED", "")
        self.q = progress.queue_state(notes, prompts, ap)

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_prompt_has_its_state(self):
        self.assertEqual(self.q["autopilot"], "on")
        self.assertEqual(self.q["running"]["n"], 12)
        self.assertEqual([r["n"] for r in self.q["queued"]], [14], "running is not also queued")
        self.assertEqual([(r["n"], r["state"]) for r in self.q["finished"]], [(11, "stopped"), (10, "done")])
        self.assertEqual(self.q["finished"][0]["why"], "needs a decision")
        self.assertEqual(self.q["latest_done"]["n"], 10, "a STOPPED prompt is not the latest done")
        self.assertEqual(self.q["stopped_total"], 1)

    def test_a_finished_prompt_is_no_longer_running_or_queued(self):
        write(self.root / "notes" / "cc-P12-running.md", "done now\nP12 DONE\n")
        q = progress.queue_state(self.root / "notes", self.root / "prompts", self.root / "autopilot")
        self.assertIsNone(q["running"])
        self.assertEqual([r["n"] for r in q["queued"]], [14])

    def test_autopilot_off_without_enabled(self):
        (self.root / "autopilot" / "ENABLED").unlink()
        q = progress.queue_state(self.root / "notes", self.root / "prompts", self.root / "autopilot")
        self.assertEqual(q["autopilot"], "off")

    def test_play_test_counts_come_from_the_files_own_summary(self):
        p = self.root / "play-tests.json"
        write(p, json.dumps({"schema": 1, "summary": {"open": 5, "failed": 1, "passed": 2, "later": 0, "blocked": 0, "total": 8, "unloggedFails": 1, "generatedAt": "2026-10-12T21:21:17Z"}, "items": []}))
        c = progress.playtest_counts(p)
        self.assertEqual((c["open"], c["failed"], c["passed"], c["total"]), (5, 1, 2, 8))
        self.assertIsNone(progress.playtest_counts(self.root / "missing.json"))

    def test_the_review_date_is_the_newest_confirmed_anywhere(self):
        st = {"a": {"confirmed": "2026-09-01"}, "b": [{"confirmed": "2026-10-02"}, {"x": {"confirmed": "2026-10-01"}}],
              "c": {"confirmed": "not a date"}}
        self.assertEqual(progress.newest_confirmed(st), "2026-10-02")
        self.assertEqual(progress.newest_confirmed({}), "")


class Freshness(unittest.TestCase):
    def pg(self, reviewed):
        return {"derived": {"reviewed": reviewed, "stale_days": 7}}

    def test_reviewed_is_plain_when_fresh_and_amber_when_older_than_seven_days(self):
        today = datetime.now().strftime("%Y-%m-%d")
        old = (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d")
        edge = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        self.assertIn('class="reviewed"', rd.reviewed_html(self.pg(today)))
        self.assertIn('class="reviewed"', rd.reviewed_html(self.pg(edge)), "7 days is not yet stale")
        self.assertIn('class="reviewed stale"', rd.reviewed_html(self.pg(old)))
        self.assertIn('class="reviewed stale"', rd.reviewed_html(self.pg("")), "never reviewed is stale")
        self.assertIn("Judgment reviewed " + old, rd.reviewed_html(self.pg(old)))

    def test_a_section_says_its_own_date_only_when_it_differs(self):
        self.assertEqual(rd.asof_html("2026-10-13", "2026-10-13"), "")
        self.assertEqual(rd.asof_html("", "2026-10-13"), "")
        self.assertIn("As of 2026-09-19", rd.asof_html("2026-09-19", "2026-10-13"))

    def test_the_queue_and_play_tests_render_their_rows(self):
        pg = {"derived": {"queue": {"autopilot": "on", "running": {"n": 12, "slug": "a-b", "state": "running", "since": "t"},
                                    "queued": [{"n": 14, "slug": "c", "state": "queued"}],
                                    "finished": [{"n": 11, "slug": "d", "state": "stopped", "why": "x", "date": "2026-10-12"}],
                                    "finished_total": 1, "stopped_total": 1, "latest_done": None},
                          "playtests": {"open": 3, "failed": 1, "passed": 2, "later": 0, "blocked": 0, "total": 6, "unloggedFails": 1}}}
        q = rd.queue_html(pg)
        for want in ("P12 running", "p-next", "P14", "p-todo", "P11", "p-no"):
            self.assertIn(want, q)
        t = rd.playtests_html(pg)
        self.assertIn("3 open", t)
        self.assertIn("not yet in the bug list", t)
        self.assertIn('data-port="8093"', t, "the link is rebuilt from the host the browser used")

    def test_the_page_links_never_say_localhost(self):
        page = (HERE.parent.parent / "dashboard.html").read_text(encoding="utf-8")
        self.assertNotIn("localhost", page)
        self.assertIn('data-port="8093"', page)
        # cc-P88 replaced the header's two links with the shared menu (nav.js, inlined in DATA:NAV): Homepage is its
        # Dashboard entry, on port 3000 of the host the browser used.
        self.assertIn("key: 'dashboard', label: 'Dashboard',    host: null, port: 3000", page)


class Judge(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.state = Path(self.tmp.name) / "s.json"
        self.state.write_text(json.dumps({
            "shard_status": {"text": "x", "confirmed": "2026-09-01"},
            "direction": {"title": "d", "confirmed": "2026-09-01"},
            "playable_gates": {"gates": [{"name": "Things to fight", "done": False, "detail": "old", "confirmed": "2026-09-01"},
                                         {"name": "Things to see", "done": False, "detail": "old", "confirmed": "2026-09-01"}]},
            "sections": {"backlog": "2026-09-01"},
            "tasks": [{"id": "C4", "title": "Creatures", "status": "todo", "note": "", "confirmed": "2026-09-01"}]}), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def j(self, *args):
        return judge.run(["--state", str(self.state), "--date", "2026-10-13", *args])

    def st(self):
        return json.loads(self.state.read_text(encoding="utf-8"))

    def test_a_gate_is_changed_and_dated(self):
        self.j("gate", "Things to fight", "--done", "yes", "--detail", "new", "--source", "a", "--source", "b")
        g = self.st()["playable_gates"]["gates"][0]
        self.assertEqual((g["done"], g["detail"], g["sources"], g["confirmed"]), (True, "new", ["a", "b"], "2026-10-13"))
        self.assertEqual(self.st()["playable_gates"]["gates"][1]["confirmed"], "2026-09-01", "only that gate")

    def test_an_ambiguous_gate_name_is_refused(self):
        with self.assertRaises(SystemExit):
            self.j("gate", "Things to", "--done", "yes")
        self.assertEqual(self.st()["playable_gates"]["gates"][0]["done"], False)

    def test_tasks_are_updated_added_and_retired(self):
        self.j("task", "C4", "--status", "in-progress")
        self.assertEqual(self.st()["tasks"][0]["status"], "in-progress")
        self.j("add-task", "F-50", "--title", "New")
        self.assertEqual([t["id"] for t in self.st()["tasks"]], ["C4", "F-50"])
        self.j("retire-task", "C4")
        self.assertEqual([t["id"] for t in self.st()["tasks"]], ["F-50"])

    def test_confirm_moves_only_the_date_and_the_review_date_follows(self):
        self.j("confirm", "section", "backlog")
        self.assertEqual(self.st()["sections"]["backlog"], "2026-10-13")
        self.assertEqual(self.st()["playable_gates"]["gates"][0]["detail"], "old")
        self.j("confirm", "all")
        self.assertEqual(progress.newest_confirmed(self.st()), "2026-10-13")


class TheRealStateFile(unittest.TestCase):
    def test_every_gate_and_task_has_a_date_and_every_gate_a_source(self):
        st = json.loads((HERE.parent / "progress-state.json").read_text(encoding="utf-8"))
        for g in st["playable_gates"]["gates"]:
            self.assertRegex(g.get("confirmed", ""), r"^\d{4}-\d{2}-\d{2}$", g["name"])
            self.assertTrue(g.get("sources"), g["name"] + " cites nothing")
        for t in st["tasks"]:
            self.assertRegex(t.get("confirmed", ""), r"^\d{4}-\d{2}-\d{2}$", t["id"])
            self.assertIn(t["status"], ("todo", "in-progress", "blocked", "done"))
        self.assertRegex(st["shard_status"]["confirmed"], r"^\d{4}-\d{2}-\d{2}$")
        raw = (HERE.parent / "progress-state.json").read_bytes()
        self.assertTrue(all(b < 128 for b in raw), "ASCII only")


if __name__ == "__main__":
    unittest.main()
