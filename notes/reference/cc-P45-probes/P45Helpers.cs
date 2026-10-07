// cc-P45 THROWAWAY PROBE helpers. Worktree only; never commit.

using Server;
using Server.Items;
using Server.Mobiles;

namespace ShatteredLegacy.Tests;

internal static class P45
{
    public static int Spot;

    // Each fact gets its own patch of ground so mobiles from earlier facts are out of range.
    public static Point3D NextSpot()
    {
        Spot++;
        return new Point3D(1000 + Spot * 40 % 2000, 1000 + Spot * 40 / 2000 * 40, 0);
    }

    // The live server registers poisons in PoisonKinds.Configure (pinned UOContent/Misc/PoisonKinds.cs:75-84);
    // the test fixture does not, so Poison.Lesser and friends are null in the host until this runs.
    public static void EnsurePoisons()
    {
        if (Poison.Poisons.Count == 0)
        {
            PoisonKinds.Configure();
        }
    }

    public static PlayerMobile Owner(Point3D at, Map map = null)
    {
        EnsurePoisons();
        var pm = new PlayerMobile { Player = true, FollowersMax = 15, Name = "owner" };
        pm.RawStr = 100;
        pm.RawDex = 100;
        pm.RawInt = 100;
        pm.AddItem(new Backpack());
        pm.MoveToWorld(at, map ?? Map.Trammel);
        pm.Hits = pm.HitsMax;
        return pm;
    }

    public static P45ProbeCompanion Companion(PlayerMobile owner, int dx = 1, int dy = 0)
    {
        var c = new P45ProbeCompanion();
        c.MoveToWorld(new Point3D(owner.X + dx, owner.Y + dy, owner.Z), owner.Map);
        c.SetControlMaster(owner);
        c.IsBonded = true;
        c.IssueOrder(OrderType.Follow, owner, owner);
        return c;
    }

    public static void Skill(Mobile m, SkillName s, double v)
    {
        m.Skills[s].Cap = 120.0;
        m.Skills[s].Base = v;
    }

    public static T Place<T>(T m, Point3D near, int dx, int dy, Map map = null) where T : Mobile
    {
        m.MoveToWorld(new Point3D(near.X + dx, near.Y + dy, near.Z), map ?? Map.Trammel);
        return m;
    }
}
