# cc-P800: log the Golem admin's character in on the private proof shard with the bot client, so its login pass runs; the shard's log
# is the proof. python -P login-probe.py <user> <password> <character>
import sys, tempfile, os
sys.path.insert(0, r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
from uobot.client import Client, Transcript, Cliloc

user, pw, name = sys.argv[1:4]
d = tempfile.mkdtemp()
tr = Transcript(os.path.join(d, "t.txt"))
c = Client(user, pw, tr, Cliloc(r"D:\UO\tool-trials\client-data-copy\Cliloc.enu", d), label="p800", test_target=("127.0.0.1", 2596))
chars = c.login()
print("characters:", chars)
c.play(chars.index(name))
c.sleep(4)
print("in the world as", name)
c.close()
