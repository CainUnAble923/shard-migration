"""cc-P773: red runs for the Python parts. Each mutant undoes one rule in a scratch copy of the code copy's scripts and
web-console folders; the matching tests must fail on it (and pass on the real code). Also the pre-change run: the tests
against git HEAD's folders (no Goblin, no playtesters.py, the old server.py).

    python -P mutate_py.py <code copy> <scratch folder> > py-mutants.txt
"""
import os
import shutil
import subprocess
import sys

code, scratch = sys.argv[1], sys.argv[2]
G = "scripts/playtest_goblin.py"
P = "web-console/playtesters.py"
S = "web-console/server.py"
MUTANTS = {
    # Goblin: the cap of 3 open tasks
    "nocap": (G, "CAP = 3\n", "CAP = 99\n"),
    # Goblin: a paused tester is not skipped
    "nopause": (G, '        if tester.get("paused"):\n', '        if False:\n'),
    # Goblin: repeats allowed (a card the tester had before)
    "repeats": (G, '        had = {t.get("card") for t in mine}\n', '        had = set()\n'),
    # Goblin: no preference for unanswered cards
    "norank": (G, "key=lambda c: (rank(answers.get(c[\"key\"], set())), tonight.get(c[\"key\"], 0), order[c[\"key\"]]))",
               "key=lambda c: order[c[\"key\"]])"),
    # Goblin: mail every night, changed or not
    "alwaysmail": (G, "    if (fresh or new) and not dry_run:\n", "    if not dry_run:\n"),
    # Goblin: settled play-test items still handed out
    "nosettled": (G, '    live = [c for c in cards if not c.get("retired") and c.get("testId", "") not in settled]\n',
                  '    live = [c for c in cards if not c.get("retired")]\n'),
    # Goblin: writes a result onto the play-test page's file
    "writesresult": (G, "    return {\"newReports\": fresh,",
                     "    open(os.path.join(notes, 'testing', 'play-tests.json'), 'a').write('\"pass\"')\n    return {\"newReports\": fresh,"),
    # Testers page: Pull back does not change the task
    "nopull": (P, '            t["status"] = "pulled"\n', '            pass\n'),
    # Testers page: a broken tester file is written over
    "overwrite": (P, "        if testers is None:\n            raise PlayTestError(err + \". Fix or remove the file before changing the list.\")\n",
                  "        if testers is None:\n            testers = []\n"),
    # Testers page: the POSTs skip the page check
    "nopagecheck": (S, "        def _testers_post(self, path):\n", "        def _testers_post(self, path, _x=None):\n            self._not_this_page = lambda: ''\n"),
}
TESTS = {
    "scripts": ("scripts/tests", "test_playtest_goblin.py"),
    "web": ("web-console/tests", "test_testers.py"),
}


def run_tests(root, which):
    d, pat = TESTS[which]
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", d, "-p", pat], cwd=root,
                       capture_output=True, text=True, timeout=600)
    tail = [l for l in (r.stdout + r.stderr).splitlines() if l.startswith(("Ran ", "OK", "FAILED", "FAIL:", "ERROR:"))]
    return r.returncode, tail


def copy(dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    for sub in ("scripts", "web-console"):
        shutil.copytree(os.path.join(code, sub), os.path.join(dst, sub),
                        ignore=shutil.ignore_patterns("__pycache__", "shard-console-cache", "art", "console-art", "legion"))


base = os.path.join(scratch, "base")
copy(base)
for which in TESTS:
    rc, tail = run_tests(base, which)
    print("baseline %s: exit %d | %s" % (which, rc, " ; ".join(tail)))

for name, (rel, old, new) in MUTANTS.items():
    dst = os.path.join(scratch, name)
    copy(dst)
    p = os.path.join(dst, rel)
    with open(p, encoding="utf-8", newline="") as f:
        text = f.read()
    if text.count(old) != 1:
        print("%s: ANCHOR NOT FOUND ONCE in %s" % (name, rel))
        continue
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(text.replace(old, new))
    which = "web" if rel.startswith("web-console") else "scripts"
    rc, tail = run_tests(dst, which)
    print("%s (%s): exit %d %s | %s" % (name, which, rc, "RED" if rc else "STILL GREEN", " ; ".join(tail)))
    shutil.rmtree(dst, ignore_errors=True)
