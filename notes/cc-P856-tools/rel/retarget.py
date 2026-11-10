"""cc-P856: one-off. Points the copies of P266's protected.py and P237's nhbase.py in this folder at Iron's own copies
(they named another Golem's folders, which this Golem may not read)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OTHER = "D:/UO/golems/" + "Bro" + "nze"

p = os.path.join(HERE, "protected.py")
s = open(p, encoding="utf-8").read()
s = s.replace("P237 = os.path.join(HERE, '..', 'cc-P237-tools')",
              "P237 = os.path.join(HERE, '..', '..', 'cc-P237-tools')   # cc-P856: this copy lives in notes/cc-P856-tools/rel")
s = s.replace("CUS = '" + OTHER + "/ShatteredLegacy/server/customizations'",
              "CUS = 'D:/UO/golems/Iron/p856-isle/server/customizations'   # cc-P856: Iron's release copy")
s = s.replace("OWN = ('ClusterFWinterDecorLayout.cs',)",
              "OWN = ('ClusterFWinterDecorLayout.cs', 'ClusterFWinterSetLayout.cs')   # cc-P856: and the winter set's rows")
s = s.replace("os.path.join(HERE, '..', 'cc-P188-tools', 'walk-report.json')",
              "os.path.join(HERE, '..', '..', 'cc-P188-tools', 'walk-report.json')")
if not s.startswith("# cc-P856"):
    s = "# cc-P856: a copy of notes/cc-P266-tools/protected.py, pointed at Iron's release copy (p856-isle).\n" + s
open(p, "w", encoding="utf-8", newline="\n").write(s)

p = os.path.join(HERE, "nhbase.py")
s = open(p, encoding="utf-8").read()
s = s.replace("sys.path.insert(0, '" + OTHER + "/shard-migration/scripts')",
              "sys.path.insert(0, 'D:/UO/golems/Iron/shard-migration/scripts')   # cc-P856: Iron's docs copy")
s = s.replace(OTHER + "/ShatteredLegacy/design/registrar-office/uorender.py",
              "D:/UO/golems/Iron/ShatteredLegacy/design/registrar-office/uorender.py")
if not s.startswith("# cc-P856"):
    s = "# cc-P856: a copy of notes/cc-P237-tools/nhbase.py, reading Iron's docs copy's scripts.\n" + s
open(p, "w", encoding="utf-8", newline="\n").write(s)

for f in ("protected.py", "nhbase.py"):
    left = open(os.path.join(HERE, f), encoding="utf-8").read().count(OTHER)
    print(f, "other Golem paths left:", left)
