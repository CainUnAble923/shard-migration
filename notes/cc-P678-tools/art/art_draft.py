# cc-P678 WRITES art/placement.json: cc-P237's community art rows moved onto SoS Haven (the author's town on the Siege
# of Sosaria map), each area kept to its design (cc-P237-tools/draft.py) and its keys. z is the tile's top surface
# (pinned GetTopSurfaceZ, sosbase.SosFacet) unless the row gives one. art_validate.py checks every row.
# Dropped (see DROPPED): the eight bridge support beams. SoS's docks are one level, decks (z-3) over the water; no
# tile has a dry floor with a plank deck 10-20 above it (one dry tile does, 3652,2658, under the deck at the seabed's
# z-15, out of sight), so there is no overhang for a brace to hold up.
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'cc-P237-tools'))
import sosbase as B
import art_src as S
F = B.sos()

NAMES = {
    'cart-fruit-a': 'a fruit cart', 'cart-fruit-b': 'a fruit cart', 'cart-veg-a': 'a vegetable cart',
    'cart-veg-b': 'a vegetable cart', 'lantern': 'an oil lantern',
    'rail-y': 'a marble railing', 'rail-y-post': 'a marble railing',
    'orc-cage': 'an orcish cage', 'orc-fire': 'an orcish campfire', 'orc-meat': 'an orcish meat rack',
    'orc-palisade-1': 'an orcish palisade', 'orc-palisade-2': 'an orcish palisade', 'orc-rug': 'an orcish hide rug',
    'orc-tent-1': 'an orcish tent', 'orc-tent-2': 'an orcish tent', 'orc-tent-3': 'an orcish hut',
    'ptg-beata': 'Beata Beatrix', 'ptg-morgan': 'Morgan le Fay', 'ptg-ophelia': 'Ophelia',
    'ptg-galahad': 'Sir Galahad at the Ruined Chapel', 'ptg-feller': "The Fairy Feller's Master-Stroke",
    'ptg-hesperides': 'The Garden of the Hesperides', 'ptg-shalott': 'The Lady of Shalott',
    'ptg-lovesong': 'The Love Song', 'ptg-towers': 'The Tune of the Seven Towers', 'ptg-roses': 'Wars of the Roses',
    'ptg-nightmare': 'The Nightmare', 'ptg-circle': 'The Magic Circle',
}

# (key, area, art key, x, y, floor z or None for the ground, mode, why)
ROWS = [
    # ---- the orc camp: the forest just west of town, west of Uzeraan's Mansion, south of the west road (P237's camp
    # kept its shape: every piece at the same offset from the fire)
    ('camp-hut', 'camp', 'orc-tent-3', 3546, 2570, None, 'camp', "the round hut, the camp's north-west"),
    ('camp-tent-long', 'camp', 'orc-tent-1', 3556, 2569, None, 'camp', 'the long tent, north-east, its back to the trees'),
    ('camp-tent-square', 'camp', 'orc-tent-2', 3553, 2579, None, 'camp', 'the square tent, south'),
    ('camp-fire', 'camp', 'orc-fire', 3556, 2577, None, 'camp', 'the campfire between the three tents'),
    ('camp-rug', 'camp', 'orc-rug', 3554, 2578, None, 'camp', 'a hide rug by the fire'),
    ('camp-meat', 'camp', 'orc-meat', 3558, 2576, None, 'camp', 'the meat rack by the fire'),
    ('camp-cage', 'camp', 'orc-cage', 3560, 2581, None, 'camp', "the cage, at the camp's east edge"),
    ('camp-palisade-w', 'camp', 'orc-palisade-1', 3544, 2576, None, 'camp', "palisade, the camp's west side"),
    ('camp-palisade-e', 'camp', 'orc-palisade-2', 3562, 2575, None, 'camp', 'palisade, the side facing the town'),
    # ---- carts: the square (its cobbles are all road; on the grass at its edges)
    ('market-fruit', 'market', 'cart-fruit-a', 3661, 2592, None, 'ground', "fruit cart on the square's east side, by the provisioner"),
    ('market-veg', 'market', 'cart-veg-a', 3636, 2599, None, 'ground', "vegetable cart in the garden on the square's south side, toward the docks"),
    # ---- carts: the east fields (the furrows at 3703-3720, 2608-2640)
    ('field-veg', 'field', 'cart-veg-b', 3701, 2614, None, 'ground', "vegetable cart on the grass at the east fields' west edge"),
    ('field-fruit', 'field', 'cart-fruit-b', 3706, 2635, None, 'ground', 'fruit cart between the fields and the farm track'),
    # ---- lanterns: on top of the docks' pier posts, and beside the main road north of the square
    ('dock-lantern-w', 'docks', 'lantern', 3644, 2674, 5, 'posttop', "on the west finger pier's post"),
    ('dock-lantern-m', 'docks', 'lantern', 3659, 2684, 5, 'posttop', "on the east finger pier's end post"),
    ('dock-lantern-e', 'docks', 'lantern', 3671, 2666, 5, 'posttop', "on the main pier's east post"),
    ('road-lantern-1', 'road', 'lantern', 3644, 2560, None, 'ground', 'beside the main road north of the square'),
    ('road-lantern-2', 'road', 'lantern', 3644, 2549, None, 'ground', "beside the main road by the Shakin' Bakery"),
    ('road-lantern-3', 'road', 'lantern', 3644, 2524, None, 'ground', 'beside the main road below the carpenters'),
    # ---- marble railings: the hall's (League office's) door, and the Healers of Haven
    ('office-rail-post', 'office', 'rail-y-post', 3671, 2563, None, 'edge', "by the hall's south door, east side, its post nearest the door"),
    ('office-rail', 'office', 'rail-y', 3671, 2564, None, 'edge', 'the railing runs on south from the post'),
    ('healer-rail-1', 'healer', 'rail-y', 3670, 2579, 0, 'indoor', "railing across the healers' hall, closing off its east bay"),
    ('healer-rail-2', 'healer', 'rail-y', 3670, 2580, 0, 'indoor', "railing across the healers' hall"),
    ('healer-rail-3', 'healer', 'rail-y-post', 3670, 2581, 0, 'indoor', 'its end post (the bay stays open at 3670,2582)'),
    # ---- paintings (north walls only: they face south, the face the client draws)
    ('inn-ptg-1', 'inn', 'ptg-ophelia', 3667, 2608, 0, 'wall', "the Haven inn, the west room's north wall"),
    ('inn-ptg-2', 'inn', 'ptg-shalott', 3671, 2608, 0, 'wall', "the Haven inn, the middle room's north wall"),
    ('inn-ptg-3', 'inn', 'ptg-lovesong', 3677, 2608, 0, 'wall', "the Haven inn, the east room's north wall"),
    ('office-ptg-1', 'office', 'ptg-galahad', 3664, 2548, 0, 'wall', "the hall (League office), the north wall by the Registrar's corner"),
    ('office-ptg-2', 'office', 'ptg-roses', 3673, 2548, 0, 'wall', "the hall (League office), the north wall's east end"),
    ('healer-ptg-1', 'healer', 'ptg-beata', 3663, 2575, 0, 'wall', "Healers of Haven, a north alcove"),
    ('healer-ptg-2', 'healer', 'ptg-hesperides', 3668, 2575, 0, 'wall', "Healers of Haven, a north alcove"),
    ('mage-ptg-1', 'mage', 'ptg-circle', 3648, 2464, 0, 'wall', "Haven Magery School, the east hall's north wall"),
    ('mage-ptg-2', 'mage', 'ptg-nightmare', 3652, 2464, 0, 'wall', "Haven Magery School, the east hall's north wall"),
    ('bard-ptg-1', 'bard', 'ptg-feller', 3672, 2528, 0, 'wall', "the Bardic Guild, the east wing's north wall"),
    ('bard-ptg-2', 'bard', 'ptg-towers', 3677, 2528, 0, 'wall', "the Bardic Guild, the east wing's north wall"),
    ('tailor-ptg', 'tailor', 'ptg-morgan', 3687, 2472, 0, 'wall', "A Stitch in Time, the shop's north wall"),
]

DROPPED = [
    ('beam-s-1', 'beam-s-2', 'beam-s-3', 'beam-s-4', 'beam-e-1', 'beam-e-2', 'beam-e-3', 'beam-e-4'),
    "SoS's docks are one level (plank decks at z-3 over the water): no dry floor with a deck 10-20 above it in sight",
]


def build():
    out = []
    for key, area, art, x, y, fz, mode, why in ROWS:
        z = fz if mode in ('posttop', 'wall') else F.top_surface(x, y, (F.avgz(x, y) if fz is None else fz) + 2)
        out.append({'key': key, 'area': area, 'x': x, 'y': y, 'z': z, 'map': 'Trammel', 'art': art,
                    'itemId': S.ID[art], 'name': NAMES[art], 'mode': mode, 'why': why})
    return out


if __name__ == '__main__':
    rows = build()
    json.dump(rows, open(os.path.join(HERE, 'placement.json'), 'w'), indent=1)
    print('wrote', len(rows), 'rows; dropped', len(DROPPED[0]))
