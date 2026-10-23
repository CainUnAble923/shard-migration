"""cc-P290: a real run of each wing trial (combat, healing, magic) on a PRIVATE test shard, through the play-test bot's
client (tools/playtest-bot/uobot: the packets a real client sends). Every step is a player action the server checks:
the core is played first (since P480 Rook shows the wings only after it, with playkit's play_core), then each trial is
started from Rook's page, the character walks to the training yard, and then fights, bandages, casts or strikes. No staff command completes anything; the Admin only seeds the tutorial ([ClusterFSeedTutorial).

    python -P wingtrials.py --port 2596 --out <folder> --map <overlay folder> --tiledata <client folder> [--name "Iron Wings"]

Writes <out>/playlog.txt (the evidence) and <out>/transcript.txt. Helpers: playkit.py (cc-P480's driver, unchanged).
Passwords from D:\\UO\\golem\\Get-GolemTestAccount.ps1, never written. Test ports only. ASCII only.
"""
import argparse, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import playkit as K  # noqa: E402

ROOK = (3500, 2572)
YARD, ECHO, VILLAGER = (3411, 2617), (3413, 2617), (3409, 2617)
# TutorialStations.All order on this branch: the nine core stations, then the wings (Rook's button = 100 + index)
ALL_INDEX = {"combat.weapons": 9, "combat.healing": 10, "magic.magery": 11, "magic.necromancy": 12,
             "magic.chivalry": 13, "magic.bushido": 14, "magic.ninjitsu": 15, "magic.mysticism": 16}
DONE = r": done\. The yard has its loans back"
P = None


def start_trial(pl, log, key):
    c = pl.c
    log("--- %s" % key)
    pl.go(ROOK, 2)
    g = K.recruiter_station(pl, None)
    if not log.check(g is not None, "%s: Rook's page opens" % key):
        return False
    m0 = len(c.messages)
    pl.trial_g0 = len(c.gumps)
    c.reply_gump(g, 100 + ALL_INDEX[key])
    log.check(c.find_text(r"training yard", since=m0, timeout=4) is not None, "%s: the page points to the training yard" % key)
    pl.go(YARD, 1)
    armed = c.find_text(r"The yard's loans are yours", since=m0, timeout=6)
    return log.check(armed is not None, "%s: at the yard the lesson starts (loans given)" % key)


def loaners(pl):
    c = pl.c
    out = []
    for s, it in list(c.items.items()):
        if it.get("container") == c.backpack() or it.get("parent") == c.serial:
            props = c.opl(s) or []
            if any("tutorial loaner" in (p or "").lower() for p in props):
                out.append(s)
    return out


def finished(pl, log, key, m0, timeout):
    c = pl.c
    done = c.find_text(DONE, since=m0, timeout=timeout)
    return done is not None


def check_returned(pl, log, key, lent):
    c = pl.c
    c.sleep(1.0)
    pl.drain()
    left = [s for s in lent if s in c.items]
    log.check(not left, "%s: every loaner went back (%d lent, %d left)" % (key, len(lent), len(left)))


def t_weapons(pl, log):
    c = pl.c
    g = pl.wait_gump(r"Swords: a longsword", 6, since=pl.trial_g0)
    if not log.check(g is not None, "combat.weapons: the page offers the six weapons"):
        return []
    m0 = len(c.messages)
    c.reply_gump(g, 10)  # Swords
    c.sleep(0.5)
    lent = loaners(pl)
    log("  loaners: %s" % [(" | ".join(c.opl(s) or [])) for s in lent])
    echo = pl.mobile_at(YARD, 8, "sparring echo")
    if echo is None and c.find_text(DONE, since=m0) is not None:
        log.check(True, "combat.weapons: the sparring echo came to the trainee, who struck back with the loaned sword")
    if not log.check(echo is not None or c.find_text(DONE, since=m0) is not None, "combat.weapons: a sparring echo stands in the yard"):
        return lent
    if echo is None:
        log.check(c.find_text(r"Hit 2 of 3", since=m0) is not None, "combat.weapons: three hits with the longsword finish it")
        return lent
    noto = pl.c.mobiles.get(echo, {}).get("notoriety")
    # gray: 3 (can be attacked), or 4 (criminal) once it has swung at the trainee; striking either is no crime
    log.check(noto in (3, 4), "%s: the echo is gray to its trainee (notoriety %s)" % ("combat.weapons", noto))
    c.send(P.war_mode(True))
    c.sleep(0.5)
    c.send(P.attack(echo))
    for _ in range(12):
        if finished(pl, log, "combat.weapons", m0, 5):
            break
        pl.go((echo_pos(pl, echo)), 1)
        c.send(P.attack(echo))
    log.check(c.find_text(DONE, since=m0) is not None, "combat.weapons: three hits with the longsword finish it")
    c.send(P.war_mode(False))
    return lent


def echo_pos(pl, serial):
    m = pl.c.mobiles.get(serial, {})
    return (m.get("x", ECHO[0]), m.get("y", ECHO[1]))


def bandage(pl, target):
    c = pl.c
    bag = next((s for s, it in c.items.items() if it.get("container") == c.backpack() and it.get("graphic") == 0x0E21), None)
    if bag is None:
        return False
    c.dclick(bag)
    if c.wait_target(5):
        c.target_obj(target)
        return True
    return False


def t_healing(pl, log):
    c = pl.c
    c.sleep(1.0)
    lent = loaners(pl)
    log("  loaners: %s" % [(" | ".join(c.opl(s) or [])) for s in lent])
    villager = pl.mobile_at(VILLAGER, 2, "villager")
    log.check(villager is not None, "combat.healing: a wounded villager stands in the yard")
    m0 = len(c.messages)
    for i in range(5):
        bandage(pl, c.serial)
        if c.find_text(r"Now the wounded villager|" + DONE, since=m0, timeout=14):
            break
    log.check(c.find_text(r"Now the wounded villager", since=m0) is not None, "combat.healing: a bandage on yourself counts")
    for i in range(5):
        if villager:
            pl.go(VILLAGER, 1)
            bandage(pl, villager)
        if finished(pl, log, "combat.healing", m0, 12):
            break
    log.check(c.find_text(DONE, since=m0) is not None, "combat.healing: then the villager: done")
    return lent


def t_spell(pl, log, key, spell_id, at):
    c = pl.c
    c.sleep(1.0)
    lent = loaners(pl)
    log("  loaners: %s" % [(" | ".join(c.opl(s) or [])) for s in lent])
    target = pl.mobile_at(at, 2, "villager" if at == VILLAGER else "echo")
    if not log.check(target is not None, "%s: the trial's %s stands in the yard" % (key, "villager" if at == VILLAGER else "training echo")):
        return lent
    if at != VILLAGER:
        noto = pl.c.mobiles.get(target, {}).get("notoriety")
        log.check(noto == 3, "%s: the echo is gray to its trainee (notoriety %s)" % (key, noto))
    m0 = len(c.messages)
    if at == VILLAGER:
        pl.go(VILLAGER, 1)
    for i in range(8):
        c.send(P.cast_spell(spell_id + 1))
        if c.wait_target(8):
            c.target_obj(target)
        if finished(pl, log, key, m0, 5):
            break
    log.check(c.find_text(DONE, since=m0) is not None, "%s: a cast at the %s finishes it" % (key, "villager" if at == VILLAGER else "echo"))
    return lent


def t_move(pl, log, key, move_id):
    c = pl.c
    c.sleep(1.0)
    lent = loaners(pl)
    log("  loaners: %s" % [(" | ".join(c.opl(s) or [])) for s in lent])
    echo = pl.mobile_at(ECHO, 2, "echo")
    if not log.check(echo is not None, "%s: a training echo stands in the yard" % key):
        return lent
    m0 = len(c.messages)
    c.send(P.war_mode(True))
    for i in range(8):
        c.send(P.cast_spell(move_id + 1))   # readies the move (Spellbook.CastSpellRequest -> SpecialMove)
        c.sleep(0.6)
        pl.go(echo_pos(pl, echo), 1)
        c.send(P.attack(echo))
        if finished(pl, log, key, m0, 6):
            break
    log.check(c.find_text(DONE, since=m0) is not None, "%s: a hit with the move readied finishes it" % key)
    c.send(P.war_mode(False))
    return lent


def t_leave(pl, log):
    c = pl.c
    if not start_trial(pl, log, "magic.magery"):
        return
    c.sleep(1.0)
    lent = loaners(pl)
    m0 = len(c.messages)
    pl.go((YARD[0] + 18, YARD[1]), 2)
    log.check(c.find_text(r"You left the training yard", since=m0, timeout=6) is not None, "leaving the yard stops the lesson")
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
    ap.add_argument("--name", default="Iron Wings")
    ap.add_argument("--only", default="")
    a = ap.parse_args(argv)
    sys.path.insert(0, a.bot)
    global P
    from uobot.client import Client, Cliloc, Transcript
    from uobot import packets
    from uobot import golemcheck as GC
    P = K.P = packets
    os.makedirs(a.out, exist_ok=True)
    log = K.Log(os.path.join(a.out, "playlog.txt"))
    tr = Transcript(os.path.join(a.out, "transcript.txt"))
    cl = Cliloc(os.path.join(a.tiledata, "Cliloc.enu"), r"D:\UO\bot-shard\cache")
    log("P290 wing trials on %s:%d" % (a.host, a.port))
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
    log.check(pl.wait_text(r"League recruiter, is waiting", 2, since=0) is not None, "first login: the character is in the tutorial")
    if not K.play_core(pl, log, "core"):
        log("=== the core did not finish; the wings stay closed")

    plan = [("combat.weapons", lambda: t_weapons(pl, log)),
            ("combat.healing", lambda: t_healing(pl, log)),
            ("magic.magery", lambda: t_spell(pl, log, "magic.magery", 4, ECHO)),
            ("magic.necromancy", lambda: t_spell(pl, log, "magic.necromancy", 108, ECHO)),
            ("magic.chivalry", lambda: t_spell(pl, log, "magic.chivalry", 201, VILLAGER)),
            ("magic.bushido", lambda: t_move(pl, log, "magic.bushido", 400)),
            ("magic.ninjitsu", lambda: t_move(pl, log, "magic.ninjitsu", 500)),
            ("magic.mysticism", lambda: t_spell(pl, log, "magic.mysticism", 682, ECHO))]
    for key, act in plan:
        if a.only and key not in a.only.split(","):
            continue
        if start_trial(pl, log, key):
            lent = act()
            check_returned(pl, log, key, lent)
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
