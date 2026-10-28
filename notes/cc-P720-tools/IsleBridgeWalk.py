# cc-P720 item 7: a real character walks the dock to the moongate's landing and back, step by step, in TazUO (the
# client's own movement, the server's own checks; no teleport). Started by TazUO in the world (Data\lscript.json).
# The character starts on the road west of the dock (the shot's commands put it there). Each step's position goes to
# the journal and to D:\UO\golems\Iron\p720-proof\bridge-walk.log. Stops short of the moongate (x 6832), which would
# send a character with no lessons left to New Haven.
import API

LOG = r"D:\UO\golems\Iron\p720-proof\bridge-walk.log"


def say(text):
    API.SysMsg("BridgeWalk: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


API.Pause(8)
say("start %s" % (where(),))
for leg, (direction, stop) in enumerate((("east", lambda x: x >= 6830), ("west", lambda x: x <= 6812))):
    last = where()
    stuck = 0
    for i in range(40):
        API.Walk(direction)
        API.Pause(0.6)
        now = where()
        say("%s step %d: %s" % (direction, i, now))
        if stop(now[0]):
            say("%s: reached %s" % (direction, now))
            break
        stuck = stuck + 1 if now == last else 0
        last = now
        if stuck >= 4:
            say("%s: STUCK at %s" % (direction, now))
            break
    API.Pause(1)
say("done %s" % (where(),))
