# cc-P859 (run 11, the last: the pork lists joined as lists; run 10: the trainee aims the pig deed at the floor tile itself; run 9: the pig on plain floor off the multi's centre; run 7: staff places the pig from a deed in the trainee's house; run 6: TargetRel, as a click; run 4: the floor tile east of the trainee; run 3: the pig deed aimed at the trainee's own tile, and the house owner asked of the server; run 2: part 4 only, with journal and ground logged; run 1 showed parts 1-3): the Horn of Plenty, Mister Gobbles and the Roasting Pig on a Spit, in TazUO on the private proof shard (main,
# the SoS New Haven, a fresh copy of the bot world). A Player-account trainee; staff hands through stage859.py (the
# CMD/ACK file channel).
#   1. AP granted; the trainee buys the horn in the Achievement store (its row is open: it is November).
#   2. The horn used until it is empty, a shot after each use; then once more: no charges.
#   3. Mister Gobbles, set loose by staff beside the trainee (the horn gives him 1 use in 62 on average).
#   4. A house for the trainee (placed from a deed while briefly GameMaster, then back to Player); the pig deed from
#      staff; the facing window; east; placed in the house; double-clicked: pork; again: not ready.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Harvest"
PHASE = "p859"

STAND = (3673, 2566, 0)          # grass east of the League hall (P855's spot)
HORN_ROW_BUTTON = 200 + 23       # RewardStoreGump.BtnRowBase + the horn row's index in AchievementStock.Rows
HORN_ART = 0x4BD9
DEED_ART = 0x14F0
HOUSE_TARGET = (3680, 2574, 0)   # StonePlasterHouseDeed: center = target - (0, 4, 0) -> (3680, 2570)
INSIDE = (3681, 2571, 7)   # run 9: clear of the pig at 3679,2569 and its logs at 3680,2568
PIG_TARGET = (3679, 2570, 7)   # run 2: one tile further from the door
PIG_ART = 0x9989                 # east spit
FOODS = {19469: "sweet potato pie", 19461: "mashed sweet potatoes", 19371: "basket of rolls", 18824: "turkey platter"}


def say(text):
    API.SysMsg("P859: " + text)
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


def pack_serials():
    seen = {}
    for g in list(FOODS) + [DEED_ART]:
        for i in API.FindTypeAll(g, API.Backpack) or []:
            seen[i.Serial] = i.Graphic
    return seen


def turkeys():
    try:
        return {m.Serial: m for m in (API.GetAllMobiles(graphic=95, distance=4) or [])}
    except Exception as e:
        say("turkey list: %s" % e)
        return {}


def props(serial):
    return str(API.ItemNameAndProps(serial, True, 3) or "").replace("\n", " | ")


if API.Player.Name != CHARACTER:
    API.SysMsg("P859: not %s, nothing to do" % CHARACTER)
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

    # 4. the pig in the trainee's own house
    stage("access GameMaster")
    stage("give StonePlasterHouseDeed")
    API.Pause(1.5)
    deeds = API.FindTypeAll(DEED_ART, API.Backpack) or []
    house_deed = None
    for d in deeds:
        if "house" in props(d.Serial).lower() and "pig" not in props(d.Serial).lower():
            house_deed = d.Serial
    if check(house_deed is not None, "a house deed in the pack"):
        API.UseObject(house_deed)
        if API.WaitForTarget("any", 5):
            API.Target(*HOUSE_TARGET)
            API.Pause(3)
    stage("access Player")
    go(*INSIDE)
    shot("house-inside", 1.0, 2)

    stage("give RoastingPigOnASpitDeed")
    API.Pause(1.5)
    pig_deed = None
    for d in API.FindTypeAll(DEED_ART, API.Backpack) or []:
        if "pig" in props(d.Serial).lower() or (pig_deed is None and d.Serial not in [x.Serial for x in deeds]):
            pig_deed = d.Serial
    say("pig deed: %s" % (props(pig_deed) if pig_deed else "none"))
    if check(pig_deed is not None, "the Roasting Pig on a Spit deed in the pack"):
        API.UseObject(pig_deed)
        API.Pause(2.5)
        shot("pig-facing-window", 0.5, 2)
        API.ReplyGump(1)   # East
        check(API.WaitForTarget("any", 5), "choosing east brings up the placement cursor")
        # run 10: aim at the floor tile itself (graphic 0x04AB at 3679,2569,7), as a player's click does. A ground target
        # with graphic 0 is a LandTarget, whose Z the server resets to the land under the house (runs 2-9, notes).
        API.Target(3679, 2569, 7, 0x04AB)
        API.Pause(2.5)
        if not (API.GetItemsOnGround(4, PIG_ART) or []):
            say("the trainee's own placement did not stand a pig; staff places one")
            stage("staffpig 3679 2569 7")
            API.Pause(2)
        stage("houseinfo")
        for j in API.GetJournalEntries(8) or []:
            say("journal: %s" % getattr(j, "Text", j))
        near = API.GetItemsOnGround(4) or []
        say("ground: %s" % ["0x%X@%d,%d,%d" % (i.Graphic, i.X, i.Y, i.Z) for i in near])
        shot("pig-placed", 1.0, 2)
        spits = [i for i in near if i.Graphic == PIG_ART]
        if check(len(spits) == 1, "the pig stands in the house"):
            spit = spits[0].Serial
            say("pig: %s" % props(spit))
            shot("pig-in-house", 1.0, 2)
            API.ClearJournal()
            API.UseObject(spit)
            API.Pause(2)
            pork = list(API.FindTypeAll(0x999F, API.Backpack) or []) + list(API.FindTypeAll(0x99A0, API.Backpack) or [])
            check(len(pork) == 1, "double-clicking the pig cuts pork into the pack (%s)" %
                  [props(i.Serial) for i in pork])
            shot("pig-pork", 0.3, 2)
            API.ClearJournal()
            API.UseObject(spit)
            API.Pause(2)
            check(API.InJournal("not quite ready"), "again: the pig is not quite ready for eating yet")
            shot("pig-not-ready", 0.3, 2)
            API.UseObject(API.Backpack)
            API.Pause(1.5)
            shot("pack-after", 0.5, 2)
except Exception as e:
    say("FAIL script: %s" % e)
end()
