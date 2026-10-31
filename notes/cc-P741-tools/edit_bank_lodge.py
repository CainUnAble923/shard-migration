"""cc-P741 items 5 and 6: the bank's surroundings and both interiors, in build_isle.py and isle-sets.json (run once).

Item 5 (Chase 10-30: "sandstone pavement around bank is a lot and unnatural", "bank needs some deco work"): the paving
is the bank's own footprint, an apron before its door and a pad round the fountain, each edged with worn dirt so it
blends into the grass by the dirt-grass transitions (no hard stone-grass seam); a dirt patch under the smithy corner;
a little planting round the walls. Inside, the practice bank's pattern (P734): the counter with its gap, three vault
chests and a strongbox behind it, scales and coin on the counter, candelabras in the corners, torches on the plain
north and west wall pieces, a bench and a potted plant for the queue, the framed carpet; the sign on the 0x0B98 hanger
(0x0B97 lies along the wall, guide 2.5).

Item 6 (Chase 10-30: "league house needs deco work and floor needs work"): one even floor, one board tile, laid under
the south row and east column of the walls as OSI's multis do (guide 2.2); the practice lodge's pattern: bookcases
0x0A98 on the north wall and 0x0A99 on the west wall facing in, none in front of a window, Elara's desk, a long table
with chairs on both sides on a framed carpet, candelabras, a brazier, torches on plain wall pieces, the banners
outside the east wall between its windows."""
import json

p = 'D:/UO/golems/Iron/shard-migration/notes/cc-P662-tools/build_isle.py'
s = open(p, encoding='utf-8').read()


def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)


rep('''    for c in cells(P.SQUARE):
        cls[c] = 'p'
    bank_floor = set(cells(P.BANK))
    lodge_floor = set(cells(P.LODGE))
    bank_ring = W.ring_of(bank_floor)
    lodge_ring = W.ring_of(lodge_floor)''',
    '''    bank_floor = set(cells(P.BANK))
    lodge_floor = set(cells(P.LODGE))
    bank_ring = W.ring_of(bank_floor)
    lodge_ring = W.ring_of(lodge_floor)
    Sq = RULES['square']
    if Sq.get('paved'):
        # cc-P741 item 5 (Chase 10-30: "sandstone pavement around bank is a lot and unnatural"): only the bank's
        # footprint, the apron before its door and the fountain's pad are paved; each paved patch is edged with worn
        # dirt, which blends into the grass by the dirt-grass transitions; the smithy corner stands on dirt. The rest of
        # the old square is grass, and the road's dirt runs up to the apron.
        paved = set(bank_floor | bank_ring)
        for r in Sq['paved']:
            paved |= set(cells((r[0] - DX, r[1] - DY, r[2] - DX, r[3] - DY)))
        for c in paved:
            cls[c] = 'p'
        worn = {(c[0] + a, c[1] + b) for c in paved for a in (-1, 0, 1) for b in (-1, 0, 1)} - paved
        for r in Sq.get('dirt', []):
            worn |= set(cells((r[0] - DX, r[1] - DY, r[2] - DX, r[3] - DY)))
        for c in worn:
            if cls.get(c) == 'g':
                cls[c] = 'd'
                laid.add(c)
        may_grow |= {(c[0] + a, c[1] + b) for c in worn for a in (-1, 0, 1) for b in (-1, 0, 1)}
    else:
        for c in cells(P.SQUARE):
            cls[c] = 'p\'''')
rep('''        rf = stream('floor ' + name)
        for (x, y) in sorted(floor | {door}):
            put(x, y, 0, S.pick_unlike(rf, table(ftable), (x, y), by_tile), '%s floor' % name)''',
    '''        rf = stream('floor ' + name)
        under = set()
        if RULES.get('floorUnderSouthEast'):
            # cc-P741 item 6 (guide 2.2): the floor also lies under the south row and the east column of the walls, as
            # in OSI's house multis, so no land shows at the room's edges
            ry2 = max(c[1] for c in ring | {door}); rx2 = max(c[0] for c in ring | {door})
            under = {c for c in ring if c[1] == ry2 or c[0] == rx2}
        for (x, y) in sorted(floor | {door} | under):
            put(x, y, 0, S.pick_unlike(rf, table(ftable), (x, y), by_tile), '%s floor' % name)''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)

# --- isle-sets.json: the interiors, the floors, the square ---------------------------------------------------------
p = 'D:/UO/golems/Iron/shard-migration/notes/cc-P662-tools/isle-sets.json'
raw = open(p, encoding='utf-8').read()
d = json.loads(raw)

BANK = [
    # the counter, serving side south toward the door, Merrin behind it (6762,3976); the gap at the east end
    ['0x0B40', 6758, 3977, 0, 'counter'], ['0x0B40', 6759, 3977, 0, 'counter'], ['0x0B40', 6760, 3977, 0, 'counter'],
    ['0x0B40', 6761, 3977, 0, 'counter'], ['0x0B40', 6762, 3977, 0, 'counter'], ['0x0B40', 6763, 3977, 0, 'counter'],
    ['0x0B40', 6764, 3977, 0, 'counter'],
    ['0x1852', 6763, 3977, 6, 'scales on the counter'], ['0x0EED', 6761, 3977, 6, 'gold coins on the counter'],
    # the vault behind the counter: three chests and a strongbox against the north wall's plain pieces
    ['0x0E41', 6758, 3973, 0, 'vault chest'], ['0x0E40', 6759, 3973, 0, 'vault chest'],
    ['0x0E41', 6766, 3973, 0, 'vault chest'], ['0x09A8', 6766, 3974, 0, 'strongbox'],
    ['0x0B26', 6765, 3973, 0, 'candelabra, north-east corner'],
    ['0x0A0C', 6762, 3973, 13, 'wall torch north'],
    ['0x0A07', 6758, 3975, 13, 'wall torch west'], ['0x0A07', 6758, 3978, 13, 'wall torch west'],
    # the queue: the framed carpet before the counter, a bench on the west wall, a potted plant and a candelabra
    ['0x0B2C', 6758, 3979, 0, 'bench'],
    ['0x0B26', 6766, 3979, 0, 'candelabra, south-east corner'],
    ['0x11CA', 6766, 3978, 0, 'potted plant'],
    ['0x0ACA', 6759, 3978, 0, 'carpet'], ['0x0ACE', 6760, 3978, 0, 'carpet'], ['0x0ACE', 6761, 3978, 0, 'carpet'],
    ['0x0ACE', 6762, 3978, 0, 'carpet'], ['0x0ACE', 6763, 3978, 0, 'carpet'], ['0x0ACE', 6764, 3978, 0, 'carpet'],
    ['0x0ACC', 6765, 3978, 0, 'carpet'],
    ['0x0ACB', 6759, 3979, 0, 'carpet'], ['0x0AD0', 6760, 3979, 0, 'carpet'], ['0x0AD0', 6761, 3979, 0, 'carpet'],
    ['0x0AD0', 6762, 3979, 0, 'carpet'], ['0x0AD0', 6763, 3979, 0, 'carpet'], ['0x0AD0', 6764, 3979, 0, 'carpet'],
    ['0x0AC9', 6765, 3979, 0, 'carpet'],
    # outside: the sign on its hanger two tiles east of the door (guide 2.5: 0x0B98 sticks out, 0x0B97 lies flat)
    ['0x0B98', 6764, 3981, 10, 'sign hanger'], ['0x0C0B', 6764, 3981, 10, 'bank sign'],
    # a little planting round the walls, off the road and the door's line
    ['0x11CA', 6760, 3981, 0, 'potted plant by the door'],
    ['0x0CA1', 6756, 3974, 0, 'fern by the north-west corner'], ['0x0C9F', 6756, 3979, 0, 'fern by the west wall'],
    ['0x0CA3', 6768, 3973, 0, 'fern by the north-east corner'], ['0x0C9C', 6770, 3971, 0, 'small palm'],
]
LODGE = [
    # Elara's desk between the door and her (she stands at 6782,3999), a book and a scroll on it
    ['0x0B4A', 6781, 3998, 0, 'writing table'], ['0x0B4A', 6782, 3998, 0, 'writing table'],
    ['0x0B4A', 6783, 3998, 0, 'writing table'],
    ['0x0FEF', 6781, 3998, 5, 'book'], ['0x0E34', 6783, 3998, 5, 'scroll'],
    # bookcases backed on plain wall pieces, facing in: 0x0A98 on the north wall, 0x0A99 on the west wall; none in front
    # of a window (north windows 6779, 6785; west window 3999)
    ['0x0A98', 6778, 3996, 0, 'bookcase, north wall'], ['0x0A98', 6784, 3996, 0, 'bookcase, north wall'],
    ['0x0A98', 6786, 3996, 0, 'bookcase, north wall'],
    ['0x0A99', 6778, 3997, 0, 'bookcase, west wall'], ['0x0A99', 6778, 3998, 0, 'bookcase, west wall'],
    ['0x0A99', 6778, 4000, 0, 'bookcase, west wall'], ['0x0A99', 6778, 4001, 0, 'bookcase, west wall'],
    ['0x0A0C', 6781, 3996, 13, 'wall torch north'], ['0x0A0C', 6783, 3996, 13, 'wall torch north'],
    ['0x0A07', 6778, 4002, 13, 'wall torch west'],
    # the long table for the League's meetings, chairs on both sides by the art (0x0B4F north of it faces south,
    # 0x0B50 south of it faces north), on a framed carpet tucked under the chairs
    ['0x0ACA', 6779, 4000, 0, 'carpet'], ['0x0ACE', 6780, 4000, 0, 'carpet'], ['0x0ACE', 6781, 4000, 0, 'carpet'],
    ['0x0ACE', 6782, 4000, 0, 'carpet'], ['0x0ACE', 6783, 4000, 0, 'carpet'], ['0x0ACE', 6784, 4000, 0, 'carpet'],
    ['0x0ACC', 6785, 4000, 0, 'carpet'],
    ['0x0ACD', 6779, 4001, 0, 'carpet'], ['0x0AC8', 6780, 4001, 0, 'carpet'], ['0x0AC8', 6781, 4001, 0, 'carpet'],
    ['0x0AC8', 6782, 4001, 0, 'carpet'], ['0x0AC8', 6783, 4001, 0, 'carpet'], ['0x0AC8', 6784, 4001, 0, 'carpet'],
    ['0x0ACF', 6785, 4001, 0, 'carpet'],
    ['0x0ACB', 6779, 4002, 0, 'carpet'], ['0x0AD0', 6780, 4002, 0, 'carpet'], ['0x0AD0', 6781, 4002, 0, 'carpet'],
    ['0x0AD0', 6782, 4002, 0, 'carpet'], ['0x0AD0', 6783, 4002, 0, 'carpet'], ['0x0AD0', 6784, 4002, 0, 'carpet'],
    ['0x0AC9', 6785, 4002, 0, 'carpet'],
    ['0x0B90', 6780, 4001, 0, 'long table'], ['0x0B90', 6781, 4001, 0, 'long table'],
    ['0x0B90', 6782, 4001, 0, 'long table'], ['0x0B90', 6783, 4001, 0, 'long table'],
    ['0x0B90', 6784, 4001, 0, 'long table'],
    ['0x0B4F', 6781, 4000, 0, 'chair'], ['0x0B4F', 6783, 4000, 0, 'chair'],
    ['0x0B50', 6780, 4002, 0, 'chair'], ['0x0B50', 6782, 4002, 0, 'chair'], ['0x0B50', 6784, 4002, 0, 'chair'],
    ['0x0FF2', 6780, 4001, 6, 'book on the table'], ['0x09EE', 6782, 4001, 6, 'mug on the table'],
    ['0x0E34', 6784, 4001, 6, 'map on the table'],
    ['0x0B26', 6786, 3998, 0, 'candelabra'], ['0x0B26', 6786, 4002, 0, 'candelabra, south-east corner'],
    ['0x0E31', 6786, 4000, 0, 'brazier'],
    # outside: the League's banners flat on the east wall between its windows (3998, 4001), Z 8 (P720)
    ['0x1589', 6788, 3997, 8, 'League banner'], ['0x1589', 6788, 4000, 8, 'League banner'],
]
assert len({(t[1], t[2], t[0]) for t in BANK}) == len(BANK)


def to_text(rows):
    return '[' + ', '.join(json.dumps(r) for r in rows) + ']'


old_bank = json.dumps(d['interiors']['bank']['pieces'])
old_lodge = json.dumps(d['interiors']['lodge']['pieces'])
# replace in the raw text, keeping the rest of the file byte for byte
import re


def replace_pieces(text, name, rows):
    i = text.index('"%s": {' % name, text.index('"interiors"'))
    j = text.index('"pieces": [', i)
    k = j + len('"pieces": ')
    depth = 0
    for n in range(k, len(text)):
        if text[n] == '[':
            depth += 1
        elif text[n] == ']':
            depth -= 1
            if depth == 0:
                break
    return text[:k] + to_text(rows) + text[n + 1:]


raw = replace_pieces(raw, 'bank', BANK)
raw = replace_pieces(raw, 'lodge', LODGE)
old = '''"lodge": {"0x04A9": 50, "0x04AA": 10, "0x04AB": 10, "0x04AC": 10, "0x04AD": 10, "0x04AE": 5, "0x04AF": 5}'''
assert old in raw
raw = raw.replace(old, '''"lodge": {"0x04A9": 1}''', 1)
old = '"square": {'
assert old in raw
raw = raw.replace(old, '"floorUnderSouthEast": true,\n  "_lodgeFloor": "cc-P741 item 6 (Chase 10-30: \\"floor needs work\\"): one board tile, 0x04A9, and the floor under the walls\' south row and east column (guide 2.2); P720 mixed seven board tiles",\n  "square": {"_paved": "cc-P741 item 5: isle coordinates x1 y1 x2 y2: the apron before the bank door, the fountain\'s pad; dirt: the smithy corner (forge, anvil)", "paved": [[6759, 3981, 6765, 3982], [6767, 3983, 6769, 3985]], "dirt": [[6768, 3974, 6770, 3978]], ', 1)
json.loads(raw)
open(p, 'w', encoding='utf-8', newline='').write(raw)
print('ok')
