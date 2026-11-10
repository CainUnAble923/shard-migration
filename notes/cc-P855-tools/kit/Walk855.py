# cc-P855: the data-driven house addon and the housing furniture batch, in TazUO on the private proof shard (main, the
# SoS New Haven). A Player-account trainee; staff hands through stage855.py (the CMD/ACK file channel).
#   1. Each of the 30 designs stood on the grass east of the League hall by staff ([DecorAddon place), one shot each.
#   2. The trainee buys the Hunt Master's buffet table in the League shop's hunt row (Renown granted first), reads the
#      deed (its author), double-clicks it: the facing window; picks east-west: the placement cursor; aims at open
#      ground: refused (not in a house), the deed kept. The Achievement store opened for its furniture rows.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Decor"
PHASE = "p855"
DESIGN_SHOTS = False   # run 1 took the 30 piece shots; run 2 is the player half only

STAND = (3673, 2566, 0)      # the trainee, north-west of the subject
SUBJECT = (3677, 2570)       # the addon's own tile
DESIGNS = [
    "grey-fireplace-small-east", "grey-fireplace-small-south", "grey-fireplace-low-east", "grey-fireplace-low-south",
    "grey-fireplace-medium-east", "grey-fireplace-medium-south", "grey-fireplace-large-east", "grey-fireplace-large-south",
    "grey-fireplace-grand-east", "grey-fireplace-grand-south", "holiday-fireplace",
    "feasting-table-1", "feasting-table-2", "feasting-table-3",
    "buffet-table-east-west", "buffet-table-north-south", "formal-dining-table-east-west", "formal-dining-table-north-south",
    "harpsichord-east", "harpsichord-south",
    "small-kitchen-northwest", "small-kitchen-southeast", "barbecue-east", "barbecue-south",
    "country-kitchen-east", "country-kitchen-south",
    "blue-couch-east", "blue-couch-north", "blue-couch-south", "blue-couch-west",
]
LEAGUE_ROW_BUTTON = 200 + 38   # LeagueShopGump.BtnRowBase + the index of "hunt.buffet" in LeagueShop.Stock
DEED_ART = 0x14F0


def say(text):
    API.SysMsg("P855: " + text)
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


def deeds():
    return [i for i in (API.FindTypeAll(DEED_ART, API.Backpack) or [])]


if API.Player.Name != CHARACTER:
    API.SysMsg("P855: not %s, nothing to do" % CHARACTER)
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
    go(*STAND)
    z = API.Player.Z
    sx, sy = SUBJECT
    for design in (DESIGNS if DESIGN_SHOTS else []):
        stage("clear %d %d %d" % (sx, sy, z))
        stage("place %s %d %d %d" % (design, sx, sy, z))
        API.Pause(1.5)
        shot(design, 1.0, 2.0)
    stage("clear %d %d %d" % (sx, sy, z))

    # 2. the player's side: the League shop's hunt row, the deed, the facing window, the refusal outside a house
    stage("grant ap 1000")
    stage("grant renown 2000")
    API.Pause(1)
    before = len(deeds())
    API.Msg("[leagueshop")
    API.Pause(2.5)
    API.ReplyGump(LEAGUE_ROW_BUTTON)
    API.Pause(2.5)
    shot("league-hunt-row-confirm", 0.5, 2)
    API.ReplyGump(1)   # LeagueShopConfirmGump.BtnBuy
    API.Pause(2.5)
    close_all()
    got = deeds()
    check(len(got) == before + 1, "the hunt row's buy put a deed in the pack (%d -> %d)" % (before, len(got)))
    deed = None
    for d in got:
        props = str(API.ItemNameAndProps(d.Serial, True, 3) or "")
        say("deed: %s" % props.replace("\n", " | "))
        if "buffet" in props.lower():   # run 1: TazUO title-cases the text
            deed = d
    if check(deed is not None, "a deed for a Hunt Master's buffet table"):
        props = str(API.ItemNameAndProps(deed.Serial, True, 3) or "")
        check("design by manwitch" in props.lower(), "the deed names its author (manwitch)")
        API.UseObject(API.Backpack)
        API.Pause(1.5)
        shot("deed-in-pack", 0.5, 2)
        close_all()
        API.UseObject(deed.Serial)
        API.Pause(2.5)
        shot("facing-window", 0.5, 2)
        API.ReplyGump(1)   # east-west
        check(API.WaitForTarget("any", 4), "choosing a facing brings up the placement cursor")
        API.ClearJournal()
        API.Target(API.Player.X + 2, API.Player.Y + 2, API.Player.Z)
        API.Pause(2)
        check(API.InJournal("house that you own"), "aimed at open ground: refused, only in a house you own")
        shot("refused-outside-house", 0.5, 2)
        check(deed.Serial in [d.Serial for d in deeds()], "the deed is kept")
    API.Msg("[apstore")
    API.Pause(2.5)
    shot("achievement-store", 0.5, 2)
    close_all()
except Exception as e:
    say("FAIL script: %s" % e)
end()
