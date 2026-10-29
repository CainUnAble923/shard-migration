"""cc-P731: log in the bot route's Iron Islander and list its evo pet's context menu (the Pet Info entry's index, for
the TazUO walk's API.ContextMenu). Usage: python -P pet_menu_probe.py <out folder>"""
import os, sys
sys.path.insert(0, r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
from uobot.client import Client, Cliloc, Transcript
from uobot import golemcheck as GC
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
tr = Transcript(os.path.join(out, "transcript.txt"))
cl = Cliloc(r"D:\UO\tool-trials\client-data-copy\Cliloc.enu", r"D:\UO\bot-shard\cache")
user, pw = GC.account("Iron", "player")
pc = Client(user, pw, tr, cl, label="player", test_target=("127.0.0.1", 2596))
chars = pc.login()
print("chars", chars)
pc.play(chars.index("Iron Islander"))
pc.sleep(3)
for s, m in list(pc.mobiles.items()):
    if s != pc.serial and "x" in m:
        print("mobile 0x%08X body 0x%04X at %s,%s name %r" % (s, m.get("body", 0), m["x"], m["y"], m.get("name")))
for s, m in list(pc.mobiles.items()):
    if s != pc.serial and m.get("body") in (0xD9, 0xC9):
        menu = pc.context_menu(s)
        print("menu 0x%08X:" % s, menu and [(e["index"], e["cliloc"], e.get("text")) for e in menu["entries"]])
pc.close()
