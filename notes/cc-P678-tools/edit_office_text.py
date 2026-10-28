r"""cc-P678: the comments that still describe the old League office house.
    python -P edit_office_text.py
"""
CODE = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/"

REPS = {
    "ClusterFNewHavenSeeder.cs": [
        ("""        // League of Extraordinary Citizens field office. Faces West, to her desk (the table at
        // 3458,2600-2601); she faced North before cc-P19, which world load still accepts.""",
         """        // League of Extraordinary Citizens field office: cc-P678, the free hall north-east of the square in SoS Haven
        // (3659-3673, 2548-2561). She faces South, with her desk on the counter east of her (3661,2549); before, she
        // faced West to the desk of the house at 3453-3462, 2596-2603, which is forest on SoS."""),
    ],
    "LeagueRegistrar.cs": [
        ("""/// stationed at the New Haven field office (Trammel 3459, 2601).""",
         """/// stationed at the New Haven field office (Trammel 3660, 2549; cc-P678, the hall north-east of the square)."""),
    ],
    "ClusterFRegistrarOfficeSeeder.cs": [
        ("""// cc-P19: props for the League of Extraordinary Citizens Field Office in New Haven (Trammel), the
// two-room house where the League Registrar sits (walls x3453-3462, y2596-2603, floor z18). Adds items
// only; the map's own bed, dresser, table and chair stay as they are.""",
         """// cc-P19: props for the League of Extraordinary Citizens Field Office in New Haven (Trammel), where the
// League Registrar sits. cc-P678: on SoS the office is the free hall north-east of the square (walls x3658-3674,
// y2547-2562, floor z0, the street door at 3667-3668,2562; the quarters are the back room behind the long counter,
// 3670-3673, 2548-2550); it was the two-room house at x3453-3462, y2596-2603, z18. Adds items only; the map's own
// counters and furniture stay as they are."""),
        ("""        // The sign, by item id (design: 0x0BCF at 3463,2597). cc-P31: 0x0BD0 at 3460,2595 left the design.""",
         """        // The sign, by item id (design: 0x0BCF at 3670,2563 since cc-P678). cc-P31: 0x0BD0 left the design."""),
    ],
}

for name, reps in REPS.items():
    p = CODE + name
    s = open(p, encoding="utf-8").read()
    for a, b in reps:
        assert s.count(a) == 1, (name, a[:60])
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
