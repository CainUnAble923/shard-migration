# cc-P267 WRITES the red run's breaks ("apply") and puts the files back ("restore": byte copies, SHA-256 checked, no
# P267-BREAK marker left). One break per fact, so the red run shows each gate failing on its own cause.
import hashlib, os, shutil, sys
SL = r'D:/ShatteredLegacy'
FILES = [SL + '/server/customizations/ClusterFHalloweenDecorSeeder.cs', SL + '/server/customizations/ClusterFSeasonalSwitch.cs',
         SL + '/server/customizations/ClusterFHalloweenDecorLayout.cs']
BAK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'breaks-backup')
BREAKS = [
    # 1. clear leaves the first tracked item in the world, still tracked (PlaceTwice...). The first version of this
    #    break untracked it but left it alive, and the second clear's stray sweep removed it: the safety net working,
    #    not the gate failing, so the fact stayed green in the first red run.
    (FILES[0], "                    Tracked.Remove(item.Serial);\n                    item.Delete();\n",
               "                    if (item != items.FirstOrDefault()) { Tracked.Remove(item.Serial); item.Delete(); } /* P267-BREAK */\n"),
    # 2. the window's end day is left out (TheSeasonWindow... theory, TheAutomaticCheck...)
    (FILES[1], "            return a <= b ? k >= a && k <= b : k >= a || k <= b;\n",
               "            return a <= b ? k >= a && k < b : k >= a || k < b; /* P267-BREAK */\n"),
    # 3. the saved serials are not read back (SurviveARestart)
    (FILES[1], "                    placed.Add(reader.ReadSerial());\n",
               "                    reader.ReadSerial(); /* P267-BREAK */\n"),
    # 4. a row moved onto Britain's banker tile (ThePlacementTable...)
    (FILES[2], '"britain", "Britain (west bank)", "Trammel", 1425, 1690, 0, 0x0A22, "a lantern", 0x000, "outside"),', None),
]
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
if sys.argv[1:] == ['apply']:
    os.makedirs(BAK, exist_ok=True)
    for f in FILES:
        shutil.copy2(f, os.path.join(BAK, os.path.basename(f)))
        open(os.path.join(BAK, os.path.basename(f) + '.sha256'), 'w').write(sha(f))
    for f, old, new in BREAKS:
        s = open(f, encoding='utf-8').read()
        if new is None:   # the layout break: replace the first britain lantern row's coordinates with the banker's
            import re
            m = re.search(r'new\("britain/lantern-1", "britain", "Britain \(west bank\)", "Trammel", (\d+), (\d+), (-?\d+),', s)
            assert m, 'no britain/lantern-1 row'
            s = s.replace(m.group(0), m.group(0).replace('%s, %s, %s,' % m.groups(), '1425, 1690, 0, /* P267-BREAK */'))
        else:
            assert s.count(old) == 1, (f, old)
            s = s.replace(old, new)
        open(f, 'w', encoding='utf-8', newline='\n').write(s)
    print('applied', len(BREAKS), 'breaks')
elif sys.argv[1:] == ['restore']:
    for f in FILES:
        b = os.path.join(BAK, os.path.basename(f))
        shutil.copy2(b, f)
        want = open(b + '.sha256').read().strip()
        assert sha(f) == want, f
        assert 'P267-BREAK' not in open(f, encoding='utf-8').read()
    print('restored', len(FILES), 'files, SHA-256 checked, no P267-BREAK left')
else:
    print('usage: breaks.py apply|restore')
