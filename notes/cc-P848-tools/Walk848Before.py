# cc-P848: the "before" run on P838's release build (sl-modernuo:cc-P838-isle). A fresh trainee walks in at the jail's real door and
# shoots the hall with the housing lesson's stop 2 signpost standing in front of the middle cell's gate, then the staff bot saves the
# world, so the next run (the P848 build on the same world) proves the old sign goes on load.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Stock"
POST = (3469, 2597)
OLD_SIGN = (3474, 2601)
SIGNPOST = 0xA854


def at(x, y):
    return (POST[0] + x, POST[1] + y)


def say(text):
    API.SysMsg("P848: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=1.5, after=2.5):
    API.Pause(settle)
    with open(SIG, "a") as f:
        f.write("SHOT " + name + "\n")
    API.Pause(after)


def close_all():
    for g in API.GetAllGumps():
        try:
            if g.PacketGumpText:
                g.Dispose()
        except Exception:
            pass


_asked = 0


def stage(line, seconds=40):
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


def end():
    with open(CMD, "a") as f:
        f.write("end" + chr(10))
    with open(SIG, "a") as f:
        f.write("END\n")
    API.Stop()


if API.Player.Name != CHARACTER:
    API.SysMsg("P848: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s (before)" % API.Player.Name)
API.Pause(7)
close_all()
API.Pause(1)
close_all()
stage("serial %x" % API.Player.Serial)
try:
    door = at(5, 9)
    stage("go %d %d 10" % (door[0], door[1] + 2))
    API.Pause(3)
    close_all()
    walk([door])
    doors = API.GetItemsOnGround(3, 0x0675 + 2 * 2) or []
    if doors:
        API.UseObject(doors[0].Serial)
        API.Pause(1.5)
    walk([at(5, 7), at(5, 6)])
    API.Pause(1.5)
    close_all()
    old = [i for i in (API.GetItemsOnGround(10, SIGNPOST) or []) if i.X == OLD_SIGN[0] and i.Y == OLD_SIGN[1]]
    say("BEFORE signposts at %d,%d: %d" % (OLD_SIGN[0], OLD_SIGN[1], len(old)))
    shot("before-hall-signpost")
    walk([at(4, 5)])
    shot("before-hall-by-the-cells")
    walk([at(5, 7)])
    stage("save", 60)
    API.Pause(3)
    say("saved")
except Exception as e:
    say("FAIL script: %s" % e)
end()
