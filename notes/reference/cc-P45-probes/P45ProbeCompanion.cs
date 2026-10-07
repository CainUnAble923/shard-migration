// cc-P45 THROWAWAY PROBE. Lives only in the D:\SL-probe-companions worktree. Never commit, never merge.
//
// A minimal companion stand-in: a BaseCreature with a human body, controlled by a test player,
// no SetDamage, a player-sized Skills.Cap, and a ForcedAI hook each probe can swap.

using System;
using System.Collections.Generic;
using ModernUO.Serialization;
using Server.Items;

namespace Server.Mobiles;

[SerializationGenerator(0, false)]
public partial class P45ProbeCompanion : BaseCreature
{
    // Swapped per probe. Read by ForcedAI, which the base constructor reads first.
    public static Func<P45ProbeCompanion, BaseAI> AIFactory;

    [Constructible]
    public P45ProbeCompanion() : base(AIType.AI_Melee, FightMode.Aggressor)
    {
        Name = "probe companion";
        Body = 0x190;
        Hue = Race.Human.RandomSkinHue();

        SetStr(100);
        SetDex(100);
        SetInt(100);
        SetHits(150);
        SetStam(100);
        SetMana(100);

        // Never SetDamage: a companion uses its weapon's dice (P41 2.3).
        Skills.Cap = 100000;

        AddItem(new Backpack { Movable = false });
    }

    // Probe switches. Not serialized: the probes set them per test.
    public bool FightBackWhileFollowing { get; set; }

    public bool UsePlayerStealthSteps { get; set; }

    public bool PlotArmor { get; set; }

    public int OnBeforeDeathCalls { get; private set; }

    protected override BaseAI ForcedAI => AIFactory?.Invoke(this);

    public override bool StandsDownOnCommand => !FightBackWhileFollowing && base.StandsDownOnCommand;

    // Ours: server/patches/BaseCreature-PlayerMobile-can-auto-stable.patch
    public override bool CanAutoStable => false;

    public bool ProbeOnMove(Direction d) => OnMove(d);

    // PlayerMobile.OnMove (pinned PlayerMobile.cs:3408-3440) copied as the seam a companion would use.
    protected override bool OnMove(Direction d)
    {
        if (!UsePlayerStealthSteps)
        {
            return base.OnMove(d);
        }

        if (Hidden)
        {
            if (!Mounted && Skills.Stealth.Value >= 25.0)
            {
                var running = (d & Direction.Running) != 0;

                if (running)
                {
                    if ((AllowedStealthSteps -= 2) <= 0)
                    {
                        RevealingAction();
                    }
                }
                else if (AllowedStealthSteps-- <= 0)
                {
                    Server.SkillHandlers.Stealth.OnUse(this);
                }
            }
            else
            {
                RevealingAction();
            }
        }

        return true;
    }

    // Penitent (a), Wrath of the Wounded: up to +30% at 25% health.
    public double WrathMax { get; set; }

    public int WrathScale(int damage)
    {
        if (WrathMax <= 0 || HitsMax <= 0)
        {
            return damage;
        }

        var missing = 1.0 - (double)Hits / HitsMax;
        var t = Math.Clamp(missing / 0.75, 0.0, 1.0);
        return (int)(damage * (1.0 + WrathMax * t));
    }

    public override void AlterMeleeDamageTo(Mobile to, ref int damage) => damage = WrathScale(damage);

    public override void AlterSpellDamageTo(Mobile to, ref int damage) => damage = WrathScale(damage);

    // Penitent (b), Shared Burden: siblings route a share of their damage to the Penitent.
    public static readonly Dictionary<Mobile, P45ProbeCompanion> Penitents = new();

    public double BurdenShare { get; set; }

    public override void Damage(int amount, Mobile from = null, bool informMount = true, bool ignoreEvilOmen = false)
    {
        var master = ControlMaster;

        if (master != null && Penitents.TryGetValue(master, out var penitent) && penitent != this &&
            penitent.Alive && penitent.InRange(this, 12) && penitent.BurdenShare > 0)
        {
            var moved = (int)(amount * penitent.BurdenShare);
            amount -= moved;
            penitent.Damage(moved, from, informMount, ignoreEvilOmen);
        }

        base.Damage(amount, from, informMount, ignoreEvilOmen);
    }

    // Penitent (c) and Otherworlder (a): cheat death, sharing one cooldown per owner (probe 13).
    public static readonly Dictionary<Mobile, DateTime> CheatDeathReadyAt = new();

    public static TimeSpan CheatDeathCooldown = TimeSpan.FromHours(1);

    public bool LastRites { get; set; }

    public static List<Mobile> PartyOf(Mobile owner)
    {
        var list = new List<Mobile> { owner };

        if (owner is PlayerMobile pm && pm.AllFollowers != null)
        {
            foreach (var f in pm.AllFollowers)
            {
                list.Add(f);
            }
        }

        return list;
    }

    public override bool OnBeforeDeath()
    {
        OnBeforeDeathCalls++;

        if ((PlotArmor || LastRites) && ControlMaster is { } owner)
        {
            CheatDeathReadyAt.TryGetValue(owner, out var readyAt);

            if (Core.Now >= readyAt)
            {
                CheatDeathReadyAt[owner] = Core.Now + CheatDeathCooldown;
                Hits = 1;

                if (PlotArmor)
                {
                    Blessed = true;
                    Timer.StartTimer(TimeSpan.FromSeconds(3), () => Blessed = false);
                }

                if (LastRites)
                {
                    foreach (var m in PartyOf(owner))
                    {
                        if (m != this && m.Alive)
                        {
                            m.Heal(m.HitsMax, this, false);
                        }
                    }
                }

                return false;
            }
        }

        return base.OnBeforeDeath();
    }
}

// Probe 4: fight back while following, defending the owner and sibling companions.
public class P45ProbeFollowAI : MeleeAI
{
    public P45ProbeFollowAI(BaseCreature m) : base(m)
    {
    }

    public Mobile LastThreat { get; private set; }

    public Mobile FindPartyThreat()
    {
        var master = Mobile.ControlMaster;

        if (master == null)
        {
            return null;
        }

        Mobile best = null;
        var bestDist = double.MaxValue;

        foreach (var m in Mobile.GetMobilesInRange(Mobile.RangePerception))
        {
            if (IsGuardAlly(m) || !m.Alive || m.IsDeadBondedPet)
            {
                continue;
            }

            var c = m.Combatant;

            if (c == null || !(c == Mobile || c == master ||
                               c is BaseCreature { ControlMaster: { } cm } && cm == master))
            {
                continue;
            }

            var dist = m.GetDistanceToSqrt(master);

            if (dist < bestDist && Mobile.CanSee(m) && Mobile.InLOS(m))
            {
                best = m;
                bestDist = dist;
            }
        }

        return best;
    }

    public override bool DoOrderFollow()
    {
        var threat = FindPartyThreat();
        LastThreat = threat;

        if (threat != null)
        {
            Mobile.Combatant = threat;
            Mobile.FocusMob = threat;
            Action = ActionType.Combat;
            Think();
            return true;
        }

        return base.DoOrderFollow();
    }

    public override bool DoOrderGuard()
    {
        var threat = FindPartyThreat();
        LastThreat = threat;

        if (threat != null)
        {
            Mobile.Combatant = threat;
            Mobile.FocusMob = threat;
            Action = ActionType.Combat;
            Think();
            return true;
        }

        return base.DoOrderGuard();
    }
}

// Probe 7: the owner's cursor, the companion's target.
public class P45RelayTarget : Server.Targeting.Target
{
    private readonly Mobile _companion;

    public P45RelayTarget(Mobile companion) : base(-1, true, Server.Targeting.TargetFlags.None) =>
        _companion = companion;

    protected override void OnTarget(Mobile from, object targeted) => _companion.Target?.Invoke(_companion, targeted);
}
