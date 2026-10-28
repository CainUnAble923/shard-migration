"""cc-P720 items 2, 4, 5: adds the bank's and the lodge's new look to P662's isle-sets.json (run again to rewrite)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(os.path.dirname(HERE), 'cc-P662-tools', 'isle-sets.json')
TEXT = open(P, encoding='utf-8').read()
MARK = ',\n  "_cc-P720":'
TEXT = TEXT.split(MARK)[0].rstrip().rstrip('}').rstrip() if MARK in TEXT else TEXT.rstrip().rstrip('}').rstrip()
R = {}
R['walls'] = {}

R['meadowFence'] = False
R['walls']['shop'] = {
    '_measured': "cc-P720: OSI's stone shop, house multi 0x00A0 (multis.py dump A0): 0x0058 east-west, 0x0057 north-south, "
                 "0x0059 the south-east corner, 0x005A the north-west post, windows 0x005E (east-west) and 0x005D "
                 "(north-south) in place of a run piece, 0x0069 the gable",
    'ew': '0x0058', 'ns': '0x0057', 'corner': '0x0059', 'post': '0x005A',
    'windowEW': '0x005E', 'windowNS': '0x005D'}
R['pitched'] = {
    '_measured': "cc-P720: the stone shop's roof (multi 0x00A0): wooden shingles 0x05C4 (west slope), 0x05C2 (ridge), "
                 "0x05C3 (east slope); eaves 19 above the floor, 3 more a tile; gable 0x0069 from 20 above the floor, "
                 "rows 5 apart. build_isle.check_pitched_roof() rebuilds that roof with the rule.",
    'west': '0x05C4', 'ridge': '0x05C2', 'east': '0x05C3', 'gable': '0x0069',
    'eaveDz': 19, 'rise': 3, 'gableDz': 5}


def carpet(x1, y1, x2, y2):
    """OSI's red carpet (Britain, 1496-1509 x 1513-1517): corners 0x0ACA NW, 0x0ACC NE, 0x0ACB SW, 0x0AC9 SE; edges
    0x0ACE north, 0x0AD0 south, 0x0ACD west, 0x0ACF east; 0x0AC8 inside."""
    out = []
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            n, s, w, e = y == y1, y == y2, x == x1, x == x2
            tid = ('0x0ACA' if n and w else '0x0ACC' if n and e else '0x0ACB' if s and w else '0x0AC9' if s and e else
                   '0x0ACE' if n else '0x0AD0' if s else '0x0ACD' if w else '0x0ACF' if e else '0x0AC8')
            out.append([tid, x, y, 0, 'carpet'])
    return out


# Isle coordinates. Bank floor x 6758-6766, y 3973-3979, door 6762,3980 (south); Merrin 6762,3976 and the practice
# bank box (a server item) 6760,3975 stay clear. Lodge floor x 6778-6786, y 3996-4002, door 6782,3995 (north); Elara
# 6782,3999 stays clear, and 6780,3996 holds the League notice board (a server item).
R['interiors'] = {
    '_rule': "cc-P720: each room's furniture, isle coordinates [id, x, y, z, what]; windows are wall tiles whose run "
             "piece becomes the set's window. Wall torches stand on the floor tile before a north or west wall at +13 "
             "(the playbook). Every inner corner holds a piece.",
    'bank': {
        'windows': [[6759, 3980], [6765, 3980], [6767, 3975], [6767, 3978], [6760, 3972], [6764, 3972], [6757, 3976]],
        'pieces': (
            [['0x0B40', x, 3977, 0, 'counter'] for x in range(6758, 6765)] +
            [['0x0E41', 6758, 3973, 0, 'vault chest'], ['0x0E41', 6759, 3973, 0, 'vault chest'],
             ['0x0E40', 6766, 3973, 0, 'vault chest'], ['0x0E40', 6766, 3974, 0, 'vault chest'],
             ['0x0B26', 6764, 3973, 0, 'candelabra'],
             ['0x0A0C', 6762, 3973, 13, 'wall torch north'], ['0x0A07', 6758, 3975, 13, 'wall torch west'],
             ['0x0A07', 6758, 3978, 13, 'wall torch west'],
             ['0x0B2C', 6758, 3979, 0, 'bench'], ['0x0B26', 6766, 3979, 0, 'candelabra'],
             ['0x0B97', 6764, 3981, 10, 'sign arm'], ['0x0C0B', 6764, 3981, 10, 'bank sign']] +
            carpet(6759, 3978, 6765, 3979)),
    },
    'lodge': {
        'windows': [[6779, 3995], [6785, 3995], [6780, 4003], [6784, 4003], [6787, 3998], [6787, 4001], [6777, 3999]],
        'pieces': (
            [['0x0A97', 6778, 3996, 0, 'bookcase'], ['0x0A98', 6784, 3996, 0, 'bookcase'],
             ['0x0A98', 6785, 3996, 0, 'bookcase'], ['0x0B26', 6786, 3996, 0, 'candelabra'],
             ['0x0A0C', 6779, 3996, 13, 'wall torch north'], ['0x0A0C', 6783, 3996, 13, 'wall torch north'],
             ['0x0A97', 6778, 3997, 0, 'bookcase'], ['0x0A97', 6778, 3998, 0, 'bookcase'],
             ['0x0A07', 6778, 3999, 13, 'wall torch west'], ['0x0A97', 6778, 4000, 0, 'bookcase'],
             ['0x0B4A', 6781, 3998, 0, 'writing table'], ['0x0B4A', 6782, 3998, 0, 'writing table'],
             ['0x0B4A', 6783, 3998, 0, 'writing table'], ['0x0FEF', 6781, 3998, 5, 'book'],
             ['0x0E34', 6783, 3998, 5, 'scroll'],
             ['0x0B90', 6786, 3999, 0, 'table'], ['0x0B4E', 6786, 3998, 0, 'chair'], ['0x0B4F', 6786, 4000, 0, 'chair'],
             ['0x0B26', 6778, 4002, 0, 'candelabra'], ['0x0B26', 6786, 4002, 0, 'candelabra'],
             ['0x1589', 6788, 3998, 8, 'League banner'], ['0x1589', 6788, 4001, 8, 'League banner']] +
            carpet(6780, 4000, 6784, 4002)),
    },
}
# appended as a block of its own, so the hand-laid file above keeps its layout
out = TEXT + MARK + ' "items 2, 4, 5 (Chase\'s isle walk, 10-28): no meadow fence; the bank and the lodge built as OSI\'s stone shop, furnished",\n'
out += '  "meadowFence": false,\n'
out += '  "wallsShop": ' + json.dumps(R['walls']['shop']) + ',\n'
out += '  "pitched": ' + json.dumps(R['pitched']) + ',\n'
out += '  "interiors": {\n    "_rule": ' + json.dumps(R['interiors']['_rule']) + ',\n'
for k in ('bank', 'lodge'):
    out += '    "%s": {"windows": %s,\n      "pieces": [\n' % (k, json.dumps(R['interiors'][k]['windows']))
    out += ',\n'.join('        ' + json.dumps(p) for p in R['interiors'][k]['pieces'])
    out += ']}' + (',' if k == 'bank' else '') + '\n'
out += '  }\n}\n'
json.loads(out)
open(P, 'w', encoding='utf-8', newline='\n').write(out)
print('wrote', P)
