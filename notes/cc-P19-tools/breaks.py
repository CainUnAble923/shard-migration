# cc-P19 red runs. WRITES to D:\ShatteredLegacy\server: applies deliberate breaks to the sources, each marked
# with "P19-BREAK", after saving byte copies; "restore" puts the copies back and checks SHA-256 and that no marker
# is left. Usage: python breaks.py A|B|restore
import hashlib, os, shutil, sys
ROOT = r'D:/ShatteredLegacy/server/'
BK = os.path.join(os.environ.get('P19_BACKUP', r'C:/Users/ckfle/AppData/Local/Temp/claude/D--UO-shard-migration/580156ec-040a-4874-9707-4223d208f4a2/scratchpad/p19-backup'))
FILES = ['customizations/ClusterFRegistrarOfficeLayout.cs', 'customizations/ClusterFMineCampSeeder.cs',
         'customizations/ClusterFRegistrarOfficeSeeder.cs', 'customizations/ClusterFNewHavenSeeder.cs']
BREAKS = {
    'A': [
        # 1: the hourglass 1 z higher in the area table (2nd occurrence) than in the design file
        ('customizations/ClusterFRegistrarOfficeLayout.cs',
         'new("office", 0x1810, "hourglass", 3458, 2600, 27),',
         'new("office", 0x1810, "hourglass", 3458, 2600, 28), // P19-BREAK', 2),
        # 2: the placer never sees an addon already on the world
        ('customizations/ClusterFMineCampSeeder.cs',
         'var existing = FindTent(type);',
         'var existing = (BaseAddon)null; // P19-BREAK'),
        # 4: the signs are never named
        ('customizations/ClusterFRegistrarOfficeSeeder.cs',
         'c.Name = SignName;',
         '// P19-BREAK c.Name = SignName;'),
        # 5: world load no longer accepts her old facing
        ('customizations/ClusterFNewHavenSeeder.cs',
         '.WasAt(3459, 2601, 18, Direction.North),',
         '.WasAt(3459, 2601, 18), // P19-BREAK'),
    ],
    'B': [
        # 3: the flowerpot moved onto the tile the doorway door swings into (3457,2598), in the area table only
        ('customizations/ClusterFRegistrarOfficeLayout.cs',
         'new("office", 0x11CA, "flowerpot", 3460, 2597, 18),',
         'new("office", 0x11CA, "flowerpot", 3457, 2598, 18), // P19-BREAK', 2),
        # 3b: the globe moved onto the Registrar's tile, in the area table only
        ('customizations/ClusterFRegistrarOfficeLayout.cs',
         'new("office", 0x1047, "globe", 3461, 2598, 18),',
         'new("office", 0x1047, "globe", 3459, 2601, 18), // P19-BREAK', 2),
    ],
}
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
mode = sys.argv[1]
if mode == 'restore':
    for f in FILES:
        shutil.copyfile(os.path.join(BK, f.replace('/', '__')), ROOT + f)
        a, b = sha(ROOT + f), sha(os.path.join(BK, f.replace('/', '__')))
        assert a == b, f
        assert 'P19-BREAK' not in open(ROOT + f).read(), f
        print('restored', f, a)
else:
    os.makedirs(BK, exist_ok=True)
    for f in FILES:
        dst = os.path.join(BK, f.replace('/', '__'))
        if not os.path.exists(dst):
            shutil.copyfile(ROOT + f, dst)
        print('backup', f, sha(dst))
    # An entry may name which occurrence to replace (the layout table lists a component twice: in Components,
    # in design order, and in its area's array, which is what the addon is built from).
    for f, old, new, *nth in BREAKS[mode]:
        s = open(ROOT + f, newline='').read()
        n = nth[0] if nth else 1
        assert s.count(old) == (2 if nth else 1), (f, old, s.count(old))
        i = -1
        for _ in range(n):
            i = s.index(old, i + 1)
        open(ROOT + f, 'w', newline='').write(s[:i] + new + s[i + len(old):])
        print('broke', f, '->', new.splitlines()[0].strip())
