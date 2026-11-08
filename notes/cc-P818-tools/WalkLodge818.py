# cc-P818 (P724's WalkFrame.py): a real character walks from the road down the new brick walk to the League lodge's east
# door, through it (TazUO opens a door walked into, guide 11.9) to Elara, and back out and up to the road, step by step in
# the client (no teleport). Each step's position goes to the journal and to LOG.
import API

LOG = r"D:\UO\golems\Iron\p818-proof\walk-lodge.log"


def say(text):
    API.SysMsg("Walk lodge: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


def leg(direction, stop, steps=30):
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
    say("%s: out of steps at %s" % (direction, now))
    return False


API.Pause(8)
open(LOG, "w").close()
say("start %s" % (where(),))
ok = leg("south", lambda p: p[1] >= 4000)                       # down the walk, x 6789
ok = leg("west", lambda p: p[0] <= 6784) and ok                 # the step, the door, inside to the carpet's end
API.Pause(1.5)
ok = leg("east", lambda p: p[0] >= 6789) and ok                 # out through the door again
ok = leg("north", lambda p: p[1] <= 3988) and ok                # up the walk to the road
API.Pause(1)
say("end %s %s" % (where(), "ALL LEGS WALKED" if ok else "A LEG FAILED"))
