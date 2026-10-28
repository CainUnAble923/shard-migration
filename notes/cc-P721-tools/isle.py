"""cc-P721: P718's isle.py, changed for P721's lessons: after the pet commands the bot holds Wren's pitchfork, switches
to war mode and attacks a pest itself before "all kill"; the heal step bandages Pip, the hurt farm boy; the first arrival
lies on the sand for a few seconds before the arrow to Tamsin.

cc-P718: P707's isle.py, changed for P718's lessons: the backpack lesson opens the character window first (a
double-click on yourself), the cloak is taken from the clothes table, Wren's pet commands ("all follow me", then "all
guard me") come before the pests, and the field gate is opened if it has swung shut. Everything else is P707's.

cc-P707: the Wakening Isle play-through (P663's bot route, rewritten for the isle), on a PRIVATE test shard, through
the play-test bot's client (tools/playtest-bot/uobot: the packets a real client sends). Nothing here grants a lesson:
every step is a player action the server checks. The walking, the evidence log and the item finders are cc-P480's
(notes/cc-P480-tools/playthrough.py, imported); the places are the isle's (TutorialWorld.cs, TutorialCorePlacement.cs).

    python -P isle.py --port 2596 --out <folder> --map <overlay folder> --tiledata <client folder>
                      [--bot <tools/playtest-bot>] [--golem Iron] [--name "Iron Islander"] [--parts seed,isle,skip]

  seed  Iron's Admin runs [ClusterFSeedTutorial (dry run, seed, seed again: idempotence) and [Tutorial copies.
  isle  Iron's Player account makes a FRESH character with the first city on the list (Tutorial Island), wakes on a
        private copy's beach, takes every lesson from Tamsin's window west to east (the farm with its pet, pests and
        bandage, the yard's death, the bank, the lodge, the vision at the stones) and walks through the dock moongate,
        ending beside Rook in New Haven. Each lesson's time is logged.
  skip  a second fresh character picks New Haven at creation and must start on the plaza with no tutorial.

Writes <out>/playlog.txt (the evidence: System lines, gumps, arrows, moves, checks) and <out>/transcript.txt (every
packet). Passwords come from D:\\UO\\golem\\Get-GolemTestAccount.ps1 and never reach a file. Test ports only. ASCII.
"""
import argparse, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # cc-P707: islegrid (python -P leaves the script folder off the path)
sys.path.insert(0, os.path.join(HERE, "..", "cc-P480-tools"))
sys.path.insert(0, os.path.join(HERE, "..", "cc-P707-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))
import playthrough as base   # cc-P480: Grid, Player, Log
import islegrid  # noqa: F401  cc-P707 run 4: the dock planks standable (it patches base.Grid; run 4 had no path to the gate)

# -- the isle (TutorialWorld.cs:36-75, TutorialCorePlacement.cs:38-75, TutorialFarm.cs:71-90) -------------------------
RECT = (6594, 3905, 6865, 4049)
BEACH, TAMSIN = (6638, 3993), (6640, 3992)
BLUE_TILE, GOLD_TILE = (6646, 3992), (6649, 3992)
CAMP, RACK, SIGN = (6656, 3990), (6665, 3992), (6692, 3990)
WREN, PESTS = (6714, 3978), (6702, 3978)
RAT, SERA = (6736, 3998), (6740, 4000)
BANK_STOP, MERRIN = (6762, 3981), (6762, 3976)
LODGE, ELARA = (6782, 3994), (6782, 3999)
STONES = (6794, 3982)
GATE = (6832, 3991)
TABLE = (6664, 3990)                       # cc-P718: TutorialCorePlacement.ClothesTable
FIELD_GATE = ((6713, 3979),)               # cc-P718: TutorialFarm.FieldGateSpots
BELOW_WREN = (6714, 3979)                  # the tile a player enters the field gate from
GATE_CLOSED = (0x0843,)                    # LightWoodGate NorthCCW, closed
ROOK_EXIT = (3632, 2584)     # HavenSpots.MoongateExit, beside Rook (3631,2584); cc-P718: P678 moved New Haven
HAVEN_START = (3634, 2586)   # HavenSpots.Start (cc-P718: P678 moved New Haven)
CORE = ["core.movement", "core.backpack", "core.paperdoll", "core.chat", "core.farm", "core.death", "core.banking",
        "core.league", "core.loop", "core.travel"]
TITLES = {"core.movement": "Walk and run", "core.backpack": "Your backpack",
          "core.paperdoll": "Your character window and clothes", "core.chat": "Speak and read your Journal",
          "core.farm": "The farm: your pet, pests and bandages", "core.death": "Death and resurrection",
          "core.banking": "The bank", "core.league": "The League of Extraordinary Citizens",
          "core.loop": "Watch a loop vision", "core.travel": "Getting around"}
DONE = r"Lesson finished\."
FLOOR, BLUE, GOLD, SUPPLY = 0x050E, 0x4F1, 0xAA1, 0x4F2   # TutorialStyle
GHOSTS = (0x192, 0x193, 0x25F, 0x260, 0x2B6, 0x2B7)
P = None


def near(a, b, r):
    return abs(a[0] - b[0]) <= r and abs(a[1] - b[1]) <= r


def walk_to(pl, log, spot, within, what):
    # cc-P718: leaving the farm field, open its gate first if it has swung shut
    if in_field(pl.pos()) and not in_field(spot):
        open_field_gate(pl, log, INSIDE_GATE)
    return log.check(pl.go(spot, within), "walked to %s %s (now %s, map %s)" % (what, spot, pl.pos(), pl.c.map_id if hasattr(pl.c, "map_id") else "?"))


def guide_station(pl, log, key):
    """Double-clicks Tamsin and presses the lesson's button (100 + its index in TutorialStations.All; the core is first)."""
    c = pl.c
    tam = pl.mobile_at(TAMSIN, 3, "Tamsin")
    if not log.check(tam is not None, "Tamsin stands near %s" % (TAMSIN,)):
        return False
    for attempt in range(2):
        n, m0 = len(c.gumps), len(c.messages)
        c.dclick(tam)
        g = c.wait_gump(lambda g: any("Tamsin: the Wakening Isle" in (t or "") for t in c.gump_text(g)), timeout=8, since=n)
        pl.drain()
        if g is not None:
            break
        c.sleep(1.5)
    if not log.check(g is not None, "Tamsin's window opens"):
        return False
    texts = [t or "" for t in c.gump_text(g)]
    log("  Tamsin's window: %s" % texts)
    if not log.check(any(TITLES[key] in t for t in texts), "Tamsin's window lists %r" % TITLES[key]):
        return False
    c.reply_gump(g, 100 + CORE.index(key))
    return True


def t_movement(pl, log):
    c = pl.c
    blue = next((s for s, it in c.items.items() if it.get("graphic") == FLOOR and it.get("hue") == BLUE
                 and (it.get("x"), it.get("y")) == BLUE_TILE), None)
    gold = next((s for s, it in c.items.items() if it.get("graphic") == FLOOR and it.get("hue") == GOLD
                 and (it.get("x"), it.get("y")) == GOLD_TILE), None)
    log.check(blue is not None, "the blue floor tile lies at %s" % (BLUE_TILE,))
    log.check(gold is not None, "the gold floor tile lies at %s" % (GOLD_TILE,))
    log.check(pl.go(BLUE_TILE, 0), "walked onto the blue tile")
    log.check(pl.wait_text(r"Now walk onto the glowing gold", 5) is not None, "the System says: now the gold tile")
    log.check(pl.go(GOLD_TILE, 0), "walked onto the gold tile")


def t_backpack(pl, log):
    c = pl.c
    walk_to(pl, log, CAMP, 2, "the camp")
    n = len(c.messages)
    c.dclick(c.serial | 0x80000000)  # cc-P718: open the character window first, as a player double-clicks themselves
    log.check(pl.wait_text(r"That is your character window", 5, since=n) is not None, "the character window counts first")
    pl.open_pack()
    bag = c.wait(lambda: pl.in_pack(0x0E76, SUPPLY), 5)
    if log.check(bag is not None, "a blue practice bag is in the backpack"):
        c.sleep(1.1)
        c.dclick(bag)


def t_paperdoll(pl, log):
    c = pl.c
    walk_to(pl, log, TABLE, 2, "the clothes table")
    cloak = c.wait(lambda: pl.item_at(TABLE, 0x1515, 0) or pl.item_at(TABLE, 0x1516, 0), 5)
    if not log.check(cloak is not None, "the cloak of the Wakening Isle lies on the clothes table"):
        return
    if pl.lift(cloak):
        c.send(P.equip(cloak, 0x14, c.serial))
        log("  -> dragged the cloak from the table onto the paperdoll")


def t_chat(pl, log):
    c = pl.c
    walk_to(pl, log, SIGN, 2, "the signpost")
    c.say("hello there")
    c.sleep(1.5)
    log.check(pl.wait_gump(DONE, 1) is None, "a different line does not finish the chat lesson")
    c.say("I am ready to learn")


def pests_near(pl):
    out = []
    for s, m in list(pl.c.mobiles.items()):
        if "x" in m and near((m["x"], m["y"]), PESTS, 14) and m.get("body") in (0xEE, 0xD7, 0x34) and s != pl.c.serial:
            out.append(s)
    return out


def find_pet(pl):
    c = pl.c
    for s_, m in list(c.mobiles.items()):
        if s_ != c.serial and "x" in m and m.get("body") in (0xD9, 0xC9) and near((m["x"], m["y"]), pl.pos(), 12):
            return s_
    return None


INSIDE_GATE = (6712, 3979)                 # the field's side of the gate


def in_field(xy):
    return 6696 <= xy[0] <= 6712 and 3968 <= xy[1] <= 3982


def open_field_gate(pl, log, stand=None):
    """cc-P718: Wren opens the field gate; if it has swung shut, double-click it (from outside, or from the field)."""
    c = pl.c
    stand = stand or BELOW_WREN
    for spot in FIELD_GATE:
        for gid in GATE_CLOSED:
            g = pl.item_at(spot, gid, 0)
            if g:
                pl.go(stand, 0)
                c.sleep(0.6)
                c.dclick(g)
                log("  -> opened the field gate at %d,%d" % spot)
                c.sleep(0.6)


def farm_pests(pl, log):
    c = pl.c
    walk_to(pl, log, BELOW_WREN, 0, "the field gate")
    open_field_gate(pl, log)
    walk_to(pl, log, PESTS, 3, "the cabbage rows")
    t0 = time.time()
    targets = 0
    while time.time() - t0 < 240 and not c.find_text(r"You cleared the farm pests", since=0):
        ps = pests_near(pl)
        if not ps:
            c.sleep(3.0)
            pl.drain()
            continue
        p = min(ps, key=lambda s_: abs(c.mobiles[s_]["x"] - pl.pos()[0]) + abs(c.mobiles[s_]["y"] - pl.pos()[1]))
        m = c.mobiles[p]
        pl.go((m["x"], m["y"]), 2)
        if targets == 0:
            c.send(P.war_mode(True))
            c.send(P.attack(p))  # cc-P721: the trainee attacks one itself (a double-click in war mode)
            log("  -> attack 0x%08X" % p)
            c.sleep(2.0)
        if not c.pet_command("all kill", settle=1.0):
            log("  'all kill' gave no target cursor")
            c.sleep(2.0)
            continue
        c.target_obj(p)
        targets += 1
        log("  -> all kill on 0x%08X at %d,%d" % (p, m["x"], m["y"]))
        c.wait(lambda: p not in c.mobiles or c.find_text(r"Farm pests defeated|You cleared", since=len(c.messages) - 1), 25)
        pl.drain()
    log.check(c.find_text(r"You cleared the farm pests", since=0) is not None,
              "the pests are cleared (%.0f s, %d targets)" % (time.time() - t0, targets))


def farm_heal(pl, log, scratched):
    c = pl.c
    pl.open_pack()
    band = c.wait(lambda: pl.in_pack(0x0E21), 5)
    if not log.check(band is not None, "bandages are in the backpack"):
        return
    c.send(P.status_request(c.serial, 4))
    pet = find_pet(pl)
    if pet:
        c.send(P.status_request(pet, 4))
    c.sleep(1.0)
    me, pm = c.mobiles.get(c.serial, {}), c.mobiles.get(pet, {}) if pet else {}
    log("  hits: you %s/%s, pet %s/%s" % (me.get("hits"), me.get("hitsMax"), pm.get("hits"), pm.get("hitsMax")))
    # cc-P718: the pet may be guarding in the field ("That is too far away"); after a scratch ("nipped") the bot bandages
    # itself at once, as the line tells a player to, before the scratch regenerates away.
    who = c.serial if scratched or not pet else pet
    pip = pl.mobile_at((6715, 3981), 0)  # cc-P721: the heal step's patient, who stays hurt (Pip, by his spot)
    if pip:
        walk_to(pl, log, (6716, 3981), 1, "Pip, the hurt farm boy")
        who = pip
    for _ in range(4):
        n = len(c.messages)
        c.sleep(1.2)
        c.dclick(band)
        if not c.wait_target(5):
            log("  the bandage gave no target cursor")
            continue
        c.target_obj(who)
        log("  -> bandage on %s" % ("the pet" if who != c.serial else "yourself"))
        said = c.find_text(r"Your bandage restored health|nipped|too far away|not damaged", since=n, timeout=14)
        if c.find_text(r"Your bandage restored health", since=n):
            break
        if said is None:
            c.find_text(r"Your bandage restored health|nipped", since=n, timeout=8)
            if c.find_text(r"Your bandage restored health", since=n):
                break
        who = pip or c.serial
        pl.drain()
    pl.drain()
    log.check(c.find_text(r"Your bandage restored health", since=0) is not None, "a bandage really healed (the farm's heal step)")


def pet_commands(pl, log, since):
    """cc-P718: Wren's pet commands: follow, then guard (speech; the pet's menu sets the same orders)."""
    c = pl.c
    c.pet_command("all follow me")
    log.check(pl.wait_text(r"Your pet follows you", 5, since=since) is not None, "'all follow me' counts")
    c.sleep(1.0)
    c.pet_command("all guard me")
    log.check(pl.wait_text(r"Your pet guards you", 5, since=since) is not None, "'all guard me' counts")
    # cc-P721: hold the pitchfork Wren put in the pack, then war mode (Tab sends the same packet).
    c.sleep(1.0)
    pl.open_pack()
    fork = c.wait(lambda: pl.in_pack(0x0E87) or pl.in_pack(0x0E88), 5)
    # a new character already holds its starting weapon: into the backpack first, as Wren says
    for s_, it in list(c.items.items()):
        if it.get("parent") == c.serial and it.get("layer") in (0x01, 0x02) and s_ != fork and pl.lift(s_):
            c.send(P.drop(s_, 60, 60, 0, c.backpack()))
            log("  -> put the held 0x%04X into the backpack" % it.get("graphic", 0))
            c.sleep(0.8)
    if log.check(fork is not None, "Wren's pitchfork is in the backpack") and pl.lift(fork):
        c.send(P.equip(fork, 0x02, c.serial))
        log("  -> dragged the pitchfork onto the paperdoll's hand")
    log.check(pl.wait_text(r"You hold the pitchfork", 5, since=since) is not None, "holding the pitchfork counts")
    c.sleep(0.8)
    c.send(P.war_mode(True))
    log("  -> war mode on")
    log.check(pl.wait_text(r"You are in war mode", 5, since=since) is not None, "war mode counts, and Wren opens the gate")


def t_farm(pl, log):
    """Wren's three steps, by her own answers: the pet window, the pests line, the bandages line."""
    c = pl.c
    walk_to(pl, log, WREN, 3, "Wren at the farm gate")
    wren = pl.mobile_at(WREN, 2, "Wren")
    if not log.check(wren is not None, "Wren the Farmhand stands at %s" % (WREN,)):
        return
    for _ in range(4):
        if c.find_text(r"You finished the farm lessons|finished the farm", since=0):
            return
        pl.go(WREN, 3)
        n, m0 = len(c.gumps), len(c.messages)
        c.sleep(1.2)
        c.dclick(wren)
        c.wait(lambda: len(c.gumps) > n or any((m.get("name") or "").startswith("Wren") for m in c.messages[m0:]), 6)
        c.sleep(0.8)
        pl.drain()
        g = next((g for g in c.gumps[n:] if any("Choose your farm pet" in (t or "") for t in c.gump_text(g))), None)
        said = " ".join(m["text"] or "" for m in c.messages[m0:] if (m.get("name") or "").startswith("Wren"))
        if g is not None:
            log("  pet window: %s" % [t for t in c.gump_text(g) if t])
            c.reply_gump(g, 1)
            c.sleep(2.0)
            pl.drain()
            log.check(pl.wait_text(r"This pet is yours to keep", 4, since=m0) is not None, "the System says the pet is yours")
            pet_commands(pl, log, m0)
        elif "obeys spoken commands" in said:
            pet_commands(pl, log, m0)
        elif "all kill" in said:
            log.check(True, "Wren explains 'all kill'")
            farm_pests(pl, log)
        elif "bandage" in said.lower():
            scratched = "nipped" in said
            log.check(True, "Wren hands bandages%s" % (" and a scratch to treat" if scratched else ""))
            farm_heal(pl, log, scratched)
        else:
            log("  Wren said: %r" % said)
            return


def t_death(pl, log):
    c = pl.c
    walk_to(pl, log, RAT, 2, "the pale echo rat in the training yard")
    echo = pl.mobile_at(RAT, 2, None)
    if not log.check(echo is not None, "the echo stands at %s" % (RAT,)):
        return
    n = len(c.gumps)
    c.dclick(echo)
    g = c.wait_gump(lambda g: any("Ready" in (t or "") for t in c.gump_text(g)), 6, since=n)
    pl.drain()
    if not log.check(g is not None, "the echo asks before the lesson kills"):
        return
    log("  echo window: %s" % [t for t in c.gump_text(g) if t])
    c.reply_gump(g, 1)
    died = c.wait(lambda: c.body in GHOSTS, 10)
    c.sleep(2.0)
    pl.drain()
    log.check(died is not None, "the character died, a ghost at %s" % (pl.pos(),))
    log.check(near(pl.pos(), SERA, 4), "the ghost is beside Sera (%s), not sent off by Young's teleport" % (pl.pos(),))
    sera = pl.mobile_at(SERA, 2, "Sera")
    n = len(c.gumps)
    if sera:
        c.dclick(sera)
    g = c.wait_gump(lambda g: any("return to life" in (t or "").lower() or "resurrect" in (t or "").lower() for t in c.gump_text(g)), 6, since=n)
    pl.drain()
    if log.check(g is not None, "double-clicking Sera as a ghost offers resurrection"):
        log("  window: %s" % [t for t in c.gump_text(g) if t])
        c.reply_gump(g, 1)
        log.check(c.wait(lambda: c.body not in GHOSTS, 8) is not None, "alive again")


def t_banking(pl, log):
    c = pl.c
    walk_to(pl, log, MERRIN, 2, "Merrin inside the practice bank")
    n = len(c.containers)
    c.say("bank", keywords=(0x0002,))
    box = c.wait(lambda: c.containers[n] if len(c.containers) > n else None, 6)
    pl.drain()
    log.check(box is not None, "saying 'bank' opens the bank box")
    pl.open_pack()
    token = c.wait(lambda: pl.in_pack(0x0EF2, SUPPLY), 5)
    log.check(token is not None, "the blue practice token is in the backpack")
    if token and box and pl.lift(token):
        c.send(P.drop(token, 60, 60, 0, box))
        log("  -> dropped the practice token into the bank box")


def t_league(pl, log):
    c = pl.c
    walk_to(pl, log, ELARA, 2, "Elara Voss inside the lodge")
    elara = pl.mobile_at(ELARA, 2, "Elara")
    if log.check(elara is not None, "Elara Voss stands at %s" % (ELARA,)):
        c.dclick(elara)


def t_loop(pl, log):
    c = pl.c
    walk_to(pl, log, STONES, 2, "the standing stones")
    mk = pl.item_at(STONES, 0x1F14, 2)
    if not log.check(mk is not None, "the blue rune stone lies at %s" % (STONES,)):
        return
    pl.vision_t0 = time.time()
    c.dclick(mk)
    log("  -> double-clicked the rune stone: the vision")


def t_travel(pl, log):
    c = pl.c
    walk_to(pl, log, GATE, 1, "the dock moongate")
    gate = pl.item_at(GATE, 0xF6C, 1)
    if log.check(gate is not None, "the moongate stands at %s" % (GATE,)):
        c.dclick(gate)
        ok = c.wait(lambda: near(pl.pos(), ROOK_EXIT, 1), 8)
        pl.drain()
        log.check(ok is not None, "the moongate took the character to %s, beside Rook" % (pl.pos(),))


TRIALS = {"core.movement": (t_movement, 10), "core.backpack": (t_backpack, 10), "core.paperdoll": (t_paperdoll, 10),
          "core.chat": (t_chat, 10), "core.farm": (t_farm, 20), "core.death": (t_death, 15),
          "core.banking": (t_banking, 10), "core.league": (t_league, 10), "core.loop": (t_loop, 70),
          "core.travel": (t_travel, 10)}


def play_isle(pl, log, times, first="core.movement", stop_at=None):
    c = pl.c
    by_title = {v: k for k, v in TITLES.items()}
    walk_to(pl, log, TAMSIN, 2, "Tamsin")
    since = len(c.gumps)
    if not guide_station(pl, log, first):
        return False
    for _ in range(len(CORE) + 2):
        lesson = c.wait_gump(lambda g: any((t or "") in by_title for t in c.gump_text(g)), 8, since=since)
        pl.drain()
        if lesson is None:
            log("  no lesson page came")
            break
        key = next(by_title[t] for t in c.gump_text(lesson) if (t or "") in by_title)
        log("--- %s" % key)
        if key == stop_at:
            log("  stopping at %s, as asked (--stop-at), at %s" % (key, pl.pos()))
            if key == "core.loop":
                walk_to(pl, log, STONES, 2, "the standing stones")
            return True
        log("  page: %s" % [t for t in c.gump_text(lesson) if t])
        t0 = time.time()
        if any(re.search(DONE, t or "") for t in c.gump_text(lesson)):
            done = lesson
        else:
            act, wait = TRIALS[key]
            since = len(c.gumps)
            act(pl, log)
            done = c.wait_gump(lambda g: any(re.search(DONE, t or "") for t in c.gump_text(g)), wait, since=since)
            pl.drain()
            if not log.check(done is not None, "%s done" % key):
                return False
        times[key] = time.time() - t0
        log("  %s took %.0f s" % (key, times[key]))
        if key == "core.travel":
            break
        since = len(c.gumps)
        c.reply_gump(done, 1)          # "Next lesson / graduate"
        c.sleep(1.0)
    pl.drain()
    return log.check(c.find_text(r"You finished the main lessons", since=0) is not None or near(pl.pos(), ROOK_EXIT, 2),
                     "the isle is done and the character stands beside Rook (%s)" % (pl.pos(),))


def party_packet(sub_, serial):
    """0xBF 0x0006: a party message (pinned IncomingExtendedCommandPackets.PartyMessage): 0x01 add (a target cursor
    follows), 0x08 accept (the leader's serial)."""
    import struct
    return struct.pack(">BHHBI", 0xBF, 10, 0x0006, sub_, serial)


def copies_report(a, tr, cl, log, label):
    from uobot.client import Client
    from uobot import golemcheck as GC
    user, pw = GC.account(a.golem, "admin")
    adm = Client(user, pw, tr, cl, label="admin", test_target=(a.host, a.port))
    chars = adm.login()
    adm.play(chars.index(a.golem) if a.golem in chars else 0)
    pw = None
    lines = [m["text"] for m in adm.command("[Tutorial copies", settle=3.0)]
    adm.close()
    log("  [Tutorial copies (%s):" % label)
    for t in lines:
        log("    %s" % t)
    return lines


def copy_of(lines, name):
    """The copy line that names this occupant ("TheFold 3 ... Iron PartyA ..."), or None."""
    for t in lines:
        if name in (t or ""):
            m = re.search(r"(TheFold \d+|map \d+|copy \d+)", t)
            return m.group(1) if m else t
    return None


def account_client(a, tr, cl, golem, label):
    from uobot.client import Client
    from uobot import golemcheck as GC
    user, pw = GC.account(golem, "player")
    c = Client(user, pw, tr, cl, label=label, test_target=(a.host, a.port))
    return c, c.login()


def rook_window(pl, log):
    c = pl.c
    rook = pl.mobile_at((3500, 2572), 3, "Rook")
    if not rook:
        log("  Rook is not near %s" % (pl.pos(),))
        return None
    n = len(c.gumps)
    c.sleep(1.2)
    c.dclick(rook)
    g = c.wait_gump(lambda g: any("Rook Hallowell" in (t or "") for t in c.gump_text(g)), 8, since=n)
    pl.drain()
    return g


def part_copies(a, tr, cl, grid, log):
    """Two friends pick New Haven, party up on the plaza and both restart the tutorial: one copy. A third trainee picks
    the isle at creation: another copy. All log out; after the hold (clusterf.tutorial.copyHoldMinutes) the copies reset
    and a returning trainee is sent to a fresh copy at their next lesson."""
    log("=== copies: a party of two shares a copy, a third trainee gets another, an empty copy resets")
    made = []
    for golem, name in (("Silver", "Silver PartyA"), ("Gold", "Gold PartyB")):
        c, chars = account_client(a, tr, cl, golem, name.split()[1])
        if name in chars:
            c.play(chars.index(name))
        else:
            c.create(name, stats=(45, 35, 10), skills=((0, 30), (17, 30), (40, 30), (43, 30)), city=1)
        pl = base.Player(c, grid, log)
        c.sleep(2.0)
        pl.drain()
        log("  %s starts at %s" % (name, c.pos[:3]))
        made.append((name, c, pl))
    (na, ca, pa), (nb, cb, pb) = made
    # the party: A adds B (a target cursor), B accepts
    ca.send(party_packet(0x01, 0))
    if log.check(ca.wait_target(6) is not None, "adding a party member gives a target cursor"):
        ca.target_obj(cb.serial)
        cb.sleep(1.5)
        cb.send(party_packet(0x08, ca.serial))
        cb.sleep(1.5)
        pa.drain(); pb.drain()
        log.check(cb.find_text(r"joined the party|You have been added to the party", since=0) is not None
                  or ca.find_text(r"joined the party", since=0) is not None, "Bronze PartyB joined Iron PartyA's party")
    for name, c, pl in made:
        g = rook_window(pl, log)
        texts = [t for t in c.gump_text(g) if t] if g else []
        log("  %s: Rook's window: %s" % (name, texts))
        if log.check(g is not None and any("Restart the tutorial" in t for t in texts), "%s: Rook offers to restart the tutorial" % name):
            c.reply_gump(g, 2)
            c.sleep(3.0)
            pl.drain()
            log.check(near(pl.pos(), BEACH, 4), "%s is on an isle beach (%s)" % (name, pl.pos()))
    lines = copies_report(a, tr, cl, log, "after the party went")
    ka, kb = copy_of(lines, na), copy_of(lines, nb)
    log.check(ka is not None and ka == kb, "the party shares one copy (%s, %s)" % (ka, kb))
    # the third trainee
    cc, chars = account_client(a, tr, cl, "Stone", "Stone")
    nc = "Stone Third"
    if nc in chars:
        cc.play(chars.index(nc))
    else:
        cc.create(nc, stats=(45, 35, 10), skills=((0, 30), (17, 30), (40, 30), (43, 30)), city=0)
    pc_ = base.Player(cc, grid, log)
    cc.sleep(3.0)
    pc_.drain()
    lines = copies_report(a, tr, cl, log, "after the third trainee")
    kc = copy_of(lines, nc)
    log.check(kc is not None and kc != ka, "the third trainee is on another copy (%s, the party's %s)" % (kc, ka))
    # everyone leaves; the hold runs out
    for c in (ca, cb, cc):
        c.close()
    hold = a.hold_minutes
    log("  all three logged out; waiting %d minutes (the hold is %d) and the minute tick" % (hold + 2, hold))
    time.sleep((hold + 2) * 60)
    lines = copies_report(a, tr, cl, log, "after the hold")
    # cc-P707 run 4: a freed copy still names a trainee logged out on it, "(away)" (CopyOf reads LogoutMap); freed is
    # "free" with the generation raised (TutorialCopies.Free), and the trainee's next login takes them to a fresh copy.
    def freed(name):
        line = next((t for t in lines if name in (t or "")), None)
        return line is not None and ": free," in line and not re.search(r"generation 0", line)
    log.check(freed(na) and freed(nc), "the copies were freed after the hold (free, generation raised)")
    ca, chars = account_client(a, tr, cl, "Silver", "PartyA")
    ca.play(chars.index(na))
    pa = base.Player(ca, grid, log)
    ca.sleep(3.0)
    pa.drain()
    log("  %s logs back in at %s" % (na, ca.pos[:3]))
    log.check(near(pa.pos(), BEACH, 4) or near(pa.pos(), TAMSIN, 4), "%s is on a fresh copy at the first lesson (%s)" % (na, pa.pos()))
    copies_report(a, tr, cl, log, "after the return")
    ca.close()


def player_client(a, tr, cl):
    from uobot.client import Client
    from uobot import golemcheck as GC
    user, pw = GC.account(a.account or a.golem, "player")
    pc = Client(user, pw, tr, cl, label="player", test_target=(a.host, a.port))
    chars = pc.login()
    return pc, chars


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=2596)
    ap.add_argument("--out", required=True)
    ap.add_argument("--map", required=True)
    ap.add_argument("--tiledata", required=True)
    ap.add_argument("--bot", default=r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
    ap.add_argument("--golem", default="Iron")
    ap.add_argument("--name", default="Iron Islander")
    ap.add_argument("--skip-name", default="Iron Skipper")
    ap.add_argument("--parts", default="seed,isle,skip")
    ap.add_argument("--from", dest="first", default="core.movement", help="the lesson to start from (resuming)")
    ap.add_argument("--hold-minutes", type=int, default=2, help="the world's clusterf.tutorial.copyHoldMinutes")
    ap.add_argument("--account", default="", help="the Golem whose Player account makes the isle and skip characters")
    ap.add_argument("--stop-at", default=None, help="stop when this lesson's page opens (the shots' trainee)")
    a = ap.parse_args(argv)
    sys.path.insert(0, a.bot)
    global P
    from uobot.client import Client, Cliloc, Transcript
    from uobot import packets as P
    from uobot import golemcheck as GC
    base.P = P
    os.makedirs(a.out, exist_ok=True)
    log = base.Log(os.path.join(a.out, "playlog.txt"))
    tr = Transcript(os.path.join(a.out, "transcript.txt"))
    cl = Cliloc(os.path.join(a.tiledata, "Cliloc.enu"), r"D:\UO\bot-shard\cache")
    parts = a.parts.split(",")
    log("P707 Wakening Isle play-through on %s:%d, parts %s" % (a.host, a.port, parts))
    grid = base.Grid(a.map, a.tiledata, RECT)
    log("walk grid %s: %d standable tiles" % (RECT, sum(1 for v in grid.stand.values() if v is not None)))

    adm = None
    if "seed" in parts:
        user, pw = GC.account(a.golem, "admin")
        adm = Client(user, pw, tr, cl, label="admin", test_target=(a.host, a.port))
        chars = adm.login()
        adm.play(chars.index(a.golem) if a.golem in chars else 0)
        pw = None
    if "seed" in parts:
        log("=== seed (the Admin)")
        for cmd in ("[ClusterFSeedTutorial dryrun", "[ClusterFSeedTutorial", "[ClusterFSeedTutorial", "[Tutorial copies"):
            log("  admin types %s" % cmd)
            for m in adm.command(cmd, settle=4.0):
                log("    %s" % m["text"])

    times = {}
    if "isle" in parts:
        log("=== isle: a fresh character on %s's Player account, Tutorial Island at creation" % a.golem)
        pc, chars = player_client(a, tr, cl)
        log("  the account's characters: %s" % [x for x in chars if x])
        log("  the city list the server sent: %s" % getattr(pc, "cities", "(not parsed)"))
        t_start = time.time()
        if a.name in chars:
            log("  %r already exists: playing it (not fresh)" % a.name)
            pc.play(chars.index(a.name))
        else:
            pc.create(a.name, stats=(45, 35, 10), skills=((0, 30), (17, 30), (40, 30), (43, 30)), city=0)
        pl = base.Player(pc, grid, log)
        pc.sleep(7.0)  # cc-P721: the first arrival lies on the sand for 5 s
        log.check(pc.find_text(r"You wake on cold sand", since=0) is not None, "the System says: you wake on cold sand")
        pl.drain()
        log("  in the world at %s" % (pc.pos[:3],))
        if a.first == "core.movement":
            log.check(near(pl.pos(), BEACH, 3), "the character wakes on the beach %s (at %s)" % (BEACH, pl.pos()))
            log.check(pl.wait_text(r"You wake on a quiet shore", 3, since=0) is not None, "the System says: you wake on a quiet shore")
            log.check(any(x["active"] and near((x["x"], x["y"]), TAMSIN, 1) for x in pc.arrows), "a quest arrow points to Tamsin")
        copies_report(a, tr, cl, log, "after the isle character woke")
        ok = play_isle(pl, log, times, a.first, a.stop_at)
        total = time.time() - t_start
        log("=== the isle took %.0f s (%.1f min); per lesson: %s" % (total, total / 60, {k: round(v) for k, v in times.items()}))
        if ok:
            rook = pl.mobile_at((3631, 2584), 2, "Rook")
            log.check(rook is not None, "Rook stands beside the arrival")
        pc.close()

    if "skip" in parts:
        log("=== skip: a fresh character picks New Haven at creation")
        pc, chars = player_client(a, tr, cl)
        if a.skip_name in chars:
            log("  %r already exists: not fresh, skipped" % a.skip_name)
        else:
            pc.create(a.skip_name, stats=(45, 35, 10), skills=((0, 30), (17, 30), (40, 30), (43, 30)), city=1)
            pl = base.Player(pc, grid, log)
            pc.sleep(3.0)
            pl.drain()
            log.check(near(pl.pos(), HAVEN_START, 2), "the New Haven pick starts on the plaza %s (at %s)" % (HAVEN_START, pc.pos[:3]))
            log.check(pc.find_text(r"wake on a quiet shore", since=0) is None, "and is not sent to the isle")
        pc.close()

    if "copies" in parts:
        part_copies(a, tr, cl, grid, log)

    if adm:
        adm.close()
    log("=== %d failed check(s): %s" % (len(log.fails), log.fails))
    tr.close()
    return 1 if log.fails else 0


if __name__ == "__main__":
    sys.exit(main())
