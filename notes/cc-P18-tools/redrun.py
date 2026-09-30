"""Deliberate breaks for the red runs, each aimed at one fact. `apply A|B` backs up and breaks;
`restore` puts every file back from its backup and checks the SHA-256 matches the one taken first."""
import hashlib
import json
import os
import shutil
import sys

ROOT = r'D:/ShatteredLegacy/'
SCR = r'C:/Users/ckfle/AppData/Local/Temp/claude/D--UO-shard-migration/e1270c9e-f74d-4ed0-afa7-c526ef24aa10/scratchpad/red/'
C = 'server/customizations/'

BREAKS = {
    'A': [
        # F-7 fact 1: guild data per account again (every character keyed to one record).
        (C + 'ClusterFAccountData.cs',
         '        GetOrCreate(m.Account).GetOrCreateGuildData(m.Serial);',
         '        GetOrCreate(m.Account).GetOrCreateGuildData((Serial)0u); // RED A'),
        (C + 'ClusterFAccountData.cs',
         '        m.Account is { } acct ? Get(acct)?.GetGuildData(m.Serial) : null;\n\n    /// <summary>This character\'s guild starter',
         '        m.Account is { } acct ? Get(acct)?.GetGuildData((Serial)0u) : null; // RED A\n\n    /// <summary>This character\'s guild starter'),
        # F-7 fact 6: the seeder never sees the stone already there.
        (C + 'ClusterFResetStone.cs',
         '            var existing = FindInNewHaven(map);',
         '            ResetStone? existing = null; // RED A'),
        # F-5 fact 2: the duration one hour longer.
        (C + 'ClusterFYoungPlayer.cs',
         'public static readonly TimeSpan Duration = TimeSpan.FromHours(336.0);',
         'public static readonly TimeSpan Duration = TimeSpan.FromHours(337.0); // RED A'),
        # F-5 fact 3: the phrase matched exactly, not loosely.
        (C + 'ClusterFYoungPlayer.cs',
         '        return Normalize(speech) == Normalize(GrowUpPhrase);',
         '        return speech == GrowUpPhrase; // RED A'),
    ],
    'B': [
        # F-7 fact 2: an old save's account guild data given to a character (serial 0).
        (C + 'ClusterFAccountData.cs',
         '        DroppedAccountGuildData = !legacy.IsEmpty || apprenticeFlags > 0;',
         '        DroppedAccountGuildData = !legacy.IsEmpty || apprenticeFlags > 0;\n        if (!legacy.IsEmpty) _guildData[0] = legacy; // RED B'),
        # F-7 fact 3: Apprentice marks neither written nor read (symmetric, so the byte count still agrees).
        (C + 'ClusterFAccountData.cs',
         '        w.Write(ApprenticeGuilds.Count);\n        foreach (var key in ApprenticeGuilds) w.Write(key);',
         '        w.Write(0); // RED B'),
        # F-7 fact 4: the reset forgets to clear exploration.
        (C + 'ClusterFDevTools.cs',
         '            data.ClearExploration();',
         '            // data.ClearExploration(); // RED B'),
        # F-7 fact 5: [ResetMyAccount honours an account name.
        (C + 'ClusterFDevTools.cs',
         '    private static void OnResetMyAccountCommand(CommandEventArgs e) => OpenSelfReset(e.Mobile);',
         '    private static void OnResetMyAccountCommand(CommandEventArgs e) // RED B\n'
         '    {\n'
         '        if (e.Length > 0 && Accounts.GetAccount(e.GetString(0)) is { } other)\n'
         '            OpenReset(e.Mobile, e.Mobile as PlayerMobile, other, selfService: true);\n'
         '        else\n'
         '            OpenSelfReset(e.Mobile);\n'
         '    }'),
        # F-5 fact 1: pinned's skill-total rule back (the patch skipped by name).
        ('docker/uo/apply-patches.sh',
         'apply_patch "$PATCHES/PlayerMobile-young-time-only.patch"',
         'SKIPPED_PATCHES+=("PlayerMobile-young-time-only.patch") # RED B'),
        # F-5 countdown: hours only.
        (C + 'ClusterFYoungPlayer.cs',
         '        return days == 0 ? h : hours == 0 ? d : $"{d} and {h}";',
         '        return $"{(int)remaining.TotalHours} hours"; // RED B'),
    ],
}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    os.makedirs(SCR, exist_ok=True)
    manifest = SCR + 'manifest.json'
    cmd = sys.argv[1]
    if cmd == 'apply':
        which = sys.argv[2]
        files = sorted({f for f, _, _ in BREAKS[which]})
        m = {}
        for f in files:
            src = ROOT + f
            bak = SCR + f.replace('/', '__')
            shutil.copyfile(src, bak)
            m[f] = sha(src)
        json.dump(m, open(manifest, 'w'))
        for f, old, new in BREAKS[which]:
            p = ROOT + f
            s = open(p, encoding='utf-8', newline='').read()
            assert s.count(old) == 1, (f, old[:60], s.count(old))
            open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
            print('broke', f, '|', new.splitlines()[0].strip()[:90])
    elif cmd == 'restore':
        m = json.load(open(manifest))
        for f, h in m.items():
            shutil.copyfile(SCR + f.replace('/', '__'), ROOT + f)
            now = sha(ROOT + f)
            print('restored', f, 'sha256', now[:16], 'OK' if now == h else 'MISMATCH')
            assert now == h
        os.remove(manifest)


main()
