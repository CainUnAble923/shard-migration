"""cc-P480 (a copy of cc-P289's driver, adapted to P480: the backpack lesson before the paperdoll, the floor tiles,
the bright supplies, Rook's core-only menu, the companion pick and the graduation elixir). cc-P289: one real play-through of the New Haven tutorial's core, on a PRIVATE test shard, through the play-test bot's
client (tools/playtest-bot/uobot, the same packets a real client sends). Nothing here grants a station: every step is a
player action the server checks (walk, equip, open, speak, die, resurrect, bank, gate, talk, watch).

    python -P playthrough.py --port 2596 --out <folder> --map <overlay folder> --tiledata <client folder>
                             [--bot <tools/playtest-bot>] [--golem Iron] [--name "Iron Trainee"] [--parts seed,core,skip]

  seed  Iron's Admin runs [ClusterFSeedTutorial dryrun, the seed, the seed again and a dry run (idempotence).
  core  Iron's Player account makes a FRESH character (normal creation, 0xF8), whose first login enters the core;
        it plays the nine core trials in order through Rook's pages and graduates at Rook, then opens its box.
  skip  The Admin clears that account's tutorial record ([Tutorial reset, the only staff step), the character logs in
        again and is entered; it says No at the second skip confirmation, then skips with both, takes Remedial
        training from Rook, plays the nine trials again and graduates.

Writes <out>/playlog.txt (System lines, gumps, arrows, moves and state changes: the evidence) and <out>/transcript.txt
(every packet line). Passwords come from D:\\UO\\golem\\Get-GolemTestAccount.ps1 and never reach a file.
Test ports only (safety.check_test_target: 2594-2599, never 2593). ASCII only.
"""
import argparse, collections, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))

# -- the places (TutorialCorePlacement.cs, TutorialRecruiter.cs, ClusterFNewHavenSeeder.cs) --------------------------
ARRIVAL = (3503, 2574)
ROOK = (3500, 2572)
FIRST_MARK, SECOND_MARK = (3499, 2571), (3501, 2571)
DEATH, HEALER, GATE, VISION = (3402, 2617), (3402, 2613), (3402, 2615), (3402, 2619)
PHRASE = "I am ready to learn"
FLOOR, BLUE, GOLD, SUPPLY = 0x050E, 0x4F1, 0xAA1, 0x4F2   # TutorialStyle
CORE = ["core.movement", "core.backpack", "core.paperdoll", "core.chat", "core.death", "core.banking",
        "core.travel", "core.league", "core.loop"]
TITLES = {"core.movement": "Walking, running and the camera", "core.paperdoll": "Your paperdoll",
          "core.backpack": "Your backpack", "core.chat": "Speaking and the journal",
          "core.death": "Death and resurrection", "core.banking": "The bank", "core.travel": "Getting around",
          "core.league": "The League of Extraordinary Citizens", "core.loop": "The loop (a vision)"}
RECT = (3370, 2540, 3540, 2650)      # the walk: the farm gate to the plaza and the bank
IMP, WET, SURF = 0x40, 0x80, 0x200
PERSON, STEP = 16, 2
LEAVE_PICK = False
P = None   # uobot.packets, imported in main once --bot is on the path


class Log:
    def __init__(self, path):
        self.f = open(path, "w", encoding="ascii", errors="replace")
        self.t0 = time.time()
        self.fails = []

    def __call__(self, text):
        line = "[%7.1f] %s" % (time.time() - self.t0, text)
        print(line, flush=True)
        self.f.write(line + "\n")
        self.f.flush()

    def check(self, ok, what):
        self("%s %s" % ("PASS" if ok else "FAIL", what))
        if not ok:
            self.fails.append(what)
        return ok


class Grid:
    """Where a walker can stand, from the map files: pinned Movement.cs reduced to land flags, impassable statics within
    PersonHeight and surfaces (P188's Walk, notes/cc-P188-tools/build_way_in.py). Server items and mobiles are added
    from what the shard shows the client; a refused step is learned and the path planned again."""

    def __init__(self, mapdir, tiledir, rect):
        from mapbuild import uofiles
        self.m = uofiles.MapFile(mapdir, 1)
        self.land, self.items = uofiles.read_tiledata(tiledir)
        x1, y1, x2, y2 = rect
        sts = collections.defaultdict(list)
        for s in uofiles.statics_in(mapdir, 1, x1, y1, x2, y2):
            sts[(s[0], s[1])].append(s)
        self.stand, self.low, self.hi = {}, {}, {}
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.stand[(x, y)], self.low[(x, y)], self.hi[(x, y)] = self._tile(x, y, sts.get((x, y), []))
        self.learned = set()

    def _tile(self, x, y, sts):
        t = self.m.get(x, y)
        if self.land[t[0]][0] & (IMP | WET):
            return None, None, None
        zs = [self.m.get(x, y)[1], self.m.get(x + 1, y)[1], self.m.get(x, y + 1)[1], self.m.get(x + 1, y + 1)[1]]
        z = (min(zs) + max(zs)) // 2
        top, low, hi = z, min(zs), max(zs)
        for s in sts:
            it = self.items[s[3]]
            if it["flags"] & SURF and s[2] + it["height"] >= top and s[2] <= z + PERSON:
                top, low, hi = max(top, s[2] + it["height"]), s[2], max(top, s[2] + it["height"])
        for s in sts:
            it = self.items[s[3]]
            if (it["flags"] & IMP) and not (it["flags"] & SURF) and s[2] < top + PERSON and s[2] + max(it["height"], 1) > top:
                return None, None, None
        return top, low, hi

    def blocked_now(self, client, mobiles=True):
        out = set(self.learned)
        for s, it in list(client.items.items()):
            if it.get("world") and "graphic" in it and it["graphic"] < len(self.items):
                td = self.items[it["graphic"]]
                if td["flags"] & IMP and not td["flags"] & SURF and "door" not in td["name"].lower():
                    out.add((it["x"], it["y"]))
        for s, m in list(client.mobiles.items()):
            if mobiles and s != client.serial and "x" in m:
                out.add((m["x"], m["y"]))
        return out

    def can(self, a, b, blocked):
        if b in blocked or self.stand.get(b) is None or self.stand.get(a) is None:
            return False
        # pinned Movement.cs steps up from the start tile's top (land: its highest corner) by StepHeight
        return self.low[b] <= max(self.stand[a], self.hi[a]) + STEP or self.stand[b] - self.stand[a] <= STEP

    def path(self, start, goals, blocked):
        goals = set(goals)
        prev = {start: None}
        q = collections.deque([start])
        while q:
            c = q.popleft()
            if c in goals:
                out = []
                while c is not None:
                    out.append(c)
                    c = prev[c]
                return out[::-1]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                n = (c[0] + dx, c[1] + dy)
                if n in prev or not self.can(c, n, blocked - goals):
                    continue
                if dx and dy and not (self.can(c, (c[0] + dx, c[1]), blocked) and self.can(c, (c[0], c[1] + dy), blocked)):
                    continue
                prev[n] = c
                q.append(n)
        return None


DIR_OF = {(0, -1): 0, (1, -1): 1, (1, 0): 2, (1, 1): 3, (0, 1): 4, (-1, 1): 5, (-1, 0): 6, (-1, -1): 7}


class Player:
    def __init__(self, client, grid, log):
        self.c, self.g, self.log = client, grid, log
        self.seen = 0            # messages already in the play log
        self.gseen = 0
        self.aseen = 0
        self.opened = []

    # -- the evidence --------------------------------------------------------------------------------------------
    def drain(self):
        c = self.c
        for m in c.messages[self.seen:]:
            self.log("  say  %s: %s" % (m["name"] or "-", m["text"]))
            if re.search(r"Guards!|a criminal", m["text"] or ""):
                self.log("  guards called; mobiles near: %s" % self.who_is_near())
        self.seen = len(c.messages)
        for g in c.gumps[self.gseen:]:
            self.log("  gump %s" % " | ".join(t for t in c.gump_text(g) if t)[:600])
        self.gseen = len(c.gumps)
        for a in c.arrows[self.aseen:]:
            self.log("  arrow %s" % ("to %d,%d" % (a["x"], a["y"]) if a["active"] else "off"))
        self.aseen = len(c.arrows)

    def earned(self, title, timeout=4):
        """An achievement's unlock gump (or a line) naming it."""
        rx = re.compile(re.escape(title), re.I)
        return self.c.wait(lambda: any(any(rx.search(t or "") for t in self.c.gump_text(g)) for g in self.c.gumps)
                           or any(rx.search(m["text"] or "") for m in self.c.messages), timeout)

    def who_is_near(self, r=10):
        out = []
        for s, m in list(self.c.mobiles.items()):
            if "x" in m and self.c.pos and abs(m["x"] - self.c.pos[0]) <= r and abs(m["y"] - self.c.pos[1]) <= r:
                out.append("0x%X body 0x%X noto %s at %d,%d %s" % (s, m.get("body", 0), m.get("notoriety"), m["x"], m["y"], m.get("name") or ""))
        return out

    def pos(self):
        return (self.c.pos[0], self.c.pos[1])

    def wait_text(self, pattern, timeout=8, since=None):
        m = self.c.find_text(pattern, since=self.seen if since is None else since, timeout=timeout)
        return m

    def wait_gump(self, pattern, timeout=8, since=None):
        rx = re.compile(pattern, re.I)
        return self.c.wait_gump(lambda g: any(rx.search(t or "") for t in self.c.gump_text(g)), timeout=timeout,
                                since=self.gseen if since is None else since)

    # -- moving ----------------------------------------------------------------------------------------------------
    def step(self, d):
        before = self.pos()
        for _ in range(2):           # the first step in a new direction only turns
            if self.c.walk(d, 1, run=True, pause=0.05) != 1:
                return False
            if self.pos() != before:
                return True
        return self.pos() != before

    def go(self, target, within=0, tries=12):
        self.opened = []
        goals = [(target[0] + dx, target[1] + dy) for dx in range(-within, within + 1) for dy in range(-within, within + 1)]
        for attempt in range(tries):
            if self.pos() in goals:
                return True
            blocked = self.g.blocked_now(self.c)
            p = self.g.path(self.pos(), goals, blocked)
            if not p:
                # a player shoves through a mobile at full stamina (pinned Mobile.CheckShove), e.g. its own pet that
                # follows it into a one-tile doorway: plan through mobiles before giving up
                p = self.g.path(self.pos(), goals, self.g.blocked_now(self.c, mobiles=False))
                if p:
                    self.log("  walk: the way is through someone; shoving (near: %s)" % self.who_is_near(3))
            if not p:
                # someone standing in a doorway closes the only way out; people move, so wait and plan again
                self.log("  walk: no path from %s to %s within %d; near: %s" % (self.pos(), target, within, self.who_is_near(3)))
                if attempt >= 4:
                    return False
                self.c.sleep(2.0)
                self.drain()
                continue
            for a, b in zip(p, p[1:]):
                if self.pos() != a:
                    break
                if not self.step(DIR_OF[(b[0] - a[0], b[1] - a[1])]):
                    # a door closes on its own, so a walk may open the same one again (up to three times); a door's tile
                    # is never learned as blocked, or every later walk through that house finds no path
                    door = self.door_at(b)
                    if door:
                        if self.opened.count(door) < 3:
                            self.opened.append(door)
                            self.log("  -> opens the door 0x%08X at %s" % (door, b))
                            self.c.dclick(door)
                            self.c.sleep(1.0)
                        break
                    self.g.learned.add(b)
                    break
            self.drain()
        ok = self.pos() in goals
        self.log("  walk: %s at %s (target %s within %d)" % ("arrived" if ok else "STUCK", self.pos(), target, within))
        return ok

    def door_at(self, xy):
        for s, it in list(self.c.items.items()):
            if it.get("world") and (it["x"], it["y"]) == xy and "door" in self.g.items[it["graphic"]]["name"].lower():
                return s
        return None

    # -- finding things ---------------------------------------------------------------------------------------------
    def mobile_at(self, xy, r=1, name=None):
        best = None
        for s, m in list(self.c.mobiles.items()):
            if s == self.c.serial or "x" not in m:
                continue
            if abs(m["x"] - xy[0]) <= r and abs(m["y"] - xy[1]) <= r:
                if name:
                    n = m.get("name") or self.c.mobile_name(s) or ""
                    if name.lower() not in n.lower():
                        continue
                best = s
        return best

    def item_at(self, xy, graphic=None, r=0):
        for s, it in self.c.world_items_near(xy[0], xy[1], r, graphic).items():
            return s
        return None

    def in_pack(self, graphic=None, hue=None):
        bp = self.c.backpack()
        for s, it in list(self.c.items.items()):
            if it.get("container") == bp and (graphic is None or it.get("graphic") == graphic) and (hue is None or it.get("hue") == hue):
                return s
        return None

    def lift(self, serial, amount=1):
        """Lifts an item, waiting out the action delay (cliloc 500119) as a player would. True when held."""
        for attempt in range(4):
            n = len(self.c.messages)
            self.c.sleep(1.1)
            self.log("  -> lift 0x%08X" % serial)
            self.c.send(P.lift(serial, amount))
            self.c.sleep(0.6)
            if not any(m.get("cliloc") in (500119, 3000000 + 500119) or "must wait" in (m["text"] or "") for m in self.c.messages[n:]):
                return True
        return False

    def open_pack(self):
        bp = self.c.backpack()
        self.c.dclick(bp)
        self.c.wait(lambda: bp in self.c.containers, 5)
        self.c.sleep(0.6)
        return bp


def recruiter_station(pl, key):
    """Double-clicks Rook and presses the station's button (BtnStationBase 100 + its index in TutorialStations.All)."""
    c = pl.c
    rook = pl.mobile_at(ROOK, 1, "Rook")
    if not rook:
        pl.log("  Rook is not at %s" % (ROOK,))
        return None
    for attempt in range(2):
        n, m0 = len(c.gumps), len(c.messages)
        c.dclick(rook)
        g = c.wait_gump(lambda g: any("league recruiter" in (t or "").lower() for t in c.gump_text(g)), timeout=8, since=n)
        pl.drain()
        # double-clicks too close together are refused ("You must wait to perform another action"): wait, once more
        if g is not None or c.find_text(r"You must wait to perform another action", since=m0) is None:
            return g
        pl.log("  the double-click on Rook was refused as too soon: again")
        c.sleep(1.5)
    return g


def press_station(pl, g, key):
    # P480: the core comes first in TutorialStations.All, in CORE's order; a button is 100 + that index
    c = pl.c
    texts = [t or "" for t in c.gump_text(g)]
    if not any(TITLES[key] in t for t in texts):
        pl.log("  no label for %s in %s" % (key, texts[:14]))
        return False
    c.reply_gump(g, 100 + CORE.index(key))
    return True


DONE = r"Done\. Your next lesson is ready"


def t_movement(pl, log):
    c = pl.c
    blue = next((s for s, it in c.items.items() if it.get("graphic") == FLOOR and it.get("hue") == BLUE
                 and (it.get("x"), it.get("y")) == FIRST_MARK), None)
    gold = next((s for s, it in c.items.items() if it.get("graphic") == FLOOR and it.get("hue") == GOLD
                 and (it.get("x"), it.get("y")) == SECOND_MARK), None)
    log.check(blue is not None, "a blue floor tile (0x%X, hue 0x%X) lies at %s" % (FLOOR, BLUE, FIRST_MARK))
    log.check(gold is not None, "a gold floor tile (0x%X, hue 0x%X) lies at %s" % (FLOOR, GOLD, SECOND_MARK))
    log.check(pl.go(FIRST_MARK, 0), "walked onto the blue tile %s" % (FIRST_MARK,))
    log.check(pl.wait_text(r"Now the glowing gold tile", 5) is not None, "the System says: now the glowing gold tile")
    log.check(pl.go(SECOND_MARK, 0), "walked onto the gold tile %s" % (SECOND_MARK,))


def t_paperdoll(pl, log):
    c = pl.c
    pl.open_pack()
    cloak = c.wait(lambda: pl.in_pack(0x1515, SUPPLY) or pl.in_pack(0x1516, SUPPLY), 5)
    if not log.check(cloak is not None, "a practice cloak is in the backpack"):
        return
    for s, it in list(c.items.items()):
        if it.get("parent") == c.serial and it.get("layer") == 0x14 and s != cloak:
            log("  already wearing a cloak 0x%08X: taking it off first" % s)
            if pl.lift(s):
                c.send(P.drop(s, 60, 60, 0, c.backpack()))
    if pl.lift(cloak):
        c.send(P.equip(cloak, 0x14, c.serial))
        log("  -> dropped the practice cloak on the paperdoll (cloak layer)")


def t_backpack(pl, log):
    c = pl.c
    pl.open_pack()
    bag = c.wait(lambda: pl.in_pack(0x0E76, SUPPLY), 5)
    if log.check(bag is not None, "a blue practice bag is in the backpack"):
        c.sleep(1.1)
        c.dclick(bag)
        log("  -> double-clicked the practice bag")


def t_chat(pl, log):
    c = pl.c
    c.say("hello there")
    c.sleep(1.5)
    log.check(pl.wait_gump(DONE, 1) is None, "a different line does not finish the chat lesson")
    c.say(PHRASE)


def t_death(pl, log):
    c = pl.c
    log.check(pl.go(DEATH, 2), "walked to the death echo at the farm gate")
    echo = pl.mobile_at(DEATH, 1, "echo")
    if not log.check(echo is not None, "the death lesson echo stands at %s" % (DEATH,)):
        return
    n = len(c.gumps)
    c.dclick(echo)
    g = c.wait_gump(lambda g: any("will kill you" in (t or "") for t in c.gump_text(g)), 6, since=n)
    pl.drain()
    if not log.check(g is not None, "the echo asks before the lesson kills"):
        return
    c.reply_gump(g, 1)
    died = c.wait(lambda: c.body in GHOSTS, 8)
    c.sleep(2.0)
    pl.drain()
    log.check(died is not None, "the character died (body 0x%X), now at %s" % (c.body or 0, pl.pos()))
    g = ghost_to_healer(pl, log)
    if log.check(g is not None, "the tutorial healer offers resurrection"):
        c.reply_gump(g, 1)


def ghost_to_healer(pl, log):
    """As the hint says: double-click Sera. If that brings nothing, walk out of her range and back in, which is what
    makes a stock healer offer (BaseHealer.OnMovement)."""
    c = pl.c
    rx = lambda g: any("return to life" in (t or "") for t in c.gump_text(g))
    n = len(c.gumps)
    healer = pl.mobile_at(HEALER, 1, "Sera")
    if healer:
        c.dclick(healer)
        log("  -> the ghost double-clicks Sera")
    g = c.wait_gump(rx, 5, since=n)
    pl.drain()
    log.check(g is not None, "double-clicking the healer as a ghost offers resurrection")
    if g is None:
        log("  walking out of the healer's range and back in")
        pl.go((HEALER[0] + 7, HEALER[1]), 1)
        n = len(c.gumps)
        pl.go(HEALER, 2)
        g = c.wait_gump(rx, 5, since=n)
        pl.drain()
    return g


def t_banking(pl, log):
    c = pl.c
    arrow = c.arrows[-1] if c.arrows else None
    bank = (arrow["x"], arrow["y"]) if arrow and arrow["active"] else (3492, 2577)
    log("  the arrow points to %s" % (bank,))
    log.check(pl.go(bank, 2), "walked to the banker")
    n = len(c.containers)
    c.say("bank", keywords=(0x0002,))
    box = c.wait(lambda: c.containers[n] if len(c.containers) > n else None, 6)
    pl.drain()
    log.check(box is not None, "saying 'bank' opens the bank box")
    pl.open_pack()
    token = c.wait(lambda: pl.in_pack(0x0EF2, SUPPLY), 5)
    log.check(token is not None, "the blue practice token (coins 0x0EF2, hue 0x%X) is in the backpack" % SUPPLY)
    if token and box and pl.lift(token):
        c.send(P.drop(token, 60, 60, 0, box))
        log("  -> dropped the practice token into the bank box")


def t_travel(pl, log):
    c = pl.c
    log.check(pl.go(GATE, 2), "walked to the tutorial moongate")
    gate = pl.item_at(GATE, 0xF6C, 0)
    if log.check(gate is not None, "the tutorial moongate stands at %s" % (GATE,)):
        c.dclick(gate)
        c.wait(lambda: abs(pl.pos()[0] - 3501) <= 1 and abs(pl.pos()[1] - 2572) <= 1, 6)
        log.check(abs(pl.pos()[0] - 3501) <= 1, "the gate took the character to %s (the plaza)" % (pl.pos(),))


def t_league(pl, log):
    c = pl.c
    arrow = c.arrows[-1] if c.arrows else None
    reg = (arrow["x"], arrow["y"]) if arrow and arrow["active"] else (3459, 2601)
    log("  the arrow points to %s" % (reg,))
    log.check(pl.go(reg, 2), "walked to the League Registrar")
    elara = pl.mobile_at(reg, 2, "Elara")
    if log.check(elara is not None, "Elara Voss stands there"):
        c.dclick(elara)


def t_loop(pl, log):
    c = pl.c
    log.check(pl.go(VISION, 2), "walked to the vision marker")
    mk = pl.item_at(VISION, 0x1F14, 0)
    pl.before = dict(c.skills)
    if log.check(mk is not None, "the vision marker lies at %s" % (VISION,)):
        c.dclick(mk)


TRIALS = [("core.movement", t_movement, 10), ("core.backpack", t_backpack, 10), ("core.paperdoll", t_paperdoll, 10),
          ("core.chat", t_chat, 10), ("core.death", t_death, 12), ("core.banking", t_banking, 10),
          ("core.travel", t_travel, 10), ("core.league", t_league, 10), ("core.loop", t_loop, 30)]
GHOSTS = (0x192, 0x193, 0x25F, 0x260, 0x2B6, 0x2B7)


def play_core(pl, log, label):
    """The core trials, each started from the previous one's done page ("Next lesson", which opens the first lesson
    not yet done; the first from Rook's page), until the server says the core is finished."""
    c = pl.c
    acts = {k: (f, w) for k, f, w in TRIALS}
    by_title = {v: k for k, v in TITLES.items()}
    pl.go(ROOK, within=2)
    g = recruiter_station(pl, "core.movement")
    if not log.check(g is not None, "%s: Rook's page opens" % label):
        return False
    texts = [t or "" for t in c.gump_text(g)]
    log("  Rook's page: %s" % texts)
    if label == "core":
        log.check(not any("Alchemy" in t or "Magery" in t for t in texts) and any("Skip the tutorial" in t for t in texts)
                  and any("open after the core" in t for t in texts),
                  "before the core, Rook's page shows the core and Skip only")
        log.check(not any("System:" in t for t in texts), "Rook's page says no 'System:'")
    since = len(c.gumps)
    press_station(pl, g, "core.movement")
    played = []
    for _ in range(len(TRIALS) + 2):
        lesson = c.wait_gump(lambda g: any((t or "") in by_title for t in c.gump_text(g)), 6, since=since)
        pl.drain()
        if lesson is None:
            break
        key = next(by_title[t] for t in c.gump_text(lesson) if (t or "") in by_title)
        log("--- %s (%s)" % (key, label))
        if any(re.search(DONE, t or "") for t in c.gump_text(lesson)):
            log("  already done: moving on")
            done = lesson
        else:
            if key == "core.chat" and label == "remedial" and not getattr(pl, "reset_tried", False):
                pl.reset_tried = True
                since = len(c.gumps)
                c.reply_gump(lesson, 2)    # "Reset this lesson"
                again = c.wait_gump(lambda g: any(TITLES[key] == (t or "") for t in c.gump_text(g)), 6, since=since)
                pl.drain()
                log.check(again is not None and not any(re.search(DONE, t or "") for t in c.gump_text(again)),
                          "Reset this lesson reopens the lesson, not done")
            act, wait = acts[key]
            since = len(c.gumps)
            act(pl, log)
            done = c.wait_gump(lambda g: any(re.search(DONE, t or "") for t in c.gump_text(g)), wait, since=since)
            pl.drain()
            if not log.check(done is not None, "%s done" % key):
                return False
            played.append(key)
        if key == "core.loop" and getattr(pl, "before", None):
            c.send(P.status_request(c.serial, 5))
            c.sleep(1.0)
            # Focus (50) rises with stamina as the walker runs and Meditation (46) with mana regeneration (both passive,
            # sped up by testCenter.skillGainMultiplier); neither is the vision's
            changed = sorted(k for k, v in pl.before.items() if c.skills.get(k) != v and k not in (46, 50))
            log.check(not changed, "the vision changed no skill (Focus and Meditation, passive, left out)%s" % (": %s" % changed if changed else ""))
        since = len(c.gumps)
        n = len(c.messages)
        c.reply_gump(done, 1)          # "Next lesson / graduate"
        c.sleep(1.0)
        if c.find_text(r"Core finished", since=n, timeout=2):
            break
    pl.drain()
    log("  trials played this run: %s" % played)
    return log.check(c.find_text(r"Core finished\. Return to Rook", since=0) is not None,
                     "the core is finished and the done page sends the player back to Rook")


# cc-P610 (P533 U4 part 5): the graduation's rewards are required evidence, not optional log lines. A missing companion
# pick (unless the character legitimately has its pet already: --farm-pet, or a remedial graduation after the pet was
# taken) and a missing graduation box are failed checks. The patterns take P480's wording and P609's plainer one.
GRADUATED = r"^System: (Graduated|You finished the tutorial)"
OPEN_IN_TOWN = r"(Open that box here in town|Double-click your reward box here in town)"
EARNED = r"(You have earned a companion|You earned a pet)"
CHOOSE_PET = ("Choose your companion", "Choose your pet")
BOX_REASONS = ("graduating the new haven tutorial", "finishing the new haven tutorial")


def graduate(pl, log, label, expect_pick=None):
    """expect_pick: True, the pick must be offered; False, it must not be (the pet is already the character's); None,
    either (a remedial graduation)."""
    c = pl.c
    log("--- graduation (%s)" % label)
    log.check(pl.go(ROOK, 2), "walked back to Rook")
    # part 3: a wing with no trial yet says so, counts nothing, and graduation does not wait for it
    g = recruiter_station(pl, None)
    if g is not None:
        texts = [t or "" for t in c.gump_text(g)]
        log.check(any(t == "Alchemy" for t in texts) and any(t == "Crafting" for t in texts),
                  "after the core, Rook's page shows the wings under headings")
        idx = 25 if any(t == "Alchemy" for t in texts) else None   # crafting.alchemy is All[25]
        if idx is not None:
            m0 = len(c.messages)
            c.reply_gump(g, 100 + idx)
            c.sleep(1.5)
            pl.drain()
            log.check(c.find_text(r"Coming soon\. This wing is optional", since=m0) is not None, "a wing station says coming soon, optional")
            g = recruiter_station(pl, None)
            log.check(g is not None and any(t == "Alchemy" for t in c.gump_text(g)), "the wing is not marked done")
    pl.open_pack()
    before = set(pl.c.contents(c.backpack()))
    g = recruiter_station(pl, None)
    if not log.check(g is not None and any("Graduate" in (t or "") for t in c.gump_text(g)), "Rook's page offers Graduate"):
        return False
    n, m0 = len(c.gumps), len(c.messages)
    c.reply_gump(g, 3)
    c.sleep(3.0)
    pl.drain()
    log.check(c.find_text(GRADUATED, since=m0) is not None, "graduated (the fanfare line)")
    log.check(c.find_text(OPEN_IN_TOWN, since=m0) is not None, "the System says to open the box in town")
    is_pick = lambda g: any(re.search(EARNED, t or "") for t in c.gump_text(g))
    pick = c.wait_gump(is_pick, 4, since=n)
    if expect_pick is True:
        log.check(pick is not None, "the companion pick is offered at graduation")
    elif expect_pick is False:
        log.check(pick is None, "no companion pick: the character already has its pet")
    if pick is not None:
        log("  the pick: %s" % [t for t in c.gump_text(pick)])
        log.check(c.find_text(EARNED, since=m0) is not None, "the System says a companion is earned")
        # closed without choosing: Rook keeps it
        c.reply_gump(pick, 0)
        c.sleep(1.2)
        g = recruiter_station(pl, None)
        has = g is not None and any(w in (t or "") for t in c.gump_text(g) for w in CHOOSE_PET)
        log.check(has, "after closing the pick, Rook's page offers 'Choose your companion'")
        if has:
            n = len(c.gumps)
            c.reply_gump(g, 4)
            pick = c.wait_gump(is_pick, 4, since=n)
            pl.drain()
            log.check(pick is not None, "Rook's button opens the pick again")
    if pick is not None and LEAVE_PICK and label == "remedial":
        c.reply_gump(pick, 0)
        log("  --leave-pick: the pick is closed again, unchosen (for the client screenshots)")
        pick = None
    elif pick is not None:
        btns = c.gump_buttons(pick)
        log("  the pet pick is offered (%d buttons): taking the first, the dog" % len(btns))
        if btns:
            n = len(c.gumps)
            c.reply_gump(pick, btns[0][2])
            hue = c.wait_gump(lambda g: any("color" in (t or "").lower() for t in c.gump_text(g)), 4, since=n)
            pl.drain()
            if hue is not None and c.gump_buttons(hue):
                c.reply_gump(hue, c.gump_buttons(hue)[0][2])
                c.sleep(1.5)
                pl.drain()
    else:
        log("  no pet pick offered")
    # the box: open it here, in the guarded town
    pl.open_pack()
    c.sleep(1.0)
    new = [s for s in pl.c.contents(c.backpack()) if s not in before]
    log("  new in the backpack: %s" % ["0x%08X graphic 0x%X" % (s, c.items[s].get("graphic", 0)) for s in new])
    found_box = False
    for s in new:
        props = c.opl(s) or []
        log("  0x%08X: %s" % (s, " | ".join(props)))
        if any(r in p.lower() for p in props for r in BOX_REASONS):   # P480: not the loop box
            found_box = True
            m0, g0 = len(c.messages), len(c.gumps)
            c.sleep(1.1)
            c.dclick(s)
            c.sleep(3.0)
            pl.drain()
            opened = len(c.gumps) > g0 or any("open" in (m["text"] or "").lower() or "receive" in (m["text"] or "").lower() for m in c.messages[m0:])
            log.check(opened, "the graduation box opens in the guarded town")
            pl.open_pack()
            c.sleep(1.0)
            elixir = next((x for x in pl.c.contents(c.backpack()) if c.items[x].get("graphic") == 0x24E2), None)
            log.check(elixir is not None, "the box held an elixir of rebirth (0x24E2): %s" % (c.opl(elixir) if elixir else None))
            break
    log.check(found_box, "the graduation box is in the backpack")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=2596)
    ap.add_argument("--out", required=True)
    ap.add_argument("--map", required=True)
    ap.add_argument("--tiledata", required=True)
    ap.add_argument("--bot", default=r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
    ap.add_argument("--golem", default="Iron")
    ap.add_argument("--name", default="Iron Trainee")
    ap.add_argument("--parts", default="seed,core,skip")
    ap.add_argument("--leave-pick", action="store_true", help="after the remedial graduation, close the pick unchosen")
    ap.add_argument("--farm-pet", action="store_true",
                    help="the character took the farm's pet before graduating: no companion pick is expected (cc-P610)")
    a = ap.parse_args(argv)
    sys.path.insert(0, a.bot)
    global P
    from uobot.client import Client, Cliloc, Transcript
    from uobot import packets as P
    from uobot import golemcheck as GC
    os.makedirs(a.out, exist_ok=True)
    log = Log(os.path.join(a.out, "playlog.txt"))
    tr = Transcript(os.path.join(a.out, "transcript.txt"))
    cl = Cliloc(os.path.join(a.tiledata, "Cliloc.enu"), r"D:\UO\bot-shard\cache")
    parts = a.parts.split(",")
    global LEAVE_PICK
    LEAVE_PICK = a.leave_pick
    log("P480 play-through on %s:%d, parts %s" % (a.host, a.port, parts))
    grid = Grid(a.map, a.tiledata, RECT)
    log("walk grid %s: %d standable tiles" % (RECT, sum(1 for v in grid.stand.values() if v is not None)))

    adm = None
    if "seed" in parts or "skip" in parts:
        user, pw = GC.account(a.golem, "admin")
        adm = Client(user, pw, tr, cl, label="admin", test_target=(a.host, a.port))
        chars = adm.login()
        adm.play(chars.index(a.golem) if a.golem in chars else 0)
        pw = None
        A = Player(adm, grid, log)
        A.drain()
    if "seed" in parts:
        log("=== seed (the Admin)")
        for cmd in ("[ClusterFSeedTutorial dryrun", "[ClusterFSeedTutorial", "[ClusterFSeedTutorial", "[ClusterFSeedTutorial dryrun"):
            log("  admin types %s" % cmd)
            replies = adm.command(cmd, settle=3.0)
            for m in replies:
                log("    %s" % m["text"])
        A.seen = len(adm.messages)
        adm.command("[go 3500 2569 14", settle=2.0)

    pl = None
    if "core" in parts:
        log("=== core: a fresh character on %s's Player account" % a.golem)
        user, pw = GC.account(a.golem, "player")
        pc = Client(user, pw, tr, cl, label="player", test_target=(a.host, a.port))
        chars = pc.login()
        pw = None
        log("  the account's characters: %s" % [x for x in chars if x])
        if a.name in chars:
            log("  %r already exists: playing it (not fresh)" % a.name)
            pc.play(chars.index(a.name))
        else:
            pc.create(a.name, stats=(45, 35, 10), skills=((0, 30), (17, 30), (40, 30), (43, 30)))
        pl = Player(pc, grid, log)
        pc.sleep(3.0)
        log("  in the world at %s" % (pc.pos[:3],))
        if pc.body in GHOSTS:
            log("  a ghost from an earlier run: to the healer first")
            g = ghost_to_healer(pl, log)
            if g:
                pc.reply_gump(g, 1)
                pc.sleep(2.0)
        pl.drain()
        log.check(pl.wait_text(r"the League recruiter, is waiting", 2, since=0) is not None, "first login: the System greets and points to the recruiter")
        log.check(any(x["active"] and (x["x"], x["y"]) == ROOK for x in pc.arrows), "first login: a quest arrow to Rook")
        if play_core(pl, log, "core"):
            graduate(pl, log, "core", expect_pick=not a.farm_pet)

    if "skip" in parts and pl is None:
        user, pw = GC.account(a.golem, "player")
        pc = Client(user, pw, tr, cl, label="player", test_target=(a.host, a.port))
        chars = pc.login()
        pw = None
        pc.play(chars.index(a.name))
        pl = Player(pc, grid, log)
        pc.sleep(3.0)
        pl.drain()
    if "skip" in parts and pl is not None and adm is not None:
        log("=== skip, remedial, graduation (the same character, record cleared by staff)")
        adm.command("[go %d %d 14" % (pl.pos()[0], pl.pos()[1] - 2), settle=2.0)
        n = len(adm.messages)
        adm.say("[Tutorial reset")
        t = adm.wait_target(6)
        if t:
            adm.target_obj(pl.c.serial)
        adm.sleep(2.0)
        for m in adm.messages[n:]:
            log("  admin: %s" % m["text"])
        pl.c.close()
        log("  the player logs out and back in")
        time.sleep(3)
        user, pw = GC.account(a.golem, "player")
        pc = Client(user, pw, tr, cl, label="player", test_target=(a.host, a.port))
        chars = pc.login()
        pw = None
        pc.play(chars.index(a.name))
        pl = Player(pc, grid, log)
        pc.sleep(3.0)
        pl.drain()
        log.check(pl.wait_text(r"the League recruiter, is waiting", 2, since=0) is not None, "after the reset the login enters the core again")
        pl.go(ROOK, 2)
        g = recruiter_station(pl, None)
        if log.check(g is not None, "Rook's page opens"):
            pc.reply_gump(g, 1)                      # Skip the tutorial
            g1 = pl.wait_gump(r"want to skip the tutorial", 5)
            pl.drain()
            if log.check(g1 is not None, "skip: the first confirmation"):
                pc.reply_gump(g1, 1)
                g2 = pl.wait_gump(r"Really\?", 5)
                pl.drain()
                if log.check(g2 is not None, "skip: the second confirmation"):
                    pc.reply_gump(g2, 0)             # No, teach me
                    pc.sleep(1.5)
                    pl.drain()
                    g = recruiter_station(pl, None)
                    log.check(g is not None and any("You are in the core lessons" in (t or "") for t in pc.gump_text(g)), "No at the second confirmation skips nothing (still InCore)")
                    pc.reply_gump(g, 1)
                    g1 = pl.wait_gump(r"want to skip the tutorial", 5)
                    pc.reply_gump(g1, 1)
                    g2 = pl.wait_gump(r"Really\?", 5)
                    pc.reply_gump(g2, 1)
                    pc.sleep(3.0)
                    pl.drain()
                    log.check(pl.earned("Didn't Read the Manual") is not None, "skipped: Didn't Read the Manual is earned")
        g = recruiter_station(pl, None)
        if log.check(g is not None and any("Remedial training" in (t or "") for t in pc.gump_text(g)), "Rook offers Remedial training to a skipper"):
            pc.reply_gump(g, 2)
            pc.sleep(1.5)
            pl.drain()
            if play_core(pl, log, "remedial"):
                graduate(pl, log, "remedial")
                log.check(pl.earned("Read the Manual Eventually") is not None, "remedial graduation: Read the Manual Eventually is earned")

    for c in (adm, pl.c if pl else None):
        if c:
            try:
                c.close()
            except Exception:
                pass
    log("=== %d failed check(s): %s" % (len(log.fails), log.fails))
    tr.close()
    return 1 if log.fails else 0


if __name__ == "__main__":
    sys.exit(main())
