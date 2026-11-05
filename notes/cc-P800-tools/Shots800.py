# cc-P800: the League sash at each step, in TazUO on the private proof shard. A new character on the Golem's admin account goes to
# Elara, takes the first sash from her menu and wears it, buys step 1 from her page with Renown earned through real achievements,
# then walks the other steps with [LeagueSash step (the fees would need 20,000 Renown; facts cover every paid step). At each step:
# her page, the worn sash in the paperdoll, and the item's own text. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Sash"
MEADOW = (1986, 2244, 0)
SASH = 0x1541
BTN_SASH, BTN_TAKE, BTN_UPGRADE = 31, 32, 33
EARN = ["mining.prospector", "mining.surveyor", "mining.master_prospector"]
STEPS = [
    (1, "Dull Copper", 2),
    (2, "Bronze", 5),
    (3, "Verite", 8),
    (4, "Blaze", 12),
    (5, "Mythril", 15),
    (6, "Celestial", 17),
]


def say(text):
    API.SysMsg("P800: " + text)
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
            if g.PacketGumpText or "PaperDoll" in g.GetType().Name:
                g.Dispose()
        except Exception:
            pass


def elara():
    for m in API.GetAllMobiles(None, 18) or []:
        if m.Name and "Elara" in m.Name:
            return m
    return None


def open_page(serial):
    close_all()
    API.UseObject(serial)
    API.Pause(2.5)
    API.ReplyGump(BTN_SASH)
    API.Pause(2.5)


if API.Player.Name != CHARACTER:
    API.SysMsg("P800: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)

API.Pause(7)
close_all()
API.Msg("[self set Blessed True")
API.Pause(1)
API.Msg("[self set Map Trammel")
API.Pause(1)
API.Msg("[self set Location (%d,%d,%d)" % MEADOW)
API.Pause(5)
close_all()
# The bot world's copy may not have her in reach: a staff [add of the real class, on this tile, then a step away.
API.Msg("[add LeagueRegistrar")
if API.WaitForTarget("any", 4):
    API.Target(API.Player.Serial)
API.Pause(2)
API.Msg("[global set CantWalk True where leagueregistrar")  # she wanders out of reach otherwise
API.Pause(2)
# The admin's robe covers the sash layer.
robe = API.FindLayer("Robe")
if robe is not None:
    API.Msg("[delete")
    if API.WaitForTarget("any", 4):
        API.Target(robe.Serial)
    API.Pause(1.5)
for step in ("east", "east", "south"):
    API.Walk(step)
    API.Pause(0.5)
API.Pause(1)
her = elara()
if not check(her is not None, "Elara is here"):
    say("mobiles: %s" % [m.Name for m in (API.GetAllMobiles(None, 18) or [])])
    with open(SIG, "a") as f:
        f.write("END\n")
    API.Stop()
say("Elara at %d,%d, me at %d,%d" % (her.X, her.Y, API.Player.X, API.Player.Y))
serial = her.Serial

# The first sash, from her menu.
API.Msg("[self set LeagueRank 1")
API.Pause(1.5)
API.UseObject(serial)
API.Pause(3)
shot("step0-1-menu")
API.ReplyGump(BTN_SASH)
API.Pause(3)
shot("step0-2-offer")
API.ReplyGump(BTN_TAKE)
API.Pause(3)
shot("step0-3-page")
sash = API.FindType(SASH, API.Backpack)
if not check(sash is not None, "the sash is in the backpack"):
    with open(SIG, "a") as f:
        f.write("END\n")
    API.Stop()
say("first sash: hue %d, %s" % (sash.Hue, API.ItemNameAndProps(sash.Serial, True, 3)))
sid = sash.Serial
close_all()
API.EquipItem(sid)
API.Pause(2)
API.UseObject(API.Player.Serial)
shot("step0-4-worn", 3)

# Step 1 bought at Elara, with Renown from achievements.
for key in EARN:
    API.Msg("[ClusterFAchievement grant %s" % key)
    API.Pause(2)
close_all()
for s, metal, rank in STEPS:
    API.Msg("[self set LeagueRank %d" % rank)
    API.Pause(1.5)
    close_all()
    if s > 1:
        API.Msg("[LeagueSash step %d" % s)
        API.Pause(2)
    open_page(serial)
    if s == 1:
        shot("step1-0-page-before")
        API.ClearJournal()
        API.ReplyGump(BTN_UPGRADE)
        API.Pause(3)
    shot("step%d-1-page" % s)
    item = API.FindItem(sid)
    text = API.ItemNameAndProps(sid, True, 3)
    say("step %d: hue %s, %s" % (s, item.Hue if item else None, text))
    check(text is not None and metal.lower() in text.lower() and ("step %d of 6" % s) in text.lower(), "step %d reads %s" % (s, metal))
    check(text is not None and ("+%d%% renown" % s) in text.lower(), "step %d says +%d%%" % (s, s))
    close_all()
    API.UseObject(API.Player.Serial)
    shot("step%d-2-worn" % s, 3)

with open(SIG, "a") as f:
    f.write("END\n")
say("done")
