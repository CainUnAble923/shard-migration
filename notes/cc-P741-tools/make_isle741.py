"""cc-P741: the bot's isle route with the farm turned round (the field 18 west, the farmhouse 12 east): Wren, the pests,
the field gate and the tile the player enters by, Pip's bench, the farmhouse door and its steps. Everything else as
the source route. Usage: python -P make_isle741.py <source isle.py> <out isle.py>
(main's route is notes/cc-P732-tools/isle.py; the release branch's is notes/cc-P733-tools/isle.py)."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8", newline="").read()
for a, b, n in [
    ("WREN, PESTS = (6714, 3978), (6702, 3978)",
     "WREN, PESTS = (6696, 3978), (6684, 3978)   # cc-P741: the field moved 18 west", 1),
    ("PIP, BESIDE_PIP = (6692, 3975), (6691, 3976)",
     "PIP, BESIDE_PIP = (6704, 3975), (6703, 3976)  # cc-P741: the farmhouse moved 12 east", 1),
    ("FIELD_GATE = ((6713, 3979),)", "FIELD_GATE = ((6695, 3979),)  # cc-P741", 1),
    ("BELOW_WREN = (6714, 3979)", "BELOW_WREN = (6696, 3979)  # cc-P741", 1),
    ("INSIDE_GATE = (6712, 3979)", "INSIDE_GATE = (6694, 3979)  # cc-P741", 1),
    ("    return 6696 <= xy[0] <= 6712 and 3968 <= xy[1] <= 3982",
     "    return 6678 <= xy[0] <= 6694 and 3968 <= xy[1] <= 3982  # cc-P741: TutorialFarm.PestField", 1),
    ("(6690, 3980)", "(6702, 3980)", 2),
    ("(6690, 3978)", "(6702, 3978)", 2),
]:
    assert s.count(a) == n, (s.count(a), a)
    s = s.replace(a, b)
open(dst, "w", encoding="utf-8", newline="").write(s)
print("wrote", dst)
