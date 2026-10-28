import os
os.chdir(r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations\Tutorial")


def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


edit("TutorialStations.cs", [
("""    Reputation,
    ShardSystems
}""", """    Reputation,
    ShardSystems,
    Client // cc-P718 item 3: client settings, optional at any time
}"""),
("""        new("shard.systems", TutorialWing.ShardSystems, "Rewards and extra jewelry slots", None, None, None,
            ["Skill progress bar", "Autoloot", "Scavenger", "Nearby loot", "Vendors: advanced shop, trade, auto buy and sell",
             "Legion scripting (advanced)", "Script library browser (advanced)"], null, "Elara Voss's house, the bank, then Rook"),
    ];""", """        new("shard.systems", TutorialWing.ShardSystems, "Rewards and extra jewelry slots", None, None, None,
            ["Skill progress bar", "Autoloot", "Scavenger", "Nearby loot", "Vendors: advanced shop, trade, auto buy and sell",
             "Legion scripting (advanced)", "Script library browser (advanced)"], null, "Elara Voss's house, the bank, then Rook"),

        // -- cc-P718 item 3: optional at any time, on the isle (Tamsin's window) or with Rook; never needed to graduate --
        new(TutorialClientTips.Key, TutorialWing.Client, "Client tips: always run", None, None, None,
            ["Options"], null, "Tamsin's window or Rook's, at any time"),
    ];

    /// <summary>cc-P718: optional lessons offered at any time, before the core is done too (Tamsin's window shows them).</summary>
    public static bool IsAnytime(string key) => key.Equals(TutorialClientTips.Key, StringComparison.OrdinalIgnoreCase);

    public static IEnumerable<TutorialStation> Anytime
    {
        get
        {
            foreach (var s in All)
            {
                if (IsAnytime(s.Key))
                {
                    yield return s;
                }
            }
        }
    }"""),
("""        ["core.loop"] = TutorialCoreTrials.Start,
    };""", """        ["core.loop"] = TutorialCoreTrials.Start,
        [TutorialClientTips.Key] = TutorialClientTips.Start, // cc-P718
    };"""),
])

edit("TutorialGumps.cs", [
("""        TutorialWing.ShardSystems => "Shard features",""", """        TutorialWing.ShardSystems => "Shard features",
        TutorialWing.Client => "Client settings","""),
("""            var groups = TutorialStations.All.Where(s => !s.IsCore).GroupBy(s => s.Wing).ToList();""",
 """            var groups = TutorialStations.All.Where(s => !s.IsCore && !TutorialStations.IsAnytime(s.Key)).GroupBy(s => s.Wing).ToList();"""),
("""        var core = TutorialStations.Core.ToList();
        var h = 100;
        if (active)
        {
            h += 24 + core.Count * Row + (wings ? 30 + Math.Max(left.Count, right.Count) * Row : 30) + 50 + (toIsle ? 30 : 0);
        }""", """        var core = TutorialStations.Core.ToList();
        var anytime = TutorialStations.Anytime.ToList(); // cc-P718: optional at any time
        var h = 100;
        if (active)
        {
            h += 24 + core.Count * Row + (wings ? 30 + Math.Max(left.Count, right.Count) * Row : 30) + 50 + (toIsle ? 30 : 0) +
                 (anytime.Count > 0 ? 30 + anytime.Count * Row : 0);
        }"""),
("""            if (wings)
            {
                AddLabel(24, y + 6, TutorialStyle.HeadingHue, "Optional trade and skill lessons");""", """            if (anytime.Count > 0)
            {
                AddLabel(24, y + 6, TutorialStyle.HeadingHue, "Optional, at any time (you can skip these)");
                y += 30;
                foreach (var s in anytime)
                {
                    var done = record!.StationsDone.Contains(s.Key);
                    AddButton(24, y, 4005, 4007, BtnStationBase + Array.IndexOf(TutorialStations.All, s));
                    AddLabel(60, y + 2, done ? TutorialStyle.DoneHue : TutorialStyle.TextHue, $"{s.Title}{(done ? " (done)" : "")}");
                    y += Row;
                }
            }

            if (wings)
            {
                AddLabel(24, y + 6, TutorialStyle.HeadingHue, "Optional trade and skill lessons");"""),
("""        if (!station.IsCore && (ClusterFTutorial.RecordOf(_pm) is not { } record || !WingsOpen(record)))""",
 """        if (!station.IsCore && !TutorialStations.IsAnytime(station.Key) &&
            (ClusterFTutorial.RecordOf(_pm) is not { } record || !WingsOpen(record)))"""),
])
print("ok")
