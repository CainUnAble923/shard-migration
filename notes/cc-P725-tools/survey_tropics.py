"""cc-P725: what OSI plants in its tropical places, counted from stock Trammel statics: Buccaneer's Den's island
(x 2560-2800, y 2000-2300) and the jungle south of Trinsic... any rect given. Prints each plant-like id (Foliage flag,
or a plant name) with its count, name, height and the ids that stand on the same tile with it (a tree's leaves).
    python -P survey_tropics.py <client folder> name=x1,y1,x2,y2 ..."""
import collections, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
from mapbuild import uofiles as U

FOLIAGE = 1 << 17
NAMES = re.compile(r'palm|banana|jungle|fern|tree|leaves|bush|plant|grass|flower|o.hii|poppies|vine|reed|yucca|weed|cattail', re.I)
folder = sys.argv[1]
items = U.read_tiledata(folder)[1]
for spec in sys.argv[2:]:
    name, r = spec.split('=')
    x1, y1, x2, y2 = (int(v) for v in r.split(','))
    st = U.statics_in(folder, 1, x1, y1, x2, y2)
    by_tile = collections.defaultdict(list)
    for (x, y, z, t) in st:
        by_tile[(x, y)].append(t)
    cnt = collections.Counter(t for (x, y, z, t) in st if items[t]['flags'] & FOLIAGE or NAMES.search(items[t]['name']))
    mates = collections.defaultdict(collections.Counter)
    for c, ts in by_tile.items():
        for t in ts:
            for u in ts:
                if u != t:
                    mates[t][u] += 1
    land = sum(1 for _ in range((x2 - x1 + 1) * (y2 - y1 + 1)))
    print('==', name, (x1, y1, x2, y2), 'tiles', land, 'plant pieces', sum(cnt.values()))
    for t, n in cnt.most_common(45):
        print('  0x%04X %-18s %5d h%-3d with %s' % (t, items[t]['name'], n, items[t]['height'],
              ' '.join('0x%04X:%d' % kv for kv in mates[t].most_common(2))))
