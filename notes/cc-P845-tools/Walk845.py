# cc-P845 (P823's Clear823.py, P806's Walk806Main.py): on the private proof shard, close the login windows, list the farmhouse's
# bench, blood and healing sign as the client sees them, and, when the tester starts on the road, walk him for real (no
# teleport) from the road (6702,3983 only) up the steps, through the door and to Pip's side, logging each leg. The shot runner takes the
# shot after its settle time, with the tester where this script left him.
import API

LOG = r"D:\UO\golems\Iron\p845-proof\walk.log"


def say(text):
    API.SysMsg("P845: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def close_all():
    for i in range(6):
        API.CloseGump()
        API.Pause(0.2)
    for g in API.GetAllGumps():
        try:
            g.Dispose()
        except Exception:
            pass


def here():
    return "%d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z)


API.Pause(4)
for _ in range(6):
    close_all()
    API.Pause(1.5)
say("start %s at %s" % (API.Player.Name, here()))

on_road = (API.Player.X, API.Player.Y) == (6702, 3983)   # only the walk-in shot starts here
if on_road:
    for (x, y) in [(6702, 3981), (6702, 3979), (6702, 3977), (6702, 3976)]:
        API.Pathfind(x, y, distance=0, wait=True, timeout=30)
        API.Pause(0.5)
        ok = API.Player.X == x and API.Player.Y == y
        say(("PASS " if ok else "FAIL ") + "walked to %d,%d: now %s" % (x, y, here()))

new = sorted((i.X, i.Y, i.Z) for i in (API.GetItemsOnGround(8, 0x0B2C) or []) if 3970 <= i.Y <= 3978 and i.X >= 6700)
old = sorted((i.X, i.Y, i.Z) for i in (API.GetItemsOnGround(8, 0x0B2D) or []) if 3970 <= i.Y <= 3978 and i.X >= 6700)
blood = sorted((i.Graphic, i.X, i.Y, i.Z) for g in (0x122A, 0x122C, 0x122D) for i in (API.GetItemsOnGround(8, g) or []))
signs = sorted((i.X, i.Y, i.Z) for i in (API.GetItemsOnGround(12, 0xA854) or []))
say(("PASS " if new == [(6704, 3975, 7), (6704, 3976, 7)] else "FAIL ") + "Pip's bench, two joined 0x0B2C pieces: %s" % new)
say(("PASS " if not old else "FAIL ") + "no crosswise 0x0B2D left in the farmhouse: %s" % old)
say("blood: %s" % blood)
say(("PASS " if (6701, 3980, 0) in signs else "FAIL ") + "the healing signpost at 6701,3980: signposts seen %s" % signs)
for _ in range(4):
    close_all()
    API.Pause(1.5)
say("done at %s" % here())
API.Stop()
