# cc-P794: each ethereal look ridden, in TazUO on the private proof shard. A new character on the Golem's admin account goes
# to an open meadow, takes the seven statuettes ([self AddToPack), and for each: double-clicks it (the real cast), shoots it
# ridden, walks, shoots again, dismounts. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Ethereal"
MEADOW = (1986, 2244, 0)
LOOKS = [
    ("windrunner", "EtherealWindrunner", 0x9ED5, 0x3ECC),
    ("lasher", "EtherealLasher", 0x9E35, 0x3ECB),
    ("tiger", "EtherealTiger", 0x9844, 0x3EC8),
    ("light-tiger", "EtherealLightTiger", 0x9844, 0x3EC7),
    ("hellhound", "EtherealAncientHellHound", 0x3FFD, 0x3EC9),
    ("boura", "EtherealBoura", 0x46F8, 0x3EC6),
    ("peacock", "EtherealPeacock", 0xA0C0, 0x3ECF),
]


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


def mount_layer(seconds):
    for _ in range(int(seconds * 2)):
        m = API.FindLayer("Mount")
        if m is not None:
            return m
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

for name, cls, statuette, mount in LOOKS:
    API.ClearJournal()
    API.Msg("[self AddToPack %s" % cls)
    it = wait_item(statuette, 10)
    if not check(it is not None, "%s: the statuette 0x%X is in the backpack" % (name, statuette)):
        continue
    API.UseObject(it.Serial)
    worn = mount_layer(8)
    if not check(worn is not None and worn.Graphic == mount, "%s: ridden, mount item 0x%X" % (name, mount)):
        say("%s: mount layer %s" % (name, worn.Graphic if worn is not None else None))
        continue
    check(worn.Hue == 0, "%s: solid (hue %d)" % (name, worn.Hue))
    shot("%s-1-ridden" % name)
    for step in ("east", "east", "south", "south"):
        API.Walk(step)
        API.Pause(0.4)
    shot("%s-2-walked" % name, 0.2)
    API.Dismount()
    API.Pause(1.5)
    back = wait_item(statuette, 6)
    check(API.FindLayer("Mount") is None and back is not None, "%s: dismounted, the statuette is back" % name)
    if back is not None:
        API.Msg("[delete")
        if API.WaitForTarget("any", 4):
            API.Target(back.Serial)
    API.Pause(1)

with open(SIG, "a") as f:
    f.write("END\n")
say("done")
