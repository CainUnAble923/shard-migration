"""cc-P827 (fix-up of cc-P803 after P824's build review; a copy of notes/cc-P803-tools/edit_layouts.py).
cc-P803: the League field office's new layout, written into design/registrar-office/layout.json of one copy.

    python -P notes/cc-P827-tools/edit_layouts.py release D:/UO/golems/Iron/p803-isle
    python -P notes/cc-P827-tools/edit_layouts.py main    D:/UO/golems/Iron/ShatteredLegacy

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
    # cc-P827 (P824 item 2): at 3463,2596 it stood south of the road with its back to the street. Every sign stands north
    # of its path, facing it (guide 6): the flat verge north of the road (y 2592-2595), off the door's line x 3459.
    c("outside", 0xA854, "signpost", 3460, 2591, 20),
    # cc-P803: a League banner on the east wall, toward the ankh's dais (as the isle lodge's, guide 2.5).
    c("outside", 0x1589, "League banner", 3463, 2599, 26),
    c("office", 0x1E25, "books", 3458, 2600, 24),
    # cc-P827 (P824 item 1): to the desk's north end; the board now hangs south of the desk and its art draws over 2601.
    c("office", 0x2D61, "inkwell", 3458, 2600, 24),
    c("office", 0x2270, "scroll", 3458, 2600, 24),
    c("office", 0x1810, "hourglass", 3458, 2600, 27),
    # cc-P803: 0x0A99 faces east (a west-wall case); in the north-east corner it showed its back. 0x0A98 faces south.
    c("office", 0x0A98, "bookcase", 3461, 2597, 18),
    # (cc-P827: the bookcase 0x0A9A at 3458,2602 gave its tile to the League board, the only free tile of this wall
    # whose art draws over no other wall piece; the office keeps its north-wall case.)
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
    # cc-P827 (P824 item 3): 3670 hung on the stained-glass window 3670,2562; 3671 has a plain wall to its north and
    # draws clear of both windows (rendered against 3672, whose arm touches the window at 3673).
    c("outside", 0x0B98, "wooden signpost", 3671, 2563, 0),
    c("outside", 0x0BCF, "wooden sign", 3671, 2563, 0),
    c("office", 0x1E25, "books", 3661, 2549, 6),
    c("office", 0x2D61, "inkwell", 3661, 2549, 6),
    c("office", 0x2270, "scroll", 3661, 2549, 6),
    c("office", 0x1810, "hourglass", 3661, 2549, 9),
    # cc-P803: on the north wall, so south-facing cases (0x0A99/0x0A9A face east, for a west wall).
    c("office", 0x0A98, "bookcase", 3660, 2548, 0),
    c("office", 0x0A97, "bookcase", 3661, 2548, 0),
    c("office", 0x0B26, "candelabra", 3659, 2548, 0),
    # cc-P827 (P824 item 4): the board moved to 3663,2548 with a free tile each side; the flowerpot goes to the
    # north-east corner.
    c("office", 0x11CA, "flowerpot", 3673, 2548, 0),
    c("quarters", 0x0E42, "wooden chest", 3672, 2548, 0),
    c("quarters", 0x0A98, "bookcase", 3670, 2548, 0),
    c("quarters", 0x2272, "scroll", 3672, 2551, 6),
]

raw = open(path, "rb").read().decode("ascii")
L = json.loads(raw)
L["components"] = RELEASE if which == "release" else MAIN
if "cc-P803" not in L["source"]:
    L["source"] += "; cc-P803 decoration review (shard-migration notes/cc-P803-league-building-deco.md)"
if "cc-P827" not in L["source"]:
    L["source"] += "; cc-P827 fix-up (notes/cc-P827-cont-fixup-league-building-deco.md)"
text = json.dumps(L, indent=1, ensure_ascii=True)
crlf = "\r\n" in raw
if crlf:
    text = text.replace("\n", "\r\n")
open(path, "wb").write((text + ("\r\n" if crlf else "\n") if raw.endswith(("\n",)) else text).encode("ascii"))
print(path, len(L["components"]), "components")
