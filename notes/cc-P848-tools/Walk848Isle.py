# cc-P848 (P842's review of P838): on the release's stock New Haven, a fresh Player-account trainee takes the housing lesson from
# Rook's station, walks on foot to stop 1 and then to stop 2 (now on the lawn south of the town wall, not in the jail), reads stop 2's
# signpost, then walks back through the town-wall gate and in at the jail's real door to shoot the hall: no signpost by the cells.
# "SHOT <name>" in SIG asks tazuo-walk.ps1 for a shot. Private proof shard only.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Lawn"
POST = (3469, 2597)          # the jail's north-west post (HavenSpots.JailPost)
START = (3501, 2572, 14)
STOP1 = (3470, 2590)
STOP2 = (3482, 2623)
SIGN2 = (3481, 2622)
OLD_SIGN = (3474, 2601)
TO_STOP1 = [(3486, 2580), (3471, 2591)]
TO_STOP2 = [(3467, 2600), (3468, 2609), (3472, 2614), (3474, 2619), (3482, 2623)]
BACK = [(3474, 2619), (3472, 2611), (3474, 2607)]
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


def window_text():
    out = ""
    for g in API.GetAllGumps():
        try:
            out += (g.PacketGumpText or "") + "\n"
        except Exception:
            pass
    return out


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


def walk(points, reach=1):
    for (x, y) in points:
        for _ in range(3):
            API.Pathfind(x, y, distance=reach, wait=True, timeout=30)
            if abs(API.Player.X - x) <= reach + 1 and abs(API.Player.Y - y) <= reach + 1:
                break
            API.Pause(1)
        say("walked to %d,%d,%d (wanted %d,%d)" % (API.Player.X, API.Player.Y, API.Player.Z, x, y))


def signs_at(x, y):
    return [i for i in (API.GetItemsOnGround(24, SIGNPOST) or []) if i.X == x and i.Y == y]


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
    # run 1: on P838's saved world the new character's account had no active tutorial ("You do not have an active tutorial").
    # run 2: the staff bot targets the trainee, so it must be in view first (go), and enter sends to the isle (go again).
    stage("go %d %d %d" % START)
    API.Pause(3)
    stage("tut reset")
    stage("tut enter")
    API.Pause(4)
    close_all()
    stage("go %d %d %d" % START)
    API.Pause(3)
    close_all()
    stage("station housing.basics")
    API.Pause(3)
    shot("0-housing-lesson-told-where")
    close_all()
    API.ClearJournal()
    walk(TO_STOP1)
    API.Pause(2)
    check(API.InJournal("You reached stop 1"), "reached housing stop 1 at %d,%d" % (API.Player.X, API.Player.Y))
    check("open lawn outside the town wall" in window_text(), "stop 1's text sends the trainee to the lawn outside the town wall")
    shot("1-stop1-window")
    close_all()
    API.ClearJournal()
    # On foot to stop 2: down the garden west of the jail, through the yard and the town-wall gate, east off the road.
    walk(TO_STOP2, 0)
    API.Pause(2)
    check(API.InJournal("You reached stop 2"), "reached housing stop 2 at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
    check("Stop 2 of 3" in window_text(), "the window shows stop 2's lesson")
    shot("2-stop2-window")
    close_all()
    new = signs_at(*SIGN2)
    check(len(new) == 1, "stop 2's signpost stands at %d,%d beside the stop" % SIGN2)
    if new:
        API.ClickObject(new[0].Serial)
        API.Pause(1.5)
        check(API.InJournal("stop 2"), "clicking the signpost reads its name")
    shot("2b-stop2-sign-on-the-lawn", 0.3, 2.0)
    # Back through the gate to the jail's door, and in.
    walk(BACK)
    shot("3-jail-from-the-yard")
    walk([at(5, 9)], 0)
    doors = API.GetItemsOnGround(3, 0x0675 + 2 * 2) or []
    say("doors seen %d" % len(doors))
    if doors:
        API.UseObject(doors[0].Serial)
        API.Pause(1.5)
    walk([at(5, 7)], 0)
    walk([at(5, 6)], 0)
    API.Pause(1.5)
    close_all()
    check(API.Player.Y == POST[1] + 6, "inside the jail hall at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
    check(not signs_at(*OLD_SIGN), "no signpost at %d,%d in front of the middle cell's gate" % OLD_SIGN)
    inside = [i for i in (API.GetItemsOnGround(10, SIGNPOST) or [])
              if POST[0] <= i.X <= POST[0] + 10 and POST[1] <= i.Y <= POST[1] + 8]
    check(not inside, "no signpost anywhere in the jail (%d)" % len(inside))
    shot("4-hall-no-signpost")
    walk([at(5, 4)], 0)
    shot("4b-hall-by-the-cells")
except Exception as e:
    say("FAIL script: %s" % e)
end()
