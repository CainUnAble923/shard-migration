"""cc-P664: the changes to existing code, as guarded replacements (the Read tool is denied on the code copy in
unattended runs). Each old text must appear exactly once. TutorialCopies.cs is written whole.

    python -P edit_code.py <code copy>/server
"""
import os, sys

SRV = sys.argv[1] if len(sys.argv) > 1 else None


def edit(rel, pairs):
    p = os.path.join(SRV, rel)
    s = open(p, encoding='utf-8', newline='').read()
    crlf = '\r\n' in s
    s = s.replace('\r\n', '\n')
    for old, new in pairs:
        assert s.count(old) == 1, (rel, old[:90], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', '\r\n') if crlf else s)
    print('edited', rel)


def main():
    edit('customizations/Tutorial/TutorialWorld.cs', [
        ("""    /// <summary>The map a trainee's core lessons are on. One copy for now, so the Fold.</summary>
    public static Map MapOf(PlayerMobile pm) => Isle;""",
         """    /// <summary>
    /// The map a trainee's core lessons are on: the tutorial copy they are on or logged out on (cc-P664, TutorialCopies),
    /// else the Fold. No side effects: copies are handed out only by TutorialStart.SendToIsle.
    /// </summary>
    public static Map MapOf(PlayerMobile pm) => TutorialCopies.CopyOf(pm) ?? Isle;"""),
    ])

    edit('customizations/Tutorial/TutorialStart.cs', [
        ("""    /// <summary>Wakes a trainee on the isle's beach (with their pets) and points them at Tamsin.</summary>
    public static void SendToIsle(PlayerMobile pm)
    {
        if (!TutorialWorld.IsOnIsle(pm))
        {
            TutorialWorld.Cross(pm, TutorialWorld.Arrival, TutorialWorld.MapOf(pm));
        }
""", """    /// <summary>Wakes a trainee on the isle's beach (with their pets) and points them at Tamsin.</summary>
    public static void SendToIsle(PlayerMobile pm) => SendToIsle(pm, atNextLesson: false);

    /// <summary>
    /// cc-P664: onto the trainee's own copy of the isle (or their party's; TutorialCopies.Claim), on the beach, or at
    /// their first undone lesson. When every copy is in use, onto the Fold's beach to wait.
    /// </summary>
    public static void SendToIsle(PlayerMobile pm, bool atNextLesson)
    {
        if (TutorialCopies.Claim(pm) is not { } copy)
        {
            TutorialCopies.Wait(pm);
            return;
        }

        if (pm.Map != copy)
        {
            TutorialWorld.Cross(pm, atNextLesson ? TutorialCopies.NextLessonSpot(pm, copy) : TutorialWorld.Ground(copy, TutorialWorld.Beach), copy);
        }

        if (atNextLesson)
        {
            ClusterFTutorial.SystemLine(pm, "You are on your own copy of the Wakening Isle, at your next lesson.");
            TutorialGuide.PointTo(pm);
            return;
        }
"""),
    ])

    edit('customizations/Tutorial/TutorialCorePlacement.cs', [
        ("""    public static string Seed(bool dryRun)
    {
        if (!IsTestShard()) { return "Tutorial: refused. Test world only; live is never seeded."; }
        var map = TutorialWorld.Isle;
        if (map == null) { return "Tutorial: refused. The Fold (map 32) is not registered."; }""",
         """    public static string Seed(bool dryRun) => SeedOn(TutorialWorld.Isle, dryRun, withHaven: true);

    /// <summary>
    /// cc-P664: seeds the isle's lessons onto <paramref name="map"/>: the Fold, or one tutorial copy (TutorialCopies seeds
    /// each on first use and after a reset). <paramref name="withHaven"/> also places Rook and the town vet in New Haven.
    /// </summary>
    public static string SeedOn(Map? map, bool dryRun, bool withHaven)
    {
        if (!IsTestShard()) { return "Tutorial: refused. Test world only; live is never seeded."; }
        if (map == null) { return "Tutorial: refused. The Fold (map 32) is not registered."; }"""),
        ("""        var rookMissing = TutorialRecruiter.Find() == null;""",
         """        var rookMissing = withHaven && TutorialRecruiter.Find() == null;"""),
        ("""        var townVetMissing = FindTownVet() == null;""",
         """        var townVetMissing = withHaven && FindTownVet() == null;"""),
        ("""        foreach (var point in new[] { GateExit, HavenSpots.Rook }.Concat(townVetMissing ? new[] { HavenSpots.VetSpot } : []))""",
         """        foreach (var point in (withHaven ? new[] { GateExit, HavenSpots.Rook } : Array.Empty<Point3D>()).Concat(townVetMissing ? new[] { HavenSpots.VetSpot } : []))"""),
        ("""        var farm = TutorialFarm.Seed(dryRun);""", """        var farm = TutorialFarm.Seed(map, dryRun);"""),
    ])

    edit('customizations/Tutorial/TutorialFarm.cs', [
        ("""        public static SeedResult Seed(bool dryRun)
        {
            if (Refusal(true) is { } refused)
            {
                return refused;
            }

            var map = TutorialWorld.Isle;
            int addons = 0""", """        public static SeedResult Seed(bool dryRun) => Seed(TutorialWorld.Isle, dryRun);

        /// <summary>cc-P664: the core farm onto one map: the Fold, or a tutorial copy (TutorialCopies).</summary>
        public static SeedResult Seed(Map map, bool dryRun)
        {
            if (Refusal(true) is { } refused)
            {
                return refused;
            }

            int addons = 0"""),
    ])

    edit('customizations/Tutorial/ClusterFTutorial.cs', [
        ("""        TutorialCoreTrials.Cancel(pm);
        if (Enabled)
        {""", """        TutorialCoreTrials.Cancel(pm);
        if (Enabled)
        {
            // cc-P664: a trainee whose copy of the isle was freed while they were away goes to a fresh one.
            TutorialCopies.OnLogin(pm);
"""),
        ("""    [Usage("Tutorial <status | enter | station <key> | skip | remedial | graduate | reset>")]""",
         """    [Usage("Tutorial <status | enter | station <key> | skip | remedial | graduate | reset | copies>")]"""),
        ("""        var key = e.Length > 1 ? e.GetString(1) : null;

        e.Mobile.SendMessage("Target a player.");""", """        var key = e.Length > 1 ? e.GetString(1) : null;

        if (verb == "copies")
        {
            // cc-P664: the isle's 16 private copies, who holds each, and who waits.
            foreach (var line in TutorialCopies.Report())
            {
                e.Mobile.SendMessage(line);
            }

            return;
        }

        e.Mobile.SendMessage("Target a player.");"""),
        ("""    [Description("Targets a player and shows or moves their account's tutorial: enter starts it, station runs one station, skip skips it (no confirmations), remedial starts remedial training, graduate graduates, reset clears the record.")]""",
         """    [Description("Targets a player and shows or moves their account's tutorial: enter starts it, station runs one station, skip skips it (no confirmations), remedial starts remedial training, graduate graduates, reset clears the record. copies (no target) lists the isle's private copies.")]"""),
    ])


if __name__ == '__main__':
    main()
