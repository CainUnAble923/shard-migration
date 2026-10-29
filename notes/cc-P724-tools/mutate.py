"""cc-P724 red-first: copies of the code copy's customizations with the change undone, so the new facts can be seen
failing (probe.sh with SRC=<copy>/<name>). Usage: python -P mutate.py <out-root>.
  noseed: SeedOn places no addons (facts 1 and 3 fail).
  onroad: the lighthouse moved onto the road to the dock (fact 2 fails)."""
import pathlib, shutil, sys

SRC = pathlib.Path("D:/UO/golems/Iron/ShatteredLegacy/server/customizations")
OUT = pathlib.Path(sys.argv[1])


def sub(root, rel, old, new):
    p = root / rel
    t = p.read_text(encoding="utf-8")
    if t.count(old) != 1:
        raise SystemExit(f"{rel}: {t.count(old)} matches for {old[:80]!r}")
    p.write_text(t.replace(old, new), encoding="utf-8", newline="\n")


for name in ("noseed", "onroad"):
    root = OUT / name
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(SRC / "Tutorial", root / "Tutorial")
sub(OUT / "noseed", "Tutorial/TutorialCorePlacement.cs", "addons = TutorialIsleAddons.Seed(map, false);", "addons = \"\";")
sub(OUT / "onroad", "Tutorial/TutorialIsleAddons.cs", "LighthouseSpot = new(6815, 3984, 0);", "LighthouseSpot = new(6815, 3991, 0);")
print("wrote", OUT)
