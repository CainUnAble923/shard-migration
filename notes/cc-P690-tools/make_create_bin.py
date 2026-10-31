"""cc-P690 (P731's, with the start city as an argument): the 0xF8 create-character bytes for the test-only creation
plugin (P731Create), made by the bot's own packet builder. City 0 is the first on the server's list (Tutorial Island),
1 the second (New Haven). Usage: python -P make_create_bin.py <name> <city> <out file>"""
import sys
sys.path.insert(0, r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
from uobot import packets as P
name, city, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
b = P.create_character(name, 2, (45, 35, 10), ((0, 30), (17, 30), (40, 30), (43, 30)), 0x83EA, 0x203B, 0x044E, 0, 0, city,
                       0x0101, 0x0101)
open(out, "wb").write(b)
print("wrote %d bytes for %r, city %d" % (len(b), name, city))
