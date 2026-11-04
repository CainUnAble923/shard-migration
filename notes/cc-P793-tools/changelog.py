# cc-P793: the CHANGELOG section and VERSION. python -P changelog.py
from pathlib import Path

CODE = Path("D:/UO/golems/Iron/ShatteredLegacy")
V = "2026.11.04"
p = CODE / "CHANGELOG.md"
s = p.read_bytes().decode("utf-8")
old = "-->\n\n## 2026.11.03.11\n"
assert s.count(old) == 1
new = f"""-->

## {V}

### Added
- Peacocks strut the meadows north of Trinsic. Tame one (Animal Taming 29.1, one follower slot, it eats fruit and grain) and ride it, with an ostard's strength and speed. A pet leash shrinks one into its own figurine. (After WiKKiD's peacock mount.)

### Staff
- Every peacock number (taming, stats, the meadows and their spawners) is in Configuration/peacock.json, written with the defaults on first start. [Peacock status|reload|seed [dryrun]. Meadow spawners are placed by themselves after every world load, once per meadow.

## 2026.11.03.11
"""
p.write_bytes(s.replace(old, new).encode("utf-8"))
(CODE / "VERSION").write_bytes((V + "\n").encode("ascii"))
