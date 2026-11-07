# cc-P812: the two staff tools in TazUO on the private proof shard. On the meadow by Britain's south road (Trammel) a staff
# character decorates a little corner with [add (a hued, named banner, a door, a lantern, a plain static), captures it with
# [VBuild capture, and reads the result in the journal (the file itself is copied from the shard's world folder by the
# runner). Then the animation locator: its gump of our bodies, and the leather wolf (body 739, an evo stage of ours on a client body) playing its actions
# with their numbers, in bursts of frames. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Tools"
SPOT = (1986, 2244, 0)


def sig(line):
    with open(SIG, "a") as f:
        f.write(line + "\n")


def say(text):
    API.SysMsg("P812: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=1.0, after=1.5):
    API.Pause(settle)
    sig("SHOT " + name)
    API.Pause(after)


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    return ok


def close_all():
    for g in API.GetAllGumps():
        try:
            if g.PacketGumpText:
                g.Dispose()
        except Exception:
            pass


def wait_journal(text, seconds):
    for _ in range(int(seconds * 2)):
        if API.InJournal(text):
            return True
        API.Pause(0.5)
    return False


def journal(seconds=6):
    for e in API.GetJournalEntries(seconds) or []:
        t = e.Text
        if "skill in" not in t and "P812" not in t and "has changed by" not in t:
            say("journal: " + t)


def fresh_target(seconds=5):
    # A cursor left from the last command would take the next answer: wait for it to go, then for the new one.
    API.Pause(0.9)
    return API.WaitForTarget("any", seconds)


def clear_cursor():
    try:
        API.CancelTarget()
    except Exception:
        pass
    API.Pause(0.3)


def add_at(what, dx, dy, dz=0):
    clear_cursor()
    API.ClearJournal()
    API.Msg("[add " + what)
    got = fresh_target(4)
    if got:
        API.Target(SPOT[0] + dx, SPOT[1] + dy, SPOT[2] + dz)
    API.Pause(1.2)
    say("add %s: target %s" % (what, got))
    journal()


if API.Player.Name != CHARACTER:
    API.SysMsg("P812: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)
API.Pause(8)
close_all()

API.Msg("[self set Map Trammel")
API.Pause(1)
API.Msg("[self set Location (%d,%d,%d)" % SPOT)
API.Pause(4)
close_all()

# ---------------------------------------------------------------- decorate, then capture
add_at("Static 0x0A99", 2, 1)
clear_cursor()
API.Msg("[set Hue 1154 Name guild_banner")
if fresh_target(4):
    API.Target(SPOT[0] + 2, SPOT[1] + 1, SPOT[2])
API.Pause(1)
add_at("Static 0x0B2C", 3, 3)
add_at("DarkWoodDoor WestCCW", 5, 1)
add_at("Lantern", 4, 3)
shot("1-decorated-corner", 1.5)

clear_cursor()
API.ClearJournal()
API.Msg("[VBuild capture p812-demo")
t1 = fresh_target(5)
if t1:
    API.Target(SPOT[0] + 1, SPOT[1], SPOT[2])
t2 = wait_journal("opposite corner", 5) and fresh_target(5)
if t2:
    API.Target(SPOT[0] + 6, SPOT[1] + 4, SPOT[2])
say("capture targets: %s %s" % (t1, t2))
check(wait_journal("Captured", 6), "[VBuild capture writes the corner")
journal(12)
for e in API.GetJournalEntries(10) or []:
    if "Captured" in e.Text or "Refused" in e.Text:
        say("journal: " + e.Text)
shot("2-captured", 0.5)

# ---------------------------------------------------------------- the animation locator
API.Msg("[AnimLocate")
API.Pause(2.5)
shot("3-animlocate-bodies", 0.5)
close_all()

API.ClearJournal()
API.Msg("[AnimLocate 739")
check(wait_journal("Animation locator", 5), "[AnimLocate 739 starts the leather wolf (body 739)")
API.Pause(0.4)
for i in range(3):
    shot("4-wolf-action-0-frame-%d" % i, 0.25, 0.1)
API.Pause(5.5)  # actions 1 and 2 play
for i in range(3):
    shot("5-wolf-action-2-frame-%d" % i, 0.25, 0.1)
for e in API.GetJournalEntries(15) or []:
    if "Body 739" in e.Text:
        say("journal: " + e.Text)
check(API.InJournal("action 2 of 12"), "the locator says each action's number")
API.Msg("[AnimLocate stop")
API.Pause(1.5)
check(API.InJournal("stopped"), "[AnimLocate stop ends the run")
shot("6-stopped", 0.5)

sig("END")
say("done")
