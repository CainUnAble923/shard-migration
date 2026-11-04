# cc-P794: a mount actually earned, in TazUO on the private proof shard. The character holds no statuette; the achievement is
# earned through the real TryGrant (staff grant, prerequisites first), the boura's statuette arrives in the backpack by itself,
# and it is ridden. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Earned"
MEADOW = (1986, 2244, 0)
CHAIN = ["mining.prospector", "mining.surveyor", "mining.master_prospector"]
STATUETTE = 0x46F8
MOUNT = 0x3EC6


def say(text):
    API.SysMsg("P794: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=1.0, after=2.5):
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


def wait_item(graphic, seconds):
    for _ in range(int(seconds * 2)):
        it = API.FindType(graphic, API.Backpack)
        if it is not None:
            return it
        API.Pause(0.5)
    return None


if API.Player.Name != CHARACTER:
    API.SysMsg("P794: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)

API.Pause(7)
close_all()
API.Msg("[self set Blessed True")
API.Pause(1)
API.Msg("[self set Map Trammel")
API.Pause(1)
API.Msg("[self set Location (%d,%d,%d)" % MEADOW)
API.Pause(5)
check(abs(API.Player.X - MEADOW[0]) < 3 and abs(API.Player.Y - MEADOW[1]) < 3, "the character is on the meadow")
close_all()
check(API.FindType(STATUETTE, API.Backpack) is None, "no boura statuette before the earn")

for key in CHAIN:
    API.Msg("[ClusterFAchievement grant %s" % key)
    API.Pause(2)
    if key != CHAIN[-1]:
        close_all()

it = wait_item(STATUETTE, 10)
shot("earned-1-popup")
if check(it is not None, "the boura statuette arrived with the achievement"):
    close_all()
    API.Pause(1)
    API.UseObject(it.Serial)
    worn = None
    for _ in range(16):
        worn = API.FindLayer("Mount")
        if worn is not None:
            break
        API.Pause(0.5)
    check(worn is not None and worn.Graphic == MOUNT, "ridden, mount item 0x%X" % MOUNT)
    shot("earned-2-ridden")

with open(SIG, "a") as f:
    f.write("END\n")
say("done")
