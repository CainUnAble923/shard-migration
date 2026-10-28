"""cc-P677 (S8 item 2): Despise revamped's two evil-side spots on the Siege of Sosaria version of the rooms.
  - The evil ankh (5472, 754, 10): the author puts a pedestal with a statue on that tile, the middle of the raised altar
    platform; the ankh goes one tile east on the same platform, in front of it (5473, 754, 10).
  - Gate3's evil end (5388, 753, 5): the room's north and south edges are lined with pedestals round a sunken middle, and
    one stands on stock's gate tile; the gate goes one tile west, between the two north pedestals (5387, 753, 5).
Both checked with probe.py / spots.Land.open_tops."""
import os

BS = chr(92)
R = BS.join(['D:', 'UO', 'golems', 'Iron', 'ShatteredLegacy', 'server', 'customizations'])


def edit(rel, pairs):
    p = os.path.join(R, *rel.split('/'))
    s = open(p, encoding='utf-8', newline='').read()
    for a, b, n in pairs:
        assert s.count(a) == n, (rel, a, s.count(a))
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('ok', rel)


edit('Services/Revamped Dungeons/DespiseRevamped/Setup.cs', [
    ('        ankh.MoveToWorld(new Point3D(5472, 754, 10), Map.Trammel);',
     '        ankh.MoveToWorld(new Point3D(5473, 754, 10), Map.Trammel); // cc-P677: SoS puts a pedestal on 5472, 754', 1),
    ('gate2 = new GateTeleporter(3948, 1960, new Point3D(5388, 753, 5), Map.Trammel);',
     'gate2 = new GateTeleporter(3948, 1960, new Point3D(5387, 753, 5), Map.Trammel); // cc-P677: SoS\'s pedestal on 5388', 1),
    ('gate1.MoveToWorld(new Point3D(5388, 753, 5), Map.Trammel);',
     'gate1.MoveToWorld(new Point3D(5387, 753, 5), Map.Trammel);', 1),
])
edit('Items/Functional/DespiseAnkh.cs', [
    ('the evil side (5472, 754, 10)', 'the evil side (5473, 754, 10; cc-P677)', 1),
])
