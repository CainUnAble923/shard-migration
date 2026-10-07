// cc-P45 THROWAWAY PROBES B10 (transformation spells) and C11-C13 (Penitent, Otherworlder, shared cheat-death
// cooldown). Worktree only; never commit.

using System;
using Server;
using Server.Mobiles;
using Server.Spells;
using Server.Spells.Necromancy;
using Xunit;
using Xunit.Abstractions;

namespace ShatteredLegacy.Tests;

[Collection("Sequential UOContent Tests")]
public class P45BranchProbe
{
    private readonly ITestOutputHelper _out;

    public P45BranchProbe(ITestOutputHelper output) => _out = output;

    private void CastAndWait(Spell spell, Mobile caster, string label)
    {
        var body = caster.BodyMod;
        var cast = spell.Cast();
        for (var i = 0; i < 1000 && caster.Spell != null; i++)
        {
            ShardTestClock.Advance(TimeSpan.FromMilliseconds(8));
        }

        _out.WriteLine($"{label}: cast={cast} BodyMod {body}->{caster.BodyMod} HueMod={caster.HueMod} " +
                       $"context={TransformationSpellHelper.GetContext(caster)?.Type.Name ?? "none"}");
    }

    [Fact]
    public void B10_CreatureCastsNecromancyTransformations()
    {
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        P45.Skill(c, SkillName.Necromancy, 120);
        P45.Skill(c, SkillName.SpiritSpeak, 120);
        c.Mana = c.ManaMax;

        CastAndWait(new WraithFormSpell(c), c, "Wraith Form");
        Assert.True(TransformationSpellHelper.UnderTransformation(c, typeof(WraithFormSpell)));
        Assert.NotEqual(0, (int)c.BodyMod);

        c.Mana = c.ManaMax;
        c.NextSpellTime = Core.TickCount;
        CastAndWait(new LichFormSpell(c), c, "Lich Form");
        Assert.True(TransformationSpellHelper.UnderTransformation(c, typeof(LichFormSpell)));

        c.Mana = c.ManaMax;
        c.NextSpellTime = Core.TickCount;
        CastAndWait(new LichFormSpell(c), c, "Lich Form again (toggles off)");
        Assert.Equal(0, (int)c.BodyMod);
    }

    [Fact]
    public void C11a_WrathOfTheWoundedScalesMeleeAndSpellDamageDealt()
    {
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        c.WrathMax = 0.30;
        var target = P45.Place(new Ratman(), owner.Location, 2, 0);

        c.Hits = c.HitsMax;
        var d = 100;
        c.AlterMeleeDamageTo(target, ref d);
        var full = d;
        c.Hits = c.HitsMax / 4;
        d = 100;
        c.AlterMeleeDamageTo(target, ref d);
        var quarter = d;
        _out.WriteLine($"wrath: 100 at full health -> {full}, at 25% -> {quarter}");
        Assert.Equal(100, full);
        Assert.Equal(130, quarter);
    }

    [Fact]
    public void C11b_SharedBurdenMovesSiblingDamageButCannotTouchAPlayer()
    {
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var penitent = P45.Companion(owner);
        var sibling = P45.Companion(owner, 0, 1);
        penitent.BurdenShare = 0.15;
        P45ProbeCompanion.Penitents[owner] = penitent;
        var attacker = P45.Place(new Ratman(), owner.Location, 2, 0);

        try
        {
            int pBefore = penitent.Hits, sBefore = sibling.Hits, oBefore = owner.Hits;
            sibling.Damage(40, attacker);
            var pAfter = penitent.Hits;
            var sAfter = sibling.Hits;
            owner.Damage(40, attacker);
            var oAfter = owner.Hits;
            var pAfterOwner = penitent.Hits;
            _out.WriteLine($"sibling hit 40: sibling {sBefore}->{sAfter}, penitent {pBefore}->{pAfter}; " +
                           $"owner hit 40: owner {oBefore}->{oAfter}, penitent {pAfter}->{pAfterOwner}");
            Assert.Equal(sBefore - 34, sAfter);
            Assert.Equal(pBefore - 6, pAfter);
            Assert.Equal(oBefore - 40, oAfter);
            Assert.Equal(pAfter, pAfterOwner);
        }
        finally
        {
            P45ProbeCompanion.Penitents.Remove(owner);
        }
    }

    [Fact]
    public void C11c_C12a_C13_CheatDeathOnceAndOneCooldownPerParty()
    {
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var penitent = P45.Companion(owner);
        var hero = P45.Companion(owner, 0, 1);
        var other = P45.Companion(owner, 1, 1);
        penitent.LastRites = true;
        hero.PlotArmor = true;
        P45ProbeCompanion.CheatDeathReadyAt.Remove(owner);
        var attacker = P45.Place(new Ratman(), owner.Location, 2, 0);

        other.Hits = 10;
        owner.Hits = 10;
        penitent.Damage(penitent.Hits + 50, attacker);
        _out.WriteLine($"penitent killing blow: alive={penitent.Alive} hits={penitent.Hits} deadPet={penitent.IsDeadPet} " +
                       $"party healed: owner {owner.Hits}/{owner.HitsMax} other {other.Hits}/{other.HitsMax}");
        Assert.True(penitent.Alive);
        Assert.False(penitent.IsDeadPet);
        Assert.Equal(1, penitent.Hits);
        Assert.Equal(owner.HitsMax, owner.Hits);
        Assert.Equal(other.HitsMax, other.Hits);

        // Same party, cooldown shared: the Hero's plot armor does not fire now.
        hero.Damage(hero.Hits + 50, attacker);
        _out.WriteLine($"hero killing blow inside the shared cooldown: deadPet={hero.IsDeadPet}");
        Assert.True(hero.IsDeadPet);

        // After the cooldown the next one fires, with the invulnerability window.
        P45ProbeCompanion.CheatDeathReadyAt[owner] = Core.Now;
        var hero2 = P45.Companion(owner, -1, 0);
        hero2.PlotArmor = true;
        hero2.Damage(hero2.Hits + 50, attacker);
        var blessed = hero2.Blessed;
        hero2.Damage(30, attacker);
        _out.WriteLine($"hero2 plot armor: alive={!hero2.IsDeadPet} hits={hero2.Hits} blessed={blessed}");
        Assert.False(hero2.IsDeadPet);
        Assert.True(blessed);
        Assert.Equal(1, hero2.Hits);
        ShardTestClock.AdvanceSeconds(3.1);
        Assert.False(hero2.Blessed);
    }

    [Fact]
    public void C12b_PartyBuffByCompanionCountReachesPlayersAndCreatures()
    {
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var a = P45.Companion(owner);
        var b = P45.Companion(owner, 0, 1);
        var count = owner.AllFollowers.Count;
        var str = owner.Str;
        var phys = owner.PhysicalResistance;

        foreach (var m in P45ProbeCompanion.PartyOf(owner))
        {
            m.AddStatMod(new StatMod(StatType.Str, "PowerOfFriendship", 2 * count, TimeSpan.FromMinutes(1)));
            m.AddResistanceMod(new ResistanceMod(ResistanceType.Physical, "PowerOfFriendship", count));
        }

        _out.WriteLine($"friendship x{count}: owner str {str}->{owner.Str} phys {phys}->{owner.PhysicalResistance}; " +
                       $"companion str {a.RawStr}->{a.Str}");
        Assert.Equal(str + 2 * count, owner.Str);
        Assert.Equal(phys + count, owner.PhysicalResistance);
        Assert.Equal(a.RawStr + 2 * count, a.Str);
    }
}
