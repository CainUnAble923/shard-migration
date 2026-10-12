# cc-P34 WRITES placement.json: the proposed rows. Modes: floor (on the ground or a floor), table (on a table top),
# wall (hung on the floor tile in front of a north or west wall, the visible faces), post (on a lamp post's tile),
# square/pier (a walkway is allowed: the square is all road, the sleigh sits on the pier). Snow spots are picked
# by pick.floor so they are never on a road, a door or a protected tile.
import json
exec(open('pick.py').read())
OSI, COM = 'osi', 'community'
R = []


def row(key, area, x, y, z, item, name, facing, layer, mode, why):
    R.append(dict(key=key, area=area, x=x, y=y, z=z, map='Trammel', itemId=item, name=name, facing=facing,
                  layer=layer, mode=mode, why=why))


# The square by the quest board (all road; the plaza's edges, the board's corner left clear)
row('sq-tree', 'square', 3512, 2577, 14, 15442, 'a christmas tree', '-', COM, 'square', 'east edge of the plaza, clear of the lamp posts and the ruined wall at 3511-3512,2580')
row('sq-bag', 'square', 3511, 2578, 14, 15443, "Santa's bag", '-', COM, 'square', 'at the tree')
row('sq-gift1', 'square', 3513, 2578, 14, 15444, 'a present', '-', COM, 'square', 'at the tree')
row('sq-gift2', 'square', 3511, 2576, 14, 15445, 'a present', '-', COM, 'square', 'at the tree')
row('sq-gift3', 'square', 3513, 2576, 14, 15446, 'a present', '-', COM, 'square', 'at the tree')
row('sq-father', 'square', 3500, 2581, 14, 15424, 'a statue of Father Christmas', '-', COM, 'square', 'west edge of the plaza')
row('sq-firepit', 'square', 3499, 2577, 14, 15429, 'a raised firepit', '-', COM, 'square', 'west of the plaza, two tiles from the Reset Stone')
row('sq-snowman', 'square', 3501, 2583, 14, 0x2328, 'a snowman', '-', OSI, 'square', 'south-west corner of the plaza (pinned Snowman.cs:5, 0x2328)')

# Entrances: a candy cane arch each side of the road where it leaves town (just off the road)
for k, (x, y, art, why) in enumerate([
        (3417, 2527, 15447, 'west road (x3420, y2527-2531), north side, on grass: 3420,2525 holds a lantern on a stone base'), (3420, 2533, 15447, 'west road, south side'),
        (3494, 2487, 15448, 'north road (y2486, x3496-3503), west side'), (3505, 2487, 15448, 'north road, east side'),
        (3541, 2562, 15447, 'east road (x3540, y2567-2572), north side, on grass: the tiles nearer have a stone base and boards'), (3540, 2574, 15447, 'east road, south side'),
        (3468, 2635, 15448, 'south road (y2636, x3469-3474), west side'), (3476, 2635, 15448, 'south road, east side')]):
    row('gate-%d' % (k + 1), 'entrance', x, y, avgz(x, y), art, 'a candy cane arch', '-', COM, 'floor', why)

# Main road: wreaths and bells on lamp posts (pinned Wreath.cs:254 0x232C, HolidayBell.cs:29 0x1C12)
for k, (x, y, z, item, nm) in enumerate([
        (3498, 2563, 15, 0x232C, 'a holiday wreath'), (3492, 2564, 15, 0x1C12, 'a holiday bell'),
        (3483, 2562, 15, 0x232C, 'a holiday wreath'), (3510, 2585, 14, 0x1C12, 'a holiday bell'),
        (3517, 2566, 16, 0x232C, 'a holiday wreath'), (3519, 2578, 7, 0x1C12, 'a holiday bell'),
        (3500, 2529, 22, 0x232C, 'a holiday wreath'), (3489, 2523, 40, 0x1C12, 'a holiday bell')]):
    row('post-%d' % (k + 1), 'main road', x, y, z, item, nm, 'north' if item == 0x232C else '-', OSI, 'post',
        'lamp post 0x0B24 at %d,%d z%d on the main road' % (x, y, z))

# Bountiful Harvest Inn (ground floor z27; the tables are 27 + 6)
for key, x, y, item, nm in [('inn-eggnog1', 3498, 2514, 15449, 'a tray of eggnog'), ('inn-cookies', 3498, 2516, 15451, 'a pan of cookies'),
                            ('inn-turkey', 3501, 2514, 15454, 'a roast turkey'), ('inn-platter', 3506, 2515, 15453, 'a holiday platter'),
                            ('inn-canes', 3506, 2517, 15452, 'a tray of candy canes'), ('inn-gingerbread', 3506, 2519, 15455, 'a gingerbread house'),
                            ('inn-eggnog2', 3507, 2522, 15450, 'a tray of eggnog')]:
    row(key, 'inn', x, y, 33, item, nm, '-', COM, 'table', 'on the table at z27 (height 6): top z33')
row('inn-fireplace', 'inn', 3508, 2515, 27, 15456, 'a christmas fireplace', 'west', COM, 'indoor', "its back to the hall's east wall (x3509), facing into the hall")
row('inn-stocking1', 'inn', 3508, 2513, 27, 0x2BD9, 'a stocking', 'north', OSI, 'wall', 'north wall of the hall (pinned Stockings.cs:6: 0x2BD9 is the north-wall facing)')
row('inn-stocking2', 'inn', 3505, 2513, 27, 0x2BDB, 'a stocking', 'north', OSI, 'wall', 'north wall of the hall (Stockings.cs:20: 0x2BDB)')
row('inn-stove1', 'inn', 3494, 2516, 27, 15434, 'an iron stove', '-', COM, 'indoor', 'the west room with the barrels: the kitchen')
row('inn-stove2', 'inn', 3508, 2524, 27, 15438, 'a stone stove', '-', COM, 'indoor', 'the south-east room, by its east wall (x3509)')
row('inn-mistletoe', 'inn', 3510, 2519, 27, 0x2375, 'mistletoe', 'west', OSI, 'wallout', 'outside, on the east wall (x3509) just south of the front door 3509,2518, by the porch rail; the east face shows; pinned Mistletoe.cs:270, 0x2375 the west-wall facing')
row('inn-painting', 'inn', 3502, 2514, 27, 15459, 'a holiday painting', 'north', COM, 'wall', 'north wall')
row('inn-snowshield', 'inn', 3497, 2515, 27, 15465, 'a snow-covered shield', 'west', COM, 'wall', "west wall of the hall")

# Healer's Hall (z35; walls x3453 and x3462, north wall y2546) and the League field office (z18)
row('heal-wreath', 'healer hall', 3461, 2547, 35, 0x232C, 'a holiday wreath', 'north', OSI, 'wall', 'north wall, by the east door 3462,2551')
row('heal-garland', 'healer hall', 3457, 2547, 35, 15457, 'a garland', 'north', COM, 'wall', 'north wall, the middle')
row('heal-painting', 'healer hall', 3454, 2549, 35, 15460, 'a holiday painting', 'west', COM, 'wall', 'west wall')
row('heal-snowpainting', 'healer hall', 3454, 2552, 35, 15463, 'a snow-covered painting', 'west', COM, 'wall', 'west wall')
row('heal-shield', 'healer hall', 3459, 2547, 35, 15466, 'a snow-covered shield', 'north', COM, 'wall', 'north wall')
row('off-wreath', 'field office', 3463, 2600, 18, 0x232D, 'a holiday wreath', 'west', OSI, 'wallout', "outside, on the east wall (x3462), whose east face shows; P31's sign is at 3463,2597")
row('off-painting', 'field office', 3454, 2600, 18, 15462, 'a holiday painting', 'west', COM, 'wall', 'quarters, west wall (clear of the P31 bookcase 3454,2602 and scroll 3454,2598)')
row('off-shield', 'field office', 3458, 2598, 18, 15465, 'a snow-covered shield', 'west', COM, 'wall', 'office, on the inner wall x3457 (its east face)')
row('off-garland', 'field office', 3457, 2597, 18, 15457, 'a garland', 'north', COM, 'wall', 'office doorway side, north wall')

# Docks
row('dock-sleigh', 'docks', 3517, 2598, top_surface(3517, 2598, 40), 15470, 'a christmas sleigh', '-', COM, 'pier', "the pier's cargo corner by the crates at 3512,2596: a delivery")

# Outdoors, lightly: snow piles (pinned SnowPiles.cs:8, hue 0x481), snowy trees (SnowyTree.cs:9, 0x2377), snow patches
snow = [('square', 3496, 2584, 0x8E2), ('square', 3514, 2571, 15467), ('inn', 3512, 2520, 0x8E0), ('inn', 3512, 2514, 0x2377),
        ('healer hall', 3448, 2545, 15468), ('healer hall', 3445, 2560, 0x8E6), ('field office', 3465, 2598, 0x8E5),
        ('field office', 3460, 2593, 15469), ('docks', 3488, 2598, 0x8E3), ('entrance', 3423, 2524, 0x2377),
        ('entrance', 3507, 2490, 15467), ('entrance', 3473, 2632, 0x8E2)]
for k, (area, cx, cy, item) in enumerate(snow):
    c = floor(cx, cy, 4, top_surface(cx, cy, 127) or 0, False, 1)
    if not c:
        print('NO SPOT near', area, cx, cy)
        continue
    _, x, y, z = c[0]
    nm = 'a snowy tree' if item == 0x2377 else ('a snow patch' if item >= 15000 else 'a pile of snow')
    row('snow-%d' % (k + 1), area, x, y, z, item, nm, '-', COM if item >= 15000 else OSI, 'floor',
        'outdoors, off the road (the nearest free tile to %d,%d)' % (cx, cy))
json.dump(R, open('placement.json', 'w'), indent=1)
print(len(R), 'rows')
