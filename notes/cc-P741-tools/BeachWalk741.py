# cc-P741: a real character walks the isle's west beach in TazUO, step by step with the client's own movement (no
# teleport): north along the sand past the beached half of the wreck, then east along the north-west beach. Each step's
# position and Z go to LOG (not the journal, so the frames show the beach); a leg that makes no progress for 4 steps is logged STUCK. P724's WalkFrame.py.
import API

LOG = r"D:\UO\golems\Iron\p741-proof\beach-walk.log"


def say(text):
    with open(LOG, "a") as f:
        f.write(text + "\n")


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


def leg(direction, stop, steps=40):
    last, stuck = where(), 0
    for i in range(steps):
        API.Walk(direction)
        API.Pause(0.7)
        now = where()
        say("%s step %d: %s" % (direction, i, now))
        if stop(now):
            say("%s: reached %s" % (direction, now))
            return True
        stuck = stuck + 1 if now == last else 0
        last = now
        if stuck >= 4:
            say("%s: STUCK at %s" % (direction, now))
            return False
    return False


API.Pause(5)
for _ in range(3):  # Clear741.py: the client's windows the login opens, so the frames show the beach
    for i in range(6):
        API.CloseGump()
        API.Pause(0.3)
    for g in API.GetAllGumps():
        try:
            g.Dispose()
        except Exception:
            pass
    API.Pause(2)
open(LOG, "w").close()
say("start %s" % (where(),))
leg("north", lambda p: p[1] <= 3985)
API.Pause(1.0)
leg("east", lambda p: p[0] >= 6650)
API.Pause(1.0)
leg("west", lambda p: p[0] <= 6631)
API.Pause(1.0)
leg("south", lambda p: p[1] >= 4002)
API.Pause(2)
say("end %s" % (where(),))
