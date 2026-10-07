// cc-P45 THROWAWAY PROBE A3: a controlled creature hiding, stealthing, attacking from hiding, picking locks,
// removing traps and poisoning its own weapon. Worktree only; never commit.

using System;
using Server;
using Server.Items;
using Server.Mobiles;
using Server.SkillHandlers;
using Xunit;
using Xunit.Abstractions;

namespace ShatteredLegacy.Tests;

[Collection("Sequential UOContent Tests")]
public class P45RogueProbe
{
    private readonly ITestOutputHelper _out;

    public P45RogueProbe(ITestOutputHelper output) => _out = output;

    private static (PlayerMobile owner, P45ProbeCompanion rogue) Rogue()
    {
        Hiding.Initialize();
        Stealth.Initialize();
        DetectHidden.Initialize();
        RemoveTrap.Initialize();
        Poisoning.Initialize();
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var rogue = P45.Companion(owner);
        P45.Skill(rogue, SkillName.Hiding, 100);
        P45.Skill(rogue, SkillName.Stealth, 100);
        return (owner, rogue);
    }

    private static bool Use(Mobile m, SkillName s)
    {
        m.NextSkillTime = Core.TickCount;
        return m.UseSkill(s);
    }

    [Fact]
    public void A3_HidesAndStealthsWithThePlayerStepCount()
    {
        var (_, rogue) = Rogue();

        Assert.True(Use(rogue, SkillName.Hiding));
        _out.WriteLine($"after Hiding: hidden={rogue.Hidden}");
        Assert.True(rogue.Hidden);

        Assert.True(Use(rogue, SkillName.Stealth));
        _out.WriteLine($"after Stealth: steps={rogue.AllowedStealthSteps} (player formula 100/5 = 20)");
        Assert.Equal(20, rogue.AllowedStealthSteps);
        Assert.True(rogue.Hidden);
    }

    [Fact]
    public void A3_StockCreatureMovementCountsStepsButNeverRestealths()
    {
        var (_, rogue) = Rogue();
        Use(rogue, SkillName.Hiding);
        Use(rogue, SkillName.Stealth);
        var steps = rogue.AllowedStealthSteps;

        // Stock Mobile.OnMove (pinned Mobile.cs:4116-4127): any Player-access mobile counts down, running reveals.
        var walked = 0;
        while (rogue.Hidden && walked < 100)
        {
            rogue.ProbeOnMove(Direction.North);
            walked++;
        }

        _out.WriteLine($"stock OnMove: {steps} steps allowed, revealed on step {walked}");
        Assert.Equal(steps + 1, walked);

        Use(rogue, SkillName.Hiding);
        Use(rogue, SkillName.Stealth);
        rogue.ProbeOnMove(Direction.North | Direction.Running);
        _out.WriteLine($"stock OnMove running: hidden after one running step={rogue.Hidden}");
        Assert.False(rogue.Hidden);

        // Hidden with no Stealth use at all: the first step reveals.
        Use(rogue, SkillName.Hiding);
        rogue.AllowedStealthSteps = 0;
        rogue.ProbeOnMove(Direction.North);
        Assert.False(rogue.Hidden);
    }

    [Fact]
    public void A3_PlayerStepRulesThroughOurOnMoveOverride()
    {
        var (_, rogue) = Rogue();
        rogue.UsePlayerStealthSteps = true;
        Use(rogue, SkillName.Hiding);
        Use(rogue, SkillName.Stealth);

        var walked = 0;
        while (rogue.Hidden && walked < 200)
        {
            rogue.ProbeOnMove(Direction.North);
            walked++;
        }

        _out.WriteLine($"player rules: still hidden after {walked} steps={rogue.Hidden} (re-stealth each 20 at 100 skill)");
        Assert.True(walked > 20, "the override re-runs Stealth.OnUse when steps run out, as PlayerMobile does");

        Use(rogue, SkillName.Hiding);
        Use(rogue, SkillName.Stealth);
        var before = rogue.AllowedStealthSteps;
        rogue.ProbeOnMove(Direction.North | Direction.Running);
        _out.WriteLine($"player rules running: steps {before}->{rogue.AllowedStealthSteps} hidden={rogue.Hidden}");
        Assert.Equal(before - 2, rogue.AllowedStealthSteps);
    }

    [Fact]
    public void A3_RealMoveRunsOnMove()
    {
        var (_, rogue) = Rogue();
        Use(rogue, SkillName.Hiding);
        Use(rogue, SkillName.Stealth);
        var loc = rogue.Location;
        var steps = rogue.AllowedStealthSteps;
        rogue.Direction = Direction.East;
        var moved = rogue.Move(Direction.East);
        _out.WriteLine($"Mobile.Move: moved={moved} {loc}->{rogue.Location} steps {steps}->{rogue.AllowedStealthSteps} " +
                       $"hidden={rogue.Hidden}");
    }

    [Fact]
    public void A3_AttackingFromHidingReveals()
    {
        var (owner, rogue) = Rogue();
        // The live server sets Mobile.DefaultWeapon in Fists.Initialize; the fixture does not (host artifact).
        Mobile.DefaultWeapon ??= new Fists();
        var monster = P45.Place(new Mongbat(), rogue.Location, 1, 0);
        Use(rogue, SkillName.Hiding);
        Assert.True(rogue.Hidden);
        _out.WriteLine($"monster can see hidden companion: {monster.CanSee(rogue)}");

        rogue.IssueOrder(OrderType.Attack, null, monster); // how an owner's "kill" reaches a companion
        _out.WriteLine($"after setting Combatant: hidden={rogue.Hidden}");
        var hiddenAfterCombatant = rogue.Hidden;

        var hp = monster.Hits;
        for (var i = 0; i < 400 && rogue.Hidden; i++)
        {
            ShardTestClock.Advance(TimeSpan.FromMilliseconds(8));
            if (i % 50 == 0)
            {
                var tok = typeof(Mobile).GetField("_combatTimerToken", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic)?.GetValue(rogue);
                _out.WriteLine($"  weapon={(rogue.Weapon as Item)?.GetType().Name} range={rogue.Weapon?.MaxRange} next={rogue.NextCombatTime} now={Core.TickCount} token={tok}");
                _out.WriteLine($"  t={i * 8}ms hidden={rogue.Hidden} combatant={rogue.Combatant?.Name ?? "null"} " +
                               $"order={rogue.ControlOrder} warmode={rogue.Warmode} dist={rogue.GetDistanceToSqrt(monster):F1}");
            }
        }

        _out.WriteLine($"after the first swing: hidden={rogue.Hidden} monster hits {hp}->{monster.Hits}");
        var hiddenAfterSwing = rogue.Hidden;

        // Control: the same companion, not hidden.
        var m2 = P45.Place(new Mongbat(), rogue.Location, 0, 1);
        rogue.Hidden = false;
        rogue.IssueOrder(OrderType.Attack, null, m2);
        var low = m2.Hits;
        for (var i = 0; i < 400; i++)
        {
            ShardTestClock.Advance(TimeSpan.FromMilliseconds(8));
            low = Math.Min(low, m2.Hits);
        }
        _out.WriteLine($"control, visible attacker: m2 lowest {low}/{m2.HitsMax} deleted={m2.Deleted} combatant={rogue.Combatant?.Name}");
        Assert.False(hiddenAfterSwing);
    }

    [Fact]
    public void A3_MonsterAiDetectHiddenIgnoresAHiddenCreatureButNotAPlayer()
    {
        var (owner, rogue) = Rogue();
        var monster = P45.Place(new Ratman(), rogue.Location, 2, 0);
        P45.Skill(monster, SkillName.DetectHidden, 100);

        var player = P45.Owner(new Point3D(rogue.X, rogue.Y + 1, rogue.Z));
        P45.Skill(player, SkillName.Hiding, 100);
        P45.Skill(player, SkillName.Stealth, 100);

        int creatureRevealed = 0, playerRevealed = 0;
        for (var i = 0; i < 60; i++)
        {
            rogue.Hidden = true;
            player.Hidden = true;
            monster.AIObject.DetectHidden();
            creatureRevealed += rogue.Hidden ? 0 : 1;
            playerRevealed += player.Hidden ? 0 : 1;
        }

        _out.WriteLine($"monster AI detect hidden x60: creature revealed {creatureRevealed}, player revealed {playerRevealed}");
        Assert.Equal(0, creatureRevealed);
        Assert.True(playerRevealed > 0);
    }

    [Fact]
    public void A3_PlayerDetectHiddenRevealsAHiddenCompanion()
    {
        var (owner, rogue) = Rogue();
        var detector = P45.Owner(new Point3D(rogue.X + 2, rogue.Y, rogue.Z));
        P45.Skill(detector, SkillName.DetectHidden, 100);

        var revealed = 0;
        for (var i = 0; i < 40; i++)
        {
            rogue.Hidden = true;
            Use(detector, SkillName.DetectHidden);
            detector.Target.Invoke(detector, detector);
            revealed += rogue.Hidden ? 0 : 1;
        }

        _out.WriteLine($"player detect hidden x40 against Hiding 100: revealed {revealed}");
        Assert.True(revealed > 0);
    }

    [Fact]
    public void A3_PicksALockWithALockpick()
    {
        var (_, rogue) = Rogue();
        P45.Skill(rogue, SkillName.Lockpicking, 100);
        var chest = new MetalChest { Locked = true, LockLevel = 50, MaxLockLevel = 90, RequiredSkill = 50 };
        chest.MoveToWorld(new Point3D(rogue.X + 1, rogue.Y, rogue.Z), rogue.Map);
        var pick = new Lockpick(5);
        rogue.Backpack.DropItem(pick);

        pick.OnDoubleClick(rogue);
        Assert.NotNull(rogue.Target);
        rogue.Target.Invoke(rogue, chest);
        ShardTestClock.Advance(TimeSpan.FromSeconds(3.1));

        _out.WriteLine($"lockpick: locked={chest.Locked} picker={chest.Picker?.Name}");
        Assert.False(chest.Locked);
        Assert.Same(rogue, chest.Picker);
    }

    [Fact]
    public void A3_RemovesATrap()
    {
        var (_, rogue) = Rogue();
        P45.Skill(rogue, SkillName.Lockpicking, 100);
        P45.Skill(rogue, SkillName.DetectHidden, 100);
        P45.Skill(rogue, SkillName.RemoveTrap, 100);
        var chest = new MetalChest { TrapType = TrapType.ExplosionTrap, TrapPower = 50, TrapLevel = 2 };
        chest.MoveToWorld(new Point3D(rogue.X + 1, rogue.Y, rogue.Z), rogue.Map);
        var hits = rogue.Hits;

        Assert.True(Use(rogue, SkillName.RemoveTrap));
        Assert.NotNull(rogue.Target);
        rogue.Target.Invoke(rogue, chest);

        _out.WriteLine($"remove trap: trap={chest.TrapType} power={chest.TrapPower} rogue hits {hits}->{rogue.Hits}");
        Assert.Equal(TrapType.None, chest.TrapType);
    }

    [Fact]
    public void A3_PoisonsItsOwnDagger()
    {
        var (_, rogue) = Rogue();
        P45.Skill(rogue, SkillName.Poisoning, 100);
        var dagger = new Dagger();
        rogue.Backpack.DropItem(dagger);
        var potion = new GreaterPoisonPotion();
        rogue.Backpack.DropItem(potion);

        Assert.True(Use(rogue, SkillName.Poisoning));
        rogue.Target.Invoke(rogue, potion);
        Assert.NotNull(rogue.Target);
        rogue.Target.Invoke(rogue, dagger);
        ShardTestClock.Advance(TimeSpan.FromSeconds(2.1));

        _out.WriteLine($"poisoning: dagger poison={dagger.Poison?.Name} charges={dagger.PoisonCharges} karma={rogue.Karma}");
        Assert.Equal(Poison.Greater, dagger.Poison);
        Assert.True(dagger.PoisonCharges > 0);
    }
}
