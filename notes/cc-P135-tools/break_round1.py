"""cc-P135 red-first, round 1: ten breaks of ClusterFMapCheck.cs at once, each aimed at a different fact. Exact
replacements; aborts if an anchor is missing. Pinned treats warnings as errors, so no break may leave anything unused."""
import sys

P = r'D:\ShatteredLegacy\server\customizations\StaffHub\ClusterFMapCheck.cs'
s = open(P, encoding='utf-8').read()

BREAKS = [
    # B1: a Surface static (a table) blocks too -> fact 2 (and the Walkable fact, which crosses the table tile)
    ('if ((f & TileFlag.Impassable) != 0 && (f & TileFlag.Surface) == 0)', 'if ((f & TileFlag.Impassable) != 0)'),
    # B2: a spread equal to the limit is refused -> fact 3
    ('public bool ZOk => Spread <= MaxZSpread;', 'public bool ZOk => Spread < MaxZSpread;'),
    # B3: a tile is read before the footprint is refused -> fact 4 (Reads must stay 0)
    ('        if (width <= 0 || height <= 0 || width > MaxFootprint || height > MaxFootprint)\n        {\n            return new ClusterFFootprintResult { Refused = $"Footprint must be positive',
     '        var probe = src.GetLandTile(Math.Max(0, x), Math.Max(0, y)).Z;\n        if (width <= 0 || height <= 0 || width > MaxFootprint || height > MaxFootprint || probe > 200)\n        {\n            return new ClusterFFootprintResult { Refused = $"Footprint must be positive'),
    # B4: the 500-spot cap is not applied to lines -> fact 5
    ('            if (r.Spots.Count >= max)\n            {\n                r.Dropped++;\n                continue;\n            }\n\n            r.Spots.Add(new ClusterFSpot(x, y, z, map, $"{source} {n}"));',
     '            if (r.Spots.Count >= max && max < 0)\n            {\n                r.Dropped++;\n                continue;\n            }\n\n            r.Spots.Add(new ClusterFSpot(x, y, z, map, $"{source} {n}"));'),
    # B5: a spawner with no map does not get the default -> fact 6
    ('var map = e.TryGetProperty("map", out var m) && m.ValueKind == JsonValueKind.String ? m.GetString() : defaultMap;',
     'var map = e.TryGetProperty("map", out var m) && m.ValueKind == JsonValueKind.String ? m.GetString() : (defaultMap == null ? null : (string)null);'),
    # B6: a spot off the map is not caught -> fact 7
    ('            else if (!OnMap(src, s.X, s.Y))\n            {\n                s.Problem = $"outside the {src.Width}x{src.Height} map";\n            }\n',
     ''),
    # B7: a duplicate is the same id at any Z -> fact 8
    ('if (!seen.Add((s.ID, s.Z)))', 'if (!seen.Add((s.ID, 0)))'),
    # B9: markers are not hued -> fact 10
    ('        Hue = BlockedHue;\n        Name = "blocked: " + reason;', '        Name = "blocked: " + reason;'),
    # B10: a shallow bed is not water -> fact 11 (StaticIsWet stays in use)
    ('                if (StaticIsWet(s.ID))\n                {\n                    bedZ = Math.Max(bedZ, s.Z);\n                }',
     '                if (StaticIsWet(s.ID) && bedZ == int.MaxValue)\n                {\n                    bedZ = Math.Max(bedZ, s.Z);\n                }'),
    # B11: the rectangle is written with inclusive x2,y2 -> fact 12
    ('            w.WriteNumber("x2", x + width);\n            w.WriteNumber("y2", y + height);', '            w.WriteNumber("x2", x + width - 1);\n            w.WriteNumber("y2", y + height - 1);'),
    # B12: .. is allowed -> fact 13
    ("if (Path.IsPathRooted(rel) || rel.StartsWith('/') || rel.Split('/').Any(p => p == \"..\"))", "if (Path.IsPathRooted(rel) || rel.StartsWith('/'))"),
]

for i, (old, new) in enumerate(BREAKS, 1):
    if s.count(old) != 1:
        sys.exit('break %d: anchor found %d times' % (i, s.count(old)))
    s = s.replace(old, new)
open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('round 1: %d breaks applied' % len(BREAKS))
