# cc-P803: the League field office in New Haven, in TazUO on the private proof shard: shots outside, inside each room,
# and the League board opened and read. RELEASE (the ML town the testers play) or main (the SoS town); PHASE names
# the shot set (before or after). make_walk.py stamps the three constants.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Stock"
RELEASE = True
PHASE = "before"

BOARD_IDS = (0x1E5E, 0x1E5F)
if RELEASE:
    SPOTS = [("outside-door-side", 3461, 2593, 18), ("outside-ankh-side", 3467, 2602, 12),
             ("inside-office", 3460, 2600, 18), ("inside-quarters", 3455, 2599, 18)]
    BOARD_SPOT = (3460, 2598, 18)
else:
    SPOTS = [("outside-door-side", 3667, 2565, 0), ("inside-hall", 3664, 2550, 0), ("inside-hall-south", 3663, 2558, 0)]
    BOARD_SPOT = (3662, 2550, 0)


def say(text):
    API.SysMsg("P803: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=2.0, after=2.5):
    API.Pause(settle)
    with open(SIG, "a") as f:
        f.write("SHOT " + PHASE + "-" + name + "\n")
    API.Pause(after)


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    return ok


def close_all():
    # the before run left the login patch-notes window open behind the board (it has no packet text): close every one
    for g in API.GetAllGumps() or []:
        try:
            g.Dispose()
        except Exception:
            pass


_asked = 0


def stage(line, seconds=25):
    global _asked
    _asked += 1
    with open(CMD, "a") as f:
        f.write(line + chr(10))
    for _ in range(seconds * 2):
        with open(ACK) as f:
            if str(_asked) in f.read().split():
                return True
        API.Pause(0.5)
    say("FAIL no answer to " + line)
    return False


def go(x, y, z):
    stage("go %d %d %d" % (x, y, z))
    API.Pause(3)
    close_all()
    say("at %d,%d,%d (wanted %d,%d)" % (API.Player.X, API.Player.Y, API.Player.Z, x, y))


def end():
    with open(CMD, "a") as f:
        f.write("end" + chr(10))
    with open(SIG, "a") as f:
        f.write("END\n")
    API.Stop()


if API.Player.Name != CHARACTER:
    API.SysMsg("P803: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s, %s, %s" % (API.Player.Name, "release" if RELEASE else "main", PHASE))
API.Pause(7)
close_all()
API.Pause(1)
close_all()
# a new character wakes lying down (the isle's wake scene): two steps get it up before any shot
for d in ("East", "East"):
    API.Walk(d)
    API.Pause(1)
stage("serial %x" % API.Player.Serial)
stage("blessed True")

try:
    for (name, x, y, z) in SPOTS:
        go(x, y, z)
        shot(name)
    bx, by, bz = BOARD_SPOT
    go(bx, by, bz)
    boards = []
    for gid in BOARD_IDS:
        boards += list(API.GetItemsOnGround(8, gid) or [])
    for b in boards:
        say("board 0x%X at %d,%d,%d" % (b.Graphic, b.X, b.Y, b.Z))
    if check(len(boards) == 1, "one League board in the office (found %d)" % len(boards)):
        b = boards[0]
        shot("board-from-the-room", 1, 2)
        before = len(API.GetAllGumps() or [])
        API.ClearJournal()
        API.UseObject(b.Serial)
        API.Pause(2.5)
        after = len(API.GetAllGumps() or [])
        check(after > before and not API.InJournal("too far"), "double-clicking the board opens it (gumps %d -> %d)" % (before, after))
        shot("board-open", 0.5, 2)
        close_all()
except Exception as e:
    say("FAIL script: %s" % e)
end()
