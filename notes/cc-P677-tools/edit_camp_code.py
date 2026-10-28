"""cc-P677 (S8 item 3): the mine camp's other spots, into the open pocket at the mountain's foot (replace_camp.py says
why). Each new tile is open on SoS at the given Z (spots.Land.open_tops, GetAverageZ on land):
  Survey Archivist 3496, 2754, 4 -> 3498, 2738, 4 (her tent's opening, with the tent)
  forge 3508, 2746, 0 -> 3499, 2746, 4;  anvil 3510, 2746, 0 -> 3498, 2746, 4
  Gervis 3505, 2749, 0 -> 3501, 2741, 1;  Mugg 3507, 2747, 0 -> 3497, 2747, 4;  Jacob Waltz 3510, 2745, 0 -> 3501, 2743, 1
The NewHavenSeederFloorVerification table (P678's measured floors) moves with them."""
import os

BS = chr(92)
R = BS.join(['D:', 'UO', 'golems', 'Iron', 'ShatteredLegacy', 'server'])


def edit(rel, pairs):
    p = os.path.join(R, *rel.split('/'))
    s = open(p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (rel, a, s.count(a))
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('ok', rel)


edit('customizations/ClusterFInstitutionSeeder.cs', [
    ('///   - Survey Archivist at Trammel 3496, 2754, Z=4 (mine camp, at its tent\'s opening)',
     '///   - Survey Archivist at Trammel 3498, 2738, Z=4 (mine camp, at its tent\'s opening; moved with it, cc-P677)'),
    ('            x: 3496, y: 2754, z: 4,', '            x: 3498, y: 2738, z: 4,'),
])
edit('customizations/SurveyArchivist.cs', [
    ('/// Location: Trammel 3496, 2754, Z=4 (mine camp, at the Survey Archivist\'s tent opening; cc-P16)',
     '/// Location: Trammel 3498, 2738, Z=4 (mine camp, at the Survey Archivist\'s tent opening; cc-P16, moved in cc-P677)'),
])
edit('customizations/ClusterFSouthMineDecor.cs', [
    ('        var forgeLocation = new Point3D(3508, 2746, 0);',
     '        // cc-P677: SoS\'s mountain covers ServUO\'s 3508, 2746 and 3510, 2746; the camp\'s open ground at its foot\n'
     '        var forgeLocation = new Point3D(3499, 2746, 4);'),
    ('        var anvilLocation = new Point3D(3510, 2746, 0);', '        var anvilLocation = new Point3D(3498, 2746, 4);'),
])
edit('customizations/ClusterFNewHavenSeeder.cs', [
    ('typeof(Gervis), () => new Gervis(), 3505, 2749, Direction.South, 0),',
     'typeof(Gervis), () => new Gervis(), 3501, 2741, Direction.South, 1), // cc-P677: 3505, 2749 is rock on SoS'),
    ('typeof(Mugg), () => new Mugg(), 3507, 2747, Direction.South, 0),',
     'typeof(Mugg), () => new Mugg(), 3497, 2747, Direction.South, 4), // cc-P677: 3507, 2747 is rock on SoS'),
    ('typeof(JacobWaltz), () => new JacobWaltz(), 3510, 2745, Direction.South, 0)',
     'typeof(JacobWaltz), () => new JacobWaltz(), 3501, 2743, Direction.South, 1)'),
])
edit('tests/Misc/NewHavenSeederFloorVerification.cs', [
    ('        ["Gervis"] = new(3505, 2749, 0),', '        ["Gervis"] = new(3501, 2741, 1), // cc-P677: the mine camp on SoS'),
    ('        ["Mugg"] = new(3507, 2747, 0),', '        ["Mugg"] = new(3497, 2747, 4),'),
    ('        ["Jacob Waltz"] = new(3510, 2745, 0),', '        ["Jacob Waltz"] = new(3501, 2743, 1),'),
])
