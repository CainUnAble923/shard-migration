"""cc-P803: the League field office's new layout, written into design/registrar-office/layout.json of one copy.

    python -P notes/cc-P803-tools/edit_layouts.py release D:/UO/golems/Iron/p803-isle
    python -P notes/cc-P803-tools/edit_layouts.py main    D:/UO/golems/Iron/ShatteredLegacy

then gen_office_layout.py on the same copy. Every change is from the review in notes/cc-P803-league-building-deco.md
(the building guide's rules: wall pieces face the room from a north or west wall, nothing on a window's floor tile, a
standing signpost where a sign arm has no wall to hang from).
"""
import json
import sys

which, root = sys.argv[1], sys.argv[2]
path = root + "/design/registrar-office/layout.json"


def c(area, i, name, x, y, z):
    return {"area": area, "id": "0x%04X" % i, "name": name, "x": x, "y": y, "z": z}


RELEASE = [
    c("outside", 0x11C9, "potted tree", 3458, 2595, 15),
    # cc-P803: the sign arm 0x0B97 + board 0x0BCF at 3463,2597 hung from nothing (no wall north of it) and stood
    # under the eave; a north-door house gets a named standing signpost by the door's corner (guide 11.12).
    c("outside", 0xA854, "signpost", 3463, 2596, 16),
    # cc-P803: a League banner on the east wall, toward the ankh's dais (as the isle lodge's, guide 2.5).
    c("outside", 0x1589, "League banner", 3463, 2599, 26),
    c("office", 0x1E25, "books", 3458, 2600, 24),
    c("office", 0x2D61, "inkwell", 3458, 2601, 24),
    c("office", 0x2270, "scroll", 3458, 2601, 24),
    c("office", 0x1810, "hourglass", 3458, 2600, 27),
    # cc-P803: 0x0A99 faces east (a west-wall case); in the north-east corner it showed its back. 0x0A98 faces south.
    c("office", 0x0A98, "bookcase", 3461, 2597, 18),
    c("office", 0x0A9A, "bookcase", 3458, 2602, 18),
    # cc-P803: off the east window's floor tile (3462,2602), beside the desk side of the room.
    c("office", 0x0B26, "candelabra", 3461, 2601, 18),
    # (the flowerpot 0x11CA stood on the north window's floor tile, 3460,2597: gone)
    # cc-P803: off the north window's floor tile (3456,2597), at the foot of the bed, facing into the room.
    c("quarters", 0x0E42, "wooden chest", 3455, 2598, 18),
    # cc-P803: off the west window's floor tile (3453,2602), on the plain west wall between the table and the dresser.
    c("quarters", 0x0A9A, "bookcase", 3454, 2599, 18),
    c("quarters", 0x2272, "scroll", 3454, 2598, 24),
]

MAIN = [
    c("outside", 0x11C9, "potted tree", 3665, 2563, 0),
    # cc-P803: 0x0B97 lies along a wall; the arm that sticks out from a south wall is 0x0B98 (guide 2.5), two tiles
    # east of the arch (3667-3668,2562).
    c("outside", 0x0B98, "wooden signpost", 3670, 2563, 0),
    c("outside", 0x0BCF, "wooden sign", 3670, 2563, 0),
    c("office", 0x1E25, "books", 3661, 2549, 6),
    c("office", 0x2D61, "inkwell", 3661, 2549, 6),
    c("office", 0x2270, "scroll", 3661, 2549, 6),
    c("office", 0x1810, "hourglass", 3661, 2549, 9),
    # cc-P803: on the north wall, so south-facing cases (0x0A99/0x0A9A face east, for a west wall).
    c("office", 0x0A98, "bookcase", 3660, 2548, 0),
    c("office", 0x0A97, "bookcase", 3661, 2548, 0),
    c("office", 0x0B26, "candelabra", 3659, 2548, 0),
    c("office", 0x11CA, "flowerpot", 3663, 2548, 0),
    c("quarters", 0x0E42, "wooden chest", 3672, 2548, 0),
    c("quarters", 0x0A98, "bookcase", 3670, 2548, 0),
    c("quarters", 0x2272, "scroll", 3672, 2551, 6),
]

raw = open(path, "rb").read().decode("ascii")
L = json.loads(raw)
L["components"] = RELEASE if which == "release" else MAIN
if "cc-P803" not in L["source"]:
    L["source"] += "; cc-P803 decoration review (shard-migration notes/cc-P803-league-building-deco.md)"
text = json.dumps(L, indent=1, ensure_ascii=True)
crlf = "\r\n" in raw
if crlf:
    text = text.replace("\n", "\r\n")
open(path, "wb").write((text + ("\r\n" if crlf else "\n") if raw.endswith(("\n",)) else text).encode("ascii"))
print(path, len(L["components"]), "components")
