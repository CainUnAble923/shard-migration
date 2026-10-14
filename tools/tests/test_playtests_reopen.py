"""cc-P102: a play-test item set back to Open records when (reopenedAt), so the overnight bot's work check can see it.

    python -m unittest tools/tests/test_playtests_reopen.py

Every fact works in a temporary folder. Standard library only. ASCII only.
"""
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
import playtests as pt  # noqa: E402


class Reopen(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="p102-pt-")
        doc = pt.new_doc()
        doc["items"].append(pt.new_item(id="M-001", source="manual", what="x", text="x"))
        os.makedirs(os.path.join(self.root, "testing"))
        pt.save(self.root, doc)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def item(self):
        with open(os.path.join(self.root, pt.DATA_REL), encoding="utf-8") as f:
            return [i for i in json.load(f)["items"] if i["id"] == "M-001"][0]

    def test_a_new_item_has_an_empty_reopenedAt(self):
        self.assertEqual("", self.item()["reopenedAt"])

    def test_pass_then_open_records_reopenedAt_and_keeps_it(self):
        pt.set_result(self.root, "M-001", "pass")
        self.assertEqual("", self.item()["reopenedAt"])
        pt.set_result(self.root, "M-001", "open")
        it = self.item()
        self.assertEqual("open", it["status"])
        self.assertEqual("", it["resultAt"])
        self.assertRegex(it["reopenedAt"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
        first = it["reopenedAt"]
        pt.set_result(self.root, "M-001", "fail", note="broke")
        self.assertEqual(first, self.item()["reopenedAt"], "marking it again keeps the last re-open")

    def test_open_on_an_open_item_is_not_a_reopen(self):
        pt.set_result(self.root, "M-001", "open")
        self.assertEqual("", self.item()["reopenedAt"])


if __name__ == "__main__":
    unittest.main()
