"""cc-P720 items 1 and 2: generates TutorialIsleFarmLayout.cs, the isle's farm, as one clean design on the flat meadow.

P663 moved P276's New Haven farm here piece by piece, keeping each piece's height above the sloped ground it stood on
there. P276's farmhouse was OSI's thatched-roof cottage (house multi 0x006E, the same art ids), but laid on a hillside,
so on the isle's flat Z 0 its foundation, walls and roof each sat at a different height (Chase 10-28: "house is jacked
up"). Now the farmhouse is the cottage multi itself, read from MultiCollection.uop, at Z 0. The field fence is one ring
laid by the run rule (walls.wall_pieces, the fence set), the pen inside it is closed, and the strays are gone.

    python -P gen_isle_farm.py <code copy>        writes server/customizations/Tutorial/TutorialIsleFarmLayout.cs
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, HERE)
from mapbuild import uofiles, walls as W  # noqa: E402
import multis  # noqa: E402

ANCHOR = (6691, 3975, 0)          # the addon's anchor, unchanged (FindAddon looks here)
HOUSE = (6690, 3975)              # the cottage multi's centre: walls x 6687-6693, y 3972-3978, steps on y 3979
COTTAGE = 0x006E
FENCE = {'ew': 0x0836, 'ns': 0x0837, 'post': 0x0835, 'corner': None}
FIELD = (6695, 3967, 6713, 3983)  # the field fence ring (TutorialFarm.PestField is its inside)
PEN = (6706, 3967, 6713, 3973)    # the animal pen in the field's north-east corner, closed
# TutorialFarm places these two itself: the field gate and the fence piece above it (cc-P718)
SERVER_FENCE = {(6713, 3978), (6713, 3979)}

# the cottage's NW foundation corner is 0x0066 in the multi, which this tiledata names an elven bookshelf; P276 used
# the north-south foundation piece there, as here
SWAP = {0x0066: 0x0064}
SKIP = {0x0001}                   # the multi's no-draw anchor
# the cottage's house sign: the multi's hanger (0x0B9A, fl 0) and its brass sign (0x0BD2, fl 1, a house's own sign
# there), both kept; the addon names the sign (TutorialFarm.HouseSignName)
KEEP_FL1 = {0x0BD2}

# the yard round the house and the field's contents: art, x, y (all at Z 0)
PROPS = [
    (0xA854, 6715, 3977),   # the farm gate's signpost (cc-P718), named by the addon
    (0x0E77, 6714, 3980),   # barrel by the gate
    (0xA300, 6684, 3976),   # wishing well, west of the house
    (0x0F36, 6688, 3970),   # sheaf of hay, behind the house
    (0x100C, 6689, 3970),   # hay sheave
    (0x0E87, 6690, 3970),   # pitchfork
    (0x0B2C, 6692, 3980),   # bench beside the steps
    (0x154D, 6688, 3980),   # water barrel beside the steps
    (0x1E34, 6702, 3976),   # scarecrow in the field
    (0x0B41, 6708, 3969),   # water trough (pen)
    (0x0B42, 6709, 3969),
    (0x0F36, 6711, 3971),   # hay in the pen
    (0x0F36, 6712, 3971),
    (0x100C, 6711, 3972),
]
# P276's chimney (0x08D5) and chicken coop (0x4514) are left out: OSI's cottage has no chimney, and on the flat meadow
# both stood apart from the house (Chase 10-28: the chimney apart, a gray structure on the roof)
# cc-P720 item 6: the farmhouse furnished, on its floor (Z 7; floor x 6688-6692, y 3973-3977, the door 6690,3978 and
# the tile inside it kept clear): pinned's stone fireplace (east) against the west wall, its small bed (south) in the
# north-east corner, a table and two chairs, a chest and a barrel in the south corners, a wall torch on the north wall
INTERIOR = [
    (0x0959, 6688, 3973, 7), (0x0953, 6688, 3974, 7),   # StoneFireplaceEastAddon
    (0x0A63, 6692, 3973, 7), (0x0A5C, 6692, 3974, 7),   # SmallBedSouthAddon
    (0x0B90, 6690, 3975, 7), (0x0B4E, 6690, 3974, 7), (0x0B4F, 6690, 3976, 7),
    (0x0E77, 6688, 3977, 7), (0x0E7D, 6692, 3977, 7),
    (0x0A0C, 6690, 3973, 20),
]
ROWS = [(0x0C6A, 3969, 6697, 6704), (0x0C7B, 3971, 6697, 6704), (0x0C7B, 3975, 6697, 6711),
        (0x0C55, 3977, 6697, 6711), (0x0C7D, 3979, 6697, 6711), (0x0C76, 3981, 6697, 6711)]


def ring(r):
    x1, y1, x2, y2 = r
    return {(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1) if x in (x1, x2) or y in (y1, y2)}


def build():
    td = uofiles.read_tiledata(uofiles.CLIENT)[1]
    name = lambda t: td[t]['name'] or 'piece'
    out = []
    for (x, y, z, tid, fl) in multis.multi(COTTAGE):
        if (fl != 0 and tid not in KEEP_FL1) or tid in SKIP:
            continue
        tid = SWAP.get(tid, tid)
        out.append((tid, HOUSE[0] + x, HOUSE[1] + y, z, name(tid)))
    fence = ring(FIELD) | {c for c in ring(PEN)}
    lay = lambda c: c in fence
    for (x, y) in sorted(fence):
        if (x, y) in SERVER_FENCE:
            continue
        for tid, role in W.wall_pieces(lay, x, y, FENCE):
            out.append((tid, x, y, 0, name(tid)))
    for (tid, y, xa, xb) in ROWS:
        for x in range(xa, xb + 1):
            out.append((tid, x, y, 0, name(tid)))
    for (tid, x, y, z) in INTERIOR:
        out.append((tid, x, y, z, name(tid)))
    for (tid, x, y) in PROPS:
        out.append((tid, x, y, 0, 'wooden signpost' if tid == 0xA854 else name(tid)))
    return out


def door():
    for (x, y, z, tid, fl) in multis.multi(COTTAGE):
        if 0x06A5 <= tid <= 0x06B4:
            return (HOUSE[0] + x, HOUSE[1] + y, z), tid
    raise SystemExit('no door in the cottage multi')


def main():
    code = sys.argv[1]
    pieces = build()
    (dx, dy, dz), dtid = door()
    rows = '\n'.join('        (0x%04X, %d, %d, %d), // %s' % (t, x, y, z, n) for (t, x, y, z, n) in pieces)
    text = '''// cc-P720 (items 1 and 2): the tutorial farm on the Wakening Isle. GENERATED by shard-migration
// notes/cc-P720-tools/gen_isle_farm.py: do not edit by hand. The farmhouse is OSI's thatched-roof cottage (house multi
// 0x%04X, MultiCollection.uop) laid whole at Z 0 on the flat meadow: P663 had moved P276's copy of it piece by piece with
// each piece's height above New Haven's slope, so nothing lined up. The field fence is one ring by the run rule (the
// fence set 0x0835-0x0837), its gate the server's (TutorialFarm.FieldGateSpots); the pen inside it is closed.
// Coordinates are absolute, on the lesson map (TutorialWorld). %d rows.

namespace Server.Tutorial;

public static class TutorialIsleFarmLayout
{
    /// <summary>The shift from P276's New Haven farm to the isle's (its stops and spots keep it).</summary>
    public static readonly Point2D Shift = new(3314, 1364);

    /// <summary>The addon's anchor, on the meadow at Z 0.</summary>
    public static readonly Point3D Anchor = new(%d, %d, %d);

    /// <summary>The farmhouse door (south wall, the cottage's own door tile, art 0x%04X), above the foundation.</summary>
    public static readonly Point3D DoorSpot = new(%d, %d, %d);

    /// <summary>Where P663's farmhouse door stood; the seeder removes a door left there by a farm laid before.</summary>
    public static readonly Point3D OldDoorSpot = new(6694, 3975, 13);

    /// <summary>Every piece: art id, x, y, z on the isle (%d rows).</summary>
    public static readonly (int Id, int X, int Y, int Z)[] Pieces =
    [
%s
    ];
}
''' % (COTTAGE, len(pieces), ANCHOR[0], ANCHOR[1], ANCHOR[2], dtid, dx, dy, dz, len(pieces), rows)
    path = os.path.join(code, 'server', 'customizations', 'Tutorial', 'TutorialIsleFarmLayout.cs')
    open(path, 'w', newline='\n', encoding='utf-8').write(text)
    print(path, len(pieces), 'pieces; door', (dx, dy, dz), hex(dtid))


if __name__ == '__main__':
    main()
