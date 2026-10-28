# cc-P722: a real character walks into the practice bank through its south door, to the counter, and back out, step by step, in TazUO (the client's own movement, the
# server's own checks; no teleport). Made by notes/cc-P722-tools/make_walks.py from P720's IsleBridgeWalk.py.
import API

LOG = r"D:\UO\golems\Iron\p722-proof\walk-bank.log"
LEGS = [('north', 1, '<=', 3978), ('south', 1, '>=', 3984)]


def say(text):
    API.SysMsg("Walk bank: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


def done(pos, axis, op, value):
    return pos[axis] >= value if op == ">=" else pos[axis] <= value


API.Pause(8)
say("start %s" % (where(),))
for direction, axis, op, value in LEGS:
    last = where()
    stuck = 0
    for i in range(40):
        API.Walk(direction)
        API.Pause(0.6)
        now = where()
        say("%s step %d: %s" % (direction, i, now))
        if done(now, axis, op, value):
            say("%s: reached %s" % (direction, now))
            break
        stuck = stuck + 1 if now == last else 0
        last = now
        if stuck >= 4:
            say("%s: STUCK at %s" % (direction, now))
            break
    API.Pause(1)
say("end %s" % (where(),))
