"""cc-P136: the status page keeps its own judgments current, and lists what still needs the overseer.

    python -m unittest tools/tests/test_self_judging.py

The derived rules (a system whose files are all in is in; a task a port-list system covers is not counted twice; a
STOPPED prompt is never progress; next to land follows the port list), the "Needs overseer review" box (owed and
empty), judge.py's needs-confirm mark and dated retirement, and the real state file with C2-C7 and S7 retired. Every
fact works in a temporary folder; nothing reads the real queue or notes except the last class. Standard library only.
ASCII only.
"""
import json
import os
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import progress  # noqa: E402
import render_dashboard as rd  # noqa: E402
import judge  # noqa: E402

TODAY = date(2026, 10, 20)


def write(path, text, mdate=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if mdate:
        t = __import__("datetime").datetime.strptime(mdate, "%Y-%m-%d").timestamp() + 12 * 3600
        os.utime(path, (t, t))


def system(title, done, files, covers=(), tier="port"):
    return {"id": title.lower(), "tier": tier, "title": title, "feeds": "", "why": "", "candidates": files,
            "done": done, "complete": files > 0 and done == files, "covers": list(covers)}


def state(**over):
    st = {"shard_status": {"text": "x", "confirmed": "2026-10-19"},
          "direction": {"title": "d", "confirmed": "2026-10-14"},
          "playable_gates": {"gates": [{"name": "Things to fight", "done": False, "confirmed": "2026-10-19"}]},
          "tasks": [{"id": "DEPLOY", "title": "Deploy P65-P84", "status": "todo", "note": "", "confirmed": "2026-10-19"}]}
    st.update(over)
    return st


class DerivedRules(unittest.TestCase):
    def test_a_system_is_in_exactly_when_every_file_is_ported(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for f in ("Services/A/One.cs", "Services/A/Two.cs", "Services/B/Three.cs"):
            write(root / "servuo" / "Scripts" / f, "//")
        write(root / "shard" / "server" / "customizations" / "One.cs", "//")
        write(root / "shard" / "server" / "customizations" / "Two.cs", "//")
        write(root / "stems.txt", "\n")
        write(root / "pl.json", json.dumps({"systems": [
            {"id": "a", "tier": "port", "title": "A", "prefixes": ["Services/A/"], "covers": ["C2"]},
            {"id": "b", "tier": "port", "title": "B", "prefixes": ["Services/B/"]}]}))
        pl = progress.port_list(root / "pl.json", root / "servuo", root / "shard", root / "stems.txt")
        self.assertEqual([r["complete"] for r in pl["systems"]], [True, False])
        self.assertEqual(pl["counted"]["in"], 1)
        self.assertEqual(pl["next"], "B", "next to land is the first port row in list order that is not in")
        self.assertEqual(pl["systems"][0]["covers"], ["C2"], "the covers list is carried to the page")

    def test_a_task_a_port_list_system_covers_is_shown_as_covered_not_counted(self):
        pl = {"systems": [system("Creatures", 5, 10, covers=["C4"]), system("Wrong", 3, 3, covers=["C2"]),
                          system("Exodus", 1, 4, covers=["C2"])]}
        tasks = [{"id": "C4", "title": "Creatures and NPCs", "status": "todo"},
                 {"id": "c2", "title": "Revamped Dungeons", "status": "todo"},
                 {"id": "F-12", "title": "Levels", "status": "todo"}]
        own, covered = progress.split_tasks(tasks, pl)
        self.assertEqual([t["id"] for t in own], ["F-12"])
        self.assertEqual([(c["id"], c["by"], c["in"]) for c in covered],
                         [("C4", ["Creatures"], False), ("c2", ["Wrong", "Exodus"], False)])
        self.assertEqual((covered[1]["done"], covered[1]["files"]), (4, 7))
        own, covered = progress.split_tasks(tasks, {"systems": [system("Wrong", 3, 3, covers=["C2"])]})
        self.assertTrue(covered[0]["in"], "covered and every covering system in")
        self.assertEqual(progress.split_tasks(tasks, None), (tasks, []), "no port list: nothing is covered")

    def test_a_stopped_prompt_never_counts_as_done(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        notes = Path(tmp.name) / "notes"
        write(notes / "cc-P10-a.md", "x\nP10 DONE\n")
        write(notes / "cc-P11-b.md", "x\nP11 STOPPED: needs Chase\n")
        q = progress.queue_state(notes, Path(tmp.name) / "prompts", Path(tmp.name) / "ap")
        self.assertEqual((q["done_total"], q["stopped_total"]), (1, 1))
        html = rd.queue_html({"derived": {"queue": q}})
        self.assertIn("1 prompts done", html)
        self.assertNotIn("2 prompts", html, "a stopped prompt is not added to the done count")


class ReviewBox(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.notes = Path(self.tmp.name) / "notes"
        self.notes.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def owed(self, st, finished=()):
        return progress.review_owed(st, list(finished), self.notes, TODAY)

    def test_nothing_owed_gives_an_empty_box(self):
        write(self.notes / "decisions-2026-10-14.md", "x")
        self.assertEqual(self.owed(state()), [])
        html = rd.review_html({"review": []})
        self.assertIn("Nothing owed", html)
        self.assertNotIn("<li", html)

    def test_a_gate_marked_needs_confirm_is_owed_and_never_set(self):
        st = state(playable_gates={"gates": [{"name": "Things to fight", "done": False, "confirmed": "2026-10-19",
                                              "needs_confirm": "Chase: is 138 of 193 creatures enough?"}]})
        lines = self.owed(st)
        self.assertEqual(len(lines), 1)
        self.assertIn("Chase: is 138 of 193", lines[0]["check"])
        self.assertIn('python tools/judge.py gate "Things to fight" --done yes', "\n".join(lines[0]["cmd"]))
        self.assertIn('python tools/judge.py confirm gate "Things to fight"', "\n".join(lines[0]["cmd"]))
        self.assertFalse(st["playable_gates"]["gates"][0]["done"], "the review never decides")

    def test_a_gate_or_status_older_than_seven_days_is_owed(self):
        st = state(playable_gates={"gates": [{"name": "Somewhere to go", "done": False, "confirmed": "2026-10-12"},
                                             {"name": "Fresh", "done": False, "confirmed": "2026-10-13"}]},
                   shard_status={"text": "x", "confirmed": "2026-10-01"})
        lines = self.owed(st)
        self.assertEqual([x["item"] for x in lines], ["Somewhere to go", "shard status"], "7 days is still fresh")
        self.assertIn('python tools/judge.py confirm gate "Somewhere to go"', "\n".join(lines[0]["cmd"]))
        self.assertIn("python tools/judge.py status", "\n".join(lines[1]["cmd"]))

    def test_a_task_row_untouched_while_a_related_prompt_finished_is_owed(self):
        st = state(tasks=[{"id": "DEPLOY", "title": "Deploy P65-P84", "status": "todo", "note": "",
                           "confirmed": "2026-10-10"},
                          {"id": "TUTORIAL", "title": "Trials", "status": "todo", "note": "P80 built",
                           "confirmed": "2026-10-10"},
                          {"id": "WIPE", "title": "Wipe", "status": "todo", "note": "P90", "confirmed": "2026-10-19"}])
        finished = [{"n": 70, "state": "done", "date": "2026-10-15"},      # in DEPLOY's range, after its date
                    {"n": 80, "state": "stopped", "date": "2026-10-15"},   # stopped: not progress
                    {"n": 90, "state": "done", "date": "2026-10-19"}]      # WIPE was confirmed that day
        lines = self.owed(st, finished)
        self.assertEqual([x["item"] for x in lines], ["DEPLOY"])
        self.assertIn("P70", lines[0]["check"])
        self.assertIn("python tools/judge.py task DEPLOY --status", "\n".join(lines[0]["cmd"]))
        self.assertIn("python tools/judge.py confirm task DEPLOY", "\n".join(lines[0]["cmd"]))

    def test_a_prompt_finished_before_the_row_was_confirmed_owes_nothing(self):
        st = state(tasks=[{"id": "DEPLOY", "title": "Deploy P65-P84", "status": "todo", "note": "",
                           "confirmed": "2026-10-10"}])
        self.assertEqual(self.owed(st, [{"n": 70, "state": "done", "date": "2026-10-09"}]), [])

    def test_direction_older_than_the_newest_decisions_note_is_owed(self):
        write(self.notes / "decisions-2026-10-14.md", "x")
        write(self.notes / "bod-choice-decision-2026-10-16.md", "x")
        lines = self.owed(state())
        self.assertEqual([x["item"] for x in lines], ["direction"])
        self.assertIn("notes/bod-choice-decision-2026-10-16.md", lines[0]["check"])
        self.assertIn("python tools/judge.py confirm direction", "\n".join(lines[0]["cmd"]))

    def test_the_box_lists_each_line_with_its_command(self):
        html = rd.review_html({"review": [{"kind": "gate", "item": "Things to fight", "check": "Is it <met>?",
                                           "cmd": ['python tools/judge.py confirm gate "Things to fight"']}]})
        self.assertIn("1 item", html)
        self.assertIn("Is it &lt;met&gt;?", html)
        self.assertIn("<code>python tools/judge.py confirm gate &quot;Things to fight&quot;</code>", html)

    def test_a_review_that_could_not_be_computed_does_not_read_as_empty(self):
        html = rd.review_html({"review": None})
        self.assertNotIn("Nothing owed", html)
        self.assertIn("could not be worked out", html)


class Refresh(unittest.TestCase):
    def test_a_failing_rule_writes_one_line_and_the_refresh_carries_on(self):
        import io
        from contextlib import redirect_stderr
        err = io.StringIO()
        with redirect_stderr(err):
            got = progress.safely("review box", lambda: 1 / 0, None)
        self.assertIsNone(got)
        self.assertEqual(len(err.getvalue().strip().splitlines()), 1)
        self.assertIn("review box", err.getvalue())

    def test_the_commit_script_still_never_lets_the_refresh_block(self):
        ps = Path(r"D:\UO\Commit-ShardWork.ps1")
        if not ps.exists():
            self.skipTest("commit script not on this machine")
        t = ps.read_text(encoding="utf-8", errors="replace")
        self.assertIn("tools\\progress.py", t)
        self.assertIn("committing anyway", t)
        self.assertIn("$dashReason", t, "the one failure line says why")


class JudgeMarks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.state = Path(self.tmp.name) / "s.json"
        self.state.write_text(json.dumps(state(tasks=[{"id": "C3", "title": "High Seas", "status": "todo",
                                                       "note": "", "confirmed": "2026-10-01"}],
                                               tasks_retired=[])), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def j(self, *a):
        return judge.run(["--state", str(self.state), "--date", "2026-10-17", *a])

    def st(self):
        return json.loads(self.state.read_text(encoding="utf-8"))

    def test_needs_confirm_survives_confirm_all_and_clears_only_on_a_decision(self):
        self.j("gate", "Things to fight", "--needs-confirm", "Chase: enough creatures?")
        self.assertEqual(self.st()["playable_gates"]["gates"][0]["needs_confirm"], "Chase: enough creatures?")
        self.j("confirm", "all")
        self.assertIn("needs_confirm", self.st()["playable_gates"]["gates"][0], "a bulk re-date never decides")
        self.j("gate", "Things to fight", "--detail", "recounted")
        self.assertIn("needs_confirm", self.st()["playable_gates"]["gates"][0], "a detail edit is not a decision")
        self.j("confirm", "gate", "Things to fight")
        self.assertNotIn("needs_confirm", self.st()["playable_gates"]["gates"][0])

    def test_retire_task_keeps_the_row_with_its_date_and_why(self):
        self.j("retire-task", "C3", "--why", "covered by the port list (High Seas, fishing half)")
        st = self.st()
        self.assertEqual(st["tasks"], [])
        self.assertEqual(st["tasks_retired"], [{"id": "C3", "title": "High Seas", "retired": "2026-10-17",
                                                "why": "covered by the port list (High Seas, fishing half)"}])


class TheRealFiles(unittest.TestCase):
    def test_c2_to_c7_and_s7_are_retired_and_gone_from_the_totals(self):
        st = json.loads((HERE.parent / "progress-state.json").read_text(encoding="utf-8"))
        live = {t["id"] for t in st["tasks"]}
        retired = {t["id"]: t for t in st["tasks_retired"]}
        for tid in ("C2", "C3", "C4", "C5", "C6", "C7", "S7"):
            self.assertNotIn(tid, live)
            self.assertIn(tid, retired)
        for tid in ("C2", "C3", "C4", "C5", "C7", "S7"):
            self.assertEqual(retired[tid]["retired"], "2026-10-17", tid)
            self.assertIn("port list", retired[tid]["why"], tid)

    def test_every_retired_row_names_the_port_list_system_that_covers_it(self):
        pl = json.loads((HERE.parent / "port-list.json").read_text(encoding="utf-8"))
        covered = {c for s in pl["systems"] for c in s.get("covers", [])}
        self.assertTrue({"C2", "C3", "C4", "C5", "C7", "S7"} <= covered)


if __name__ == "__main__":
    unittest.main()
