# cc-P871 (P857's Walk857.py; the build review P866, item 2): every one of the six carpet styles laid NON-square in
# TazUO on the private proof shard, so a width/height or x/y swap would show. A Player-account trainee places a small
# stone house from a deed (so the trainee really owns it), then lays each style in turn with the carpet deed (as woven),
# 5 by 3 (x by y) and 3 by 4 alternately, checks that each of the four corner pieces stands on its own corner tile and
# that the middle count fits the size, takes a shot, and rolls it back up into the deed through the confirm.
# Staff hands through stage871.py (the CMD/ACK file channel) only hand over the deeds
# and move the trainee. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Carpet"
PHASE = "p871"

CX, CY = 1986, 2242            # the house's centre (StonePlasterHouseDeed: 7 by 7, door on the south wall at y+3)
STAND = (1986, 2250, 0)        # on the grass south of the plot
INSIDE = (1988, 2243, 7)       # inside, east of the carpet's area
# The house's floor is x 1984-1988, y 2240-2244 (multi 0x64, -2..2); the door at 1986,2245 keeps carpets off row 2244.
# (corner A, corner B, the floor tile IDs there, width, height): 5 by 3 along x, then 3 by 4 along y.
WIDE = ((1984, 2240), (1988, 2242), 0x04B4, 0x04AB, 5, 3)
DEEP = ((1984, 2240), (1986, 2243), 0x04B4, 0x04AB, 3, 4)
# The six styles' art as VariableCarpetSettings.Styles has it: map NW, NE, SE, SW corners, then the middle.
STYLES = [("blue patterned", 0xAC3, 0xAC5, 0xAC2, 0xAC4, 0xABD), ("blue plain", 0xAC3, 0xAC5, 0xAC2, 0xAC4, 0xABE),
          ("blue with gold", 0xAD3, 0xAD5, 0xAD2, 0xAD4, 0xAD1), ("red patterned", 0xACA, 0xACC, 0xAC9, 0xACB, 0xAC7),
          ("red plain", 0xACA, 0xACC, 0xAC9, 0xACB, 0xAC8), ("gold patterned", 0xADC, 0xADE, 0xADB, 0xADD, 0xADA)]
AS_WOVEN = 100


def say(text):
    API.SysMsg("P871: " + text)
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


def pack_item(word):
    for it in API.ItemsInContainer(API.Backpack, True) or []:
        text = (API.ItemNameAndProps(it.Serial, True, 2) or "").lower()
        if word in text:
            return it
    return None


def gump_with(text, seconds=6):
    for _ in range(seconds * 2):
        for g in API.GetAllGumps() or []:
            try:
                if API.GumpContains(text, g.ServerSerial):
                    return g.ServerSerial
            except Exception:
                pass
        API.Pause(0.5)
    return None


def target_tile(x, y, z, wait=True, graphic=0):
    if wait and not API.WaitForTarget("any", 6):
        say("FAIL no target cursor for %d,%d" % (x, y))
        return False
    if not wait:
        API.Pause(2.5)   # a house deed's cursor is a multi target, which WaitForTarget does not report
    API.Target(x, y, z, graphic)   # graphic 0: the ground; a floor tile's ID: that floor, as a click on it sends
    API.Pause(1.5)
    return True


def lay(deed, hue_button, style_button, a, b, z, ga=0, gb=0):
    """Double-click the deed, pick a colour (redraws the gump), then a style, then the two corners."""
    API.UseObject(deed.Serial)
    gid = gump_with("Choose a carpet")
    if not gid:
        say("FAIL no carpet gump")
        return None
    API.ReplyGump(hue_button, gid)
    API.Pause(1.5)
    gid = gump_with("Choose a carpet")
    if not gid:
        say("FAIL no carpet gump after the colour")
        return None
    API.ReplyGump(style_button, gid)
    API.Pause(1)
    target_tile(a[0], a[1], z, graphic=ga)
    target_tile(b[0], b[1], z, graphic=gb)
    API.Pause(1.5)
    return True




def at(graphic, x, y):
    for it in API.GetItemsOnGround(10, graphic) or []:
        if it.X == x and it.Y == y:
            return True
    return False


if API.Player.Name != CHARACTER:
    API.SysMsg("P871: not %s, nothing to do" % CHARACTER)
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
    stage("pack StonePlasterHouseDeed")
    stage("pack VariableCarpetDeed")
    API.Pause(2)
    house_deed = pack_item("plaster")
    check(house_deed is not None and pack_item("carpet deed") is not None, "both deeds in the pack")

    # The trainee places the house: it is the trainee's own.
    API.UseObject(house_deed.Serial)
    API.Pause(2.5)
    API.Target(CX, CY + 4, 0, 0)
    API.Pause(4)
    stage("house")
    check(pack_item("plaster") is None, "the house deed is used: the house stands at %d,%d" % (CX, CY))

    go(*INSIDE)
    z = API.Player.Z
    for i, (name, nw, ne, se, sw, middle) in enumerate(STYLES):
        (a, b, ga, gb, w, h) = WIDE if i % 2 == 0 else DEEP
        deed = pack_item("carpet deed")
        if deed is None:
            check(False, "%s: no carpet deed in the pack" % name)
            break
        API.ClearJournal()
        lay(deed, AS_WOVEN, i + 1, a, b, z, ga, gb)
        x0, y0, x1, y1 = a[0], a[1], b[0], b[1]
        corners = [("NW", nw, x0, y0), ("NE", ne, x1, y0), ("SE", se, x1, y1), ("SW", sw, x0, y1)]
        placed = [c for c in corners if at(c[1], c[2], c[3])]
        mids = [m for m in (API.GetItemsOnGround(10, middle) or []) if x0 < m.X < x1 and y0 < m.Y < y1]
        check(len(placed) == 4, "%s %d by %d: the four corners on their own tiles (%s)" % (
            name, w, h, ", ".join("%s 0x%X at %d,%d" % (c[0], c[1], c[2], c[3]) for c in placed)))
        check(len(mids) == (w - 2) * (h - 2), "%s %d by %d: %d middle tiles inside the border (%d wanted)" % (
            name, w, h, len(mids), (w - 2) * (h - 2)))
        stage("house")
        shot("%d-%s-%dx%d" % (i, name.replace(" ", "-"), w, h))
        # roll it up again through the confirm, for the next style
        any_piece = [c for c in (API.GetItemsOnGround(10, nw) or []) if c.X == x0 and c.Y == y0]
        if any_piece:
            API.UseObject(any_piece[0].Serial)
            gid = gump_with("Roll up this carpet")
            if gid:
                API.ReplyGump(1, gid)
                API.Pause(2)
        check(pack_item("carpet deed") is not None and not at(nw, x0, y0), "%s: rolled back up into the deed" % name)
except Exception as e:
    say("FAIL script: %s" % e)
end()
