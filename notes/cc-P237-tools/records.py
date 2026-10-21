# cc-P237: this set's tiledata and animdata records, and where each value comes from (OSI's tiledata.mul, read
# 2026-10-21 through nhbase/uofiles). WRITES records.json's new entries with --write (once); prints otherwise.
# The server carries the same table (ClusterFCommunityArtRecords.Records in ClusterFCommunityArtSeeder.cs); the
# package fact compares the two.
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art_src as S
REC = 'D:/UO/golems/Bronze/ShatteredLegacy/player-package/vendor/shattered-legacy-art/records.json'
# UNKNOWN3 is bit 0x04000000, which pinned names TileFlag.Unknown3 (Server/TileData.cs); OSI sets it on these pieces
IMP, WALL, TRANSP, NOSHOOT, ART_A, ART_AN, LIGHT, ANIM, UNKNOWN3 = 0x40, 0x10, 0x4, 0x2000, 0x4000, 0x8000, 0x800000, 0x1000000, 0x4000000
# key: (name, flags, weight, layer (the light shape for a light source), height, from)
TABLE = {
    'cart-fruit-a': ('fruit cart', IMP | ART_A, 255, 0, 3, "OSI's ore cart 0x1A82 (Impassable, height 3), ArticleA for 'a fruit cart'"),
    'cart-fruit-b': ('fruit cart', IMP | ART_A, 255, 0, 3, 'as the other facing'),
    'cart-veg-a': ('vegetable cart', IMP | ART_A, 255, 0, 3, "OSI's ore cart 0x1A82"),
    'cart-veg-b': ('vegetable cart', IMP | ART_A, 255, 0, 3, 'as the other facing'),
    'lantern': ('oil lantern', ANIM | LIGHT | ART_AN, 255, 2, 2, "OSI's lantern 0x0A15 (Animation | LightSource, light 2, height 2) without Wearable; ArticleAn"),
    'rail-y': ('marble railing', IMP | TRANSP | ART_A, 255, 0, 5, "OSI's wooden banister 0x08AE (Impassable | Transparent | ArticleA, height 5)"),
    'rail-y-post': ('marble railing', IMP | TRANSP | ART_A, 255, 0, 5, "OSI's wooden banister 0x08AE"),
    'beam-ew-left': ('support beam', IMP | WALL | UNKNOWN3, 255, 0, 16, "OSI's wood supports 0x019C (Impassable | Wall | Unknown3, height 16)"),
    'beam-ew-right': ('support beam', IMP | WALL | UNKNOWN3, 255, 0, 16, "OSI's wood supports 0x019C"),
    'beam-ns-left': ('support beam', IMP | WALL | UNKNOWN3, 255, 0, 16, "OSI's wood supports 0x019C"),
    'beam-ns-right': ('support beam', IMP | WALL | UNKNOWN3, 255, 0, 16, "OSI's wood supports 0x019C"),
    'orc-cage': ('orcish cage', IMP | ART_AN, 255, 0, 20, 'ours: Impassable, the height of a tent wall (OSI 0x01F0, 20)'),
    'orc-fire': ('orcish campfire', LIGHT | ART_AN, 255, 29, 1, "OSI's campfire 0x0DE3 (LightSource, light 29, height 1, walk-through) without Animation (one frame) and Damaging"),
    'orc-meat': ('orcish meat rack', IMP | ART_AN, 255, 0, 15, "ours: Impassable, as OSI's chicken on a spit 0x1E94, taller (15)"),
    'orc-palisade-1': ('orcish palisade', IMP | WALL | NOSHOOT | ART_AN | UNKNOWN3, 255, 0, 20, "OSI's palisade 0x0221 (Impassable | Wall | NoShoot | Unknown3, height 20) without Damaging; ArticleAn"),
    'orc-palisade-2': ('orcish palisade', IMP | WALL | NOSHOOT | ART_AN | UNKNOWN3, 255, 0, 20, "OSI's palisade 0x0221"),
    'orc-tent-1': ('orcish tent', IMP | WALL | NOSHOOT | ART_AN, 255, 0, 20, "OSI's tent wall 0x01F0 (Impassable | Wall | NoShoot, height 20); ArticleAn"),
    'orc-tent-2': ('orcish tent', IMP | WALL | NOSHOOT | ART_AN, 255, 0, 20, "OSI's tent wall 0x01F0"),
    'orc-tent-3': ('orcish hut', IMP | WALL | NOSHOOT | ART_AN, 255, 0, 20, "OSI's tent wall 0x01F0"),
}
# OSI's lantern 0x0A15 animdata: 8 steps over its three lit frames, interval 6. The pack gives no timing of its own.
ANIMS = {'lantern': ([0, 1, 2, 1, 0, 0, 1, 0], 6, 0)}


def tiledata():
    out = []
    for first, key, what, pack, files, how in S.GROUPS:
        if key in TABLE:
            n, f, w, l, h, why = TABLE[key]
            assert len(n) <= 19
            out.append({'id': first, 'name': n, 'flags': '0x%08X' % f, 'weight': w, 'layer': l, 'count': 0, 'animId': 0,
                        'hue': 0, 'light': 0, 'height': h})
    return out


def animdata():
    return [{'id': S.ID[k], 'frames': fr, 'interval': iv, 'start': st} for k, (fr, iv, st) in ANIMS.items()]


def line(d):
    return '    ' + json.dumps(d, separators=(', ', ': ')).replace('{', '{ ', 1)[:-1] + ' }'


if __name__ == '__main__':
    t, a = tiledata(), animdata()
    for d in t + a: print(line(d))
    if '--write' not in sys.argv: raise SystemExit(0)
    text = open(REC, encoding='utf-8').read()
    if '"id": %d' % S.FIRST in text: raise SystemExit('already written')
    # append after the last tiledata entry and the last animdata entry, keeping the file's one-record-a-line layout
    ti = text.index('  "animdata": [')
    head, tail = text[:ti], text[ti:]
    k = head.rstrip().rfind('}')
    head = head[:k + 1] + ',\n' + ',\n'.join(line(d) for d in t) + head[k + 1:]
    ai = tail.index('  "equipAnims": [')
    mid, rest = tail[:ai], tail[ai:]
    k = mid.rstrip().rfind('}')
    mid = mid[:k + 1] + ',\n' + ',\n'.join(line(d) for d in a) + mid[k + 1:]
    new = head + mid + rest
    json.loads(new)
    open(REC, 'w', encoding='utf-8', newline='\n').write(new)
    print('wrote', len(t), 'tiledata and', len(a), 'animdata records')
