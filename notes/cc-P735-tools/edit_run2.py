"""cc-P735 (second edit, after the fake-shard fact): on a locked account, look at the other ready pool accounts' lists
first (a login that makes no character holds nothing in the world, so the account goes straight back, no rest); only
when every ready account shows New Haven locked does the harness unlock one with a skipped throwaway.
Usage: python -P edit_run2.py <code copy>"""
import sys

p = sys.argv[1] + "/tools/playtest-bot/uobot/run.py"
s = open(p, encoding="utf-8", newline="").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''        self.haven_open = set()     # cc-P735: pool accounts whose start list shows New Haven unlocked
''', '''        self.haven_open = set()     # cc-P735: pool accounts whose start list shows New Haven unlocked
        self.haven_shut = set()     # cc-P735: pool accounts seen locked since the last unlock
''')
rep('''                if city == HAVEN_CITY:
                    ready.sort(key=lambda a: a not in self.haven_open)   # stable: keeps first_login's order within
''', '''                if city == HAVEN_CITY:
                    # open first, then not yet looked at, then seen locked (stable: keeps first_login's order within)
                    ready.sort(key=lambda a: 0 if a in self.haven_open else 2 if a in self.haven_shut else 1)
''')
rep('''            if city == HAVEN_CITY and self.haven_locked(c):
                self.unlock_haven(c)   # rests this account; take the next ready one
                continue
''', '''            if city == HAVEN_CITY and self.haven_locked(c):
                with self.pool_lock:
                    self.haven_shut.add(acct)
                    unseen = [a for a in POOL if self.pool_rest[a] <= time.time() and a not in self.haven_shut]
                if unseen:
                    # nothing was made on this login, so nothing stays in the world: the account is free again at once
                    c.close()
                    with self.pool_lock:
                        self.pool_rest[acct] = 0.0
                    continue
                self.unlock_haven(c)   # rests this account; take the next ready one
                continue
''')
rep('''            self.haven_open.add(acct)
        finally:
            self.done(c)
''', '''            self.haven_open.add(acct)
            self.haven_shut.discard(acct)
        finally:
            self.done(c)
''')
open(p, "w", encoding="utf-8", newline="").write(s)
print("edited", p)
