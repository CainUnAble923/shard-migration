# cc-P810: the staff events in TazUO on the private proof shard. As staff: the Staff Hub's Events tab and its new button,
# then a mine maze laid on the meadow by Britain's south road (1990-2001, 2240-2245, Trammel; the start row is x 1990) and an
# egg hidden 15 tiles off. Then the character drops to Player: the hunt's arrow, the egg found, a walk into the maze until a
# mine, the rise at the start, and the safe path walked to the finish. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Events"
MEADOW = (1986, 2244, 0)
C1 = (1990, 2240)
C2 = (2001, 2245)
EGG = (1975, 2232)


def sig(line):
    with open(SIG, "a") as f:
        f.write(line + "\n")


def say(text):
    API.SysMsg("P810: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=1.5, after=2.5):
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


def journal_line(text, seconds=30):
    for e in API.GetJournalEntries(seconds) or []:
        if text in e.Text:
            return e.Text
    return None


def go(x, y):
    API.Msg("[self set Location (%d,%d,0)" % (x, y))
    API.Pause(2)


def step_to(x, y):
    # One tile at a time, straight lines only: never a diagonal that could cut over a mine.
    for _ in range(80):
        px, py = API.Player.X, API.Player.Y
        if (px, py) == (x, y):
            return
        if px != x:
            API.Walk("east" if x > px else "west")
        else:
            API.Walk("south" if y > py else "north")
        API.Pause(0.45)


if API.Player.Name != CHARACTER:
    API.SysMsg("P810: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)
API.Pause(7)
close_all()

API.Msg("[self set Map Trammel")
API.Pause(1)
go(MEADOW[0], MEADOW[1])
close_all()
say("at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))

# ---------------------------------------------------------------- staff: the hub and the setup
API.Msg("[SL")
API.Pause(2.5)
API.ReplyGump(4)          # the Events tab
API.Pause(2.5)
shot("1-staff-hub-events-tab")
API.ReplyGump(5010)       # Egg hunt, maze
API.Pause(2.5)
shot("2-staff-events-gump")
close_all()

go(C1[0], C1[1])
API.Msg("[StaffEvents maze corner1")
API.Pause(1)
go(C2[0], C2[1])
API.Msg("[StaffEvents maze corner2")
API.Pause(1)
API.ClearJournal()
API.Msg("[StaffEvents maze lay")
check(wait_journal("Mine maze laid", 6), "the mine maze is laid")
API.ClearJournal()
API.Msg("[StaffEvents maze path")
API.Pause(2)
line = journal_line("Safe path:")
path = []
if line:
    for pair in line.split(":", 1)[1].split():
        x, y = pair.split(",")
        path.append((int(x), int(y)))
check(len(path) > 0, "staff read the safe path (%d tiles)" % len(path))

go(EGG[0], EGG[1])
API.ClearJournal()
API.Msg("[StaffEvents egg here")
check(wait_journal("Egg hidden", 6), "the egg is hidden")
API.Msg("[StaffEvents status")
API.Pause(1.5)

# ---------------------------------------------------------------- a player now
go(MEADOW[0], MEADOW[1] - 4)
API.Msg("[self set Blessed False")
API.Pause(1)
API.Msg("[self set AccessLevel Player")
API.Pause(1)
say("waiting for the hunt's arrow")
API.Pause(23)
shot("3-egg-hunt-arrow", 0.5)

API.Pathfind(EGG[0] + 1, EGG[1] + 1, distance=1, wait=True, timeout=30)
API.Pause(1)
eggs = API.GetItemsOnGround(4, 0x47E6) or []
check(len(eggs) > 0, "the egg is on the ground here")
shot("4-the-egg", 1)
API.ClearJournal()
if eggs:
    API.UseObject(eggs[0].Serial)
check(wait_journal("found the egg", 6), "double-clicking the egg wins the hunt")
shot("5-egg-found", 1)

# Into the maze, along a lane off the safe path, until a mine.
start_lane_y = path[0][1] if path else C1[1]
lane_y = C1[1] + ((start_lane_y - C1[1] + 3) % 6)
API.Pathfind(C1[0] - 1, lane_y, distance=0, wait=True, timeout=30)
step_to(C1[0] - 1, lane_y)
shot("6-maze-start", 1)
API.ClearJournal()
for _ in range(14):
    API.Walk("east")
    API.Pause(0.6)
    if API.InJournal("stepped on a mine"):
        break
check(wait_journal("stepped on a mine", 3), "a mine goes off under the player")
shot("7-mine-death", 0.8)
check(wait_journal("rise at the maze", 3), "the player is told their belongings are safe")
API.Pause(7)
say("after the mine: %d,%d" % (API.Player.X, API.Player.Y))
shot("8-risen-at-start", 1)

# The safe path to the finish.
if path:
    API.ClearJournal()
    step_to(path[0][0], path[0][1])
    for (x, y) in path[1:]:
        step_to(x, y)
    check(wait_journal("crossed the mine maze", 5), "walking the safe path wins a place")
    shot("9-maze-crossed", 1)

sig("END")
say("done")
