"""cc-P707: the copy hold becomes a setting, clusterf.tutorial.copyHoldMinutes (30), so a test world can watch a reset.

    python -P edit_hold.py <code repo>
"""
import os
import sys

repo = sys.argv[1]
copies = os.path.join(repo, 'server', 'customizations', 'Tutorial', 'TutorialCopies.cs')
tests = os.path.join(repo, 'server', 'tests', 'Tutorial', 'TutorialCopiesVerification.cs')


def edit(path, pairs):
    s = open(path, 'rb').read().decode('utf-8')
    crlf = '\r\n' in s
    for old, new in pairs:
        if crlf:
            old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
        assert s.count(old) == 1, (path, old[:70])
        s = s.replace(old, new)
    open(path, 'wb').write(s.encode('utf-8'))


edit(copies, [
    ('''//   - a copy is held while anyone is on it online, and for 30 minutes after the last occupant left or logged out
//     (HoldAfterLeaving); then Tick frees it''', '''//   - a copy is held while anyone is on it online, and for 30 minutes after the last occupant left or logged out
//     (HoldAfterLeaving; cc-P707: the setting clusterf.tutorial.copyHoldMinutes, 30); then Tick frees it'''),
    ('''    /// <summary>How long a copy stays held after its last occupant left or logged out.</summary>
    public static readonly TimeSpan HoldAfterLeaving = TimeSpan.FromMinutes(30);
''', '''    /// <summary>
    /// How long a copy stays held after its last occupant left or logged out. cc-P707: the setting
    /// clusterf.tutorial.copyHoldMinutes (30, at least 1), so a test world can watch a copy reset.
    /// </summary>
    public static TimeSpan HoldAfterLeaving =>
        TimeSpan.FromMinutes(Math.Max(1, ServerConfiguration.GetOrUpdateSetting("clusterf.tutorial.copyHoldMinutes", 30)));
'''),
])

edit(tests, [
    ('''    // ---------------------------------------------------------------- 4

    [Fact]
    public void LoginAfterTheCopyWasFreedGoesToAFreshCopyAtTheNextLesson()''', '''    // ---------------------------------------------------------------- 3b (cc-P707)

    [Fact]
    public void TheHoldIsTheSettingSoATestWorldCanShortenIt()
    {
        Assert.Equal(TimeSpan.FromMinutes(30), TutorialCopies.HoldAfterLeaving);
        var pm = Trainee("CopyShortHold");
        var slot = TutorialCopies.SlotOf(pm.Map);
        var generation = slot.Generation;
        var now = Core.Now;
        try
        {
            ServerConfiguration.SetSetting("clusterf.tutorial.copyHoldMinutes", 2);
            Assert.Equal(TimeSpan.FromMinutes(2), TutorialCopies.HoldAfterLeaving);
            LogOut(pm, now);
            TutorialCopies.Tick(now + TimeSpan.FromMinutes(1));
            Assert.True(slot.InUse); // held for the two minutes
            TutorialCopies.Tick(now + TimeSpan.FromMinutes(3));
            Assert.False(slot.InUse); // freed after them
            Assert.Equal(generation + 1, slot.Generation);
            ServerConfiguration.SetSetting("clusterf.tutorial.copyHoldMinutes", 0);
            Assert.Equal(TimeSpan.FromMinutes(1), TutorialCopies.HoldAfterLeaving); // never less than a minute
        }
        finally
        {
            ServerConfiguration.SetSetting("clusterf.tutorial.copyHoldMinutes", 30);
        }
    }

    // ---------------------------------------------------------------- 4

    [Fact]
    public void LoginAfterTheCopyWasFreedGoesToAFreshCopyAtTheNextLesson()'''),
])
print('ok')
