"""cc-P762: a brand-new character for the isle-landing shot, made through the real creation packet on the Iron Golem's
Player account: it asks for an Elf and New Haven (the locked entry), and must wake on the Wakening Isle as a Human. The
bot's client makes it, sees the wake, stands it up and logs out; TazUO then logs the same character in for the shot.

    python -P newbie762.py --port 2596 --out <folder> [--name "Iron Newbie"]
Test ports only (the uobot client's test_target guard). ASCII."""
import argparse, os, sys

ap = argparse.ArgumentParser()
ap.add_argument("--host", default="127.0.0.1")
ap.add_argument("--port", type=int, default=2596)
ap.add_argument("--out", required=True)
ap.add_argument("--name", default="Iron Newbie")
ap.add_argument("--bot", default=r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
ap.add_argument("--tiledata", default=r"D:\UO\tool-trials\client-data-copy")
a = ap.parse_args()
sys.path.insert(0, a.bot)
from uobot.client import Client, Cliloc, Transcript  # noqa: E402
from uobot import golemcheck as GC  # noqa: E402

os.makedirs(a.out, exist_ok=True)
tr = Transcript(os.path.join(a.out, "newbie-transcript.txt"))
cl = Cliloc(os.path.join(a.tiledata, "Cliloc.enu"), r"D:\UO\bot-shard\cache")
user, pw = GC.account("Iron", "player")
c = Client(user, pw, tr, cl, label="newbie", test_target=(a.host, a.port))
pw = None
chars = c.login()
out = []
out.append("cities sent: %s" % (getattr(c, "cities", None),))
if a.name in chars:
    out.append("%r already exists" % a.name)
else:
    c.create(a.name, race="elf", female=True, stats=(45, 35, 10), skills=((40, 30), (27, 30), (1, 30), (17, 30)), city=1)
    c.find_text(r"Move to get up", since=0, timeout=14)
    c.walk(2, 1)
    c.sleep(6.0)
    out.append("body 0x%X at %s map %s" % (c.body or 0, (c.pos or ())[:3], getattr(c, "map_id", "?")))
    for m in c.messages:
        out.append("  %s" % m.get("text"))
c.close()
tr.close()
with open(os.path.join(a.out, "newbie.txt"), "w", encoding="ascii", errors="replace") as f:
    f.write("\n".join(out) + "\n")
print("\n".join(out))
