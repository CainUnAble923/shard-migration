# cc-P763: Iron the Tester (made a GameMaster on the private world copy only, so [LootBox give works) stands in
# Britain (guarded), is given boxes of several themes, grades, rarities and seasons, and opens each with the client's
# own double-click; the runner (isle-shots742.ps1, its "sig" file) takes a shot of each reveal. Logs to LOG.
import API

LOG = r"D:\UO\golems\Iron\p763-proof\loot.log"
SIG = r"D:\UO\golems\Iron\p763-proof\loot-signal.txt"
CHARACTER = "Iron the Tester"
BOX = 0x09AA
BOXES = [
    ("Explorer 3 Epic none", "loot-01-epic-explorer"),
    ("Miner 4 Rare none", "loot-02-rare-miner"),
    ("Scholar 6 Legendary none", "loot-03-legendary-scholar"),
    ("Fisher 2 Common halloween", "loot-04-halloween-fisher"),
    ("Sailor 3 Epic winter", "loot-05-winter-epic-sailor"),
    ("Herbalist 2 Rare spring", "loot-06-spring-herbalist"),
    ("Boss 5 Legendary none", "loot-07-legendary-boss"),
]


def say(text):
    with open(LOG, "a") as f:
        f.write(text + "\n")
    API.SysMsg("P763: " + text)


def signal(text):
    with open(SIG, "a") as f:
        f.write(text + "\n")


def clear():
    for _ in range(4):
        API.CloseGump()
        API.Pause(0.3)


def boxes():
    found = []
    for it in API.ItemsInContainer(API.Backpack):
        if int(it.Graphic) == BOX:
            found.append(int(it.Serial))
    return found


if API.Player.Name != CHARACTER:
    API.SysMsg("P763: not %s, the script does not run" % CHARACTER)
else:
    API.Pause(6)
    clear()
    say("start at %s,%s" % (API.Player.X, API.Player.Y))
    for args, shot in BOXES:
        before = set(boxes())
        API.ClearJournal()
        API.Msg("[LootBox give " + args)
        new = []
        for _ in range(20):
            API.Pause(0.5)
            new = [s for s in boxes() if s not in before]
            if new:
                break
        if not new:
            say("FAIL no box for %s" % args)
            continue
        API.Pause(1.0)
        API.UseObject(new[0])
        API.Pause(3.0)
        opened = API.InJournal("You open the")
        say(("PASS " if opened else "FAIL ") + "%s opened" % args)
        signal("SHOT " + shot)
        API.Pause(2.0)
        clear()
        API.Pause(1.0)
    say("END")
    signal("DONE")
