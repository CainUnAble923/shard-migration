"""cc-P731: make a brand-new character on Iron's Player account with the isle pick, and drop the connection at once,
so its first real session is TazUO's. The server starts the wake at creation; a disconnect while lying drops the
login hold, and the next login (TazUO's) runs the login handlers again (cc-P728, TutorialWake). Prints the account's
characters before and after. Usage: python -P create_fresh.py <out folder> <name>"""
import os
import sys

sys.path.insert(0, r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
from uobot.client import Client, Cliloc, Transcript
from uobot import golemcheck as GC

out, name = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
tr = Transcript(os.path.join(out, "create-transcript.txt"))
cl = Cliloc(r"D:\UO\tool-trials\client-data-copy\Cliloc.enu", r"D:\UO\bot-shard\cache")
user, pw = GC.account("Iron", "player")
pc = Client(user, pw, tr, cl, label="player", test_target=("127.0.0.1", 2596))
chars = pc.login()
print("characters before: %s" % [c for c in chars if c])
if name in chars:
    print("%r exists already: not fresh, stopping" % name)
    pc.close()
    sys.exit(2)
if all(chars):
    print("no free slot")
    pc.close()
    sys.exit(3)
pc.create(name, stats=(45, 35, 10), skills=((0, 30), (17, 30), (40, 30), (43, 30)), city=0)
print("created %r at %s; journal so far: %s" % (name, pc.pos[:3], [m["text"] for m in pc.messages]))
pc.close()
print("dropped the connection")
