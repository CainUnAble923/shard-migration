# cc-P799: New Haven on the stock town in TazUO, private proof shard, the release image. A new character does what Chase asked for:
# a ghost walks up to the League ankh; the music lesson in the theater; the walk from the square to the mine, on foot, and the
# dig; the Animals lesson at the stables (bandage, then tame). Short shots of the other places. "SHOT <name>" in SIG asks
# tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Stock"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
PLAZA = (3503, 2574, 14)
TO_MINE = [(3488, 2589), (3487, 2607), (3488, 2625), (3479, 2643), (3477, 2661), (3479, 2679), (3491, 2697), (3497, 2715),
           (3499, 2733), (3513, 2747), (3514, 2747)]
PICK, BANDAGE = 0x0E86, 0x0E21
HORSES = (0xC8, 0xCC, 0xE2, 0xE4)


def say(text):
    API.SysMsg("P799: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=1.5, after=2.5):
    API.Pause(settle)
    with open(SIG, "a") as f:
        f.write("SHOT " + name + "\n")
    API.Pause(after)


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    return ok


def close_all():
    for g in API.GetAllGumps():
        try:
            if g.PacketGumpText:
                g.Dispose()
        except Exception:
            pass


def wait_journal(text, seconds):
    for _ in range(int(seconds * 2)):
        if API.InJournal(text):
            return True
        API.Pause(0.5)
    return False


_asked = 0


def stage(line, seconds=25):
    """Staff hands: stage799.py does it and answers with the request's number."""
    global _asked
    _asked += 1
    with open(CMD, "a") as f:
        f.write(line + chr(10))
    for _ in range(seconds * 2):
        with open(ACK) as f:
            if str(_asked) in f.read().split():
                return True
        API.Pause(0.5)
    say("FAIL no answer to " + line)
    return False


def go(x, y, z):
    stage("go %d %d %d" % (x, y, z))
    API.Pause(3)
    close_all()


def station(key):
    API.ClearJournal()
    stage("station " + key)
    API.Pause(2)


def walk(points):
    for (x, y) in points:
        for _ in range(3):
            API.Pathfind(x, y, distance=1, wait=True, timeout=30)
            if abs(API.Player.X - x) <= 2 and abs(API.Player.Y - y) <= 2:
                break
            API.Pause(1)
        say("walked to %d,%d (wanted %d,%d)" % (API.Player.X, API.Player.Y, x, y))


def horse():
    for body in HORSES:
        found = API.GetAllMobiles(body, 8)
        if found:
            return found[0]
    return None


def end():
    with open(CMD, "a") as f:
        f.write("end" + chr(10))
    with open(SIG, "a") as f:
        f.write("END\n")
    API.Stop()


if API.Player.Name != CHARACTER:
    API.SysMsg("P799: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)
API.Pause(7)
close_all()
API.Pause(1)
close_all()
for d in ("East", "East"):
    API.Walk(d)
    API.Pause(1)
stage("serial %x" % API.Player.Serial)
API.ClearJournal()

try:
    # 1. The ankh: a ghost walks up to it and takes the offer.
    go(3468, 2600, 27)
    say("by the ankh at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
    shot("1-ankh-alive")
    stage("young False")  # a young ghost is moved away by pinned (PlayerMobile), which is not what this shows
    stage("kill")
    API.Pause(3)
    check(API.Player.IsDead, "the character is a ghost")
    API.Pathfind(3465, 2600, distance=0, wait=True, timeout=15)
    API.Pause(2)
    say("ghost at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
    shot("1-ankh-ghost-offer", 0.5)
    for g in API.GetAllGumps():
        try:
            API.ReplyGump(1, g.ServerSerial)
        except Exception as e:
            say("gump reply: %s" % e)
    API.Pause(3)
    check(not API.Player.IsDead, "the ankh resurrected the ghost")
    shot("1-ankh-alive-again")
    stage("blessed True")

    # 2. The music lesson, in the theater.
    go(3414, 2602, 55)
    station("bard.trial")
    API.Pause(2)
    close_all()
    API.Pause(1)
    shot("2-theater-echoes-on-stage")
    API.Pause(1)

    # 3. The mining lesson: from the square, on foot.
    go(*PLAZA)
    station("gathering.mining")
    shot("3-mining-told-where")
    walk(TO_MINE)
    check(abs(API.Player.X - 3514) <= 3 and abs(API.Player.Y - 2747) <= 3, "walked from the square to the mine")
    API.Pause(2)
    shot("3-mine-arrival")
    pick = API.FindType(PICK, API.Backpack)
    check(pick is not None, "the lesson lent a pickaxe at the mine")
    got = False
    if pick is not None:
        for attempt in range(12):
            API.ClearJournal()
            API.UseObject(pick.Serial)
            if API.WaitForTarget("any", 4):
                API.Target(3514, 2746, 0)
            API.Pause(3.5)
            if API.InJournal("You dig some") or API.InJournal("Lesson finished") or API.InJournal("finished"):
                got = True
                break
    check(got, "digging the rock wall by the mine works")
    shot("3-mine-dug")
    API.Pause(1)

    # 4. Animals, at the stables, from the square.
    go(*PLAZA)
    station("animals.taming")
    shot("4-animals-told-where")
    walk([(3520, 2575), (3534, 2577)])
    API.Pause(3)
    shot("4-stables-arrival")
    h = horse()
    check(h is not None, "an injured horse waits in the stall")
    bandage = API.FindType(BANDAGE, API.Backpack)
    check(bandage is not None, "the lesson has bandages")
    if h is not None and bandage is not None:
        healed = False
        for attempt in range(6):
            API.ClearJournal()
            API.UseObject(bandage.Serial)
            if API.WaitForTarget("any", 4):
                API.Target(h.Serial)
            API.Pause(7)
            if API.InJournal("tame") or API.InJournal("healed") or API.InJournal("Taming"):
                healed = True
                break
        check(healed, "bandaging the horse moves the lesson on")
        shot("4-horse-healed")
        tamed = False
        for attempt in range(5):
            API.ClearJournal()
            API.UseSkill("Animal Taming")
            if API.WaitForTarget("any", 5):
                API.Target(h.Serial)
            if attempt == 0:
                shot("4-taming-started", 1.0, 0.5)
            if wait_journal("accept you as master", 16):
                tamed = True
                break
            for text in ("can't tame", "too far", "no chance", "cannot be tamed", "too many followers", "fail to tame", "must wait", "start to tame", "not tamable", "master", "Target cannot", "see", "angry", "already", "can not", "cannot"):
                if API.InJournal(text):
                    say("journal has: " + text)
            near = API.FindMobile(h.Serial)
            say("horse %s at %s, me %d,%d,%d" % (near.Name if near else None, (near.X, near.Y, near.Z) if near else None, API.Player.X, API.Player.Y, API.Player.Z))
            API.Pause(2)
        check(tamed, "taming the horse works")
        shot("4-horse-tamed")
    # The other places.
    API.Pause(1)
    for name, spot in (("5-rook-bench", (3504, 2533, 22)), ("5-warrior-yard", (3529, 2544, 20)), ("5-magery-school", (3486, 2501, 52)),
                       ("5-mine-sign", (3477, 2619, 10)), ("5-stables-sign", (3519, 2575, 5)), ("5-housing-signs", (3469, 2600, 11))):
        go(*spot)
        shot(name)
    say("done")
except Exception as e:
    say("FAIL the script stopped: %s" % e)
end()
