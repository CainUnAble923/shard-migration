# cc-P844 (P814's Walk814Isle.py, cut down): P834's pieces as main has them, walked on foot in TazUO with the client's own
# steps (Pathfind, no teleport) on the private proof shard: the clothes stop, the chat stop, the farm gate and Pip on his
# bench in the farmhouse. Each sign and piece is clicked so its name shows over it, then a shot is asked for through the
# signal file shots844.ps1 watches ("SHOT <name>", "DONE"). Each step's position and Z go to the log.
import API

LOG = r"D:\UO\golems\Iron\p844-proof\tour.log"
SIG = r"D:\UO\golems\Iron\p844-proof\tour.sig"
CHARACTER = "Iron the Tester"


def say(text):
    API.SysMsg("P844: " + text)
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
            g.Dispose()
        except Exception:
            pass


def walk(points, reach=0):
    for (x, y) in points:
        for _ in range(3):
            API.Pathfind(x, y, distance=reach, wait=True, timeout=30)
            if abs(API.Player.X - x) <= reach + 1 and abs(API.Player.Y - y) <= reach + 1:
                break
            API.Pause(1)
        say("walked to %d,%d,%d (wanted %d,%d)" % (API.Player.X, API.Player.Y, API.Player.Z, x, y))


def at(graphic, x, y, dist=12):
    return [s for s in (API.GetItemsOnGround(dist, graphic) or []) if s.X == x and s.Y == y]


def read(graphic, x, y, name, what):
    found = at(graphic, x, y)
    if not check(bool(found), "%s 0x%04X is at %d,%d" % (what, graphic, x, y)):
        return False
    API.ClearJournal()
    API.ClickObject(found[0].Serial)
    API.Pause(1)
    return check(API.InJournal(name), "%s reads '%s'" % (what, name))


def end():
    with open(SIG, "a") as f:
        f.write("DONE\n")
    API.Stop()


if API.Player.Name != CHARACTER:
    API.SysMsg("P844: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s at %d,%d,%d" % (API.Player.Name, API.Player.X, API.Player.Y, API.Player.Z))
API.Pause(6)
for _ in range(6):
    close_all()
    API.Pause(1)

# 1. the clothes stop: the rack and the table (Rack -1,-2)
walk([(6663, 3993)])
read(0x0B8F, 6664, 3990, "table", "the clothes table")
read(0x0EC6, 6665, 3990, "clothes rack", "the clothes rack")
shot("tazuo-clothes-table-read", 0.1, 2)

# 2. the chat stop: the farm signpost north of the road (Signpost -2,-4)
walk([(6672, 3993), (6680, 3991), (6688, 3990)])
read(0xA854, 6690, 3986, "Farm signpost: say 'I am ready to learn'", "the chat signpost")
shot("tazuo-chat-signpost-read", 0.1, 2)

# 3. the farm gate: the gate's signpost, the field gate and its fence piece, Wren
walk([(6692, 3986), (6694, 3982)])
read(0xA854, 6697, 3977, "Farm signpost: Wren the Farmhand at the gate", "the farm gate signpost")
shot("tazuo-farm-gate-signpost-read", 0.1, 2)
gate = [s for s in (API.GetItemsOnGround(8) or []) if s.X == 6695 and s.Y == 3979 and "gate" in (s.Name or "").lower()]
check(bool(gate), "the field gate is at 6695,3979" + (" (0x%04X, %s)" % (gate[0].Graphic, gate[0].Name) if gate else ""))
fence = at(0x0837, 6695, 3978)
check(bool(fence), "the fence piece 0x0837 is at 6695,3978")
shot("tazuo-field-gate-and-fence", 0.5, 2)

# 4. Pip on his bench: in at the farmhouse door (south wall, 6702,3978), to the table
walk([(6701, 3981), (6702, 3979)])
doors = [s for s in (API.GetItemsOnGround(3) or []) if s.X == 6702 and s.Y == 3978]
if doors:
    API.UseObject(doors[0].Serial)
    API.Pause(1.5)
walk([(6702, 3977), (6702, 3976)])
for bx, by in ((6704, 3975), (6704, 3976)):
    b = [s for s in (API.GetItemsOnGround(4) or []) if s.X == bx and s.Y == by and s.Z == 7 and "bench" in (s.Name or "").lower()]
    check(len(b) == 1, "one bench piece at %d,%d,7%s" % (bx, by, (": 0x%04X" % b[0].Graphic) if b else ""))
shot("tazuo-pip-on-bench", 0.5, 2)
mobs = [m for m in (API.GetAllMobiles() or []) if m.X == 6704 and m.Y == 3975]
check(bool(mobs), "Pip is on the bench at 6704,3975")
if mobs:
    API.ClickObject(mobs[0].Serial)
    API.Pause(1)
shot("tazuo-pip-on-bench-named", 0.1, 2)
walk([(6702, 3978), (6702, 3980)])
say("end at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
end()
