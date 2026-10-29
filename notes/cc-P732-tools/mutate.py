"""cc-P732 red-first: copies of the code copy's Tutorial customizations with one part of the fix undone, so the facts can
be seen failing (probe.sh with SRC=<out-root>/<name>). Usage: python -P mutate.py <out-root>.
  frozen: the trainee frozen while lying again (P728).
  noresend: the pose sent once only.
  earlydawn: the light comes up while they still lie (P728's 2 s and 4 s)."""
import pathlib
import shutil
import sys

SRC = pathlib.Path("D:/UO/golems/Iron/ShatteredLegacy/server/customizations")
OUT = pathlib.Path(sys.argv[1])


def sub(root, rel, old, new):
    p = root / rel
    t = p.read_text(encoding="utf-8")
    if t.count(old) != 1:
        raise SystemExit(f"{rel}: {t.count(old)} matches for {old[:80]!r}")
    p.write_text(t.replace(old, new), encoding="utf-8", newline="\n")


for name in ("frozen", "noresend", "earlydawn"):
    root = OUT / name
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(SRC / "Tutorial", root / "Tutorial")
W = "Tutorial/TutorialWake.cs"
sub(OUT / "frozen", W, "        _dawn.Remove(pm.Serial);\n        pm.CheckLightLevels(true);\n        HoldPose(pm, lie);",
    "        _dawn.Remove(pm.Serial);\n        pm.Frozen = true;\n        pm.CheckLightLevels(true);\n        HoldPose(pm, lie);")
sub(OUT / "noresend", W, "        if (s % HoldEverySeconds == 1)\n        {\n            HoldPose(pm, lie);\n        }",
    "        if (s == -1)\n        {\n            HoldPose(pm, lie);\n        }")
sub(OUT / "earlydawn", W, "        if (s == 1)\n        {\n            pm.CheckLightLevels(true);\n        }",
    "        if (s == 1)\n        {\n            pm.CheckLightLevels(true);\n        }\n\n"
    "        if (s == 2) { lie.Light = 14; pm.CheckLightLevels(true); }\n"
    "        else if (s == 4) { lie.Light = 6; pm.CheckLightLevels(true); }")
print("wrote", OUT)
