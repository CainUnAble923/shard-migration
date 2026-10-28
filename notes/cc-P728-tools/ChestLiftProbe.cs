using System;
using Server;
using Server.Accounting;
using Server.Items;
using Server.Mobiles;
using Server.Tests.Network;
using Server.Tutorial;
using Xunit;
using Xunit.Abstractions;

namespace ShatteredLegacy.Tests;

[Collection("Sequential UOContent Tests")]
public class ChestLiftProbe
{
    private readonly ITestOutputHelper _out;
    public ChestLiftProbe(ITestOutputHelper o) => _out = o;

    [Fact]
    public void LiftAndEquipFromTheChest()
    {
        ShardTestHost.EnsureAccounts();
        var acct = new Account($"probe{Guid.NewGuid():N}"[..16], "probe-only");
        var pm = new PlayerMobile { Player = true, Race = Race.Human, Body = 0x190, Name = "Probe", RawStr = 60, RawDex = 60, RawInt = 60 };
        pm.AddItem(new Backpack());
        acct[0] = pm;
        pm.MoveToWorld(new Point3D(1000, 1000, 0), Map.Trammel);
        var ns = PacketTestUtilities.CreateTestNetState();
        ns.Account = acct; pm.NetState = ns; ns.Mobile = pm;
        var cases = new (string Name, Func<Item> Make, bool Own)[]
        {
            ("plain cloak, plain chest", () => new Cloak(), false),
            ("isle cloak, MOVABLE cloak chest", () => new WakeningIsleCloak(pm), true),
            ("plain cloak, cloak chest", () => new Cloak(), true),
            ("isle cloak regular loot, cloak chest", () => new WakeningIsleCloak(pm) { LootType = LootType.Regular }, true),
            ("isle cloak no owner, cloak chest", () => new WakeningIsleCloak(null), true),
            ("isle cloak, cloak chest", () => new WakeningIsleCloak(pm), true),
        };
        foreach (var (name, make, own) in cases)
        {
            pm.NextActionTime = 0;
            pm.Holding = null;
            Container chest = own ? new TutorialCloakChest(pm) : new WoodenChest { Movable = false };
            if (name.Contains("MOVABLE")) { chest.Movable = true; }
            var item = make();
            chest.DropItem(item);
            chest.MoveToWorld(new Point3D(1001, 1001, 0), Map.Trammel);
            pm.Lift(item, 1, out var rejected, out var reason);
            _out.WriteLine($"lift {name}: rejected={rejected} reason={reason}");
            pm.Holding = null;
            chest.Delete();
        }
        Assert.Fail("probe output above");
    }
}
