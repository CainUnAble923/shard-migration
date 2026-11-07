# cc-P811: the casino in TazUO on the private proof shard. The machines and the table placed themselves at world load in the
# Haven inn's east room (3670-3672, 2608-2610, Trammel). The character plays the slots and a hand of blackjack and reads
# [Casino status before and after. "SHOT <name>" lines in SIG ask tazuo-walk.ps1 for a shot.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Casino"
STAND = (3671, 2609, 0)
SLOT, TABLE = 0x9A96, 0xB34


def sig(line):
    with open(SIG, "a") as f:
        f.write(line + "\n")


def say(text):
    API.SysMsg("P811: " + text)
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


def journal(text, seconds=20):
    out = []
    for e in API.GetJournalEntries(seconds) or []:
        if text in e.Text:
            out.append(e.Text)
    return out


if API.Player.Name != CHARACTER:
    API.SysMsg("P811: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)
API.Pause(9)
close_all()

API.Msg("[self set Map Trammel")
API.Pause(1)
API.Msg("[self set Location (%d,%d,%d)" % STAND)
API.Pause(4)
close_all()
say("at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))

slots = API.GetItemsOnGround(4, SLOT) or []
tables = API.GetItemsOnGround(4, TABLE) or []
check(len(slots) == 2, "two slot machines stand in the room (%d)" % len(slots))
check(len(tables) >= 1, "the blackjack table stands in the room (%d)" % len(tables))
shot("1-casino-room", 2)

API.ClearJournal()
API.Msg("[Casino status")
API.Pause(2)
for line in journal("Casino") + journal("Slots:") + journal("Blackjack:"):
    say("books before: " + line)
shot("2-books-before", 0.5)

# The slots: ten pulls at 100 gold.
if slots:
    API.UseObject(slots[0].Serial)
    API.Pause(2)
    shot("3-slot-machine", 1)
    API.ReplyGump(11)  # the 100 gold bet
    API.Pause(1.5)
    wins = 0
    for i in range(10):
        API.ClearJournal()
        API.ReplyGump(1)
        API.Pause(1.6)
        if journal("you win"):
            wins += 1
            say("win: " + journal("you win")[0])
    say("ten pulls, %d win(s)" % wins)
    shot("4-slot-after-pulls", 0.5)
    close_all()

# A hand of blackjack at 100 gold: stand on what comes.
if tables:
    API.UseObject(tables[0].Serial)
    API.Pause(2)
    shot("5-blackjack-table", 1)
    API.ReplyGump(1)  # deal
    API.Pause(2)
    shot("6-blackjack-dealt", 1)
    API.ReplyGump(3)  # stand (does nothing if the deal settled it)
    API.Pause(2)
    shot("7-blackjack-result", 1)
    close_all()

API.ClearJournal()
API.Msg("[Casino status")
API.Pause(2)
lines = journal("Slots:") + journal("Blackjack:") + journal("Gold taken")
for line in lines:
    say("books after: " + line)
check(any("Slots: today in 1,000" in l for l in lines), "the books count the ten pulls")
shot("8-books-after", 0.5)

sig("END")
say("done")
