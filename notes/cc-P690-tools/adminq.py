"""cc-P690: Iron's Admin (Administrator) types staff commands on the private proof shard and logs every reply; for
queries and Administrator steps while the owner's account was held "in use".
    python -P adminq.py <out file> "<command>" ["<command>" ...]"""
import os
import sys
import time

sys.path.insert(0, r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
from uobot.client import Client, Cliloc, Transcript
from uobot import golemcheck as GC

out = sys.argv[1]
f = open(out, "a", encoding="ascii", errors="replace")
t0 = time.time()


def log(s):
    line = "[%6.1f] %s" % (time.time() - t0, s)
    print(line, flush=True)
    f.write(line + "\n")


tr = Transcript(os.path.join(os.path.dirname(out), "adminq-transcript.txt"))
cl = Cliloc(r"D:\UO\tool-trials\client-data-copy\Cliloc.enu", r"D:\UO\bot-shard\cache")
user, pw = GC.account("Iron", "admin")
c = Client(user, pw, tr, cl, label="admin", test_target=("127.0.0.1", 2596))
pw = None
chars = c.login()
c.play(chars.index("Iron") if "Iron" in chars else 0)
c.sleep(2.0)
for cmd in sys.argv[2:]:
    log("=== %s" % cmd)
    n = len(c.messages)
    c.say(cmd)
    c.sleep(6.0)
    for m in c.messages[n:]:
        if m.get("name") in (None, "", "System") or "=" in (m.get("text") or ""):
            log("    %s" % m.get("text"))
c.close()
