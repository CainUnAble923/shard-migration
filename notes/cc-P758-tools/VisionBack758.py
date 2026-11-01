# cc-P758: the disconnect mid-vision, part 2. After VisionDrop758.py's hard disconnect (the client killed in the
# chamber), TazUO logs the same trainee back in. This script checks it stands on the very tile it started the vision
# from (START, written by part 1), not in the chamber strip, seen, and free to move.
import API

LOG = r"D:\UO\golems\Iron\p758-proof\drop.log"
SIG = r"D:\UO\golems\Iron\p758-proof\back-signal.txt"
START = r"D:\UO\golems\Iron\p758-proof\drop-start.txt"
CHARACTER = "Iron Visionary"
STRIP = (6170, 3752, 6570, 3760)
FAILS = []


def say(text):
    with open(LOG, "a") as f:
        f.write(text + "\n")
    API.SysMsg("P758: " + text)


def signal(text):
    with open(SIG, "a") as f:
        f.write(text + "\n")


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    if not ok:
        FAILS.append(what)
    return ok


def where():
    p = API.Player
    return (int(p.X), int(p.Y), int(p.Z))


def hidden():
    for name in ("IsHidden", "Hidden"):
        v = getattr(API.Player, name, None)
        if v is not None:
            return bool(v)
    return None


if API.Player.Name != CHARACTER:
    API.SysMsg("P758: not %s, the script does not run" % CHARACTER)
else:
    API.Pause(6)
    with open(START) as f:
        start = tuple(int(v) for v in f.read().split())
    here = where()
    say("logged back in at %s (the vision started from %s)" % (here, start))
    signal("SHOT drop-02-back")
    check(here == start, "back on the very tile the vision started from (%s, was %s)" % (here, start))
    check(not (STRIP[0] <= here[0] <= STRIP[2] and STRIP[1] <= here[1] <= STRIP[3]), "not in the chamber strip")
    check(hidden() in (False, None), "seen (hidden flag: %s)" % (hidden(),))
    # free to move: the first step may only turn, so walk south up to three times, then come back
    moved = here
    for _ in range(3):
        API.Walk("south")
        API.Pause(0.8)
        moved = where()
        if moved != here:
            break
    check(moved != here, "free to move (stepped to %s)" % (moved,))
    API.Walk("north")
    API.Pause(0.8)
    signal("SHOT drop-03-moved")
    API.Pause(1.5)
    say("END part 2, %d failed: %s" % (len(FAILS), FAILS))
    signal("DONE")
