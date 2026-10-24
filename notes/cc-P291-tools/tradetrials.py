"""cc-P291: a real run of each of the 20 new wing trials (gathering, crafting, animals, bard, thieving, the four tours) on a
PRIVATE test shard, through the play-test bot's client (tools/playtest-bot/uobot: the packets a real client sends).
Every step is a player action the server checks: the core is played first (Rook shows the wings only after it, playkit's
play_core), then each trial is started from Rook's page, the character walks to its place and digs, chops, fishes, lights
a fire, crafts through the craft menu, herds, tames, plays, steals or walks the tour. No staff command completes
anything; the Admin only seeds the tutorial ([ClusterFSeedTutorial).

    python -P tradetrials.py --port 2596 --out <folder> --map <overlay folder> --tiledata <client folder>
                             [--name "Iron Trades"] [--only key,key]

Writes <out>/playlog.txt (the evidence) and <out>/transcript.txt. Helpers: playkit.py (cc-P480's driver, unchanged).
Passwords from D:\\UO\\golem\\Get-GolemTestAccount.ps1, never written. Test ports only. ASCII only.
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import playkit as K  # noqa: E402

ROOK = (3500, 2572)
YARD = (3426, 2626)                 # TutorialWingTrials.TradesYard
WORK = (YARD[0] + 2, YARD[1])       # the vein, tree, pond, first echo
MARK, CHEST = (YARD[0] + 1, YARD[1]), (YARD[0] - 1, YARD[1])
FIELD, GOAT = (3390, 2606), (3395, 2606)
DONE = r": done\. The yard has its loans back"
SK = dict(AnimalLore=2, ItemID=3, ArmsLore=4, Begging=6, Peacemaking=9, DetectHidden=14, Discordance=15, Herding=20,
          Hiding=21, Provocation=22, Snooping=28, Poisoning=30, Stealing=33, AnimalTaming=35, TasteID=36, Tracking=38,
          Stealth=47, RemoveTrap=48)
# The tours' stops (TutorialTradeTrials.cs Trades[...].Stops): the porch, the bank, the gate, the plaza, the yard,
# the healer, the Registrar.
TOURS = {"housing.basics": [(3383, 2612), (3492, 2577)],
         "travel.wing": [(3402, 2615), (3500, 2572)],
         "reputation.wing": [(3411, 2617), (3402, 2613), (3500, 2572)],
         "shard.systems": [(3459, 2601), (3492, 2577), (3500, 2572)]}
P = None
M = None  # uobot.checks_p224_mule: the craft menu helpers


def index_of(key):
    # Rook's button is 100 + the station's index in TutorialStations.All (the code's order, not this list's)
    return ALL.index(key)


ALL = ["core.movement", "core.backpack", "core.paperdoll", "core.chat", "core.death", "core.banking", "core.travel",
       "core.league", "core.loop", "combat.weapons", "combat.healing", "magic.magery", "magic.necromancy",
       "magic.chivalry", "magic.bushido", "magic.ninjitsu", "magic.mysticism", "gathering.mining",
       "gathering.lumberjacking", "gathering.fishing", "gathering.camping", "crafting.blacksmithy",
       "crafting.tailoring", "crafting.carpentry", "crafting.tinkering", "crafting.alchemy", "crafting.fletching",
       "crafting.cooking", "crafting.inscription", "crafting.cartography", "animals.taming", "bard.trial",
       "thieving.trial", "housing.basics", "travel.wing", "reputation.wing", "shard.systems"]


def start_trial(pl, log, key, place, loans=True):
    c = pl.c
    log("--- %s" % key)
    pl.go(ROOK, 2)
    g = K.recruiter_station(pl, None)
    if not log.check(g is not None, "%s: Rook's page opens" % key):
        return False
    m0 = len(c.messages)
    pl.trial_g0 = len(c.gumps)
    c.reply_gump(g, 100 + index_of(key))
    if not loans:
        return log.check(c.find_text(r"short walk|Follow the arrow", since=m0, timeout=5) is not None,
                         "%s: the tour starts and points at its first stop" % key)
    log.check(c.find_text(r"Follow the arrow to", since=m0, timeout=4) is not None, "%s: the page points to its place" % key)
    pl.go(place, 1)
    armed = c.find_text(r"loans are yours", since=m0, timeout=6)
    return log.check(armed is not None, "%s: at its place the lesson starts (loans given)" % key)


def loaners(pl):
    c = pl.c
    out = []
    for s, it in list(c.items.items()):
        if it.get("container") == c.backpack() or it.get("parent") == c.serial:
            props = c.opl(s) or []
            if any("tutorial loaner" in (p or "").lower() for p in props):
                out.append(s)
    return out


def loaner(pl, name):
    c = pl.c
    for s, it in list(c.items.items()):
        if it.get("container") == c.backpack() or it.get("parent") == c.serial:
            if any(("tutorial loaner: " + name) in (p or "").lower() for p in (c.opl(s) or [])):
                return s
    return None


def prop_near(pl, xy, word, r=1):
    c = pl.c
    for s, it in c.world_items_near(xy[0], xy[1], r).items():
        if any(word in (p or "").lower() for p in (c.opl(s) or [])):
            return s
    return None


def check_returned(pl, log, key, lent):
    c = pl.c
    c.sleep(1.0)
    pl.drain()
    left = [s for s in lent if s in c.items]
    log.check(not left, "%s: every loaner went back (%d lent, %d left)" % (key, len(lent), len(left)))


def done(pl, m0, timeout):
    return pl.c.find_text(DONE, since=m0, timeout=timeout) is not None


def step_or_done(pl, m0, timeout, label=None):
    rx = r"Step done: %s|%s" % (re.escape(label), DONE) if label else r"Step done|" + DONE
    return pl.c.find_text(rx, since=m0, timeout=timeout) is not None


def use_tool(pl, tool, target, waitfor=12):
    c = pl.c
    c.dclick(tool)
    if not c.wait_target(5):
        return False
    c.target_obj(target)
    return True


def use_skill(pl, skill, *targets, extra_wait=0.6):
    """Uses a skill and answers its target cursors in turn; an instrument prompt takes the loaned lute."""
    c = pl.c
    n = len(c.messages)
    c.send(P.use_skill(SK[skill]))
    for t in targets:
        if not c.wait_target(6):
            return False
        if c.find_text(r"instrument", since=n) and getattr(pl, "lute", None) and not getattr(pl, "lute_picked", False):
            pl.lute_picked = True
            c.target_obj(pl.lute)
            if not c.wait_target(6):
                return False
        c.target_obj(t)
        c.sleep(extra_wait)
    return True


def t_harvest(pl, log, key, tool_name, word, equip=False):
    c = pl.c
    c.sleep(1.0)
    lent = loaners(pl)
    log("  loaners: %s" % [(" | ".join(c.opl(s) or [])) for s in lent])
    tool = loaner(pl, tool_name)
    target = prop_near(pl, WORK, word, 2)
    if not log.check(tool is not None and target is not None, "%s: the loaned %s and the %s are there" % (key, tool_name, word)):
        return lent
    m0 = len(c.messages)
    for i in range(14):
        use_tool(pl, tool, target)
        if done(pl, m0, 7):
            break
        pl.drain()
    log.check(done(pl, m0, 0), "%s: a harvest finishes it" % key)
    return lent


def t_camping(pl, log):
    c = pl.c
    c.sleep(1.0)
    lent = loaners(pl)
    kindling = loaner(pl, "kindling")
    if not log.check(kindling is not None, "gathering.camping: the loaned kindling is in the pack"):
        return lent
    m0 = len(c.messages)
    for i in range(10):
        c.dclick(kindling)
        if done(pl, m0, 4):
            break
        c.sleep(1.0)
        kindling = loaner(pl, "kindling") or kindling
    log.check(done(pl, m0, 0), "gathering.camping: a lit campfire finishes it")
    return lent


CRAFTS = {
    "crafting.blacksmithy": ("smith's hammer", "Bladed", "dagger", ("ArmsLore", 0x0F52, None)),
    "crafting.tailoring": ("sewing kit", "Hats", "skullcap", None),
    "crafting.carpentry": ("saw", "Other", "barrel staves", None),
    "crafting.tinkering": ("tinker's tools", "Tools", "scissors", ("ItemID", None, "odd curio")),
    "crafting.alchemy": ("mortar and pestle", "Refresh", "refresh", ("TasteID", None, "apple")),
    "crafting.fletching": ("fletcher's tools", "Materials", "kindling", None),
    "crafting.cooking": ("skillet", "Ingredients", "dough", None),
    "crafting.inscription": ("scribe's pen", "First Circle", "Magic Arrow", None),
    "crafting.cartography": ("mapmaker's pen", "Maps", "local map", None),
}


def gump_entries(c, g):
    """(x, y, text) of each label in a gump layout: xmfhtmlgump[color] clilocs, text and htmlgump lines."""
    out, lay, lines = [], g["layout"], g["lines"]
    for m in re.finditer(r"\{\s*xmfhtmlgump(?:color)?\s+(-?\d+)\s+(-?\d+)\s+\d+\s+\d+\s+(\d+)", lay):
        out.append((int(m.group(1)), int(m.group(2)), c.cliloc.text(int(m.group(3)))))
    for m in re.finditer(r"\{\s*text\s+(-?\d+)\s+(-?\d+)\s+\d+\s+(\d+)\s*\}", lay):
        i = int(m.group(3))
        out.append((int(m.group(1)), int(m.group(2)), lines[i] if i < len(lines) else ""))
    for m in re.finditer(r"\{\s*htmlgump\s+(-?\d+)\s+(-?\d+)\s+\d+\s+\d+\s+(\d+)", lay):
        i = int(m.group(3))
        out.append((int(m.group(1)), int(m.group(2)), re.sub(r"<[^>]+>", "", lines[i]) if i < len(lines) else ""))
    return out


def press_beside(c, g, label, dx=35, dy=3, min_x=0):
    """The craft menu's rows (pinned CraftGump.cs): a button at (x, y) and its label at (x + 35, y + 3). Groups are the
    left column (label x 50), items the right (label x 255): min_x picks the column (Alchemy's group "Refresh" holds
    the item "refresh")."""
    want = label.strip().lower()
    buttons = c.gump_buttons(g)
    for x, y, text in gump_entries(c, g):
        if x >= min_x and (text or "").strip().lower() == want:
            for bx, by, bid in buttons:
                if bx == x - dx and by == y - dy:
                    n = len(c.gumps)
                    c.reply_gump(g, bid)
                    return M.craft_gump(c, n, 10)
    return None


def t_craft(pl, log, key):
    c = pl.c
    tool_name, group, item, covered = CRAFTS[key]
    pl.go(YARD, 0)   # the anvil and forge reach two tiles
    c.sleep(1.0)
    lent = loaners(pl)
    log("  loaners: %s" % [(" | ".join(c.opl(s) or [])) for s in lent])
    tool = loaner(pl, tool_name)
    if not log.check(tool is not None, "%s: the loaned %s is in the pack" % (key, tool_name)):
        return lent
    m0 = len(c.messages)
    for i in range(6):
        try:
            g = M.open_craft(c, tool)
        except AssertionError as e:
            log("  %s" % e)
            c.sleep(1.5)
            continue
        g2 = press_beside(c, g, group)
        if g2 is None:
            log("  craft menu: no %r group: %s" % (group, [e[2] for e in gump_entries(c, g)][:40]))
        else:
            g3 = press_beside(c, g2, item, min_x=200)
            if g3 is None:
                log("  craft menu: no %r row: %s" % (item, [e[2] for e in gump_entries(c, g2)][:60]))
        c.sleep(1.5)
        pl.drain()
        if step_or_done(pl, m0, 2):
            break
    made = step_or_done(pl, m0, 2)
    log.check(made, "%s: a %s made in the craft menu counts" % (key, item))
    if covered and made:
        skill, graphic, word = covered
        for i in range(8):
            target = None
            for s, it in list(c.items.items()):
                if it.get("container") != c.backpack():
                    continue
                if graphic is not None and it.get("graphic") == graphic and s not in lent:
                    target = s
                if word and any(word in (p or "").lower() for p in (c.opl(s) or [])):
                    target = s
            if target is None:
                log("  no %s target in the pack" % skill)
                break
            use_skill(pl, skill, target)
            if done(pl, m0, 4):
                break
            c.sleep(1.2)
        log.check(done(pl, m0, 0), "%s: then %s finishes it" % (key, skill))
    else:
        log.check(done(pl, m0, 2), "%s: done" % key)
    if done(pl, m0, 0):
        kept = [s for s, it in c.items.items() if it.get("container") == c.backpack() and s not in lent]
        log("  the pack after: %d own items (the product stays)" % len(kept))
    return lent


def t_animals(pl, log):
    c = pl.c
    c.sleep(1.0)
    lent = loaners(pl)
    log("  loaners: %s" % [(" | ".join(c.opl(s) or [])) for s in lent])
    goat = pl.mobile_at(GOAT, 3, "tutorial goat")
    if not log.check(goat is not None, "animals.taming: the tutorial goat is in the pen"):
        return lent
    crook = loaner(pl, "shepherd's crook")
    m0 = len(c.messages)
    pl.go((3393, 2606), 0)
    for i in range(6):
        c.dclick(crook)
        if c.wait_target(5):
            c.target_obj(goat)
            if c.wait_target(5):
                gm = c.mobiles.get(goat, {})
                c.target_xyz(3396, 2607, gm.get("z", 0))
        if step_or_done(pl, m0, 3, "Herding"):
            break
        c.sleep(1.0)
    log.check(step_or_done(pl, m0, 0, "Herding"), "animals.taming: the goat herded")
    for i in range(6):
        use_skill(pl, "AnimalTaming", goat)
        if step_or_done(pl, m0, 20, "Animal Taming"):
            break
        c.sleep(2.0)
    log.check(step_or_done(pl, m0, 0, "Animal Taming"), "animals.taming: the goat tamed")
    for i in range(6):
        c.sleep(1.5)
        use_skill(pl, "AnimalLore", goat)
        if step_or_done(pl, m0, 4, "Animal Lore"):
            break
    log.check(step_or_done(pl, m0, 0, "Animal Lore"), "animals.taming: lore on the goat")
    bandage = loaner(pl, "bandage")
    for i in range(6):
        c.sleep(1.0)
        if bandage:
            use_tool(pl, bandage, goat)
        if done(pl, m0, 12):
            break
    log.check(done(pl, m0, 0), "animals.taming: a bandage on the goat finishes it")
    c.sleep(1.0)
    log.check(goat not in c.mobiles or "x" not in c.mobiles.get(goat, {}) or pl.mobile_at(GOAT, 8, "tutorial goat") is None,
              "animals.taming: the goat went back with the loans")
    return lent


def t_bard(pl, log):
    c = pl.c
    c.sleep(1.0)
    lent = loaners(pl)
    pl.lute, pl.lute_picked = loaner(pl, "lute"), False
    e1 = pl.mobile_at(WORK, 0, "echo")
    e2 = pl.mobile_at((WORK[0], WORK[1] + 2), 0, "echo")
    if not log.check(e1 is not None and e2 is not None and pl.lute is not None, "bard.trial: two echoes and a lute"):
        return lent
    m0 = len(c.messages)
    for skill, targets, label in (("Peacemaking", (e1,), "Peacemaking"), ("Provocation", (e1, e2), "Provocation"),
                                  ("Discordance", (e2,), "Discordance")):
        for i in range(6):
            use_skill(pl, skill, *targets)
            if step_or_done(pl, m0, 5, label):
                break
            c.sleep(6.0)   # the bard skills' delay
        log.check(step_or_done(pl, m0, 0, label), "bard.trial: %s on the echoes" % skill)
    log.check(done(pl, m0, 3), "bard.trial: the three finish it")
    return lent


def t_thief(pl, log):
    c = pl.c
    c.sleep(1.0)
    lent = loaners(pl)
    log("  loaners: %s" % [(" | ".join(c.opl(s) or [])) for s in lent])
    pl.go(YARD, 0)   # beside both: the chest (lockpicking and stealing reach one tile) and the mark (snooping)
    chest = prop_near(pl, CHEST, "practice chest", 1)
    mark = pl.mobile_at(MARK, 0, "mark")
    if not log.check(chest is not None and mark is not None, "thieving.trial: the practice chest and the mark are there"):
        return lent
    m0 = len(c.messages)

    def attempt(label, act, tries=6, wait=4, pause=10.5):
        for i in range(tries):
            act()
            if step_or_done(pl, m0, wait, label):
                break
            c.sleep(pause)
        return log.check(step_or_done(pl, m0, 0, label), "thieving.trial: %s" % label)

    attempt("Detecting Hidden", lambda: use_skill(pl, "DetectHidden", chest))
    attempt("Remove Trap", lambda: use_skill(pl, "RemoveTrap", chest))
    pick = loaner(pl, "lockpicks")
    attempt("Lockpicking", lambda: use_tool(pl, loaner(pl, "lockpicks") or pick, chest), pause=1.5)
    c.dclick(chest)
    c.sleep(1.5)
    purse = next((s for s, it in c.items.items() if it.get("container") == chest), None)
    log("  the chest holds: %s" % [(" | ".join(c.opl(s) or [])) for s, it in c.items.items() if it.get("container") == chest])
    if purse:
        attempt("Stealing", lambda: use_skill(pl, "Stealing", purse))
    else:
        log.check(False, "thieving.trial: the purse is in the opened chest")
    pack = next((s for s, it in c.items.items() if it.get("parent") == mark and it.get("layer") == 0x15), None)
    if log.check(pack is not None, "thieving.trial: the mark wears a backpack"):
        attempt("Snooping", lambda: c.dclick(pack), pause=1.5)
    attempt("Begging", lambda: use_skill(pl, "Begging", mark), wait=8)
    potion, dagger = loaner(pl, "lesser poison potion"), loaner(pl, "dagger")
    attempt("Poisoning", lambda: use_skill(pl, "Poisoning", potion, dagger), wait=8)

    def track():
        n = len(c.gumps)
        c.send(P.use_skill(SK["Tracking"]))
        g = c.wait_gump(None, 6, since=n)
        if g:
            c.reply_gump(g, 1)
    attempt("Tracking", track)
    attempt("Hiding", lambda: c.send(P.use_skill(SK["Hiding"])), tries=8)
    attempt("Stealth", lambda: c.send(P.use_skill(SK["Stealth"])), tries=8)
    log.check(done(pl, m0, 3), "thieving.trial: the ten finish it")
    return lent


def t_tour(pl, log, key):
    c = pl.c
    start = len(c.messages)
    c.sleep(0.5)
    lent = loaners(pl)
    for i, stop in enumerate(TOURS[key]):
        m0 = len(c.messages)
        pl.go(stop, 2)
        ok = c.find_text(r"Step done|" + DONE, since=m0, timeout=4) is not None
        log.check(ok, "%s: stop %d at %s counted" % (key, i + 1, stop))
    log.check(c.find_text(DONE, since=start, timeout=3) is not None, "%s: the last stop finishes it" % key)
    return lent


def t_leave(pl, log):
    c = pl.c
    if not start_trial(pl, log, "gathering.mining", YARD):
        return
    c.sleep(1.0)
    lent = loaners(pl)
    m0 = len(c.messages)
    pl.go((YARD[0] - 20, YARD[1] - 6), 2)
    log.check(c.find_text(r"You left the trades yard", since=m0, timeout=6) is not None, "leaving the trades yard stops the lesson")
    check_returned(pl, log, "leaving", lent)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=2596)
    ap.add_argument("--out", required=True)
    ap.add_argument("--map", required=True)
    ap.add_argument("--tiledata", required=True)
    ap.add_argument("--bot", default=r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
    ap.add_argument("--golem", default="Iron")
    ap.add_argument("--name", default="Iron Trades")
    ap.add_argument("--only", default="")
    a = ap.parse_args(argv)
    sys.path.insert(0, a.bot)
    global P, M
    from uobot.client import Client, Cliloc, Transcript
    from uobot import packets
    from uobot import golemcheck as GC
    from uobot import checks_p224_mule as mule
    P = K.P = packets
    M = mule
    os.makedirs(a.out, exist_ok=True)
    log = K.Log(os.path.join(a.out, "playlog.txt"))
    tr = Transcript(os.path.join(a.out, "transcript.txt"))
    cl = Cliloc(os.path.join(a.tiledata, "Cliloc.enu"), r"D:\UO\bot-shard\cache")
    log("P291 trade trials on %s:%d" % (a.host, a.port))
    grid = K.Grid(a.map, a.tiledata, (3370, 2540, 3540, 2650))

    user, pw = GC.account(a.golem, "admin")
    adm = Client(user, pw, tr, cl, label="admin", test_target=(a.host, a.port))
    chars = adm.login()
    pw = None
    adm.play(chars.index(a.golem) if a.golem in chars else 0)
    for cmd in ("[ClusterFSeedTutorial",):
        log("  admin types %s" % cmd)
        for m in adm.command(cmd, settle=3.0):
            log("    %s" % m["text"])
    adm.command("[go 3500 2569 14", settle=2.0)

    user, pw = GC.account(a.golem, "player")
    pc = Client(user, pw, tr, cl, label="player", test_target=(a.host, a.port))
    chars = pc.login()
    pw = None
    log("  the account's characters: %s" % [x for x in chars if x])
    if a.name in chars:
        pc.play(chars.index(a.name))
    else:
        pc.create(a.name, stats=(45, 35, 10), skills=((0, 30), (17, 30), (40, 30), (43, 30)))
    pl = K.Player(pc, grid, log)
    pc.sleep(3.0)
    pl.drain()
    entered = pl.wait_text(r"League recruiter, is waiting|Welcome back", 2, since=0) is not None
    log.check(entered, "login: the character is in the tutorial")
    if not K.play_core(pl, log, "core"):
        log("=== the core did not finish; the wings stay closed")

    plan = [("gathering.mining", YARD, lambda: t_harvest(pl, log, "gathering.mining", "pickaxe", "practice vein")),
            ("gathering.lumberjacking", YARD, lambda: t_harvest(pl, log, "gathering.lumberjacking", "hatchet", "practice tree")),
            ("gathering.fishing", YARD, lambda: t_harvest(pl, log, "gathering.fishing", "fishing pole", "practice pond")),
            ("gathering.camping", YARD, lambda: t_camping(pl, log))]
    plan += [(k, YARD, (lambda k=k: t_craft(pl, log, k))) for k in CRAFTS]
    plan += [("animals.taming", FIELD, lambda: t_animals(pl, log)),
             ("bard.trial", YARD, lambda: t_bard(pl, log)),
             ("thieving.trial", YARD, lambda: t_thief(pl, log))]
    plan += [(k, None, (lambda k=k: t_tour(pl, log, k))) for k in TOURS]
    for key, place, act in plan:
        if a.only and key not in a.only.split(","):
            continue
        if start_trial(pl, log, key, place, loans=place is not None):
            lent = act()
            check_returned(pl, log, key, lent)
    if not a.only:
        t_leave(pl, log)

    for c in (adm, pc):
        try:
            c.close()
        except Exception:
            pass
    log("=== %d failed check(s): %s" % (len(log.fails), log.fails))
    tr.close()
    return 1 if log.fails else 0


if __name__ == "__main__":
    sys.exit(main())
