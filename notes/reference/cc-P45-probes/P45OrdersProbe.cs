// cc-P45 THROWAWAY PROBES B4 and B7: fight back while following, and the master's cursor relayed to the
// companion's spell. Worktree only; never commit.

using System;
using Server;
using Server.Mobiles;
using Server.Spells.Third;
using Xunit;
using Xunit.Abstractions;

namespace ShatteredLegacy.Tests;

[Collection("Sequential UOContent Tests")]
public class P45OrdersProbe
{
    private readonly ITestOutputHelper _out;

    public P45OrdersProbe(ITestOutputHelper output) => _out = output;

    [Fact]
    public void B4_StockFollowingCompanionIgnoresAnAttackOnItsOwner()
    {
        P45ProbeCompanion.AIFactory = null;
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        var monster = P45.Place(new Ratman(), owner.Location, 2, 0);
        monster.Combatant = owner;

        c.AIObject.Obey();
        _out.WriteLine($"stock follow, owner attacked: companion combatant={c.Combatant?.Name ?? "null"} order={c.ControlOrder}");
        Assert.Null(c.Combatant);

        monster.Combatant = c;
        c.AIObject.Obey();
        _out.WriteLine($"stock follow, companion attacked: combatant={c.Combatant?.Name ?? "null"} order={c.ControlOrder} " +
                       $"StandsDown={c.StandsDownOnCommand}");
        Assert.Null(c.Combatant);
    }

    [Fact]
    public void B4_ForcedAiFollowDefendsOwnerSiblingAndSelf()
    {
        P45ProbeCompanion.AIFactory = m => new P45ProbeFollowAI(m);
        try
        {
            ShardTestClock.Arm();
            var owner = P45.Owner(P45.NextSpot());
            var c = P45.Companion(owner);
            var sibling = P45.Companion(owner, 0, 1);
            Assert.IsType<P45ProbeFollowAI>(c.AIObject);

            var m1 = P45.Place(new Ratman(), owner.Location, 3, 0);
            m1.Combatant = owner;
            c.AIObject.Obey();
            _out.WriteLine($"owner attacked: combatant={c.Combatant?.GetType().Name} order={c.ControlOrder}");
            Assert.Same(m1, c.Combatant);
            Assert.Equal(OrderType.Follow, c.ControlOrder);

            m1.Delete();
            c.Combatant = null;
            var m2 = P45.Place(new Ratman(), owner.Location, -3, 0);
            m2.Combatant = sibling;
            c.AIObject.Obey();
            _out.WriteLine($"sibling attacked: combatant={c.Combatant?.GetType().Name} order={c.ControlOrder}");
            Assert.Same(m2, c.Combatant);

            m2.Delete();
            c.Combatant = null;
            var m3 = P45.Place(new Ratman(), owner.Location, 0, -3);
            m3.Combatant = c;
            c.AIObject.Obey();
            _out.WriteLine($"self attacked: combatant={c.Combatant?.GetType().Name} order={c.ControlOrder}");
            Assert.Same(m3, c.Combatant);

            // Guard: pinned FindGuardTarget covers master and self only; our DoOrderGuard adds siblings.
            m3.Delete();
            c.Combatant = null;
            c.IssueOrder(OrderType.Guard, owner, owner);
            var m4 = P45.Place(new Ratman(), owner.Location, 3, 3);
            m4.Combatant = sibling;
            c.AIObject.Obey();
            _out.WriteLine($"guard, sibling attacked: combatant={c.Combatant?.GetType().Name} order={c.ControlOrder}");
            Assert.Same(m4, c.Combatant);
        }
        finally
        {
            P45ProbeCompanion.AIFactory = null;
        }
    }

    [Fact]
    public void B4_StockGuardDoesNotDefendASibling()
    {
        P45ProbeCompanion.AIFactory = null;
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        var sibling = P45.Companion(owner, 0, 1);
        c.IssueOrder(OrderType.Guard, owner, owner);
        var m = P45.Place(new Ratman(), owner.Location, 3, 3);
        m.Combatant = sibling;
        c.AIObject.Obey();
        _out.WriteLine($"stock guard, sibling attacked: combatant={c.Combatant?.GetType().Name ?? "null"}");
        Assert.Null(c.Combatant);
    }

    [Fact]
    public void B4_StandsDownOffMakesAFollowingCompanionAnswerADirectAttack()
    {
        P45ProbeCompanion.AIFactory = null;
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        c.FightBackWhileFollowing = true;
        var m = P45.Place(new Ratman(), owner.Location, 2, 0);
        m.Combatant = c;
        _out.WriteLine($"StandsDownOnCommand=false, attacked: order={c.ControlOrder} target={c.ControlTarget?.GetType().Name} " +
                       $"combatant={c.Combatant?.GetType().Name}");
        Assert.Equal(OrderType.Attack, c.ControlOrder);
    }

    [Fact]
    public void B7_MasterCursorRelayRunsRangeFromTheCompanion()
    {
        P45ProbeCompanion.AIFactory = null;
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        P45.Skill(c, SkillName.Magery, 100);
        P45.Skill(c, SkillName.EvalInt, 100);
        c.Mana = c.ManaMax;

        // c stands 1 east of the owner. Near: 10 east of the owner (9 from c). Far from c, near the owner: 5 west.
        c.MoveToWorld(new Point3D(owner.X + 9, owner.Y, owner.Z), owner.Map);
        c.IssueOrder(OrderType.Stay, null, null); // or it walks back to its owner while the spell is cast
        var near = P45.Place(new Ratman(), owner.Location, 14, 0);   // 5 from c, 14 from the owner
        var far = P45.Place(new Ratman(), owner.Location, -5, 0);    // 14 from c, 5 from the owner
        near.Hits = near.HitsMax;
        far.Hits = far.HitsMax;

        int Cast(Mobile target)
        {
            var hits = target.Hits;
            var spell = new FireballSpell(c);
            var cast = spell.Cast();
            for (var i = 0; i < 1000 && c.Target == null; i++)
            {
                ShardTestClock.Advance(TimeSpan.FromMilliseconds(8));
            }

            _out.WriteLine($"cast={cast} companion target={c.Target?.GetType().FullName}");
            Assert.NotNull(c.Target);

            _out.WriteLine($"at the pick: companion->target {c.GetDistanceToSqrt(target):F1}, owner->target " +
                           $"{owner.GetDistanceToSqrt(target):F1}");
            owner.Target = new P45RelayTarget(c);
            owner.Target.Invoke(owner, target);

            // Keep the lowest reading: the test host regenerates a hit every 8 ms (ShardTestClock, Q-060).
            var lowest = target.Hits;
            for (var i = 0; i < 400; i++)
            {
                ShardTestClock.Advance(TimeSpan.FromMilliseconds(8));
                lowest = Math.Min(lowest, target.Hits);
            }

            return hits - lowest;
        }

        var nearDamage = Cast(near);
        _out.WriteLine($"near the companion, far from the owner: damage={nearDamage} (hits {near.Hits}/{near.HitsMax})");
        c.Mana = c.ManaMax;
        c.NextSpellTime = Core.TickCount;
        ShardTestClock.AdvanceSeconds(2);
        var farDamage = Cast(far);
        _out.WriteLine($"far from the companion, near the owner: damage={farDamage}");

        Assert.True(nearDamage > 0, "the companion's spell landed on a target out of the owner's range");
        Assert.True(farDamage <= 0, "the companion's range, not the owner's, refused the far target");
    }
}
