# cc-P804: Herbalism in TazUO on the private proof shard: the skill in the skills window, a wild patch picked, processing into a bundle
# and reagents, the Order's herb table, and a raised bed with reagent plants. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot,
# "CLICK x y" for a click in the window. The bed is placed by staff in the open: a house needs its own rig, and the facts cover the bed.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Herb"
PATCH = (3625, 2558)
TABLE = (3606, 2500)
BED = (1986, 2244, 0)
GARLIC_ART = 0x18E1
RAW, BUNDLE, REAGENT = 0xF84, 0x1A9C, 0xF84


def sig(line):
    with open(SIG, "a") as f:
        f.write(line + "\n")


def say(text):
    API.SysMsg("P804: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=1.5, after=2.5):
    API.Pause(settle)
    sig("SHOT " + name)
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


def journal(seconds=8):
    for e in API.GetJournalEntries(seconds) or []:
        if "skill in" not in e.Text and "P804" not in e.Text and "has changed by" not in e.Text:
            say("journal: " + e.Text)


if API.Player.Name != CHARACTER:
    API.SysMsg("P804: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)

API.Pause(7)
close_all()
API.Msg("[self set Blessed True")
API.Pause(1)
robe = API.FindLayer("Robe")
if robe is not None:
    API.Msg("[delete")
    if API.WaitForTarget("any", 4):
        API.Target(robe.Serial)
    API.Pause(1.5)

# The skill: the client knows it, and the window lists it.
s = API.GetSkill("Herbalism")
check(s is not None, "the client has a Herbalism skill (%s)" % (s.Value if s is not None else None))
API.Msg("[self set Skills.Herbalism.Base 30")
API.Pause(1.5)
close_all()
import System
from System.Reflection import Assembly, BindingFlags
F = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Instance
try:
    asm = Assembly.GetEntryAssembly()
    client = asm.GetType("ClassicUO.Client")
    game = client.GetProperty("Game", F).GetValue(None)
    uo = game.GetType().GetProperty("UO", F).GetValue(game)
    world = uo.GetType().GetProperty("World", F).GetValue(uo)
    groups = world.GetType().GetProperty("SkillsGroupManager", F).GetValue(world).Groups
    for g in groups:
        g.IsMaximized = g.Contains(58)
        if g.Contains(58):
            say("Herbalism is in the group %s" % g.Name)
    asm.GetType("ClassicUO.Game.GameActions").GetMethod("OpenSkills", F).Invoke(None, System.Array[System.Object]([world]))
except Exception as e:
    say("skills window: %s" % e)
API.Pause(3)
shot("1-skills-window")
close_all()

# Foraging.
API.Msg("[self set Map Trammel")
API.Pause(1)
API.Msg("[go %d %d" % (PATCH[0] - 1, PATCH[1] + 1))
API.Pause(6)
say("at %d,%d" % (API.Player.X, API.Player.Y))
close_all()
shot("2-patch")
found = API.GetItemsOnGround(10, GARLIC_ART) or []
check(len(found) > 0, "a wild garlic patch stands here")
got = None
for i in range(12):
    found = API.GetItemsOnGround(10, GARLIC_ART) or []
    if not found:
        break
    API.Pathfind(found[0].X, found[0].Y)
    API.Pause(3)
    API.UseObject(found[0].Serial)
    API.Pause(1.2)
    got = API.FindType(RAW, API.Backpack)
    if got is not None:
        break
journal(20)
check(got is not None, "raw garlic is in the backpack")
if got is not None:
    say(str(API.ItemNameAndProps(got.Serial, True, 3)))
API.Pause(1)
shot("3-picked")

# Processing.
if got is None:
    API.Msg("[self AddToPack RawHerb")
    API.Pause(2)
    got = API.FindType(RAW, API.Backpack)
if got is not None:
    API.Msg("[set Amount 12")
    if API.WaitForTarget("any", 4):
        API.Target(got.Serial)
    API.Pause(2)
API.UseObject(API.Backpack)
API.Pause(2)
shot("4-herbs-in-pack")
API.UseObject(got.Serial)
API.Pause(2.5)
bundle = API.FindType(BUNDLE, API.Backpack)
check(bundle is not None, "the herbs made a bundle")
if bundle is not None:
    say(str(API.ItemNameAndProps(bundle.Serial, True, 3)))
shot("5-bundle")
if bundle is not None:
    API.UseObject(bundle.Serial)
    API.Pause(2.5)
journal(10)
shot("6-reagents")

# The ledger.
API.Msg("[herbalism")
API.Pause(2.5)
shot("7-ledger")
close_all()

# The Order's table.
API.Msg("[go %d %d" % (TABLE[0] + 1, TABLE[1] + 1))
API.Pause(6)
say("at %d,%d" % (API.Player.X, API.Player.Y))
table = API.GetItemsOnGround(5, 0x0B7D) or []
check(len(table) > 0, "the herb table stands in the hall")
if table:
    API.UseObject(table[0].Serial)
    API.Pause(3)
    shot("8-table")
    API.ReplyGump(1)
    API.Pause(3)
    journal(5)
    shot("9-starter")
close_all()

# A bed.
API.UseObject(API.Backpack)
for g in API.GetAllGumps():
    try:
        if "Grid" in g.GetType().Name or "Container" in g.GetType().Name:
            g.Dispose()
    except Exception:
        pass
API.Msg("[self set Map Trammel")
API.Pause(1)
API.Msg("[self set Location (%d,%d,%d)" % BED)
API.Pause(5)
close_all()
for dx, dy in ((6, 0), (7, 0), (6, 1), (7, 1)):
    API.Msg("[add RaisedGardenPlantItem")
    if API.WaitForTarget("any", 4):
        API.Target(API.Player.X + dx, API.Player.Y + dy, API.Player.Z)
    API.Pause(1)
API.Msg("[add RaisedGardenAddon Small")
if API.WaitForTarget("any", 4):
    API.Target(API.Player.X + 6, API.Player.Y, API.Player.Z)
API.Pause(2)
for prop, val in (("PlantType", "Mandrake"), ("PlantHue", "Plain"), ("PlantStatus", "Stage9")):
    API.Msg("[area set %s %s where RaisedGardenPlantItem" % (prop, val))
    if API.WaitForTarget("any", 4):
        API.Target(API.Player.X + 5, API.Player.Y - 1, API.Player.Z)
        if API.WaitForTarget("any", 4):
            API.Target(API.Player.X + 9, API.Player.Y + 3, API.Player.Z)
    API.Pause(1.5)
journal(12)
shot("10-bed", 3)

sig("END")
say("done")
