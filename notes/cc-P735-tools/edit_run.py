"""cc-P735: the bot's fresh() can ask for creation's New Haven city (index 1, "The Bountiful Harvest Inn").
P717 locks New Haven for an account until a character of it graduates or skips; on a locked pool account the harness
first makes a throwaway that wakes on the isle and has the bot's Admin skip its tutorial ([Tutorial skip), which
unlocks New Haven for the whole account (TutorialStart.Unlock), then rests that account and takes the next.
Usage: python -P edit_run.py <code copy>"""
import sys

p = sys.argv[1] + "/tools/playtest-bot/uobot/run.py"
s = open(p, encoding="utf-8", newline="").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''POOL = ["slbot-player2", "slbot-player3", "slbot-player4"]
REST_SECONDS = 330
''', '''POOL = ["slbot-player2", "slbot-player3", "slbot-player4"]
REST_SECONDS = 330
# cc-P735: creation's start list (TutorialStart.Cities): 0 the isle, 1 New Haven ("The Bountiful Harvest Inn"). An account
# sees index 1 as "New Haven (locked)" until a character of it graduates or skips (cc-P717), and a locked pick wakes on
# the isle.
ISLE_CITY, HAVEN_CITY = 0, 1
LOCKED_HAVEN = "New Haven (locked)"
''')

rep('''        self.first_logins = {}      # account -> what the first login saw (P64-1)
''', '''        self.first_logins = {}      # account -> what the first login saw (P64-1)
        self.haven_open = set()     # cc-P735: pool accounts whose start list shows New Haven unlocked
''')

rep('''    def fresh(self, race="human", female=False, label="fresh"):
        """A brand-new character on a rested pool account, through the real creation packet. Disconnect it with
        done() so the account can rest."""
        # Thread-safe: the soak asks for three at once. An account is marked busy (rest = forever) the moment it is
        # picked, and done() starts its rest.
        while True:
            with self.pool_lock:
                now = time.time()
                ready = [a for a in POOL if self.pool_rest[a] <= now]
                if ready:
                    acct = ready[0]
                    self.pool_rest[acct] = float("inf")
                    break
                wait = min(self.pool_rest.values()) - now
            self.tr.write("harness", "all pool accounts busy or resting; waiting %.0f s" % min(wait, 30))
            time.sleep(max(1.0, min(wait, 30)))
        self.fresh_count += 1
        c = Client(acct, self.secrets.get("poolPassword", self.secrets["playerPassword"]), self.tr, self.cliloc, label)
        c.account = acct
        first = acct not in self.first_logins
        try:
            chars = c.login()
        except Exception:
            self.done(c)
            raise
''', '''    def fresh(self, race="human", female=False, label="fresh", city=ISLE_CITY, first_login=False):
        """A brand-new character on a rested pool account, through the real creation packet. Disconnect it with
        done() so the account can rest.

        cc-P735: city=HAVEN_CITY asks for creation's New Haven start: a character whose account has finished or skipped
        the tutorial (on an isle-ready world city 0 wakes on the isle). first_login=True prefers an account this run has
        not made a character on yet (P64-1)."""
        # Thread-safe: the soak asks for three at once. An account is marked busy (rest = forever) the moment it is
        # picked, and done() starts its rest.
        while True:
            with self.pool_lock:
                now = time.time()
                ready = [a for a in POOL if self.pool_rest[a] <= now]
                if first_login:
                    ready.sort(key=lambda a: a in self.first_logins)
                if city == HAVEN_CITY:
                    ready.sort(key=lambda a: a not in self.haven_open)   # stable: keeps first_login's order within
                if ready:
                    acct = ready[0]
                    self.pool_rest[acct] = float("inf")
                else:
                    acct = None
                    wait = min(self.pool_rest.values()) - now
            if acct is None:
                self.tr.write("harness", "all pool accounts busy or resting; waiting %.0f s" % min(wait, 30))
                time.sleep(max(1.0, min(wait, 30)))
                continue
            c = Client(acct, self.secrets.get("poolPassword", self.secrets["playerPassword"]), self.tr, self.cliloc, label)
            c.account = acct
            try:
                chars = c.login()
            except Exception:
                self.done(c)
                raise
            if city == HAVEN_CITY and self.haven_locked(c):
                self.unlock_haven(c)   # rests this account; take the next ready one
                continue
            if city == HAVEN_CITY:
                self.haven_open.add(acct)
            break
        self.fresh_count += 1
        first = acct not in self.first_logins
''')

rep('''        try:
            c.create(name[:16], race=race, female=female)
        except Exception:
            self.done(c)
            raise
        c.name = name[:16]
''', '''        try:
            c.create(name[:16], race=race, female=female, city=city)
        except Exception:
            self.done(c)
            raise
        c.name = name[:16]
''')

rep('''    def done(self, c):
''', '''    @staticmethod
    def haven_locked(c):
        """cc-P735: the start list this login was sent shows New Haven locked (cc-P717), or has no New Haven entry."""
        cities = [n for _, n, _ in (c.cities or [])]
        return len(cities) <= HAVEN_CITY or cities[HAVEN_CITY] == LOCKED_HAVEN

    def unlock_haven(self, c):
        """cc-P735: open New Haven for c's pool account the way a player does (cc-P717: a character of the account skips
        the tutorial; graduating does the same): a throwaway made with the isle's city wakes on the isle, and the bot's
        Admin skips its tutorial ([Tutorial skip, ClusterFTutorial.Skip -> TutorialStart.Unlock). The account then rests
        like any other; the throwaway is never answered a window, so the patch-notes bulletin stays unseen for P64-1
        (ClusterFBulletin marks it seen only on a reply). The throwaway is left in its slot (fresh() reuses full slots)."""
        acct = c.account
        try:
            slot = next((i for i, n in enumerate(c.chars) if not n), None)
            if slot is None:
                c.delete_character(0)
                c.wait(lambda: len(c.chars) > 0 and not c.chars[0], 10)
            self.fresh_count += 1
            n = self.fresh_count
            name = "Bot Unlock %s%s" % (chr(65 + (n // 26) % 26), chr(97 + n % 26))
            c.create(name[:16], race="human", female=False, city=ISLE_CITY)
            with self.admin_lock:
                a = self.ensure_admin()
                a.command("[go 0x%X" % c.serial, 1.0)
                a.command("[Tutorial skip", 0.2)
                if a.wait_target(6):
                    a.target_obj(c.serial)
            skipped = c.find_text(r"You skipped the tutorial", timeout=10) is not None
            self.tr.write("harness", "%s: New Haven locked; %s (at %s) woke on the isle, the Admin skipped its tutorial: %s"
                          % (acct, name, (c.pos or ())[:3], "yes" if skipped else "NO"))
            if not skipped:
                raise LoginFailed("could not open New Haven for %s: the skip of %s was not seen" % (acct, name))
            self.haven_open.add(acct)
        finally:
            self.done(c)

    def done(self, c):
''')

open(p, "w", encoding="utf-8", newline="").write(s)
print("edited", p)
