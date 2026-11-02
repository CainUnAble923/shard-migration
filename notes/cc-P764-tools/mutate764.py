# cc-P764: makes one mutant folder per rule of the pet leash, each undoing that rule, for the red-first check.
# Usage: python -P mutate764.py <ShatteredLegacy\server\customizations> <out folder>
# Each mutant folder holds ClusterFPetLeash.cs and Tutorial\ (a copy, one file changed), for probe764.sh to mount.
import shutil
import sys
from pathlib import Path

src = Path(sys.argv[1])
out = Path(sys.argv[2])

LEASH = "ClusterFPetLeash.cs"
SKIP = "Tutorial/TutorialGateSkip.cs"
CARE = "Tutorial/TutorialPetCare.cs"

# name: (file, old, new): the old text must occur exactly once.
MUTANTS = {
    # Restore lets anyone holding the figurine call the pet out.
    "noowner": (LEASH, "        if (owner != pm)\n        {\n            pm.SendMessage(\n", "        if (owner == null)\n        {\n            pm.SendMessage(\n"),
    # No fight rule at all.
    "nocombat": (LEASH, "    public static bool InCombat(Mobile m)\n    {\n", "    public static bool InCombat(Mobile m)\n    {\n        return false;\n"),
    # Summons can be leashed.
    "nosummon": (LEASH, "        if (pet.Summoned || pet is BaseTalismanSummon)", "        if (pet is BaseTalismanSummon)"),
    # Pets carrying items can be leashed.
    "nopack": (LEASH, "        if (pet.Backpack?.Items.Count > 0)", "        if (false)"),
    # Someone else's pet can be leashed.
    "notowned": (LEASH, "        if (!pet.Controlled || pet.ControlMaster != pm)", "        if (!pet.Controlled)"),
    # Queen's loyalty floor, raised to full on restore: loyalty is not kept.
    "loyalty": (LEASH, "        pm.Followers += pet.ControlSlots;\n", "        pet.Loyalty = BaseCreature.MaxLoyalty;\n        pm.Followers += pet.ControlSlots;\n"),
    # The starter scroll gives no leash.
    "nostarter": (SKIP, "        pm.AddToBackpack(new PetLeash());", "        // no leash"),
    # The animal trainer does not sell it.
    "noshop": (CARE, ",\n            new GenericBuyInfo(\"a pet leash\", typeof(PetLeash), ClusterFPetLeash.Price, 20, PetLeash.LeashItemID, 0)", ""),
}


def read(p: Path) -> tuple[str, str]:
    raw = p.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    return raw.replace("\r\n", "\n"), nl


for name, (rel, old, new) in MUTANTS.items():
    d = out / name
    if d.exists():
        shutil.rmtree(d)
    (d / "Tutorial").mkdir(parents=True)
    shutil.copy2(src / LEASH, d / LEASH)
    shutil.copytree(src / "Tutorial", d / "Tutorial", dirs_exist_ok=True)
    text, nl = read(d / rel)
    n = text.count(old)
    if n != 1:
        sys.exit(f"{name}: the text to change occurs {n} times in {rel}")
    (d / rel).write_text(text.replace(old, new).replace("\n", nl), encoding="utf-8", newline="")
    print("mutant", name)
