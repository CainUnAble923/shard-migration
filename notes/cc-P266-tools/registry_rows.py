# cc-P266 WRITES: appends this set's rows to registry.csv (once; refuses if any of the IDs is there), 47 art rows and
# the advent calendar's gump row. One row per ID, written before any PNG is made (P26's rule). The license column
# carries the author's own words from each folder's SOURCE.txt and the credit rule.
import csv, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art_src as S
REG = 'D:/UO/golems/Bronze/ShatteredLegacy/player-package/vendor/shattered-legacy-art/registry.csv'
PACK = {
    'mrriots-christmas': ('MrRiots "Christmas Art for UO" (servuo.dev 2013)',
                          'MrRiots: "Per usual, use these freely and edit them/label as you wish" (SOURCE.txt); credit MrRiots (the animated trees: thanks to Vorspire, per the author); built partly from OSI/EA assets: ship only as our PNG overrides inside the player package, never as an EA file, do not repost'),
    'mrriots-christmas-calendar': ('MrRiots "Christmas Calendar [Gump/Item]" (servuo.dev 2069)',
                                   'MrRiots: "Use as you wish, edit as you wish, enjoy!" (SOURCE.txt); credit MrRiots; built partly from OSI/EA assets: ship only as our PNG overrides inside the player package, never as an EA file, do not repost'),
}
# the IDs that get a tiledata record (records.json and the server's ClusterFWinterDecorArt.Records)
RECORDS = {'tree-large', 'tree-small', 'candle-tall', 'candle-short', 'antler', 'advent', 'potted'}


def rows():
    out = []
    for first, key, what, pack, files, how in S.GROUPS:
        src, lic = PACK[pack]
        n = len(files)
        for k, f in enumerate(files):
            i = first + k
            rel = f.split('/third-party/' + pack + '/', 1)[1]
            w = what if n == 1 else '%s, frame %d of %d' % (what.split(', animated')[0], k + 1, n)
            if k == 0 and key in RECORDS:
                w += ' (base ID: the item ID; has our tiledata%s record)' % (' and animdata' if n > 1 else '')
            out.append([str(i), '0x%04X' % i, 'winter decor (cc-P266, F-22): ' + w, '%s %s' % (src, rel), lic, 'art'])
    src, lic = PACK['mrriots-christmas-calendar']
    out.append([str(S.GUMP_ID), '0x%04X' % S.GUMP_ID, 'winter decor (cc-P266, F-22): the advent calendar gump, 400 x 400 (WinterAdventCalendarGump)',
                '%s AdventCalendar.bmp' % src, lic, 'gump'])
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
