"""cc-P801: the New Haven jail as data. One layout, relative to its north-west wall post, for both lands.

    python -u -P -W ignore notes/cc-P801-tools/gen_jail.py mock sos|stock out.jpg [roofless]
    python -u -P -W ignore notes/cc-P801-tools/gen_jail.py json out.json
    python -u -P -W ignore notes/cc-P801-tools/gen_jail.py cs TutorialJailLayout.cs

Footprint 11 x 9: walls x 0..10, y 0..8. Three cells along the north wall (y 1..3, bars on y 3), the guard
hall south of them (y 4..7), the door in the south wall at x 5.
Rules: notes/guides/building-and-decorating.md 2.2 (post NW, corner SE, south piece on the north and south rows, east
piece on the west and east columns), 2.3 (roof at wall Z + 20, x0+1..x1+1, y0+1..y1+1, pitched along y).
"""
import json
import os
import sys

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P708-tools', 'p281sos'))

W, H_ = 10, 8          # last wall column, last wall row
DOOR_X = 5
POST, SOUTH, EAST, CORNER = 0x0036, 0x0034, 0x0035, 0x0033    # grey brick (guide 2.2)
WIN_S, WIN_E = 0x003B, 0x003C                                 # guide 2.2, windows by wall
FLOOR = 0x0519          # stone paver (checked in the render)
BAR_EW = 0x0821         # iron fence, east-west (checked in the render)
IRON_GATE = 0x0828      # IronGate WestCCW's closed art, a static: a cell gate never opens
GATES = (2, 5, 9)
ROOF_W, ROOF_E, ROOF_R = 0x05C4, 0x05C3, 0x05C2               # shingles (guide 2.3)
GABLE = 0x0055          # grey brick gable


def layout():
    """[(role, id, dx, dy, dz)], dz above the floor."""
    r = []
    # floor, inside the box and under the south row and east column (guide 2.2)
    for x in range(1, W + 1):
        for y in range(1, H_ + 1):
            r.append(('floor', FLOOR, x, y, 0))
    # walls
    r.append(('wall', POST, 0, 0, 0))
    r.append(('wall', CORNER, W, H_, 0))
    for x in range(1, W + 1):
        r.append(('wall', WIN_S if x in () else SOUTH, x, 0, 0))
    # cc-P820 (P815 review item 1): the south row runs between the corners. The south-west tile (0, H_) takes the
    # "east" piece only (the west column's loop below); a "south" piece there stuck out past the west wall as a stub.
    for x in range(1, W):
        if x == DOOR_X:
            continue
        r.append(('wall', WIN_S if x in (2, 8) else SOUTH, x, H_, 0))
    for y in range(1, H_ + 1):
        r.append(('wall', WIN_E if y in (6,) else EAST, 0, y, 0))
    for y in range(0 + 1, H_):
        r.append(('wall', WIN_E if y in (6,) else EAST, W, y, 0))
    # cell dividers, stone, y 1..3 (north-south runs)
    for x in (3, 7):
        for y in (1, 2, 3):
            r.append(('wall', EAST, x, y, 0))
    # bars along the south side of the cells, y 3 (east-west runs); the middle tile of each cell is its locked gate.
    # x 3 and 7 are the dividers' own tiles; x 10 is the east wall's.
    for x in (1, 2, 4, 5, 6, 8, 9):
        r.append(('gate' if x in GATES else 'bars', IRON_GATE if x in GATES else BAR_EW, x, 3, 0))
    # roof
    cols = list(range(1, W + 2))
    mid = len(cols) // 2
    for i, x in enumerate(cols):
        rise = min(i, len(cols) - 1 - i)
        rid = ROOF_R if i == mid else (ROOF_W if i < mid else ROOF_E)
        for y in range(1, H_ + 2):
            r.append(('roof', rid, x, y, 19 + rise * 3))
    for i, x in enumerate(cols):
        rise = min(i, len(cols) - 1 - i)
        for c in range(rise):
            r.append(('gable', GABLE, x, H_, 20 + c * 3))
    # guard hall furniture. The crate and the ledger are lesson items, placed by the server at CRATE and LEDGER.
    r += [
        ('prop', 0x0B4A, 2, 5, 0),      # the warden's writing table
        ('prop', 0x0E34, 2, 5, 6),      # a scroll on it, beside the ledger
        # cc-P820 (P815 review items 2 and 3): no wall torches. The one at (1, 6) hung on the west window's floor tile,
        # and both, 15 high at floor + 13, came through the low west eave as orange patches on the roof (guide 11.3,
        # 11.4). A standing candelabra (15 high, under the eave at floor + 22) north of the warden's table lights the hall.
        ('prop', 0x0B26, 2, 4, 0),      # candelabra, behind the warden's table from the camera
        ('prop', 0x0B2C, 8, 4, 0),      # bench along the bars
        ('prop', 0x0B2C, 9, 4, 0),
        ('prop', 0x1262, 1, 1, 7),      # shackles in the cells
        ('prop', 0x1262, 8, 1, 7),
        ('prop', 0x0F34, 5, 1, 0),      # hay
        ('prop', 0x0F34, 1, 2, 0),
        ('prop', 0x0F34, 9, 1, 0),
        ('sign', 0x0B98, 7, 9, -2),     # shop sign's hanger, two tiles east of the door (guide 2.5)
        ('sign', 0x0BD2, 7, 9, -2),     # its board
    ]
    return r


NAMES = {'sign': 'The New Haven Jail'}

# cc-P820: the marked crate (CrateSpot, moved from (9, 7)) and the ledger (LedgerSpot) as the server places them.
SERVER_PLACED = [(0x0E3D, 7, 4, 0), (0x0FEF, 2, 5, 6)]


def emit_cs(path):
    """TutorialJailLayout.cs: the one place the server reads the jail from (this file generates it)."""
    rows = layout()
    out = ['// cc-P801: the New Haven jail, relative to its north-west wall post and floor Z. Generated by shard-migration',
           '// notes/cc-P801-tools/gen_jail.py; do not edit by hand. The door, the crate, the ledger and the people are placed by',
           '// TutorialJail.cs. Rules: notes/guides/building-and-decorating.md 2.2, 2.3, 2.5.', '',
           '#nullable enable', '', 'namespace Server.Tutorial;', '', 'public static class TutorialJailLayout', '{',
           '    /// <summary>Item ID, X and Y from the post, Z from the floor.</summary>',
           '    public static readonly (int Id, int X, int Y, int Z)[] Pieces =', '    [']
    line = '       '
    for _, i, x, y, z in rows:
        c = ' (0x%04X, %d, %d, %d),' % (i, x, y, z)
        if len(line) + len(c) > 118:
            out.append(line)
            line = '       '
        line += c
    out += [line, '    ];', '}', '']
    open(path, 'w', newline=chr(10)).write(chr(10).join(out))
    print('pieces', len(rows))


SITES = {
    # NW post, floor Z (client estimates; the seeder reads them again)
    'sos': ('D:/UO/golems/Iron/p708-work/sosclient', 3702, 2634, 21),
    'stock': ('D:/UO/tool-trials/client-data-copy', 3469, 2597, 11),
}


def main():
    if sys.argv[1] == 'cs':
        emit_cs(sys.argv[2])
        return
    if sys.argv[1] == 'json':
        json.dump([{'role': a, 'id': '0x%04X' % b, 'dx': c, 'dy': d, 'dz': e} for a, b, c, d, e in layout()],
                  open(sys.argv[2], 'w'), indent=0)
        return
    import hallbase as H
    client, ox, oy, fz = SITES[sys.argv[2]]
    H.CLIENT = H.uofiles.CLIENT = client
    F = H.Facet(1)
    roofless = len(sys.argv) > 4
    extra = [(i, ox + x, oy + y, fz + z) for role, i, x, y, z in layout() if not (roofless and role in ('roof', 'gable'))]
    # cc-P820: the lesson items the server places (TutorialJail.cs CrateSpot, LedgerSpot), drawn too for the review
    extra += [(i, ox + x, oy + y, fz + z) for i, x, y, z in SERVER_PLACED]
    H.render(F, ox - 12, oy - 12, ox + 24, oy + 24, extra=extra, grid=0, out=sys.argv[3])
    print('south-row land', [F.landz(ox + x, oy + 9) for x in range(11)])
    print('box land', min(F.landz(ox + x, oy + y) for x in range(11) for y in range(9)),
          max(F.landz(ox + x, oy + y) for x in range(11) for y in range(9)))


if __name__ == '__main__':
    main()
