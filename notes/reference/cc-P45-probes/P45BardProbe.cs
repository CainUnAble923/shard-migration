// cc-P45 THROWAWAY PROBE A2: a controlled creature as a bard through the real skill handlers. Worktree only.

using System;
using Server;
using Server.Items;
using Server.Mobiles;
using Server.SkillHandlers;
using Xunit;
using Xunit.Abstractions;

namespace ShatteredLegacy.Tests;

[Collection("Sequential UOContent Tests")]
public class P45BardProbe
{
    private readonly ITestOutputHelper _out;

    public P45BardProbe(ITestOutputHelper output) => _out = output;

    private static void Handlers()
    {
        // The real server reaches these through AssemblyHandler.Invoke("Initialize"); the fixture does not.
        Peacemaking.Initialize();
        Provocation.Initialize();
        Discordance.Initialize();
    }

    private static (PlayerMobile owner, P45ProbeCompanion bard, Lute lute) Bard(double skill, double music)
    {
        Handlers();
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var bard = P45.Companion(owner);
        P45.Skill(bard, SkillName.Musicianship, music);
        P45.Skill(bard, SkillName.Peacemaking, skill);
        P45.Skill(bard, SkillName.Provocation, skill);
        P45.Skill(bard, SkillName.Discordance, skill);
        var lute = new Lute();
        bard.Backpack.DropItem(lute);
        BaseInstrument.SetInstrument(bard, lute);
        return (owner, bard, lute);
    }

    private static bool Use(Mobile m, SkillName s)
    {
        m.NextSkillTime = Core.TickCount;
        return m.UseSkill(s);
    }

    [Fact]
    public void A2_TargetedPeacemakingOnAMonster()
    {
        var (owner, bard, _) = Bard(120, 120);
        var monster = P45.Place(new Mongbat(), owner.Location, 3, 0);
        monster.Combatant = owner;
        Assert.True(monster.Warmode || monster.Combatant != null);

        Assert.True(Use(bard, SkillName.Peacemaking), "UseSkill reached the handler");
        _out.WriteLine($"target after UseSkill: {bard.Target?.GetType().FullName}");
        Assert.NotNull(bard.Target);
        bard.Target.Invoke(bard, monster);

        _out.WriteLine($"mongbat: pacified={monster.BardPacified} combatant={monster.Combatant?.Name ?? "null"} " +
                       $"until={monster.BardEndTime - Core.Now}");
        Assert.True(monster.BardPacified);
        Assert.Null(monster.Combatant);
    }

    [Fact]
    public void A2_AreaPeacemakingAlsoCalmsTheOwnerAndSiblings()
    {
        var (owner, bard, _) = Bard(120, 120);
        var sibling = P45.Companion(owner, 0, 1);
        var monster = P45.Place(new Mongbat(), owner.Location, 3, 0);
        owner.Warmode = true;
        owner.Combatant = monster;
        sibling.Warmode = true;
        sibling.Combatant = monster;

        Use(bard, SkillName.Peacemaking);
        bard.Target.Invoke(bard, bard); // targeting self is area mode

        _out.WriteLine($"area peace: owner combatant={owner.Combatant?.Name ?? "null"} warmode={owner.Warmode}; " +
                       $"sibling combatant={sibling.Combatant?.Name ?? "null"} pacified={sibling.BardPacified}; " +
                       $"monster pacified={monster.BardPacified}");
        Assert.True(monster.BardPacified);
        // The stock area mode does not spare the party: this is the finding, not a wish.
        Assert.Null(owner.Combatant);
        Assert.False(owner.Warmode);
        Assert.True(sibling.BardPacified);
    }

    [Fact]
    public void A2_ProvokesOneMonsterOntoAnother()
    {
        var (owner, bard, _) = Bard(120, 120);
        var a = P45.Place(new Mongbat(), owner.Location, 3, 0);
        var b = P45.Place(new Ratman(), owner.Location, 4, 1);

        Use(bard, SkillName.Provocation);
        Assert.NotNull(bard.Target);
        bard.Target.Invoke(bard, a);
        _out.WriteLine($"second target: {bard.Target?.GetType().Name}");
        Assert.NotNull(bard.Target);
        bard.Target.Invoke(bard, b);

        _out.WriteLine($"provoke: a.provoked={a.BardProvoked} a.combatant={a.Combatant?.GetType().Name} " +
                       $"a.BardMaster={a.BardMaster?.Name} b.combatant={b.Combatant?.GetType().Name}");
        Assert.True(a.BardProvoked);
        Assert.Same(b, a.Combatant);
    }

    [Fact]
    public void A2_ProvocationRefusesPlayersAndPets()
    {
        var (owner, bard, _) = Bard(120, 120);
        var a = P45.Place(new Mongbat(), owner.Location, 3, 0);
        var sibling = P45.Companion(owner, 0, 1);

        Use(bard, SkillName.Provocation);
        bard.Target.Invoke(bard, owner);
        _out.WriteLine($"provoke the owner: next target={bard.Target?.GetType().Name ?? "none"}");
        Assert.Null(bard.Target);

        Use(bard, SkillName.Provocation);
        bard.Target.Invoke(bard, a);
        bard.Target.Invoke(bard, sibling);
        _out.WriteLine($"provoke onto sibling pet: a.provoked={a.BardProvoked} a.combatant={a.Combatant?.Name}");
    }

    [Fact]
    public void A2_DiscordsAMonsterAndRefusesAPlayer()
    {
        var (owner, bard, _) = Bard(120, 120);
        var monster = P45.Place(new Ratman(), owner.Location, 3, 0);
        var res = monster.PhysicalResistance;

        Use(bard, SkillName.Discordance);
        Assert.NotNull(bard.Target);
        bard.Target.Invoke(bard, monster);
        var effect = 0;
        var discorded = Discordance.GetEffect(monster, ref effect);
        _out.WriteLine($"discord: effect={effect} phys {res}->{monster.PhysicalResistance}");
        Assert.True(discorded);
        Assert.True(monster.PhysicalResistance < res);

        var other = P45.Owner(new Point3D(owner.X + 2, owner.Y, owner.Z));
        Use(bard, SkillName.Discordance);
        bard.Target.Invoke(bard, other);
        effect = 0;
        Assert.False(Discordance.GetEffect(other, ref effect));
    }

    [Fact]
    public void A2_MusicianshipAndBardSkillsGainForACompanion()
    {
        var (owner, bard, lute) = Bard(50, 50);
        lute.UsesRemaining = 10000;
        var pm0 = bard.Skills.Musicianship.Base;
        var pe0 = bard.Skills.Peacemaking.Base;
        var di0 = bard.Skills.Discordance.Base;

        for (var i = 0; i < 80; i++)
        {
            Use(bard, SkillName.Peacemaking);
            bard.Target?.Invoke(bard, bard);
        }

        for (var i = 0; i < 80; i++)
        {
            var m = P45.Place(new Ettin(), owner.Location, 3, 0);
            if (i == 0)
            {
                var diff = lute.GetDifficultyFor(m) - 10.0;
                _out.WriteLine($"ettin discord range {diff - 25:F1}..{diff + 25:F1}");
            }

            Use(bard, SkillName.Discordance);
            bard.Target?.Invoke(bard, m);
            m.Delete();
        }

        _out.WriteLine($"gains: Musicianship {pm0}->{bard.Skills.Musicianship.Base} Peacemaking {pe0}->" +
                       $"{bard.Skills.Peacemaking.Base} Discordance {di0}->{bard.Skills.Discordance.Base}");
        Assert.True(bard.Skills.Musicianship.Base > pm0);
        Assert.True(bard.Skills.Peacemaking.Base > pe0);
        Assert.True(bard.Skills.Discordance.Base > di0);
    }
}
