# cc-P740 run 2: IsleWalk740.py (as now made) cut after the wake: the wake checked again with the server-window count.
# cc-P740 (P733's, with P740's wake and bandages): a real character plays the isle's new steps in TazUO (the client's own movement, gumps, drags and
# commands; no teleport): the first login's wake, the cloak chest, Wren's pitchfork, war mode, the pests, the pet
# reward, Pet Info from the pet's menu, the healing lesson with Pip in the farmhouse, then the dock both ways.
# Each step goes to the journal and to LOG; "SHOT <name>" lines in SIG ask the runner (tazuo-walk.ps1) for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"

FINISHED = "Lesson finished"
TAMSIN = (6640, 3992)
BLUE_TILE, GOLD_TILE = (6646, 3992), (6649, 3992)
CAMP, TABLE, SIGN = (6656, 3990), (6664, 3990), (6692, 3990)
WREN, BELOW_WREN, PESTS = (6714, 3978), (6714, 3979), (6702, 3978)
PIP = (6692, 3975)
STEPS = (6690, 3980)
PET_INFO_ENTRY = 11   # the pet's context menu, entry 11 (cliloc 1900017), read by pet_menu_probe.py


def say(text):
    API.SysMsg("P740: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=2.0, clear=False):
    if clear:  # run 8: the windows hid what the facing check looks at; they come back with the next server message
        for g, _ in gumps():
            try:
                g.Dispose()
            except Exception:
                pass
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


def gump_ids(g):
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


def log_gumps(label):
    gs = gumps()
    say("%s: %d server gumps" % (label, len(gs)))
    for g, t in gs:
        say("   gump %s: %s" % (gump_ids(g), t[:160].replace("\n", " ")))


def wait_gump(text, seconds):
    for _ in range(int(seconds * 2)):
        g = find_gump(text)
        if g is not None:
            return g
        API.Pause(0.5)
    return None


def reply(text, button, seconds=10):
    g = wait_gump(text, seconds)
    if g is None:
        say("no gump with %r" % text)
        return False
    gid = gump_ids(g)
    say("reply %d to gump %s (%r)" % (button, gid, text))
    if gid:
        API.ReplyGump(button, gid)
    else:
        API.ReplyGump(button)
    API.Pause(1.0)
    return True


def wait_journal(text, seconds):
    for _ in range(int(seconds * 2)):
        if API.InJournal(text):
            return True
        API.Pause(0.5)
    return False


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    return ok


def go(xy, dist=0, what=""):
    # run 5: TazUO's Pathfind gave up on every target more than about 10 tiles off, so walk legs of at most 8 tiles
    for _ in range(12):
        p = where()
        dx, dy = xy[0] - p[0], xy[1] - p[1]
        n = max(abs(dx), abs(dy))
        if n <= 8:
            break
        k = 8.0 / n
        API.Pathfind(p[0] + int(round(dx * k)), p[1] + int(round(dy * k)), distance=1, wait=True, timeout=20)
        if where() == p:
            API.Walk(("east" if dx > 0 else "west") if abs(dx) >= abs(dy) else ("south" if dy > 0 else "north"))
            API.Pause(0.6)
    for _ in range(3):
        API.Pathfind(xy[0], xy[1], distance=dist, wait=True, timeout=30)
        p = where()
        if abs(p[0] - xy[0]) <= max(dist, 0) and abs(p[1] - xy[1]) <= max(dist, 0):
            break
        API.Pause(1.0)
    p = where()
    return check(abs(p[0] - xy[0]) <= dist + 1 and abs(p[1] - xy[1]) <= dist + 1,
                 "walked to %s %s (at %s)" % (what, xy, p))


def mobiles_near(xy, r, graphics=None, name=None):
    out = []
    for m in API.GetAllMobiles():
        try:
            if m.Serial == API.Player.Serial:
                continue
            if abs(m.X - xy[0]) > r or abs(m.Y - xy[1]) > r:
                continue
            if graphics and m.Graphic not in graphics:
                continue
            if name and name not in (m.Name or ""):
                continue
            out.append(m)
        except Exception:
            pass
    return out


def steps(direction, n):
    for _ in range(n):
        API.Walk(direction)
        API.Pause(0.6)
        say("  %s -> %s" % (direction, where()))


def next_lesson():
    if wait_gump(FINISHED, 15) is None:
        check(False, "the lesson finished")
        return False
    check(True, "the lesson finished")
    return reply(FINISHED, 1)


# -- 0. first login: only the wake scene, lying until the first move -------------------------------------------------
CHARACTER = "Iron Ember"   # the brand-new character TazUO creates (ui.ps1); any other character: do nothing
if API.Player.Name != CHARACTER:
    API.SysMsg("P740: not %s, the walk does not run" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s, %s" % (API.Player.Name, where()))
import time
T0 = time.time()
UP = "You wake on a quiet shore"
for t, name in ((2, "lying-02"), (5, "lying-05"), (10, "lying-10")):
    while time.time() - T0 < t:
        API.Pause(0.25)
    say("%s: at %s, %d server windows, up: %s" % (name, where(), len(gumps()), API.InJournal(UP)))
    shot(name, 0.1)
check(not API.InJournal(UP), "still down 10 s in, without moving")
say("over the head: You lie on the wet sand... (TazUO keeps an overhead line off the journal: see the lying-02 shot)")
check(API.InJournal("Move to get up"), "Move to get up. (by %d s)" % int(time.time() - T0))
check(len([1 for _, t in gumps() if t]) == 0, "no server window while lying")
start = where()
t1 = time.time()
API.Turn("south")
with open(SIG, "a") as f:
    f.write("BURST getting-up 14 400\n")
up_after, first_gump = None, None
while time.time() - t1 < 15:
    if first_gump is None and len([1 for _, t in gumps() if t]) > 0:   # run 1: the quest arrow is a gump without text
        first_gump = time.time() - t1
    if up_after is None and API.InJournal(UP):
        up_after = time.time() - t1
    if up_after is not None and first_gump is not None:
        break
    API.Pause(0.2)
say("after the turn: first lines at %s s, first server window at %s s" % (
    None if up_after is None else round(up_after, 1), None if first_gump is None else round(first_gump, 1)))
check(up_after is not None and 3.5 <= up_after <= 9, "the first lines come after the get-up and the dawn (%s s after the turn)" % (None if up_after is None else round(up_after, 1)))
check(first_gump is not None and up_after is not None and first_gump >= up_after + 1.5, "no window before they are up and the light is back; the windows %s s after the lines" % (None if first_gump is None or up_after is None else round(first_gump - up_after, 1)))
check(where()[:2] == start[:2], "they stay on their tile (%s, was %s)" % (where(), start))
shot("up-day", 0.5)
API.Pause(2.0)
log_gumps("stood up")
shot("up-wreck-beach", 0.5, clear=True)

say("end of the wake (run 2)")
with open(SIG, "a") as f:
    f.write("END" + chr(10))
