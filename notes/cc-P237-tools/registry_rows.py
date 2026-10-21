# cc-P237 WRITES: appends this set's rows to registry.csv (once; refuses if any of the IDs is there). One row per ID,
# written before any PNG is made (P26's rule). The license column carries each folder's credit rule from its SOURCE.txt.
import csv, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art_src as S
REG = 'D:/UO/golems/Bronze/ShatteredLegacy/player-package/vendor/shattered-legacy-art/registry.csv'
PACK = {
    'farm-carts': ('Moonrose "Farm carts" (servuo.dev; downloaded 2026-09-30, FarmCartGraphics.zip)',
                   'none stated (the folder has no SOURCE.txt; D:\\UO\\third-party\\README.md: Moonrose, none stated); community work: credit Moonrose, ship only inside the player package'),
    'oil-lantern': ('Ems "Oil lantern" (servuo.dev 2592)',
                    'none stated; see SOURCE.txt; community work: credit Ems, ship only inside the player package'),
    'marble-railings': ('OUTLANDSOwyn "Marble Railings, Bannisters, Ladder" (servuo.dev 2663)',
                        'none stated; see SOURCE.txt; community work: credit OUTLANDSOwyn, ship only inside the player package'),
    'bridge-support-beam': ('gollin "Bridge support beam 1.0" (servuo.dev 2396)',
                            'none stated; see SOURCE.txt; community work: credit gollin, ship only inside the player package'),
    'orc-encampment': ('Vrark "Orc encampment 1" (servuo.dev 2395)',
                       'Vrark: "you are welcome to do with as you wish" (he asks to see it on the shard); credit Vrark; see SOURCE.txt'),
    'paintings-odin': ('Odin "Paintings" (servuo.dev 2351)',
                       'none stated; see SOURCE.txt; public-domain paintings; community work: credit Odin, ship only inside the player package, do not repost'),
    'paintings-odin-2': ('Odin "Nightmare & The Magic Circle" (servuo.dev 2375)',
                         'none stated; see SOURCE.txt; public-domain paintings; community work: credit Odin, ship only inside the player package, do not repost'),
}
# the IDs that get a tiledata record (records.json and the server's ClusterFCommunityArtArt.Records)
RECORDS = {'cart-fruit-a', 'cart-fruit-b', 'cart-veg-a', 'cart-veg-b', 'lantern', 'rail-y', 'rail-y-post',
           'beam-ew-left', 'beam-ew-right', 'beam-ns-left', 'beam-ns-right', 'orc-cage', 'orc-fire', 'orc-meat',
           'orc-palisade-1', 'orc-palisade-2', 'orc-tent-1', 'orc-tent-2', 'orc-tent-3'}


def rows():
    out = []
    for first, key, what, pack, files, how in S.GROUPS:
        src, lic = PACK[pack]
        n = len(files)
        for k, f in enumerate(files):
            i = first + k
            rel = f.split('/third-party/' + pack + '/', 1)[1]
            w = what if n == 1 else '%s, frame %d of %d' % (what.split(' (')[0], k + 1, n)
            if k == 0 and key in RECORDS:
                w += ' (base ID: the item ID; has our tiledata%s record)' % (' and animdata' if n > 1 else '')
            out.append([str(i), '0x%04X' % i, 'New Haven community art (cc-P237, F-21): ' + w, '%s %s' % (src, rel), lic, 'art'])
    return out


if __name__ == '__main__':
    new = rows()
    text = open(REG, encoding='ascii').read()
    have = {l.split(',')[0] for l in text.splitlines() if l and not l.startswith('#')}
    clash = [r[0] for r in new if r[0] in have]
    if clash: raise SystemExit('already registered: %s' % clash)
    if '--dry' in sys.argv:
        for r in new: print(','.join(r))
        raise SystemExit(0)
    buf = io.StringIO(); csv.writer(buf, lineterminator='\n').writerows(new)
    open(REG, 'a', encoding='ascii', newline='').write(buf.getvalue())
    print('appended', len(new))
