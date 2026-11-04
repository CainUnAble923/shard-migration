# cc-P793: makes one mutant folder per rule of the Peacock, each undoing that rule, for the red-first check.
# Usage: python -P mutate793.py <ShatteredLegacy\server> <out folder>
# Each mutant folder holds Mounts\ (the three Peacock files), ShardBodyTypes.cs and shrink.json, for probe793.sh to mount.
import shutil
import sys
from pathlib import Path

server = Path(sys.argv[1])
out = Path(sys.argv[2])

BIRD = "Mounts/Peacock.cs"
TABLE = "Mounts/PeacockTable.cs"
SYS = "Mounts/PeacockSystem.cs"
TYPES = "ShardBodyTypes.cs"
ROWS = "shrink.json"

# name: (file, old, new): the old text must occur exactly once.
MUTANTS = {
    # Body 1440 left untyped (Empty): no idle, and it could open doors.
    "nobodyrow": (TYPES, '            (1440, BodyType.Animal, "peacock (cc-P793: the tamable mount)")\n', "            (2133, BodyType.Animal, \"again\")\n"),
    # The wrong mount item: another creature under the rider.
    "wrongitem": (BIRD, "MountItemId = 0x3ECF;", "MountItemId = 0x3ECE;"),
    # Not tamable.
    "notame": (BIRD, "        Tamable = true;\n", "        Tamable = false;\n"),
    # A mount that cannot be ridden.
    "noride": (BIRD, '    public override string DefaultName => "a peacock";\n', '    public override void OnDoubleClick(Mobile from) { }\n    public override string DefaultName => "a peacock";\n'),
    # Eats meat, not fruit and grain.
    "food": (BIRD, "FoodType.FruitsAndVeggies | FoodType.GrainsAndHay", "FoodType.Meat"),
    # The taming numbers ignore the table.
    "nocfg": (BIRD, "        MinTameSkill = t.MinTameSkill;\n", "        MinTameSkill = 29.1;\n"),
    # Nothing is saved: a hand-written Serialize and Deserialize in place of the generator's.
    "nosave": (BIRD, "[SerializationGenerator(0, false)]\npublic partial class Peacock : BaseMount\n{\n", "public partial class Peacock : BaseMount\n{\n    public Peacock(Serial serial) : base(serial) { }\n    public override void Serialize(IGenericWriter writer) { }\n    public override void Deserialize(IGenericReader reader) { }\n\n"),
    # It carries gold: something it grants.
    "loot": (BIRD, "        Fame = t.Fame;\n", "        PackGold(10);\n        Fame = t.Fame;\n"),
    # No figurine row: the leash falls back on the virtue stone.
    "noshrink": (ROWS, '  "0x05a0": "0xA0C0"\n', ""),
    # The seed does not look for what is there.
    "noidem": (SYS, "            if (FindAt(map, spot.Location) != null)\n            {\n                present++;", "            if (false)\n            {\n                present++;"),
    # A dry run places.
    "dryplaces": (SYS, "            if (!dryRun)\n", "            if (true)\n"),
    # Enabled is ignored.
    "offignored": (SYS, "        if (!t.Enabled)\n", "        if (false)\n"),
    # The spawner keeps pinned's default home range.
    "nohome": (SYS, "                spawner.HomeRange = spot.HomeRange;\n", ""),
    # A bad slot count is accepted.
    "novalidate": (TABLE, '        Range(errors, "controlSlots", t.ControlSlots, t.ControlSlots, 1, 5);\n', ""),
    # A meadow on the fenced rooster island.
    "fenced": (TABLE, "X = 1986, Y = 2244, Z = 0", "X = 2900, Y = 1400, Z = 0"),
}


def base(folder):
    (folder / "Mounts").mkdir(parents=True)
    m = server / "customizations/Mobiles/Mounts"
    for name in ("Peacock.cs", "PeacockTable.cs", "PeacockSystem.cs"):
        shutil.copy(m / name, folder / "Mounts" / name)
    shutil.copy(server / "customizations/Mobiles/Evo/ShardBodyTypes.cs", folder / "ShardBodyTypes.cs")
    shutil.copy(server / "data/shrink.json", folder / "shrink.json")


if out.exists():
    shutil.rmtree(out)
base(out / "_base")
for name, (rel, old, new) in MUTANTS.items():
    d = out / name
    base(d)
    p = d / rel
    s = p.read_bytes().decode("utf-8")
    assert s.count(old) == 1, name
    p.write_bytes(s.replace(old, new).encode("utf-8"))
print(len(MUTANTS), "mutants in", out)
