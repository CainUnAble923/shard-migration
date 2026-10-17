"""cc-P134: map UOP chunks in name order, not offset order (D:\\UO\\tools\\vseUOAware)."""
import os

ROOT = r'D:\UO\tools\vseUOAware'
NOTE = '// vseUOAware by ghostbyte420, GPL-3.0. Modified for Shattered Legacy 2026-10-17 (cc-P134): %s\n'


def edit(rel, pairs, note):
    p = os.path.join(ROOT, rel)
    raw = open(p, 'rb').read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    s = raw.decode('utf-8-sig')
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, (rel, old, n)
        s = s.replace(old, new)
    if note:
        s = NOTE % note + s
    open(p, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + s.encode('utf-8'))
    print('edited', rel)


edit('Services/uopFileReader.cs', [(
    '''    /// <summary>
    /// Finds the entry whose stored hash matches''',
    '''    /// <summary>
    /// The chunks of a map*LegacyMUL.uop in map order: entry k is the one named
    /// "build/&lt;file name, lower case&gt;/&lt;k:D8&gt;.dat" (as ClassicUO/TazUO find them by hash). The
    /// archive's on-disk order is not map order: in client 7.0.117.0's map1LegacyMUL.uop, 112 of its 113
    /// chunks are out of offset order, so ordering by offset reads the wrong block. Falls back to offset
    /// order only when no chunk matches the naming.
    /// </summary>
    public static List<UopEntry> ReadMapEntriesInOrder(string uopFilePath)
    {
        var entries = ReadEntries(uopFilePath);
        var byHash = new Dictionary<ulong, UopEntry>();
        foreach (var e in entries)
            byHash.TryAdd(e.Hash, e);

        string prefix = "build/" + Path.GetFileNameWithoutExtension(uopFilePath).ToLowerInvariant() + "/";
        var ordered = new List<UopEntry>();
        for (int k = 0; k < entries.Count; k++)
        {
            if (!byHash.TryGetValue(UopHashHelper.HashFileName($"{prefix}{k:D8}.dat"), out var e))
                break;
            ordered.Add(e);
        }

        return ordered.Count > 0 ? ordered : entries.OrderBy(e => e.Offset).ToList();
    }

    /// <summary>
    /// Finds the entry whose stored hash matches''')],
    'ReadMapEntriesInOrder added (map chunks\n// by name, not by offset).')

edit('Services/MapCoordinateReader.cs', [
    ('var entries = isUop ? uopFileReader.ReadEntries(mapUopFilePath).OrderBy(e => e.Offset).ToList() : null;',
     'var entries = isUop ? uopFileReader.ReadMapEntriesInOrder(mapUopFilePath) : null;'),
    ('var entries = uopFileReader.ReadEntries(mapFilePath).OrderBy(e => e.Offset).ToList();',
     'var entries = uopFileReader.ReadMapEntriesInOrder(mapFilePath);'),
], 'UOP map chunks are read in name order\n// (uopFileReader.ReadMapEntriesInOrder); offset order read the wrong blocks of our client\'s maps.')

edit('Services/MapAsciiRenderer.cs', [(
    '''            var entries = uopFileReader.ReadEntries(mapFilePath)
                .OrderBy(e => e.Offset)
                .ToList();''',
    '''            var entries = uopFileReader.ReadMapEntriesInOrder(mapFilePath);''')],
    'UOP map chunks are read in name order\n// (uopFileReader.ReadMapEntriesInOrder).')
