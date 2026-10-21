# cc-P237 WRITES: the red run's breaks, one per server fact, and "restore" (byte copies, SHA-256 checked, no
# P237-BREAK left). python breaks.py apply | restore
import os, sys, shutil, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
CUS = 'D:/UO/golems/Bronze/ShatteredLegacy/server/customizations'
BAK = os.path.join(HERE, 'breaks-backup')
SEEDER = CUS + '/ClusterFCommunityArtSeeder.cs'
LAYOUT = CUS + '/ClusterFCommunityArtLayout.cs'
RUNE = CUS + '/ShatteredRunestone.cs'
FILES = [SEEDER, LAYOUT, RUNE]
BREAKS = [
    # 1. two rows on one tile at one z: the rug moved onto the campfire's tile
    (LAYOUT, 'new("camp-rug", "camp", 3599, 2623, 0,', 'new("camp-rug", "camp", 3601, 2622, 0, /* P237-BREAK */'),
    # 2. place forgets what is already placed
    (SEEDER, '                if (have.Contains(row.Key))', '                if (false && have.Contains(row.Key)) // P237-BREAK'),
    # 3. clear also deletes a same-art item on a row's tile that is not ours
    (SEEDER, '            lines.Add($"[CommunityArt] {(dryRun ? "dry run: would remove" : "removed")} {items.Count} community art item(s); nothing else is touched.");',
     '            foreach (var o in World.Items.Values.Where(i => i is not CommunityArt && !i.Deleted && ClusterFCommunityArtLayout.Rows.Any(r => r.ItemId == i.ItemID && r.X == i.X && r.Y == i.Y)).ToList()) { if (!dryRun) o.Delete(); } // P237-BREAK\n'
     '            lines.Add($"[CommunityArt] {(dryRun ? "dry run: would remove" : "removed")} {items.Count} community art item(s); nothing else is touched.");'),
    # 4. the key is not what the row says (it no longer round-trips to the row's key)
    (SEEDER, '            _key = row.Key;', '            _key = row.Key + "-"; // P237-BREAK'),
    # 5. the server never writes the records
    (RUNE, '            ClusterFCommunityArtRecords.Apply();', '            // ClusterFCommunityArtRecords.Apply(); // P237-BREAK'),
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
            assert 'P237-BREAK' not in open(f, encoding='utf-8').read(), f
        print('restored', len(FILES), 'files, SHA-256 equal, no P237-BREAK left')
