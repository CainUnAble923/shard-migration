# cc-P731: a real character plays the isle's new steps in TazUO (the client's own movement, gumps, drags and
# commands; no teleport): the first login's wake, the cloak chest, Wren's pitchfork, war mode, the pests, the pet
# reward, Pet Info from the pet's menu, the healing lesson with Pip in the farmhouse, then the dock both ways.
# Each step goes to the journal and to LOG; "SHOT <name>" lines in SIG ask the runner (tazuo-walk.ps1) for a shot.
import API

LOG = r"D:\UO\golems\Iron\p731-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p731-proof\shots.sig"

FINISHED = "Lesson finished"
TAMSIN = (6640, 3992)
BLUE_TILE, GOLD_TILE = (6646, 3992), (6649, 3992)
CAMP, TABLE, SIGN = (6656, 3990), (6664, 3990), (6692, 3990)
WREN, BELOW_WREN, PESTS = (6714, 3978), (6714, 3979), (6702, 3978)
PIP = (6692, 3975)
STEPS = (6690, 3980)
PET_INFO_ENTRY = 11   # the pet's context menu, entry 11 (cliloc 1900017), read by pet_menu_probe.py


def say(text):
    API.SysMsg("P731: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=2.0, clear=False):
    if clear:  # run 8: the windows hid what the facing check looks at; they come back with the next server message
        for g, _ in gumps():
            try:
                g.Dispose()
            except Exception:
                pass
    API.Pause(settle)
    with open(SIG, "a") as f:
        f.write("SHOT " + name + "\n")
    API.Pause(2.5)


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


def gumps():
    out = []
    for g in API.GetAllGumps():
        try:
            t = g.PacketGumpText or ""
        except Exception:
            t = ""
        out.append((g, t))
    return out


def gump_ids(g):
    for obj in (g, getattr(g, "Gump", None)):
        for attr in ("ServerSerial", "GumpID", "ID"):
            try:
                v = getattr(obj, attr)
                if v:
                    return int(v)
            except Exception:
                pass
    return None


def find_gump(text):
    for g, t in gumps():
        if text in t:
            return g
    return None


def log_gumps(label):
    gs = gumps()
    say("%s: %d server gumps" % (label, len(gs)))
    for g, t in gs:
        say("   gump %s: %s" % (gump_ids(g), t[:160].replace("\n", " ")))


def wait_gump(text, seconds):
    for _ in range(int(seconds * 2)):
        g = find_gump(text)
        if g is not None:
            return g
        API.Pause(0.5)
    return None


def reply(text, button, seconds=10):
    g = wait_gump(text, seconds)
    if g is None:
        say("no gump with %r" % text)
        return False
    gid = gump_ids(g)
    say("reply %d to gump %s (%r)" % (button, gid, text))
    if gid:
        API.ReplyGump(button, gid)
    else:
        API.ReplyGump(button)
    API.Pause(1.0)
    return True


def wait_journal(text, seconds):
    for _ in range(int(seconds * 2)):
        if API.InJournal(text):
            return True
        API.Pause(0.5)
    return False


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    return ok


def go(xy, dist=0, what=""):
    # run 5: TazUO's Pathfind gave up on every target more than about 10 tiles off, so walk legs of at most 8 tiles
    for _ in range(12):
        p = where()
        dx, dy = xy[0] - p[0], xy[1] - p[1]
        n = max(abs(dx), abs(dy))
        if n <= 8:
            break
        k = 8.0 / n
        API.Pathfind(p[0] + int(round(dx * k)), p[1] + int(round(dy * k)), distance=1, wait=True, timeout=20)
        if where() == p:
            API.Walk(("east" if dx > 0 else "west") if abs(dx) >= abs(dy) else ("south" if dy > 0 else "north"))
            API.Pause(0.6)
    for _ in range(3):
        API.Pathfind(xy[0], xy[1], distance=dist, wait=True, timeout=30)
        p = where()
        if abs(p[0] - xy[0]) <= max(dist, 0) and abs(p[1] - xy[1]) <= max(dist, 0):
            break
        API.Pause(1.0)
    p = where()
    return check(abs(p[0] - xy[0]) <= dist + 1 and abs(p[1] - xy[1]) <= dist + 1,
                 "walked to %s %s (at %s)" % (what, xy, p))


def mobiles_near(xy, r, graphics=None, name=None):
    out = []
    for m in API.GetAllMobiles():
        try:
            if m.Serial == API.Player.Serial:
                continue
            if abs(m.X - xy[0]) > r or abs(m.Y - xy[1]) > r:
                continue
            if graphics and m.Graphic not in graphics:
                continue
            if name and name not in (m.Name or ""):
                continue
            out.append(m)
        except Exception:
            pass
    return out


def steps(direction, n):
    for _ in range(n):
        API.Walk(direction)
        API.Pause(0.6)
        say("  %s -> %s" % (direction, where()))


def next_lesson():
    if wait_gump(FINISHED, 15) is None:
        check(False, "the lesson finished")
        return False
    check(True, "the lesson finished")
    return reply(FINISHED, 1)


# -- 0. first login: only the wake scene, lying until the first move -------------------------------------------------
CHARACTER = "Iron Dawn"   # the brand-new character TazUO creates (ui.ps1); any other character: do nothing
if API.Player.Name != CHARACTER:
    API.SysMsg("P731: not %s, the walk does not run" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s, %s" % (API.Player.Name, where()))
API.Pause(3)
log_gumps("at login")
shot("wake-1", 0.5)
check(len(gumps()) == 0, "no server window while lying")
check(wait_journal("Move to get up", 15), "the System says: Move to get up.")
check(not API.InJournal("You wake on a quiet shore"), "still lying: the first lesson's lines wait")
log_gumps("lying, before the first move")
shot("wake-2", 0.5)
# run 4 found TazUO sends no step or turn while the player is Frozen (PlayerMobile.Walk: IsParalyzed), so try both
# the ways a player would, for the record, then wait for the stand-up (TutorialWake.SafetySeconds, 60 s)
t_lie = 0
for d in ("east", "north", "west"):
    API.Walk(d)
    API.Pause(1.5)
    t_lie += 1.5
    say("after Walk(%s): %s, journal 'quiet shore': %s" % (d, where(), API.InJournal("You wake on a quiet shore")))
API.Turn("south")
API.Pause(1.5)
t_lie += 1.5
say("after Turn(south): %s, journal 'quiet shore': %s" % (where(), API.InJournal("You wake on a quiet shore")))
check(API.InJournal("You wake on a quiet shore"), "a step or a turn in TazUO gets the trainee up")
shot("tried-to-move", 0.5)
while t_lie < 75 and not API.InJournal("You wake on a quiet shore"):
    API.Walk("east")
    API.Pause(1.0)
    t_lie += 1.0
say("stood up after about %d s of trying to move (%s)" % (t_lie, where()))
API.Pause(3.0)
check(API.InJournal("You wake on a quiet shore"), "the trainee is up and the first lesson starts")
log_gumps("stood up")
shot("up", 0.5)

# -- 1. movement -----------------------------------------------------------------------------------------------------
if wait_gump("Walk and run", 6) is None:
    go(TAMSIN, 2, "Tamsin")
    t = mobiles_near(TAMSIN, 3, name="Tamsin")
    if t:
        API.UseObject(t[0].Serial)
        reply("Tamsin: the Wakening Isle", 100)
go(BLUE_TILE, 0, "the blue tile")
API.Pause(1.5)
go(GOLD_TILE, 0, "the gold tile")
next_lesson()

# -- 2. backpack -----------------------------------------------------------------------------------------------------
go(CAMP, 2, "the camp")
API.UseObject(API.Player.Serial)
API.Pause(1.2)
API.UseObject(API.Backpack)
API.Pause(1.2)
bag = API.FindType(0x0E76, API.Backpack, hue=0x4F2)
if check(bag is not None, "the blue practice bag is in the backpack"):
    API.UseObject(bag.Serial)
next_lesson()

# -- 3. the cloak chest ----------------------------------------------------------------------------------------------
go(TABLE, 2, "the clothes table")
API.Pause(2.0)
chest = None
for it in API.GetItemsOnGround(4):
    if it.Graphic in (0x0E43, 0x0E42) and it.Hue == 0x4F2:
        chest = it
if check(chest is not None, "a chest stands by the clothes rack (at %s)" % ((chest.X, chest.Y, chest.Z) if chest else None,)):
    shot("chest", 1.0, clear=True)
    API.UseObject(chest.Serial)
    API.Pause(1.5)
    cloak = None
    for it in API.ItemsInContainer(chest.Serial):
        if it.Graphic in (0x1515, 0x1516):
            cloak = it
    shot("chest-open", 0.5)
    if check(cloak is not None, "the cloak of the Wakening Isle is in the chest"):
        API.MoveItem(cloak.Serial, API.Backpack)
        API.Pause(1.5)
        API.EquipItem(cloak.Serial)
        API.Pause(1.5)
    gone = True
    for it in API.GetItemsOnGround(4):
        if it.Serial == chest.Serial:
            gone = False
    check(gone, "the chest goes once the cloak is taken")
next_lesson()

# -- 4. chat ---------------------------------------------------------------------------------------------------------
go(SIGN, 2, "the signpost")
API.Msg("hello there")
API.Pause(1.5)
API.Msg("I am ready to learn")
next_lesson()

# -- 5. the farm: pitchfork, war mode, pests, then the pet --------------------------------------------------------------
go(WREN, 3, "Wren at the farm gate")
wren = mobiles_near(WREN, 2, name="Wren")
if check(len(wren) > 0, "Wren stands at the farm gate"):
    wren = wren[0]
    API.ClearJournal()
    API.UseObject(wren.Serial)
    check(wait_journal("Before the pests, a weapon", 6), "Wren hands the pitchfork first")
    check(not API.InJournal("Choose your farm pet"), "no pet before the pests")
    # run 6: moves too close together get "You must wait to perform another action", so pace them
    API.Pause(1.5)
    API.ClearRightHand()
    API.Pause(1.5)
    API.ClearLeftHand()
    API.Pause(1.5)
    fork = API.FindType(0x0E87, API.Backpack) or API.FindType(0x0E88, API.Backpack)
    if check(fork is not None, "Wren's pitchfork is in the backpack"):
        for _ in range(3):
            API.EquipItem(fork.Serial)
            if wait_journal("You hold the pitchfork", 5):
                break
            API.Pause(1.5)
    check(API.InJournal("You hold the pitchfork"), "holding the pitchfork counts")
    shot("pitchfork", 1.0, clear=True)
    API.SetWarMode(True)
    check(wait_journal("I opened the field gate", 6), "war mode counts, and Wren opens the gate")
    go(BELOW_WREN, 0, "the field gate")
    rounds, kinds = 0, set()
    shot_taken = False
    while rounds < 40 and not API.InJournal("The cabbage rows are clear"):
        ps = mobiles_near(PESTS, 14, graphics=(0xEE, 0xD7, 0x34))
        if not ps:
            API.Pause(3.0)
            rounds += 1
            continue
        p = min(ps, key=lambda m: abs(m.X - API.Player.X) + abs(m.Y - API.Player.Y))
        kinds.add(hex(p.Graphic))
        say("attack %s 0x%X at %s,%s" % (p.Name, p.Graphic, p.X, p.Y))
        API.Pathfind(p.X, p.Y, distance=1, wait=True, timeout=15)
        API.Attack(p.Serial)
        for _ in range(12):
            API.Pause(2.0)
            m = API.FindMobile(p.Serial)
            if m is None or m.IsDead or API.InJournal("The cabbage rows are clear"):
                break
            if abs(m.X - API.Player.X) > 1 or abs(m.Y - API.Player.Y) > 1:
                API.Pathfind(m.X, m.Y, distance=1, wait=True, timeout=10)
                API.Attack(m.Serial)
            if not shot_taken:
                shot("pests", 0.1)
                shot_taken = True
        rounds += 1
    check(API.InJournal("The cabbage rows are clear"), "the pests are cleared (kinds %s)" % sorted(kinds))
    API.Pause(1.0)
    check(find_gump("The cabbage rows are clear") is not None, "the lesson window says the rows are clear: back to Wren")
    shot("cleared", 0.5)
    API.SetWarMode(False)
    go(BELOW_WREN, 1, "back to Wren")
    API.UseObject(wren.Serial)
    g = wait_gump("Choose your farm pet", 8)
    if check(g is not None, "the pet window comes after the cleared rows: the pet is the reward"):
        shot("pet-choice", 0.5)
        reply("Choose your farm pet", 1)
    check(wait_journal("This pet is yours to keep", 6), "the System says the pet is yours")
    check(wait_journal("Pet Info", 6), "the System says how to see Pet Info")
    API.Pause(2.0)
    pet = None
    for m in mobiles_near((API.Player.X, API.Player.Y), 12, graphics=(0xD9, 0xC9)):
        pet = m
    if check(pet is not None, "the pet stands by (%s)" % ((pet.Name, hex(pet.Graphic), pet.X, pet.Y) if pet else None,)):
        shot("pet", 1.0, clear=True)
        API.ContextMenu(pet.Serial, PET_INFO_ENTRY)
        g = wait_gump("Pet Info:", 8)  # run 7 matched the color window by the pet name
        log_gumps("after the pet's menu, Pet Info")
        check(g is not None, "Pet Info from the pet's menu opens its window")
        shot("petinfo", 0.5)
        if g is not None:
            try:
                g.Dispose()
            except Exception:
                pass
    API.Msg("all follow me")
    check(wait_journal("Your pet follows you", 6), "'all follow me' counts")
    API.Pause(1.0)
    API.Msg("all guard me")
    check(wait_journal("Your pet guards you", 6), "'all guard me' counts")
    check(wait_journal("Lesson finished: The farm", 8), "the farm lesson is finished")
    next_lesson()

# -- 6. healing: Pip on his bench in the farmhouse -------------------------------------------------------------------
check(wait_journal("sits hurt on the bench", 6), "the healing lesson points at Pip in the farmhouse")
go(STEPS, 0, "the farmhouse steps")
steps("north", 3)
steps("northeast", 1)
pip = mobiles_near(PIP, 0, name="Pip")
check(len(pip) > 0, "Pip sits on his bench at %s (we stand at %s)" % (PIP, where()))
shot("pip", 1.0, clear=True)
band = API.FindType(0x0E21, API.Backpack)
healed = False
if check(band is not None, "bandages are in the backpack") and pip:
    for _ in range(4):
        API.ClearJournal()
        API.UseObject(band.Serial)
        if API.WaitForTarget("any", 5):
            API.Target(pip[0].Serial)
            say("bandage on Pip")
            if wait_journal("Your bandage restored health", 16):
                healed = True
                break
        API.Pause(1.5)
check(healed, "a bandage really heals Pip")
check(wait_gump(FINISHED, 10) is not None, "the healing lesson is finished")
shot("healed", 0.5)
steps("southwest", 1)
steps("south", 3)
check(abs(API.Player.X - STEPS[0]) <= 1 and abs(API.Player.Y - STEPS[1]) <= 1, "back out of the farmhouse (at %s)" % (where(),))

# -- 7. the dock to the moongate's landing, both ways ------------------------------------------------------------------
for wp in ((6720, 3990), (6750, 3992), (6790, 3992), (6812, 3991)):
    go(wp, 1, "the road")
go((6812, 3991), 0, "the road at the dock")
start = where()
for direction, stop in (("east", lambda p: p[0] >= 6830), ("west", lambda p: p[0] <= 6812)):
    last, stuck = where(), 0
    for i in range(40):
        API.Walk(direction)
        API.Pause(0.6)
        now = where()
        say("  %s step %d: %s" % (direction, i, now))
        if stop(now):
            break
        stuck = stuck + 1 if now == last else 0
        last = now
        if stuck >= 4:
            say("  %s: STUCK at %s" % (direction, now))
            break
    check(stop(where()), "the dock %s: reached %s" % (direction, where()))
    if direction == "east":
        shot("dock-landing", 1.0, clear=True)
say("end %s" % (where(),))
with open(SIG, "a") as f:
    f.write("END\n")
