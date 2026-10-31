"""cc-P708: moves six halls in design/guild-halls/halls.json onto Chase's picks on the Siege of Sosaria land (Zigholtul's
places), and writes their old posts to old-posts.json (read by edit_moves.py for the server's MovedFrom table).
Rows are rewritten in place, as one line per field group, the file's own layout. Run once; refuses a row already moved.
    python -P edit_halls.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = 'D:/UO/golems/Iron/ShatteredLegacy/design/guild-halls/halls.json'

SOS = " (a place on Zigholtul's Siege of Sosaria map)"
NEW = {
    'league': dict(
        guild="The League (headquarters)", kind="reuse",
        building_name="Valunstead keep, the gatehouse rooms inside the moat (public registry; the great hall behind is the meeting room)" + SOS,
        town="Valunstead", facet=1, rect=[554, 312, 574, 321],
        npc=dict(type="LeagueSteward", x=559, y=317, z=20, facing="East"),
        sign=dict(type="BrassSign", facing="North", x=563, y=320, z=20, name="League Headquarters"),
        travel=dict(x=564, y=322, z=17, note="the keep's south door, over the moat bridge")),
    'merchants': dict(
        guild="Merchants' Exchange", kind="reuse",
        building_name="the counting house in the walled yard north of Valunstead's bank" + SOS,
        town="Valunstead", facet=1, rect=[487, 383, 497, 398],
        npc=dict(type="MerchantGuildmaster", x=492, y=391, z=20, facing="East"),
        sign=dict(type="MerchantsGuild", facing="West", x=497, y=386, z=20, name="The Merchants' Exchange"),
        travel=dict(x=499, y=388, z=15, note="the east doors, on the yard")),
    'healers': dict(
        guild="Healers' Covenant", kind="reuse",
        building_name="Fort Whitestone, the south wing east of the gate" + SOS,
        town="Fort Whitestone", facet=1, rect=[880, 1040, 912, 1056],
        npc=dict(type="HealerGuildmaster", x=902, y=1046, z=32, facing="West"),
        sign=dict(type="HealersGuild", facing="West", x=887, y=1050, z=32, name="The Healers' Covenant"),
        travel=dict(x=890, y=1058, z=30, note="the causeway outside the south gate")),
    'rangers': dict(
        guild="Rangers' League", kind="reuse",
        building_name="Fort Viridian, the inner court of the ruined fort" + SOS,
        town="Fort Viridian", facet=1, rect=[986, 970, 1016, 1018],
        npc=dict(type="OutridersGuildmaster", x=1003, y=1004, z=0, facing="East"),
        sign=dict(type="ArchersGuild", facing="West", x=1013, y=1000, z=0, name="The Rangers' League"),
        travel=dict(x=1015, y=1003, z=0, note="the east gap in the court wall, by the road")),
    'tinkers': dict(
        guild="Tinkers' Union", kind="reuse",
        building_name="Hammerhill, the stone workshop on the west lane (ground floor)" + SOS,
        town="Hammerhill", facet=1, rect=[1484, 1019, 1494, 1027],
        npc=dict(type="TinkerGuildmaster", x=1488, y=1023, z=10, facing="East"),
        sign=dict(type="TinkersGuild", facing="West", x=1493, y=1022, z=10, name="The Tinkers' Union"),
        travel=dict(x=1495, y=1023, z=5, note="the east doors, on the lane")),
    'custodians': dict(
        guild="The Custodians", kind="reuse",
        building_name="Hammerhill, the civic works office north of the bank (ground floor)" + SOS,
        town="Hammerhill", facet=1, rect=[1555, 964, 1566, 973],
        npc=dict(type="SanitationWarden", x=1560, y=967, z=10, facing="South"),
        sign=dict(type="BrassSign", facing="North", x=1559, y=972, z=10, name="The Custodians"),
        travel=dict(x=1560, y=974, z=5, note="the south doors, on the street")),
}


def row_text(key, r):
    head = {k: r[k] for k in ('guild', 'kind', 'building_name', 'town', 'facet', 'rect')}
    s = '    {"key": %s, %s,\n' % (json.dumps(key), json.dumps(head, ensure_ascii=False)[1:-1])
    s += '     "npc": %s,\n' % json.dumps(r['npc'], ensure_ascii=False)
    s += '     "sign": %s,\n' % json.dumps(r['sign'], ensure_ascii=False)
    s += '     "travel": %s}' % json.dumps(r['travel'], ensure_ascii=False)
    return s


text = open(PLAN, encoding='utf-8').read()
data = json.loads(text)
old = {h['key']: h for h in data['halls']}
posts = {}
for key, r in NEW.items():
    h = old[key]
    assert h['town'] != r['town'], (key, 'already moved')
    posts[key] = dict(town=h['town'], facet=h['facet'], npc=h['npc'], sign=h['sign'], kind=h['kind'],
                      building=h.get('building'))
    # the row: from its '{"key": "<key>"' to the closing '}' before the next row's ',\n    {' or the list's end
    m = re.search(r'    \{"key": "%s",.*?\}\}(?=,\n    \{|\n  \])' % re.escape(key), text, re.S)
    assert m, key
    text = text[:m.start()] + row_text(key, r) + text[m.end():]
json.loads(text)
open(PLAN, 'w', encoding='utf-8', newline='\n').write(text)
json.dump(posts, open(os.path.join(HERE, 'old-posts.json'), 'w'), indent=1)
print('moved', ', '.join(NEW))
