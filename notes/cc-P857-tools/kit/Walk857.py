# cc-P857: the carpet deed in TazUO on the private proof shard. A Player-account trainee places a small stone house from
# a deed on open grass (so the trainee really owns it), then uses a carpet deed: the gump, a colour, a refusal outside the
# house, a 4 by 4 carpet laid with two corner targets inside, the removal confirm, the roll-up back into a deed, and a
# second carpet in another style. Staff hands through stage857.py (the CMD/ACK file channel) only hand over the deeds
# and move the trainee. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Carpet"
PHASE = "p857"

CX, CY = 1986, 2242            # the house's centre (StonePlasterHouseDeed: 7 by 7, door on the south wall at y+3)
STAND = (1986, 2250, 0)        # on the grass south of the plot
INSIDE = (1988, 2243, 7)       # inside, east of the carpet's area
CARPET_A, CARPET_B = (1984, 2240), (1987, 2243)   # 4 by 4, clear of the door
FLOOR_A, FLOOR_B = 0x04B4, 0x04A9                 # the house floor tiles there (multi 0x64 at -2,-2 and 1,1, z 7)
OUT_A, OUT_B = (1991, 2247), (1993, 2249)         # on the grass outside: refused
RED_MIDDLE, BLUEGOLD_MIDDLE = 0xAC7, 0xAD1


def say(text):
    API.SysMsg("P857: " + text)
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


if API.Player.Name != CHARACTER:
    API.SysMsg("P857: not %s, nothing to do" % CHARACTER)
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
    carpet_deed = pack_item("carpet deed")
    check(house_deed is not None and carpet_deed is not None, "both deeds in the pack")
    if carpet_deed is not None:
        props = (API.ItemNameAndProps(carpet_deed.Serial, True, 2) or "")
        check("Milva" in props, "the carpet deed names its authors: " + props.replace("\n", " | "))

    # 1. The trainee places the house: it is the trainee's own.
    API.ClearJournal()
    API.UseObject(house_deed.Serial)
    API.Pause(2.5)
    say("house cursor up: %s" % API.HasTarget())
    API.Target(CX, CY + 4, 0, 0)
    API.Pause(4)
    for phrase in ("placement cancellation", "could not be created", "cannot be created in this area",
                   "already own a house", "foundation", "no build", "must be in your pack", "deed for this plot"):
        if API.InJournal(phrase):
            say("house journal: " + phrase)
    say("house cursor after: %s" % API.HasTarget())
    stage("house")
    placed = pack_item("plaster") is None
    check(placed, "the house deed is used: the house stands at %d,%d" % (CX, CY))
    if not placed:
        shot("house-refused")

    # 2. The gump, then a colour: the previews redraw in that colour.
    API.UseObject(carpet_deed.Serial)
    gid = gump_with("Choose a carpet")
    check(gid is not None, "the carpet gump opens")
    shot("gump")
    API.ReplyGump(103, gid)   # Wine
    API.Pause(1.5)
    gid = gump_with("Choose a carpet")
    check(gid is not None, "a colour button redraws the gump")
    shot("gump-wine")
    close_all()

    # 3. Outside the house: refused, the deed kept.
    API.ClearJournal()
    lay(carpet_deed, 103, 4, OUT_A, OUT_B, 0)
    check(API.InJournal("house that you own") is True, "outside the house: refused")
    check(pack_item("carpet deed") is not None, "the deed is kept after the refusal")
    shot("refused-outside")

    # 4. Inside: a 4 by 4 red patterned carpet in wine.
    go(*INSIDE)
    z = API.Player.Z
    API.ClearJournal()
    lay(carpet_deed, 103, 4, CARPET_A, CARPET_B, z, FLOOR_A, FLOOR_B)
    middles = list(API.GetItemsOnGround(6, RED_MIDDLE) or [])
    check(len(middles) == 4, "laid: %d middle tiles (4 for 4 by 4)" % len(middles))
    check(pack_item("carpet deed") is None, "the deed is used up")
    check(API.InJournal("roll it up again") is True, "the server says it is laid")
    stage("house")
    shot("carpet-laid")

    # 5. The removal confirm, then yes: rolled up into a deed.
    if middles:
        API.UseObject(middles[0].Serial)
        gid = gump_with("Roll up this carpet")
        check(gid is not None, "double-clicking the carpet asks first")
        shot("remove-confirm")
        if gid:
            API.ReplyGump(1, gid)
            API.Pause(2)
    left = list(API.GetItemsOnGround(6, RED_MIDDLE) or [])
    check(len(left) == 0, "rolled up: %d middle tiles left" % len(left))
    carpet_deed = pack_item("carpet deed")
    check(carpet_deed is not None, "a carpet deed is back in the pack")
    shot("rolled-up")

    # 6. The same deed again: blue with gold, as woven.
    if carpet_deed is not None:
        lay(carpet_deed, 100, 3, CARPET_A, CARPET_B, z, FLOOR_A, FLOOR_B)
        blue = list(API.GetItemsOnGround(6, BLUEGOLD_MIDDLE) or [])
        check(len(blue) == 4, "a second carpet, blue with gold: %d middle tiles" % len(blue))
        stage("house")
        shot("carpet-blue-gold")
except Exception as e:
    say("FAIL script: %s" % e)
end()
