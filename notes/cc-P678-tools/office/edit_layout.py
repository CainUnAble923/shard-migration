r"""cc-P678 WRITES: moves the League field office design (design/registrar-office/layout.json in the Iron code copy)
from the old New Haven house (x3453-3462, y2596-2603, z18) into the free hall of SoS Haven (walls x3658-3674,
y2547-2562, floor z0, doorway 3667-3668,2562). Same 14 components in the same order; tabletop items keep their
height above the table (old desk top 24 on floor 18: books 24 -> counter top 6, hourglass 27 -> 9).
Run once; check.py verifies the tiles. Keeps the file's form (indent 1, LF, no trailing newline, ASCII).
"""
import json

PATH = "D:/UO/golems/Iron/ShatteredLegacy/design/registrar-office/layout.json"

NEW = [  # (area, id, name) -> x, y, z, in design order
    ("outside", "0x11C9", "potted tree", 3665, 2563, 0),     # outside the south doorway, west of it
    ("outside", "0x0B97", "wooden signpost", 3670, 2563, 0),  # outside the south doorway, east of it
    ("outside", "0x0BCF", "wooden sign", 3670, 2563, 0),
    ("office", "0x1E25", "books", 3661, 2549, 6),             # on the counter East of the Registrar (top z6)
    ("office", "0x2D61", "inkwell", 3661, 2549, 6),
    ("office", "0x2270", "scroll", 3661, 2549, 6),
    ("office", "0x1810", "hourglass", 3661, 2549, 9),
    ("office", "0x0A99", "bookcase", 3660, 2548, 0),          # north wall, behind the Registrar
    ("office", "0x0A9A", "bookcase", 3661, 2548, 0),          # north wall, behind the desk
    ("office", "0x0B26", "candelabra", 3659, 2548, 0),        # north-west corner
    ("office", "0x11CA", "flowerpot", 3663, 2548, 0),         # north wall; the League board hangs at 3662,2547
    ("quarters", "0x0E42", "wooden chest", 3672, 2548, 0),    # the back room behind the long counter
    ("quarters", "0x0A9A", "bookcase", 3670, 2548, 0),
    ("quarters", "0x2272", "scroll", 3672, 2551, 6),          # on the long counter (top z6)
]

text = open(PATH, "rb").read().decode("ascii")
L = json.loads(text)
assert json.dumps(L, indent=1) == text
assert len(L["components"]) == len(NEW)
for c, (a, i, n, x, y, z) in zip(L["components"], NEW):
    assert (c["area"], c["id"], c["name"]) == (a, i, n), (c, a, i, n)
    c["x"], c["y"], c["z"] = x, y, z
L["building"] = ("League of Extraordinary Citizens Field Office (Haven, SoS Trammel), the hall walls x3658-3674 "
                 "y2547-2562, floor z0, doorway 3667-3668,2562")
L["source"] = ("design/registrar-office/registrar.py; cc-P678 moved it into SoS Haven "
               "(shard-migration notes/cc-P678-tools/office), z from the SoS map files")
open(PATH, "wb").write(json.dumps(L, indent=1).encode("ascii"))
print("wrote", PATH)
