"""cc-P690: the server's location for Iron Islander, and what stands within 3 of a treasure pin (the owner goes there).
python -P probe_pin.py <secrets.json> <out folder> <x> <y>"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
import tour
from uobot.client import Client, Cliloc, Transcript
from uobot import packets as P

out, x, y = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
os.makedirs(out, exist_ok=True)
log = tour.Log(os.path.join(out, "probe-pin.txt"))
tr = Transcript(os.path.join(out, "probe-pin-transcript.txt"))
cl = Cliloc(r"D:\UO\tool-trials\client-data-copy\Cliloc.enu", r"D:\UO\bot-shard\cache")
TC = tour.make_client_class(Client, P)
s = json.load(open(sys.argv[1], encoding="utf-8"))
adm = TC(s["owner"], s["ownerPassword"], tr, cl, label="owner", test_target=("127.0.0.1", 2596))
s = None
adm.login()
adm.play(0)
adm.sleep(2)
tour.ADM = adm
log("Iron Islander, by the server: %s" % (tour.server_loc("Iron Islander"),))
tour.staff(adm, log, "[global set Map Trammel where playermobile Name == \"Generic Player\"", settle=1.0)
tour.staff(adm, log, "[go %d %d" % (x, y + 2), settle=3.0)
for sr, it in sorted(adm.world_items_near(x, y, 3).items()):
    log("  item 0x%X graphic %s at %s,%s,%s" % (sr, hex(it.get("graphic", 0)), it.get("x"), it.get("y"), it.get("z")))
for sr, m in adm.mobiles.items():
    if "x" in m and abs(m["x"] - x) <= 8 and abs(m["y"] - y) <= 8 and sr != adm.serial:
        log("  mobile 0x%X body %s at %s,%s %s" % (sr, hex(m.get("body", 0)), m["x"], m["y"], m.get("name")))
adm.close()
