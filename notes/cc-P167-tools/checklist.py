"""cc-P181: the pre-render checklist for the Burrows (notes/map-building-playbook.md section 4). Re-plans the build
from layout.json and plan-sets.json (no map file is touched) and prints the PASS/FAIL table for the notes.

    python -P checklist.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
import build_burrows as bb  # noqa: E402
from mapbuild import checklist as C, uofiles, walls as W  # noqa: E402

SOUTH_FACING = {0x0A97, 0x0A98, 0x0A9B, 0x0A9D, 0x0B26}   # bookcases with the back on the north edge, plus the end candelabra
EAST_FACING = {0x0A99, 0x0A9A, 0x0A9C, 0x0A9E}


def main():
    layout = json.load(open(bb.LAYOUT, encoding='utf-8'))
    rules = json.load(open(bb.RULES, encoding='utf-8'))
    spawners, pts = bb.read_points()
    land, statics, stats, counts, floor, opening, walls, report = bb.plan(layout, rules, spawners, pts, quiet=True)
    prev = json.load(open(bb.CELLS))
    rows = [(o['name'], tuple(o['rect'])) for o in layout['obstacles'] if o['name'].startswith('Stacks')]
    solid = lambda c: c not in floor
    groups = W.opening_groups(opening, solid)
    results = [
        ('walls against a test room', ) + C.walls_against_test_room(rules['wallSets']),
        ('no diagonal wall runs', ) + C.no_diagonal_runs(walls),
        ('rows straight (the Stacks)', ) + C.rows_straight(statics, rows, {'south-facing': SOUTH_FACING, 'east-facing': EAST_FACING}),
        ('every inner corner dressed', ) + C.corners_dressed(report['corners']),
        ('every opening framed or a passage', ) + C.frames_all(report['frames'], len(groups)),
        ('variety: no identical decor side by side', ) + C.variety(statics, skip_why=('wall', 'stone pillar', 'frame', 'end piece', 'crawlway')),
        ('transitions audited (slope spread <= 12)', ) + C.transitions(report['slope audit']),
        ('one wall piece per tile', ) + (not report['doubled wall tiles'], report['doubled wall tiles'] or 'no doubled wall tiles'),
        ('walkable-floor gate', ) + C.gate(uofiles.same_cells(prev, floor, opening, walls)),
    ]
    print(C.table(results))
    print()
    print('statics %d, distinct ids %d, land tiles %d' % (len(statics), len({s[3] for s in statics}), len(land)))
    return all(r[1] for r in results)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
