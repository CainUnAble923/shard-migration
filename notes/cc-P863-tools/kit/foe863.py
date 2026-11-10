"""cc-P863: the other team for the Color Wars proof. A second real player (the Golem's Player account, "Iron the Tester")
logs in with the uobot client and does what Walk863.py asks through a file: one line per request in FOE_CMD, each
answered by its line number in FOE_ACK. "join <dir>" (n, e, s or w) walks up to two steps (onto the gate), waits for the gate's question and
answers Join; "where" logs where it stands; "end" logs out. Private proof shard only (the client's test_target guard).

    python -P foe863.py [--port 2596]
"""
import argparse
import os
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, default=2596)
ap.add_argument("--bot", default=r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
a = ap.parse_args()
sys.path.insert(0, a.bot)
from uobot.client import Client, Cliloc, Transcript  # noqa: E402
from uobot import golemcheck as GC  # noqa: E402

BASE = r"D:\UO\golems\Iron\p740-proof"
CMD, ACK = os.path.join(BASE, "foe.cmd"), os.path.join(BASE, "foe.ack")
OUT = os.path.join(BASE, "foe")
os.makedirs(OUT, exist_ok=True)
for f in (CMD, ACK):
    open(f, "w").close()

NAME = "Iron the Tester"
tr = Transcript(os.path.join(OUT, "foe-transcript.txt"))
cl = Cliloc(r"D:\UO\tool-trials\client-data-copy\Cliloc.enu", r"D:\UO\bot-shard\cache")
user, pw = GC.account("Iron", "player")
c = None
for _ in range(120):
    try:
        c = Client(user, pw, tr, cl, label="foe", test_target=("127.0.0.1", a.port))
        chars = c.login()
        break
    except Exception:  # the shard is still loading
        c = None
        time.sleep(3)
pw = None
if c is None:
    sys.exit("no shard")
print("characters", chars, flush=True)
if NAME in chars:
    c.play(chars.index(NAME))
elif chars:
    c.play(0)
else:
    c.create(NAME)
c.sleep(4)
print("in world at", c.pos, flush=True)

done = 0
idle = 0
while idle < 2400:
    lines = open(CMD).read().splitlines()
    if done >= len(lines):
        c.sleep(0.5)
        c.keepalive()
        idle += 1
        continue
    idle = 0
    w = lines[done].split()
    print(lines[done], flush=True)
    if w[0] == "join":
        since = len(c.gumps)
        g = None
        moved = 0
        for _ in range(2):  # the first step may only turn the character to face the gate
            moved += c.walk(w[1], 1)
            g = c.wait_gump(lambda g: any("Color Wars" in t for t in c.gump_text(g)), 6, since)
            if g:
                break
        print("stepped", moved, "gump", bool(g), flush=True)
        if g:
            c.sleep(1.5)
            c.reply_gump(g, 1)
            c.sleep(2)
        print("now at", c.pos, flush=True)
    elif w[0] == "where":
        print("at", c.pos, flush=True)
    elif w[0] == "end":
        break
    done += 1
    with open(ACK, "a") as f:
        f.write("%d\n" % done)
c.close()
tr.close()
