"""cc-P685: register GenChamps-sos-sites.patch in apply-patches.sh, by exact text."""
import sys

p = "D:/UO/golems/Iron/ShatteredLegacy/docker/uo/apply-patches.sh"
s = open(p, encoding="utf-8", newline="").read()
old = 'apply_patch "$PATCHES/GenTeleporter-sos-teleporters.patch"\n'
new = old + ('# cc-P685 (SoS swap S12): Felucca\'s champion altars on the SoS land (three Lost Lands sites move, LL08\'s eject point)\n'
             'apply_patch "$PATCHES/GenChamps-sos-sites.patch"\n')
if "\r\n" in s:
    old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
if s.count(old) != 1:
    sys.exit(f"expected one match, found {s.count(old)}")
open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
print("edited", p)
