# cc-P863: Color Wars in TazUO on the private proof shard. As staff: the Staff Hub's Events tab and its new Color Wars
# button, the arena opened on the meadow by Britain's south road (1987-2002, 2237-2246, Trammel) for 2 teams, the gate
# placed west of it, and the other team's player (the uobot client foe863.py, "Iron the Tester" on the Golem's Player
# account) brought beside the gate; it steps in and answers Join. The battle is started. Then this character drops to
# Player, steps into the gate for real, answers Join, finds itself in its team's colour with the lent kit, walks to the
# other player and fights. This proof copy ends Color Wars at the first kill (CwKillsToWin 1, proof-shard.ps1), so the
# kill also shows the winners' tokens and everyone home with their own things. "SHOT <name>" lines in SIG ask
# tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
FOE_CMD, FOE_ACK = r"D:/UO/golems/Iron/p740-proof/foe.cmd", r"D:/UO/golems/Iron/p740-proof/foe.ack"
CHARACTER = "Iron Wars"
FOE = "Iron the Tester"
C1 = (1987, 2237)
C2 = (2002, 2246)
GATE = (1983, 2242)
MEADOW = (1980, 2244)


def sig(line):
    with open(SIG, "a") as f:
        f.write(line + "\n")


def say(text):
    API.SysMsg("P863: " + text)
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
    for g in API.GetAllGumps() or []:
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


def go(x, y):
    API.Msg("[self set Location (%d,%d,0)" % (x, y))
    API.Pause(2)


_asked = 0


def foe(line, seconds=40):
    global _asked
    _asked += 1
    with open(FOE_CMD, "a") as f:
        f.write(line + "\n")
    for _ in range(seconds * 2):
        with open(FOE_ACK) as f:
            if str(_asked) in f.read().split():
                return True
        API.Pause(0.5)
    say("FAIL the other player did not answer " + line)
    return False


def find_foe():
    for m in API.GetAllMobiles() or []:
        try:
            if FOE in (m.Name or ""):
                return m
        except Exception:
            pass
    return None


def gump_with(text):
    for g in API.GetAllGumps() or []:
        try:
            if text in (g.PacketGumpText or ""):
                return g
        except Exception:
            pass
    return None


if API.Player.Name != CHARACTER:
    API.SysMsg("P863: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)
API.Pause(7)
close_all()

API.Msg("[self set Map Trammel")
API.Pause(1)
go(MEADOW[0], MEADOW[1])
close_all()
say("at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))

# ---------------------------------------------------------------- staff: the hub, the arena, the gate
API.Msg("[SL")
API.Pause(2.5)
API.ReplyGump(4)          # the Events tab
API.Pause(2.5)
shot("1-staff-hub-events-tab")
API.ReplyGump(5011)       # Color Wars
API.Pause(2.5)
shot("2-color-wars-gump-closed")
close_all()

go(C1[0], C1[1])
API.Msg("[ColorWars corner1")
API.Pause(1)
go(C2[0], C2[1])
API.Msg("[ColorWars corner2")
API.Pause(1)
API.ClearJournal()
API.Msg("[ColorWars open 2")
check(wait_journal("Color Wars arena open", 6), "the arena is open for two teams")
go(GATE[0], GATE[1])
API.ClearJournal()
API.Msg("[ColorWars gate")
check(wait_journal("Color Wars is open!", 6), "the gate is placed and the shard is told")

# The other team's player, beside the gate: it steps in and answers Join.
API.Msg('[global set Location (%d,%d,0) where playermobile Name == "%s"' % (GATE[0] - 1, GATE[1], FOE))
API.Pause(2)
go(GATE[0] - 2, GATE[1] + 2)
API.ClearJournal()
foe("join e")
API.Pause(1)
API.ClearJournal()
API.Msg("[ColorWars status")
check(wait_journal(" 1 players", 5), "the other player stepped into the gate and joined a team")
API.Msg("[ColorWars")
API.Pause(2.5)
shot("3-color-wars-gump-open")
close_all()

API.ClearJournal()
API.Msg("[ColorWars start")
check(wait_journal("The battle has begun", 6), "staff start the battle")
# On this proof copy the other player is left one hit from death, so one landed blow ends the fight.
API.Msg('[global set Hits 1 where playermobile Name == "%s"' % FOE)
API.Pause(1)

# ---------------------------------------------------------------- a player now
go(GATE[0], GATE[1] + 1)
API.Msg("[self set Blessed False")
API.Pause(1)
API.Msg("[self set AccessLevel Player")
API.Pause(1.5)
own = API.FindType(0x0EED, API.Backpack)
say("own gold in the pack before: %s" % ("yes, %d" % own.Amount if own else "none"))
API.UseObject(API.Backpack)
API.Pause(1.5)
shot("4-before-the-gate-own-things")
close_all()

API.ClearJournal()
API.Walk("north")
API.Pause(2)
check(gump_with("join a team") is not None, "stepping into the gate asks first")
shot("5-the-gate-asks", 0.5)
API.ReplyGump(1)          # Join
check(wait_journal("You join the", 8), "joined a team")
API.Pause(2)
inside = C1[0] <= API.Player.X <= C2[0] and C1[1] <= API.Player.Y <= C2[1]
check(inside, "in the arena at %d,%d" % (API.Player.X, API.Player.Y))
API.UseObject(API.Backpack)
API.Pause(1.5)
shot("6-in-the-arena-with-the-kit")
close_all()

# ---------------------------------------------------------------- the fight
f = find_foe()
check(f is not None, "the other player is in view")
API.SetWarMode(True)
won = False
for _ in range(60):
    f = find_foe()
    if f is None or API.InJournal("has won Color Wars"):
        break
    if abs(f.X - API.Player.X) > 1 or abs(f.Y - API.Player.Y) > 1:
        API.Pathfind(f.X, f.Y, distance=1, wait=True, timeout=15)
    API.Attack(f.Serial)
    API.Pause(2.0)
    if API.InJournal("defeats"):
        shot("7-the-kill", 0.2, 1.5)
        break
won = wait_journal("has won Color Wars", 10)
check(won, "the first kill won Color Wars (this proof copy's setting)")
check(wait_journal("Festival Token", 5), "the winners are paid Festival Tokens")
API.SetWarMode(False)
API.Pause(2)
check(abs(API.Player.X - GATE[0]) <= 1 and abs(API.Player.Y - (GATE[1] + 1)) <= 1,
      "home where this character joined (%d,%d)" % (API.Player.X, API.Player.Y))
API.UseObject(API.Backpack)
API.Pause(1.5)
back = API.FindType(0x0EED, API.Backpack)
check(back is not None, "own things back in the pack")
shot("8-won-and-home-with-own-things")
foe("where")
foe("end", 10)
say("done")
