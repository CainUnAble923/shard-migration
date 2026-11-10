# cc-P867 (P864's review of P855, item 2): every wall-backed decor piece stood against the wall its facing names, in
# real New Haven buildings on main (SoS Trammel), shot from the default camera in TazUO on the private proof shard.
# Staff hands (stage867.py, the CMD/ACK file channel) stand each design with [DecorAddon place at the spot town867.py
# found (on the floor, back row against a full plain wall, clear of windows, protected tiles and clutter), the trainee
# stands south-east of it in the same room for the shot, then staff clear it. The player's own placement from a deed
# inside a house they own is run 4's (notes; its logs are in notes/cc-P867-tools/run4).
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Hearth"
PHASE = "p867"

# from town867.py (python -P town867.py > town-out.txt), unchanged: (design, facing, x, y, z, stand)
TOWN = [
    ('grey-fireplace-small-east', 'east', 3624, 2573, 0, (3627, 2579, 0)),
    ('grey-fireplace-small-south', 'south', 3620, 2610, 0, (3624, 2615, 0)),
    ('grey-fireplace-low-east', 'east', 3624, 2572, 0, (3630, 2575, 0)),
    ('grey-fireplace-low-south', 'south', 3583, 2583, 0, (3585, 2589, 0)),
    ('grey-fireplace-medium-east', 'east', 3625, 2572, 0, (3631, 2575, 0)),
    ('grey-fireplace-medium-south', 'south', 3619, 2611, 0, (3624, 2615, 0)),
    ('grey-fireplace-large-east', 'east', 3625, 2572, 0, (3631, 2575, 0)),
    ('grey-fireplace-large-south', 'south', 3583, 2584, 0, (3585, 2590, 0)),
    ('grey-fireplace-grand-east', 'east', 3625, 2572, 0, (3631, 2575, 0)),
    ('grey-fireplace-grand-south', 'south', 3583, 2584, 0, (3585, 2590, 0)),
    ('country-kitchen-east', 'east', 3624, 2572, 0, (3630, 2575, 0)),
    ('country-kitchen-south', 'south', 3583, 2583, 0, (3585, 2589, 0)),
    ('small-kitchen-northwest', 'northwest', 3667, 2593, 0, (3673, 2598, 0)),
    ('small-kitchen-southeast', 'southeast', 3610, 2578, 0, (3611, 2579, 0)),
    ('harpsichord-east', 'east', 3625, 2573, 0, (3631, 2575, 0)),
    ('harpsichord-south', 'south', 3620, 2611, 0, (3624, 2615, 0)),
    ('blue-couch-east', 'east', 3624, 2572, 0, (3630, 2575, 0)),
    ('blue-couch-south', 'south', 3583, 2583, 0, (3585, 2589, 0)),
    ('holiday-fireplace', 'south', 3582, 2584, 0, (3585, 2590, 0)),
]


def say(text):
    API.SysMsg("P867: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=2.0, after=2.5):
    API.Pause(settle)
    with open(SIG, "a") as f:
        f.write("SHOT " + PHASE + "-" + name + "\n")
    API.Pause(after)


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
    stage("go %d %d %d Trammel" % (x, y, z))
    API.Pause(3)
    close_all()
    ok = (API.Player.X, API.Player.Y) == (x, y)
    say("%s at %d,%d,%d (wanted %d,%d,%d)" % ("PASS" if ok else "FAIL", API.Player.X, API.Player.Y, API.Player.Z, x, y, z))


def end():
    with open(CMD, "a") as f:
        f.write("end" + chr(10))
    with open(SIG, "a") as f:
        f.write("END\n")
    API.Stop()


if API.Player.Name != CHARACTER:
    API.SysMsg("P867: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s, main, %s (town run)" % (API.Player.Name, PHASE))
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
    for design, facing, x, y, z, stand in TOWN:
        stage("clear %d %d %d" % (x, y, z))
        stage("place %s %d %d %d" % (design, x, y, z))
        say("%s (faces %s) stood by staff at %d,%d,%d" % (design, facing, x, y, z))
        go(*stand)
        shot(design, 2.5, 2.5)
        stage("clear %d %d %d" % (x, y, z))
except Exception as e:
    say("FAIL script: %s" % e)
end()
