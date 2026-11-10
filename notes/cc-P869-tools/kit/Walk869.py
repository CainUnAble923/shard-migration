# cc-P869 (P856's Walk856.py, fix-up of the build review P865): New Haven's winter set in TazUO on the private proof
# shard, at its moved spots. A Player-account trainee; staff hands through stage856.py (the CMD/ACK file channel): the
# winter decor put up by staff ([ClusterFWinterDecor place, as on December 1). Then for each piece the trainee is set
# down beside the middle of its west or north side (P865 item 5: so the camera, centred on the trainee, frames the
# whole piece), a part of the piece is looked for, the camera takes it, and the trainee walks 4 tiles along that side
# and back with the client's own walk (API.Walk, no teleport), each step's position and z logged.
# RELEASE picks the town: True the ML plaza (release branch), False the SoS New Haven (main).
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Winter"
RELEASE = False
PHASE = "p869-release" if RELEASE else "p869-main"

# (shot name, where the trainee stands, the walk out and back, a part of the piece the check looks for);
# spots.py chose them (standable, reached, within 2 of the piece's base, the leg's tiles standable and free)
if RELEASE:
    SPOTS = [("train", (3433, 2614, 45), ("North", "South"), 0x1B73),
             ("snowman-bench", (3501, 2596, 1), ("North", "South"), 0x9E1B),
             ("santa-bench", (3505, 2588, 16), ("West", "East"), 0x4A99),
             ("snow-globe", (3522, 2591, 1), ("North", "South"), 0x17CD)]
else:
    SPOTS = [("train", (3649, 2595, 0), ("North", "South"), 0x1B73),
             ("snowman-bench", (3643, 2600, 0), ("North", "South"), 0x9E1B),
             ("santa-bench", (3622, 2595, 0), ("West", "East"), 0x4A99),
             ("snow-globe", (3628, 2603, 0), ("North", "South"), 0x17CD)]


def say(text):
    API.SysMsg("P869: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=2.0, after=2.5):
    API.Pause(settle)
    with open(SIG, "a") as f:
        f.write("SHOT " + PHASE + "-" + name + "\n")
    API.Pause(after)


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    return ok


def close_all():
    for g in API.GetAllGumps() or []:
        try:
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


def go(x, y, z):
    stage("go %d %d %d" % (x, y, z))
    API.Pause(3)
    close_all()
    say("at %d,%d,%d (wanted %d,%d)" % (API.Player.X, API.Player.Y, API.Player.Z, x, y))


def walk_leg(name, out, back, steps=4):
    """Walks steps tiles out and the same back with the client's own walk, logging each step; a step that does not
    move, or moves z by more than 2, fails."""
    sx, sy = API.Player.X, API.Player.Y
    good = True
    for d in [out] * steps + [back] * steps:
        bx, by, bz = API.Player.X, API.Player.Y, API.Player.Z
        for _ in range(3):
            API.Walk(d)
            API.Pause(0.6)
            if (API.Player.X, API.Player.Y) != (bx, by):
                break
        moved = (API.Player.X, API.Player.Y) != (bx, by)
        say("%s step %s: %d,%d,%d -> %d,%d,%d" % (name, d, bx, by, bz, API.Player.X, API.Player.Y, API.Player.Z))
        good = good and moved and abs(API.Player.Z - bz) <= 2
    check(good and (API.Player.X, API.Player.Y) == (sx, sy), "%s: walked %d tiles %s and back beside it, each step one tile, z within 2" % (name, steps, out))


def end():
    with open(CMD, "a") as f:
        f.write("end" + chr(10))
    with open(SIG, "a") as f:
        f.write("END\n")
    API.Stop()


if API.Player.Name != CHARACTER:
    API.SysMsg("P869: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s, %s" % (API.Player.Name, PHASE))
API.Pause(7)
close_all()
API.Pause(1)
close_all()
for d in ("East", "East"):   # a new character wakes lying down
    API.Walk(d)
    API.Pause(1)
stage("serial %x" % API.Player.Serial)
stage("blessed True")
stage("winter place", 60)

try:
    for (name, (x, y, z), (out, back), part) in SPOTS:
        go(x, y, z)
        found = list(API.GetItemsOnGround(14, part) or [])
        check(len(found) > 0, "%s: its part 0x%X stands near %d,%d (%d found)" % (name, part, x, y, len(found)))
        shot(name)
        walk_leg(name, out, back)
except Exception as e:
    say("FAIL script: %s" % e)
stage("winter clear", 60)
end()
