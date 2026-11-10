// cc-P858 red stub: the code before the change had no such lamps; only the names the facts use, all inert.
#nullable enable
using System;
using ModernUO.Serialization;
namespace Server.Items;
public readonly record struct LampLook(int Unlit, int Lit);
[SerializationGenerator(0, false)]
public abstract partial class ShardLamp : BaseLight
{
    protected ShardLamp() : base(0x1) { }
    public virtual LampLook[] Looks => [];
    public virtual string Credit => "";
    public int LookIndex => -1;
    public override int LitItemID => 0x1;
}
[SerializationGenerator(0, false)] public partial class DragonLantern : ShardLamp { [Constructible] public DragonLantern() { } }
[SerializationGenerator(0, false)] public partial class BirdLamp : ShardLamp { [Constructible] public BirdLamp() { } }
[SerializationGenerator(0, false)] public partial class KoiLamp : ShardLamp { [Constructible] public KoiLamp() { } }
[SerializationGenerator(0, false)] public partial class DragonEggLamp : ShardLamp { [Constructible] public DragonEggLamp() { } }
[SerializationGenerator(0, false)] public partial class StainedGlassLamp : ShardLamp { [Constructible] public StainedGlassLamp() { } }
[SerializationGenerator(0, false)] public partial class TallAntiqueLamp : ShardLamp { [Constructible] public TallAntiqueLamp() { } }
[SerializationGenerator(0, false)] public partial class TallModernLamp : ShardLamp { [Constructible] public TallModernLamp() { } }
[SerializationGenerator(0, false)] public partial class OrnateTableLamp : ShardLamp { [Constructible] public OrnateTableLamp() { } }
[SerializationGenerator(0, false)] public partial class DragonBrazier : ShardLamp { [Constructible] public DragonBrazier() { } }
[SerializationGenerator(0, false)] public partial class CandleTray : ShardLamp { [Constructible] public CandleTray() { } }
[SerializationGenerator(0, false)] public partial class JackLantern : ShardLamp { [Constructible] public JackLantern() { } }
public static class ShardLampStock
{
    public static readonly (string Key, string Label, int Art, Func<ShardLamp> Make)[] All = [];
    public const string HalloweenKey = "jacklantern";
}
