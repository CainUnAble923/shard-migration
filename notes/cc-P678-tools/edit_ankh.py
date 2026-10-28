r"""cc-P678: Chase's New Haven ankh (fidelity D-123) moves beside the new League office, on grass at 3676,2562,0.
On SoS the static ankh it stood over (3464,2600,27) is forest; the town's own working ankh is pinned haven.cfg's
AnkhNorth at 3606,2582. crosscheck.py checks the two tiles clear.
    python -P edit_ankh.py
"""
ROOT = "D:/UO/golems/Iron/ShatteredLegacy/server/"

REPS = {
    "customizations/ClusterFAnkhs.cs": [
        ("""// Chase, 2026-10-16: the ankh by the League Registrar's office in New Haven "needs to be usable". It is a map
// static (0x3/0x2, facing west, Trammel 3464,2600,27), not pinned's working ankh""",
         """// Chase, 2026-10-16: the ankh by the League Registrar's office in New Haven "needs to be usable". It was a map
// static (0x3/0x2, facing west, Trammel 3464,2600,27), not pinned's working ankh"""),
        ("""        // Ours (fidelity D-123): Chase's New Haven ankh, over the static 0x3/0x2 at 3464,2600-2601,27, same art and facing.
        new("AnkhWest 0x0003", 1, 3464, 2600, 27, "ours, Chase 2026-10-16"),""",
         """        // Ours (fidelity D-123): Chase's New Haven ankh by the League office. It stood over the static 0x3/0x2 at
        // 3464,2600-2601,27; on SoS (cc-P678) that is forest and the office is the hall north-east of the square, so
        // the ankh stands on the grass by the hall's south-east corner, 3676,2562-2563,0, same art and facing.
        // (The town's own working ankh is pinned haven.cfg's AnkhNorth at 3606,2582, placed by [Decorate.)
        new("AnkhWest 0x0003", 1, 3676, 2562, 0, "ours, Chase 2026-10-16; cc-P678 by the new office"),"""),
    ],
    "tests/Misc/AnkhVerification.cs": [
        ("""//   1. Seeding puts a working AnkhWest, art 0x3 over 0x2, on the New Haven static (3464,2600-2601,27), places every""",
         """//   1. Seeding puts a working AnkhWest, art 0x3 over 0x2, by New Haven's League office (3676,2562-2563,0; cc-P678,
//      was over the static at 3464,2600-2601,27, forest on SoS), places every"""),
        ("""    private static readonly Point3D NewHaven = new(3464, 2600, 27);""",
         """    private static readonly Point3D NewHaven = new(3676, 2562, 0);"""),
    ],
}

for name, reps in REPS.items():
    p = ROOT + name
    s = open(p, encoding="utf-8").read()
    for a, b in reps:
        assert s.count(a) == 1, (name, a[:60])
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
