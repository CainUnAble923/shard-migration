"""cc-P735 (third edit, after the first live run, run1):
- the looks at other accounts' lists came 10 ms apart and the server closed the third connection (P64-1 ERROR,
  "no character list after the game login"); pause between them;
- T-039 unlocked a second account while the first one it had just opened was only resting. Now, for a New Haven
  character: when a pool account is known open (and, for P64-1, has had no character this run), wait for it and log
  in to no other; otherwise look at the accounts not seen yet, then unlock one seen locked.
Usage: python -P edit_run3.py <code copy>"""
import sys

p = sys.argv[1] + "/tools/playtest-bot/uobot/run.py"
s = open(p, encoding="utf-8", newline="").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''REST_SECONDS = 330
''', '''REST_SECONDS = 330
LOOK_PAUSE = 3.0   # cc-P735: between quick logins that only read an account's start list (run1: 10 ms apart, refused)
''')
rep('''                ready = [a for a in POOL if self.pool_rest[a] <= now]
                if first_login:
                    ready.sort(key=lambda a: a in self.first_logins)
                if city == HAVEN_CITY:
                    # open first, then not yet looked at, then seen locked (stable: keeps first_login's order within)
                    ready.sort(key=lambda a: 0 if a in self.haven_open else 2 if a in self.haven_shut else 1)
                if ready:
''', '''                ready = [a for a in POOL if self.pool_rest[a] <= now]
                if first_login:
                    ready.sort(key=lambda a: a in self.first_logins)
                if city == HAVEN_CITY:
                    usable = [a for a in self.haven_open if not (first_login and a in self.first_logins)]
                    if usable:
                        # an open account exists: wait for it (it may be resting), and log in to no locked one
                        ready = [a for a in ready if a in usable]
                    else:
                        # not yet looked at first, then seen locked (stable: keeps first_login's order within)
                        ready.sort(key=lambda a: 2 if a in self.haven_shut else 1)
                if ready:
''')
rep('''                if unseen:
                    # nothing was made on this login, so nothing stays in the world: the account is free again at once
                    c.close()
                    with self.pool_lock:
                        self.pool_rest[acct] = 0.0
                    continue
''', '''                if unseen:
                    # nothing was made on this login, so nothing stays in the world: the account is free again at once
                    c.close()
                    with self.pool_lock:
                        self.pool_rest[acct] = 0.0
                    time.sleep(LOOK_PAUSE)
                    continue
''')
rep('''            self.tr.write("harness", "%s: New Haven locked; %s (at %s) woke on the isle, the Admin skipped its tutorial: %s"
                          % (acct, name, (c.pos or ())[:3], "yes" if skipped else "NO"))''',
    '''            self.tr.write("harness", "%s: New Haven locked; %s made with the isle's city, the Admin skipped its tutorial: %s"
                          " (now at %s)" % (acct, name, "yes" if skipped else "NO", (c.pos or ())[:3]))''')
open(p, "w", encoding="utf-8", newline="").write(s)
print("edited", p)
