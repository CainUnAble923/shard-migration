# cc-P827 (a copy of notes/cc-P803-tools/main/WalkMainAfter.py, after P824's review: the new spots, main's office
# seeded from the current layout first, and a real walk past each changed piece, both ways).
# cc-P803: the League field office in New Haven, in TazUO on the private proof shard: shots outside, inside each room,
# and the League board opened and read. RELEASE (the ML town the testers play) or main (the SoS town); PHASE names
# the shot set (before or after). make_walk.py stamps the three constants.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Stock"
RELEASE = True
PHASE = "after"

BOARD_IDS = (0x1E5E, 0x1E5F)
if RELEASE:
    SPOTS = [("outside-door-side", 3461, 2593, 18), ("outside-sign-from-the-street", 3463, 2594, 15),
             ("outside-ankh-side", 3467, 2602, 12), ("inside-office", 3460, 2600, 18), ("inside-office-west-wall", 3460, 2602, 18),
             ("inside-quarters", 3455, 2599, 18)]
    BOARD_SPOT = (3460, 2601, 18)
    # from the front door's step north to the road along the door's line, east past the signpost, and back
    WALK_FROM = (3459, 2595, 15)
    WALK = ["North", "North", "North", "East", "East", "West", "West", "South", "South", "South"]
else:
    SPOTS = [("outside-door-side", 3667, 2565, 0), ("outside-sign", 3670, 2566, 0), ("inside-hall", 3664, 2550, 0),
             ("inside-hall-north-wall", 3663, 2551, 0), ("inside-hall-south", 3663, 2558, 0)]
    BOARD_SPOT = (3663, 2550, 0)
    # in through the arch and out again, past the sign arm
    WALK_FROM = (3667, 2565, 0)
    WALK = ["North", "North", "North", "North", "South", "South", "South", "South", "East", "East", "East", "West", "West", "West"]


def say(text):
    API.SysMsg("P827: " + text)
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
    API.SysMsg("P827: not %s, nothing to do" % CHARACTER)
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
if not RELEASE:
    stage("office", 40)  # P824 item 5: this world's office decor stood in the other town's house


def walk_leg():
    x, y, z = WALK_FROM
    go(x, y, z)
    say("walk from %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
    for d in WALK:
        px, py = API.Player.X, API.Player.Y
        API.Walk(d)
        API.Pause(0.8)
        moved = API.Player.X != px or API.Player.Y != py
        say("%s %s -> %d,%d,%d" % ("step" if moved else "STUCK", d, API.Player.X, API.Player.Y, API.Player.Z))
    check((API.Player.X, API.Player.Y) == (x, y), "walked out and back to %d,%d" % (x, y))

try:
    walk_leg()
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
