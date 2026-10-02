# cc-P29: deliberate breaks for the red run of Parts D, E and F, with byte-exact restore checked by SHA-256.
#   python mutate.py apply R2     back up each target, then apply its breaks (refuses if a break does not match once)
#   python mutate.py restore R2   put the backups back and compare hashes with the pre-break ones
import hashlib, json, os, shutil, sys

SHARD = r'D:/ShatteredLegacy/server/customizations'
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mutate-backup')

BREAKS = {
    'R2': [
        # D1: the dry run places anyway -> ADryRunPlacesNothing
        ('ClusterFFountainStepsSeeder.cs', '            if (!dryRun)\n            {\n                var stone',
         '            if (true)\n            {\n                var stone'),
        # D2: an existing stone is never found -> RunTwiceItLaysTwelveStonesInOneChain (twice the stones)
        ('ClusterFFountainStepsSeeder.cs', '            if (item.X == p.X && item.Y == p.Y && IsStep(item))',
         '            if (false && item.X == p.X && item.Y == p.Y && IsStep(item))'),
        # D3: the line stops five stones short, at 1123, 962 (4 from the fountain) -> ALuckyCoinThrownFromTheEndStone...
        ('ClusterFFountainStepsSeeder.cs',
         '        new(1123, 962), new(1123, 961), new(1122, 961), new(1122, 960), new(1121, 960), new(1121, 959)\n',
         '        new(1123, 962)\n'),
        # E1: the set writes the wrong key -> SettingArtificersTo15000MakesAMasterArtificer
        ('ClusterFGuildStandingCommand.cs', '            guild.GuildReputation[key] = amount.Value;',
         '            guild.GuildReputation[key + "x"] = amount.Value;'),
        # E2: an unknown key falls back to artificers -> AnUnknownGuildKeyIsRefusedWithTheValidKeys
        ('ClusterFGuildStandingCommand.cs', '        key = null;\n        return false;',
         '        key = "artificers";\n        return true;'),
        # E3: mining gets the Directory's generic ladder -> WithNoAmountItReadsStandingAndTheGuildsOwnRankBack
        ('ClusterFGuildStandingCommand.cs', '        key == "mining"\n', '        key == "no-such-guild"\n'),
        # F: the old label -> TheImbuingTableEntrySaysImbueItem
        ('ArtificersGuildmaster.cs', '    public const int LabelCliloc = 1114267;', '    public const int LabelCliloc = 6277;'),
    ],
}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main(cmd, run):
    files = sorted({f for f, _, _ in BREAKS[run]})
    os.makedirs(BACKUP, exist_ok=True)
    manifest = os.path.join(BACKUP, f'{run}.json')
    if cmd == 'apply':
        hashes = {}
        for f in files:
            src = os.path.join(SHARD, f)
            shutil.copy2(src, os.path.join(BACKUP, f))
            hashes[f] = sha(src)
        for f, old, new in BREAKS[run]:
            p = os.path.join(SHARD, f)
            s = open(p, 'rb').read().decode('utf-8')
            if s.count(old) != 1:
                raise SystemExit(f'{f}: break does not match exactly once: {old!r}')
            open(p, 'wb').write(s.replace(old, new).encode('utf-8'))
            print('broke', f, '|', new.strip()[:70])
        json.dump(hashes, open(manifest, 'w'), indent=1)
    else:
        hashes = json.load(open(manifest))
        for f in files:
            dst = os.path.join(SHARD, f)
            shutil.copy2(os.path.join(BACKUP, f), dst)
            print(f, 'identical' if sha(dst) == hashes[f] else 'DIFFERS', sha(dst)[:16])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
