# cc-P795: the Drover's Handbook in TazUO on the private proof shard. A new character on the Golem's admin account goes to the
# Trinsic road meadow (wild peacocks, P793), gets the book and the three scrolls in the pack, fills the book, and casts all four
# pages on real wild animals. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Drover"
BIRD = 1440
BOOK = 0x0FEF
SCROLL = 0x0E34
MEADOW = (1986, 2244, 0)


def say(text):
    API.SysMsg("P795: " + text)
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


def birds(dist=22):
    for _ in range(40):
        found = API.GetAllMobiles(BIRD, dist)
        if found:
            return found
        API.Pause(0.5)
    return []


def wait_journal(text, seconds):
    for _ in range(int(seconds * 2)):
        if API.InJournal(text):
            return True
        API.Pause(0.5)
    return False


def in_pack(graphic):
    return API.FindType(graphic, API.Backpack)


def cast(command, serial):
    API.ClearJournal()
    API.Msg(command)
    if not API.WaitForTarget("any", 6):
        say("no target cursor for " + command)
        return False
    API.Target(serial)
    return True


if API.Player.Name != CHARACTER:
    API.SysMsg("P795: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)

API.Pause(7)
close_all()

API.Msg("[self set Blessed True")
API.Pause(1)
API.Msg("set herding 100")
API.Pause(1)
API.Msg("[self set Map Trammel")
API.Pause(1)
API.Msg("[self set Location (%d,%d,%d)" % MEADOW)
API.Pause(5)
say("at %d,%d" % (API.Player.X, API.Player.Y))
check(abs(API.Player.X - MEADOW[0]) < 3 and abs(API.Player.Y - MEADOW[1]) < 3, "the character is on the meadow")
close_all()

# The book and the pages, in the pack.
for name in ("DroversHandbook", "CalmScroll", "HerdScroll", "LureScroll"):
    API.Msg("[self addtopack " + name)
    API.Pause(1.5)
API.UseObject(API.Backpack)
API.Pause(2)
book = in_pack(BOOK)
check(book is not None, "the book is in the pack, art 0x0FEF")
if book is None:
    with open(SIG, "a") as f:
        f.write("SHOT 0-no-book\nEND\n")
    API.Stop()
shot("1-book-and-scrolls-in-pack")

API.UseObject(book.Serial)
API.Pause(2)
shot("2-gump-corral-only")
close_all()

for _ in range(3):
    scroll = in_pack(SCROLL)
    if scroll is None:
        break
    API.MoveItem(scroll.Serial, book.Serial)
    API.Pause(1.5)
check(in_pack(SCROLL) is None, "the three scrolls went into the book")
API.UseObject(book.Serial)
API.Pause(2)
shot("3-gump-all-four-pages")
close_all()

found = birds()
check(len(found) > 0, "a wild peacock is on the meadow")
if not found:
    with open(SIG, "a") as f:
        f.write("SHOT 0-no-peacock\nEND\n")
    API.Stop()
bird = found[0]
API.Pathfind(bird.X, bird.Y, distance=3, wait=True, timeout=20)

cast("[Corral", bird.Serial)
check(wait_journal("easier for your next taming", 5), "Corral on a wild peacock")
shot("4-corral", 0.3, 1.0)
API.Pause(2)

cast("[Calm", bird.Serial)
check(wait_journal("You calm", 5), "Calm on a wild peacock")
shot("5-calm", 0.3, 1.0)
API.Pause(2)

# Herd: the bird, then a spot 6 tiles off.
x, y = API.Player.X + 6, API.Player.Y
API.ClearJournal()
cast("[Herd", bird.Serial)
API.Pause(1)
got = API.WaitForTarget("any", 6)
check(got, "Herd asks for a spot")
API.Target(x, y, API.Player.Z)
check(wait_journal("walk where you pointed", 5), "Herd sends the flock")
shot("6-herd-a", 0.5, 0.3)
API.Pause(3)
shot("6-herd-b", 0.2, 0.5)
near = API.FindMobile(bird.Serial)
if near is not None:
    say("herded bird at %d,%d, spot %d,%d" % (near.X, near.Y, x, y))
    check(abs(near.X - x) + abs(near.Y - y) < 6, "the herded bird walked to the spot")
API.Pause(2)

# Lure: stand about 11 tiles from the bird, then pull it over.
near = API.FindMobile(bird.Serial)
API.Pathfind(near.X - 11, near.Y, distance=1, wait=True, timeout=20)
API.Pause(1)
near = API.FindMobile(bird.Serial)
far = near.Distance if near is not None else -1
say("bird %d tiles off before Lure" % far)
cast("[Lure", bird.Serial)
check(wait_journal("walks where it was instructed", 5), "Lure on a wild peacock")
shot("7-lure-a", 0.5, 0.3)
API.Pause(8)
near = API.FindMobile(bird.Serial)
now = near.Distance if near is not None else -1
say("bird %d tiles off after Lure" % now)
check(0 <= now < far, "the lured bird came closer")
shot("7-lure-b", 0.2, 1.0)

say("done")
with open(SIG, "a") as f:
    f.write("END\n")
API.Stop()
