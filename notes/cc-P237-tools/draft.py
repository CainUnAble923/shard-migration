# cc-P237 WRITES placement.json: the proposed rows (key, area, x, y, z, item, name, mode, why). z is the tile's
# top surface at or below the given floor (pinned GetTopSurfaceZ) unless the row gives one. validate.py checks it.
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nhbase as B
import art_src as S
F = B.Facet(1)

NAMES = {
    'cart-fruit-a': 'a fruit cart', 'cart-fruit-b': 'a fruit cart', 'cart-veg-a': 'a vegetable cart',
    'cart-veg-b': 'a vegetable cart', 'lantern': 'an oil lantern',
    'rail-y': 'a marble railing', 'rail-x': 'a marble railing', 'rail-y-post': 'a marble railing',
    'rail-x-post': 'a marble railing', 'rail-post': 'a marble post',
    'beam-ew-bottom': 'a support beam', 'beam-ew-left': 'a support beam', 'beam-ew-right': 'a support beam',
    'beam-ns-bottom': 'a support beam', 'beam-ns-left': 'a support beam', 'beam-ns-right': 'a support beam',
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
    # ---- the orc camp: the meadow west of P188's walk to the Rootdeep hole
    ('camp-hut', 'camp', 'orc-tent-3', 3591, 2615, None, 'camp', "the round hut, the camp's north-west"),
    ('camp-tent-long', 'camp', 'orc-tent-1', 3601, 2614, None, 'camp', 'the long tent, north-east, its back to the old wall'),
    ('camp-tent-square', 'camp', 'orc-tent-2', 3598, 2624, None, 'camp', 'the square tent, south'),
    ('camp-fire', 'camp', 'orc-fire', 3601, 2622, None, 'camp', 'the campfire between the three tents'),
    ('camp-rug', 'camp', 'orc-rug', 3599, 2623, None, 'camp', 'a hide rug by the fire'),
    ('camp-meat', 'camp', 'orc-meat', 3603, 2621, None, 'camp', 'the meat rack by the fire'),
    ('camp-cage', 'camp', 'orc-cage', 3605, 2626, None, 'camp', "the cage, at the camp's east edge"),
    ('camp-palisade-w', 'camp', 'orc-palisade-1', 3589, 2621, None, 'camp', "palisade, the camp's west side"),
    ('camp-palisade-e', 'camp', 'orc-palisade-2', 3607, 2620, None, 'camp', 'palisade, the side facing the walk'),
    # ---- carts: the market square (the plaza is all road; off the plaza's walkway, clear of the board and lamps)
    ('market-fruit', 'market', 'cart-fruit-a', 3512, 2574, None, 'ground', "fruit cart on the square's east side"),
    ('market-veg', 'market', 'cart-veg-a', 3506, 2581, None, 'ground', "vegetable cart on the square's south side, toward the docks"),
    # ---- carts: the west fields (New Haven has no farm buildings; the hay meadows west of the Healer's Hall)
    ('field-veg', 'field', 'cart-veg-b', 3450, 2584, None, 'ground', 'vegetable cart in the west meadow by the hay'),
    ('field-fruit', 'field', 'cart-fruit-b', 3452, 2588, None, 'ground', 'fruit cart in the west meadow, by the path down to the office'),
    # ---- lanterns: on top of the docks' mooring posts, and beside the main road north of the square
    ('dock-lantern-w', 'docks', 'lantern', 3500, 2604, 8, 'posttop', "on the west finger pier's mooring post"),
    ('dock-lantern-m', 'docks', 'lantern', 3507, 2610, 7, 'posttop', "on the middle finger pier's mooring post"),
    ('dock-lantern-e', 'docks', 'lantern', 3523, 2601, 6, 'posttop', "on the east pier's mooring post"),
    ('road-lantern-1', 'road', 'lantern', 3509, 2561, None, 'ground', 'beside the main road north of the square'),
    ('road-lantern-2', 'road', 'lantern', 3514, 2549, None, 'ground', "beside the main road by the Warriors' yard"),
    ('road-lantern-3', 'road', 'lantern', 3506, 2535, None, 'ground', 'beside the main road below the inn'),
    # ---- marble railings: the field office's entrance steps, and the Healer's Hall upper room
    ('office-rail-post', 'office', 'rail-y-post', 3460, 2594, None, 'edge', "by the office door's steps, east side, its post nearest the door (3460,2595 is kept clear: P19's old sign stood there)"),
    ('office-rail', 'office', 'rail-y', 3460, 2593, None, 'edge', 'the railing runs on north from the post'),
    ('healer-rail-1', 'healer', 'rail-y', 3456, 2550, 35, 'indoor', "railing across the hall's upper room"),
    ('healer-rail-2', 'healer', 'rail-y', 3456, 2551, 35, 'indoor', "railing across the hall's upper room"),
    ('healer-rail-3', 'healer', 'rail-y-post', 3456, 2552, 35, 'indoor', 'its end post'),
    # ---- bridge support beams: braces under the raised boardwalk (z15) where it overhangs the lower pier, on its south
    # face (y 2591, the bays between its posts that hold no crates or barrels) and its east face (x 3519)
    ('beam-s-1', 'docks', 'beam-ew-left', 3501, 2591, 0, 'beam', 'south face, the bay west of the water tub'),
    ('beam-s-2', 'docks', 'beam-ew-right', 3502, 2591, 0, 'beam', 'south face, the same bay'),
    ('beam-s-3', 'docks', 'beam-ew-left', 3510, 2591, 0, 'beam', 'south face, the bay by the lantern post'),
    ('beam-s-4', 'docks', 'beam-ew-right', 3511, 2591, 0, 'beam', 'south face, the same bay'),
    ('beam-e-1', 'docks', 'beam-ns-left', 3519, 2582, 0, 'beam', 'east face, the north bay'),
    ('beam-e-2', 'docks', 'beam-ns-right', 3519, 2583, 0, 'beam', 'east face, the north bay'),
    ('beam-e-3', 'docks', 'beam-ns-left', 3519, 2585, 0, 'beam', 'east face, the south bay'),
    ('beam-e-4', 'docks', 'beam-ns-right', 3519, 2586, 0, 'beam', 'east face, the south bay'),
    # ---- paintings (north walls only: they face south, the face the client draws)
    ('inn-ptg-1', 'inn', 'ptg-ophelia', 3495, 2513, 27, 'wall', "inn, the west room's north wall"),
    ('inn-ptg-2', 'inn', 'ptg-shalott', 3499, 2513, 27, 'wall', "inn, the common room's north wall"),
    ('inn-ptg-3', 'inn', 'ptg-lovesong', 3507, 2513, 27, 'wall', "inn, the east room's north wall"),
    ('office-ptg-1', 'office', 'ptg-galahad', 3454, 2597, 18, 'wall', "field office, the Registrar's quarters, over the bed"),
    ('office-ptg-2', 'office', 'ptg-roses', 3455, 2597, 18, 'wall', "field office, the Registrar's quarters, over the bed"),
    ('healer-ptg-1', 'healer', 'ptg-beata', 3454, 2547, 35, 'wall', "Healer's Hall, the upper room's north wall"),
    ('healer-ptg-2', 'healer', 'ptg-hesperides', 3460, 2547, 35, 'wall', "Healer's Hall, the upper room's north wall"),
    ('mage-ptg-1', 'mage', 'ptg-circle', 3466, 2500, 51, 'wall', "Magery School, the long hall's north wall"),
    ('mage-ptg-2', 'mage', 'ptg-nightmare', 3486, 2488, 51, 'wall', "Magery School, the north library, between two bookcases"),
    ('bard-ptg-1', 'bard', 'ptg-feller', 3415, 2598, 55, 'wall', "Bardic Guild, the hall's north wall"),
    ('bard-ptg-2', 'bard', 'ptg-towers', 3417, 2598, 55, 'wall', "Bardic Guild, the hall's north wall"),
    ('tailor-ptg', 'tailor', 'ptg-morgan', 3500, 2550, 20, 'wall', "A Stitch In Time, the shop's north wall"),
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
    print('wrote', len(rows), 'rows')
