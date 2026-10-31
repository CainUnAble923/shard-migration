"""cc-P731: the 0xF8 create-character bytes for the TazUO plugin (P731Create), made by the bot's own packet builder:
the same fields as the bot route's character (isle pick, city 0). Usage: python -P make_create_bin.py <name> <out file>"""
import sys
sys.path.insert(0, r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
from uobot import packets as P
name, out = sys.argv[1], sys.argv[2]
b = P.create_character(name, 2, (45, 35, 10), ((0, 30), (17, 30), (40, 30), (43, 30)), 0x83EA, 0x203B, 0x044E, 0, 0, 0,
                       0x0101, 0x0101)
open(out, "wb").write(b)
print("wrote %d bytes for %r" % (len(b), name))
