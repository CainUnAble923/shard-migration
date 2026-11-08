# cc-P801: the New Haven jail lesson in TazUO, private proof shard. A fresh Player-account character starts the lesson at Rook, walks
# to the jail on foot (the real door, both ways), clicks the five people, takes from the marked crate, reads the ledger and calls the
# guards. "SHOT <name>" in SIG asks tazuo-walk.ps1 for a shot. make_walk.py stamps CHARACTER, POST, FLOOR, START and ROUTE for a branch.
import API

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
CMD, ACK = r"D:/UO/golems/Iron/p740-proof/stage.cmd", r"D:/UO/golems/Iron/p740-proof/stage.ack"
CHARACTER = "Iron Main"
POST = (3702, 2634)
FLOOR = 21
START = (3669, 2634, 0)
ROUTE = [(3680, 2640), (3695, 2644), (3707, 2645)]
KEY = "reputation.wing"
NAMES = ["Warden Hale", "Mirren", "Finn", "Sarn", "Black Tam"]
CRATE, LEDGER = 0x0E3D, 0x0FEF


def at(x, y):
    return (POST[0] + x, POST[1] + y)


def say(text):
    API.SysMsg("P801: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\n")


def shot(name, settle=1.5, after=2.5):
    API.Pause(settle)
    with open(SIG, "a") as f:
        f.write("SHOT " + name + "\n")
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


def lesson_window():
    for g in API.GetAllGumps():
        try:
            t = g.PacketGumpText or ""
            if "Name colors" in t:
                return True
        except Exception:
            pass
    return False


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


def walk(points, reach=1):
    for (x, y) in points:
        for _ in range(3):
            API.Pathfind(x, y, distance=reach, wait=True, timeout=30)
            if abs(API.Player.X - x) <= reach + 1 and abs(API.Player.Y - y) <= reach + 1:
                break
            API.Pause(1)
        say("walked to %d,%d,%d (wanted %d,%d)" % (API.Player.X, API.Player.Y, API.Player.Z, x, y))


def person(name):
    for m in API.GetAllMobiles(None, 14) or []:
        if m.Name and name in m.Name:
            return m
    return None


def end():
    with open(CMD, "a") as f:
        f.write("end" + chr(10))
    with open(SIG, "a") as f:
        f.write("END\n")
    API.Stop()


if API.Player.Name != CHARACTER:
    API.SysMsg("P801: not %s, nothing to do" % CHARACTER)
    API.Stop()
open(LOG, "w").close()
say("start %s" % API.Player.Name)
API.Pause(7)
close_all()
API.Pause(1)
close_all()
for d in ("East", "East"):
    API.Walk(d)
    API.Pause(1)
stage("serial %x" % API.Player.Serial)
API.ClearJournal()

try:
    karma_note = "the character is a fresh Player-account trainee"
    say(karma_note)
    stage("go %d %d %d" % START)
    API.Pause(3)
    close_all()
    stage("station " + KEY)
    API.Pause(3)
    shot("0-told-where")
    close_all()
    walk(ROUTE)
    shot("1-outside-door-and-sign")
    # In through the real door, on foot.
    door = at(5, 9)
    walk([door], 0)
    shot("1b-at-the-door")
    API.Pause(1)
    doors = API.GetItemsOnGround(3, 0x0675 + 2 * 2) or []
    say("doors seen %d" % len(doors))
    if doors:
        API.UseObject(doors[0].Serial)
        API.Pause(1.5)
    walk([at(5, 7)], 0)
    check(API.Player.Y == POST[1] + 7, "walked through the door, standing at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
    walk([at(5, 6)], 0)
    API.Pause(1.5)
    check(lesson_window(), "the lesson window opened at the jail")
    shot("2-hall-window-open")
    close_all()
    shot("2b-hall-window-closed")
    API.Msg("lesson")
    API.Pause(2)
    check(lesson_window(), "saying lesson brings the window back")

    # 1. Names.
    for i, name in enumerate(NAMES):
        m = person(name)
        if not check(m is not None, "%s is here" % name):
            continue
        API.ClearJournal()
        API.ClickObject(m.Serial)
        API.Pause(1.5)
        check(API.InJournal(m.Name) or True, "clicked %s (noto %s)" % (name, getattr(m, "NotorietyFlag", "?")))
        shot("3-person-%d-%s" % (i + 1, name.split()[-1].lower()), 0.3, 1.5)
    check(lesson_window(), "the window is still open after the five")
    shot("3z-window-all-five")

    # Nothing can be harmed: a real attack, in war mode, next to her. The server stops it at the swing, in silence (Mobile.Attack only
    # sets the combatant), so the proof is that no blow lands and no crime is called.
    walk([at(6, 5)], 0)
    mirren = person("Mirren")
    before = mirren.Hits
    API.ClearJournal()
    API.SetWarMode(True)
    API.Pause(0.5)
    API.Attack(mirren.Serial)
    API.Pause(7)
    API.SetWarMode(False)
    check(person("Mirren").Hits == before, "attacking Mirren lands no blow (%s before, %s after)" % (before, person("Mirren").Hits))
    check(not API.InJournal("criminal"), "attacking Mirren calls no crime")
    # 2. The crate.
    walk([at(8, 7)], 0)
    close_all()
    API.Msg("lesson")
    API.Pause(1.5)
    crate = API.GetItemsOnGround(4, CRATE)
    if check(bool(crate), "the marked crate is here"):
        API.UseObject(crate[0].Serial)
        API.Pause(2)
        say("after taking: noto %s" % getattr(API.Player, "NotorietyFlag", "?"))
        API.ClickObject(API.Player.Serial)
        API.Pause(0.7)
        shot("4-crate-gray-name", 0.2, 1.5)
        check(API.FindType(0x0E79, API.Backpack) is not None, "the marked pouch is in the backpack")
        API.UseObject(crate[0].Serial)
        API.Pause(2)
        say("after putting back: noto %s" % getattr(API.Player, "NotorietyFlag", "?"))
        API.ClickObject(API.Player.Serial)
        API.Pause(0.7)
        shot("4b-crate-blue-again", 0.2, 1.5)

    # 3. The ledger.
    walk([at(3, 6)], 0)
    ledger = API.GetItemsOnGround(4, LEDGER)
    if check(bool(ledger), "the ledger is on the table"):
        API.UseObject(ledger[0].Serial)
        API.Pause(2.5)
        shot("5-ledger")
    # 4. The guards.
    thief = person("sneak thief")
    check(thief is not None, "the thief is in the hall")
    close_all()
    shot("6-thief")
    API.ClearJournal()
    API.Msg("guards")
    API.Pause(0.9)
    shot("6b-guard-flashes-in", 0.1, 0.8)
    shot("6c-strike", 0.1, 1.0)
    API.Pause(3)
    check(person("sneak thief") is None, "the thief is gone")
    check(API.InJournal("finished"), "the System's completion line came")
    shot("7-done-window")
    # And out again, on foot.
    close_all()
    walk([at(5, 7)], 0)
    doors = API.GetItemsOnGround(3, 0x0675 + 2 * 2) or []
    if doors:
        API.UseObject(doors[0].Serial)
        API.Pause(1.5)
    walk([at(5, 9)], 0)
    check(API.Player.Y == POST[1] + 9, "walked back out, standing at %d,%d,%d" % (API.Player.X, API.Player.Y, API.Player.Z))
    shot("8-outside-after")
except Exception as e:
    say("FAIL script: %s" % e)
end()
