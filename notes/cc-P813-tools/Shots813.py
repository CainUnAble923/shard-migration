# cc-P813: the TazUO shots of Chase's Claude Design gumps in use and the Finishers banner placed. Runs in the Player's
# TazUO (Iron the Tester) on the private proof shard; the Golem's admin (stage813.py) types the staff commands it asks
# for through a file. Each shot is asked of shots813.ps1 with a "SHOT <name>" line in SIG; "DONE" ends the run.
import API

BASE = "D:\\UO\\golems\\Iron\\p813-proof\\"
CMD = BASE + "stage.cmd"
ACK = BASE + "stage.ack"
SIG = BASE + "shot-signal.txt"
LOG = BASE + "shots813.log"
ME = "Iron the Tester"
WHERE = 'where playermobile Name == "' + ME + '"'
asked = [0]


def say(text):
    with open(LOG, "a") as f:
        f.write(text + "\n")


def signal(text):
    with open(SIG, "a") as f:
        f.write(text + "\n")


def acked():
    try:
        with open(ACK) as f:
            return len([l for l in f.read().splitlines() if l.strip()])
    except Exception:
        return 0


def stage(line, wait=30):
    with open(CMD, "a") as f:
        f.write(line + "\n")
    asked[0] += 1
    for _ in range(int(wait * 2)):
        if acked() >= asked[0]:
            say("staged: " + line)
            return True
        API.Pause(0.5)
    say("NOT STAGED: " + line)
    return False


def clear():
    for _ in range(2):
        for i in range(6):
            API.CloseGump()
            API.Pause(0.2)
        for g in API.GetAllGumps():
            try:
                g.Dispose()
            except Exception:
                pass
        API.Pause(1)


def shot(name, settle=3):
    API.Pause(settle)
    signal("SHOT " + name)
    API.Pause(3)
    say("shot " + name)


API.Pause(8)
clear()
say("at %d,%d,%d" % (int(API.Player.X), int(API.Player.Y), int(API.Player.Z)))
stage("cmd [global set Blessed True " + WHERE)

# 1. "Didn't Read the Sign": revoked and granted again, so the popup shows as it does at the moongate.
stage("cmd [ClusterFAchievement revoke tutorial.gateSkip {user}")
stage("cmd [ClusterFAchievement grant tutorial.gateSkip {user}")
shot("skip-achievement-popup")
clear()

# 2. The pet choice scroll, from the Player's own backpack.
stage("cmd [global addtopack PetChoiceScroll " + WHERE)
API.Pause(2)
scroll = API.FindType(0x0E34, API.Backpack)
if scroll:
    API.UseObject(scroll.Serial)
    shot("pet-choice-scroll")
else:
    say("NO SCROLL in the backpack")
clear()

# 3. The League shop, as a player opens it.
API.Msg("[leagueshop")
shot("league-shop")
clear()

# 4. The Finishers banner, placed by staff two tiles south-east of the Player (it draws below him, clear of the
#    windows at the top left), and one more beside it.
x, y, z = int(API.Player.X), int(API.Player.Y), int(API.Player.Z)
stage("addat %d %d %d FinishersBanner" % (x + 2, y + 2, z))
stage("addat %d %d %d FinishersBanner" % (x + 3, y + 1, z))
shot("finishers-banner", 4)

stage("end", 5)
signal("DONE")
say("done")
