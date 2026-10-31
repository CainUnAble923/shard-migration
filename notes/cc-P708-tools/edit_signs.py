"""cc-P708: the six moved halls' signs, rehung by the building guide's rule (notes/guides/building-and-decorating.md
2.5 and the wall-mounted rule): on the floor tile just outside the door's wall, two tiles along from the door, at the
wall's base Z less 2 (OSI multi 0x64: floor 7, sign 5); a sign on a south wall takes the even art (SignFacing West, as
pinned's house signs 0x0BD2), one on an east wall the odd (SignFacing North, as P281's east-door signs). The first
placement put each sign on the wall tile itself, where the wall drew over it (no sign in any TazUO shot).
    python -P edit_signs.py
"""
import json
import re

PLAN = 'D:/UO/golems/Iron/ShatteredLegacy/design/guild-halls/halls.json'
SIGNS = {
    'league': ('West', 566, 321, 18),       # south wall at y 320, door 564
    'merchants': ('North', 498, 390, 18),   # east wall at x 497, doors 387-388
    'healers': ('West', 893, 1056, 30),     # the south face of the gate's east tower (893,1055), gate 888-892
    'rangers': ('North', 1014, 1008, 3),    # east face of the court wall (1013,1008), gap 1001-1006
    'tinkers': ('North', 1494, 1026, 8),    # east wall at x 1493, doors 1023-1024
    'custodians': ('West', 1563, 973, 8),   # south wall at y 972, doors 1560-1561
}
text = open(PLAN, encoding='utf-8').read()
for key, (facing, x, y, z) in SIGNS.items():
    m = re.search(r'(    \{"key": "%s",.*?\n     "sign": )(\{[^}]*\})' % key, text, re.S)
    assert m, key
    sign = json.loads(m.group(2))
    sign.update(facing=facing, x=x, y=y, z=z)
    new = json.dumps({k: sign[k] for k in ('type', 'facing', 'x', 'y', 'z', 'name')}, ensure_ascii=False)
    text = text[:m.start(2)] + new + text[m.end(2):]
json.loads(text)
open(PLAN, 'w', encoding='utf-8', newline='\n').write(text)
print('rehung', ', '.join(SIGNS))
