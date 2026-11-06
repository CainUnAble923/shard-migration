# cc-P806: Rook's bench on main, on a copy of the bot world (seeded by main's older image with the crosswise pieces): the joined bench,
# Rook facing the square, from the moongate exit in front of him. The items at the bench are listed for the log.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Main"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"


def say(text):
    API.SysMsg("P806: " + text)
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


if API.Player.Name != CHARACTER:
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)
API.Pause(7)
close_all()
API.Pause(1)
close_all()
stage("serial %x" % API.Player.Serial)
try:
    go(3669, 2634, 0)
    say("at the moongate exit %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
    shot("1-main-rook-from-the-moongate-exit")
    new = [(i.X, i.Y, i.Z) for i in (API.GetItemsOnGround(5, 0x0B2D) or [])]
    old = [(i.X, i.Y, i.Z) for i in (API.GetItemsOnGround(5, 0x0B2C) or [])]
    say(("PASS " if len(new) == 2 else "FAIL ") + "two joined pieces 0x0B2D: %s" % new)
    say(("PASS " if not old else "FAIL ") + "no old 0x0B2C left: %s" % old)
    go(3667, 2634, 0)
    shot("1-main-rook-bench")
    stage("rookdir")
    say("done")
except Exception as e:
    say("FAIL the script stopped: %s" % e)
with open(CMD, "a") as f:
    f.write("end" + chr(10))
with open(SIG, "a") as f:
    f.write("END\n")
API.Stop()
