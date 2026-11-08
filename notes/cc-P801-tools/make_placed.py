"""cc-P801: notes/cc-P801-review/placed.md, from gen_jail.py's layout: one line per piece on each branch's plot.
    python -u -P -W ignore notes/cc-P801-tools/make_placed.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import gen_jail as G

WHAT = {'floor': 'stone paver', 'wall': 'grey brick wall', 'bars': 'iron bars', 'gate': 'locked cell gate (static)', 'roof': 'shingle roof',
        'gable': 'grey brick gable', 'prop': 'furnishing', 'sign': 'shop sign, named The New Haven Jail'}
LESSON = [
    ('0x0675+', 5, 8, 0, 'WestCCW', 'MetalDoor, the south door (server item, seeded)'),
    ('0x0E3D', 9, 7, 0, 'south-facing art', 'the marked crate (TutorialJailCrate, hue 0x22, seeded)'),
    ('0x0FEF', 2, 5, 6, 'on the table', "the warden's ledger (TutorialJailLedger, seeded)"),
    ('mobile', 1, 5, 0, 'East', 'Warden Hale, yellow'),
    ('mobile', 6, 4, 0, 'North', 'Mirren, blue'),
    ('mobile', 2, 2, 0, 'South', 'Finn, gray, west cell'),
    ('mobile', 5, 2, 0, 'South', 'Sarn, orange, middle cell'),
    ('mobile', 9, 2, 0, 'South', 'Black Tam, red, east cell'),
    ('mobile', 6, 6, 0, 'lesson only', 'a sneak thief, private to the trainee, gone with the lesson'),
    ('mobile', 7, 6, 0, 'lesson only', 'a New Haven guard, private to the trainee, gone with the lesson'),
]
out = ['# cc-P801 placed pieces: the New Haven jail', '',
       'One layout (`notes/cc-P801-tools/gen_jail.py`, generates `TutorialJailLayout.cs`), two plots. Everything is seeded on world load, only what is missing.', '']
for title, ox, oy, fz in (('Main, SoS land: post 3702,2634, floor Z 21', 3702, 2634, 21), ('Release branch, stock New Haven: post 3469,2597, floor Z 11', 3469, 2597, 11)):
    out += ['## ' + title, '', '### Lesson items and people', '']
    for i, x, y, z, face, what in LESSON:
        out.append('- %s, %d,%d,%d, %s, %s' % (i, ox + x, oy + y, fz + z, face, what))
    out += ['', '### Building', '']
    for role, i, x, y, z in G.layout():
        out.append('- 0x%04X, %d,%d,%d, %s' % (i, ox + x, oy + y, fz + z, WHAT[role]))
    out.append('')
open(os.path.join(G.DOCS, 'notes', 'cc-P801-review', 'placed.md'), 'w', newline='\n').write('\n'.join(out))
print('placed.md lines', len(out))
