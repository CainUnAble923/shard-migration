import os
os.chdir(r"D:\UO\golems\Iron\ShatteredLegacy")
s = open("CHANGELOG.md", encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
old = "## 2026.10.28.3"
assert s.count(old) == 1
lines = [
    "## 2026.10.28.4", "",
    "### Changed",
    "- A new character walks until you turn on Always run (Options, then Gameplay, then Movement), and starts with its character window closed: double-click yourself to open it. Characters you already have keep their own settings.",
    "", "",
]
s = s.replace(old, nl.join(lines) + old)
open("CHANGELOG.md", "w", encoding="utf-8", newline="").write(s)
v = open("VERSION", encoding="utf-8", newline="").read()
assert "2026.10.28.3" in v
open("VERSION", "w", encoding="utf-8", newline="").write(v.replace("2026.10.28.3", "2026.10.28.4"))
print("ok")
