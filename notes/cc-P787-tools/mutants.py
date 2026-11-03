# cc-P787: one mutant per fact. Copies the Beekeeping folder to <out>/m<n>, applies one break (the old text must be
# found exactly once), and prints the probe command for it. Usage: python -P mutants.py <src> <out>
import os, shutil, sys
SRC, OUT = sys.argv[1], sys.argv[2]
M = {
  1: ("BeekeepingTable.cs", "            else if (Forbidden(type) is { } why)", "            else if (false && Forbidden(type) is { } why)",
      "BeekeepingTable.cs", "            if (type == null || !Sellable.Contains(type))", "            if (type == null)"),
  2: ("HouseBeehive.cs", "        if (HivesIn(house) >= T.MaxHivesPerHouse)", "        if (false)"),
  3: ("HouseBeehive.cs", "        NextCheck = now + TimeSpan.FromHours(t.CheckHours);", "        NextCheck = NextCheck;"),
  4: ("HouseBeehive.cs", "p.PlantStatus >= Plants.PlantStatus.Plant && p.PlantStatus <= Plants.PlantStatus.DecorativePlant", "true"),
  5: ("HouseBeehive.cs", "                Parasites = false;\n                return \"The poison", "                return \"The poison"),
  6: ("HouseBeehive.cs", "            Leave();\n", "            Population = 1;\n"),
  7: ("HouseBeehive.cs", "        Honey = 0;\n        Wax = 0;\n        tool.UseOnce(from);", "        Honey = 0;\n        Wax = 0;"),
  8: ("BeekeepingSystem.cs", "        foreach (var c in t.Candles)", "        foreach (var c in t.Candles.Take(0))"),
  10: ("WildBeehive.cs", "            if (FindAt(map, spot.Location) != null)", "            if (false)"),
  11: ("HouseBeehive.cs", "    private void AfterDeserialization()\n    {\n        _all.Add(this);", "    private void AfterDeserialization()\n    {\n        _all.Add(this);\n        _honey = 0;"),
}
for n, spec in M.items():
    d = os.path.join(OUT, f"m{n}")
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(SRC, d)
    for i in range(0, len(spec), 3):
        f, old, new = spec[i:i+3]
        p = os.path.join(d, f)
        s = open(p, encoding="utf-8", newline="").read()
        assert s.count(old) == 1, (n, f, old, s.count(old))
        open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
    print(f"m{n} ready")
