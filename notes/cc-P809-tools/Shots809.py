# cc-P809: the pet perch and horse barding in TazUO on the private proof shard. A staff character on open ground (1986, 2244,
# Trammel; as P808, since main's guild coordinates are not the halls) places two perches and their perched pets, then tames a
# horse, puts valorite barding on it, and rides it. The perch's placement rules (house co-owners, own tamed pet) are proven
# by the facts; here staff place the pets, as P804 placed its bed. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Perch"
MEADOW = (1986, 2244, 0)
HORSES = (0xC8, 0xE2, 0xE4, 0xCC)
BARDED = 284
DEED = 0x14F0


def sig(line):
    with open(SIG, "a") as f:
        f.write(line + "\n")


def say(text):
    API.SysMsg("P809: " + text)
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


def wait_journal(text, seconds):
    for _ in range(int(seconds * 2)):
        if API.InJournal(text):
            return True
        API.Pause(0.5)
    return False


def close_packs():
    for g in API.GetAllGumps():
        try:
            if "Grid" in g.GetType().Name or "Container" in g.GetType().Name:
                g.Dispose()
        except Exception:
            pass


def mobiles(graphics, dist=12):
    out = []
    for g in graphics:
        out += API.GetAllMobiles(g, dist) or []
    return out


def add_at(what, dx, dy, dz=0):
    API.Msg("[add " + what)
    if API.WaitForTarget("any", 4):
        API.Target(MEADOW[0] + dx, MEADOW[1] + dy, MEADOW[2] + dz)
    API.Pause(1.5)


if API.Player.Name != CHARACTER:
    API.SysMsg("P809: not %s, nothing to do" % CHARACTER)
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
API.Msg("set animaltaming 100")
API.Pause(1)
API.Msg("[self set Map Trammel")
API.Pause(1)
API.Msg("[self set Location (%d,%d,%d)" % MEADOW)
API.Pause(5)
close_all()
say("at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))

# ---------------------------------------------------------------- perches
# The camera looks north-west: stand north-west of the subject, the perches south-east of the character.
add_at("PetPerchAddon", 2, 2)
add_at("PerchedPet", 2, 2, 12)
add_at("PetPerchAddon", 4, 1)
add_at("PerchedPet", 4, 1, 12)
API.Msg("[area set Body 5 Name Talon where PerchedPet")
if API.WaitForTarget("any", 4):
    API.Target(MEADOW[0] + 3, MEADOW[1], MEADOW[2])
    if API.WaitForTarget("any", 4):
        API.Target(MEADOW[0] + 5, MEADOW[1] + 1, MEADOW[2])
API.Pause(1.5)
API.Msg("[area set Name Pecky Hue 89 where PerchedPet")
if API.WaitForTarget("any", 4):
    API.Target(MEADOW[0] + 2, MEADOW[1] + 2, MEADOW[2])
    if API.WaitForTarget("any", 4):
        API.Target(MEADOW[0] + 2, MEADOW[1] + 2, MEADOW[2])
API.Pause(1.5)
for x0, y0 in ((2, 2), (4, 1)):
    API.Msg("[area set Z 12 where PerchedPet")
    if API.WaitForTarget("any", 4):
        API.Target(MEADOW[0] + x0, MEADOW[1] + y0, MEADOW[2])
        if API.WaitForTarget("any", 4):
            API.Target(MEADOW[0] + x0, MEADOW[1] + y0, MEADOW[2])
    API.Pause(1.5)
lizards = API.GetAllMobiles(716, 8) or []
eagles = API.GetAllMobiles(5, 8) or []
check(len(lizards) > 0, "a perched chicken lizard (body 716) stands on its perch")
check(len(eagles) > 0, "a perched eagle (body 5) stands on its perch")
for m in lizards + eagles:
    say("perched: %s at %d,%d,%d" % (m.Name, m.X, m.Y, m.Z))
shot("1-perches", 2.5)

# ---------------------------------------------------------------- barding
add_at("Horse", -3, 2)
found = mobiles(HORSES, 8)
check(len(found) > 0, "a wild horse stands on the meadow")
horse = found[0] if found else None
tamed = False
if horse is not None:
    shot("2-plain-horse")
    for attempt in range(6):
        horse = API.FindMobile(horse.Serial) or horse
        API.Pathfind(horse.X, horse.Y, distance=2, wait=True, timeout=10)
        API.ClearJournal()
        API.UseSkill("Animal Taming")
        if API.WaitForTarget("any", 5):
            API.Target(horse.Serial)
        if wait_journal("accept you as master", 25):
            tamed = True
            break
        API.Pause(3)
check(tamed, "Animal Taming tames the horse")

API.Msg("[self AddToPack CraftedHorseBarding")
API.Pause(2)
barding = API.FindType(DEED, API.Backpack)
API.Msg("[set Resource Valorite Exceptional True")
if barding is not None and API.WaitForTarget("any", 4):
    API.Target(barding.Serial)
API.Pause(1.5)
if barding is not None:
    say("barding: " + str(API.ItemNameAndProps(barding.Serial, True, 3)).replace("\n", " | "))
check(barding is not None, "horse barding is in the pack")
API.UseObject(API.Backpack)
API.Pause(2)
shot("3-barding-in-pack")
close_all()

if barding is not None and horse is not None and tamed:
    API.ClearJournal()
    API.UseObject(barding.Serial)
    if API.WaitForTarget("any", 4):
        API.Target(horse.Serial)
    check(wait_journal("You place the barding", 6), "the barding goes on the horse")
    API.Pause(1.5)
    h = API.FindMobile(horse.Serial)
    check(h is not None and h.Graphic == BARDED, "the horse is the armored horse (body %s)" % (h.Graphic if h else None))
    close_packs()
    API.Pathfind(horse.X - 2, horse.Y - 2, distance=0, wait=True, timeout=10)
    shot("4-barded-horse", 2)

    for attempt in range(4):
        h = API.FindMobile(horse.Serial) or horse
        API.Pathfind(h.X, h.Y, distance=1, wait=True, timeout=10)
        API.Pause(0.5)
        API.UseObject(horse.Serial)
        API.Pause(2.5)
        if API.FindLayer("Mount") is not None:
            break
    check(API.FindLayer("Mount") is not None, "the character rides the barded horse")
    shot("5-riding-barded-horse", 2)
    for i in range(3):
        API.Walk("East")
        API.Pause(0.3)
    shot("6-riding-moved", 1)


API.Msg("[self AddToPack PetPerchDeed")
API.Pause(2)
API.UseObject(API.Backpack)
API.Pause(2)
shot("7-perch-deed-in-pack")
sig("END")
say("done")
