# cc-P872 (P858's Walk858.py, fix-up after the build review P868): also checks the wagon's roof is bare (no rune glyph,
# no vent near) and that the black cat now sits on the potion kegs on the south porch.
# cc-P858: the fortune teller's wagon and the lamps in TazUO on the private proof shard. A Player-account trainee; staff
# hands through stage858.py (the CMD/ACK file channel) force a festival season (the stall and the wagon go up, as on a
# season's first day), move the trainee, lay eleven lamps round a spot and set the night. The trainee walks up the
# wagon's stair to the porch and inside for real (API.Walk, each step's x,y,z logged), walks back down, then lights the
# lamps by double-click and one is turned by staff. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Lamps"
PHASE = "p872"

WAGON = (3647, 2632, 0)              # FestivalMarket.DefaultWagonAt
FOOT = (WAGON[0], WAGON[1] + 11, 0)   # the tile below the stair's bottom step (the stair is y +6..+9, its foot +10)
INSIDE_Y = WAGON[1] + 1               # inside the wagon, past the doorway at y +3
OVERVIEW = (3641, 2631, 0)            # on the grass between the stall and the wagon
LAMP_SPOT = (3658, 2630, 0)           # on the square east of the wagon
LAMP_TYPES = ["DragonLantern", "BirdLamp", "KoiLamp", "DragonEggLamp", "StainedGlassLamp", "TallAntiqueLamp",
              "TallModernLamp", "OrnateTableLamp", "DragonBrazier", "CandleTray", "JackLantern"]
LAMP_OFFSETS = [(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (-2, 0), (2, 0), (-2, 2), (-1, 2), (0, 2), (1, 2)]
# unlit (first look) and lit art of each, in LAMP_TYPES order
LAMP_ART = [(0x4C40, 0x4C41), (0x4C44, 0x4C45), (0x4C48, 0x4C49), (0x4C4C, 0x4C4D), (0x4C50, 0x4C51), (0x4C52, 0x4C53),
            (0x4C56, 0x4C57), (0x49C2, 0x49C1), (0x194E, 0x194D), (0x983E, 0x983F), (0x4694, 0x4691)]


def say(text):
    API.SysMsg("P872: " + text)
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


def pos():
    return (API.Player.X, API.Player.Y, API.Player.Z)


def walk_to_y(direction, target_y, label, shots):
    """Steps the client one tile at a time toward target_y, logging each step; shots maps a y to a shot name."""
    stuck = 0
    zs = []
    for _ in range(40):
        x, y, z = pos()
        zs.append(z)
        if y == target_y:
            break
        if y in shots:
            shot(shots.pop(y), settle=0.8, after=1.5)
        API.Walk(direction)
        API.Pause(0.9)
        nx, ny, nz = pos()
        say("%s step: %d,%d,%d -> %d,%d,%d" % (label, x, y, z, nx, ny, nz))
        if (nx, ny) == (x, y):
            stuck += 1
            if stuck >= 4:
                say("FAIL %s stuck at %d,%d,%d" % (label, x, y, z))
                break
        else:
            stuck = 0
    return zs


if API.Player.Name != CHARACTER:
    API.SysMsg("P872: not %s, nothing to do" % CHARACTER)
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
stage("festival winter", 60)
stage("wagon")

try:
    # 1. The stall and the wagon together.
    go(*OVERVIEW)
    parts = list(API.GetItemsOnGround(14, 0x0722) or [])
    check(len(parts) >= 8, "the wagon's stair stands near the stall (%d step pieces in view)" % len(parts))
    shot("stall-and-wagon")
    roof = []
    for g in (0x4862, 0x4856, 0x4844, 0x2419):
        roof.extend(API.GetItemsOnGround(18, g) or [])
    check(len(roof) == 0, "the wagon's roof is bare: no rune glyph or vent in view (%d found)" % len(roof))

    # 1b. cc-P872: the black cat now sits on the potion kegs on the south porch (3646,2636, z 31), beside the door.
    cats = [c for c in (API.GetItemsOnGround(14, 0x4689) or []) if (c.X, c.Y) == (3646, 2636)]
    check(len(cats) == 1 and cats[0].Z == 31, "the black cat sits on the porch kegs at 3646,2636,31 (%s)" % [(c.X, c.Y, c.Z) for c in cats])

    # 2. Up the stair for real, onto the porch and inside, then back down.
    go(*FOOT)
    shot("stair-foot")
    zs = walk_to_y("North", INSIDE_Y, "up", {WAGON[1] + 5: "porch"})
    x, y, z = pos()
    check(y == INSIDE_Y and z >= 17, "walked up the stair and inside: at %d,%d,%d" % (x, y, z))
    check(all(b - a <= 6 for a, b in zip(zs, zs[1:])), "every step up rose at most one stair step: %s" % zs)
    shot("inside")
    walk_to_y("South", FOOT[1], "down", {WAGON[1] + 7: "stair-going-down"})
    x, y, z = pos()
    check(y == FOOT[1] and abs(z) <= 2, "walked back down to the street: at %d,%d,%d" % (x, y, z))
    shot("down-again")

    # 3. The lamps: laid round a spot by staff, then the night, then lit one by one by the trainee.
    lx, ly, lz = LAMP_SPOT
    for t, (dx, dy) in zip(LAMP_TYPES, LAMP_OFFSETS):
        stage("addat %s %d %d %d" % (t, lx + dx, ly + dy, lz))
    go(*LAMP_SPOT)
    found = []
    for (unlit, lit) in LAMP_ART:
        found.extend(API.GetItemsOnGround(3, unlit) or [])
    check(len(found) == 11, "eleven lamps laid, all unlit (%d found)" % len(found))
    shot("lamps-day")
    stage("light 26")
    API.Pause(2)
    shot("lamps-night-unlit")
    for it in found:   # run 1: 0.6 s apart drew "You must wait to perform another action" five times
        API.UseObject(it.Serial)
        API.Pause(1.4)
    API.Pause(1.5)
    lit = []
    for (unlit, l) in LAMP_ART:
        lit.extend(API.GetItemsOnGround(3, l) or [])
    check(len(lit) == 11, "double-click lit all eleven (%d lit)" % len(lit))
    shot("lamps-night-lit")

    # 4. One lamp turned while lit (the decorator's path, by staff here): it keeps its light.
    lantern = list(API.GetItemsOnGround(3, 0x4C41) or [])
    if lantern:
        stage("flip %x" % lantern[0].Serial)
        API.Pause(1.5)
        check(len(list(API.GetItemsOnGround(3, 0x4C43) or [])) == 1, "the dragon lantern turned east and stayed lit")
        shot("lantern-turned")
    # And one put out again.
    jack = list(API.GetItemsOnGround(3, 0x4691) or [])
    if jack:
        API.UseObject(jack[0].Serial)
        API.Pause(1.2)
        check(len(list(API.GetItemsOnGround(3, 0x4694) or [])) == 1, "the jack-o-lantern goes out on a second double-click")
    stage("light clear")
except Exception as e:
    say("FAIL script: %s" % e)
end()
