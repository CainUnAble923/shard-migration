"""cc-P90: the feature-ideas inbox (tools/ideas.py) and its routes in the play-test service.

    python -m unittest tools/tests/test_feature_ideas.py

Every fact works in a temporary folder. The only real file read is docs/feature-queue.md, by the parser facts, which
never write. The service fact starts D:\\ShatteredLegacy\\docker\\test-queue\\server.py on a free local port against a
temporary root and stops it afterwards; it is skipped if that file is not there. Standard library only. ASCII only.
"""
import json
import multiprocessing
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import ideas  # noqa: E402

SERVER = Path(os.environ.get("SL_SHARD", r"D:\ShatteredLegacy")) / "docker" / "test-queue" / "server.py"


def _add_many(root, n, tag, go):
    sys.path.insert(0, str(TOOLS))
    import ideas as i2
    go.wait(30)                       # both writers start at the same moment
    for k in range(n):
        i2.add(root, "%s idea %d" % (tag, k))


class IdeasStore(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="ideas-")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def read(self):
        with open(os.path.join(self.root, "testing", "feature-ideas.json"), "r", encoding="ascii") as f:
            return f.read()

    def test_add_gives_the_next_id_and_writes_stable_pretty_json(self):
        a = ideas.add(self.root, "  Bank   deposit from the pack ", "Two lines\n  of text  ", "crafting", "P71-3")
        b = ideas.add(self.root, "Second")
        self.assertEqual(("I-001", "I-002"), (a["id"], b["id"]))
        self.assertEqual("Bank deposit from the pack", a["title"])
        self.assertEqual("Two lines\nof text", a["description"])
        self.assertEqual(("crafting", "P71-3", "new"), (a["area"], a["playtest"], a["status"]))
        text = self.read()
        doc = json.loads(text)
        self.assertEqual(["schema", "nextId", "copiedAt", "ideas", "deleted"], list(doc))
        self.assertEqual(list(ideas.new_idea()), list(doc["ideas"][0]))
        self.assertEqual(3, doc["nextId"])
        self.assertTrue(text.endswith("}\n") and "\n  \"ideas\": [" in text, "pretty-printed, one trailing newline")
        self.assertFalse(os.path.exists(os.path.join(self.root, "testing", "feature-ideas.json.tmp")), "no temp file left")
        self.assertFalse(os.path.exists(os.path.join(self.root, "testing", "feature-ideas.json.lock")), "lock released")

    def test_bad_input_is_refused_and_nothing_is_written(self):
        for kw in ({"title": "  "}, {"title": "x", "area": "fishing"}, {"title": "x", "playtest": "nonsense"}):
            with self.assertRaises(ValueError):
                ideas.add(self.root, **kw)
        self.assertFalse(os.path.exists(os.path.join(self.root, "testing", "feature-ideas.json")))

    def test_edit_changes_only_what_is_given(self):
        a = ideas.add(self.root, "Old title", "Old text", "combat")
        e = ideas.edit(self.root, a["id"], title="New title", area="")
        self.assertEqual(("New title", "Old text", ""), (e["title"], e["description"], e["area"]))
        self.assertEqual(a["createdAt"], e["createdAt"])
        with self.assertRaises(KeyError):
            ideas.edit(self.root, "I-999", title="x")

    def test_status_changes_and_their_rules(self):
        a = ideas.add(self.root, "Climbing gear")
        self.assertEqual("taken", ideas.set_status(self.root, a["id"], "taken")["status"])
        b = ideas.set_status(self.root, a["id"], "became", feature="f-44")
        self.assertEqual(("became", "F-44", ""), (b["status"], b["feature"], b["reason"]))
        with self.assertRaises(ValueError):
            ideas.set_status(self.root, a["id"], "became")                  # no F-number
        with self.assertRaises(ValueError):
            ideas.set_status(self.root, a["id"], "declined")                # no reason
        with self.assertRaises(ValueError):
            ideas.set_status(self.root, a["id"], "done")                    # not a status
        d = ideas.set_status(self.root, a["id"], "declined", reason="Covered by F-36")
        self.assertEqual(("declined", "", "Covered by F-36"), (d["status"], d["feature"], d["reason"]))
        n = ideas.set_status(self.root, a["id"], "new")
        self.assertEqual(("new", "", ""), (n["status"], n["feature"], n["reason"]))

    def test_mark_taken_moves_only_new_ideas(self):
        a = ideas.add(self.root, "One")
        b = ideas.add(self.root, "Two")
        ideas.set_status(self.root, b["id"], "declined", reason="no")
        self.assertEqual([a["id"]], ideas.mark_taken(self.root, [a["id"], b["id"], "I-777"]))
        doc = ideas.load(self.root)
        self.assertEqual(["taken", "declined"], [i["status"] for i in doc["ideas"]])

    def test_delete_and_an_id_is_never_reused(self):
        ideas.add(self.root, "One")
        two = ideas.add(self.root, "Two")
        self.assertEqual("I-002", ideas.delete(self.root, two["id"], "Same as One"))
        three = ideas.add(self.root, "Three")
        self.assertEqual("I-003", three["id"], "the deleted I-002 is not handed out again")
        self.assertEqual(["I-001", "I-003"], [i["id"] for i in ideas.load(self.root)["ideas"]])
        with self.assertRaises(KeyError):
            ideas.delete(self.root, "I-002", "again")
        # A file whose counter fell behind (edited by hand) still never reuses an id.
        path = os.path.join(self.root, "testing", "feature-ideas.json")
        doc = json.loads(self.read())
        doc["nextId"] = 1
        with open(path, "w", encoding="ascii") as f:
            json.dump(doc, f)
        self.assertEqual("I-004", ideas.add(self.root, "Four")["id"])

    def test_two_writers_at_once_lose_nothing(self):
        # Two processes released together, each adding 80 ideas as fast as it can, through the same lock and atomic
        # write. Without the lock this loses adds or fails outright (watched on 2026-10-13, see the P90 notes).
        ctx = multiprocessing.get_context("spawn")
        go = ctx.Event()
        procs = [ctx.Process(target=_add_many, args=(self.root, 80, t, go)) for t in ("a", "b")]
        for p in procs:
            p.start()
        time.sleep(1.5)
        go.set()
        for p in procs:
            p.join(60)
            self.assertEqual(0, p.exitcode)
        doc = json.loads(self.read())
        found = [i["id"] for i in doc["ideas"]]
        self.assertEqual(160, len(found), "every add kept")
        self.assertEqual(160, len(set(found)), "no id given twice")
        self.assertEqual(["I-%03d" % n for n in range(1, 161)], found)
        self.assertEqual(161, doc["nextId"])

    def test_summary_counts_by_status(self):
        for t in ("a", "b", "c"):
            ideas.add(self.root, t)
        ideas.set_status(self.root, "I-002", "taken")
        s = ideas.summary(ideas.load(self.root))
        self.assertEqual({"new": 2, "taken": 1, "became": 0, "declined": 0, "total": 3}, s)


class CopyText(unittest.TestCase):
    def test_the_format_for_the_features_chat(self):
        doc = {"ideas": [
            ideas.new_idea(id="I-002", title="Bank deposit from the pack", area="crafting", playtest="P71-3",
                           description="Two lines\nof text"),
            ideas.new_idea(id="I-001", title="Bare idea"),
            ideas.new_idea(id="I-003", title="Already taken", status="taken"),
        ]}
        pts = {"items": [{"id": "P71-3", "label": "Fill a BOD", "what": "x"}]}
        self.assertEqual(
            "New feature ideas from the play-test page (2), for F-numbers or a decline:\n"
            "\n"
            "I-001: Bare idea\n"
            "Area: (none)\n"
            "Linked play test: (none)\n"
            "Description: (none)\n"
            "\n"
            "I-002: Bank deposit from the pack\n"
            "Area: crafting\n"
            "Linked play test: P71-3 (Fill a BOD)\n"
            "Description:\n"
            "  Two lines\n"
            "  of text\n", ideas.copy_text(doc, pts))
        self.assertEqual("", ideas.copy_text({"ideas": [doc["ideas"][2]]}), "nothing new, nothing to copy")


class FeatureQueueParser(unittest.TestCase):
    SAMPLE = """# Feature queue
## Where things stand
### Not an entry
## Open
### F-1: Craft X, keep going on failure (added 2026-09-29)
### F-3: Custodians folded into Clean Up Britannia (added 2026-09-29, was: Custodian scoring)
### F-42: Epic crafting (planned, added 2026-10-11)
## Batched
| ID | Batch prompt | Notes |
|---|---|---|
| F-1 | cc-P18-reset | Part 3 of 3. Mentions F-42 in the notes only. |
| F-24, F-33 (research only) | cc-P47-league-research | Notes only. |
## Dropped
| ID | Why |
|---|---|
| F-2 | Diminishing returns on tokens. Dropped 2026-09-29 by Chase. |
"""

    def test_the_shapes_the_file_uses(self):
        f = {e["id"]: e for e in ideas.parse_feature_queue(self.SAMPLE)}
        self.assertEqual(["F-1", "F-2", "F-3", "F-24", "F-33", "F-42"], [e["id"] for e in ideas.parse_feature_queue(self.SAMPLE)])
        self.assertEqual(("Craft X, keep going on failure", "2026-09-29", "Open", ["cc-P18-reset"]),
                         (f["F-1"]["title"], f["F-1"]["added"], f["F-1"]["section"], f["F-1"]["batched"]))
        self.assertEqual("Custodians folded into Clean Up Britannia", f["F-3"]["title"])
        self.assertEqual(("Epic crafting", "2026-10-11", []), (f["F-42"]["title"], f["F-42"]["added"], f["F-42"]["batched"]),
                         "an F-number in a row's notes is not a batch")
        self.assertEqual(("Batched", ["cc-P47-league-research"]), (f["F-24"]["section"], f["F-24"]["batched"]))
        self.assertEqual(("Dropped", "Diminishing returns on tokens"), (f["F-2"]["section"], f["F-2"]["title"]))

    def test_the_real_feature_queue(self):
        path = ROOT / "docs" / "feature-queue.md"
        text = path.read_text(encoding="utf-8")
        got = ideas.parse_feature_queue(text)
        heads = re.findall(r"^### (F-\d+):", text, re.M)
        ids = [e["id"] for e in got]
        self.assertEqual(len(ids), len(set(ids)), "each F-number once")
        for h in heads:
            self.assertIn(h, ids, "every heading is an entry")
        by = {e["id"]: e for e in got}
        for h in heads:
            self.assertTrue(by[h]["title"] and "(added" not in by[h]["title"], h + " has a clean title")
            self.assertRegex(by[h]["added"], r"^\d{4}-\d{2}-\d{2}$", h + " has its added date")
        counts = ideas.section_counts(got)
        print("\n  feature-queue.md: %d entries, %d headings, by section %s, %d batched" % (
            len(got), len(heads), counts, sum(1 for e in got if e["batched"])))
        self.assertEqual(len(heads), sum(1 for e in got if e["added"]), "only headings carry an added date")
        self.assertEqual("Dropped", by["F-2"]["section"], "F-2 is in the Dropped table")
        self.assertTrue(by["F-9"]["batched"], "F-9 is in the Batched table and stays under Open")


@unittest.skipUnless(SERVER.exists(), "the play-test service is not on this machine")
class ServiceRoutes(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="ideas-svc-")
        for d in ("notes", "docs", "testing"):
            os.makedirs(os.path.join(self.root, d))
        shutil.copy(ROOT / "docs" / "feature-queue.md", os.path.join(self.root, "docs", "feature-queue.md"))
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        self.port = s.getsockname()[1]
        s.close()
        self.proc = subprocess.Popen([sys.executable, "-B", str(SERVER), "--root", self.root, "--lib", str(TOOLS),
                                      "--bind", "127.0.0.1", "--port", str(self.port), "--status-page", os.devnull],
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

    def get(self, path):
        with urllib.request.urlopen("http://127.0.0.1:%d%s" % (self.port, path), timeout=5) as r:
            return json.loads(r.read().decode("utf-8"))

    def post(self, path, body):
        req = urllib.request.Request("http://127.0.0.1:%d%s" % (self.port, path), data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode("utf-8"))

    def test_add_list_copy_and_count(self):
        self.assertEqual(0, self.get("/api/summary")["ideas_new"])
        code, j = self.post("/api/ideas/add", {"title": "Climbing gear", "area": "world"})
        self.assertEqual((200, "I-001"), (code, j["idea"]["id"]))
        self.assertEqual(400, self.post("/api/ideas/add", {"title": ""})[0], "no title is a 400")
        self.assertEqual(404, self.post("/api/ideas/delete", {"id": "I-404", "reason": "gone"})[0], "an unknown id is a 404")
        doc = self.get("/api/ideas")
        self.assertEqual((1, 1), (doc["summary"]["new"], len(doc["ideas"])))
        self.assertIn("F-43", [f["id"] for f in doc["features"]], "the real queue is listed")
        self.assertEqual(1, self.get("/api/summary")["ideas_new"])
        cp = self.get("/api/ideas/copy")
        self.assertEqual(["I-001"], cp["ids"])
        self.assertTrue(cp["text"].startswith("New feature ideas from the play-test page (1)"))
        self.assertEqual((200, {"taken": ["I-001"]}), self.post("/api/ideas/taken", {"ids": cp["ids"]}))
        self.assertEqual(0, self.get("/api/summary")["ideas_new"])
        self.assertEqual(200, self.post("/api/ideas/status", {"id": "I-001", "status": "became", "feature": "F-44"})[0])
        self.assertEqual(200, self.post("/api/ideas/edit", {"id": "I-001", "description": "Ropes"})[0])
        self.assertEqual((200, {"deleted": "I-001"}), self.post("/api/ideas/delete", {"id": "I-001", "reason": "Became F-44 elsewhere"}))
        self.assertEqual("I-002", self.post("/api/ideas/add", {"title": "Next"})[1]["idea"]["id"])


if __name__ == "__main__":
    unittest.main()
