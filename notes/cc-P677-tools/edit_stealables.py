"""cc-P677 (S8 item 2): the stealable artifacts our patch appends that stood on stock land the Siege of Sosaria map has
replaced: Ararat's 3 (the Exploring the Deep wreck, 6303-6313, 1664-1756: the author's dungeon caves now, and this
shard builds no wreck) and Castle Blackthorne's 6 (Blackthorn is off, item 1; P691 moves it into the Fold). Saves match
entries by index, so they stay in place, parked on Map.Internal; CheckRespawn never spawns a parked entry.
Usage: edit_stealables.py <b copy of StealableArtifacts.cs (pinned + our patch)>"""
import sys

p = sys.argv[1]
s = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'

parked = [
    ('new(Map.Trammel, new Point3D(6303, 1664, 11)', 'new(Map.Internal, new Point3D(6303, 1664, 11)'),
    ('new(Map.Trammel, new Point3D(6303, 1756, 20)', 'new(Map.Internal, new Point3D(6303, 1756, 20)'),
    ('new(Map.Trammel, new Point3D(6313, 1753, -14)', 'new(Map.Internal, new Point3D(6313, 1753, -14)'),
    ('new(Map.Trammel, new Point3D(6436, 2606, 11)', 'new(Map.Internal, new Point3D(6436, 2606, 11)'),
    ('new(Map.Trammel, new Point3D(6298, 2673, 0)', 'new(Map.Internal, new Point3D(6298, 2673, 0)'),
    ('new(Map.Trammel, new Point3D(6455, 2700, 0)', 'new(Map.Internal, new Point3D(6455, 2700, 0)'),
    ('new(Map.Felucca, new Point3D(6436, 2606, 11)', 'new(Map.Internal, new Point3D(6436, 2606, 11)'),
    ('new(Map.Felucca, new Point3D(6298, 2673, 0)', 'new(Map.Internal, new Point3D(6298, 2673, 0)'),
    ('new(Map.Felucca, new Point3D(6455, 2700, 0)', 'new(Map.Internal, new Point3D(6455, 2700, 0)'),
]
for a, b in parked:
    assert s.count(a) == 1, a
    s = s.replace(a, b)

a = '        //Ararat Stealables (Exploring the Deep) - Artifact rarity 8' + nl
b = ('        // Shattered Legacy (cc-P677): parked on Map.Internal, never spawned (CheckRespawn), slots kept. The Siege of' + nl +
     '        // Sosaria map puts the author\'s dungeons where the Ararat wreck and Castle Blackthorne stood (this shard builds' + nl +
     '        // no wreck; Blackthorn is off until P691 moves it into the Fold, which gives its 6 their new spots).' + nl + a)
assert s.count(a) == 1
s = s.replace(a, b)

a = ('            if (Item == null && Core.Now >= NextRespawn)' + nl)
b = ('            if (Entry.Map == Map.Internal)' + nl +
     '            {' + nl +
     '                return; // Shattered Legacy (cc-P677): a parked entry keeps its slot and never spawns' + nl +
     '            }' + nl + nl + a)
assert s.count(a) == 1
s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
