// cc-P45 THROWAWAY PROBES B8 (looting) and B9 (mounts). Worktree only; never commit.

using System;
using Server;
using Server.Items;
using Server.Mobiles;
using Server.Network;
using Xunit;
using Xunit.Abstractions;

namespace ShatteredLegacy.Tests;

[Collection("Sequential UOContent Tests")]
public class P45LootMountProbe
{
    private readonly ITestOutputHelper _out;

    public P45LootMountProbe(ITestOutputHelper output) => _out = output;

    private static Corpse KillFor(Mobile killer, BaseCreature victim)
    {
        victim.Damage(victim.Hits + 10, killer);
        var corpse = victim.Corpse as Corpse;
        Assert.NotNull(corpse);
        return corpse;
    }

    private (bool lifted, LRReason reason) Lift(Mobile who, Item item)
    {
        who.NextActionTime = Core.TickCount;
        who.Lift(item, item.Amount, out var rejected, out var reason);
        if (!rejected)
        {
            who.Drop(who.Backpack, new Point3D(-1, -1, 0));
        }

        return (!rejected, reason);
    }

    [Theory]
    [InlineData("Trammel")]
    [InlineData("Felucca")]
    public void B8_ACompanionLiftingFromItsOwnersKillIsJudgedAsItself(string facet)
    {
        ShardTestClock.Arm();
        var map = facet == "Felucca" ? Map.Felucca : Map.Trammel;
        var owner = P45.Owner(P45.NextSpot(), map);
        var c = P45.Companion(owner);

        var victim = P45.Place(new Ratman(), owner.Location, 1, 1, map);
        var corpse = KillFor(owner, victim);
        var gold = new Gold(50);
        corpse.DropItem(gold);

        _out.WriteLine($"{facet}: " +
                       $"IsCriminalAction(owner)={corpse.IsCriminalAction(owner)} IsCriminalAction(companion)=" +
                       $"{corpse.IsCriminalAction(c)} CanLoot(companion)={corpse.CanLoot(c, gold)}");

        var (lifted, reason) = Lift(c, gold);
        _out.WriteLine($"{facet}: companion lift={lifted} reason={reason} companion criminal={c.Criminal} " +
                       $"owner criminal={owner.Criminal}");

        // The finding either way: the companion is judged as itself, not as its owner.
        Assert.True(corpse.IsCriminalAction(c));
        Assert.False(corpse.IsCriminalAction(owner));
    }

    [Fact]
    public void B8_CodeThatMovesItemsDirectlyBypassesEveryLootingCheck()
    {
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot(), Map.Felucca);
        var c = P45.Companion(owner);
        var stranger = P45.Owner(new Point3D(owner.X + 3, owner.Y, owner.Z), Map.Felucca);
        var victim = P45.Place(new Ratman(), owner.Location, 1, 1, Map.Felucca);
        var corpse = KillFor(stranger, victim);
        var gold = new Gold(50);
        corpse.DropItem(gold);

        // The Squire and Mercenary pattern: DropItem / MoveToContainer straight into the pack.
        c.Backpack.DropItem(gold);
        _out.WriteLine($"direct move from a stranger's kill: in pack={gold.IsChildOf(c.Backpack)} " +
                       $"companion criminal={c.Criminal} IsCriminalAction(owner)={corpse.IsCriminalAction(owner)}");
        Assert.True(gold.IsChildOf(c.Backpack));
        Assert.False(c.Criminal);
    }

    [Fact]
    public void B9_EtherealRiddenByCodeAndDismountedFollowingTheOwner()
    {
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        var ethy = new EtherealHorse();
        c.Backpack.DropItem(ethy);
        var ownerMount = new EtherealHorse();
        owner.Backpack.DropItem(ownerMount);

        // OnThink-style rule: mount when the owner is mounted, dismount when the owner is not.
        void Follow()
        {
            if (owner.Mounted && !c.Mounted)
            {
                var pack = c.Backpack.FindItemByType<EtherealMount>();
                if (pack != null)
                {
                    pack.Rider = c;
                }
            }
            else if (!owner.Mounted && c.Mounted)
            {
                c.Mount.Rider = null;
            }
        }

        ownerMount.Rider = owner;
        Follow();
        _out.WriteLine($"owner mounted: companion mounted={c.Mounted} mount={c.Mount?.GetType().Name} " +
                       $"companion followers={c.Followers} owner followers={owner.Followers}");
        Assert.True(c.Mounted);

        ownerMount.Rider = null;
        Follow();
        _out.WriteLine($"owner dismounted: companion mounted={c.Mounted} ethereal in pack={ethy.IsChildOf(c.Backpack)}");
        Assert.False(c.Mounted);
        Assert.True(ethy.IsChildOf(c.Backpack));

        // The player's path: double-click validates the clicker; a creature caller gets the same checks.
        var validate = ethy.Validate(c);
        _out.WriteLine($"EtherealMount.Validate(companion)={validate}");
    }

    [Fact]
    public void B9_RealMountKeepsItsMasterAndSlotsWhileACompanionRides()
    {
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        var horse = P45.Place(new Horse(), owner.Location, 2, 0);
        horse.SetControlMaster(owner);
        var before = owner.Followers;

        horse.Rider = c;
        _out.WriteLine($"ridden: companion mounted={c.Mounted} horse map={horse.Map} horse master={horse.ControlMaster?.Name} " +
                       $"owner followers {before}->{owner.Followers}");
        Assert.True(c.Mounted);
        Assert.Same(owner, horse.ControlMaster);
        Assert.Equal(before, owner.Followers);

        horse.Rider = null;
        _out.WriteLine($"dismounted: horse map={horse.Map} at={horse.Location} order={horse.ControlOrder} target={horse.ControlTarget?.Name}");
        horse.IssueOrder(OrderType.Follow, owner, owner);
        Assert.Equal(OrderType.Follow, horse.ControlOrder);
        Assert.Equal(owner.Map, horse.Map);

        // A companion riding is not blocked by CheckMountAllowed, which only checks PlayerMobile.
        Assert.True(BaseMount.CheckMountAllowed(c));
    }
}
