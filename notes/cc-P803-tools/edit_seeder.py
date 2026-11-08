"""cc-P803: the office seeder swaps a stale office decor for the current layout on world load (both copies), and on the
release the sign becomes the standing signpost 0xA854.  python -P notes/cc-P803-tools/edit_seeder.py <release|main> <root>"""
import sys
which, root = sys.argv[1], sys.argv[2]
p = root + "/server/customizations/ClusterFRegistrarOfficeSeeder.cs"
s = open(p, encoding="utf-8").read()
nl = "\r\n" if "\r\n" in s else "\n"
s = s.replace("\r\n", "\n")

old = '''        private static bool _seedOnWorldLoad;

        public static void Configure()
        {
            _seedOnWorldLoad = ServerConfiguration.GetOrUpdateSetting("clusterf.registrarOffice.seedOnWorldLoad", false);

            EventSink.WorldLoad += OnWorldLoad;
            CommandSystem.Register("ClusterFSeedRegistrarOffice", AccessLevel.Administrator, OnSeedCommand);
        }

        private static void OnWorldLoad()
        {
            if (!_seedOnWorldLoad)
            {
                return;
            }
'''
new = '''        private static bool _seedOnWorldLoad;
        private static bool _upgradeOnWorldLoad;

        public static void Configure()
        {
            _seedOnWorldLoad = ServerConfiguration.GetOrUpdateSetting("clusterf.registrarOffice.seedOnWorldLoad", false);
            // cc-P803: a world that already holds the office decor gets the current layout by itself (guide 7). Only an
            // office standing in this layout's own building is swapped (UpgradeStale), so a world whose office is in
            // another town's house is left alone, and a world with no office decor still gets none from this.
            _upgradeOnWorldLoad = ServerConfiguration.GetOrUpdateSetting("clusterf.registrarOffice.upgradeOnWorldLoad", true);

            EventSink.WorldLoad += OnWorldLoad;
            CommandSystem.Register("ClusterFSeedRegistrarOffice", AccessLevel.Administrator, OnSeedCommand);
        }

        private static void OnWorldLoad()
        {
            if (_upgradeOnWorldLoad)
            {
                // After the load: addons made inside World.Load reach World.Items only once it ends (cc-P726).
                Timer.DelayCall(TimeSpan.Zero, () =>
                {
                    foreach (var line in UpgradeStale())
                    {
                        Console.WriteLine(line);
                    }
                });
            }

            if (!_seedOnWorldLoad)
            {
                return;
            }
'''
assert s.count(old) == 1, "configure"
s = s.replace(old, new)

old2 = '''        internal static List<BaseAddon> FindOfficeAddons()'''
new2 = '''        /// <summary>
        /// cc-P803: true when the addon's components are exactly its area's layout (item id and tile, as a multiset).
        /// </summary>
        internal static bool IsCurrent(BaseAddon addon)
        {
            var row = Array.Find(Addons, a => a.Type == addon.GetType());
            if (row.Components == null)
            {
                return false;
            }

            static string Key(int id, int x, int y, int z) => $"{id:X4}@{x},{y},{z}";
            var want = row.Components.Select(c => Key(c.ItemID, c.X, c.Y, c.Z)).OrderBy(k => k, StringComparer.Ordinal);
            var have = addon.Components.Select(c => Key(c.ItemID, c.X, c.Y, c.Z)).OrderBy(k => k, StringComparer.Ordinal);
            return want.SequenceEqual(have);
        }

        /// <summary>cc-P803: the current layout's box, three tiles round every component.</summary>
        internal static bool InThisBuilding(Point3D p)
        {
            var all = ClusterFRegistrarOfficeLayout.Components;
            return p.X >= all.Min(c => c.X) - 3 && p.X <= all.Max(c => c.X) + 3 &&
                   p.Y >= all.Min(c => c.Y) - 3 && p.Y <= all.Max(c => c.Y) + 3;
        }

        /// <summary>
        /// cc-P803: on a world whose office decor (all of it in this layout's building) differs from the current layout,
        /// runs Replace: the three office addons go and the current layout is placed. Nothing when there is no office
        /// decor, when it is current, or when any of it stands elsewhere. Running it again changes nothing.
        /// </summary>
        internal static List<string> UpgradeStale()
        {
            var found = FindOfficeAddons();
            if (found.Count == 0)
            {
                return [];
            }

            if (!found.TrueForAll(a => InThisBuilding(a.Location)))
            {
                return ["ClusterF registrar office upgrade: office decor stands outside this layout's building; left alone."];
            }

            if (found.TrueForAll(IsCurrent) && found.Count == Addons.Length)
            {
                return [];
            }

            var lines = Replace(false);
            lines.Insert(0, "ClusterF registrar office upgrade: the decor was an older layout; replacing it with the current one.");
            return lines;
        }

        internal static List<BaseAddon> FindOfficeAddons()'''
assert s.count(old2) == 1, "find"
s = s.replace(old2, new2)
if "using System.Linq;" not in s:
    s = s.replace("using System.Collections.Generic;\n", "using System.Collections.Generic;\nusing System.Linq;\n", 1)

if which == "release":
    old3 = '''        // The sign, by item id (design: 0x0BCF at 3463,2597). cc-P31: 0x0BD0 at 3460,2595 left the design.
        public const int SignItemID = 0x0BCF;'''
    new3 = '''        // The sign, by item id. cc-P31: 0x0BD0 at 3460,2595 left the design. cc-P803: the sign arm 0x0B97 and its board
        // 0x0BCF at 3463,2597 hung from no wall (none north of that tile), under the eave; the office's door is in its north
        // wall, so the sign is a named standing signpost by the north-east corner, 3463,2596 (building guide 11.12).
        public const int SignItemID = 0xA854;'''
    assert s.count(old3) == 1, "sign"
    s = s.replace(old3, new3)
    s = s.replace("    // Outside: a potted tree by the front door, and the signpost with its sign on the east wall.",
                  "    // Outside: a potted tree by the front door, the named signpost by the north-east corner and a League banner on\n    // the east wall (cc-P803).")
open(p, "w", encoding="utf-8", newline=nl).write(s)
print("ok", p)
