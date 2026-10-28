r"""cc-P678 WRITES office/gen_office_layout.py: the cc-P31 generator with ROOT at the Iron code copy and GEN naming
the copy (so the generated headers say which script wrote them). Nothing else changes.
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(HERE, "..", "..", "cc-P31-tools", "gen_office_layout.py")
t = open(src).read()
old_root = "ROOT = r'D:/" + "ShatteredLegacy'"
assert old_root in t and "GEN = 'notes/cc-P31-tools/gen_office_layout.py'" in t
t = t.replace(old_root, "ROOT = r'D:/UO/golems/Iron/ShatteredLegacy'")
t = t.replace("GEN = 'notes/cc-P31-tools/gen_office_layout.py'", "GEN = 'notes/cc-P678-tools/office/gen_office_layout.py'")
t = "# cc-P678: a copy of notes/cc-P31-tools/gen_office_layout.py, ROOT at the Iron code copy, GEN at this path.\n" + t
open(os.path.join(HERE, "gen_office_layout.py"), "w", newline="\n").write(t)
print("wrote gen_office_layout.py")
