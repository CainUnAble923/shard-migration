# cc-P751 (the P748 build review, item 6): a real character walks the isle in TazUO with the client's own steps (no
# teleport): the west beach past the wreck, then every lesson leg from the wake spot to the dock end, in and out of the
# farmhouse (its step and door), the bank door and the lodge door, and the dock back to the land. The route is
# walk-paths.json (walk_paths.py: the builder's walker on this branch's map). Each step's position and Z go to LOG, with
# the change in Z from the step before; a tile the client cannot reach in 8 tries is logged STUCK and the leg ends, and
# the next leg starts with the client's own pathfinding back to its start (logged RECOVER). At each door the walker
# signals a shot (SIG, read by isle-shots751.ps1). TazUO opens a door walked into, as a player's client does.
import API
import json

ROUTE = r"D:\UO\golems\Iron\shard-migration\notes\cc-P751-tools\walk-paths.json"
LOG = r"D:\UO\golems\Iron\p751-proof\isle-walk.log"
SIG = r"D:\UO\golems\Iron\p751-proof\walk-signal.txt"
DIRS = {(0, -1): "north", (1, -1): "northeast", (1, 0): "east", (1, 1): "southeast",
        (0, 1): "south", (-1, 1): "southwest", (-1, 0): "west", (-1, -1): "northwest"}
SHOTS = {"farmhouse: up the step and in at the door": "walk-farmhouse-in",
         "farmhouse: out at the door and down the step": "walk-farmhouse-out",
         "bank: in at the south door": "walk-bank-in", "bank: out at the south door": "walk-bank-out",
         "lodge: in at the north door": "walk-lodge-in", "lodge: out at the north door": "walk-lodge-out",
         "stop 9 to the dock end (stop 10, beside the moongate)": "walk-dock-end",
         "dock: back to the landing road": "walk-dock-back",
         "beach: west sand north past the wreck": "walk-beach"}


def say(text):
    with open(LOG, "a") as f:
        f.write(text + "\n")


def signal(text):
    with open(SIG, "a") as f:
        f.write(text + "\n")


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


def sign(v):
    # plain ints and no bool math: in TazUO's IronPython, (v > 0) - (v < 0) on the client's numbers made keys that
    # missed DIRS, so every such step was logged STUCK without a step being tried (the first walk, 2026-10-31; the
    # same trap as SL_Lumberjack's 2026-10-05 KeyError)
    v = int(v)
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0


def step_to(x, y):
    """One tile toward (x, y) with the client's own walk; up to 8 tries (a turn costs one)."""
    for _ in range(8):
        p = where()
        if (p[0], p[1]) == (x, y):
            return True
        d = DIRS.get((sign(int(x) - int(p[0])), sign(int(y) - int(p[1]))))
        if d is None:
            say("    no direction for (%d, %d) from %s" % (x, y, p))
            return False
        API.Walk(d)
        API.Pause(0.6)
    p = where()
    return (p[0], p[1]) == (x, y)


def walk_leg(leg):
    name, path = leg["name"], leg["path"]
    start = path[0]
    p = where()
    if (p[0], p[1]) != (start[0], start[1]):
        say("RECOVER: pathfinding from %s to the leg's start %s" % (p, tuple(start)))
        API.Pathfind(start[0], start[1], distance=0, wait=True, timeout=30)
    say("LEG %s: %d steps from %s" % (name, len(path) - 1, where()))
    last = where()
    worst = 0
    for i, t in enumerate(path[1:], 1):
        ok = step_to(t[0], t[1])
        now = where()
        dz = now[2] - last[2]
        worst = max(worst, abs(dz))
        say("  step %d: %s dZ %+d (walker %s)%s" % (i, now, dz, t[2], "" if ok else "  STUCK, wanted (%d, %d)" % (t[0], t[1])))
        last = now
        if name in SHOTS and i == min(len(path) - 1, max(1, (len(path) - 1) // 2 + 1)):
            signal("SHOT %s-mid" % SHOTS[name])
            API.Pause(2.5)
        if not ok:
            say("LEG %s: STUCK at %s" % (name, now))
            return False
    say("LEG %s: reached %s; largest step in Z %d" % (name, where(), worst))
    if name in SHOTS:
        signal("SHOT %s-end" % SHOTS[name])
        API.Pause(2.5)
    return True


API.Pause(5)
for _ in range(3):  # close the windows the login opens, so the frames show the isle (Clear741.py)
    for i in range(6):
        API.CloseGump()
        API.Pause(0.3)
    for g in API.GetAllGumps():
        try:
            g.Dispose()
        except Exception:
            pass
    API.Pause(2)
open(LOG, "w").close()
legs = json.load(open(ROUTE))
say("start %s, %s; %d legs" % (API.Player.Name, where(), len(legs)))
results = []
for leg in legs:
    results.append((leg["name"], walk_leg(leg)))
    API.Pause(0.8)
stuck = [n for n, ok in results if not ok]
say("end %s; %d of %d legs walked to their end%s" % (where(), len(results) - len(stuck), len(results),
                                                      "" if not stuck else "; stuck: " + "; ".join(stuck)))
signal("DONE")
