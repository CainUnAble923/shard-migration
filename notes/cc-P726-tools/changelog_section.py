"""cc-P726: the CHANGELOG section 2026.10.28.8 and VERSION (after P728's .7, which this branch carries)."""
import os

REPO = os.path.join("D:" + os.sep, "UO", "golems", "Iron", "ShatteredLegacy")
p = os.path.join(REPO, "CHANGELOG.md")
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
assert "## 2026.10.28.8" not in s
anchor = "## 2026.10.28.7" + nl
assert s.count(anchor) == 1
section = [
    "## 2026.10.28.8",
    "",
    "### Added",
    "- Pet Info: click your evo pet with the right mouse button and choose Pet Info, or type [PetInfo and click it, to see its kind, its stage, how close it is to the next one, its loyalty and how it grows.",
    "- Test shard: a new lesson on the Wakening Isle, Healing: Pip the farm boy sits hurt on a bench inside the farmhouse, and you bandage him.",
    "- Test shard: on the Wakening Isle, the Quests button on your character window shows your lessons: which are done, the one you are on with its steps ticked, and what comes next. Your other quests are one click away.",
    "",
    "### Changed",
    "- Test shard: at the farm, your pet is now Wren's thanks for clearing the rats and snakes: first the pitchfork, war mode and the pests, then you choose a dog or a cat, then its commands.",
    "- The cloak of the Wakening Isle and Wren's pitchfork now help you heal: worn and held on the Wakening Isle they make a rat fight safe, and elsewhere they still give a little hit point regeneration.",
    "",
    "",
]
s = s.replace(anchor, nl.join(section) + anchor, 1)
open(p, "w", encoding="utf-8", newline="").write(s)
v = os.path.join(REPO, "VERSION")
vs = open(v, encoding="utf-8", newline="").read()
assert vs.strip() == "2026.10.28.7", vs
open(v, "w", encoding="utf-8", newline="").write(vs.replace("2026.10.28.7", "2026.10.28.8"))
print("ok")
