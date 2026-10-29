# cc-P732: a brand-new character's wake on the Wakening Isle in TazUO (its first login is TazUO's own: the test-only
# creation plugin made it from the character list). Shots while lying (P731 saw the character standing in daylight), then
# the player's first move, a turn, which must get them up at once (P731: nothing happened for a minute), then the dawn.
# Each step goes to the journal and to LOG; "SHOT <name>" lines in SIG ask the runner (tazuo-walk.ps1) for a shot.
import time

import API

LOG = r"D:\UO\golems\Iron\p732-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p732-proof\shots.sig"
CHARACTER = "Iron Dusk"
UP = "You wake on a quiet shore"

if API.Player.Name != CHARACTER:
    API.SysMsg("P732: not %s, the script does not run" % CHARACTER)
    API.Stop()

T0 = time.time()


def say(text):
    API.SysMsg("P732: " + text)
    with open(LOG, "a") as f:
        f.write("[%5.1f] %s\n" % (time.time() - T0, text))


def shot(name):
    with open(SIG, "a") as f:
        f.write("SHOT " + name + "\n")
    API.Pause(1.0)


def where():
    p = API.Player
    return (p.X, p.Y, p.Z, str(p.Direction) if hasattr(p, "Direction") else "?")  # run 1: a name ("north"), not a number


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    return ok


def gumps():
    return len(API.GetAllGumps())


open(LOG, "w").close()
say("start %s at %s" % (API.Player.Name, where()))
for t, name in ((2, "lying-02"), (6, "lying-06"), (12, "lying-12"), (25, "lying-25")):
    while time.time() - T0 < t:
        API.Pause(0.25)
    say("%s: at %s, %d server windows, up: %s" % (name, where(), gumps(), API.InJournal(UP)))
    shot(name)
check(not API.InJournal(UP), "still down 25 s in, without moving")
check(API.InJournal("Move to get up"), "the System said: Move to get up.")
check(gumps() == 0, "no server window while lying")

# the first move: a turn
start = where()
t1 = time.time()
API.Turn("south")
API.Pause(0.4)
shot("getting-up")
up_after = None
while time.time() - t1 < 6:
    if API.InJournal(UP):
        up_after = time.time() - t1
        break
    API.Pause(0.2)
check(up_after is not None and up_after < 3, "the turn got them up (%s s after it)" % (None if up_after is None else round(up_after, 1)))
check(where()[:2] == start[:2], "and they stay on their tile (%s, was %s)" % (where(), start))
API.Pause(1.0)
shot("up-dawn")
API.Pause(3.0)
say("after the dawn: %d server windows" % gumps())
shot("up-day")
for i in range(3):
    API.Walk("east")
    API.Pause(0.7)
    say("  east -> %s" % (where(),))
check(where()[0] > start[0], "now they walk (%s)" % (where(),))
say("end")
with open(SIG, "a") as f:
    f.write("END\n")
