"""cc-P735 (fourth edit, after live run 2, run2):
- P64-1's relog used secrets["playerPassword"], but fresh() makes pool characters with poolPassword (falling back to
  playerPassword). With a Golem's own accounts the two differ, so the relog was refused (0x82 reason 3, bad password)
  and the account stayed busy for ever. The relog now uses fresh()'s password, and a failed relog still rests it.
- fresh() waited only for an open account even when that account was busy for ever (a check that never gave it back),
  and printed the wait over every account (0.0 rests gave -1793493431 s). It now waits only on an open account that
  will come back, and the wait is over the accounts it can take.
Usage: python -P edit_run4.py <code copy>"""
import sys

root = sys.argv[1]


def edit(path, pairs):
    p = root + path
    s = open(p, encoding="utf-8", newline="").read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, s.count(a), a[:90])
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)
    print("edited", p)


edit("/tools/playtest-bot/uobot/run.py", [
    ('''                    usable = [a for a in self.haven_open if not (first_login and a in self.first_logins)]
                    if usable:
                        # an open account exists: wait for it (it may be resting), and log in to no locked one
                        ready = [a for a in ready if a in usable]
''', '''                    usable = [a for a in self.haven_open if not (first_login and a in self.first_logins)
                              and self.pool_rest[a] != float("inf")]
                    if usable:
                        # an open account exists and will come back: wait for it, and log in to no locked one
                        ready = [a for a in ready if a in usable]
'''),
    ('''                else:
                    acct = None
                    wait = min(self.pool_rest.values()) - now
''', '''                else:
                    acct = None
                    pending = [t for a, t in self.pool_rest.items() if t > now and (city != HAVEN_CITY or not usable
                               or a in usable)]
                    wait = (min(pending) - now) if pending else 1.0
'''),
])
edit("/tools/playtest-bot/uobot/checks.py", [
    ('''        c2 = Client(acct, ctx.secrets["playerPassword"], ctx.tr, ctx.cliloc, "relog")
        chars = c2.login()
        c2.play(chars.index(c.name) if c.name in chars else 0)
        c2.sleep(3.0)
        again = [x for x in c2.gumps if any(re.match(r"^Shattered Legacy \\d{4}\\.", t) for t in all_text(c2, x))]
        c2.account = acct
        ctx.done(c2)
''', '''        # cc-P735: the pool's password, as fresh() logs in (run2: playerPassword is the Golem's own player's, refused)
        c2 = Client(acct, ctx.secrets.get("poolPassword", ctx.secrets["playerPassword"]), ctx.tr, ctx.cliloc, "relog")
        c2.account = acct
        try:
            chars = c2.login()
            c2.play(chars.index(c.name) if c.name in chars else 0)
            c2.sleep(3.0)
            again = [x for x in c2.gumps if any(re.match(r"^Shattered Legacy \\d{4}\\.", t) for t in all_text(c2, x))]
        finally:
            ctx.done(c2)   # run2: a refused relog left the account busy for ever
'''),
])
