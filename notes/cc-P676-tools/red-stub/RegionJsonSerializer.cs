/*************************************************************************
 * ModernUO                                                              *
 * Copyright 2019-2026 - ModernUO Development Team                       *
 * Email: hi@modernuo.com                                                *
 * File: RegionJsonSerializer.cs                                         *
 *                                                                       *
 * This program is free software: you can redistribute it and/or modify  *
 * it under the terms of the GNU General Public License as published by  *
 * the Free Software Foundation, either version 3 of the License, or     *
 * (at your option) any later version.                                   *
 *                                                                       *
 * You should have received a copy of the GNU General Public License     *
 * along with this program.  If not, see <http://www.gnu.org/licenses/>. *
 *************************************************************************/

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.Json.Serialization;
using System.Text.Json.Serialization.Metadata;
using Server.Json;
using Server.Logging;

namespace Server;

public static class RegionJsonSerializer
{
    private static readonly ILogger logger = LogFactory.GetLogger(typeof(RegionJsonSerializer));

    private static JsonDerivedType[] _derivedTypes = { new(typeof(Region), nameof(Region)) };

    public static IJsonTypeInfoResolver RegionJsonTypeInfoResolver => new DefaultJsonTypeInfoResolver()
    {
        Modifiers =
        {
            static typeInfo =>
            {
                if (typeInfo.Type != typeof(Region))
                {
                    return;
                }

                typeInfo.PolymorphismOptions = new JsonPolymorphismOptions();
                for (var i = 0; i < _derivedTypes.Length; i++)
                {
                    typeInfo.PolymorphismOptions.DerivedTypes.Add(_derivedTypes[i]);
                }
            },
            static typeInfo =>
            {
                if (!typeInfo.Type.IsAssignableTo(typeof(Region)))
                {
                    return;
                }

                typeInfo.OnDeserialized = o =>
                {
                    if (o is Region region && Core.Expansion >= region.MinExpansion && Core.Expansion <= region.MaxExpansion)
                    {
                        // Set the child level since it is not part of the JSON data, and our constructor skips setting parent.
                        if (region.Parent != null)
                        {
                            region.ChildLevel = region.Parent.ChildLevel + 1;
                        }
                        region.Register();
                    }
                };
            }
        }
    };

    private static JsonSerializerOptions _options = new(JsonConfig.DefaultOptions)
    {
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingDefault,
        TypeInfoResolver = RegionJsonTypeInfoResolver,
    };

    public static void Register<TRegion>() where TRegion : Region
    {
        for (var i = 0; i < _derivedTypes.Length; i++)
        {
            if (_derivedTypes[i].DerivedType == typeof(TRegion))
            {
                throw new Exception(
                    $"Type '{typeof(TRegion)}' has already been registered for serialization with the region loader."
                );
            }
        }

        Array.Resize(ref _derivedTypes, _derivedTypes.Length + 1);
        _derivedTypes[^1] = new JsonDerivedType(typeof(TRegion), typeof(TRegion).Name);
    }

    internal static void LoadRegions()
    {
        var path = Path.Join(Core.BaseDirectory, "Data/regions.json");

        logger.Information("Loading regions");

        var stopwatch = Stopwatch.StartNew();

        var regions = LoadShardRegions(path) ?? JsonConfig.Deserialize<List<Region>>(path, _options);
        if (regions == null)
        {
            throw new JsonException($"Failed to deserialize {path}.");
        }

        var count = 0;
        foreach (var region in regions)
        {
            if (Core.Expansion >= region.MinExpansion && Core.Expansion <= region.MaxExpansion)
            {
                count++;
            }
        }

        stopwatch.Stop();

        logger.Information(
            "Loading regions {Status} ({Count} regions) ({Duration:F2} seconds)",
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
        return (JsonArray)pinned.DeepClone(); // cc-P676 red stub: the shard file changes nothing
#pragma warning disable CS0162
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
}
