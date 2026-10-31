"""cc-P751: one mutant copy of the code copy's Tutorial customizations per fix, each undoing that fix only, so each new
fact (TutorialIsleReviewFixesVerification) can be seen failing. Writes <out>/<name>/Tutorial.
    python -I mutate751.py <code copy> <out folder>"""
import os, shutil, sys
code, out = sys.argv[1], sys.argv[2]
src = os.path.join(code, 'server', 'customizations', 'Tutorial')
MUTANTS = {
    'fence': [('TutorialIsleFarmLayout.cs', '(0x0838, 6677, 3967, 0), // wooden post', '(0x0835, 6677, 3967, 0), // wooden fence')],
    'hearth': [('TutorialIsleFarmLayout.cs', '(0x0967, 6702, 3973, 7), // fireplace', '(0x0959, 6700, 3973, 7), // fireplace'),
               ('TutorialIsleFarmLayout.cs', '(0x0961, 6703, 3973, 7), // fireplace', '(0x0953, 6700, 3974, 7), // fireplace')],
    'door': [('TutorialFarm.cs', 'new DarkWoodDoor(DoorFacing.WestCCW);', 'new DarkWoodDoor(DoorFacing.WestCW);'),
             ('TutorialFarm.cs', 'if (isleDoor != null && isleDoor.ClosedId == IsleDoorClosedId) { present++; }',
              'if (isleDoor != null) { present++; }')],
    'lodgesign': [('TutorialCorePlacement.cs', '        (SignpostId, LodgeSign, LodgeSignName) // cc-P751\n', '')],
}
for name, edits in MUTANTS.items():
    dst = os.path.join(out, name, 'Tutorial')
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    for f, old, new in edits:
        p = os.path.join(dst, f)
        s = open(p, encoding='utf-8').read()
        assert s.count(old) == 1, (name, f, old)
        s = s.replace(old, new)
        if name == 'lodgesign':
            s = s.replace('"practice bank box"),\n', '"practice bank box")\n')
        open(p, 'w', encoding='utf-8', newline='').write(s)
    print(name, 'ok')
