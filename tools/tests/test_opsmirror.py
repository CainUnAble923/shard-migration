"""cc-P107: the testing/ mirror refreshed from Haven before each commit (tools/opsmirror.py).

    python -m unittest tools/tests/test_opsmirror.py

Facts: before the cutover nothing is fetched or written; after it Haven's export becomes testing/ and the changed files
are named; Haven unreachable, no token, or a bundle that does not check out each leave the previous mirror exactly as
it was; and the command line always exits 0, so a commit is never blocked. Temporary folders only. ASCII only.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
import opsdata  # noqa: E402
import opsmirror  # noqa: E402
import playtests as pt  # noqa: E402


def tree(root):
    out = {}
    for d, _, names in os.walk(os.path.join(root, "testing")):
        for n in names:
            with open(os.path.join(d, n), "rb") as f:
                out[os.path.relpath(os.path.join(d, n), root).replace(os.sep, "/")] = f.read()
    return out


class Mirror(unittest.TestCase):
    def setUp(self):
        self.haven = tempfile.mkdtemp(prefix="p107-haven-")
        self.mirror = tempfile.mkdtemp(prefix="p107-mirror-")
        pt.save(self.mirror, pt.new_doc())                       # the mirror as of the last commit
        self.before = tree(self.mirror)
        pt.add_manual(self.haven, "Marked on Haven", by="kid@example.com")   # Haven moved on since

    def tearDown(self):
        shutil.rmtree(self.haven, ignore_errors=True)
        shutil.rmtree(self.mirror, ignore_errors=True)

    def from_haven(self, api, token):
        self.asked = (api, token)
        return json.loads(json.dumps(opsdata.export_bundle(self.haven)))

    def test_before_the_cutover_nothing_is_fetched_or_written(self):
        called = []
        r = opsmirror.refresh(self.mirror, "local", "http://haven", "t", fetch=lambda a, t: called.append(1))
        self.assertEqual("skipped", r["state"])
        self.assertIn("not cut over", r["line"])
        self.assertEqual([], called)
        self.assertEqual(self.before, tree(self.mirror))

    def test_after_it_havens_export_becomes_the_mirror_and_the_changes_are_named(self):
        r = opsmirror.refresh(self.mirror, "haven", "http://haven:8094", "tok", fetch=self.from_haven)
        self.assertEqual("refreshed", r["state"])
        self.assertEqual(("http://haven:8094", "tok"), self.asked)
        self.assertEqual(tree(self.haven), tree(self.mirror))
        self.assertEqual(["testing/SUMMARY.md", "testing/play-tests.json"], r["changed"])
        self.assertIn("2 changed", r["line"])
        again = opsmirror.refresh(self.mirror, "haven", "http://haven:8094", "tok", fetch=self.from_haven)
        self.assertEqual([], again["changed"], "nothing new: nothing changed")

    def test_unreachable_no_token_or_a_bad_bundle_leave_the_mirror_as_it_was(self):
        def down(api, token):
            raise urllib.error.URLError("connection refused")

        def tampered(api, token):
            b = self.from_haven(api, token)
            b["files"]["testing/SUMMARY.md"]["text"] += "x"
            return b
        for fetch, token, state in ((down, "tok", "unreachable"), (self.from_haven, "", "refused"), (tampered, "tok", "refused")):
            r = opsmirror.refresh(self.mirror, "haven", "http://haven:8094", token, fetch=fetch)
            self.assertEqual(state, r["state"])
            self.assertIn("NOT refreshed", r["line"])
            self.assertIn("previous mirror stays", r["line"])
            self.assertEqual(self.before, tree(self.mirror))

    def test_the_command_line_exits_0_whatever_happens(self):
        state = os.path.join(self.haven, "state.json")
        with open(state, "w") as f:
            json.dump({"mode": "haven"}, f)
        cfg = os.path.join(self.haven, "haven-ops.json")
        with open(cfg, "w") as f:
            json.dump({"stateFile": state, "tokenFile": os.path.join(self.haven, "no-token.txt"), "haven": {"opsApi": "http://127.0.0.1:9"}}, f)
        p = subprocess.run([sys.executable, "-B", str(TOOLS / "opsmirror.py"), "--root", self.mirror, "--config", cfg],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(0, p.returncode, p.stderr)
        self.assertIn("NOT refreshed", p.stdout)
        self.assertEqual(self.before, tree(self.mirror))


if __name__ == "__main__":
    unittest.main()
