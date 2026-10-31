"""cc-P741: four mutant copies of the Tutorial customizations, each undoing one change, for the red runs of
TutorialIsleCoastVerification (probe.sh with SRC=<mutant>). python -P mutate741.py <out folder>"""
import os, shutil, subprocess, sys

CODE = 'D:/UO/golems/Iron/ShatteredLegacy'
TUT = os.path.join(CODE, 'server', 'customizations', 'Tutorial')
out = sys.argv[1]

MUTANTS = {
    # 1: the old half wreck is never swapped
    'nowreckswap': ('TutorialIsleAddons.cs',
                    'if (item is WakeningIsleShipwreckAddon w && !w.Deleted &&',
                    'if (false && item is WakeningIsleShipwreckAddon w && !w.Deleted &&'),
    # 3: a farm laid before the move is left as it was
    'nofarmmove': ('TutorialFarm.cs',
                   '        public static int MoveFromOldLayout(Map map)\n        {\n',
                   '        public static int MoveFromOldLayout(Map map)\n        {\n            if (map != null) { return 0; }\n'),
    # 4: the old chat signpost stays where it was
    'nochatmove': ('TutorialCorePlacement.cs',
                   '    public static int MoveChatSignpost(Map map)\n    {\n',
                   '    public static int MoveChatSignpost(Map map)\n    {\n        if (map != null) { return 0; }\n'),
}
for name, (f, old, new) in MUTANTS.items():
    d = os.path.join(out, name, 'Tutorial')
    shutil.rmtree(os.path.dirname(d), ignore_errors=True)
    shutil.copytree(TUT, d)
    p = os.path.join(d, f)
    s = open(p, encoding='utf-8').read()
    assert old in s, (name, old)
    open(p, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new, 1))
    print(name, 'written')
# 2: P720's farm layout (the farmhouse west of the field, six full rows of crops)
d = os.path.join(out, 'oldlayout', 'Tutorial')
shutil.rmtree(os.path.dirname(d), ignore_errors=True)
shutil.copytree(TUT, d)
old = subprocess.run(['git', '-C', CODE, 'show', 'HEAD:server/customizations/Tutorial/TutorialIsleFarmLayout.cs'],
                     capture_output=True, text=True, encoding='utf-8').stdout
old = old.replace('public static readonly Point3D OldDoorSpot = new(6694, 3975, 13);',
                  'public static readonly Point3D[] OldDoorSpots = [new(6694, 3975, 13)];')
open(os.path.join(d, 'TutorialIsleFarmLayout.cs'), 'w', encoding='utf-8', newline='\n').write(old)
print('oldlayout written')
