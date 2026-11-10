# cc-P867 (P864's review of P855, items 2 and 3): the wall-backed decor pieces placed by a player in their own house,
# against the wall each facing names, in TazUO on the private proof shard (main, the SoS New Haven).
# Staff hands (stage867.py, the CMD/ACK file channel) place OSI's large brick house on open grass east
# of the town and make the trainee its owner, then hand the trainee one deed per piece. The trainee double-clicks each
# deed, picks the facing in the deed's window, and targets the floor tile the plan names (plan867.py); a shot from the
# default camera inside the room after each round; staff clear the round before the next.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Hearth"
PHASE = "p867"

# from plan867.py (python -P plan867.py), unchanged
MAP = "Felucca"
HOUSE = (1227, 1353, 0)
ROUNDS = [
    ('grey-fireplace-small-east', [('grey-fireplace-small-east', 'east', 1229, 1341, 19, 'owner')], (1233, 1344, 19)),
    ('grey-fireplace-small-south', [('grey-fireplace-small-south', 'south', 1223, 1340, 19, 'owner')], (1227, 1344, 19)),
    ('grey-fireplace-low-east', [('grey-fireplace-low-east', 'east', 1229, 1342, 19, 'staff')], (1233, 1344, 19)),
    ('grey-fireplace-low-south', [('grey-fireplace-low-south', 'south', 1224, 1340, 19, 'owner')], (1227, 1344, 19)),
    ('grey-fireplace-medium-east', [('grey-fireplace-medium-east', 'east', 1230, 1342, 19, 'staff')], (1233, 1344, 19)),
    ('grey-fireplace-medium-south', [('grey-fireplace-medium-south', 'south', 1224, 1341, 19, 'owner')], (1227, 1344, 19)),
    ('grey-fireplace-large-south', [('grey-fireplace-large-south', 'south', 1225, 1341, 19, 'owner')], (1227, 1344, 19)),
    ('grey-fireplace-grand-south', [('grey-fireplace-grand-south', 'south', 1225, 1341, 19, 'owner')], (1227, 1344, 19)),
    ('country-kitchen-east', [('country-kitchen-east', 'east', 1229, 1342, 19, 'staff')], (1233, 1344, 19)),
    ('country-kitchen-south', [('country-kitchen-south', 'south', 1224, 1340, 19, 'owner')], (1227, 1344, 19)),
    ('small-kitchen-northwest', [('small-kitchen-northwest', 'northwest', 1223, 1347, 19, 'staff')], (1233, 1351, 19)),
    ('small-kitchen-southeast', [('small-kitchen-southeast', 'southeast', 1226, 1343, 19, 'staff')], (1227, 1344, 19)),
    ('harpsichord-east', [('harpsichord-east', 'east', 1223, 1340, 19, 'owner')], (1227, 1344, 19)),
    ('harpsichord-south', [('harpsichord-south', 'south', 1223, 1341, 19, 'owner')], (1227, 1344, 19)),
    ('blue-couch-east', [('blue-couch-east', 'east', 1229, 1342, 19, 'staff')], (1233, 1344, 19)),
    ('blue-couch-south', [('blue-couch-south', 'south', 1224, 1340, 19, 'owner')], (1227, 1344, 19)),
    ('holiday-fireplace', [('holiday-fireplace', 'south', 1224, 1341, 19, 'staff')], (1227, 1344, 19)),
]
# the house (plan867.py): deed, house class, centre
HOUSE_DEED, HOUSE_TYPE, CENTRE = "BrickHouseDeed", "guildhouse", (1228, 1346)
# each group's facings in the deed window's order (ShardDecorDesigns.Facings: keys, ordinal); button = index + 1
FACINGS = {
    "grey-fireplace-small": ["east", "south"], "grey-fireplace-low": ["east", "south"],
    "grey-fireplace-medium": ["east", "south"], "grey-fireplace-large": ["east", "south"],
    "grey-fireplace-grand": ["east", "south"],
    "country-kitchen": ["east", "south"], "harpsichord": ["east", "south"],
    "blue-couch": ["east", "north", "south", "west"], "small-kitchen": ["northwest", "southeast"],
    "holiday-fireplace": ["south"],
}
STAND = (1233, 1351, 19)    # the south room's south-east corner: where the trainee first stands
CLEAR_AT = (1228, 1343, 19)  # [DecorAddon clear takes the data addons within 6 tiles (both north rooms)
DEED_ART = 0x14F0


def say(text):
    API.SysMsg("P867: " + text)
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


def stage(line, seconds=30):
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
    stage("go %d %d %d %s" % (x, y, z, MAP))
    API.Pause(3)
    close_all()
    say("at %d,%d,%d (wanted %d,%d,%d)" % (API.Player.X, API.Player.Y, API.Player.Z, x, y, z))


def end():
    with open(CMD, "a") as f:
        f.write("end" + chr(10))
    with open(SIG, "a") as f:
        f.write("END\n")
    API.Stop()


def deeds():
    return [i for i in (API.FindTypeAll(DEED_ART, API.Backpack) or [])]


def group_of(design, wall):
    for g in FACINGS:
        if design == g or design.startswith(g + "-"):
            return g
    return None


def place(design, ox, oy, oz):
    g = group_of(design, None)
    facing = design[len(g) + 1:] if design != g else FACINGS[g][0]
    before = set(d.Serial for d in deeds())
    stage("deed " + g)
    API.Pause(1.5)
    new = [d for d in deeds() if d.Serial not in before]
    if not check(len(new) == 1, "%s: a deed for %s in the pack" % (design, g)):
        return False
    deed = new[0]
    API.ClearJournal()
    API.UseObject(deed.Serial)
    API.Pause(2)
    if len(FACINGS[g]) > 1:
        API.ReplyGump(FACINGS[g].index(facing) + 1)
    if not check(API.WaitForTarget("any", 5), "%s: the placement cursor (facing %s)" % (design, facing)):
        return False
    API.Target(ox, oy, oz)
    API.Pause(2.5)
    gone = deed.Serial not in [d.Serial for d in deeds()]
    refused = API.InJournal("house that you own") or API.InJournal("cannot") or API.InJournal("blocked")
    return check(gone and not refused, "%s placed by the owner at %d,%d,%d (deed used: %s)" % (design, ox, oy, oz, gone))


if API.Player.Name != CHARACTER:
    API.SysMsg("P867: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s, main, %s" % (API.Player.Name, PHASE))
API.Pause(7)
close_all()
API.Pause(1)
close_all()
for d in ("East", "East"):   # a new character wakes lying down
    API.Walk(d)
    API.Pause(1)
stage("serial %x" % API.Player.Serial)
stage("blessed True")

try:
    stage("house %d %d %d %s %s %s %d %d" % (HOUSE + (MAP, HOUSE_DEED, HOUSE_TYPE) + CENTRE), 40)
    API.Pause(2)
    go(*STAND)
    check(API.Player.Z == STAND[2], "standing on the house's ground floor (z %d)" % API.Player.Z)
    shot("empty-room", 2.5, 2)
    # a few real steps in the room, to show it is the house's floor and walkable
    for d in ("North", "North", "West", "South", "South", "East"):
        API.Walk(d)
        API.Pause(0.6)
    say("after the steps: %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
    go(*STAND)
    for name, pieces, stand in ROUNDS:
        for design, facing, ox, oy, oz, who in pieces:
            if who == "owner":
                place(design, ox, oy, oz)
            else:   # no spot passes the door rule: staff stand it (no house rules), still against its wall
                stage("place %s %d %d %d" % (design, ox, oy, oz))
                say("%s stood by staff at %d,%d,%d (no spot passes the door rule)" % (design, ox, oy, oz))
        close_all()
        go(*stand)
        shot(name, 2.5, 2.5)
        stage("clear %d %d %d" % CLEAR_AT)
        stage("clear %d %d %d" % (1226, 1348, 19))
        API.Pause(1.5)
except Exception as e:
    say("FAIL script: %s" % e)
end()
