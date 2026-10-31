"""cc-P740 red-first (P732's way): copies of the code copy's Tutorial customizations with one part of the fix undone, so
the facts can be seen failing (probe.sh with SRC=<out-root>/<name>). Usage: python -P mutate.py <out-root>.
  olddark: P732's near-night dark (24) again.
  fastup: the first move ends the lie at once (no slow get-up, moves not refused while it plays).
  noline: no "You lie on the wet sand..." over the head.
  lightfirst: the light comes up as the get-up starts.
  windowsearly: the lines and windows come with the dawn, not after it.
  notable: the seed places no bandages on the farmhouse table.
  nowren: Wren says her farm line during the healing lesson (no bandages again).
  nohint: Wren never says where the bandages are.
  hoard: the table gives a stack every time.
  shortrise: P740's first try, a 3 s rise (the light could come up while the get-up, sent again for ClassicUO, plays)."""
import pathlib
import shutil
import sys

SRC = pathlib.Path("D:/UO/golems/Iron/ShatteredLegacy/server/customizations")
OUT = pathlib.Path(sys.argv[1])
W = "Tutorial/TutorialWake.cs"
F = "Tutorial/TutorialFarm.cs"

MUTANTS = {
    "olddark": (W, "    public const int DarkLight = 16;", "    public const int DarkLight = 24;"),
    "fastup": (W, "        if (now || pm.Deleted || pm.NetState == null || !pm.Alive)", "        if (true)"),
    "noline": (W, "            Overhead(pm, lie, LieOverheadLine);", "            // no line"),
    "lightfirst": (W, "        lie.Rising = 0;\n", "        lie.Rising = 0;\n        lie.Light = DawnLight[0];\n"),
    "windowsearly": (W, "        Dawn(pm, 0, () => AfterDawn(pm, lie));", "        Dawn(pm, 0);\n        AfterDawn(pm, lie);"),
    "notable": (F, "                new TutorialTableBandages().MoveToWorld(TableBandagesSpot, map);",
                "                // no table"),
    "nowren": (F, "hand.SayTo(pm, HealingOn(pm) ? WrenBandages(pm) : DoneLine);", "hand.SayTo(pm, DoneLine);"),
    "nohint": (F, "            if (said >= HintTimes || TutorialFarmhand", "            if (true || TutorialFarmhand"),
    "hoard": (F, "            if (taken >= TableTakes)", "            if (false)"),
    "shortrise": (W, "    public const int GetUpSeconds = 4;", "    public const int GetUpSeconds = 3;"),
}


def sub(root, rel, old, new):
    p = root / rel
    t = p.read_text(encoding="utf-8")
    if t.count(old) != 1:
        raise SystemExit(f"{rel}: {t.count(old)} matches for {old[:80]!r}")
    p.write_text(t.replace(old, new), encoding="utf-8", newline="\n")


for name, (rel, old, new) in MUTANTS.items():
    root = OUT / name
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(SRC / "Tutorial", root / "Tutorial")
    sub(root, rel, old, new)
print("wrote", OUT, ", ".join(MUTANTS))
