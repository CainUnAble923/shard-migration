"""cc-P719: client README, 0007's row: "ExternalImages" + BEL + "rt" back to "ExternalImages\\art"."""
BS = chr(92)
p = BS.join(["D:", "UO", "golems", "Iron", "ShatteredLegacy", "client", "README.md"])
s = open(p, encoding="utf-8", newline="").read()
bad = "ExternalImages" + chr(7) + "rt"
assert s.count(bad) == 1, s.count(bad)
s = s.replace(bad, "ExternalImages" + BS + "art")
assert chr(7) not in s
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
