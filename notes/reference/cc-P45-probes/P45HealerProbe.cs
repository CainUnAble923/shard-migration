// cc-P45 THROWAWAY PROBE A1: a controlled creature as a bandage and potion healer. Worktree only; never commit.

using System;
using Server;
using Server.Gumps;
using Server.Items;
using Server.Mobiles;
using Server.Tests.Network;
using Xunit;
using Xunit.Abstractions;

namespace ShatteredLegacy.Tests;

[Collection("Sequential UOContent Tests")]
public class P45HealerProbe
{
    private readonly ITestOutputHelper _out;

    public P45HealerProbe(ITestOutputHelper output) => _out = output;

    private static Bandage GiveBandages(Mobile healer, int amount = 50)
    {
        var b = new Bandage(amount);
        healer.Backpack.DropItem(b);
        return b;
    }

    // The player's path: double-click bandages, target the patient. The companion's cursor is Invoked.
    private static BandageContext Apply(Mobile healer, Bandage b, Mobile patient)
    {
        b.OnDoubleClick(healer);
        Assert.NotNull(healer.Target);
        healer.Target.Invoke(healer, patient);
        return BandageContext.GetContext(healer);
    }

    // Advance until the bandage lands, holding the patient's hits down (the test host regenerates 125 hits/s).
    private static (double seconds, int lowest, int after) Finish(BandageContext ctx, Mobile patient, int hold)
    {
        var start = Core.Now;
        var lowest = int.MaxValue;
        var guard = 0;

        while (ctx.Running && guard++ < 2000)
        {
            if (patient.Alive && patient.Hits > hold)
            {
                patient.Hits = hold;
            }

            lowest = Math.Min(lowest, patient.Hits);
            ShardTestClock.Advance(TimeSpan.FromMilliseconds(8));
        }

        return ((Core.Now - start).TotalSeconds, lowest, patient.Hits);
    }

    [Fact]
    public void A1_HealsOwnerAndSiblingWithRealBandagesAtPlayerSpeedAndMath()
    {
        ShardTestClock.Arm();
        var at = P45.NextSpot();
        var owner = P45.Owner(at);
        var healer = P45.Companion(owner);
        var sibling = P45.Companion(owner, 0, 1);
        P45.Skill(healer, SkillName.Healing, 100);
        P45.Skill(healer, SkillName.Anatomy, 100);
        var b = GiveBandages(healer);
        var before = b.Amount;

        owner.Hits = 20;
        var ctx = Apply(healer, b, owner);
        Assert.NotNull(ctx);
        var (secs, low, after) = Finish(ctx, owner, 20);
        var expected = 3.2 - Math.Sin(healer.Dex / 130.0) * 2.5;
        _out.WriteLine($"owner: dex={healer.Dex} delay={secs:F2}s expected={expected:F2}s hits {low}->{after} " +
                       $"bandages {before}->{b.Amount}");
        Assert.InRange(secs, expected - 0.05, expected + 0.05);
        Assert.True(after > low + 10, "the bandage healed the owner by the AOS formula range");
        Assert.Equal(before - 1, b.Amount);

        sibling.Hits = 20;
        ctx = Apply(healer, b, sibling);
        Assert.NotNull(ctx);
        (secs, low, after) = Finish(ctx, sibling, 20);
        _out.WriteLine($"sibling: delay={secs:F2}s hits {low}->{after} primary={BandageContext.GetPrimarySkill(sibling)}");
        Assert.Equal(SkillName.Healing, BandageContext.GetPrimarySkill(sibling));
        Assert.True(after > low + 10);

        // Self-heal uses the self formula (5 + 0.5 * (120 - dex) / 10 under AOS).
        healer.Hits = 20;
        ctx = Apply(healer, b, healer);
        (secs, _, _) = Finish(ctx, healer, 20);
        _out.WriteLine($"self: delay={secs:F2}s expected={5.0 + 0.5 * ((120 - healer.Dex) / 10.0):F2}s");
        Assert.InRange(secs, 5.0 + 0.5 * ((120 - healer.Dex) / 10.0) - 0.05, 5.0 + 0.5 * ((120 - healer.Dex) / 10.0) + 0.05);
    }

    [Fact]
    public void A1_HealingAndAnatomyGainForACompanionHealer()
    {
        ShardTestClock.Arm();
        var at = P45.NextSpot();
        var owner = P45.Owner(at);
        var healer = P45.Companion(owner);
        var sibling = P45.Companion(owner, 0, 1);
        P45.Skill(healer, SkillName.Healing, 50);
        P45.Skill(healer, SkillName.Anatomy, 50);
        var b = GiveBandages(healer, 200);

        for (var i = 0; i < 60; i++)
        {
            sibling.Hits = 20;
            var ctx = Apply(healer, b, sibling);
            Finish(ctx, sibling, 20);
        }

        _out.WriteLine($"after 60 bandages: Healing {healer.Skills.Healing.Base:F1} Anatomy {healer.Skills.Anatomy.Base:F1}");
        Assert.True(healer.Skills.Healing.Base > 50.0);
        Assert.True(healer.Skills.Anatomy.Base > 50.0);
    }

    [Fact]
    public void A1_CuresPoisonOnTheOwner()
    {
        ShardTestClock.Arm();
        var at = P45.NextSpot();
        var owner = P45.Owner(at);
        var healer = P45.Companion(owner);
        P45.Skill(healer, SkillName.Healing, 100);
        P45.Skill(healer, SkillName.Anatomy, 100);
        var b = GiveBandages(healer);

        owner.ApplyPoison(null, Poison.Lesser);
        Assert.True(owner.Poisoned);
        var ctx = Apply(healer, b, owner);
        Finish(ctx, owner, owner.HitsMax);
        _out.WriteLine($"owner poisoned after bandage: {owner.Poisoned}");
        Assert.False(owner.Poisoned);
    }

    [Fact]
    public void A1_ResurrectsTheOwnerAndASiblingWithBandages()
    {
        using var ns = PacketTestUtilities.CreateTestNetState();
        ShardTestClock.Arm();
        var at = P45.NextSpot();
        var owner = P45.Owner(at);
        owner.NetState = ns;
        var healer = P45.Companion(owner);
        var sibling = P45.Companion(owner, 0, 1);
        P45.Skill(healer, SkillName.Healing, 120);
        P45.Skill(healer, SkillName.Anatomy, 120);
        var b = GiveBandages(healer);

        try
        {
            sibling.Kill();
            _out.WriteLine($"sibling dead pet: {sibling.IsDeadPet}");
            Assert.True(sibling.IsDeadPet);

            var ctx = Apply(healer, b, sibling);
            Assert.NotNull(ctx);
            var (secs, _, _) = Finish(ctx, sibling, 1000);
            _out.WriteLine($"sibling res: delay={secs:F2}s gump to owner={owner.HasGump<PetResurrectGump>()} " +
                           $"stillDead={sibling.IsDeadPet}");
            Assert.True(owner.HasGump<PetResurrectGump>(), "a non-master healer sends the master the pet-res gump");

            owner.Kill();
            Assert.False(owner.Alive);
            _out.WriteLine($"living companion sees the ghost: {healer.CanSee(owner)} (ghost warmode={owner.Warmode})");
            owner.Warmode = true; // a ghost manifests to be seen and targeted, as for a player healer
            _out.WriteLine($"dead owner: hits={owner.Hits}/{owner.HitsMax} poisoned={owner.Poisoned} " +
                           $"canFit={owner.Map?.CanFit(owner.Location, 16, false, false)} " +
                           $"canBeBeneficial={healer.CanBeBeneficial(owner, false, true)}");
            ctx = Apply(healer, b, owner);
            Assert.NotNull(ctx);
            (secs, _, _) = Finish(ctx, owner, 1000);
            _out.WriteLine($"owner res: delay={secs:F2}s ResurrectGump={owner.HasGump<ResurrectGump>()}");
            Assert.True(owner.HasGump<ResurrectGump>());
        }
        finally
        {
            owner.NetState = null;
        }
    }

    [Fact]
    public void A1_DrinksHealAndCurePotionsThroughTheRealDoubleClick()
    {
        ShardTestClock.Arm();
        var at = P45.NextSpot();
        var owner = P45.Owner(at);
        var c = P45.Companion(owner);

        var heal = new GreaterHealPotion();
        c.Backpack.DropItem(heal);
        c.Hits = 20;
        heal.OnDoubleClick(c);
        var healed = c.Hits;
        _out.WriteLine($"heal potion: 20 -> {healed}, potion deleted={heal.Deleted}, bottle={c.Backpack.FindItemByType<Bottle>() != null}");
        Assert.True(healed > 21);
        Assert.True(heal.Deleted);

        var cure = new GreaterCurePotion();
        c.Backpack.DropItem(cure);
        c.ApplyPoison(null, Poison.Regular);
        Assert.True(c.Poisoned);
        cure.OnDoubleClick(c);
        _out.WriteLine($"cure potion: poisoned after={c.Poisoned}");
        Assert.False(c.Poisoned);
    }

    [Fact]
    public void A1_CanHealOwnerIsTheSeparateNonBandagePath()
    {
        // Pinned's built-in creature healer (BaseCreature.CanHeal/CanHealOwner) is a different path from BeginHeal.
        ShardTestClock.Arm();
        var at = P45.NextSpot();
        var owner = P45.Owner(at);
        var c = P45.Companion(owner);
        _out.WriteLine($"default CanHeal={c.CanHeal} CanHealOwner={c.CanHealOwner}");
        Assert.False(c.CanHealOwner);
    }
}
