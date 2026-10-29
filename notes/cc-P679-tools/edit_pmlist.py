"""cc-P679: PMList's Trammel and Felucca gates onto the SoS land. Rewrites one copy of pinned PublicMoongate.cs.

    python -P edit_pmlist.py <PublicMoongate.cs>

Each of the author's stone circles is centred on the stock gate's own tile, raised or lowered: the gate keeps x, y
and takes the circle's floor (spots.Land.avgz, notes/cc-P679-tools/gates.txt). New Haven's gate is S7's
HavenSpots.PublicMoongate. Jhelom, Skara Brae, Magincia (pinned already reads its Z off the map) and Buccaneer's Den
stand as they are.
"""
import sys

NOTE = '    // Shattered Legacy (cc-P679, SoS swap S4): the gates on the Siege of Sosaria land. Each of the author\'s stone\n' \
       '    // circles is centred on the stock tile at a new height, so a gate keeps its x, y and takes the circle\'s floor.\n' \
       '    // New Haven\'s gate is in the author\'s Haven (cc-P678, HavenSpots). Notes: shard-migration notes/cc-P679-*.md.\n'
SWAPS = [
    ('new Point3D(4467, 1283, 5), 1012003),   // Moonglow', 'new Point3D(4467, 1283, 23), 1012003),  // Moonglow'),
    ('new Point3D(1336, 1997, 5), 1012004),   // Britain', 'new Point3D(1336, 1997, 15), 1012004),  // Britain'),
    ('new Point3D(771, 752, 5), 1012006),     // Yew', 'new Point3D(771, 752, 15), 1012006),    // Yew'),
    ('new Point3D(2701, 692, 5), 1012007),    // Minoc', 'new Point3D(2701, 692, 20), 1012007),   // Minoc'),
    ('new Point3D(1828, 2948, -20), 1012008), // Trinsic', 'new Point3D(1828, 2948, -16), 1012008), // Trinsic'),
]
HAVEN = ('new PMEntry(new Point3D(3450, 2677, 25), 1078098)                                   // New Haven',
         'new PMEntry(Server.Tutorial.HavenSpots.PublicMoongate, 1078098)                      // New Haven')


def main():
    path = sys.argv[1]
    text = open(path, encoding='utf-8', newline='').read()
    for old, new in SWAPS:
        n = text.count(old)
        assert n == 2, (old, n)  # Trammel and Felucca
        text = text.replace(old, new)
    assert text.count(HAVEN[0]) == 1
    text = text.replace(HAVEN[0], HAVEN[1])
    anchor = 'public class PMList\n{\n'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + NOTE)
    open(path, 'w', encoding='utf-8', newline='').write(text)


if __name__ == '__main__':
    main()
