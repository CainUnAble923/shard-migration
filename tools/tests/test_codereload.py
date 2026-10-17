"""cc-P137: the play-test service picks up its own code when it changes, without cutting a request short.

    python -m unittest tools/tests/test_codereload.py

The gate and the watcher (tools/codereload.py) on their own, then the real service (D:\\ShatteredLegacy\\docker\\
test-queue\\server.py) run from a scratch copy of the tools folder: an edited tools module is loaded in place (same
process, new behaviour), and an edited server.py makes the service drain and exit for the container to restart it.
Standard library only. ASCII only.
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
sys.path.insert(0, str(TOOLS))
import codereload  # noqa: E402

SERVER = Path(os.environ.get("SL_SHARD", r"D:\ShatteredLegacy")) / "docker" / "test-queue" / "server.py"


class GateFacts(unittest.TestCase):
    def test_drain_waits_for_running_work_and_holds_new_work_until_reopened(self):
        g = codereload.Gate()
        order = []
        started = threading.Event()
        release = threading.Event()

        def running():
            with g.work():
                started.set()
                release.wait(5)
                order.append("running finished")

        def late():
            with g.work():
                order.append("late ran")

        t1 = threading.Thread(target=running); t1.start()
        started.wait(5)
        result = {}
        t2 = threading.Thread(target=lambda: result.setdefault("drained", g.drain(5))); t2.start()
        time.sleep(0.1)
        t3 = threading.Thread(target=late); t3.start()
        time.sleep(0.1)
        self.assertEqual([], order, "the drain waits; the late request waits")
        release.set()
        t2.join(5)
        self.assertTrue(result["drained"])
        time.sleep(0.1)
        self.assertEqual(["running finished"], order, "the late request still waits at the closed gate")
        order.append("reloaded")
        g.reopen()
        t3.join(5); t1.join(5)
        self.assertEqual(["running finished", "reloaded", "late ran"], order)

    def test_a_drain_that_times_out_opens_the_gate_again(self):
        g = codereload.Gate()
        release = threading.Event()
        t = threading.Thread(target=lambda: g.work().__enter__() or release.wait(5))
        with g.work():
            self.assertFalse(g.drain(0.1))
        ran = []
        with g.work():
            ran.append(1)
        self.assertEqual([1], ran)
        release.set()


class NestedWork(unittest.TestCase):
    def test_work_inside_work_on_one_thread_never_waits_for_a_drain(self):
        # server.py: POST /api/import runs the importer, which takes the gate again, inside the request's own gate.
        g = codereload.Gate()
        inner_ran = threading.Event()
        in_outer = threading.Event()
        go_inner = threading.Event()

        def request():
            with g.work():
                in_outer.set()
                go_inner.wait(5)
                with g.work():
                    inner_ran.set()

        t = threading.Thread(target=request); t.start()
        in_outer.wait(5)
        result = {}
        d = threading.Thread(target=lambda: result.setdefault("drained", g.drain(5))); d.start()
        time.sleep(0.1)
        go_inner.set()
        self.assertTrue(inner_ran.wait(2), "the nested work ran at once")
        d.join(5)
        self.assertTrue(result["drained"])
        g.reopen()
        t.join(5)


class WatcherFacts(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="p137-watch-")
        self.f = os.path.join(self.dir, "mod.py")
        Path(self.f).write_text("X = 1\n")
        self.calls = []
        self.answer = True
        self.w = codereload.Watcher(lambda: codereload.code_files(self.dir), self.change, log=lambda m: None)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def change(self):
        self.calls.append(1)
        return self.answer

    def touch(self, text):
        # Each touch moves the time on by a whole second more than the last: two quick writes of the same size
        # must never read as the same file.
        Path(self.f).write_text(text)
        self.bumps = getattr(self, "bumps", 0) + 1
        st = os.stat(self.f)
        os.utime(self.f, ns=(st.st_atime_ns, st.st_mtime_ns + self.bumps * 1_000_000_000))

    def test_a_change_must_hold_still_for_one_more_poll(self):
        self.assertFalse(self.w.poll(), "nothing changed")
        self.touch("X = 2\n")
        self.assertFalse(self.w.poll(), "first sight of a change: wait one poll")
        self.touch("X = 3\n")
        self.assertFalse(self.w.poll(), "still moving")
        self.assertTrue(self.w.poll())
        self.assertEqual([1], self.calls)
        self.assertFalse(self.w.poll(), "loaded; nothing new")

    def test_a_change_that_could_not_drain_is_tried_again(self):
        self.touch("X = 2\n")
        self.w.poll()
        self.answer = False
        self.assertFalse(self.w.poll())
        self.answer = True
        self.assertTrue(self.w.poll())
        self.assertEqual([1, 1], self.calls)

    def test_reload_modules_changes_the_same_module_object(self):
        sys.path.insert(0, self.dir)
        try:
            import mod  # noqa: F401
            self.assertEqual(1, mod.X)
            same = mod
            # A same-size edit that keeps the file's time (a quick save, a pull within the second): only the
            # removed .pyc makes the reload read the new source.
            st = os.stat(self.f)
            Path(self.f).write_text("X = 7\n")
            os.utime(self.f, ns=(st.st_atime_ns, st.st_mtime_ns))
            codereload.reload_modules([mod])
            self.assertEqual(7, same.X)
        finally:
            sys.path.remove(self.dir)
            sys.modules.pop("mod", None)


def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close()
    return p


@unittest.skipUnless(SERVER.exists(), "the play-test service is not on this machine")
class TheService(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="p137-svc-")
        self.lib = os.path.join(self.tmp, "tools")
        shutil.copytree(TOOLS, self.lib, ignore=shutil.ignore_patterns("tests", "__pycache__", "obsolete", "*.json"))
        self.svc = os.path.join(self.tmp, "svc")
        os.makedirs(self.svc)
        shutil.copy(SERVER, self.svc)
        self.root = os.path.join(self.tmp, "root")
        for d in ("notes", "docs", "testing"):
            os.makedirs(os.path.join(self.root, d))
        self.port = free_port()
        env = {k: v for k, v in os.environ.items() if not k.startswith(("PLAYTESTS_", "ACCESS_", "REPO_STAMP", "RELOAD_"))}
        self.proc = subprocess.Popen(
            [sys.executable, "-B", os.path.join(self.svc, "server.py"), "--root", self.root, "--lib", self.lib,
             "--html", str(SERVER.parent / "html"), "--bind", "127.0.0.1", "--port", str(self.port),
             "--status-page", os.devnull, "--deployed", os.devnull, "--import-seconds", "3600",
             "--reload-seconds", "0.2"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
        for _ in range(100):
            if self.proc.poll() is not None:
                self.fail("the service exited: " + self.proc.stdout.read().decode("utf-8", "replace")[-800:])
            try:
                self.items()
                return
            except OSError:
                time.sleep(0.1)
        self.fail("the service did not start")

    def tearDown(self):
        if self.proc.poll() is None:
            self.proc.terminate()
        self.proc.wait(10)
        self.proc.stdout.close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def items(self):
        with urllib.request.urlopen("http://127.0.0.1:%d/api/items" % self.port, timeout=10) as r:
            return json.loads(r.read().decode("utf-8"))

    def bump(self, path, extra):
        with open(path, "a", encoding="ascii") as f:
            f.write(extra)
        st = os.stat(path)
        os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + 10_000_000))

    def test_an_edited_tools_module_is_loaded_in_the_same_process(self):
        before = self.items()
        self.assertNotIn("reloaded", before.get("who", {}))
        code = before["service"]["code"]
        self.bump(os.path.join(self.lib, "playwho.py"), "\n\n_p137_annotate = annotate\n\n\ndef annotate(doc, *a, **k):\n"
                  "    _p137_annotate(doc, *a, **k)\n    doc.setdefault(\"who\", {})[\"reloaded\"] = True\n")
        for _ in range(50):
            time.sleep(0.1)
            now = self.items()
            if now.get("who", {}).get("reloaded"):
                break
        self.assertTrue(now.get("who", {}).get("reloaded"), "the new playwho.py runs")
        self.assertNotEqual(code, now["service"]["code"])
        self.assertIsNone(self.proc.poll(), "no restart: the same process")

    def test_a_tools_module_that_fails_to_load_keeps_the_old_code_running(self):
        self.bump(os.path.join(self.lib, "playwho.py"), "\n\ndef broken(:\n")
        time.sleep(1.0)
        self.assertIsNone(self.proc.poll())
        self.assertIn("items", self.items(), "still serving on the old code")

    def test_an_edited_server_py_drains_and_exits_for_the_container_to_restart(self):
        self.bump(os.path.join(self.svc, "server.py"), "\n# p137\n")
        self.assertEqual(0, self.proc.wait(10))
        out = self.proc.stdout.read().decode("utf-8", "replace")
        self.assertIn("server.py changed", out)


if __name__ == "__main__":
    unittest.main()
