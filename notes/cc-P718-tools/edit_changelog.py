import os
os.chdir(r"D:\UO\golems\Iron\ShatteredLegacy")
s = open("CHANGELOG.md", encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
old = "## 2026.10.27.4"
assert s.count(old) == 1
lines = [
    "## 2026.10.28.2", "",
    "### Added",
    "- Test shard: on the Wakening Isle, Tamsin, Wren and Elara speak first when you come near and tell you to double-click them, every half minute until you do.",
    "- Test shard: your cloak from the Wakening Isle is yours to keep. It waits on the table by the clothes rack: drag it onto your character to wear it. It stays with you after death and cannot be sold, traded or dropped.",
    "- Test shard: optional client tips, at any time from Tamsin's or Rook's window. The first shows how to turn on Always run.",
    "- Test shard: at the farm, Wren teaches pet commands before the pests: say \"all follow me\", then \"all guard me\" (or use your pet's menu), and let your pet take at least one pest with \"all kill\". She hands you bandages, says how to use them, and how to make more with scissors and cloth.",
    "",
    "### Changed",
    "- Test shard: the backpack lesson starts by opening your character window: double-click yourself, or click the paperdoll button.",
    "- Test shard: the farm's rats and snakes stay behind the field gate and leave you alone until your pest lesson; Wren opens the gate when it starts.",
    "- Test shard: the signposts on the Wakening Isle are proper standing signposts, named so you can tell what they say.",
    "",
    "### Fixed",
    "- Test shard: fighting on the Wakening Isle no longer floods the screen with skill gains: each skill can rise at most once every 10 seconds there.",
    "",
    "### Staff",
    "- clusterf.tutorial.gainSecondsPerSkill (10) sets the Wakening Isle's gain pace; 0 turns it off.",
    "", "",
]
s = s.replace(old, nl.join(lines) + old)
open("CHANGELOG.md", "w", encoding="utf-8", newline="").write(s)
v = open("VERSION", encoding="utf-8", newline="").read()
open("VERSION", "w", encoding="utf-8", newline="").write(v.replace("2026.10.27.4", "2026.10.28.2"))
print("ok")
