// cc-P859 RED stub: the same API as Items/Thanksgiving/HornOfPlenty.cs with no behaviour. Never shipped.
#nullable enable
using System;
using ModernUO.Serialization;
using Server.Gumps;
using Server.Mobiles;

namespace Server.Items;

[SerializationGenerator(0, false)]
public partial class HornOfPlenty : Item
{
    public static Func<DateTime> Clock = () => Core.Now;
    public static Func<double> Roll = Utility.RandomDouble;

    [SerializableField(0)] private int _charges;
    [SerializableField(1)] private DateTime _nextRecharge;

    [Constructible]
    public HornOfPlenty() : base(0x4BD9) { }

    public static bool IsHarvestMonth(DateTime when) => false;
    public bool CheckRecharge() => false;
    public void Use(Mobile from, double roll) { }
}

[SerializationGenerator(0, false)]
public partial class RoastingPigOnASpitAddon : BaseAddon
{
    public static Func<double> Roll = Utility.RandomDouble;
    [SerializableField(0)] private DateTime _nextEatTime;

    [Constructible]
    public RoastingPigOnASpitAddon(bool east = false, DateTime nextEatTime = default) { }
}

[SerializationGenerator(0, false)]
public partial class RoastingPigOnASpitDeed : BaseAddonDeed, IRewardOption
{
    [SerializableField(0)] private DateTime _nextEatTime;

    [Constructible]
    public RoastingPigOnASpitDeed() { }

    public override BaseAddon Addon => new RoastingPigOnASpitAddon();
    public void GetOptions(RewardOptionList list) { }
    public void OnOptionSelected(Mobile from, int choice) { }
}

[SerializationGenerator(0, false)]
public partial class PulledPorkPlatter : Food
{
    [Constructible]
    public PulledPorkPlatter() : base(0x97B) { }
}

[SerializationGenerator(0, false)]
public partial class PulledPorkSandwich : Food
{
    [Constructible]
    public PulledPorkSandwich() : base(0x97B) { }
}
