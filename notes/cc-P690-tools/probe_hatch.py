"""cc-P690: what stands on Rootdeep's hatch tile, and where the server has a player who steps on it (staff [get).
python -P probe_hatch.py <secrets.json> <out folder>"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\scripts")
import tour
from uobot.client import Client, Cliloc, Transcript
from uobot import packets as P
from uobot import golemcheck as GC
from mapbuild import uofiles

out = sys.argv[2]
os.makedirs(out, exist_ok=True)
log = tour.Log(os.path.join(out, "probe-hatch.txt"))
tr = Transcript(os.path.join(out, "probe-transcript.txt"))
cl = Cliloc(r"D:\UO\tool-trials\client-data-copy\Cliloc.enu", r"D:\UO\bot-shard\cache")
TC = tour.make_client_class(Client, P)
_, items = uofiles.read_tiledata(r"D:\UO\tool-trials\client-data-copy")
s = json.load(open(sys.argv[1], encoding="utf-8"))
adm = TC(s["owner"], s["ownerPassword"], tr, cl, label="owner", test_target=("127.0.0.1", 2596))
s = None
adm.login()
adm.play(0)
adm.sleep(2)
user, pw = GC.account("Iron", "player")
c = TC(user, pw, tr, cl, label="player", test_target=("127.0.0.1", 2596))
ch = c.login()
c.play(ch.index("Iron Islander"))
c.sleep(3)
w = tour.Walker(c, tour.Grid(items), log)
log("player at %s facet %s" % (c.pos, c.facet))
tour.staff(adm, log, "[go 3620 2619 0", settle=2.5)
for sr, it in adm.world_items_near(3618, 2620, 1).items():
    log("  item 0x%X graphic %s at %s,%s,%s" % (sr, hex(it.get("graphic", 0)), it.get("x"), it.get("y"), it.get("z")))
w.go((3621, 2620), 0, what="beside the hatch")
for xy in ((3620, 2620), (3619, 2620), (3618, 2620)):
    w.go(xy, 0, what="to %s" % (xy,))
    c.sleep(1.5)
    r = tour.staff(adm, log, '[global get Location where playermobile Name == "Iron Islander"', settle=2.0)
    log("  client pos %s" % (c.pos,))
c.close()
adm.close()
