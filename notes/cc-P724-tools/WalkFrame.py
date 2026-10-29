# cc-P724: a real character walks the dock east into the moongate frame (up its steps onto the floor, short of the gate),
# then back west to the road, step by step in TazUO (the client's own movement; no teleport). Then, from the road again,
# east all the way into the gate. Positions go to the journal and to LOG. From P722's walk template.
import API

LOG = r"D:\UO\golems\Iron\p724-work\walk-frame.log"


def say(text):
    API.SysMsg("Walk frame: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def where():
    p = API.Player
    return (p.X, p.Y, p.Z, API.GetMap() if hasattr(API, "GetMap") else "?")


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


API.Pause(8)
open(LOG, "w").close()
say("start %s" % (where(),))
leg("east", lambda p: p[0] >= 6830)
API.Pause(1.5)
leg("west", lambda p: p[0] <= 6812)
API.Pause(1.5)
say("now into the gate")
leg("east", lambda p: p[0] < 6800 or p[0] >= 6832)
API.Pause(3)
say("end %s" % (where(),))
