# cc-P769 (P740's IsleWalk740.py, cut down): a brand-new character's first minutes on the Wakening Isle in TazUO, with a
# shot of each changed lesson text: the wake hint (how to get up), the first lesson's window with its tip, "lesson" said
# aloud reopening the window, and the backpack lesson's new steps. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API
import time

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Paige"
FINISHED = "Lesson finished"
BLUE_TILE, GOLD_TILE = (6646, 3992), (6649, 3992)
CAMP = (6656, 3990)


def say(text):
    API.SysMsg("P769: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=2.0):
    API.Pause(settle)
    with open(SIG, "a") as f:
        f.write("SHOT " + name + "\n")
    API.Pause(2.5)


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


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


def find_gump(text):
    for g, t in gumps():
        if text in t:
            return g
    return None


def wait_gump(text, seconds):
    for _ in range(int(seconds * 2)):
        g = find_gump(text)
        if g is not None:
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


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    return ok


def go(xy, dist=0):
    for _ in range(3):
        API.Pathfind(xy[0], xy[1], distance=dist, wait=True, timeout=30)
        p = where()
        if abs(p[0] - xy[0]) <= dist and abs(p[1] - xy[1]) <= dist:
            return True
        API.Pause(1.0)
    return False


if API.Player.Name != CHARACTER:
    API.SysMsg("P769: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s at %s" % (API.Player.Name, where()))
T0 = time.time()

# 1. the wake: the hint says how to get up
while time.time() - T0 < 7:
    API.Pause(0.25)
check(API.InJournal("right mouse button"), "the wake hint says how to get up")
shot("1-wake-hint", 0.1)
API.Turn("south")
for _ in range(40):
    if find_gump("Walk and run") is not None:
        break
    API.Pause(0.5)

# 3. the first lesson's window, with its tip
check(wait_gump("Walk and run", 20) is not None, "the first lesson's window")
check(wait_gump("Tip:", 2) is not None, "the lesson window has a tip")
shot("3-movement-lesson-tip", 1.0)

# 4. "lesson" said aloud opens the window again
close_all()
API.Pause(1.0)
check(find_gump("Walk and run") is None, "the lesson window is closed")
API.Msg("lesson")
check(wait_gump("Walk and run", 8) is not None, "saying lesson opened it again")
shot("4-lesson-said-aloud", 1.0)

# 2. the backpack lesson's steps
go(BLUE_TILE, 0)
API.Pause(1.5)
go(GOLD_TILE, 0)
g = wait_gump(FINISHED, 15)
if check(g is not None, "the movement lesson finished"):
    gid = gump_id(g)
    if gid:
        API.ReplyGump(1, gid)
    else:
        API.ReplyGump(1)
check(wait_gump("Open Paperdoll", 15) is not None, "the backpack lesson names Open Paperdoll")
shot("2-backpack-lesson-steps", 1.0)
API.Pause(1.0)
with open(SIG, "a") as f:
    f.write("END\n")
say("done")
