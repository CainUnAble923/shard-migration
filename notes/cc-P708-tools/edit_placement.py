"""cc-P708: ClusterFGuildHallPlacement takes a moved hall's old site away before placing (place) and with the rest
(clear): OldSite(h) lists the hall's parts standing off its current site and a guildmaster of the old type at an old
post (ClusterFGuildHallMoves). Each replaced text must occur exactly once.
    python -P edit_placement.py
"""
P = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/ClusterFGuildHallPlacement.cs'
s = open(P, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s else '\n'


def rep(old, new):
    global s
    old, new = old.replace('\n', NL), new.replace('\n', NL)
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


# 1. the header
rep("""//   [ClusterFGuildHalls runes [hall]              a bag of recall runes marked at the travel stops
//""", """//   [ClusterFGuildHalls runes [hall]              a bag of recall runes marked at the travel stops
//
// cc-P708: six halls moved onto the Siege of Sosaria land (ClusterFGuildHallMoves). place and clear first take away what
// a world still has of a moved hall at its old site: its sign, guild house and doors standing off its current site (a
// stock sign the old sign hid is shown again), and a guildmaster of the old type within a tile of the old post.
//""")

# 2. OldSite and TakeAway, before Place
rep("""        public static List<string> Place(string key, bool dryRun, bool isTestShard)
        {""", """        /// <summary>
        /// cc-P708: what a world still has of the hall at an old site: its own parts off its current site, and a
        /// guildmaster of the old type within a tile of an old post (ClusterFGuildHallMoves). Nothing is changed.
        /// </summary>
        public static List<IEntity> OldSite(Hall h)
        {
            var map = MapOf(h);
            var stale = new List<IEntity>();
            foreach (var part in Parts(h))
            {
                var current = part.Map == map && part switch
                {
                    GuildHallSign => part.Location == h.Sign,
                    GuildHallBuilding => h.Kind == Kind.New && part.Location == h.MultiAt,
                    GuildHallDoor => h.Kind == Kind.New && GuildHouseDoors.Any(d =>
                        part.Location == new Point3D(h.MultiAt.X + d.Dx, h.MultiAt.Y + d.Dy, h.MultiAt.Z + d.Dz)),
                    _ => true
                };
                if (!current)
                {
                    stale.Add(part);
                }
            }

            foreach (var moved in ClusterFGuildHallMoves.All.Where(m => m.Key == h.Key))
            {
                var oldMap = moved.MapIndex >= 0 && moved.MapIndex < Map.Maps.Length ? Map.Maps[moved.MapIndex] : null;
                if (oldMap == null || oldMap == Map.Internal)
                {
                    continue;
                }

                foreach (var m in oldMap.GetMobilesInRange(moved.Npc, 1))
                {
                    if (!m.Deleted && m.GetType() == moved.NpcType && !(m.Map == map && m.Location == h.Npc))
                    {
                        stale.Add(m);
                    }
                }
            }

            return stale;
        }

        // cc-P708: deletes what OldSite found (showing again a stock sign an old sign hid); one line per thing.
        private static IEnumerable<string> TakeAway(List<IEntity> stale, bool dryRun)
        {
            foreach (var e in stale)
            {
                yield return $"the old {e.GetType().Name} at {e.Location}";
                if (dryRun)
                {
                    continue;
                }

                if (e is GuildHallSign { HiddenStockSign: { Deleted: false } stock })
                {
                    stock.Visible = true;
                }

                e.Delete();
            }
        }

        public static List<string> Place(string key, bool dryRun, bool isTestShard)
        {""")

# 3. Place: take the old site away first
rep("""                var parts = Parts(h);
                var did = new List<string>();

                if (h.Kind == Kind.New)""", """                // cc-P708: a moved hall's old site goes first
                var stale = OldSite(h);
                var did = TakeAway(stale, dryRun).Select(t => $"{(dryRun ? "would take away" : "took away")} {t}").ToList();
                var parts = Parts(h).Except(stale.OfType<Item>()).ToList();

                if (h.Kind == Kind.New)""")

# 4. Clear: the old guildmaster too (the old parts are among Parts already)
rep("""                var npc = FindNpc(h);
                if (npc != null)
                {
                    gone.Add($"the {h.NpcType.Name} at {npc.Location}");""", """                // cc-P708: a guildmaster still at a moved hall's old post
                gone.AddRange(TakeAway(OldSite(h).OfType<Mobile>().Cast<IEntity>().ToList(), dryRun));

                var npc = FindNpc(h);
                if (npc != null)
                {
                    gone.Add($"the {h.NpcType.Name} at {npc.Location}");""")

open(P, 'w', encoding='utf-8', newline='').write(s)
print('ok')
