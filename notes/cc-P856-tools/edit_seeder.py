"""cc-P856: one-off edit of the winter decor seeder (code copy): every row (P678's layout and the winter set's), the
addon layer, and the top-up of new rows at world load while the decor is up."""
import sys

# the main copy by default; the release copy (p856-isle) as the argument
p = sys.argv[1] if len(sys.argv) > 1 else r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations\ClusterFWinterDecorSeeder.cs"
s = open(p, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old, s.count(old))
    s = s.replace(old, new)


rep("""// [ClusterFWinterDecor status | preview [area] | place [area] | clear [area] [dryrun]]   (up and down still work)""",
    """// cc-P856: the rows are P678's layout (ClusterFWinterDecorLayout) and the winter set's (ClusterFWinterSetLayout: the
// Christmas train, the snowman and Santa benches in the park west of the hall, the large snow globe in the garden south
// of the square), whose layer "addon" makes a WinterSeasonAddon instead of a WinterDecor. A world whose decor is already
// up when new rows arrive (a deploy in December) gets them at the next start: TopUp places the rows of the winter set
// that are missing, only while the decor is up (the automatic check last put it up, it is the season, and some of it
// stands), so a staff clear of the whole decor still stands.
//
// [ClusterFWinterDecor status | preview [area] | place [area] | clear [area] [dryrun]]   (up and down still work)""")

rep("""            // One line at every start, so a log (and nothing else) shows what the world holds.
            EventSink.WorldLoad += () =>
            {
                foreach (var line in Status())
                {
                    Console.WriteLine(line);
                }
            };""",
    """            // One line at every start, so a log (and nothing else) shows what the world holds.
            EventSink.WorldLoad += () =>
            {
                foreach (var line in Status())
                {
                    Console.WriteLine(line);
                }
            };
            // cc-P856: after the load (items made inside World.Load reach World.Items only after it), the winter set's
            // missing rows while the decor is up.
            EventSink.WorldLoad += () => Timer.DelayCall(TimeSpan.Zero, () =>
            {
                foreach (var line in TopUp())
                {
                    Console.WriteLine(line);
                }
            });""")

rep("""        public static IEnumerable<string> Areas() => ClusterFWinterDecorLayout.Rows.Select(r => r.Area).Distinct();""",
    """        /// <summary>cc-P856: every row the decor places: P678's layout, then the winter set's addons.</summary>
        public static readonly ClusterFWinterDecorLayout.Row[] AllRows =
            ClusterFWinterDecorLayout.Rows.Concat(ClusterFWinterSetLayout.Rows).ToArray();

        public static IEnumerable<string> Areas() => AllRows.Select(r => r.Area).Distinct();""")

rep("""                ? ClusterFWinterDecorLayout.Rows
                : ClusterFWinterDecorLayout.Rows.Where(""", """                ? AllRows
                : AllRows.Where(""")
rep("""item is IWinterDecorItem w ? ClusterFWinterDecorLayout.Rows.FirstOrDefault(""", """item is IWinterDecorItem w ? AllRows.FirstOrDefault(""")
rep("""{placed.Count} of {ClusterFWinterDecorLayout.Rows.Length} rows placed""", """{placed.Count} of {AllRows.Length} rows placed""")
rep("""{g.Count()}/{ClusterFWinterDecorLayout.Rows.Count(r => r.Area == g.Key)}""", """{g.Count()}/{AllRows.Count(r => r.Area == g.Key)}""")

rep("""        public static Item Make(ClusterFWinterDecorLayout.Row row) =>
            row.Layer == CalendarLayer ? new WinterAdventCalendar(row) : new WinterDecor(row);""",
    """        public static Item Make(ClusterFWinterDecorLayout.Row row) =>
            row.Layer switch
            {
                CalendarLayer => new WinterAdventCalendar(row),
                ClusterFWinterSetLayout.AddonLayer => new WinterSeasonAddon(row),
                _ => new WinterDecor(row)
            };

        /// <summary>
        /// cc-P856: places the winter set's rows that are missing, only while the decor is up: the automatic check is on
        /// and last put it up, it is the season, and at least one tracked piece stands. What it did, or nothing.
        /// </summary>
        public static List<string> TopUp()
        {
            var lines = new List<string>();
            if (!Season.Automatic || Season.LastAutomatic != true || !Season.IsInSeason(Season.Clock()) || Placed().Count == 0)
            {
                return lines;
            }

            var have = new HashSet<string>(Placed().Concat(Strays()).Select(i => ((IWinterDecorItem)i).Key), StringComparer.Ordinal);
            var placed = 0;
            foreach (var row in ClusterFWinterSetLayout.Rows)
            {
                if (have.Contains(row.Key))
                {
                    continue;
                }

                var item = Make(row);
                item.MoveToWorld(new Point3D(row.X, row.Y, row.Z), Facet);
                Tracked.Add(item.Serial);
                placed++;
            }

            if (placed > 0)
            {
                lines.Add($"[{Label}] the decor is up: placed {placed} new winter set piece(s) it did not have yet.");
            }

            return lines;
        }""")

rep("""        [Description("The New Haven winter decor (clusterf.seasonal.winter.start to .end, default December 1 to January 6). status says the date, the season and what is placed. preview lists what place would do. place puts up the rows not already placed, all areas or one (bank, square, main road, inn, entrance, healer hall, field office, docks);""",
    """        [Description("The New Haven winter decor (clusterf.seasonal.winter.start to .end, default December 1 to January 6). status says the date, the season and what is placed. preview lists what place would do. place puts up the rows not already placed, all areas or one (bank, square, main road, inn, entrance, healer hall, field office, docks, park);""")
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
