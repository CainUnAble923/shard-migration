// cc-P857 red stub: the code before the change. There was no carpet deed; these are only the names the facts use, so
// they compile. Nothing here lays, sizes, checks or removes anything.
#nullable enable
using ModernUO.Serialization;
using Server.Gumps;
using Server.Network;

namespace Server.Items;

public sealed record VariableCarpetStyle(
    string Name, int NorthCorner, int EastCorner, int SouthCorner, int WestCorner,
    int NorthWestEdge, int NorthEastEdge, int SouthEastEdge, int SouthWestEdge, int Middle);

public enum VariableCarpetResult { Placed, NotInPack, NoMap, TwoFloors, TooSmall, TooBig, Occupied, NotInHouse, DoorTooClose, Blocked }

public static class VariableCarpetSettings
{
    public const int MinSide = 0;
    public const int DefaultMaxSide = 0;
    public static int? MaxSideOverride { get; set; }
    public static int MaxSide => 0;
    public static readonly VariableCarpetStyle[] Styles = [];
    public static readonly (string Name, int Hue)[] Hues = [];
    public static int HueAt(int index) => -1;
    public static VariableCarpetResult CheckSize(int width, int height) => VariableCarpetResult.Blocked;
}

[SerializationGenerator(0, false)]
public partial class VariableCarpetAddon : BaseAddon
{
    [Constructible]
    public VariableCarpetAddon(int style, int width, int height) { }
    public int Style => -1;
    public int Width => -1;
    public int Height => -1;
    public bool TryRemove(Mobile from) => false;
}

[SerializationGenerator(0, false)]
public partial class VariableCarpetDeed : BaseAddonDeed
{
    [Constructible]
    public VariableCarpetDeed() { }
    public override BaseAddon? Addon => null;
    public void BeginPlace(Mobile from, int style, int hueIndex) { }
    public VariableCarpetResult Place(Mobile from, Map? map, Point3D a, Point3D b, int style, int hueIndex) =>
        VariableCarpetResult.Blocked;
}

public sealed class VariableCarpetGump : DynamicGump
{
    public const int StyleButtonBase = 1;
    public const int HueButtonBase = 100;
    public VariableCarpetGump() : base(0, 0) { }
    public int HueIndex => -1;
    protected override void BuildLayout(ref DynamicGumpBuilder builder) { }
}

public sealed class VariableCarpetRemoveGump : DynamicGump
{
    public const int RemoveButton = 1;
    public VariableCarpetRemoveGump() : base(0, 0) { }
    protected override void BuildLayout(ref DynamicGumpBuilder builder) { }
}
