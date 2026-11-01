"""cc-P761: one mutant per new fact, each undoing one part of the Stranger's outfit. Writes <out>/<name>/Tutorial.
Usage: python mutate761.py <code copy customizations> <out folder>"""
import pathlib, shutil, sys
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
MUTANTS = {
    "named": ('new TutorialVisionFigure("") { Hue = 0x83EA };', 'new TutorialVisionFigure("the Stranger") { Hue = 0x83EA };'),
    "nocowl": ('        f.AddItem(new TutorialVisionProp(TutorialVisionScene.CowlId) { Hue = hue, Layer = Layer.Helm });\n', ''),
    "fixedhue": ('TutorialVisionProp(TutorialVisionScene.CloakId) { Hue = hue,', 'TutorialVisionProp(TutorialVisionScene.CloakId) { Hue = TutorialVisionScene.StrangerHue,'),
}
for name, (a, b) in MUTANTS.items():
    d = out / name / "Tutorial"
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(src / "Tutorial", d)
    f = d / "TutorialVisionScene.cs"
    s = f.read_text(encoding="utf-8")
    assert s.count(a) == 1, (name, a)
    f.write_text(s.replace(a, b), encoding="utf-8", newline="")
    print("mutant", name)
