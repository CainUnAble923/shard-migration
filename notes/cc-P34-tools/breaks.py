# cc-P34 WRITES: the red run's deliberate breaks, one per fact, each marked P34-BREAK; "restore" puts the byte copies
# back, checks SHA-256 and that no P34-BREAK marker is left. Usage: python breaks.py apply | restore
import hashlib, os, shutil, sys
ROOT = r'D:/ShatteredLegacy/server'
KEEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'break-copies')
BREAKS = [
    # fact 2: a row on the arrival tile
    ('customizations/ClusterFWinterDecorLayout.cs',
     'new("sq-gift2", "square", 3511, 2576, 14,', 'new("sq-gift2", "square", 3503, 2574, 14, /* P34-BREAK */'),
    # fact 3: January 6 left out of the season
    ('customizations/ClusterFWinterDecorSeeder.cs',
     'local.Month == 12 || local.Month == 1 && local.Day <= 6;', 'local.Month == 12 || local.Month == 1 && local.Day < 6; // P34-BREAK'),
    # fact 4: take-down also deletes any item with the same art on a decor tile (the lookalike)
    ('customizations/ClusterFWinterDecorSeeder.cs',
     "                    item.Delete();\n                }\n            }\n\n            lines.Add($\"[WinterDecor] {(dryRun ? \"dry run: would remove\"",
     "                    var hit = new List<Item>(); foreach (var other in item.GetItemsAt()) { if (other != item && other.ItemID == item.ItemID) hit.Add(other); } foreach (var o in hit) o.Delete(); // P34-BREAK\n                    item.Delete();\n                }\n            }\n\n            lines.Add($\"[WinterDecor] {(dryRun ? \"dry run: would remove\""),
    # fact 6: the server forgets the winter records
    ('customizations/ShatteredRunestone.cs', '            ClusterFWinterDecorArt.Apply();', '            // ClusterFWinterDecorArt.Apply(); P34-BREAK'),
    # fact 5: the saved state loses "down"
    ('customizations/ClusterFWinterDecorSeeder.cs',
     'writer.Write((byte)(LastAutomatic == null ? 0 : LastAutomatic.Value ? 2 : 1));',
     'writer.Write((byte)(LastAutomatic == null ? 0 : 2)); // P34-BREAK'),
]
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
if sys.argv[1] == 'apply':
    os.makedirs(KEEP, exist_ok=True)
    files = sorted({f for f, _, _ in BREAKS})
    for f in files:
        src = os.path.join(ROOT, f)
        shutil.copyfile(src, os.path.join(KEEP, f.replace('/', '__')))
        open(os.path.join(KEEP, f.replace('/', '__') + '.sha'), 'w').write(sha(src))
    for f, a, b in BREAKS:
        p = os.path.join(ROOT, f); s = open(p, encoding='ascii', newline='').read()
        assert s.count(a) == 1, (f, a[:60])
        open(p, 'w', encoding='ascii', newline='').write(s.replace(a, b))
    print('applied', len(BREAKS), 'breaks to', files)
else:
    for n in os.listdir(KEEP):
        if n.endswith('.sha'): continue
        dst = os.path.join(ROOT, n.replace('__', '/'))
        shutil.copyfile(os.path.join(KEEP, n), dst)
        assert sha(dst) == open(os.path.join(KEEP, n + '.sha')).read(), dst
        assert 'P34-BREAK' not in open(dst, encoding='ascii').read(), dst
    print('restored and checked')
