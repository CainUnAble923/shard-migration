"""cc-P818: the League lodge's door to the east wall, in the isle driver's data (run once; idempotent). Text edits, so
isle-sets.json keeps its hand-written layout.

isle-sets.json interiors.lodge.pieces (shifted coordinates, as the file holds them):
  - the brazier 0x0E31 inside on the new door's floor tile (6786,4000) goes; two braziers stand outside instead, either
    side of the door's approach (6788,3999 and 6788,4001): the lit doorway;
  - the candelabra 0x0B26 at 6786,3998 stood on the floor tile of the east window 6787,3998 (guide 11.4): to 6786,3999;
  - the League banner 0x1589 at 6788,4000 (Z 8) hung on the door's own tile: to 6788,4002, the plain wall south of the
    window 6787,4001 (the other stays at 6788,3997);
  - a walk of sandstone bricks 0x0525-0x0528 (the bank apron's tan) from the road (6789,3990) south to the door's
    step (6789,4000, 6788,4000).
build_isle.py's LODGE_DOOR moves from (6358, 2003) (north wall, 6782,3995) to (6363, 2008) (east wall, 6787,4000).
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, '..', 'cc-P662-tools')
p = os.path.join(TOOLS, 'isle-sets.json')
s = open(p, encoding='utf-8').read()
if 'cc-P818' not in s:
    walk = [(6788, 4000)] + [(6789, y) for y in range(4000, 3989, -1)]
    added = ['["0x0E31", 6788, 3999, 0, "brazier by the east door (cc-P818)"]',
             '["0x0E31", 6788, 4001, 0, "brazier by the east door (cc-P818)"]']
    added += ['["0x%04X", %d, %d, 0, "walk to the east door (cc-P818)"]' % (0x0525 + (x + y) % 4, x, y) for (x, y) in walk]
    for old, new in (
            ('["0x0E31", 6786, 4000, 0, "brazier"], ', ''),
            ('["0x0B26", 6786, 3998, 0, "candelabra"]',
             '["0x0B26", 6786, 3999, 0, "candelabra, beside the east door (cc-P818: off the window 6787,3998)"]'),
            ('["0x1589", 6788, 4000, 8, "League banner"]',
             '["0x1589", 6788, 4002, 8, "League banner (cc-P818: off the door)"], ' + ', '.join(added))):
        assert s.count(old) == 1, old
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)
d = json.loads(s)  # still valid JSON
print('lodge pieces', len(d['interiors']['lodge']['pieces']))

b = os.path.join(TOOLS, 'build_isle.py')
s = open(b, encoding='utf-8').read()
s2 = re.sub(r'^LODGE_DOOR = \(6358, 2003\)$',
            'LODGE_DOOR = (6363, 2008)   # cc-P818: the east wall (6787,4000); was (6358, 2003), the north wall',
            s, flags=re.M)
if s2 != s:
    open(b, 'w', encoding='utf-8', newline='\n').write(s2)
print('door moved' if s2 != s else 'door already moved')
