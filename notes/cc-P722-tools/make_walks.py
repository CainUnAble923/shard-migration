"""cc-P722: write the real-character walk scripts (Legion, run inside TazUO) and the shot spec that starts them.

Each walk is P720's IsleBridgeWalk.py made general: legs of (direction, stop test); every step is the client's own
movement (API.Walk), so the server's own checks decide; doors open the way TazUO opens them for a player (Auto open
doors, on by default). Each step's position goes to the journal and to D:\\UO\\golems\\Iron\\p722-proof\\walk-<name>.log.
A leg that does not move for 4 steps logs STUCK. Usage: make_walks.py <out folder>
"""
import json
import os
import sys

OUT = sys.argv[1]
LOGDIR = "D:" + chr(92) + "UO" + chr(92) + "golems" + chr(92) + "Iron" + chr(92) + "p722-proof"

# name: start (x, y, z), legs [(direction, axis, op, value)], what
WALKS = {
    # the dock to the moongate's landing (stops short of the gate at x 6832) and back to the road
    "bridge": ((6812, 3991, 0), [("east", 0, ">=", 6830), ("west", 0, "<=", 6812)],
               "the dock by the moongate, east onto the landing and back west to the road"),
    # the practice bank: its door is in the south wall at 6762,3980; the floor is y 3973-3980
    "bank": ((6762, 3984, 0), [("north", 1, "<=", 3978), ("south", 1, ">=", 3984)],
             "into the practice bank through its south door, to the counter, and back out"),
    # cc-P722: the bank again, round the lesson's signpost (6762,3982, on the door's line): east, north, west, in
    "bank2": ((6762, 3984, 0), [("east", 0, ">=", 6763), ("north", 1, "<=", 3981), ("west", 0, "<=", 6762),
                                ("north", 1, "<=", 3978), ("west", 0, "<=", 6762), ("south", 1, ">=", 3981),
                                ("east", 0, ">=", 6763), ("south", 1, ">=", 3984)],
              "round the bank's lesson sign and in through the south door to the counter, then back to the door"),
    # the League lodge: its door is in the north wall at 6782,3995; Elara stands at 6782,3999
    "lodge": ((6782, 3991, 0), [("south", 1, ">=", 3997), ("north", 1, "<=", 3991)],
              "into the League lodge through its north door, to Elara's desk, and back out"),
    # Wren's farmhouse (OSI's cottage): its door is in the south wall at 6690,3978, its floor at z 7
    "farmhouse": ((6690, 3982, 0), [("north", 1, "<=", 3975), ("south", 1, ">=", 3982)],
                  "into Wren's farmhouse through its south door and back out"),
}

TEMPLATE = '''# cc-P722: a real character walks {what}, step by step, in TazUO (the client's own movement, the
# server's own checks; no teleport). Made by notes/cc-P722-tools/make_walks.py from P720's IsleBridgeWalk.py.
import API

LOG = r"{log}"
LEGS = {legs!r}


def say(text):
    API.SysMsg("Walk {name}: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\\n")


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


def done(pos, axis, op, value):
    return pos[axis] >= value if op == ">=" else pos[axis] <= value


API.Pause(8)
say("start %s" % (where(),))
for direction, axis, op, value in LEGS:
    last = where()
    stuck = 0
    for i in range(40):
        API.Walk(direction)
        API.Pause(0.6)
        now = where()
        say("%s step %d: %s" % (direction, i, now))
        if done(now, axis, op, value):
            say("%s: reached %s" % (direction, now))
            break
        stuck = stuck + 1 if now == last else 0
        last = now
        if stuck >= 4:
            say("%s: STUCK at %s" % (direction, now))
            break
    API.Pause(1)
say("end %s" % (where(),))
'''

who = '"Iron the Tester"'
spec = []
for name, (start, legs, what) in WALKS.items():
    script = "Walk" + name.capitalize() + ".py"
    log = LOGDIR + chr(92) + "walk-" + name + ".log"
    with open(os.path.join(OUT, script), "w", encoding="ascii", newline="\n") as f:
        f.write(TEMPLATE.format(what=what, log=log, legs=legs, name=name))
    loc = "(%d,%d,%d)" % start
    spec.append({
        "name": "walk-" + name,
        "character": "Iron the Tester",
        "commands": [
            "[global set Map TheFold where playermobile Name == " + who,
            "[global set Location " + loc + " where playermobile Name == " + who,
            "[global set LogoutMap TheFold where playermobile Name == " + who,
            "[global set LogoutLocation " + loc + " where playermobile Name == " + who,
        ],
        "what": "a real character walks " + what + " (" + script + ")",
        "legion": script,
        "settle": 10,
        "frames": 40,
        "frameMs": 1000,
    })
with open(os.path.join(OUT, "walks.json"), "w", encoding="ascii", newline="\n") as f:
    json.dump(spec, f, indent=1)
print("wrote", len(spec), "walks")
