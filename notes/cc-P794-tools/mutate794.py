# cc-P794: makes one mutant of EtherealLooks.cs per rule, each undoing that rule, for the red-first check.
# Usage: python -P mutate794.py <EtherealLooks.cs> <out folder>
import shutil
import sys
from pathlib import Path

src = Path(sys.argv[1])
out = Path(sys.argv[2])
text = src.read_bytes().decode("utf-8")

# name: (old, new): the old text must occur exactly once.
MUTANTS = {
    # Pinned's translucent hue, not solid.
    "translucent": ("    public override int EtherealHue => EtherealLooks.Hue;\n", ""),
    # The slots ignore the setting.
    "slots": ("    public override int FollowerSlots => EtherealLooks.FollowerSlots;\n", ""),
    # Pinned's single click: "Veteran Reward".
    "click": ("    public override void OnSingleClick(Mobile from) => LabelTo(from, DefaultName);\n", ""),
    # It cannot be cast.
    "nocast": ("    public override int FollowerSlots => EtherealLooks.FollowerSlots;\n", "    public override int FollowerSlots => EtherealLooks.FollowerSlots;\n\n    public override bool Validate(Mobile from) => false;\n"),
    # The wrong mount items and statuettes, one each.
    "wrongmount": ("public EtherealPeacock() : base(0xA0C0, 0x3ECF)", "public EtherealPeacock() : base(0xA0C0, 0x3ECE)"),
    "wrongdark": ("public EtherealTiger() : base(0x9844, 0x3EC8)", "public EtherealTiger() : base(0x9844, 0x3EC7)"),
    "wrongart": ("public EtherealWindrunner() : base(0x9ED5, 0x3ECC)", "public EtherealWindrunner() : base(0x579, 0x3ECC)"),
    # A wrong name.
    "name": ('    public override string DefaultName => "an ethereal lasher statuette";', '    public override string DefaultName => "a lasher";'),
    # Nothing is saved.
    "nosave": ("[SerializationGenerator(0, false)]\npublic partial class EtherealBoura : EtherealLook\n{\n", "public partial class EtherealBoura : EtherealLook\n{\n    public EtherealBoura(Serial serial) : base(serial) { }\n    public override void Serialize(IGenericWriter writer) { }\n    public override void Deserialize(IGenericReader reader) { }\n\n"),
    # It is lost when its rider dies.
    "death": ("    public override int FollowerSlots => EtherealLooks.FollowerSlots;\n", "    public override int FollowerSlots => EtherealLooks.FollowerSlots;\n\n    public override DeathMoveResult OnParentDeath(Mobile parent) { Delete(); return DeathMoveResult.RemainEquipped; }\n"),
    # Not blessed.
    "unblessed": ("    protected EtherealLook(int itemID, int mountID) : base(itemID, mountID)\n    {\n", "    protected EtherealLook(int itemID, int mountID) : base(itemID, mountID)\n    {\n        LootType = LootType.Regular;\n"),
}

if out.exists():
    shutil.rmtree(out)
(out / "_base").mkdir(parents=True)
shutil.copy(src, out / "_base" / "EtherealLooks.cs")
for name, (old, new) in MUTANTS.items():
    assert text.count(old) == 1, name
    d = out / name
    d.mkdir()
    (d / "EtherealLooks.cs").write_bytes(text.replace(old, new).encode("utf-8"))
print(len(MUTANTS), "mutants in", out)
