# cc-P266: this set's tiledata and animdata records, and where each value comes from (OSI's tiledata.mul and
# animdata.mul in the client copy, read 2026-10-21 through nhbase/uofiles). WRITES records.json's new entries with
# --write (once); prints otherwise. The server carries the same table (ClusterFWinterDecorArt.Records in
# ClusterFWinterDecorSeeder.cs); the package fact compares the two.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art_src as S
REC = 'D:/UO/golems/Bronze/ShatteredLegacy/player-package/vendor/shattered-legacy-art/records.json'
BG, IMP, ART_A, ART_AN, LIGHT, ANIM, UNKNOWN3 = 0x1, 0x40, 0x4000, 0x8000, 0x800000, 0x1000000, 0x4000000
# key: (name, flags, weight, light shape (the tiledata quality byte, what pinned reads as the light), height, from)
TABLE = {
    'tree-large': ('christmas tree', ANIM | ART_A | IMP | BG, 255, 0, 20, "OSI's tree 0x0CCA (Background | ArticleA | Impassable, height 20), Animation added: the lights twinkle"),
    'tree-small': ('christmas tree', ANIM | ART_A | IMP | BG, 255, 0, 10, "OSI's tree 0x0CCA for the flags, Animation added; height 10 as OSI's small banana tree 0x0CAB"),
    'candle-tall': ('candle stand', ANIM | LIGHT | ART_A | IMP | UNKNOWN3, 255, 29, 15, "OSI's tall candelabra 0x0B26 (Animation | LightSource | ArticleA | Impassable | Unknown3, light 29, height 15)"),
    'candle-short': ('candle', ANIM | LIGHT | ART_A, 255, 2, 1, "OSI's lit candle 0x0B1A (Animation | LightSource | ArticleA, light 2, height 1): walk-over, as OSI's floor candles are"),
    'antler': ('antler candelabra', ANIM | LIGHT | ART_AN | IMP, 255, 1, 5, "OSI's candelabra 0x0B1D (Animation | LightSource | ArticleA | Impassable, light 1, height 5); ArticleAn for 'an antler candelabra'"),
    'advent': ('advent candles', ANIM | LIGHT | ART_A, 255, 2, 3, "OSI's holiday candle 0x236E (Animation | LightSource | PartialHue | ArticleA, light 2, height 3) without PartialHue (nothing hues it)"),
    'potted': ('potted tree', ART_A | IMP, 255, 0, 5, "OSI's potted tree 0x11C8 (ArticleA | Impassable, height 5)"),
}
# Animdata: OSI's lit candle 0x0B1A, candelabra 0x0B1D / 0x0B26 and holiday candle 0x236E all run their frames at
# interval 3 (about 300 ms a frame); the trees' twinkling lights take the same, the pack gives no timing of its own.
# The antler candelabra's four files are four frames in a row (OSI's 0x0B1D plays 0,1,2,1 over three frames).
ANIMS = {
    'tree-large': (list(range(11)), 3, 0),
    'tree-small': (list(range(11)), 3, 0),
    'candle-tall': ([0, 1, 2, 3], 3, 0),
    'candle-short': ([0, 1, 2, 3], 3, 0),
    'antler': ([0, 1, 2, 3], 3, 0),
    'advent': ([0, 1, 2, 3], 3, 0),
}


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
