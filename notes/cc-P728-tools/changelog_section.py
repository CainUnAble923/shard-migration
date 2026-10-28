"""cc-P728: the CHANGELOG section 2026.10.28.7 and VERSION."""
import os

REPO = os.path.join("D:" + os.sep, "UO", "golems", "Iron", "ShatteredLegacy")
p = os.path.join(REPO, "CHANGELOG.md")
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
assert "## 2026.10.28.7" not in s
anchor = "## 2026.10.28.6" + nl
assert s.count(anchor) == 1
section = [
    "## 2026.10.28.7",
    "",
    "### Changed",
    "- Test shard: waking on the Wakening Isle's beach, you stay down on the sand until you move; your first move gets you up and the first lesson starts. If you wait, the System says \"Move to get up.\"",
    "- Test shard: on a new character's first login, the patch notes, your first achievement and the welcome lines wait until you have stood up on the beach, and the guild welcome waits until you reach town.",
    "- Test shard: at the clothes stop, a chest appears with your cloak of the Wakening Isle inside: double-click the chest, then drag the cloak to your backpack or onto your character. Only you can open it, and it goes once you have the cloak.",
    "- Test shard: at the farm, Wren hands you the pitchfork first: hold it and switch to war mode, then teach your pet its commands, then the pests.",
    "- Test shard: when the cabbage rows are clear, Wren, the System and the lesson window all say so and tell you to go back to Wren, and the arrow points at her. Each finished lesson names the next one and points at its signpost, and typing [lesson opens the lesson window again.",
    "",
    "### Fixed",
    "- Test shard: Wren no longer says \"Defeat 0 more rats or grass snakes\"; she says what is still left to do.",
    "",
    "### Staff",
    "- New Wakening Isle pieces (like Pip at the farm) now appear on the test world by themselves at each restart, on the isle and on every copy; the server log lists what was placed.",
    "",
    "",
]
s = s.replace(anchor, nl.join(section) + anchor, 1)
open(p, "w", encoding="utf-8", newline="").write(s)
v = os.path.join(REPO, "VERSION")
vs = open(v, encoding="utf-8", newline="").read()
assert vs.strip() == "2026.10.28.6", vs
open(v, "w", encoding="utf-8", newline="").write(vs.replace("2026.10.28.6", "2026.10.28.7"))
print("ok")
