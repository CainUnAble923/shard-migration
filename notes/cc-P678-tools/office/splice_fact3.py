r"""cc-P678 WRITES: replaces fact 3 of RegistrarOfficeVerification.cs (the old house's doors) with fact3.cs.txt."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
P = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Misc/RegistrarOfficeVerification.cs"
t = open(P, encoding="utf-8").read()
a = t.index("    [Fact]\n    public void NoComponentSitsOnADoorItsSwingOrTheRegistrarTile()")
b = t.index("    // ---------------------------------------------------------------- 4")
new = open(os.path.join(HERE, "fact3.cs.txt"), encoding="utf-8").read()
t = t[:a] + new + "\n" + t[b:]
open(P, "w", encoding="utf-8", newline="").write(t)
print("spliced", b - a, "->", len(new))
