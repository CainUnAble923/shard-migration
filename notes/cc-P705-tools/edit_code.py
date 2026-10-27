"""cc-P705: the code changes, as guarded replacements (the Read tool is denied on the code copy in unattended runs).
Each old text must appear exactly once.

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
        assert s.count(old) == 1, (rel, old[:80], s.count(old))
        s = s.replace(old, new)
    if crlf:
        s = s.replace('\n', '\r\n')
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('edited', rel)



def main():
    edit('customizations/Tutorial/TutorialWorld.cs', [
        ("""    public static Point3D Ground(Map map, Point2D p) => new(p.X, p.Y, map.GetAverageZ(p.X, p.Y));
    """, """    /// <summary>
        /// Where someone stands at <paramref name="p"/>: the walkable surface there (cc-P705, Codex on P663: a dock's planks
        /// over the sea, not the sea floor under them), else the land's average Z.
        /// </summary>
        public static Point3D Ground(Map map, Point2D p)
        {
            var avg = map.GetAverageZ(p.X, p.Y);
            var statics = new List<(int Z, int ItemId)>();
            foreach (var tile in map.Tiles.GetStaticAndMultiTiles(p.X, p.Y))
            {
                statics.Add((tile.Z, tile.ID));
            }

            return new Point3D(p.X, p.Y, SurfaceZ(avg, statics));
        }

        /// <summary>
        /// The highest walkable surface (Surface and not Impassable) whose top is above the land and within a person's height
        /// of it (PersonHeight 16, pinned Movement), else <paramref name="landAvg"/>: planks 2 above the sea are stood on, a
        /// roof 20 above a floor is not.
        /// </summary>
        public static int SurfaceZ(int landAvg, IEnumerable<(int Z, int ItemId)> statics)
        {
            var best = landAvg;
            foreach (var (z, id) in statics)
            {
                var data = TileData.ItemTable[id & TileData.MaxItemValue];
                if (!data.Surface || data.Impassable)
                {
                    continue;
                }

                var top = z + data.CalcHeight;
                if (top > best && top < landAvg + 16)
                {
                    best = top;
                }
            }

            return best;
        }

        /// <summary>
        /// cc-P705: whether the isle's land is on this server's map (P662's patch): the beach fits a person. Until it is, the
        /// site is void and a "Tutorial Island" pick starts in New Haven instead (TutorialStart). A seam for tests.
        /// </summary>
        public static Func<bool> IsleReady { get; set; } = () => Isle is { } isle && isle.CanFit(Arrival, 16, false, false);
    """),
        ("""using System.Collections.Generic;
    using Server.Mobiles;""", """using System;
    using System.Collections.Generic;
    using Server.Mobiles;"""),
    ])

    edit('customizations/Tutorial/HavenSpots.cs', [
        ("""    /// <summary>The New Haven start: character creation's city, the skip, the Fold's send-home (3503,2574,14).</summary>
        public static readonly Point3D Start = new(3503, 2574, 14);""",
         """    /// <summary>
        /// The New Haven start: character creation's city (with the tutorial on or off, cc-P705), the skip, the Fold's
        /// send-home (3503,2574,14). Settable only as a seam for tests; S7 changes the value here.
        /// </summary>
        public static Point3D Start { get; set; } = new(3503, 2574, 14);"""),
    ])

    edit('customizations/CharacterCreation.cs', [
        ("""        return
            [
                new("New Haven", "The Bountiful Harvest Inn", 1150168, 3503, 2574, 14, Map.Trammel)
            ];
        }""", """        return TutorialOffCities();
        }

        // cc-P705 (Codex on P663): the tutorial-off list reads New Haven's start from HavenSpots too, so S7 moves it with
        // every other New Haven spot.
        public static CityInfo[] TutorialOffCities() =>
        [
            new("New Haven", "The Bountiful Harvest Inn", 1150168, Server.Tutorial.HavenSpots.Start.X,
                Server.Tutorial.HavenSpots.Start.Y, Server.Tutorial.HavenSpots.Start.Z, Server.Tutorial.HavenSpots.Map)
        ];"""),
    ])

    edit('customizations/Tutorial/TutorialStart.cs', [
        ("""        /// <summary>New Haven, nothing else.</summary>
            Haven
        }""", """        /// <summary>New Haven, nothing else.</summary>
            Haven,
            /// <summary>cc-P705: chose the isle, but the isle's land is not on this server's map yet; New Haven, tutorial unused.</summary>
            IsleMissing
        }"""),
        ("""        var choice = ClusterFTutorial.Enabled ? ChoiceOf(city) : Choice.None;
            if (choice == Choice.None || IsStaff(pm))
            {
                return (city.Location, city.Map);
            }

            Record(pm, choice);
            return Decide(pm, choice) == Outcome.Isle && TutorialWorld.Isle != null
                ? (TutorialWorld.Arrival, TutorialWorld.Isle)
                : (HavenSpots.Start, HavenSpots.Map);""", """        var choice = ClusterFTutorial.Enabled ? ChoiceOf(city) : Choice.None;
            if (choice == Choice.None || IsStaff(pm))
            {
                // cc-P705 (Codex on P663): the isle's entry carries display coordinates in the sea; nobody is placed there.
                return ChoiceOf(city) == Choice.Isle ? (HavenSpots.Start, HavenSpots.Map) : (city.Location, city.Map);
            }

            Record(pm, choice);
            return Decide(pm, choice) == Outcome.Isle && TutorialWorld.Isle != null && TutorialWorld.IsleReady()
                ? (TutorialWorld.Arrival, TutorialWorld.Isle)
                : (HavenSpots.Start, HavenSpots.Map);"""),
        ("""        ClusterFAccountPersistence.GetOrCreate(acct).FlagValues.Remove(Key(pm));
            var outcome = Decide(pm, choice);
            switch (outcome)""", """        ClusterFAccountPersistence.GetOrCreate(acct).FlagValues.Remove(Key(pm));
            var outcome = Decide(pm, choice);
            // cc-P705: a release with the start choice but without the isle's map patch never strands anyone in the void.
            if (outcome == Outcome.Isle && !TutorialWorld.IsleReady())
            {
                outcome = Outcome.IsleMissing;
            }

            switch (outcome)"""),
        ("""            case Outcome.Haven:
                    SendHome(pm);
                    break;
            }""", """            case Outcome.Haven:
                    SendHome(pm);
                    break;
                case Outcome.IsleMissing:
                    SendHome(pm);
                    ClusterFTutorial.SystemLine(pm, "The Wakening Isle is not open on this world yet, so this character starts in New Haven. Your account has not used its tutorial: a character you make once the isle opens can still take it.");
                    break;
            }"""),
    ])


if __name__ == '__main__':
    main()
