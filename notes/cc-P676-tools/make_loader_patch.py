"""cc-P676: edit the b/ copy of pinned RegionJsonSerializer.cs so LoadRegions takes Data/ShatteredLegacy/regions-*.json
in place of pinned's regions of the maps those files name. The patch is then diff -u a b (fuzz 0).
Usage: make_loader_patch.py <b copy of RegionJsonSerializer.cs>"""
import sys

p = sys.argv[1]
s = open(p, encoding='ascii', newline='').read()
crlf = '\r\n' in s
s = s.replace('\r\n', '\n')

subs = [
    ('using System.Text.Json;\nusing System.Text.Json.Serialization;\n',
     'using System.Linq;\nusing System.Text.Json;\nusing System.Text.Json.Nodes;\nusing System.Text.Json.Serialization;\n'),
    ('''        var regions = JsonConfig.Deserialize<List<Region>>(path, _options);
        if (regions == null)''',
     '''        var regions = LoadShardRegions(path) ?? JsonConfig.Deserialize<List<Region>>(path, _options);
        if (regions == null)'''),
    ('''            "Loading regions {Status} ({Count} regions) ({Duration:F2} seconds)",
            "done",
            count,
            stopwatch.Elapsed.TotalSeconds
        );
    }
''',
     '''            "Loading regions {Status} ({Count} regions) ({Duration:F2} seconds)",
            "done",
            count,
            stopwatch.Elapsed.TotalSeconds
        );
    }

    // Shattered Legacy (cc-P676): Data/ShatteredLegacy/regions-<map>.json (Trammel's on the Siege of Sosaria land)
    // replaces pinned's regions of every map it names; every other map keeps pinned's. Null when there is no such file.
    private static List<Region> LoadShardRegions(string path)
    {
        var dir = Path.Join(Core.BaseDirectory, "Data/ShatteredLegacy");
        var files = Directory.Exists(dir) ? Directory.GetFiles(dir, "regions-*.json").Order().ToArray() : [];
        if (files.Length == 0)
        {
            return null;
        }

        var merged = MergeShardRegions(ParseArray(path), files.Select(ParseArray));
        logger.Information("Regions: {Files} replace pinned's regions of their maps", string.Join(", ", files.Select(Path.GetFileName)));
        return merged.Deserialize<List<Region>>(_options);
    }

    private static JsonArray ParseArray(string file) =>
        JsonNode.Parse(
            File.ReadAllText(file),
            documentOptions: new JsonDocumentOptions { AllowTrailingCommas = true, CommentHandling = JsonCommentHandling.Skip }
        )!.AsArray();

    /// <summary>
    /// Shattered Legacy (cc-P676): pinned's region list with the regions of each map the shard files name replaced by
    /// theirs, put where that map's first pinned region stood (parents come before children in both).
    /// </summary>
    public static JsonArray MergeShardRegions(JsonArray pinned, IEnumerable<JsonArray> shard)
    {
        var ours = shard.SelectMany(a => a).ToList();
        var maps = new HashSet<string>(ours.Select(r => (string)r!["Map"]!), StringComparer.OrdinalIgnoreCase);
        var merged = new JsonArray();
        var placed = false;
        foreach (var r in pinned)
        {
            if (!maps.Contains((string)r!["Map"]!))
            {
                merged.Add(r.DeepClone());
                continue;
            }

            if (!placed)
            {
                foreach (var o in ours)
                {
                    merged.Add(o!.DeepClone());
                }

                placed = true;
            }
        }

        if (!placed)
        {
            foreach (var o in ours)
            {
                merged.Add(o!.DeepClone());
            }
        }

        return merged;
    }
'''),
]
for a, b in subs:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
if crlf:
    s = s.replace('\n', '\r\n')
open(p, 'w', encoding='ascii', newline='').write(s)
print('ok')
