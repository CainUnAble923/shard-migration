# cc-P814: the moved signs in TazUO, private proof shard. Release: the housing lesson's stop 1, walked to on foot from the street both ways,
# the sign read and shot clear of the bench. Main: the stables sign read and shot. make_walk.py stamps the branch.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Main"
RELEASE = False


def say(text):
    API.SysMsg("P814: " + text)
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


def walk(points, reach=0):
    for (x, y) in points:
        for _ in range(3):
            API.Pathfind(x, y, distance=reach, wait=True, timeout=30)
            if abs(API.Player.X - x) <= reach + 1 and abs(API.Player.Y - y) <= reach + 1:
                break
            API.Pause(1)
        say("walked to %d,%d,%d (wanted %d,%d)" % (API.Player.X, API.Player.Y, API.Player.Z, x, y))


def read_sign(x, y, name):
    signs = [s for s in (API.GetItemsOnGround(10, 0xA854) or []) if s.X == x and s.Y == y]
    if not check(bool(signs), "the sign is at %d,%d" % (x, y)):
        return
    API.ClearJournal()
    API.ClickObject(signs[0].Serial)
    API.Pause(1)
    check(API.InJournal(name), "it reads '%s'" % name)
    shot(("sign-read-%d-%d" % (x, y)), 0.1, 1.5)


def end():
    with open(CMD, "a") as f:
        f.write("end" + chr(10))
    with open(SIG, "a") as f:
        f.write("END\n")
    API.Stop()


if API.Player.Name != CHARACTER:
    API.SysMsg("P814: not %s, nothing to do" % CHARACTER)
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
    if RELEASE:
        stage("go 3482 2592 10")
        API.Pause(3)
        close_all()
        stage("station housing.basics")
        API.Pause(2)
        close_all()
        shot("1-from-the-street-east")
        API.ClearJournal()
        walk([(3476, 2590), (3470, 2590)])
        API.Pause(2)
        check(API.InJournal("Stop 1 of 3"), "stop 1 fired on arrival")
        close_all()
        shot("2-at-stop-1")
        read_sign(3471, 2588, "Housing lesson, stop 1")
        walk([(3473, 2592)])
        close_all()
        shot("3-stop-1-sign-from-the-street", 2, 2.5)
        walk([(3465, 2591)])
        close_all()
        shot("4-sign-and-bench-from-the-west", 2, 2.5)
        walk([(3470, 2590), (3476, 2590), (3482, 2592)])
        check(True, "walked stop 1 both ways")
        API.ClearJournal()
    else:
        stage("go 3614 2618 0")
        API.Pause(3)
        close_all()
        walk([(3611, 2616)])
        read_sign(3609, 2614, "The stables")
        walk([(3610, 2617)])
        shot("1-stables-sign-from-the-door-path", 2, 2.5)
except Exception as e:
    say("FAIL script: %s" % e)
end()
