# cc-P734: a real character walks the practice farmgate, step by step in TazUO (the client's own movement, the server's
# own checks; no teleport). A closed door or gate in the way is double-clicked open, as a player would. Made by
# notes/cc-P734-tools/make_walks.py.
import API

LOG = r"D:\UO\golems\Iron\p734-proof\walk-farmgate.log"
LEGS = [('east', 0, '>=', 5712), ('west', 0, '<=', 5709)]
DOORS = set(range(0x0675, 0x06F5)) | set(range(0x0839, 0x0849))


def say(text):
    API.SysMsg("Walk farmgate: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


def done(pos, axis, op, value):
    return pos[axis] >= value if op == ">=" else pos[axis] <= value


def open_door():
    for it in API.GetItemsOnGround(2) or []:
        if it.Graphic in DOORS:
            API.UseObject(it.Serial)
            say("opened a door or gate 0x%04X at %d,%d,%d" % (it.Graphic, it.X, it.Y, it.Z))
            API.Pause(1)
            return True
    return False


API.Pause(8)
open(LOG, "w").close()
say("start %s" % (where(),))
for direction, axis, op, value in LEGS:
    last = where()
    stuck = 0
    opened = False
    for i in range(40):
        API.Walk(direction)
        API.Pause(0.6)
        now = where()
        say("%s step %d: %s" % (direction, i, now))
        if done(now, axis, op, value):
            say("%s: reached %s" % (direction, now))
            break
        # No progress along the leg's axis counts as stuck (a side-step shuffle is not progress).
        stuck = stuck + 1 if (now[axis] - last[axis]) * (1 if op == ">=" else -1) <= 0 else 0
        last = now
        if stuck >= 2 and not opened:
            opened = open_door()
            stuck = 0
        if stuck >= 4:
            say("%s: STUCK at %s" % (direction, now))
            break
    API.Pause(1)
say("end %s" % (where(),))
