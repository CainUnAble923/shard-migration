"""cc-P677: ExodusSummoningAlter.ShrineSpots on the SoS shrines. The author's shrines lay their glyph tiles flat (stock
raised a platform), so each tome spot is its glyph's tile at the one open standing Z there (probe.py, spots.check).
Honor has no glyph on SoS (only his region): its spot keeps x, y on the region's ground."""
import os

BS = chr(92)
p = BS.join(['D:', 'UO', 'golems', 'Iron', 'ShatteredLegacy', 'server', 'customizations', 'Services', 'Revamped Dungeons',
             'TheExodusEncounter', 'Items', 'ExodusSummoningAltar.cs'])
s = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
old = [
    '        /// <summary>ServUO: the tome\'s spot per shrine region name.</summary>',
    '        ("Shrine of Compassion", new Point3D(1858, 875, 12)),',
    '        ("Shrine of Honesty", new Point3D(4209, 564, 60)),',
    '        ("Shrine of Honor", new Point3D(1727, 3528, 15)),',
    '        ("Shrine of Humility", new Point3D(4274, 3697, 12)),',
    '        ("Shrine of Justice", new Point3D(1301, 634, 28)),',
    '        ("Shrine of Sacrifice", new Point3D(3355, 290, 16)),',
    '        ("Shrine of Spirituality", new Point3D(1606, 2490, 20)),',
    '        ("Shrine of Valor", new Point3D(2492, 3931, 17))',
]
new = [
    '        /// <summary>The tome\'s spot per shrine region name. ServUO\'s spots stood on stock\'s raised shrines; on the Siege of',
    '        /// Sosaria land (cc-P677) each is the shrine glyph\'s tile at its standing Z. Honor has no glyph there, only its',
    '        /// region, so its spot is ServUO\'s x, y on the ground.</summary>',
    '        ("Shrine of Compassion", new Point3D(1858, 875, 0)),',
    '        ("Shrine of Honesty", new Point3D(4209, 564, 65)),',
    '        ("Shrine of Honor", new Point3D(1727, 3528, 3)),',
    '        ("Shrine of Humility", new Point3D(4274, 3697, 0)),',
    '        ("Shrine of Justice", new Point3D(1301, 634, 16)),',
    '        ("Shrine of Sacrifice", new Point3D(3355, 290, 4)),',
    '        ("Shrine of Spirituality", new Point3D(1595, 2490, 25)),',
    '        ("Shrine of Valor", new Point3D(2492, 3931, 10))',
]
a = nl.join(old)
if a not in s:
    a = nl.join(['    ' + l if False else l for l in old])
assert s.count(nl.join(old[1:])) == 1, 'spots'
s = s.replace(nl.join(old[1:]), nl.join(new[3:]))
summ = [l for l in s.split(nl) if 'ServUO: the tome' in l]
assert len(summ) == 1, summ
indent = summ[0][:len(summ[0]) - len(summ[0].lstrip())]
s = s.replace(summ[0], nl.join(indent + l.strip() for l in new[:3]))
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
