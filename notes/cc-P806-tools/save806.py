"""cc-P799: staff hands for the TazUO walk. A real trainee must be on a Player account (staff are never entered in the tutorial), and a
Player has no commands, so this bot logs the Golem's admin in and does what Walk799.py asks through a file: one line per request in
CMD, each answered by its line number in ACK. Private proof shard only (the uobot client's test_target guard).

    python -P stage799.py [--port 2596] [--name "Iron Stock"]
"""
import argparse
import os
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, default=2596)
ap.add_argument("--name", default="Iron Stock")
ap.add_argument("--bot", default=r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
a = ap.parse_args()
sys.path.insert(0, a.bot)
from uobot.client import Client, Cliloc, Transcript  # noqa: E402
from uobot import golemcheck as GC  # noqa: E402

BASE = r"D:\UO\golems\Iron\p740-proof"
CMD, ACK = os.path.join(BASE, "stage.cmd"), os.path.join(BASE, "stage.ack")
OUT = os.path.join(BASE, "stage")
os.makedirs(OUT, exist_ok=True)

tr = Transcript(os.path.join(OUT, "stage-transcript.txt"))
cl = Cliloc(r"D:\UO\tool-trials\client-data-copy\Cliloc.enu", r"D:\UO\bot-shard\cache")
user, pw = GC.account("Iron", "admin")
c = None
for _ in range(120):
    try:
        c = Client(user, pw, tr, cl, label="stage", test_target=("127.0.0.1", a.port))
        chars = c.login()
        break
    except Exception as e:  # the shard is still loading
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
WHERE = 'where playermobile Name == "%s"' % a.name
c.command("[self set Map Trammel", 1)
c.command("[self set Location (3503,2574,14)", 2)
c.command("[self set Hidden True", 1)
print("staged at", c.pos, flush=True)


def glob(prop):
    r = c.command('[global set %s %s' % (prop, WHERE), 1)
    print(prop, [m.get("text") for m in r][:3], flush=True)


def go(x, y, z):
    p = "(%d,%d,%d)" % (x, y, z)
    glob("Map Trammel")
    glob("Location " + p)
    glob("LogoutMap Trammel")
    glob("LogoutLocation " + p)


def on_player(command, serial):
    c.command(command, 0.5)
    if c.wait_target(6):
        c.target_obj(serial)
    c.sleep(1)


r = c.command("[save", 10)
print("saved", [m.get("text") for m in r][:4], flush=True)
r = c.command('[global get ItemID where Static Name == "wooden bench"', 2)
print("benches", [m.get("text") for m in r][:6], flush=True)
r = c.command('[global get Direction where TutorialRecruiter', 1)
print("rook", [m.get("text") for m in r][:4], flush=True)
c.close()
tr.close()
