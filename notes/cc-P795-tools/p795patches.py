NL = chr(10)
# Builds the three .patch files from the patched sources copied out of the builder image: diff -u, 3+3 context.
import shutil
import subprocess
from pathlib import Path

S = Path(r"D:/UO/golems/Iron/shard-migration/notes/cc-P795-tools/pat")
OUT = Path(r"D:/UO/golems/Iron/ShatteredLegacy/server/patches")

JOBS = [
    ("Spellbook.cs", "Projects/UOContent/Items/Skill Items/Magical/Spellbook.cs", "Spellbook-drover-type.patch", [
        ("    Arcanist,\n    Mystic\n}", "    Arcanist,\n    Mystic,\n    Drover // Shattered Legacy (cc-P795): the Drover's Handbook, IDs 693-696\n}"),
        ("        if (spellID >= 677 && spellID < 693)\n        {\n            return SpellbookType.Mystic;\n        }\n",
         "        if (spellID >= 677 && spellID < 693)\n        {\n            return SpellbookType.Mystic;\n        }\n\n"
         "        // Shattered Legacy (cc-P795): the Drover's Handbook\n"
         "        if (spellID >= 693 && spellID < 697)\n        {\n            return SpellbookType.Drover;\n        }\n"),
    ]),
    ("AnimalTaming.cs", "Projects/UOContent/Skills/AnimalTaming.cs", "AnimalTaming-drover-corral.patch", [
        ("from.Skills.AnimalTaming.Value >= creature.CurrentTameSkill)) // Shattered Legacy (cc-P130): a trained pet asks for more (ServUO :184)\n",
         "from.Skills.AnimalTaming.Value >= creature.CurrentTameSkill - Server.Spells.Drover.DroverCorral.Bonus(from, creature))) // Shattered Legacy (cc-P130): a trained pet asks for more (ServUO :184); cc-P795: Corral\n"),
        ("var minSkill = m_Creature.CurrentTameSkill + m_Creature.Owners.Count * 6.0; // Shattered Legacy (cc-P130): ServUO :402" + NL,
         "var minSkill = m_Creature.CurrentTameSkill + m_Creature.Owners.Count * 6.0; // Shattered Legacy (cc-P130): ServUO :402" + NL +
         "                        minSkill -= Server.Spells.Drover.DroverCorral.Spend(m_Tamer, m_Creature); // Shattered Legacy (cc-P795): Corral, used up here" + NL),
    ]),
    ("SBAnimalTrainer.cs", "Projects/UOContent/Mobiles/Vendors/SBInfo/SBAnimalTrainer.cs", "SBAnimalTrainer-drovers-handbook.patch", [
        ('                Add(new AnimalBuyInfo(1, "a rabbit", typeof(Rabbit), 106, 10, 205, 0));\n',
         '                Add(new AnimalBuyInfo(1, "a rabbit", typeof(Rabbit), 106, 10, 205, 0));\n'
         '                Add(new GenericBuyInfo(typeof(Server.Items.DroversHandbook), Server.Spells.Drover.DroverSettings.BookPrice, 20, 0x0FEF, 0)); // Shattered Legacy (cc-P795)\n'
         '                Add(new GenericBuyInfo(typeof(Server.Items.CalmScroll), Server.Spells.Drover.DroverSettings.CalmScrollPrice, 20, Server.Spells.Drover.DroverSettings.ScrollArt, Server.Spells.Drover.DroverSettings.ScrollHue));\n'
         '                Add(new GenericBuyInfo(typeof(Server.Items.HerdScroll), Server.Spells.Drover.DroverSettings.HerdScrollPrice, 20, Server.Spells.Drover.DroverSettings.ScrollArt, Server.Spells.Drover.DroverSettings.ScrollHue));\n'
         '                Add(new GenericBuyInfo(typeof(Server.Items.LureScroll), Server.Spells.Drover.DroverSettings.LureScrollPrice, 20, Server.Spells.Drover.DroverSettings.ScrollArt, Server.Spells.Drover.DroverSettings.ScrollHue));\n'),
    ]),
]

for name, tree, patch, edits in JOBS:
    src = S / name
    text = src.read_bytes().decode("utf-8")
    assert "\r\n" not in text
    new = text
    for old, rep in edits:
        assert new.count(old) == 1, old
        new = new.replace(old, rep)
    edited = S / (name + ".new")
    edited.write_bytes(new.encode("utf-8"))
    r = subprocess.run(["diff", "-u", "--label", "a/" + tree + "	", "--label", "b/" + tree + "	", str(src).replace("\\", "/"), str(edited).replace("\\", "/")],
                       capture_output=True)
    assert r.returncode == 1, r
    (OUT / patch).write_bytes(r.stdout)
    print(patch, len(r.stdout))
