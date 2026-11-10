"""cc-P860 (P859's stage859.py, plus "skill <Name> <value>" ([SetSkill on the trainee) and "dens" ([PolarBearDens status)).
cc-P859 (P855's stage855.py, plus "give", "spawn" and "access" for the Horn of Plenty proof). cc-P855 (P849's stage849.py, plus "grant", "place" and "clear" for the decor addon proof). cc-P827 (a copy of notes/cc-P803-tools/stage803.py, plus "office": replace the office decor). cc-P803: staff hands for the TazUO walk. A real trainee must be on a Player account (staff are never entered in the tutorial), and a
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
ap.add_argument("--name", default="Iron Frost")
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
        go(int(w[1]), int(w[2]), int(w[3]))
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
    elif w[0] == "give":  # cc-P859: give <Type> into the trainee's pack
        on_player("[AddToPack " + w[1], serial)
    elif w[0] == "spawn":  # cc-P859: spawn <Type> at the trainee's feet
        on_player("[add " + w[1], serial)
    elif w[0] == "access":  # cc-P859: access <Player|GameMaster> (a house placed by the trainee, then back to Player)
        glob("AccessLevel " + w[1])
    elif w[0] == "houseinfo":  # cc-P859 run 3: who owns the houses on this copy
        for prop in ("Owner", "Location", "Z"):
            r = c.command('[global get %s where smalloldhouse' % prop, 1)
            print("house", prop, [m.get("text") for m in r][:6], flush=True)
    elif w[0] == "staffpig":  # cc-P859 run 7: staff places an east pig from a deed at x y z (exact ground target)
        x, y, z = int(w[1]), int(w[2]), int(w[3])
        c.command("[AddToPack RoastingPigOnASpitDeed", 0.5)
        if c.wait_target(6):
            c.target_self()
        c.sleep(1.5)
        bp = c.backpack()
        if bp:
            c.dclick(bp)  # open it so its contents are sent
            c.sleep(1.5)
        deeds = [s for s, it in c.contents(bp).items() if it.get("graphic") == 0x14F0]
        print("staff deeds", ["%X" % s for s in deeds], flush=True)
        if deeds:
            n = len(c.gumps)
            c.dclick(max(deeds))
            g = c.wait_gump(since=n)
            print("facing gump", bool(g), flush=True)
            if g:
                c.reply_gump(g, 1)  # East
                if c.wait_target(6):
                    c.target_xyz(x, y, z, 0x04AB)  # run 10: the floor tile, not land (a LandTarget drops to land Z)
                    c.sleep(2)
        print("staffpig texts", [str(m) for m in c.texts_since(0)][-8:], flush=True)
    elif w[0] == "skill":  # cc-P860: skill <Name> <value> on the trainee
        on_player("[SetSkill %s %s" % (w[1], w[2]), serial)
    elif w[0] == "getskill":  # cc-P860 run 2: read a skill back off the trainee ([GetSkill)
        n = len(c.texts_since(0))
        on_player("[GetSkill %s" % w[1], serial)
        print("getskill", [str(m) for m in c.texts_since(0)][n:][-4:], flush=True)
    elif w[0] == "dens":  # cc-P860: the ridable polar bear dens on this world copy
        r = c.command("[PolarBearDens status", 2)
        print("dens", [m.get("text") for m in r][:6], flush=True)
        r = c.command("[global get Location where RidablePolarBear", 2)
        print("bears", [m.get("text") for m in r][:8], flush=True)
    elif w[0] == "end":
        break
    done += 1
    with open(ACK, "a") as f:
        f.write("%d\n" % done)
c.close()
tr.close()
