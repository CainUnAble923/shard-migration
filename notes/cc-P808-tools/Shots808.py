# cc-P808: the Clockwork Scavenger in TazUO on the private proof shard: the Tinker guildmaster's answer, the frame, the parts used,
# the Scavenger following, and loot lifted from a corpse. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a
# shot. The character joins the Tinkers' Union by its own gump, and [GuildStanding sets Journeyman standing.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Cogs"
OPEN = (1986, 2244, 0)  # open ground (P804's bed spot); main's halls moved with the SoS map, so staff places a Tinker guildmaster here
PARTS = (("Gears", 0x1053, 10), ("Springs", 0x105D, 10), ("ClockParts", 0x104F, 5), ("AxleGears", 0x1051, 2), ("IronIngot", 0x1BF2, 50))
FRAME_HUE = 0x972


def sig(line):
    with open(SIG, "a") as f:
        f.write(line + "\n")


def say(text):
    API.SysMsg("P808: " + text)
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
        if "P808" not in e.Text and "has changed by" not in e.Text:
            say("journal: " + e.Text)


def has_line(text, seconds=10):
    return any(text in e.Text for e in (API.GetJournalEntries(seconds) or []))


def frame():
    for i in API.FindTypeAll(0x104F, API.Backpack) or []:
        if i.Hue == FRAME_HUE:
            return i
    return None


if API.Player.Name != CHARACTER:
    API.SysMsg("P808: not %s, nothing to do" % CHARACTER)
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

# A Tinker guildmaster on open ground; join, and Journeyman standing.
API.Msg("[self set Map Trammel")
API.Pause(1)
API.Msg("[self set Location (%d,%d,%d)" % OPEN)
API.Pause(5)
say("at %d,%d" % (API.Player.X, API.Player.Y))
close_all()
API.Msg("[add TinkerGuildmaster")
if API.WaitForTarget("any", 4):
    API.Target(API.Player.X + 2, API.Player.Y, API.Player.Z)
API.Pause(1.5)
API.Msg("[area set CantWalk true where TinkerGuildmaster")
if API.WaitForTarget("any", 4):
    API.Target(API.Player.X - 4, API.Player.Y - 4, API.Player.Z)
    if API.WaitForTarget("any", 4):
        API.Target(API.Player.X + 4, API.Player.Y + 4, API.Player.Z)
API.Pause(1.5)
API.Msg("scavenger")
API.Pause(2)
check(has_line("Join the Tinkers' Union first"), "a stranger is sent to join first")
API.Msg("I wish to join")
API.Pause(2.5)
API.ReplyGump(1)
API.Pause(2)
close_all()
API.Msg("scavenger")
API.Pause(2)
check(has_line("Journeyman"), "an Initiate is told to come back at Journeyman")
API.Msg("[GuildStanding tinkers 5000")
if API.WaitForTarget("any", 4):
    API.Target(API.Player.Serial)
API.Pause(2)
API.Msg("scavenger")
API.Pause(2.5)
journal(4)
shot("1-guildmaster-gives-the-frame")
f = frame()
check(f is not None, "the frame is in the backpack")

# The frame, before the parts.
if f is not None:
    say(str(API.ItemNameAndProps(f.Serial, True, 3)))
    API.UseObject(API.Backpack)
    API.Pause(2)
    API.UseObject(f.Serial)
    API.Pause(2)
    check(has_line("still needs"), "the frame lists what it still needs")
    shot("2-frame-needs-parts")

# The parts, then the frame again.
for name, art, amount in PARTS:
    API.Msg("[self AddToPack %s %d" % (name, amount))
    API.Pause(1.2)
journal(6)
API.Pause(1)
shot("3-parts-in-pack")
f = frame()
if f is not None:
    API.UseObject(f.Serial)
    API.Pause(3)
check(has_line("clicks to life"), "the Scavenger is built")
check(frame() is None, "the frame is used up")
scav = None
for m in API.GetAllMobiles() or []:
    if m.Name and "Scavenger" in m.Name:
        scav = m
check(scav is not None, "the Scavenger stands here")
if scav is not None:
    say(str(API.ItemNameAndProps(scav.Serial, True, 3)) if hasattr(API, "ItemNameAndProps") else scav.Name)
close_all()
shot("4-scavenger-built")

# It follows a few steps.
API.Pathfind(API.Player.X - 3, API.Player.Y + 3)
API.Pause(5)

# A monster to loot: an orc killed beside it (its own loot: gold and the like).
API.Msg("[add Orc")
if API.WaitForTarget("any", 4):
    API.Target(API.Player.X, API.Player.Y + 1, API.Player.Z)
API.Pause(2)
orc = None
for m in API.GetAllMobiles() or []:
    if m.Graphic == 0x11:  # the orc's body; its name may not have reached the client yet
        orc = m
if orc is not None:
    API.Msg("[kill")
    if API.WaitForTarget("any", 4):
        API.Target(orc.Serial)
API.Pause(1.5)
corpse = None
for i in range(6):
    for c in API.GetItemsOnGround(6, 0x2006) or []:
        corpse = c
    if corpse is not None:
        break
    API.Pause(1)
check(orc is not None, "the orc stands here")
check(corpse is not None, "the orc's corpse is here")
if corpse is not None:
    API.UseObject(corpse.Serial)
def where():
    sc = None
    for m in API.GetAllMobiles() or []:
        if m.Name and "Scavenger" in m.Name:
            sc = m
    g = API.FindType(0xEED, corpse.Serial) if corpse is not None else None
    say("player %d,%d scavenger %s corpse %s gold in corpse %s" % (API.Player.X, API.Player.Y,
        "%d,%d" % (sc.X, sc.Y) if sc else "?", "%d,%d" % (corpse.X, corpse.Y) if corpse else "?", g.Amount if g else 0))


where()
shot("5-corpse", 0.3, 1.0)
if corpse is not None:
    API.Pathfind(corpse.X, corpse.Y)
got = False
for i in range(25):
    API.Pause(1)
    if has_line("Clockwork Scavenger collects", 30):
        got = True
        break
where()
journal(12)
check(got, "the Scavenger lifted the loot")
API.UseObject(API.Backpack)
API.Pause(2)
shot("6-loot-collected")

sig("END")
say("done")
