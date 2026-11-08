"""cc-P820 (P801's make_placed.py): notes/cc-P820-review/placed.md, from gen_jail.py's layout: one line per piece on each branch's plot.
    python -u -P -W ignore notes/cc-P820-tools/make_placed.py
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cc-P801-tools'))
import gen_jail as G

PROPS = {0x0B4A: "the warden's writing table", 0x0E34: 'a scroll on the table', 0x0B26: 'standing candelabra, free-standing north of the table (replaces the two west-wall torches; 15 high, under the roof at floor + 22)',
         0x0B2C: 'bench along the bars, facing the hall', 0x1262: 'shackles on the cell wall', 0x0F34: 'hay in a cell', 0x0B98: 'shop sign hanger, sticks out from the south wall, two tiles east of the door', 0x0BD2: 'its board, named The New Haven Jail'}
WHAT = {'floor': 'stone paver', 'wall': 'grey brick wall', 'bars': 'iron bars', 'gate': 'locked cell gate (static)', 'roof': 'shingle roof',
        'gable': 'grey brick gable', 'prop': 'furnishing', 'sign': 'shop sign, named The New Haven Jail'}
LESSON = [
    ('0x0675+', 5, 8, 0, 'WestCCW', 'MetalDoor, the south door (server item, seeded)'),
    ('0x0E3D', 7, 4, 0, 'stands free in the hall', 'the marked crate (TutorialJailCrate, hue 0x22, seeded), beside the bench; cc-P820 moved it from the south-east corner (9,7)'),
    ('0x0FEF', 2, 5, 6, 'on the table', "the warden's ledger (TutorialJailLedger, seeded)"),
    ('mobile', 1, 5, 0, 'East', 'Warden Hale, yellow'),
    ('mobile', 6, 4, 0, 'North', 'Mirren, blue'),
    ('mobile', 2, 2, 0, 'South', 'Finn, gray, west cell'),
    ('mobile', 5, 2, 0, 'South', 'Sarn, orange, middle cell'),
    ('mobile', 9, 2, 0, 'South', 'Black Tam, red, east cell'),
    ('mobile', 6, 6, 0, 'lesson only', 'a sneak thief, private to the trainee, gone with the lesson'),
    ('mobile', 7, 6, 0, 'lesson only', 'a New Haven guard, private to the trainee, gone with the lesson'),
]
out = ['# cc-P820 placed pieces: the New Haven jail (P801, fixed after the P815 review)', '',
       'One layout (`notes/cc-P801-tools/gen_jail.py`, generates `TutorialJailLayout.cs`), two plots. Everything is seeded on world load, only what is missing.',
       'Walls by the guide 2.2 rule: post 0x0036 NW, L corner 0x0033 SE, "south" 0x0034 on the north row to the NE tile and on the south row between the corners, "east" 0x0035 on the west column to the SW tile and on the east column; windows 0x003B (south wall) and 0x003C (west and east walls).', '']
for title, ox, oy, fz in (('Main, SoS land: post 3702,2634, floor Z 21', 3702, 2634, 21), ('Release branch, stock New Haven: post 3469,2597, floor Z 11', 3469, 2597, 11)):
    out += ['## ' + title, '', '### Lesson items and people', '']
    for i, x, y, z, face, what in LESSON:
        out.append('- %s, %d,%d,%d, %s, %s' % (i, ox + x, oy + y, fz + z, face, what))
    out += ['', '### Removed on load from a cc-P801 world (TutorialJail.Retired)', '',
            '- 0x0034, %d,%d,%d, grey brick "south" piece on the south-west corner tile (stub past the west wall; the tile keeps its 0x0035)' % (ox, oy + 8, fz),
            '- 0x0A07, %d,%d,%d, wall torch on the floor tile of the west window' % (ox + 1, oy + 6, fz + 13),
            '- 0x0A07, %d,%d,%d, wall torch, west wall (with the other, it showed through the low eave)' % (ox + 1, oy + 4, fz + 13),
            '- the marked crate moves from %d,%d,%d to %d,%d,%d (the same item)' % (ox + 9, oy + 7, fz, ox + 7, oy + 4, fz)]
    out += ['', '### Building', '']
    for role, i, x, y, z in G.layout():
        out.append('- 0x%04X, %d,%d,%d, %s' % (i, ox + x, oy + y, fz + z, PROPS.get(i, WHAT[role]) if role in ('prop', 'sign') else WHAT[role]))
    out.append('')
open(os.path.join(G.DOCS, 'notes', 'cc-P820-review', 'placed.md'), 'w', newline='\n').write('\n'.join(out))
print('placed.md lines', len(out))
