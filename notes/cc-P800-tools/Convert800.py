# cc-P800: an old League sash in a saved world, for run-convert.ps1. A new character takes a BoundCosmeticSash, labels it as P79's
# League sash bound to its account, and saves. The script's restarts of the shard do the rest; their logs are the proof.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CHARACTER = "Iron Old"
SASH = 0x1541


def say(text):
    API.SysMsg("P800: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


if API.Player.Name != CHARACTER:
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)
API.Pause(7)
API.Msg("[self AddToPack BoundCosmeticSash")
API.Pause(3)
it = API.FindType(SASH, API.Backpack)
say("old sash found: %s" % (it is not None))
if it is not None:
    for prop in ("BoundAccount iron-admin", "Label League"):  # one per [set: a multi-pair set does nothing
        API.Msg("[set %s" % prop)
        if API.WaitForTarget("any", 4):
            API.Target(it.Serial)
        API.Pause(2)
    for prop in ("BoundAccount", "Label"):
        API.Msg("[get %s" % prop)
        if API.WaitForTarget("any", 4):
            API.Target(it.Serial)
        API.Pause(2)
    API.Msg("[get Account")
    if API.WaitForTarget("any", 4):
        API.Target(API.Player.Serial)
    API.Pause(2)
    for e in API.GetJournalEntries(30) or []:
        if "skill in" not in e.Text and "P800" not in e.Text:
            say("journal: " + e.Text)
    say(str(API.ItemNameAndProps(it.Serial, True, 3)))
API.Msg("[save")
API.Pause(6)
with open(SIG, "a") as f:
    f.write("SHOT saved\n")
API.Pause(3)
with open(SIG, "a") as f:
    f.write("END\n")
say("done")
