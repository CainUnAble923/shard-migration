# cc-P31 red runs, in the form of notes/cc-P19-tools/breaks.py. WRITES to D:\ShatteredLegacy\server: applies
# deliberate breaks, each marked "P31-BREAK" (or, for A's reverted generated files, the P19 bytes from git HEAD),
# after saving byte copies; "restore" puts the copies back and checks SHA-256 and that no marker is left.
# Usage: python breaks.py A|B|C|restore
import hashlib, os, shutil, subprocess, sys
REPO = r'D:/ShatteredLegacy'
ROOT = REPO + '/server/'
BK = os.path.join(os.environ.get('P31_BACKUP', r'C:/Users/ckfle/AppData/Local/Temp/claude/D--UO-shard-migration/5fc896b7-21b9-490b-879f-c469fdb6134a/scratchpad/p31-backup'))
FILES = ['customizations/ClusterFRegistrarOfficeLayout.cs', 'customizations/ClusterFRegistrarOfficeSeeder.cs',
         'tests/Misc/RegistrarOfficeLayoutDesignCopy.cs']
SEEDER = 'customizations/ClusterFRegistrarOfficeSeeder.cs'
LAYOUT = 'customizations/ClusterFRegistrarOfficeLayout.cs'
# A: the layout not regenerated (both generated files as cc-P19 left them, git HEAD), so facts 1, 2, 4 and 6
#    see the 18-component office; and the dry run deletes (fact 7).
REVERT_A = ['customizations/ClusterFRegistrarOfficeLayout.cs', 'tests/Misc/RegistrarOfficeLayoutDesignCopy.cs']
BREAKS = {
    'A': [
        (SEEDER, '            if (!dryRun)\n            {\n                foreach (var addon in found)',
                 '            if (true) // P31-BREAK\n            {\n                foreach (var addon in found)'),
    ],
    'B': [
        # 3: the candelabra on the Registrar's tile, in the area table only (2nd occurrence)
        (LAYOUT, 'new("office", 0x0B26, "candelabra", 3461, 2602, 18),',
                 'new("office", 0x0B26, "candelabra", 3459, 2601, 18), // P31-BREAK', 2),
        # 6: replace deletes nothing
        (SEEDER, '                    addon.Delete();', '                    // P31-BREAK addon.Delete();'),
    ],
    'C': [
        # 6: replace also deletes every other loose item in the house box (statics, doors, anything)
        (SEEDER, '            if (!dryRun)\n            {\n                foreach (var addon in found)',
                 '            if (!dryRun)\n            {\n'
                 '                var loose = new List<Item>(); // P31-BREAK\n'
                 '                foreach (var it in World.Items.Values)\n'
                 '                {\n'
                 '                    if (it.Map == Map.Trammel && it.Parent == null && it is not AddonComponent && it is not BaseAddon &&\n'
                 '                        it.X >= 3448 && it.X <= 3468 && it.Y >= 2590 && it.Y <= 2608)\n'
                 '                    {\n'
                 '                        loose.Add(it);\n'
                 '                    }\n'
                 '                }\n'
                 '                foreach (var it in loose)\n'
                 '                {\n'
                 '                    it.Delete();\n'
                 '                }\n'
                 '                foreach (var addon in found)'),
    ],
}
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
mode = sys.argv[1]
if mode == 'restore':
    for f in FILES:
        src = os.path.join(BK, f.replace('/', '__'))
        shutil.copyfile(src, ROOT + f)
        a, b = sha(ROOT + f), sha(src)
        assert a == b, f
        assert 'P31-BREAK' not in open(ROOT + f).read(), f
        print('restored', f, a)
else:
    os.makedirs(BK, exist_ok=True)
    for f in FILES:
        dst = os.path.join(BK, f.replace('/', '__'))
        if not os.path.exists(dst):
            shutil.copyfile(ROOT + f, dst)
        print('backup', f, sha(dst))
    if mode == 'A':
        for f in REVERT_A:
            data = subprocess.run(['git', '--no-optional-locks', '-C', REPO, 'show', 'HEAD:server/' + f],
                                  capture_output=True, check=True).stdout
            open(ROOT + f, 'wb').write(data)
            print('reverted to HEAD (cc-P19)', f, hashlib.sha256(data).hexdigest())
    for f, old, new, *nth in BREAKS[mode]:
        s = open(ROOT + f, newline='').read()
        n = nth[0] if nth else 1
        assert s.count(old) == (2 if nth else 1), (f, old, s.count(old))
        i = -1
        for _ in range(n):
            i = s.index(old, i + 1)
        open(ROOT + f, 'w', newline='').write(s[:i] + new + s[i + len(old):])
        print('broke', f, '->', new.splitlines()[0].strip())
