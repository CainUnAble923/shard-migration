"""cc-P867: P855's stage855.py plus "house" (staff places a two-story stone house and hands it to the trainee) and
"deed" (a ShardDecorDeed into the trainee's pack). cc-P855 (P849's stage849.py, plus "grant", "place" and "clear" for the decor addon proof). cc-P827 (a copy of notes/cc-P803-tools/stage803.py, plus "office": replace the office decor). cc-P803: staff hands for the TazUO walk. A real trainee must be on a Player account (staff are never entered in the tutorial), and a
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
ap.add_argument("--name", default="Iron Decor")
ap.add_argument("--bot", default=r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
a = ap.parse_args()
sys.path.insert(0, a.bot)
from uobot.client import Client, Cliloc, Transcript  # noqa: E402
from uobot import golemcheck as GC  # noqa: E402

BASE = r"D:\UO\golems\Iron\p740-proof"
CMD, ACK = os.path.join(BASE, "stage.cmd"), os.path.join(BASE, "stage.ack")
OUT = os.path.join(BASE, "stage")
os.makedirs(OUT, exist_ok=True)
for f in (CMD, ACK):
    open(f, "w").close()

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

# cc-P867 (run 2): a house deed's cursor is the multi placement cursor, packet 0x99 (byte id, byte allow ground, u32
# target id, ...), which uobot's reader does not record, so wait_target never saw it and no house was placed. Record it
# here as a cursor; the answer is the usual 0x6C ground target with that id. (Only this staging copy is patched.)
import struct  # noqa: E402
_handle = c._handle


def _handle867(p):
    if p and p[0] == 0x99 and len(p) >= 6:
        c.target = (struct.unpack(">i", bytes(p[2:6]))[0], 1)
        c.log("<- 0x99 multi target cursor %d" % c.target[0])
        return
    return _handle(p)


c._handle = _handle867
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


def go(x, y, z, facet="Trammel"):
    p = "(%d,%d,%d)" % (x, y, z)
    glob("Map " + facet)
    glob("Location " + p)
    glob("LogoutMap " + facet)
    glob("LogoutLocation " + p)


def on_player(command, serial):
    c.command(command, 0.5)
    if c.wait_target(6):
        c.target_obj(serial)
    c.sleep(1)


done = 0
serial = 0
idle = 0
while idle < 1200:
    lines = open(CMD).read().splitlines()
    if done >= len(lines):
        c.sleep(0.5)
        c.keepalive()
        idle += 1
        continue
    idle = 0
    w = lines[done].split()
    print(lines[done], flush=True)
    if w[0] == "serial":
        serial = int(w[1], 16)
    elif w[0] == "go":
        go(int(w[1]), int(w[2]), int(w[3]), w[4] if len(w) > 4 else "Trammel")
    elif w[0] == "blessed":
        glob("Blessed " + w[1])
    elif w[0] == "young":
        glob("Young " + w[1])
    elif w[0] == "kill":
        on_player("[kill", serial)
    elif w[0] == "res":
        on_player("[res", serial)
    elif w[0] == "station":
        on_player("[Tutorial station " + w[1], serial)
    elif w[0] == "rookdir":  # cc-P806: what the server holds for Rook
        r = c.command('[global get Direction where TutorialRecruiter', 1)
        print("rook", [m.get("text") for m in r][:4], flush=True)
    elif w[0] == "office":  # cc-P827 (P824 item 5): this town's office decor from the current layout, on this world copy
        r = c.command("[ClusterFSeedRegistrarOffice replace", 4)
        print("office", [m.get("text") for m in r][:8], flush=True)
    elif w[0] == "grant":  # cc-P855: grant <tokens|ap|renown> <amount> to the trainee
        r = c.command('[RewardStores grant %s %s %s' % (a.name, w[1], w[2]), 1)
        print("grant", [m.get("text") for m in r][:3], flush=True)
    elif w[0] == "place":  # cc-P855: place <design> x y z (staff dressing, no house rules)
        r = c.command('[DecorAddon place %s %s %s %s' % (w[1], w[2], w[3], w[4]), 1)
        print("place", [m.get("text") for m in r][:3], flush=True)
    elif w[0] == "clear":  # cc-P855: clear x y z
        r = c.command('[DecorAddon clear %s %s %s' % (w[1], w[2], w[3]), 1)
        print("clear", [m.get("text") for m in r][:3], flush=True)
    elif w[0] == "house":  # cc-P867: house x y z map deed type cx cy: staff places that house deed there, the trainee owns it
        # run 1: staff aimed from New Haven, 200 tiles off, and no house was made; stand beside the plot first
        c.command("[self set Map %s" % w[4], 1)
        c.command("[self set Location (%d,%d,%d)" % (int(w[1]) + 6, int(w[2]) + 4, int(w[3])), 2)
        print("staff at", c.pos, flush=True)
        c.command("[AddToPack %s" % w[5], 0.5)
        if c.wait_target(6):
            c.target_self()
        c.sleep(1.5)
        pack = c.backpack()
        c.dclick(pack)
        c.sleep(2)
        deeds = [s for s, it in c.contents(pack).items() if it.get("graphic") == 0x14F0]
        print("house deeds in staff pack", [hex(d) for d in deeds], flush=True)
        if deeds:
            c.dclick(max(deeds))
            if c.wait_target(6):
                c.target_xyz(int(w[1]), int(w[2]), int(w[3]), 0)
            c.sleep(3)
            r = c.command("[global set Owner 0x%x where %s X == %s Y == %s" % (serial, w[6], w[7], w[8]), 1.5)
            print("house owner", [m.get("text") for m in r][:4], flush=True)
            r = c.command("[global get Location where %s" % w[6], 1)
            print("house at", [m.get("text") for m in r][:4], flush=True)
    elif w[0] == "deed":  # cc-P867: deed <group>: a ShardDecorDeed for that group into the trainee's pack
        c.command("[AddToPack ShardDecorDeed %s" % w[1], 0.5)
        if c.wait_target(6):
            c.target_obj(serial)
        c.sleep(1)
        print("deed", w[1], flush=True)
    elif w[0] == "end":
        break
    done += 1
    with open(ACK, "a") as f:
        f.write("%d\n" % done)
c.close()
tr.close()
