// cc-P856 red stub: the winter set's API with no behaviour (no designs, no rows, inert addons).
using System.Collections.Generic;
using ModernUO.Serialization;

namespace Server.Items
{
    public sealed record WinterSetPart(int ItemID, int X, int Y, int Z, int Hue, LightType? Light, string Name);

    public sealed record WinterSetDesign(string Key, string Name, string Credit, IReadOnlyList<WinterSetPart> Parts);

    public static class WinterSetDesigns
    {
        public static readonly Dictionary<string, WinterSetDesign> All = new();
    }

    [SerializationGenerator(0, false)]
    public partial class WinterSetComponent : AddonComponent
    {
        public WinterSetComponent(int itemID) : base(itemID)
        {
        }
    }

    [SerializationGenerator(0, false)]
    public partial class WinterSetAddon : BaseAddon
    {
        [SerializableField(0)]
        private string _design;

        public WinterSetAddon(string design)
        {
        }
    }

    [SerializationGenerator(0, false)]
    public partial class WinterSetDeed : BaseAddonDeed
    {
        [SerializableField(0)]
        private string _design;

        public WinterSetDeed(string design)
        {
        }

        public override BaseAddon Addon => new WinterSetAddon(_design);
    }

    [SerializationGenerator(0, false)]
    public partial class WinterSeasonAddon : WinterSetAddon, IWinterDecorItem
    {
        [SerializableField(0)]
        private string _key;

        public WinterSeasonAddon(ClusterFWinterDecorLayout.Row row) : base("")
        {
        }
    }
}

namespace Server
{
    public static class ClusterFWinterSetLayout
    {
        public const string AddonLayer = "addon";

        public static readonly ClusterFWinterDecorLayout.Row[] Rows = System.Array.Empty<ClusterFWinterDecorLayout.Row>();

        public static string DesignOf(string key) => null;
    }
}
