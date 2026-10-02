# cc-P27: deliberate breaks for the red runs, and their exact restore. Writes only the four files named below in
# D:\ShatteredLegacy, and only between `apply` and `restore`.
#   python mutate.py apply R1|R2     back up, then apply that run's breaks (each must match exactly once)
#   python mutate.py restore         put the backups back and check SHA-256 against the backup
import hashlib, json, os, shutil, sys

ROOT = r'D:\ShatteredLegacy\server\customizations'
BACKUP = os.path.join(os.environ.get('P27_SCRATCH', '.'), 'mutate-backup')
SEEDER = 'ClusterFFountainOfFortuneSeeder.cs'
COIN = r'Items\Quest\LuckyCoin.cs'
IMBUE = 'ArtificersImbueGump.cs'

RUNS = {
    'R1': [
        # A1: a dry run places anyway.
        (SEEDER, '        if (!dryRun)\n            new FountainOfFortune()', '        if (true)\n            new FountainOfFortune()'),
        # A2: an existing fountain is never found, so a second run places a second one.
        (SEEDER, '        var existing = FindNear(map);', '        FountainOfFortune existing = null;'),
        # A3: the coin's range one shorter, so the nearest shore tile (3 from the fountain's corner) is out of range.
        (COIN, 'base(3, false, TargetFlags.None)', 'base(2, false, TargetFlags.None)'),
        # B-a: the essence is never taken on success.
        (IMBUE, 'if (essence != null && !GuildResources.TryConsume(_pm, essence))',
                'if (essence != null && !GuildResources.Has(_pm, essence))'),
        # B-b: the check sees only the top level of the pack (the pre-cc-P27 reach).
        (IMBUE, '            if (!GuildResources.Has(_pm, essence))\n',
                '            if (_pm.Backpack == null || !_pm.Backpack.Items.Exists(i => essence.Matches(i)))\n'),
        # B-e: the gump stops saying where the essences are.
        (IMBUE, '        return $"{stock.Total} {what}: {stock.Pack} in pack, {stock.Bank} in bank";',
                '        return $"{stock.Total} {what}";'),
    ],
    'R2': [
        # B-d: no refusal before the skill check.
        (IMBUE, '            if (!GuildResources.Has(_pm, essence))\n', '            if (_pm == null)\n'),
        # B-c and B-d: the essence taken is the last candidate (the bank's), and none found is not a refusal.
        (IMBUE, '        if (essence != null && !GuildResources.TryConsume(_pm, essence))\n        {',
                '        var p27Last = essence == null ? null : GuildResources.Candidates(_pm, essence);\n'
                '        if (p27Last?.Count > 0) p27Last[^1].Delete();\n'
                '        if (_pm == null)\n        {'),
    ],
}

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def main():
    cmd = sys.argv[1]
    if cmd == 'apply':
        os.makedirs(BACKUP, exist_ok=True)
        files = sorted({f for f, _, _ in RUNS[sys.argv[2]]})
        record = {}
        for f in files:
            src = os.path.join(ROOT, f)
            dst = os.path.join(BACKUP, f.replace('\\', '_'))
            shutil.copyfile(src, dst)
            record[f] = sha(src)
        json.dump(record, open(os.path.join(BACKUP, 'sha.json'), 'w'), indent=1)
        for f, old, new in RUNS[sys.argv[2]]:
            p = os.path.join(ROOT, f)
            text = open(p, encoding='utf-8', newline='').read()
            n = text.count(old)
            if n != 1:
                raise SystemExit(f'{f}: expected 1 match, found {n}: {old!r}')
            open(p, 'w', encoding='utf-8', newline='').write(text.replace(old, new))
            print(f'broke {f}: {old.strip()[:60]!r}')
    elif cmd == 'restore':
        record = json.load(open(os.path.join(BACKUP, 'sha.json')))
        for f, h in record.items():
            p = os.path.join(ROOT, f)
            shutil.copyfile(os.path.join(BACKUP, f.replace('\\', '_')), p)
            ok = sha(p) == h
            print(f'restored {f}: sha256 {sha(p)[:16]} {"identical" if ok else "DIFFERS"}')
            if not ok:
                raise SystemExit(1)

if __name__ == '__main__':
    main()
