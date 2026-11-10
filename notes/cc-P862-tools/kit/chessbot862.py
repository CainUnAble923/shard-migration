"""cc-P862: the opponent for the Battle Chess proof (stage867.py's login). A real trainee is on a Player account and has
no commands, so this bot logs the Golem's admin in on the private proof shard, moves the trainee (TazUO) to the board in
the Haven inn's yard, stands beside it as the second player, accepts each invitation, and plays the moves of whichever
colour it was given: Scholar's mate for White (e4, Bc4, Qh5, Qxf7#), and e5, Nc6, Nf6 for Black. The second game it
just accepts (the trainee resigns it). Each step goes to the transcript and stdout.

    python -P chessbot862.py [--port 2596] [--name "Iron Chess"]
"""
import argparse
import re
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, default=2596)
ap.add_argument("--name", default="Iron Chess")
ap.add_argument("--bot", default=r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
a = ap.parse_args()
sys.path.insert(0, a.bot)
from uobot.client import Client, Cliloc, Transcript  # noqa: E402
from uobot import golemcheck as GC  # noqa: E402

BASE = r"D:\UO\golems\Iron\p740-proof"
BX, BY, BZ = 3673, 2628, 0           # the board's rim, north-west corner (battle-chess.json defaults)
TRAINEE = (3672, 2636, 0)            # by the south-west corner: the default camera frames the board right of them
ME = (3670, 2637, 0)
WHITE = ["e2e4", "f1c4", "d1h5", "h5f7"]
BLACK = ["e7e5", "b8c6", "g8f6"]


def world(sq):
    f, r = ord(sq[0]) - 97, int(sq[1]) - 1
    return BX + 1 + f, BY + 8 - r, BZ + 5


tr = Transcript(BASE + r"\stage\chessbot-transcript.txt")
cl = Cliloc(r"D:\UO\tool-trials\client-data-copy\Cliloc.enu", r"D:\UO\bot-shard\cache")
user, pw = GC.account("Iron", "admin")
c = None
for _ in range(120):
    try:
        c = Client(user, pw, tr, cl, label="chessbot", test_target=("127.0.0.1", a.port))
        chars = c.login()
        break
    except Exception:
        c = None
        time.sleep(3)
pw = None
if c is None:
    sys.exit("no shard")


def say(t):
    print(time.strftime("%H:%M:%S"), t, flush=True)


say("characters %s" % chars)
if not chars:
    c.create("Iron Stage")
else:
    c.play(0)
c.sleep(4)
c.command("[self set Map Trammel", 1)
c.command("[self set Hidden False", 1)
c.command("[self set Location (%d,%d,%d)" % ME, 2)
for line in c.command("[BattleChess status", 2):
    say("status: %s" % line.get("text"))

# Bring the trainee to the board once they are in the world.
where = 'where playermobile Name == "%s"' % a.name
loc = "(%d,%d,%d)" % TRAINEE
for i in range(90):
    r = c.command("[global set Map Trammel %s" % where, 1)
    if any("has been set" in str(m.get("text")) for m in r):
        for prop, val in (("Location", loc), ("LogoutMap", "Trammel"), ("LogoutLocation", loc), ("Blessed", "True")):
            r = c.command("[global set %s %s %s" % (prop, val, where), 1)
            say("trainee %s %s: %s" % (prop, val, [m.get("text") for m in r][:2]))
        break
    c.sleep(2)
else:
    say("the trainee never came")

# Then play: accept each invitation, learn the colour, answer each move cursor.
games = 0
seen = 0
deadline = time.time() + 18 * 60
while time.time() < deadline and games < 2:
    g = c.wait_gump(lambda g: "invites you" in " ".join(c.gump_text(g)), timeout=30, since=seen)
    if not g:
        continue
    seen = c.gumps.index(g) + 1
    games += 1
    mark = len(c.messages)
    c.sleep(1)
    c.reply_gump(g, 1)
    m = c.find_text(r"You play (White|Black)", since=mark, timeout=10)
    colour = re.search(r"You play (White|Black)", m["text"]).group(1) if m else "?"
    say("game %d: I play %s" % (games, colour))
    if games == 2:
        c.find_text(r"resigns|wins|drawn|stopped", since=mark, timeout=300)
        say("game 2 over")
        continue

    moves = list(WHITE if colour == "White" else BLACK)
    while moves:
        mark2 = len(c.messages)
        if not c.wait_target(120):
            say("no cursor came")
            break
        mv = moves.pop(0)
        c.sleep(1.5)
        c.target_xyz(*world(mv[:2]))
        if not c.wait_target(10):
            say("no second cursor after %s" % mv[:2])
            break
        c.sleep(0.8)
        c.target_xyz(*world(mv[2:]))
        say("played %s" % mv)
        c.sleep(1)
        for t in c.texts_since(mark2):
            if "check" in t.lower() or "refus" in t.lower() or "can't" in t.lower():
                say("  text: %s" % t)
    m = c.find_text(r"checkmate|wins|drawn", since=mark, timeout=120)
    say("game 1 ended: %s" % (m["text"] if m else "?"))

for line in c.command("[BattleChess status", 2):
    say("status: %s" % line.get("text"))
say("done")
c.close()
