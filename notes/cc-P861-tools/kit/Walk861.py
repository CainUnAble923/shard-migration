# cc-P861: the names and [VBuild statify in TazUO on the private proof shard, on main's New Haven square (the town region
# "Haven"). A Player-account trainee watches; staff hands through stage861.py do what only staff can:
#   1. names: two provisioners named "Aaron" (pinned's male list) stand side by side; the trainee clicks both (the
#      names show over their heads); staff runs [ShardNames dedupe; the trainee clicks again: one is still Aaron, the
#      other has a new name from the same list. [ShardNames status lists our lists in stage-out.txt.
#   2. statify: staff adds a stone fountain (an addon); the camera takes it; staff freezes it with [VBuild statify on its
#      middle part; the fountain still stands, now as plain statics, and the server holds the addon on the internal map;
#      [VBuild undo puts the addon back.
# "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Names"
PHASE = "p861"

STAND = (3658, 2603, 0)                 # main's New Haven square, inside the town region "Haven"
TWINS = [(3660, 2601, 0), (3661, 2601, 0)]
STAFF = (3657, 2600, 0)                  # staff, hidden, near enough to see the fountain's parts
FOUNTAIN = (3655, 2605, 0)               # StoneFountainAddon's origin; its middle part there is 0x173A
FOUNTAIN_MIDDLE = 0x173A
NAME = "Aaron"


def say(text):
    API.SysMsg("P861: " + text)
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
    for g in API.GetAllGumps() or []:
        try:
            g.Dispose()
        except Exception:
            pass


_asked = 0


def stage(line, seconds=30):
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


def twins():
    """The two provisioners at the twin spots, by serial, in serial order (the older first)."""
    found = []
    for m in list(API.GetAllMobiles(0x190, 8) or []) + list(API.GetAllMobiles(0x191, 8) or []):
        if (m.X, m.Y) in [(x, y) for x, y, z in TWINS] and m.Serial != API.Player.Serial:
            found.append(m)
    return sorted(found, key=lambda m: m.Serial)


def names_of(ms):
    out = []
    for m in ms:
        API.ClickObject(m.Serial)     # a single click: the name over the head, and the client learns it
        API.Pause(0.8)
    API.Pause(1)
    for m in ms:
        mm = API.FindMobile(m.Serial)
        out.append(mm.Name if mm is not None else None)
    return out


def ground(graphic, x, y, r=1):
    return [i for i in (API.GetItemsOnGround(10, graphic) or []) if abs(i.X - x) <= r and abs(i.Y - y) <= r]


if API.Player.Name != CHARACTER:
    API.SysMsg("P861: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)
API.Pause(7)
close_all()
API.Pause(1)
close_all()
for d in ("East", "East"):   # a new character wakes lying down
    API.Walk(d)
    API.Pause(1)
stage("serial %x" % API.Player.Serial)
stage("blessed True")
stage("young False")
stage("names")

try:
    go(*STAND)
    stage("staffgo %d %d %d" % STAFF)

    # 1. Two townsfolk named alike, then the town rule.
    for (x, y, z) in TWINS:
        stage("addat %d %d %d Provisioner set Name %s CantWalk true" % (x, y, z, NAME))
    API.Pause(2)
    # Run 1: a wandering townsperson stepped onto a twin spot; the two are the ones named Aaron there, by serial.
    near = twins()
    named = names_of(near)
    ms = [m for m, n in zip(near, named) if n == NAME]
    check(len(ms) == 2, "two provisioners named %s stand at the twin spots (%d of %d there)" % (NAME, len(ms), len(near)))
    before = names_of(ms)
    say("names before: %s" % before)
    check(before == [NAME, NAME], "both are named %s" % NAME)
    shot("1-twins-before", 0.5)

    stage("dedupe")
    API.Pause(2)
    after = names_of(ms)
    say("names after: %s" % after)
    check(len(after) == 2 and after[0] == NAME and after[1] not in (None, "", NAME),
          "the older keeps %s, the other has a new name: %s" % (NAME, after))
    shot("2-twins-after", 0.5)

    # 2. A placed addon frozen into statics, then undone.
    stage("addat %d %d %d StoneFountainAddon" % FOUNTAIN)
    API.Pause(2)
    parts = ground(FOUNTAIN_MIDDLE, FOUNTAIN[0], FOUNTAIN[1])
    check(len(parts) == 1, "the stone fountain stands (its middle part 0x173A at %d,%d)" % FOUNTAIN[:2])
    addon_part = parts[0].Serial if parts else 0
    shot("3-fountain-addon", 0.5)

    stage("statify %d %d %X" % (FOUNTAIN[0], FOUNTAIN[1], FOUNTAIN_MIDDLE))
    stage("addonmap StoneFountainAddon")
    API.Pause(2)
    parts = ground(FOUNTAIN_MIDDLE, FOUNTAIN[0], FOUNTAIN[1])
    check(len(parts) == 1 and parts[0].Serial != addon_part,
          "statified: a piece of the same art stands there, a new item (a plain static), not the addon's part")
    shot("4-fountain-statics", 0.5)

    stage("undo")
    stage("addonmap StoneFountainAddon")
    API.Pause(2)
    parts = ground(FOUNTAIN_MIDDLE, FOUNTAIN[0], FOUNTAIN[1])
    check(len(parts) == 1 and parts[0].Serial == addon_part, "undo: the addon's own part is back and the static is gone")
    shot("5-fountain-back", 0.5)
except Exception as e:
    say("FAIL script: %s" % e)
end()
