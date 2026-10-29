"""cc-P725: the walk after the shore change. Compares plan-cells.json (this build's walkable tiles, pinned movement)
with P720's, and checks that no walkable tile is sea: wet land, or a tile under one of OSI's whole-tile or half-tile
water pieces (0x1797-0x17A4, 0x17A9-0x17AC). OSI's small surf pieces (0x17A5-0x17A8, 0x17AD-0x17B2) lie on the
last sand tile, which stays walkable as on OSI's beaches.
    python -P walk_check.py <built folder> <before plan-cells.json> <after plan-cells.json>"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
from mapbuild import uofiles as U

folder, before, after = sys.argv[1:4]
b = {tuple(c) for c in json.load(open(before))['walkable']}
a = {tuple(c) for c in json.load(open(after))['walkable']}
ltd = U.read_tiledata()[0]
mf = U.MapFile(folder, 1)
SEA_PIECES = set(range(0x1797, 0x17A5)) | set(range(0x17A9, 0x17AD))
water_st = {(x, y) for (x, y, z, t) in U.statics_in(folder, 1, 6594, 3905, 6865, 4049) if t in SEA_PIECES}
wet = [c for c in a if ltd[mf.get(*c)[0]][0] & (U.WET | U.IMPASSABLE) or c in water_st]
print('walkable before', len(b), 'after', len(a), '; new', len(a - b), '; lost', len(b - a))
deck = {(x, y) for (x, y, z, t) in U.statics_in(folder, 1, 6594, 3905, 6865, 4049) if t in (0x07C9, 0x07CD)}
print('walkable tiles over the sea on the dock planks:', len([c for c in wet if c in deck]))
print('walkable tiles that are sea, off the dock:', len([c for c in wet if c not in deck]), sorted(c for c in wet if c not in deck)[:10])
lost = sorted(b - a)
print('lost tiles, their land and statics:')
for c in lost[:15]:
    print('  ', c, mf.get(*c), [s for s in U.statics_in(folder, 1, c[0], c[1], c[0], c[1])])
