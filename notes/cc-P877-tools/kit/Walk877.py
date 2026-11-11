# cc-P877 (P861's Walk861.py, redone for the fix-up of P876's FAIL): [VBuild statify and the town name rule in TazUO on
# the private proof shard, on main's New Haven square (the town region "Haven"). A Player-account trainee watches; staff
# hands through stage877.py do what only staff can:
#   1. Fountain of Youth (P876 item 2): staff adds a fixed Fountain of Youth on the square and tries [VBuild statify on
#      its middle part: refused, the fountain's own part still stands there and the server holds it on Trammel.
#   2. Stone fountain (P876 item 1, the review shots again): staff adds a stone fountain; statify freezes it into plain
#      statics; [VBuild undo puts the addon back.
#   3. Mara (Codex's second P2 on P861): staff adds a provisioner named Mara first (the older), then Mara the town
#      steward (ClusterFTownsfolk plaza), and runs [ShardNames dedupe: the steward keeps Mara, the older provisioner
#      gets a new name. P861's rule (the oldest keeps it) would have renamed the steward.
# "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Fixup"
PHASE = "p877"

STAND = (3658, 2603, 0)                 # main's New Haven square, inside the town region "Haven"
STAFF = (3657, 2600, 0)                 # staff, hidden, near enough to see both fountains' parts
YOUTH = (3651, 2600, 0)                 # the test Fountain of Youth's origin (paved square, NW of the stone fountain)
FOUNTAIN = (3655, 2605, 0)              # StoneFountainAddon's origin (P861's spot)
MIDDLE = 0x173A                         # both fountains' middle part (pinned's stone fountain art)
MARAS = [(3660, 2601, 0), (3661, 2601, 0)]   # P861's twin spots: the provisioner first, then the steward


def say(text):
    API.SysMsg("P877: " + text)
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


def at_spot(spot):
    """The people standing on a spot, by serial (the older first)."""
    found = []
    for m in list(API.GetAllMobiles(0x190, 10) or []) + list(API.GetAllMobiles(0x191, 10) or []):
        if (m.X, m.Y) == spot[:2] and m.Serial != API.Player.Serial:
            found.append(m)
    return sorted(found, key=lambda m: m.Serial)


def name_of(m):
    API.ClickObject(m.Serial)     # a single click: the name over the head, and the client learns it
    API.Pause(1.2)
    mm = API.FindMobile(m.Serial)
    return mm.Name if mm is not None else None


def ground(graphic, x, y, r=1):
    return [i for i in (API.GetItemsOnGround(12, graphic) or []) if abs(i.X - x) <= r and abs(i.Y - y) <= r]


if API.Player.Name != CHARACTER:
    API.SysMsg("P877: not %s, nothing to do" % CHARACTER)
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

try:
    go(*STAND)
    stage("staffgo %d %d %d" % STAFF)

    # 1. The Fountain of Youth is refused.
    stage("addat %d %d %d FountainOfYouthAddon" % YOUTH)
    API.Pause(2)
    parts = ground(MIDDLE, YOUTH[0], YOUTH[1], 0)
    check(len(parts) == 1, "the Fountain of Youth stands (its middle part 0x173A at %d,%d)" % YOUTH[:2])
    youth_part = parts[0].Serial if parts else 0
    shot("1-youth-before", 0.5)

    stage("statify %d %d %X" % (YOUTH[0], YOUTH[1], MIDDLE))
    stage("addonmap FountainOfYouthAddon")
    API.Pause(2)
    parts = ground(MIDDLE, YOUTH[0], YOUTH[1], 0)
    check(len(parts) == 1 and parts[0].Serial == youth_part,
          "statify refused the Fountain of Youth: its own middle part still stands there, no frozen copy")
    shot("2-youth-refused", 0.5)

    # 2. A stone fountain frozen into statics, then undone (P861's proof again, for the review folder).
    stage("addat %d %d %d StoneFountainAddon" % FOUNTAIN)
    API.Pause(2)
    parts = ground(MIDDLE, FOUNTAIN[0], FOUNTAIN[1], 0)
    check(len(parts) == 1, "the stone fountain stands (its middle part 0x173A at %d,%d)" % FOUNTAIN[:2])
    addon_part = parts[0].Serial if parts else 0
    shot("3-fountain-addon", 0.5)

    stage("statify %d %d %X" % (FOUNTAIN[0], FOUNTAIN[1], MIDDLE))
    stage("addonmap StoneFountainAddon")
    API.Pause(2)
    parts = ground(MIDDLE, FOUNTAIN[0], FOUNTAIN[1], 0)
    check(len(parts) == 1 and parts[0].Serial != addon_part,
          "statified: a piece of the same art stands there, a new item (a plain static), not the addon's part")
    shot("4-fountain-statics", 0.5)

    stage("undo")
    stage("addonmap StoneFountainAddon")
    API.Pause(2)
    parts = ground(MIDDLE, FOUNTAIN[0], FOUNTAIN[1], 0)
    check(len(parts) == 1 and parts[0].Serial == addon_part, "undo: the addon's own part is back and the static is gone")
    shot("5-fountain-back", 0.5)

    # 3. Mara keeps her name; the older namesake is renamed.
    stage("addat %d %d %d Provisioner set Name Mara Female true Body 0x191 CantWalk true" % MARAS[0])
    API.Pause(1)
    stage("addat %d %d %d ClusterFTownsfolk plaza" % MARAS[1])
    API.Pause(2)
    older = at_spot(MARAS[0])
    steward = at_spot(MARAS[1])
    older = [m for m in older if name_of(m) == "Mara"]
    steward = [m for m in steward if name_of(m) == "Mara"]
    ok = check(len(older) == 1 and len(steward) == 1 and older[0].Serial < steward[0].Serial,
               "two people named Mara: the provisioner (older) and the town steward")
    shot("6-maras-before", 0.5)
    if ok:
        stage("dedupe")
        API.Pause(2)
        o, s = name_of(older[0]), name_of(steward[0])
        say("names after: provisioner %s, steward %s" % (o, s))
        check(s == "Mara", "the town steward keeps Mara")
        check(o not in (None, "", "Mara"), "the older provisioner has a new name: %s" % o)
        shot("7-maras-after", 0.5)
except Exception as e:
    say("FAIL script: %s" % e)
end()
