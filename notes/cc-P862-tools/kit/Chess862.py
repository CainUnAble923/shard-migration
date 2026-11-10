# cc-P862: Battle Chess in TazUO on the private proof shard. The board placed itself at world load in the Haven inn's yard
# (rim 3673-3682, 2628-2637, Trammel). chessbot862.py (the Golem's admin, through uobot) brings this trainee to the board
# and stands beside it as the opponent. The trainee opens the board, picks a set, invites the bot and plays Scholar's mate
# (as White) or its answer (as Black), then a second game with the Undead set that it resigns. "SHOT <name>" lines in SIG
# ask tazuo-walk.ps1 for a shot from the default camera.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Chess"
BX, BY, BZ = 3673, 2628, 0
STAND = (3672, 2635)   # one step north of where the bot puts the trainee (the step gets them up)
BOT_AT = (3670, 2637)
DARK = 0x050F
WHITE = ["e2e4", "f1c4", "d1h5", "h5f7"]
BLACK = ["e7e5", "b8c6", "g8f6"]


def sig(line):
    with open(SIG, "a") as f:
        f.write(line + "\n")


def say(text):
    # The log only: chat lines in the game view would cover the board in the shots.
    with open(LOG, "a") as f:
        f.write(text + "\n")


def close_others():
    # The new trainee's Wakening Isle window and other windows not of the game stay out of the shots.
    for g in API.GetAllGumps() or []:
        try:
            t = g.PacketGumpText or ""
            if t and ("What changed" in t or ("Battle Chess" not in t and "Resign" not in t)):
                g.Dispose()
        except Exception:
            pass


def shot(name, settle=1.5, after=2.5):
    close_others()
    API.Pause(settle)
    sig("SHOT " + name)
    API.Pause(after)


def check(ok, what):
    say(("PASS " if ok else "FAIL ") + what)
    return ok


def world(sq):
    f, r = ord(sq[0]) - 97, int(sq[1]) - 1
    return BX + 1 + f, BY + 8 - r, BZ + 5


def journal(text, seconds=30):
    out = []
    for e in API.GetJournalEntries(seconds) or []:
        if text in e.Text:
            out.append(e.Text)
    return out


def wait_journal(texts, timeout):
    for _ in range(int(timeout * 2)):
        for t in texts:
            hits = journal(t, 60)
            if hits:
                return hits[-1]
        API.Pause(0.5)
    return None


def bot():
    for m in API.GetAllMobiles(None, 14) or []:
        if m.X == BOT_AT[0] and m.Y == BOT_AT[1] and m.Serial != API.Player.Serial:
            return m
    return None


def open_board():
    squares = API.GetItemsOnGround(14, DARK) or []
    if not squares:
        return False
    API.UseObject(squares[0].Serial)
    API.Pause(2)
    return True


def invite(set_button):
    if not check(open_board(), "the board answers a double-click"):
        return False
    API.ReplyGump(set_button)
    API.Pause(1.5)
    API.ReplyGump(1)
    if not API.WaitForTarget("any", 6):
        check(False, "a cursor to choose the opponent")
        return False
    b = bot()
    if not check(b is not None, "the opponent stands by the board"):
        return False
    API.Target(b.Serial)
    return True


if API.Player.Name != CHARACTER:
    API.SysMsg("P862: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)
for i in range(180):
    if API.Player.X == STAND[0] and API.Player.Y == STAND[1] + 1:
        break
    API.Pause(1)
API.Pause(2)
for k in range(4):  # a new character wakes lying down; a step gets them up (the first may only turn them)
    if API.Player.Y == STAND[1]:
        break
    API.Walk("north")
    API.Pause(1.2)
API.Pause(4)
say("at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
check(API.Player.X == STAND[0] and API.Player.Y == STAND[1], "the trainee stands by the board's south-west corner")

squares = API.GetItemsOnGround(14, DARK) or []
check(len(squares) == 32, "the board's 32 dark squares stand in the inn's yard (%d)" % len(squares))
shot("01-board-in-the-inn-yard", 2)

# Game 1: the Classic set.
API.ClearJournal()
if invite(10):
    shot("02-invitation-sent", 0.5, 1.5)
    colour_line = wait_journal(["You play White", "You play Black"], 20)
    check(colour_line is not None, "the opponent accepted and the colours were drawn: %s" % colour_line)
    white = colour_line is not None and "You play White" in colour_line
    shot("03-classic-pieces-set-up", 3)

    moves = WHITE if white else BLACK
    for n, mv in enumerate(moves):
        if not API.WaitForTarget("any", 120):
            check(False, "my move's cursor came for %s" % mv)
            break
        API.Pause(1)
        fx, fy, fz = world(mv[:2])
        tx, ty, tz = world(mv[2:])
        API.Target(fx, fy, fz)
        API.WaitForTarget("any", 6)
        API.Pause(0.5)
        API.Target(tx, ty, tz)
        say("played %s" % mv)
        if n == 0:
            shot("04-a-pawn-walks", 0.5, 1)
        elif mv == "h5f7":
            shot("06-the-queen-strikes", 1.0, 0.2)
            shot("07-lightning-takes-the-pawn", 0.3, 0.5)
        elif n == len(moves) - 1 and not white:
            # The opponent's last move takes f7: shoot the fight as it comes.
            for k in range(5):
                shot("06-capture-%d" % k, 1.0, 0.2)

    over = wait_journal(["wins by checkmate", "drawn", "wins"], 40)
    check(over is not None and "checkmate" in over, "the game ends in checkmate: %s" % over)
    shot("08-checkmate", 1)
    rec = journal("Your Battle Chess record", 60)
    check(len(rec) > 0, "the record is told: %s" % (rec[-1] if rec else None))
    API.Pause(22)
    left = [m for m in (API.GetAllMobiles(None, 14) or []) if "white" in (m.Name or "") or "black" in (m.Name or "")]
    check(len(left) == 0, "the pieces left the board after the game (%d left)" % len(left))
    shot("09-board-free-again", 1)

# Game 2: the Undead set, resigned.
API.ClearJournal()
if invite(14):
    colour_line = wait_journal(["You play White", "You play Black"], 20)
    check(colour_line is not None, "the second game started: %s" % colour_line)
    shot("10-undead-pieces-set-up", 3)
    API.ReplyGump(2)  # Resign, in the game window
    API.Pause(1.5)
    API.ReplyGump(1)  # yes
    over = wait_journal(["resigns"], 10)
    check(over is not None, "resigning ends the game: %s" % over)
    shot("11-resigned", 1)
    API.Pause(22)

if open_board():
    shot("12-board-window-with-record", 1)

sig("END")
say("done")
