// cc-P860 red stub: the code before the change. Only the names the facts use, all inert: a mount with no numbers of its
// own and no dens. Swapped in for RidablePolarBear.cs and RidablePolarBearDens.cs by red-all.sh.
#nullable enable
using System.Collections.Generic;
using ModernUO.Serialization;

namespace Server.Mobiles;

[SerializationGenerator(0, false)]
public partial class RidablePolarBear : BaseMount
{
    public const string Credit = "";
    [Constructible]
    public RidablePolarBear() : base(0xC8, 0x3E9F, AIType.AI_Animal, FightMode.Aggressor) { }
}

public static class RidablePolarBearDens
{
    public record Den(string Name, Point3D Location, int Count, int HomeRange, int MinDelayMinutes, int MaxDelayMinutes);
    public static readonly Den[] Dens = [];
    public const int SearchRange = 1;
    public static List<string> Seed(bool dryRun = false) => [];
}
