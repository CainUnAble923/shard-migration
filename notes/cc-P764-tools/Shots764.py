# cc-P764 (P769's Shots769.py, rewritten): the pet leash in TazUO on the private proof shard. A new character on the
# Golem's admin account takes a pet choice scroll ([self AddToPack), picks the dog (the leash comes with it), leashes
# the dog, and calls it back out. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API
import time

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Leash"
SCROLL, LEASH, FIGURINE, DOG_BODY = 0x0E34, 0x1374, 0x2588, 0xD9


def say(text):
    API.SysMsg("P764: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=2.0):
    API.Pause(settle)
    with open(SIG, "a") as f:
        f.write("SHOT " + name + "\n")
    API.Pause(2.5)


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    return ok


def gumps():
    out = []
    for g in API.GetAllGumps():
        try:
            t = g.PacketGumpText or ""
        except Exception:
            t = ""
        out.append((g, t))
    return out


def gump_id(g):
    for obj in (g, getattr(g, "Gump", None)):
        for attr in ("ServerSerial", "GumpID", "ID"):
            try:
                v = getattr(obj, attr)
                if v:
                    return int(v)
            except Exception:
                pass
    return None


def wait_gump(text, seconds):
    for _ in range(int(seconds * 2)):
        for g, t in gumps():
            if text in t:
                return g
        API.Pause(0.5)
    return None


def close_all():
    for g, t in gumps():
        if t:
            try:
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


def my_dog(seconds):
    for _ in range(int(seconds * 2)):
        found = API.GetAllMobiles(DOG_BODY, 6)
        if found:
            return found[0]
        API.Pause(0.5)
    return None


if API.Player.Name != CHARACTER:
    API.SysMsg("P764: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)

# Up off the beach (the wake lesson), and the lesson window out of the way.
API.Pause(7)
API.Walk("South")
API.Pause(2)
close_all()

# The pet choice scroll, as a moongate skipper gets it, and the dog.
API.Msg("[self AddToPack PetChoiceScroll")
scroll = wait_item(SCROLL, 10)
if check(scroll is not None, "the pet choice scroll is in the backpack"):
    API.UseObject(scroll.Serial)
    g = wait_gump("Choose your pet", 10)
    if check(g is not None, "the pet choice window"):
        gid = gump_id(g)
        if gid:
            API.ReplyGump(1, gid)
        else:
            API.ReplyGump(1)
leash = wait_item(LEASH, 10)
check(leash is not None, "the scroll gave a leash")
dog = my_dog(10)
check(dog is not None, "the dog is here")
API.UseObject(API.Backpack)
shot("1-dog-and-leash", 2.0)

# Leash the dog: the figurine in the backpack.
if leash is not None and dog is not None:
    API.UseObject(leash.Serial)
    if check(API.WaitForTarget("any", 5), "the leash asks for a target"):
        API.Target(dog.Serial)
fig = wait_item(FIGURINE, 10)
check(fig is not None, "a dog figurine is in the backpack")
check(API.InJournal("shrinks into a figurine"), "the shrink line")
API.UseObject(API.Backpack)
shot("2-shrunk-dog-figurine", 2.0)

# Call the dog back out.
if fig is not None:
    API.UseObject(fig.Serial)
check(my_dog(10) is not None, "the dog is back")
check(API.InJournal("comes out of the figurine"), "the restore line")
shot("3-restored-dog", 2.0)

with open(SIG, "a") as f:
    f.write("END\n")
say("done")
