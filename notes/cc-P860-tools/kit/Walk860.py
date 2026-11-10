# cc-P860: the ridable polar bear in TazUO on the private proof shard (P793's Shots793.py and P859's Walk859.py). A
# Player-account trainee goes to a den on Dagger Isle (its spawner seeded by itself on this copy of an existing world),
# finds a wild ridable polar bear, tames it with Animal Taming (the trainee's own skill use and target), has it follow,
# rides it (the mount item must be 0x3EC5), rides about, dismounts, and leashes it to the polar bear's figurine. Staff
# hands through stage860.py only move the trainee, set the skill, hand over a leash and report what the server holds.
# "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Frost"
PHASE = "p860"

BODY, MOUNT_ITEM, FIGURINE, LEASH = 213, 0x3EC5, 0x20E1, 0x1374
DEN = (4090, 325, 0)           # RidablePolarBearDens: "Dagger Isle, north snowfield", home range 10
STAND = (4085, 320, 0)         # a few tiles north-west of the den's centre, so the camera looks across it


def say(text):
    API.SysMsg("P860: " + text)
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


def text_of(serial):
    try:
        return (API.ItemNameAndProps(serial, True, 2) or "").lower()
    except Exception:
        return ""


def ridable_bears(dist=24):
    """Body-213 mobiles that are ridable polar bears (a plain polar bear shares the body; ours names Milva)."""
    out = []
    for m in API.GetAllMobiles(BODY, dist) or []:
        t = (m.Name or "").lower() + " " + text_of(m.Serial)
        if "ridable" in t or "milva" in t:
            out.append(m)
    return out


def wait_bear(seconds):
    for _ in range(int(seconds * 2)):
        found = ridable_bears()
        if found:
            return found[0]
        API.Pause(0.5)
    return None


def wait_item(graphic, seconds):
    for _ in range(int(seconds * 2)):
        it = API.FindType(graphic, API.Backpack)
        if it is not None:
            return it
        API.Pause(0.5)
    return None


def wait_journal(text, seconds):
    for _ in range(int(seconds * 2)):
        if API.InJournal(text):
            return True
        API.Pause(0.5)
    return False


if API.Player.Name != CHARACTER:
    API.SysMsg("P860: not %s, nothing to do" % CHARACTER)
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
stage("dens")

try:
    go(*STAND)
    # Run 1: skills set before the move were gone after it (taming said "no chance"; leaving the isle resets a new
    # character), so they are set here, on Dagger Isle, and read back.
    stage("skill AnimalTaming 100")
    stage("skill AnimalLore 100")
    stage("getskill AnimalTaming")
    API.Pause(1)
    bear = wait_bear(25)
    check(bear is not None, "a wild ridable polar bear is at the den (seeded by itself on this world copy)")
    if bear is None:
        shot("0-no-bear")
        end()
    say("bear %x at %d,%d: %s" % (bear.Serial, bear.X, bear.Y, text_of(bear.Serial).replace("\n", " | ")))
    shot("1-wild-bear")

    # Tame it: the trainee's own skill use and target.
    API.ClearJournal()
    tamed = False
    for attempt in range(8):
        b = API.FindMobile(bear.Serial) or bear
        API.Pathfind(b.X, b.Y, distance=2, wait=True, timeout=10)
        API.UseSkill("Animal Taming")
        if API.WaitForTarget("any", 5):
            API.Target(bear.Serial)
        if wait_journal("accept you as master", 25):
            tamed = True
            break
        API.Pause(4)
    check(tamed, "Animal Taming tames it")
    MINE = bear.Serial
    shot("2-tamed", 0.5)

    # It follows.
    API.Msg("all follow me")
    API.Pause(1)
    API.Pathfind(DEN[0] + 6, DEN[1] + 4, distance=0, wait=False)
    shot("3-following-a", 0.6, 0.3)
    shot("3-following-b", 0.3, 0.3)
    API.Pause(6)

    # Ride it.
    for attempt in range(6):
        me = API.FindMobile(MINE)
        if me is None:
            break
        API.Pathfind(me.X, me.Y, distance=1, wait=True, timeout=10)
        API.Pause(0.5)
        API.UseObject(MINE)
        API.Pause(1.5)
        if API.FindLayer("Mount") is not None:
            break
    mount = API.FindLayer("Mount")
    say("mount layer: %s" % (hex(mount.Graphic) if mount is not None else None))
    check(mount is not None and mount.Graphic == MOUNT_ITEM, "riding: the mount item is 0x3EC5")
    shot("4-ridden", 1.0)

    API.Pathfind(DEN[0] - 6, DEN[1] + 6, distance=0, wait=False)
    shot("5-ridden-walking-a", 0.6, 0.3)
    shot("5-ridden-walking-b", 0.3, 0.3)
    shot("5-ridden-walking-c", 0.3, 0.3)
    API.Pause(6)
    shot("5-ridden-stopped", 0.5)

    # Down again.
    API.Dismount()
    API.Pause(2)
    back = API.FindMobile(MINE)
    check(back is not None and API.FindLayer("Mount") is None, "dismounted: the bear is back on the snow")
    shot("6-dismounted", 1.0)

    # The leash's figurine.
    stage("give PetLeash")
    leash = wait_item(LEASH, 10)
    if check(leash is not None and back is not None, "a leash in the backpack"):
        API.UseObject(leash.Serial)
        if check(API.WaitForTarget("any", 5), "the leash asks for a target"):
            API.Target(MINE)
    fig = wait_item(FIGURINE, 10)
    check(fig is not None, "the polar bear figurine 0x20E1 is in the backpack")
    API.UseObject(API.Backpack)
    shot("7-figurine", 2.0)
    stage("dens")
except Exception as e:
    say("FAIL script: %s" % e)
end()
