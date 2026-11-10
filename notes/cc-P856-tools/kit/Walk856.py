# cc-P856: New Haven's winter set in TazUO on the private proof shard. A Player-account trainee; staff hands through
# stage856.py (the CMD/ACK file channel): the winter decor put up by staff ([ClusterFWinterDecor place, as on December
# 1), then the trainee stands north-west of each piece of the set and the camera takes it, and a check that each piece's
# parts stand on the ground there. RELEASE picks the town: True the ML plaza (release branch), False the SoS New Haven
# (main). The release kit's copy has RELEASE = True.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Winter"
RELEASE = False
PHASE = "p856-release" if RELEASE else "p856-main"

# (shot name, where the trainee stands, a part of the piece the check looks for)
if RELEASE:
    SPOTS = [("train", (3543, 2518, 20), 0x1B73), ("santa-bench", (3500, 2585, 14), 0x4A99),
             ("snow-globe", (3516, 2589, 1), 0x17CD), ("snowman-bench", (3501, 2593, 1), 0x9E1B)]
else:
    SPOTS = [("train", (3607, 2533, 0), 0x1B73), ("snowman-bench", (3614, 2541, 0), 0x9E1B),
             ("santa-bench", (3610, 2551, 0), 0x4A99), ("snow-globe", (3636, 2554, 0), 0x17CD)]


def say(text):
    API.SysMsg("P856: " + text)
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


def end():
    with open(CMD, "a") as f:
        f.write("end" + chr(10))
    with open(SIG, "a") as f:
        f.write("END\n")
    API.Stop()


if API.Player.Name != CHARACTER:
    API.SysMsg("P856: not %s, nothing to do" % CHARACTER)
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
    for (name, (x, y, z), part) in SPOTS:
        go(x, y, z)
        found = list(API.GetItemsOnGround(14, part) or [])
        check(len(found) > 0, "%s: its part 0x%X stands near %d,%d (%d found)" % (name, part, x, y, len(found)))
        shot(name)
except Exception as e:
    say("FAIL script: %s" % e)
stage("winter clear", 60)
end()
