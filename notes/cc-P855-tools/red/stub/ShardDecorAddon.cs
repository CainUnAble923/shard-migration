// cc-P855 red mutant "stub": the ShardDecor API with no behaviour, so the new facts compile against the code before the
// change (no addon, no data, no store rows: the probe keeps the image's own store files and installs no data).

#nullable enable

using System;
using System.Collections.Generic;
using ModernUO.Serialization;
using Server.Gumps;
using Server.Network;

namespace Server.Items;

public sealed record ShardDecorPart(int ItemID, int X, int Y, int Z, int Hue, LightType? Light, string? Name);

public sealed class ShardDecorDesign
{
    public string Key { get; init; } = "";
    public string Name { get; init; } = "";
    public string Credit { get; init; } = "";
    public string Group { get; init; } = "";
    public string Facing { get; init; } = "";
    public IReadOnlyList<ShardDecorPart> Parts { get; init; } = [];
    public string GroupName => Name;
}

public static class ShardDecorDesigns
{
    public static string? FolderOverride { get; set; }
    public static IReadOnlyList<string> Refused => [];
    public static IReadOnlyDictionary<string, ShardDecorDesign> All => new Dictionary<string, ShardDecorDesign>();
    public static ShardDecorDesign? Get(string? key) => null;
    public static List<ShardDecorDesign> Facings(string? group) => [];
    public static IEnumerable<string> Groups() => [];
    public static int Reload() => 0;
    public static ShardDecorDesign Parse(string key, string text) => new() { Key = key };
    public static ShardDecorAddon Place(string design, Map map, Point3D at) => new(design);
    public static int Clear(Map map, Point3D at, int range) => 0;
}

[SerializationGenerator(0, false)]
public partial class ShardDecorComponent : AddonComponent
{
    public ShardDecorComponent(int itemID) : base(itemID)
    {
    }
}

[SerializationGenerator(0, false)]
public partial class ShardDecorAddon : BaseAddon
{
    [SerializableField(0)]
    private string? _design;

    [SerializableField(1)]
    private string? _group;

    [SerializableField(2)]
    private string? _credit;

    public ShardDecorAddon(string design)
    {
    }
}

[SerializationGenerator(0, false)]
public partial class ShardDecorDeed : BaseAddonDeed
{
    [SerializableField(0)]
    private string? _group;

    public ShardDecorDeed(string group)
    {
    }

    public string? Design { get; set; }

    public override BaseAddon Addon => new ShardDecorAddon("");

    public bool ChooseFacing(Mobile from, int index) => false;
}

public sealed class ShardDecorFacingGump : DynamicGump
{
    public ShardDecorFacingGump(ShardDecorDeed deed, List<ShardDecorDesign> facings) : base(60, 60)
    {
    }

    public IReadOnlyList<ShardDecorDesign> Choices => [];

    protected override void BuildLayout(ref DynamicGumpBuilder builder)
    {
    }

    public override void OnResponse(NetState sender, in RelayInfo info)
    {
    }
}
