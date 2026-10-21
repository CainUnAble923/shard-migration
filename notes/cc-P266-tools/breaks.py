# cc-P266 WRITES: the red run's breaks, one per server fact, and "restore" (byte copies, SHA-256 checked, no
# P266-BREAK left). python breaks.py apply | restore
import os, sys, shutil, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
CUS = 'D:/UO/golems/Bronze/ShatteredLegacy/server/customizations'
BAK = os.path.join(HERE, 'breaks-backup')
SEEDER = CUS + '/ClusterFWinterDecorSeeder.cs'
LAYOUT = CUS + '/ClusterFWinterDecorLayout.cs'
CALENDAR = CUS + '/WinterAdventCalendar.cs'
FILES = [SEEDER, LAYOUT, CALENDAR]
BREAKS = [
    # 1. (fact 1) a row's ID that nobody registered: the gnome's ID bumped past the block
    (LAYOUT, 'new("sq-gnome", "square", 3512, 2578, 14, 0x33B2,', 'new("sq-gnome", "square", 3512, 2578, 14, 0x33B7, /* P266-BREAK */'),
    # 2. (fact 2) a row on P237's fruit cart tile
    (LAYOUT, 'new("bank-plush", "bank", 3490, 2568, 20,', 'new("bank-plush", "bank", 3512, 2574, 20, /* P266-BREAK */'),
    # 3. (fact 3, 4) the end of the season a day early: January 6 left out
    (SEEDER, '        public const string DefaultEnd = "01-06";', '        public const string DefaultEnd = "01-05"; // P266-BREAK'),
    # 4. (fact 5, 6) place forgets to remember what it placed, by serial
    (SEEDER, '                item.MoveToWorld(new Point3D(row.X, row.Y, row.Z), Facet);\n                Tracked.Add(item.Serial);',
     '                item.MoveToWorld(new Point3D(row.X, row.Y, row.Z), Facet); // P266-BREAK: not tracked'),
    # 5. (fact 5) clear also deletes a same-art item on a row's tile that is not ours
    (SEEDER, '            lines.Add($"[{Label}] {(dryRun ? "dry run: would remove" : "removed")} {items.Count} tracked item(s) by serial" +',
     '            foreach (var o in World.Items.Values.Where(i => i is not IWinterDecorItem && !i.Deleted && ClusterFWinterDecorLayout.Rows.Any(r => r.ItemId == i.ItemID && r.X == i.X && r.Y == i.Y)).ToList()) { if (!dryRun) o.Delete(); } // P266-BREAK\n'
     '            lines.Add($"[{Label}] {(dryRun ? "dry run: would remove" : "removed")} {items.Count} tracked item(s) by serial" +'),
    # 6. (fact 7) the candle stand gives no light
    (SEEDER, 'TileFlag.Impassable | TileFlag.Unknown3, 255, 15, 29),', 'TileFlag.Impassable | TileFlag.Unknown3, 255, 15, 0), // P266-BREAK'),
    # 7. (fact 8) a door opens before its day
    (CALENDAR, '            if (day > local.Day)\n            {\n                return AdventDoorResult.NotYet;\n            }',
     '            if (false && day > local.Day) // P266-BREAK\n            {\n                return AdventDoorResult.NotYet;\n            }'),
]


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()


if __name__ == '__main__':
    if sys.argv[1] == 'apply':
        os.makedirs(BAK, exist_ok=True)
        for f in FILES:
            shutil.copy2(f, os.path.join(BAK, os.path.basename(f)))
            open(os.path.join(BAK, os.path.basename(f) + '.sha256'), 'w').write(sha(f))
        for f, a, b in BREAKS:
            t = open(f, encoding='utf-8').read()
            assert t.count(a) == 1, (f, a)
            open(f, 'w', encoding='utf-8', newline='').write(t.replace(a, b))
        print('applied', len(BREAKS))
    else:
        for f in FILES:
            b = os.path.join(BAK, os.path.basename(f))
            shutil.copy2(b, f)
            want = open(b + '.sha256').read().strip()
            assert sha(f) == want, f
            assert 'P266-BREAK' not in open(f, encoding='utf-8').read(), f
        print('restored', len(FILES), 'files, SHA-256 equal, no P266-BREAK left')
