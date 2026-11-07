"""cc-P813 (P799's stage799.py): staff hands for the TazUO shots. The Player has no commands, so this bot logs the Golem's
admin in and types what Shots813.py asks through a file: one request a line in CMD, each answered by its line number in
ACK. Private proof shard only (the uobot client's test_target guard).

    python -P stage813.py [--port 2596]

Requests:
    cmd <text>                    type <text> as the admin ({user} is the player's account name)
    addat <x> <y> <z> <type>      [add <type>, then target the ground at x, y, z
    end
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

BASE = r"D:\UO\golems\Iron\p813-proof"
CMD, ACK = os.path.join(BASE, "stage.cmd"), os.path.join(BASE, "stage.ack")
OUT = os.path.join(BASE, "stage")
os.makedirs(OUT, exist_ok=True)
for f in (CMD, ACK):
    open(f, "w").close()

tr = Transcript(os.path.join(OUT, "stage-transcript.txt"))
cl = Cliloc(r"D:\UO\tool-trials\client-data-copy\Cliloc.enu", r"D:\UO\bot-shard\cache")
player_user, _pp = GC.account("Iron", "player")
_pp = None
user, pw = GC.account("Iron", "admin")
c = None
for _ in range(120):
    try:
        c = Client(user, pw, tr, cl, label="stage", test_target=("127.0.0.1", a.port))
        chars = c.login()
        break
    except Exception:  # the shard is still loading
        c = None
        time.sleep(3)
pw = None
if c is None:
    sys.exit("no shard")
print("characters", chars, flush=True)
if not chars:
    c.create("Iron Stage")
else:
    c.play(0)
c.sleep(4)
c.command("[self set Hidden True", 1)
print("staged at", c.pos, flush=True)

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
    line = lines[done]
    w = line.split()
    print(line, flush=True)
    if w[0] == "cmd":
        text = line[4:].replace("{user}", player_user)
        r = c.command(text, 1.5)
        print("  ", [m.get("text") for m in r][:4], flush=True)
    elif w[0] == "addat":
        c.command("[add " + w[4], 0.5)
        if c.wait_target(6):
            c.target_xyz(int(w[1]), int(w[2]), int(w[3]))
        c.sleep(1)
    elif w[0] == "end":
        break
    done += 1
    with open(ACK, "a") as f:
        f.write("%d\n" % done)
c.close()
tr.close()
