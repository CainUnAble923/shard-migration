# cc-P793: the Peacock in TazUO on the private proof shard. A new character on the Golem's admin account goes to the
# Trinsic road meadow, finds a wild peacock (seeded by itself on this copy of an existing world), tames it with Animal
# Taming, has it follow, rides it, dismounts and leashes it. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API
import time

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Peacock"
BODY, FIGURINE, LEASH = 1440, 0xA0C0, 0x1374
MEADOW = (1986, 2244, 0)


def say(text):
    API.SysMsg("P793: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=1.5, after=2.5):
    API.Pause(settle)
    with open(SIG, "a") as f:
        f.write("SHOT " + name + "\n")
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


def peacock(seconds, dist=20):
    for _ in range(int(seconds * 2)):
        found = API.GetAllMobiles(BODY, dist)
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
    API.SysMsg("P793: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)

API.Pause(7)
close_all()

API.Msg("[self set Blessed True")
API.Pause(1)
API.Msg("set animaltaming 100")
API.Pause(1)
API.Msg("[self set Map Trammel")
API.Pause(1)
API.Msg("[self set Location (%d,%d,%d)" % MEADOW)
API.Pause(5)
say("at %d,%d" % (API.Player.X, API.Player.Y))
check(abs(API.Player.X - MEADOW[0]) < 3 and abs(API.Player.Y - MEADOW[1]) < 3, "the character is on the meadow")
close_all()

API.ClearJournal()
API.Msg("[Peacock status")
API.Pause(2)
check(API.InJournal("spawner there"), "[Peacock status names a meadow spawner")

bird = peacock(20)
check(bird is not None, "a wild peacock is on the meadow")
if bird is None:
    with open(SIG, "a") as f:
        f.write("SHOT 0-no-peacock\nEND\n")
    API.Stop()

shot("1-wild-peacock", 1.0)

# Close enough to tame.
API.Pathfind(bird.X, bird.Y, distance=2, wait=True, timeout=20)
API.ClearJournal()
tamed = False
for attempt in range(6):
    bird = peacock(10) or bird
    API.Pathfind(bird.X, bird.Y, distance=2, wait=True, timeout=10)
    API.UseSkill("Animal Taming")
    if API.WaitForTarget("any", 5):
        API.Target(bird.Serial)
    if wait_journal("accept you as master", 25):
        tamed = True
        break
    API.Pause(3)
check(tamed, "Animal Taming tames it")
MINE = bird.Serial  # the meadow has wild ones too: from here on, only this one
shot("2-tamed", 0.5)

# It follows: a burst of frames while it walks.
API.Msg("all follow me")
API.Pause(1)
API.Pathfind(MEADOW[0] + 8, MEADOW[1] + 2, distance=0, wait=False)
shot("3-walking-a", 0.4, 0.3)
shot("3-walking-b", 0.2, 0.3)
shot("3-walking-c", 0.2, 0.3)
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
check(API.FindMobile(MINE) is None or API.FindMobile(MINE).Distance > 18, "riding: the tamed peacock left the ground")
mount = None
try:
    mount = API.FindLayer("Mount")
except Exception as e:
    say("FindLayer: %s" % e)
say("mount layer: %s" % (mount.Graphic if mount is not None else None))
check(mount is not None and mount.Graphic == 0x3ECF, "the mount item is 0x3ECF")
shot("4-ridden", 1.0)

API.Pathfind(MEADOW[0] - 6, MEADOW[1] - 6, distance=0, wait=False)
shot("5-ridden-walking-a", 0.4, 0.3)
shot("5-ridden-walking-b", 0.2, 0.3)
shot("5-ridden-walking-c", 0.2, 0.3)
API.Pause(6)

# Down again.
API.Dismount()
API.Pause(2)
bird = API.FindMobile(MINE)
check(bird is not None, "dismounted: the tamed peacock is back on the ground")
shot("6-dismounted", 1.0)

# The leash's figurine.
API.Msg("[self AddToPack PetLeash")
leash = wait_item(LEASH, 10)
if check(leash is not None and bird is not None, "a leash in the backpack"):
    API.UseObject(leash.Serial)
    if check(API.WaitForTarget("any", 5), "the leash asks for a target"):
        API.Target(bird.Serial)
fig = wait_item(FIGURINE, 10)
check(fig is not None, "the peacock figurine 0xA0C0 is in the backpack")
API.UseObject(API.Backpack)
shot("7-figurine", 2.0)

with open(SIG, "a") as f:
    f.write("END\n")
say("done")
