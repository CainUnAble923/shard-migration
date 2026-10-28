"""cc-P719: repair the README row edit_readme.py wrote with "\a" read as a bell character."""
BS = chr(92)
p = BS.join(["D:", "UO", "golems", "Iron", "ShatteredLegacy", "client", "README.md"])
s = open(p, encoding="utf-8", newline="").read()
bad = "player-package" + BS + "payload" + chr(7) + "pp" + BS + "Launch-Settings.ps1"
assert s.count(bad) == 1, s.count(bad)
s = s.replace(bad, BS.join(["player-package", "payload", "app", "Launch-Settings.ps1"]))
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
