# cc-P758: the disconnect mid-vision, part 1. A brand-new trainee (made by the bot's client, stopped at the standing
# stones with every lesson before the vision done, isle.py --stop-at core.loop) is logged in by TazUO. This script
# double-clicks the vision's signpost, waits until the trainee is in the chamber and the Stranger has struck, writes
# the tile it started on to START, and asks the runner (isle-shots758.ps1) to KILL the client: a hard disconnect, no
# logout. Part 2 (VisionBack758.py) logs back in and checks the trainee stands on that tile.
import API
import time

LOG = r"D:\UO\golems\Iron\p758-proof\drop.log"
SIG = r"D:\UO\golems\Iron\p758-proof\drop-signal.txt"
START = r"D:\UO\golems\Iron\p758-proof\drop-start.txt"
CHARACTER = "Iron Visionary"
LOOP_SIGN = (6794, 3981)            # TutorialCorePlacement.SignPoint("core.loop")
STRIP = (6170, 3752, 6570, 3760)    # TutorialVisionChamber.Strip
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


def in_strip(p):
    return STRIP[0] <= p[0] <= STRIP[2] and STRIP[1] <= p[1] <= STRIP[3]


def clear():
    for _ in range(6):
        API.CloseGump()
        API.Pause(0.3)
    for g in API.GetAllGumps():
        try:
            g.Dispose()
        except Exception:
            pass


if API.Player.Name != CHARACTER:
    API.SysMsg("P758: not %s, the script does not run" % CHARACTER)
else:
    API.Pause(6)
    for _ in range(3):
        clear()
        API.Pause(2)
    start = where()
    with open(START, "w") as f:
        f.write("%d %d %d\n" % start)
    say("start %s at %s" % (CHARACTER, start))
    signal("SHOT drop-00-at-the-stones")
    sign = None
    for it in API.GetItemsOnGround(6, 0xA854):
        if (int(it.X), int(it.Y)) == LOOP_SIGN:
            sign = it
    if check(sign is not None, "the vision's signpost stands at %s" % (LOOP_SIGN,)):
        t0 = None
        for attempt in range(3):
            API.UseObject(sign.Serial)
            t1 = time.time()
            while time.time() - t1 < 4 and not in_strip(where()):
                API.Pause(0.1)
            if in_strip(where()):
                t0 = time.time() - 0.2
                say("the vision started on double-click %d" % (attempt + 1))
                break
            say("double-click %d: no vision yet (at %s)" % (attempt + 1, where()))
            clear()
            API.Pause(1.0)
        if check(t0 is not None, "the vision started"):
            # past the strike (8 s) and the burst (9 s), before the shatter (16 s)
            while time.time() - t0 < 10.0:
                API.Pause(0.1)
            p = where()
            check(in_strip(p), "mid-vision, in the chamber at %s" % (p,))
            signal("SHOT drop-01-mid-vision")
            API.Pause(1.0)
            say("END part 1, %d failed: %s; asking for the hard disconnect" % (len(FAILS), FAILS))
            signal("KILL")
    if FAILS:
        signal("DONE")
