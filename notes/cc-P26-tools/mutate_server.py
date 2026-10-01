# cc-P26: red run for server/tests/Items/ShatteredRunestoneVerification.cs. Applies every break, or restores.
#     python mutate_server.py apply      (writes backups beside this script, records SHA-256)
#     python mutate_server.py apply 2 5  (only breaks r2 and r5: red run 2, for what r1 masked)
#     python mutate_server.py restore    (puts the files back and checks SHA-256)
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
R = r'D:\ShatteredLegacy\server\customizations\ShatteredRunestone.cs'
S = r'D:\ShatteredLegacy\server\customizations\ClusterFResetStone.cs'

BREAKS = [
    # r1 (fact 1 and 2): design 2 one ID off
    (R, '{ 0x3C10, 0x3C1B, 0x3C26, 0x3C31 }', '{ 0x3C10, 0x3C1C, 0x3C26, 0x3C31 }'),
    # r2 (fact 2): the setter takes any number
    (R, '                var itemId = ItemIdOf(value); // throws for anything but 1 to 4: [props then says it was not set\n                _design = value;\n                ItemID = itemId;',
        '                _design = value;\n                ItemID = value is >= 1 and <= 4 ? DesignItemIds[value - 1] : ItemID;'),
    # r3 (fact 3): the server keeps EA's UNUSED tiledata
    (R, '        public static void Configure() => Apply();\n\n        public static void Apply()\n        {',
        '        public static void Configure() => Apply();\n\n        public static void Apply()\n        {\n            return;'),
    # r4 (fact 4): an old Reset Stone keeps its old look
    (S, '            ItemID = StoneGraphic;\n            Hue = StoneHue;\n        }', '        }'),
    # r5 (fact 1, hand-set ItemID): not put back at load
    (R, '            ItemID = DesignItemIds[_design - 1];\n        }\n    }\n}', '        }\n    }\n}'),
]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    man = os.path.join(HERE, 'mutate_server.manifest.json')
    if sys.argv[1] == 'apply':
        m = {}
        for p in {b[0] for b in BREAKS}:
            m[p] = sha(p)
            open(os.path.join(HERE, os.path.basename(p) + '.bak'), 'wb').write(open(p, 'rb').read())
        pick = [int(x) for x in sys.argv[2:]] or list(range(1, len(BREAKS) + 1))
        for n, (p, old, new) in enumerate(BREAKS, 1):
            if n not in pick:
                continue
            s = open(p, encoding='ascii').read()
            assert s.count(old) == 1, (p, old)
            open(p, 'w', encoding='ascii', newline='\n').write(s.replace(old, new))
        json.dump(m, open(man, 'w'))
        print('applied breaks %s' % pick)
    else:
        m = json.load(open(man))
        for p, h in m.items():
            b = os.path.join(HERE, os.path.basename(p) + '.bak')
            open(p, 'wb').write(open(b, 'rb').read())
            assert sha(p) == h, p
            os.remove(b)
        os.remove(man)
        print('restored, byte-identical: ' + ', '.join('%s %s' % (os.path.basename(p), h[:12]) for p, h in m.items()))


if __name__ == '__main__':
    main()
