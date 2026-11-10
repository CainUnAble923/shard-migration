// cc-P858 red stub: the code before the change had no wagon; only the names the facts use, all inert.
#nullable enable
using ModernUO.Serialization;
namespace Server.Items;
public sealed record WagonPart(int ItemID, int X, int Y, int Z, int Hue, LightType? Light, string? Name);
public static class FortuneTellerWagonDesign { public const string Credit = ""; public static readonly WagonPart[] Parts = []; }
[SerializationGenerator(0, false)] public partial class FortuneTellerWagonComponent : AddonComponent { public FortuneTellerWagonComponent(int itemID) : base(itemID) { } }
[SerializationGenerator(0, false)] public partial class FortuneTellerWagon : BaseAddon { [Constructible] public FortuneTellerWagon() { } }
