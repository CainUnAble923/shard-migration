"""cc-P817 (P731's make_create_bin.py): the 0xF8 create-character bytes for the TazUO plugin (P731Create), made by the
bot's own packet builder. P731's asked for Alchemy, which main's start rules refuse (P714); this one sends the Fighter
template (profession 1: Swordsmanship, Tactics, Anatomy, Healing at 30; 45/35/10), a male Human, city 0 (the isle).

    python -P make_create_bin.py <name> <out file> [profession] [genderRace] [city]

genderRace as the packet has it (SA): 2/3 human, 4/5 elf, 6/7 gargoyle (male/female). The extra arguments make the
packets an old or third-party client could send: an elf, a gargoyle, the Maker (3), New Haven (city 1)."""
import sys
sys.path.insert(0, r"D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot")
from uobot import packets as P

name, out = sys.argv[1], sys.argv[2]
profession = int(sys.argv[3]) if len(sys.argv) > 3 else 1
gender_race = int(sys.argv[4]) if len(sys.argv) > 4 else 2
city = int(sys.argv[5]) if len(sys.argv) > 5 else 0
skills = ((40, 30), (27, 30), (1, 30), (17, 30))   # Swordsmanship, Tactics, Anatomy, Healing (the Fighter's)
b = P.create_character(name, gender_race, (45, 35, 10), skills, 0x83EA, 0x203B, 0x044E, 0, 0, city,
                       0x0101, 0x0101, profession=profession)
open(out, "wb").write(b)
print("wrote %d bytes for %r (profession %d, genderRace %d, city %d)" % (len(b), name, profession, gender_race, city))
