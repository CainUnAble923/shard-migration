// cc-P861 red stub: the code before the change. Only the names the facts use, all inert: no name lists, no rule, no
// statify. With the HEAD copies of the builder (plus Stashed), the seasonal switch and the gargish outcast.
#nullable enable
using System;
using System.Collections.Generic;
using Server.Items;
using Server.Mobiles;

namespace Server.Misc
{
    public sealed class ShardNameRow
    {
        public string Type { get; set; } = "";
        public string Mode { get; set; } = "new";
        public string[] Names { get; set; } = [];
    }

    public sealed class ShardNameFile
    {
        public string Credit { get; set; } = "";
        public List<ShardNameRow> Lists { get; set; } = [];
    }

    public static class ShardNames
    {
        public const string FileName = "names-shard.json";
        public static string? FindDataFile(string fileName, bool ours = true) => null;
        public static ShardNameFile Read(string path) => new();
        public static List<string> Apply(ShardNameFile file) => [];
        public static string? ListOf(BaseCreature m) => null;
        public static List<string> DedupeAmong(IEnumerable<BaseCreature> people, bool dryRun, out int renamed)
        {
            renamed = 0;
            return [];
        }
    }
}

namespace Server
{
    public static class AddonStatify
    {
        public static readonly Type[] SeededTypes = [];
        public static BaseAddon? AddonOf(object? targeted) => null;
        public static List<Static>? Statify(Mobile by, BaseAddon? addon, out string? refused)
        {
            refused = "not built";
            return null;
        }
    }
}
