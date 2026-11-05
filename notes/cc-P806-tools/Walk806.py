# cc-P806: the P805 review's fixes in TazUO, private proof shard, release image, on a world P799's image seeded and saved (the upgrade).
# A new character: Rook on his joined bench, facing the yard; the bard lesson played in the theater, both echoes in view with the
# gump closed; each of the four signs single-clicked; the bucket from inside the stall; on foot: the housing lesson's stops, the
# stables sign, the mine sign, there and back. "SHOT <name>" in SIG asks tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Stock"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
PLAZA = (3503, 2574, 14)
SIGN = 0xA854
LUTE = (0x0EB3, 0x0EB4)
ECHO_A, ECHO_B = (3412, 2604), (3413, 2603)


def say(text):
    API.SysMsg("P806: " + text)
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
    """On foot, logging each leg's end and Z."""
    for (x, y) in points:
        for _ in range(3):
            API.Pathfind(x, y, distance=1, wait=True, timeout=30)
            if abs(API.Player.X - x) <= 2 and abs(API.Player.Y - y) <= 2:
                break
            API.Pause(1)
        say("walked to %d,%d,%d (wanted %d,%d)" % (API.Player.X, API.Player.Y, API.Player.Z, x, y))


def near(x, y, r=2):
    return abs(API.Player.X - x) <= r and abs(API.Player.Y - y) <= r


def echoes():
    found = []
    for m in API.GetAllMobiles(0x190, 14):
        if "echo" in (m.Name or ""):
            found.append(m)
    return found


def journal(seconds=14):
    try:
        for e in API.GetJournalEntries(seconds) or []:
            say("  j: %s" % e.Text)
    except Exception as ex:
        say("  journal: %s" % ex)


def play(skill, targets):
    """One use of a bard skill: the instrument if asked (the skill goes on by itself after it), then each target."""
    API.ClearJournal()
    API.UseSkill(skill)
    picked = False
    queue = list(targets)
    for _ in range(len(targets) + 2):
        if not API.WaitForTarget("any", 3):
            break
        if not picked and API.InJournal("What instrument"):
            lute = None
            for g in LUTE:
                lute = lute or API.FindType(g, API.Backpack)
            say("lute %s" % (lute.Serial if lute else None))
            API.Target(lute.Serial)
            picked = True
        elif queue:
            API.Target(queue.pop(0))
        API.Pause(0.8)
    API.Pause(3)


def read_sign(x, y, text, name):
    """Stand south of the sign, single-click it, shoot the name over it."""
    close_all()
    API.ClearJournal()
    found = None
    for i in API.GetItemsOnGround(6, SIGN) or []:
        if i.X == x and i.Y == y:
            found = i
    if not check(found is not None, "sign at %d,%d is there" % (x, y)):
        return
    API.ClickObject(found.Serial)
    API.Pause(1)
    check(API.InJournal(text), "single click reads '%s'" % text)
    shot(name, 0.2, 1.5)


if API.Player.Name != CHARACTER:
    API.SysMsg("P806: not %s, nothing to do" % CHARACTER)
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
# not blessed: pinned refuses a blessed mobile any harmful act, so the bard skills all say "You cannot calm that!"
API.ClearJournal()

try:
    # 1, 2. Rook on the joined bench, from the yard, in front of him and from the south-west.
    go(3502, 2532, 22)
    say("in the yard at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
    shot("1-rook-from-the-moongate-exit")
    go(3500, 2532, 22)
    shot("1-rook-bench")
    stage("rookdir")

    # 3. The bard lesson on the floor of the theater, played with the real skills.
    go(3414, 2602, 55)
    station("bard.trial")
    API.Pause(2)
    close_all()
    API.Pause(1)
    close_all()
    e = echoes()
    check(len(e) == 2, "two echoes in sight, %d" % len(e))
    for m in e:
        say("echo %s at %d,%d,%d" % (m.Name, m.X, m.Y, m.Z))
    shot("3-theater-both-echoes-gump-closed")
    if len(e) == 2:
        a, b = e[0].Serial, e[1].Serial
        def lesson(skill, targets, words, name):
            for attempt in range(8):
                play(skill, targets)
                ok = API.InJournalAny(words)
                journal()
                if ok:
                    return check(True, name)
                API.Pause(7)
            return check(False, name)

        lesson("Peacemaking", [a], ["You play your hypnotic music"], "Peacemaking on an echo")
        close_all()
        API.Pause(8)
        brawl = lesson("Provocation", [a, b], ["Provocation worked"], "Provocation sets the echoes fighting")
        close_all()
        with open(SIG, "a") as f:
            f.write("BURST 3-brawl 6 1000\n")
        API.Pause(7)
        API.Pause(9)
        check(API.InJournal("stop fighting") or API.InJournal("catch their breath"), "the brawl ended by itself")
        lesson("Discordance", [a], ["You play jarring music", "finished"], "Discordance on an echo")
        API.Pause(2)
        journal(10)
    say("journal bard: lesson done=%s" % API.InJournal("finished"))
    shot("3-bard-lesson-done")
    close_all()

    # 7. Each sign read, by its road; 4. the stables on foot from the square.
    go(*PLAZA)
    walk([(3519, 2572), (3520, 2570)])
    read_sign(3520, 2568, "The stables", "4-stables-sign-read")
    close_all()
    walk([(3519, 2573)])
    shot("4-stables-sign-from-the-street")
    walk([(3522, 2577), (3534, 2577)])
    check(near(3534, 2577), "walked in by the stables' door to the aisle")
    # the bucket, from inside the stall, nothing open
    close_all()
    go(3534, 2575, 7)
    close_all()
    for i in API.GetItemsOnGround(4, 0x0FFA) or []:
        say("bucket at %d,%d,%d" % (i.X, i.Y, i.Z))
    check(bool(API.GetItemsOnGround(4, 0x0FFA)), "the bucket is in the stall")
    shot("7-bucket-from-the-stall")
    walk([(3522, 2577), (3519, 2573)])
    check(near(3519, 2573), "walked back out")

    # 6. The housing lesson on foot: stop 1 beside the sign on the street, stop 2 on the lawn.
    go(*PLAZA)
    station("housing.basics")
    API.Pause(1)
    close_all()
    API.ClearJournal()
    walk([(3488, 2589), (3468, 2592)])
    API.Pause(3)
    check(API.InJournal("Stop 1 of 3"), "stop 1 comes up by its sign")
    read_sign(3469, 2589, "Housing lesson, stop 1", "6-stop1-sign-read")
    close_all()
    shot("6-stop1-from-the-street")
    API.ClearJournal()
    walk([(3474, 2604)])
    API.Pause(3)
    check(API.InJournal("Stop 2 of 3"), "stop 2 comes up on the lawn")
    read_sign(3474, 2601, "Housing lesson, stop 2", "6-stop2-sign-read")
    close_all()

    # 5. The mine sign: down the road from the gate, to its road, and back.
    go(3481, 2616, 10)
    shot("5-mine-sign-from-the-gate")
    walk([(3476, 2622), (3470, 2628)])
    check(near(3470, 2628), "walked down from the gate to the road by the sign")
    walk([(3469, 2626)])
    read_sign(3469, 2624, "To the mine", "5-mine-sign-read")
    close_all()
    walk([(3470, 2628), (3476, 2622), (3481, 2617)])
    check(near(3481, 2617), "walked back to the gate")
    say("done")
except Exception as e:
    say("FAIL the script stopped: %s" % e)
with open(CMD, "a") as f:
    f.write("end" + chr(10))
with open(SIG, "a") as f:
    f.write("END\n")
API.Stop()
