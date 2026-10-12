# cc-P34 WRITES: appends the 47 winter rows to registry.csv (once; refuses if any of the IDs is there).
import csv, io, os
exec(open('convert_art.py').read().split("if __name__")[0])
REG = r'D:/ShatteredLegacy/player-package/vendor/shattered-legacy-art/registry.csv'
WHAT = {
    15424: 'Father Christmas statue (animated torch, 5 frames)', 15429: 'raised firepit (animated, 5 frames)',
    15434: 'iron stove (animated, 4 frames)', 15438: 'stone stove (animated, 4 frames)',
    15442: 'decorated Christmas tree', 15443: "Santa's bag", 15444: 'present (orange)', 15445: 'present (pink)',
    15446: 'present (green)', 15447: 'candy cane arch, facing 1', 15448: 'candy cane arch, facing 2',
    15449: 'eggnog tray', 15450: 'eggnog tray (second)', 15451: 'pan of Christmas cookies', 15452: 'tray of candy canes',
    15453: 'holiday platter', 15454: 'roast turkey', 15455: 'gingerbread house', 15456: 'Christmas fireplace',
    15457: 'garland (on a north wall, faces south)', 15458: 'garland (on a west wall, faces east)',
    15459: 'holiday painting A (north wall, faces south)', 15460: 'holiday painting A (west wall, faces east)',
    15461: 'holiday painting B (north wall, faces south)', 15462: 'holiday painting B (west wall, faces east)',
    15463: 'snow-covered painting (west wall, faces east)', 15464: 'snow-covered painting (north wall, faces south)',
    15465: 'snow-covered shield (west wall, faces east)', 15466: 'snow-covered shield (north wall, faces south)',
    15467: 'snow patch 1', 15468: 'snow patch 2', 15469: 'snow patch 3', 15470: 'Christmas sleigh',
}
RECORDS = {15424: 'tiledata and animdata', 15429: 'tiledata and animdata', 15434: 'tiledata and animdata',
           15438: 'tiledata and animdata', 15442: 'tiledata', 15456: 'tiledata', 15470: 'tiledata'}
PACK = {'For ServUO 2': 'MrRiots "Winter/Christmas Related stuff" (servuo.dev 2388) For ServUO 2',
        'Christmas sprites': 'Vrark "Christmas sprites" (servuo.dev 2545)'}
rows = []
for first, files in GROUPS:
    n = len(files)
    for k, f in enumerate(files):
        i = first + k
        rel = f.split('/winter-holiday/')[1]
        pack = PACK[rel.split('/')[0]]
        what = WHAT[first] if n == 1 else '%s frame %d of %d' % (WHAT[first].split(' (')[0], k + 1, n)
        if k == 0 and first in RECORDS:
            what += ' (base ID: the item ID; has our %s record)' % RECORDS[first]
        rows.append([str(i), '0x%04X' % i, 'winter decor (F-22): ' + what, '%s %s' % (pack, rel.split('/', 1)[1]),
                     'none stated; see SOURCE.txt', 'art'])
text = open(REG, encoding='ascii').read()
have = {l.split(',')[0] for l in text.splitlines() if l and not l.startswith('#')}
clash = [r[0] for r in rows if r[0] in have]
if clash: raise SystemExit('already registered: %s' % clash)
buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n'); w.writerows(rows)
open(REG, 'a', encoding='ascii', newline='').write(buf.getvalue())
print('appended', len(rows))
