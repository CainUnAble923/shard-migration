# cc-P266 WRITES placement.json: P34's 61 rows as they are (notes/cc-P34-tools/placement.json, the table Chase has
# not walked yet), plus this task's rows for the bank, the square and the main roads. Every row is then checked by
# validate.py; nothing here reads the map. Modes (validate.py has the rules): floor, square, pier, table, wall, post,
# indoor, wallout (P34's), wallfoot (new: outside, at the foot of a wall, a street tile allowed).
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art_src as S
I = S.ID
OSI = {'snow-a': 0x08E2, 'snow-b': 0x08E0, 'snow-c': 0x08E6, 'snow-d': 0x08E5, 'snow-e': 0x08E3, 'snowy-tree': 0x2377,
       'wreath-n': 0x232C, 'wreath-w': 0x232D, 'gift-a': 0x3C54, 'gift-b': 0x3C55, 'gift-c': 0x3C56,
       'patch-1': 0x3C6B, 'patch-2': 0x3C6C, 'patch-3': 0x3C6D}
SNOW_NAME = {0x08E2: 'a pile of snow', 0x08E0: 'a pile of snow', 0x08E6: 'a pile of snow', 0x08E5: 'a pile of snow', 0x08E3: 'a pile of snow'}

rows = json.load(open(os.path.join(HERE, '..', 'cc-P34-tools', 'placement.json')))
assert len(rows) == 61


def row(key, area, x, y, z, item, name, mode, why, facing='-', layer='community'):
    rows.append({'key': key, 'area': area, 'x': x, 'y': y, 'z': z, 'map': 'Trammel', 'itemId': item, 'name': name,
                 'facing': facing, 'layer': layer, 'mode': mode, 'why': why})


# ---------------------------------------------------------------- the bank, inside (floor z20)
# The hall is x3485-3490, y2569-2578; the tellers stand at 3484,2570 and 3484,2576 (pinned Vendors.json) with the
# west wall x3483 behind them; the doors are in the east wall x3491 at y2571 and y2573 (swings 3492,2570 and
# 3492,2574). The alcove north of the hall is x3487-3490, y2565-2568, its north wall y2564, its west wall x3486.
# The walk from the doors to the tellers crosses x3485-3490 at y2570-2577: nothing that blocks goes there.
row('bank-tree', 'bank', 3489, 2565, 20, I['tree-large'], 'a decorated Christmas tree', 'indoor',
    'the alcove, against its north wall; the tellers and the doors are clear')
row('bank-gift1', 'bank', 3488, 2566, 20, OSI['gift-a'], 'a present', 'indoor', 'at the tree')
row('bank-gift2', 'bank', 3490, 2566, 20, OSI['gift-c'], 'a present', 'indoor', 'at the tree')
row('bank-gnome', 'bank', 3489, 2567, 20, I['gnome'], 'a holiday gnome', 'indoor', 'in front of the tree')
row('bank-soldier', 'bank', 3490, 2567, 20, I['soldier'], 'a toy soldier', 'indoor', 'in front of the tree')
row('bank-plush', 'bank', 3490, 2568, 20, I['plush-dragon'], 'a dragon plushie', 'indoor', 'at the alcove mouth')
row('bank-calendar', 'bank', 3487, 2566, 20, I['calendar-w'], 'an advent calendar', 'wall',
    'the alcove\'s west wall (x3486), beside the tree: double-click to open a door', facing='west', layer='calendar')
row('bank-ribbon-w', 'bank', 3487, 2567, 20, I['ribbon-w'], 'a ribbon garland', 'wall', 'the alcove\'s west wall, under the calendar', facing='west')
row('bank-ribbon-n', 'bank', 3486, 2569, 20, I['ribbon-n'], 'a ribbon garland', 'wall', 'the hall\'s north wall (y2568), its west end', facing='north')
row('bank-candle-tall', 'bank', 3487, 2569, 20, I['candle-tall'], 'a tall candle stand', 'indoor', 'the hall\'s north wall, east of the garland; the north wall shows behind it')
row('bank-antler', 'bank', 3488, 2570, 20, I['antler'], 'an antler candelabra', 'indoor', 'the hall\'s north side, off the carpet and the tellers\' line')
row('bank-potted', 'bank', 3490, 2569, 20, I['potted'], 'a potted holiday tree', 'indoor', 'the hall\'s north-east, at the alcove mouth')
row('bank-poinsettia-1', 'bank', 3486, 2570, 20, I['poinsettia'], 'a poinsettia', 'indoor', 'the hall\'s north-west corner')
row('bank-poinsettia-2', 'bank', 3486, 2577, 20, I['poinsettia'], 'a poinsettia', 'indoor', 'the hall\'s south-west corner')
row('bank-candle-short-1', 'bank', 3484, 2572, 20, I['candle-short'], 'a candle', 'indoor', 'the tellers\' line, against the west wall between the two tellers')
row('bank-candle-short-2', 'bank', 3484, 2574, 20, I['candle-short'], 'a candle', 'indoor', 'the tellers\' line, against the west wall between the two tellers')

# ---------------------------------------------------------------- the bank, outside (ground z14-15; the walls at z20)
row('bank-out-tree-n', 'bank', 3493, 2567, 15, I['tree-small'], 'a decorated Christmas tree', 'wallfoot',
    'outside, north of the porch and the hitching post, by the east face', layer='community')
row('bank-out-tree-s', 'bank', 3493, 2576, 14, I['tree-small'], 'a decorated Christmas tree', 'wallfoot',
    'outside, south of the porch, by the east face')
row('bank-out-tree-sw', 'bank', 3479, 2580, 15, I['tree-small'], 'a decorated Christmas tree', 'wallfoot',
    'outside, at the foot of the south face, west of the Minter\'s door (3481,2579)')
row('bank-out-tree-se', 'bank', 3484, 2580, 15, I['tree-small'], 'a decorated Christmas tree', 'wallfoot',
    'outside, at the foot of the south face, east of the Minter\'s door')
row('bank-wreath-n', 'bank', 3492, 2566, 20, OSI['wreath-w'], 'a holiday wreath', 'wallout',
    'outside, on the east face (x3491) north of the porch; the east face shows (pinned Wreath.cs:258, 0x232D the west-wall facing)', facing='west', layer='osi')
row('bank-wreath-s', 'bank', 3492, 2578, 20, OSI['wreath-w'], 'a holiday wreath', 'wallout',
    'outside, on the east face south of the porch, by the hitching post', facing='west', layer='osi')
row('bank-snow-1', 'bank', 3493, 2565, 15, OSI['snow-a'], 'a pile of snow', 'floor', 'the grass north-east of the bank', layer='osi')
row('bank-snow-2', 'bank', 3494, 2566, 15, OSI['patch-1'], 'a snow patch', 'floor', 'the grass north-east of the bank')
row('bank-snow-3', 'bank', 3495, 2568, 15, OSI['snow-c'], 'a pile of snow', 'floor', 'the grass east of the porch', layer='osi')
row('bank-snow-4', 'bank', 3496, 2578, 14, OSI['patch-2'], 'a snow patch', 'floor', 'the grass south-east of the bank')
row('bank-snow-5', 'bank', 3495, 2580, 14, OSI['snow-b'], 'a pile of snow', 'floor', 'the grass south-east of the bank', layer='osi')
row('bank-snow-6', 'bank', 3490, 2581, 14, OSI['snowy-tree'], 'a snowy tree', 'floor', 'the grass south of the bank', layer='osi')
row('bank-snow-7', 'bank', 3474, 2571, 7, OSI['snowy-tree'], 'a snowy tree', 'floor', 'the slope west of the bank, by the fence', layer='osi')
row('bank-snow-8', 'bank', 3475, 2583, 7, OSI['snow-d'], 'a pile of snow', 'floor', 'the slope south-west of the bank', layer='osi')

# ---------------------------------------------------------------- the square (z14): more at P34's tree, and the grass on its north-east
row('sq-gnome', 'square', 3512, 2578, 14, I['gnome'], 'a holiday gnome', 'square', 'at the foot of the square\'s tree (sq-tree 3512,2577), south')
row('sq-soldier', 'square', 3513, 2577, 14, I['soldier'], 'a toy soldier', 'square', 'at the foot of the square\'s tree, east')
row('sq-tree-ne-1', 'square', 3509, 2570, 14, I['tree-small'], 'a decorated Christmas tree', 'floor', 'the grass north-east of the square, by the road in from the north')
row('sq-tree-ne-2', 'square', 3513, 2570, 14, I['tree-small'], 'a decorated Christmas tree', 'floor', 'the grass north-east of the square')
row('sq-snow-ne', 'square', 3507, 2569, 14, OSI['snow-e'], 'a pile of snow', 'floor', 'the grass north-east of the square, between the two trees', layer='osi')
row('sq-poinsettia', 'square', 3511, 2577, 14, I['poinsettia'], 'a poinsettia', 'square', 'at the foot of the square\'s tree, west, by Santa\'s bag')

# ---------------------------------------------------------------- the main roads: small lit trees on the grass beside the road, snow between
row('road-inn-w', 'main road', 3498, 2536, 21, I['tree-small'], 'a decorated Christmas tree', 'floor', 'the road south from the inn, west side, below the lamp post at 3500,2529')
row('road-inn-e', 'main road', 3507, 2535, 20, I['tree-small'], 'a decorated Christmas tree', 'floor', 'the road south from the inn, east side')
row('road-inn-snow', 'main road', 3496, 2536, 22, OSI['patch-3'], 'a snow patch', 'floor', 'the grass west of the road below the inn')
row('road-healer', 'main road', 3484, 2544, 15, I['tree-small'], 'a decorated Christmas tree', 'floor', 'the road west to the Healer\'s Hall')
row('road-main-w', 'main road', 3494, 2560, 15, I['tree-small'], 'a decorated Christmas tree', 'floor', 'the main road into the square, west side, north-east of the bank')
row('road-main-e', 'main road', 3512, 2561, 14, I['tree-small'], 'a decorated Christmas tree', 'floor', 'the main road into the square, east side')
row('road-main-snow-w', 'main road', 3493, 2559, 15, OSI['snow-a'], 'a pile of snow', 'floor', 'the grass beside the main road, west', layer='osi')
row('road-main-snow-e', 'main road', 3511, 2563, 14, OSI['patch-1'], 'a snow patch', 'floor', 'the grass beside the main road, east')
row('road-east-n', 'main road', 3521, 2567, 7, I['tree-small'], 'a decorated Christmas tree', 'floor', 'the east road to the gate, on the grass north of it (the road runs low here, z6-7)')
row('road-east-s', 'main road', 3519, 2572, 6, I['tree-small'], 'a decorated Christmas tree', 'floor', 'the east road to the gate, south side')
row('road-east-snow', 'main road', 3524, 2567, 6, OSI['snow-c'], 'a pile of snow', 'floor', 'the grass north of the east road', layer='osi')

# ---------------------------------------------------------------- the inn: the advent candles on a free table
row('inn-advent', 'inn', 3503, 2513, 33, I['advent'], 'advent candles', 'table', 'on the table at z27 (height 6) by the north wall, a table P34 left bare')

json.dump(rows, open(os.path.join(HERE, 'placement.json'), 'w', encoding='ascii'), indent=1)
print('wrote', len(rows), 'rows (61 of P34, %d new)' % (len(rows) - 61))
