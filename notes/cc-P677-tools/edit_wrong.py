"""cc-P677 (S8 item 2): three of Wrong revamped's teleporter ends on the Siege of Sosaria version of the rooms, and the
sparkle WrongDecoration puts on each (P669's literal patterns do not read that table's format).
  - 5827, 590, 1 -> 5827, 592, 0: the floor now begins two tiles south (590-591 are rock).
  - 5690, 573, 25 -> 5690, 571, 25: the upper floor (Z 25) now ends at y 571 (572-574 rock).
  - 5872, 532, 24 -> 5872, 532, 15: the floor there is at Z 15.
Checked with spots.Land.open_tops."""
import os

BS = chr(92)
R = BS.join(['D:', 'UO', 'golems', 'Iron', 'ShatteredLegacy', 'server', 'customizations', 'Services', 'Revamped Dungeons',
             'WrongDungeon'])


def edit(name, pairs):
    p = os.path.join(R, name)
    s = open(p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (name, a, s.count(a))
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('ok', name)


edit('Generate.cs', [
    ('(new Point3D(5690, 569, 25), new Point3D(5827, 590, 1)),',
     '(new Point3D(5690, 569, 25), new Point3D(5827, 592, 0)), // cc-P677: ServUO 5827, 590, 1, rock on SoS'),
    ('(new Point3D(5829, 595, 0), new Point3D(5690, 573, 25)),',
     '(new Point3D(5829, 595, 0), new Point3D(5690, 571, 25)), // cc-P677: ServUO 5690, 573, 25, rock on SoS'),
    ('(new Point3D(5690, 569, 25), new Point3D(5872, 532, 24)),',
     '(new Point3D(5690, 569, 25), new Point3D(5872, 532, 15)), // cc-P677: ServUO z 24; the floor is 15 on SoS'),
])
edit('WrongDecoration.cs', [
    ('new("Static", 0x375A, 5690, 573, 25, null),', 'new("Static", 0x375A, 5690, 571, 25, null), // cc-P677: with its teleporter'),
    ('new("Static", 0x375A, 5827, 590, 1, null),', 'new("Static", 0x375A, 5827, 592, 0, null), // cc-P677: with its teleporter'),
    ('new("Static", 0x375A, 5872, 532, 24, null),', 'new("Static", 0x375A, 5872, 532, 15, null), // cc-P677: with its teleporter'),
])
