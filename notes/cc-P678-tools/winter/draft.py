# cc-P678 WRITES placement.json: New Haven's winter rows (old-rows.json, the 109 rows P34 and P266 placed on the old
# plaza) moved into SoS Haven. Each row keeps its key, area, item, name, hue, facing and layer; its new tile is the
# nearest tile to an anchor (within a radius, optionally inside a box) that passes rules.check for the row's mode,
# with z from the mode (the walk's standing z, a table top, a lamp post's z). Anchors are picked by hand from the town
# map (view.py) per area, keeping each area's intent; the "why" says where. A row whose search finds nothing is
# reported and left out (dropped), never forced. Reads the map; writes nothing else.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rules as R

OLD = {r['key']: r for r in json.load(open(os.path.join(HERE, 'old-rows.json')))}
BANK_IN = (3616, 2610, 3629, 2621)     # the Second Bank of Haven, inside
HALL = (3624, 2528, 3638, 2534)        # the Shakin' Bakery's dining hall (two long tables), the feast
KITCHEN = (3624, 2536, 3638, 2550)     # the bakery's kitchen and shop rooms south of the hall
HEALERS = (3659, 2576, 3673, 2585)     # the Healers of Haven
OFFICE = (3659, 2548, 3673, 2561)      # the League field office (3659-3673, 2548-2561)

# key: (anchor, mode, radius, box, why). anchor is (x, y) or ('rel', key, dx, dy): next to an earlier row.
SPEC = [
    # ---------------------------------------------------------------- the square: the street north of the mansion's
    # garden (3613-3665, 2581-2590), the start 3634,2586. The tree group east of the start, as P34's stood east of the
    # plaza; the statue, firepit and snowman west of it by the Reset Stone; grass and snow beside it.
    ('sq-tree', (3642, 2584), 'square', 3, None, 'the square\'s street east of the start, clear of the lamp post 3646,2582 and the fountain'),
    ('sq-bag', ('rel', 'sq-tree', -1, 1), 'square', 1, None, 'at the tree'),
    ('sq-gift1', ('rel', 'sq-tree', 1, 1), 'square', 1, None, 'at the tree'),
    ('sq-gift2', ('rel', 'sq-tree', -1, -1), 'square', 1, None, 'at the tree'),
    ('sq-gift3', ('rel', 'sq-tree', 1, -1), 'square', 1, None, 'at the tree'),
    ('sq-gnome', ('rel', 'sq-tree', 0, 1), 'square', 1, None, 'at the foot of the square\'s tree, south'),
    ('sq-soldier', ('rel', 'sq-tree', 1, 0), 'square', 1, None, 'at the foot of the square\'s tree, east'),
    ('sq-poinsettia', ('rel', 'sq-tree', -1, 0), 'square', 1, None, 'at the foot of the square\'s tree, west'),
    ('sq-father', (3627, 2584), 'square', 3, None, 'west part of the square, north side, past Rook and the board'),
    ('sq-firepit', (3629, 2589), 'square', 2, None, 'west of the start, a few tiles from the Reset Stone (3632,2587)'),
    ('sq-snowman', (3624, 2590), 'square', 3, None, 'south-west corner of the square, by the mansion garden'),
    ('snow-1', (3630, 2592), 'floor', 4, None, 'the mansion garden\'s grass south of the square'),
    ('snow-2', (3644, 2578), 'floor', 3, None, 'the grass strip north-east of the square, between the magic shop and the main street'),
    ('sq-tree-ne-1', (3643, 2575), 'floor', 3, None, 'the grass north-east of the square, by the main street in from the north'),
    ('sq-tree-ne-2', (3644, 2580), 'floor', 3, None, 'the grass north-east of the square'),
    ('sq-snow-ne', (3643, 2577), 'floor', 3, None, 'the grass north-east of the square, between the two trees'),
    # ---------------------------------------------------------------- entrances: an arch each side of a road into town.
    # 0x3C57 (gates 1, 2, 5, 6) flank a road running east-west, 0x3C58 (3, 4, 7, 8) one running north-south, as P34's.
    ('gate-1', (3567, 2555), 'floor', 3, (3566, 2550, 3575, 2557), 'the west road where it enters the town box (x3568), north side'),
    ('gate-2', (3568, 2561), 'floor', 3, (3566, 2560, 3575, 2566), 'the west road, south side'),
    ('gate-3', (3645, 2648), 'floor', 3, (3640, 2644, 3645, 2652), 'the street down to the docks (x3646-3658), west side: the way in from the sea'),
    ('gate-4', (3659, 2648), 'floor', 3, (3659, 2644, 3662, 2652), 'the street down to the docks, east side'),
    ('gate-5', (3699, 2577), 'floor', 3, None, 'the east road out of the streets toward the farmhouse, the vet and the moongate, north side'),
    ('gate-6', (3693, 2585), 'floor', 3, None, 'the east road, south side'),
    ('gate-7', (3722, 2706), 'floor', 3, (3715, 2700, 3723, 2712), 'the south road (x3724-3728) where it leaves the town, west side'),
    ('gate-8', (3730, 2706), 'floor', 3, (3728, 2700, 3736, 2712), 'the south road, east side'),
    ('snow-10', (3566, 2553), 'floor', 4, None, 'by the west gate'),
    ('snow-11', (3642, 2646), 'floor', 4, None, 'by the docks gate'),
    ('snow-12', (3720, 2703), 'floor', 4, None, 'by the south gate'),
    # ---------------------------------------------------------------- the main road: wreaths and bells on the main
    # street's lamp posts (pinned haven.cfg items), small lit trees and snow on the grass beside it and the east road
    ('post-1', (3658, 2563), 'post', 0, None, 'lamp post 3658,2563 on the main street, by the League office'),
    ('post-2', (3658, 2568), 'post', 0, None, 'lamp post 3658,2568 on the main street'),
    ('post-3', (3657, 2545), 'post', 0, None, 'lamp post 3657,2545 on the main street'),
    ('post-4', (3646, 2582), 'post', 0, None, 'lamp post 3646,2582 where the main street meets the square'),
    ('post-5', (3646, 2534), 'post', 0, None, 'lamp post 3646,2534 on the main street, by the bakery'),
    ('post-6', (3646, 2607), 'post', 0, None, 'lamp post 3646,2607 on the main street south of the square'),
    ('post-7', (3657, 2521), 'post', 0, None, 'lamp post 3657,2521 where the main street leaves the north plaza'),
    ('post-8', (3657, 2622), 'post', 0, None, 'lamp post 3657,2622 on the main street by the smithy'),
    ('road-inn-w', (3643, 2526), 'floor', 3, None, 'the main street by the bakery (the feast), west side'),
    ('road-inn-e', (3661, 2525), 'floor', 4, None, 'the main street by the bakery, east side'),
    ('road-inn-snow', (3642, 2529), 'floor', 3, None, 'the grass west of the main street by the bakery'),
    ('road-healer', (3664, 2571), 'floor', 4, None, 'the grass by the Healers of Haven, off the main street'),
    ('road-main-w', (3643, 2560), 'floor', 3, None, 'the main street into the square, west side'),
    ('road-main-e', (3661, 2570), 'floor', 3, None, 'the main street into the square, east side'),
    ('road-main-snow-w', (3644, 2557), 'floor', 3, None, 'the grass beside the main street, west'),
    ('road-main-snow-e', (3665, 2572), 'floor', 3, None, 'the grass beside the main street, east'),
    ('road-east-n', (3692, 2572), 'floor', 3, None, 'the east road, on the grass north of it'),
    ('road-east-s', (3683, 2583), 'floor', 3, None, 'the east road, south side'),
    ('road-east-snow', (3695, 2574), 'floor', 3, None, 'the grass north of the east road'),
    # ---------------------------------------------------------------- the inn's feast: SoS Haven's inn (3664-3678,
    # 2608-2622) is bedrooms with one table, so the feast goes to the Shakin' Bakery's dining hall (3624-3638, 2528-2534:
    # two long tables, walls north and west); the stoves to the bakery's rooms south of it. The area keeps its name.
    ('inn-eggnog1', (3625, 2530), 'table', 2, HALL, 'on the west long table'),
    ('inn-cookies', (3627, 2531), 'table', 2, HALL, 'on the west long table'),
    ('inn-turkey', (3629, 2530), 'table', 2, HALL, 'on the west long table'),
    ('inn-platter', (3632, 2530), 'table', 2, HALL, 'on the east long table'),
    ('inn-canes', (3634, 2532), 'table', 2, HALL, 'on the east long table'),
    ('inn-gingerbread', (3636, 2530), 'table', 2, HALL, 'on the east long table'),
    ('inn-eggnog2', (3636, 2532), 'table', 2, HALL, 'on the east long table'),
    ('inn-advent', (3629, 2532), 'table', 2, HALL, 'on the west long table, a table end P34 left bare'),
    ('inn-fireplace', (3638, 2531), 'indoor', 2, (3638, 2528, 3638, 2534), 'its back to the hall\'s east wall (x3639), facing into the hall'),
    ('inn-stocking1', (3631, 2528), 'wall', 3, HALL, 'north wall of the hall'),
    ('inn-stocking2', (3637, 2528), 'wall', 3, HALL, 'north wall of the hall'),
    ('inn-painting', (3634, 2528), 'wall', 3, HALL, 'north wall of the hall'),
    ('inn-snowshield', (3624, 2532), 'wall', 3, HALL, 'west wall of the hall'),
    ('inn-stove1', (3629, 2544), 'indoor', 4, KITCHEN, 'the bakery\'s kitchen, by its ovens'),
    ('inn-stove2', (3626, 2550), 'indoor', 4, KITCHEN, 'the bakery\'s south room'),
    ('inn-mistletoe', (3640, 2531), 'wallout', 3, (3640, 2528, 3640, 2534), 'outside, on the hall\'s east wall (x3639), whose east face shows'),
    ('snow-3', (3642, 2531), 'floor', 4, None, 'outdoors by the hall, off the road'),
    ('snow-4', (3630, 2525), 'floor', 4, None, 'outdoors north of the hall'),
    # ---------------------------------------------------------------- the healer hall: the Healers of Haven
    ('heal-wreath', (3665, 2576), 'wall', 4, HEALERS, 'north wall'),
    ('heal-garland', (3666, 2576), 'wall', 4, HEALERS, 'north wall, the middle'),
    ('heal-shield', (3668, 2576), 'wall', 4, HEALERS, 'north wall'),
    ('heal-painting', (3659, 2580), 'wall', 4, HEALERS, 'west wall'),
    ('heal-snowpainting', (3659, 2583), 'wall', 4, HEALERS, 'west wall'),
    ('snow-5', (3676, 2578), 'floor', 4, None, 'outdoors east of the healers'),
    ('snow-6', (3671, 2588), 'floor', 4, None, 'outdoors south of the healers'),
    # ---------------------------------------------------------------- the field office: the League field office
    ('off-wreath', (3675, 2555), 'wallout', 4, (3675, 2548, 3675, 2561), 'outside, on the east wall (x3674), whose east face shows'),
    ('off-painting', (3659, 2557), 'wall', 4, OFFICE, 'west wall'),
    ('off-shield', (3659, 2552), 'wall', 4, OFFICE, 'west wall'),
    ('off-garland', (3671, 2549), 'wall', 8, OFFICE, 'north wall'),
    ('snow-7', (3677, 2552), 'floor', 4, None, 'outdoors east of the office'),
    ('snow-8', (3676, 2560), 'floor', 4, None, 'outdoors east of the office'),
    # ---------------------------------------------------------------- the docks
    ('dock-sleigh', (3670, 2659), 'pier', 4, (3645, 2657, 3672, 2684), 'the docks\' cross pier, east end: a delivery'),
    ('snow-9', (3640, 2651), 'floor', 4, None, 'the grass above the docks'),
    # ---------------------------------------------------------------- the bank: the Second Bank of Haven. Inside, the
    # tree group in the front room (3616-3622, 2610-2613) against its north wall, the calendar and garlands on its
    # walls; candles and plants clear of the tellers (3620,2617), the counter and the Rootdeep hatch (3619,2620).
    ('bank-tree', (3621, 2610), 'indoor', 2, BANK_IN, 'the front room, against its north wall; the tellers and the doors are clear'),
    ('bank-gift1', ('rel', 'bank-tree', -1, 1), 'indoor', 1, BANK_IN, 'at the tree'),
    ('bank-gift2', ('rel', 'bank-tree', 1, 1), 'indoor', 1, BANK_IN, 'at the tree'),
    ('bank-gnome', ('rel', 'bank-tree', 0, 1), 'indoor', 1, BANK_IN, 'in front of the tree'),
    ('bank-soldier', ('rel', 'bank-tree', 1, 2), 'indoor', 1, BANK_IN, 'in front of the tree'),
    ('bank-plush', ('rel', 'bank-tree', 0, 2), 'indoor', 1, BANK_IN, 'in front of the tree'),
    ('bank-calendar', (3616, 2612), 'wall', 3, BANK_IN, 'the front room\'s west wall (x3615), across from the tree: double-click to open a door'),
    ('bank-ribbon-w', (3616, 2613), 'wall', 3, BANK_IN, 'the west wall, by the calendar'),
    ('bank-ribbon-n', (3618, 2610), 'wall', 3, BANK_IN, 'the front room\'s north wall (y2609)'),
    ('bank-candle-tall', (3622, 2613), 'indoor', 1, BANK_IN, 'the front room\'s south-east corner, by the tree group, clear of the tellers\' aisle (x3616-3618)'),
    ('bank-antler', (3625, 2615), 'indoor', 3, BANK_IN, 'the hall\'s north-east corner, off the tellers\' line'),
    ('bank-potted', (3625, 2618), 'indoor', 3, BANK_IN, 'the hall\'s east side, by the vault door'),
    ('bank-poinsettia-1', (3616, 2615), 'indoor', 3, BANK_IN, 'the hall\'s north-west corner'),
    ('bank-poinsettia-2', (3625, 2621), 'indoor', 3, BANK_IN, 'the hall\'s south-east corner'),
    ('bank-candle-short-1', (3616, 2617), 'indoor', 3, BANK_IN, 'the hall\'s west side'),
    ('bank-candle-short-2', (3624, 2619), 'indoor', 3, BANK_IN, 'the hall\'s east side'),
    ('bank-out-tree-n', (3618, 2608), 'wallfoot', 3, None, 'outside, at the foot of the north face'),
    ('bank-out-tree-s', (3622, 2623), 'wallfoot', 3, None, 'outside, at the foot of the south face'),
    ('bank-out-tree-sw', (3614, 2620), 'wallfoot', 3, None, 'outside, at the foot of the west face, south end'),
    ('bank-out-tree-se', (3614, 2612), 'wallfoot', 3, None, 'outside, at the foot of the west face, north end'),
    ('bank-wreath-n', (3624, 2610), 'wallout', 3, (3624, 2609, 3624, 2614), 'outside, on the front room\'s east face (x3623), north of its way in'),
    ('bank-wreath-s', (3624, 2613), 'wallout', 3, (3624, 2609, 3624, 2614), 'outside, on the front room\'s east face, south of its way in'),
    ('bank-snow-1', (3612, 2627), 'floor', 4, None, 'the grass south of the bank'),
    ('bank-snow-2', (3616, 2628), 'floor', 4, None, 'the grass south of the bank'),
    ('bank-snow-3', (3620, 2628), 'floor', 4, None, 'the grass south of the bank'),
    ('bank-snow-4', (3626, 2628), 'floor', 4, None, 'the grass south of the bank'),
    ('bank-snow-5', (3630, 2629), 'floor', 4, None, 'the grass south of the bank'),
    ('bank-snow-6', (3610, 2622), 'floor', 4, None, 'the grass south-west of the bank'),
    ('bank-snow-7', (3623, 2630), 'floor', 4, None, 'the grass south of the bank'),
    ('bank-snow-8', (3633, 2630), 'floor', 4, None, 'the grass south-east of the bank'),
]


def main():
    assert sorted(k for k, *_ in SPEC) == sorted(OLD), set(OLD) ^ {k for k, *_ in SPEC}
    order = [r['key'] for r in json.load(open(os.path.join(HERE, 'old-rows.json')))]
    placed, taken, dropped, log = {}, {}, [], []
    for key, anchor, mode, rad, box, why in SPEC:
        o = OLD[key]
        if anchor[0] == 'rel':
            if anchor[1] not in placed:
                dropped.append((key, 'its anchor row %s was dropped' % anchor[1])); continue
            a = placed[anchor[1]]
            ax, ay = a['x'] + anchor[2], a['y'] + anchor[3]
        else:
            ax, ay = anchor
        cands = sorted(((x, y) for x in range(ax - rad, ax + rad + 1) for y in range(ay - rad, ay + rad + 1)
                        if not box or (box[0] <= x <= box[2] and box[1] <= y <= box[3])),
                       key=lambda p: ((p[0] - ax) ** 2 + (p[1] - ay) ** 2, p[1], p[0]))
        got, first = None, None
        for (x, y) in cands:
            z = R.zfor(mode, x, y)
            if z is None: continue
            r = dict(o, x=x, y=y, z=z, mode=mode, map='Trammel', why=why, oldx=o['x'], oldy=o['y'], oldz=o['z'])
            errs = R.check(r, taken)
            if not errs:
                got = r; break
            if first is None: first = '%d,%d: %s' % (x, y, ' / '.join(errs))
        if got is None:
            dropped.append((key, 'nothing within %d of %d,%d passes (nearest tried %s)' % (rad, ax, ay, first))); continue
        if (got['x'], got['y']) != (ax, ay): log.append('%s: anchor %d,%d -> %d,%d' % (key, ax, ay, got['x'], got['y']))
        placed[key] = got
        taken[(got['x'], got['y'])] = key
    rows = [placed[k] for k in order if k in placed]
    json.dump(rows, open(os.path.join(HERE, 'placement.json'), 'w', encoding='ascii'), indent=1)
    out = ['wrote %d rows, dropped %d' % (len(rows), len(dropped))] + ['moved off its anchor: ' + l for l in log] + \
          ['DROPPED %s: %s' % d for d in dropped]
    print('\n'.join(out))
    open(os.path.join(HERE, 'draft.out.txt'), 'w', encoding='ascii', newline='\n').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()
