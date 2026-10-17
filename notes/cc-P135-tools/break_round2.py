"""cc-P135 red-first, round 2: five more breaks of ClusterFMapCheck.cs, one fact each."""
import sys

P = r'D:\ShatteredLegacy\server\customizations\StaffHub\ClusterFMapCheck.cs'
s = open(P, encoding='utf-8').read()

BREAKS = [
    # B8: buried only when strictly more than 10 below -> fact 8 (the -10 static)
    ('if (s.Z <= landZ - BuriedThreshold)', 'if (s.Z < landZ - BuriedThreshold)'),
    # B13: the overlay is allowed on live -> fact 9
    ('        if (!isTestShard)\n        {\n            return "The overlay places temporary markers and runs on the test shard only. \'list\' works here.";\n        }\n',
     ''),
    # B15: the water surface limit is the hard limit -> fact 11 (Z -125 is no longer a fault)
    ('public const int WaterSurfaceLimit = 120;', 'public const int WaterSurfaceLimit = 127;'),
    # B16: a third token that is not a number is a bad line, never a map -> fact 5 ("13,23,Malas")
    ('                else if (parts.Length == 3)\n                {\n                    map = parts[2];\n                }\n', ''),
    # B19: a decoration entry gives a spot for the first map only -> fact 6
    ('            foreach (var map in maps)\n            {\n                if (r.Spots.Count >= max)', '            foreach (var map in maps.Take(1))\n            {\n                if (r.Spots.Count >= max)'),
]

for i, (old, new) in enumerate(BREAKS, 1):
    if s.count(old) != 1:
        sys.exit('break %d: anchor found %d times' % (i, s.count(old)))
    s = s.replace(old, new)
open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('round 2: %d breaks applied' % len(BREAKS))
