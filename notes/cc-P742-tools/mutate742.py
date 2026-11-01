"""cc-P742: one mutant copy of the code copy's Tutorial customizations per fix, each undoing that fix only, so each fact in
TutorialVisionChamberVerification can be seen failing. Writes <out>/<name>/Tutorial.
    python -P mutate742.py <code copy> <out folder>"""
import os
import shutil
import sys

code, out = sys.argv[1], sys.argv[2]
src = os.path.join(code, "server", "customizations", "Tutorial")
SCENE, ROOM, LAYOUT = "TutorialVisionScene.cs", "TutorialVisionChamber.cs", "TutorialVisionChamberLayout.cs"
MUTANTS = {
    # fact 1: the post at the north-west swapped for the corner piece
    "corner": [(LAYOUT, "[ 0x0244, 0, 0, 0 ]", "[ 0x0243, 0, 0, 0 ]")],
    # fact 2: the vision stays where the player stands
    "noenter": [(SCENE, "                EnterChamber(s);\n", "")],
    # fact 3: the Gem breaks with no flash
    "noflash": [(SCENE, "                    Screen(s, ScreenEffectType.LightFlash); // cc-P742: the light of the breaking Gem\n"
                        "                    SetLight(s, Flash);\n", "")],
    # facts 4 and 5: the old return, to the stones, hidden left as the chamber set it
    "oldreturn": [(SCENE, "Restore(pm, scene.Map, scene.Origin, scene.WasHidden);", "Restore(pm, scene.Map);")],
    # facts 4 and 5: the room left standing
    "keeproom": [(SCENE, "        LeaveChamber(scene);\n", "")],
    # fact 6: the save forgets the spot
    "nospot": [(SCENE, "            writer.Write(origin != null); // version 1", "            writer.Write(false); // version 1")],
    # fact 6b: a version 0 save read as version 1
    "v0": [(SCENE, "            if (version >= 1)\n", "            if (version >= 0)\n")],
    # fact 7: no login check
    "nologin": [(SCENE, "        TutorialVisionStore.Recover(pm);\n        SendOutOfChamber(pm);\n",
                 "        TutorialVisionStore.Recover(pm);\n")],
    # fact 8: every scene in slot 0
    "oneslot": [(ROOM, "            if (!taken.Contains(slot)) { return slot; }", "            return slot;")],
}
for name, edits in MUTANTS.items():
    dst = os.path.join(out, name, "Tutorial")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    for f, old, new in edits:
        p = os.path.join(dst, f)
        s = open(p, encoding="utf-8").read()
        assert s.count(old) == 1, (name, f, old)
        s = s.replace(old, new)
        open(p, "w", encoding="utf-8", newline="").write(s)
    print(name, "ok")
