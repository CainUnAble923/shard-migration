"""
The play-test service picks up its own code when it changes (cc-P137).

P115's Who and Mine filters showed nothing for a day: the sl-play-tests container ran the code it started with until
someone restarted it. On the game PC the tools folder is a live mount, and on Haven a sidecar pulls the repo every two
minutes, so the new files were there; only the running Python was old. A restart from the commit step would reach the
game PC's container but not Haven's, so the service watches its own files and works the same on both.

    gate = Gate()                                   # every request and every import runs inside gate.work()
    Watcher(lambda: code_files(lib), on_change)     # polls; on_change once a change has held still for one more poll

When the tools modules change, server.py drains the gate (new requests wait at it; requests and imports already
running finish), reloads the modules in place with importlib.reload (reload_modules), and opens the gate again: the
waiting requests then run on the new code. Nothing is cut short and nothing is refused. When server.py itself changes
it cannot be reloaded in place: the service drains the same way and exits, and the container's restart policy
(unless-stopped, both composes) starts it on the new file; only requests that arrive in that second see a refused
connection, and the page then says "Not saved" rather than losing anything quietly. Standard library only. ASCII only.
"""
import hashlib
import importlib
import os
import threading
import time
from contextlib import contextmanager


class Gate:
    """Work runs inside work(); drain() waits for running work to finish and holds new work until reopen(). Work
    inside work on the same thread (server.py's POST /api/import runs the importer, which takes the gate again) is
    part of the outer work and never waits."""

    def __init__(self):
        self._cv = threading.Condition()
        self._busy = 0
        self._closed = False
        self._depth = threading.local()

    @property
    def busy(self):
        with self._cv:
            return self._busy

    @contextmanager
    def work(self):
        depth = getattr(self._depth, "n", 0)
        if depth:
            self._depth.n = depth + 1
            try:
                yield
            finally:
                self._depth.n = depth
            return
        with self._cv:
            while self._closed:
                self._cv.wait()
            self._busy += 1
        self._depth.n = 1
        try:
            yield
        finally:
            self._depth.n = 0
            with self._cv:
                self._busy -= 1
                self._cv.notify_all()

    def drain(self, timeout):
        """Close the gate and wait for running work. True when idle (the gate stays closed until reopen); False on
        timeout (the gate is opened again)."""
        end = time.monotonic() + timeout
        with self._cv:
            self._closed = True
            while self._busy:
                left = end - time.monotonic()
                if left <= 0:
                    self._closed = False
                    self._cv.notify_all()
                    return False
                self._cv.wait(left)
            return True

    def reopen(self):
        with self._cv:
            self._closed = False
            self._cv.notify_all()


def reload_modules(modules):
    """importlib.reload each module, in the order given (dependencies first: playtests before ideas and bugs). The
    module objects stay the same, so every `import x` binding elsewhere sees the new code. Each module's cached .pyc
    goes first: it records the source's mtime to the second and its size, so an edit in the same second that keeps the
    size would otherwise load the old bytecode."""
    for m in modules:
        cached = getattr(m, "__cached__", None)
        if cached:
            try:
                os.remove(cached)
            except OSError:
                pass
        importlib.reload(m)


def code_files(lib):
    """The tools modules the service imports: every .py directly in its tools folder."""
    try:
        return [os.path.join(lib, n) for n in sorted(os.listdir(lib)) if n.endswith(".py")]
    except OSError:
        return []


def fingerprint(paths):
    """A short hash of each file's name, size and modification time; a missing file counts as its own state."""
    h = hashlib.sha1()
    for p in paths:
        try:
            st = os.stat(p)
            h.update(("%s|%d|%d\n" % (p, st.st_size, st.st_mtime_ns)).encode("utf-8"))
        except OSError:
            h.update(("%s|missing\n" % p).encode("utf-8"))
    return h.hexdigest()[:12]


class Watcher:
    """Polls `paths()` every `seconds`. A changed fingerprint must read the same on the next poll before on_change
    runs, so a file mid-copy (a git pull, an editor save) is never loaded half written. on_change returning False
    (it could not drain in time) leaves the change pending, and it is tried again."""

    def __init__(self, paths, on_change, seconds=5.0, log=print):
        self.paths, self.on_change, self.seconds, self.log = paths, on_change, seconds, log
        self.loaded = fingerprint(paths())
        self._pending = None
        self._stop = threading.Event()

    def poll(self):
        """One check; True when on_change ran and succeeded."""
        now = fingerprint(self.paths())
        if now == self.loaded:
            self._pending = None
            return False
        if now != self._pending:
            self._pending = now
            return False
        self.log("code changed (%s -> %s)" % (self.loaded, now))
        if self.on_change() is False:
            return False
        self._pending = None
        self.loaded = now
        return True

    def run(self):
        while not self._stop.wait(self.seconds):
            try:
                self.poll()
            except Exception as e:  # a watcher that died would bring the stale-code bug back without a word
                self.log("code watch error: %s" % e)

    def start(self):
        threading.Thread(target=self.run, daemon=True).start()
        return self

    def stop(self):
        self._stop.set()
