// cc-P45 THROWAWAY PROBES B5 and B6: the abandoned-pet delete against a room registry, and logging out with the
// owner. Worktree only; never commit.

using System;
using System.Reflection;
using Server;
using Server.Mobiles;
using Xunit;
using Xunit.Abstractions;

namespace ShatteredLegacy.Tests;

[Collection("Sequential UOContent Tests")]
public class P45PersistenceProbe
{
    private readonly ITestOutputHelper _out;

    public P45PersistenceProbe(ITestOutputHelper output) => _out = output;

    private static readonly FieldInfo PendingDelete =
        typeof(BaseCreature).GetField("_pendingDeleteTimer", BindingFlags.Instance | BindingFlags.NonPublic);

    private static Timer DeleteTimerOf(BaseCreature bc) => (Timer)PendingDelete!.GetValue(bc);

    private static byte[] Save(Mobile m)
    {
        var buffer = new byte[65536];
        var writer = new BufferWriter(buffer, true);
        m.Serialize(writer);
        writer.Flush();
        return buffer;
    }

    // Room the way P41 6(b) proposes: internalize, release control, flag stabled.
    private static void Room(BaseCreature c, Mobile owner)
    {
        c.ControlTarget = null;
        c.ControlOrder = OrderType.Stay;
        c.Internalize();
        c.SetControlMaster(null);
        c.IsStabled = true;
        c.StabledBy = owner;
    }

    [Fact]
    public void B5_AfterDeserializationRunsInsideTheLoadAndTheRegistryStillWins()
    {
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        c.Owners.Add(owner); // so LastOwner is set and the abandoned-pet branch is live
        Room(c, owner);
        _out.WriteLine($"roomed: controlled={c.Controlled} lastOwner={c.LastOwner?.Name} stabled={c.IsStabled} " +
                       $"timer={DeleteTimerOf(c)?.Running}");

        var bytes = Save(c);
        var ai = c.AIObject;

        // --- restart --- IsStabled is not saved (rebuilt from PlayerMobile.Stabled at load), so a loaded
        // companion starts false. Read back into the same object, as ShrunkPetVerification does.
        c.IsStabled = false;
        c.StabledBy = null;
        c.Deserialize(new BufferReader(bytes));
        var timerRightAfterDeserialize = DeleteTimerOf(c);
        var runningRightAfterDeserialize = timerRightAfterDeserialize?.Running == true;
        // AfterDeserialization ends with ChangeAIType (BaseCreature.cs:2512), which builds a new AI object.
        var ranSynchronously = !ReferenceEquals(ai, c.AIObject);
        _out.WriteLine($"right after Deserialize: timer={(timerRightAfterDeserialize == null ? "null" : "set")} " +
                       $"AfterDeserialization ran={ranSynchronously} lastOwner={c.LastOwner?.Name ?? "null"}");

        // The registry's own Deserialize runs inside World.Load after the Mobiles persistence (priority 1),
        // so it always runs after this AfterDeserialization. Setting IsStabled stops the timer (BaseCreature.cs:897-906).
        c.IsStabled = true;
        c.StabledBy = owner;

        ShardTestClock.Advance(TimeSpan.FromMilliseconds(64)); // first slices after load
        var ranAfterSlices = !ReferenceEquals(ai, c.AIObject);
        _out.WriteLine($"after the first slices: AfterDeserialization ran={ranAfterSlices}");
        var timer = DeleteTimerOf(c);
        _out.WriteLine($"after the first slices: timer={(timer == null ? "null" : $"running={timer.Running}")}");

        Assert.True(runningRightAfterDeserialize, "AfterDeserialization ran inside Deserialize and started it");
        Assert.True(timer?.Running != true, "the registry restored IsStabled before AfterDeserialization ran");
    }

    [Fact]
    public void B5_WithoutTheRegistryTheThreeDayDeleteStarts()
    {
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        Room(c, owner);
        _out.WriteLine($"hired by SetControlMaster: LastOwner={c.LastOwner?.Name ?? "null"} (Owners is filled by taming)");
        if (c.LastOwner == null)
        {
            c.Owners.Add(owner); // what AnimalTaming does; a companion system might too
        }

        var bytes = Save(c);

        c.IsStabled = false;
        c.StabledBy = null;
        c.Deserialize(new BufferReader(bytes));
        ShardTestClock.Advance(TimeSpan.FromMilliseconds(64));
        var timer = DeleteTimerOf(c);
        _out.WriteLine($"no registry: timer={(timer == null ? "null" : $"running={timer.Running} delay={timer.Delay}")}");
        Assert.True(timer?.Running == true);
        Assert.Equal(TimeSpan.FromDays(3), timer.Delay);
    }

    // B6: logout with the owner. Seam: EventSink.Logout and PlayerMobile.PlayerLoginEvent (both public). The
    // companion stays controlled while it is off the map, so no stabling and no abandoned-pet clock applies.
    private static void LogoutCompanions(PlayerMobile pm)
    {
        foreach (var f in pm.AllFollowers)
        {
            if (f is P45ProbeCompanion c && c.Map != Map.Internal && !c.IsStabled)
            {
                c.ControlTarget = null;
                c.ControlOrder = OrderType.Stay;
                c.Internalize();
            }
        }
    }

    private static void LoginCompanions(PlayerMobile pm)
    {
        foreach (var f in pm.AllFollowers)
        {
            if (f is P45ProbeCompanion c && c.Map == Map.Internal && !c.IsStabled)
            {
                c.MoveToWorld(pm.Location, pm.Map);
                c.IssueOrder(OrderType.Follow, pm, pm);
            }
        }
    }

    [Fact]
    public void B6_LogoutRestartAndLoginBesideTheOwner()
    {
        Assert.True(Core.SE);
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        var roomed = P45.Companion(owner, 0, 1);
        var slots = owner.Followers;
        Room(roomed, owner);
        _out.WriteLine($"before logout: followers={owner.Followers} (roomed one released its slots)");

        // Logout: pinned OnLogout runs AutoStablePets; ours runs beside it.
        owner.AutoStablePets();
        LogoutCompanions(owner);
        _out.WriteLine($"after logout: map={c.Map} stabled={c.IsStabled} controlled={c.Controlled} " +
                       $"autostabled={owner.AutoStabled?.Contains(c) == true} roomed map={roomed.Map} roomed stabled={roomed.IsStabled}");
        Assert.Equal(Map.Internal, c.Map);
        Assert.False(c.IsStabled);
        Assert.True(c.Controlled);
        Assert.False(owner.AutoStabled?.Contains(c) == true);

        // --- restart while logged out ---
        var bytes = Save(c);
        owner.Followers = 0;
        owner.RemoveFollower(c);
        c.Deserialize(new BufferReader(bytes));
        ShardTestClock.Advance(TimeSpan.FromMilliseconds(64));
        owner.AutoStablePets(); // what startup CheckPets runs
        var timer = DeleteTimerOf(c);
        _out.WriteLine($"after restart: followers={owner.Followers} inAllFollowers={owner.AllFollowers?.Contains(c)} " +
                       $"deleteTimer={(timer == null ? "null" : timer.Running.ToString())} controlled={c.Controlled}");
        Assert.True(timer?.Running != true);
        Assert.Contains(c, owner.AllFollowers);

        // Login
        owner.ClaimAutoStabledPets();
        LoginCompanions(owner);
        _out.WriteLine($"after login: map={c.Map} at={c.Location} owner at={owner.Location} order={c.ControlOrder} " +
                       $"target={c.ControlTarget?.Name} roomed map={roomed.Map} followers={owner.Followers}");
        Assert.Equal(owner.Map, c.Map);
        Assert.Equal(owner.Location, c.Location);
        Assert.Equal(OrderType.Follow, c.ControlOrder);
        Assert.Equal(Map.Internal, roomed.Map);
        Assert.Equal(slots - roomed.ControlSlots, owner.Followers);
    }

    [Fact]
    public void B6_AGhostCompanionLoggedOutIsCaughtByTheDeadPetAbandonSweep()
    {
        ShardTestClock.Arm();
        var owner = P45.Owner(P45.NextSpot());
        var c = P45.Companion(owner);
        c.Kill();
        Assert.True(c.IsDeadPet);
        LogoutCompanions(owner);
        owner.Internalize(); // a logged-out player is moved to the internal map after the logout delay

        var timer = new LoyaltyTimer();
        var next = typeof(LoyaltyTimer).GetField("m_NextHourlyCheck", BindingFlags.Instance | BindingFlags.NonPublic)!;
        var tick = typeof(LoyaltyTimer).GetMethod("OnTick", BindingFlags.Instance | BindingFlags.NonPublic)!;

        next.SetValue(timer, DateTime.MinValue);
        tick.Invoke(timer, null);
        _out.WriteLine($"first sweep: abandonTime={c.OwnerAbandonTime} deleted={c.Deleted}");

        // Wind the abandon clock back rather than turning the wheel through a whole day.
        if (c.OwnerAbandonTime != DateTime.MinValue)
        {
            c.OwnerAbandonTime = Core.Now - c.BondingAbandonDelay - TimeSpan.FromMinutes(1);
        }

        next.SetValue(timer, DateTime.MinValue);
        tick.Invoke(timer, null);
        _out.WriteLine($"after {c.BondingAbandonDelay}: deleted={c.Deleted}");
        var deletedWithoutMarker = c.Deleted;

        var c2 = P45.Companion(owner);
        c2.Kill();
        LogoutCompanions(owner);
        c2.IsStabled = true; // the registry's marker for a logged-out companion
        next.SetValue(timer, DateTime.MinValue);
        tick.Invoke(timer, null);
        _out.WriteLine($"marker case first sweep: abandonTime={c2.OwnerAbandonTime}");
        c2.OwnerAbandonTime = Core.Now - c2.BondingAbandonDelay - TimeSpan.FromMinutes(1);
        next.SetValue(timer, DateTime.MinValue);
        tick.Invoke(timer, null);
        _out.WriteLine($"with IsStabled set while logged out: deleted={c2.Deleted}");

        Assert.True(deletedWithoutMarker);
        Assert.False(c2.Deleted);
    }
}
