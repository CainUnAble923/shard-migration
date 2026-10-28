r"""cc-P678 part 4, second pass: the hatch moves from the bank's north annex (where the winter decor's tree group
stands) to the main hall's south-west corner, one tile west of Old Haven's hole (crosscheck.py found the spot clear of
every seasonal row and three tiles from the bankers).
    python -P edit_hatch2.py
"""
CODE = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/"

REPS = {
    "ClusterFRootdeepSeeder.cs": [
        ("""//     the bank's back room (3621,2611; the north annex, entered from the main room by its door at 3616,2614): the""",
         """//     the corner of the bank's main hall (3618,2620, one tile west of the old hole, three from the bankers): the"""),
        ("""//     in the same room (3618,2612). The retarget above still points an older ladder at the new landing.""",
         """//     in the same hall (3621,2620). The retarget above still points an older ladder at the new landing."""),
        ("""    /// <summary>cc-P678: the cellar hatch in the Second Bank of Haven's back room (OldHavenBurrowsRegion.HoleEntrance).</summary>
    public static readonly Point2D Hole = new(3621, 2611);""",
         """    /// <summary>cc-P678: the cellar hatch in the Second Bank of Haven's main hall (OldHavenBurrowsRegion.HoleEntrance).</summary>
    public static readonly Point2D Hole = new(3618, 2620);"""),
        ("""    public const int MouthX1 = 3621, MouthY1 = 2611, MouthX2 = 3621, MouthY2 = 2611;""",
         """    public const int MouthX1 = 3618, MouthY1 = 2620, MouthX2 = 3618, MouthY2 = 2620;"""),
        ("""    /// cc-P678: where the ladder up lands: the bank's back room, three tiles west of the hatch (cc-P413's was outside the""",
         """    /// cc-P678: where the ladder up lands: the bank's main hall, three tiles east of the hatch (cc-P413's was outside the"""),
        ("""    public static readonly Point2D BesideHatch = new(3618, 2612);""",
         """    public static readonly Point2D BesideHatch = new(3621, 2620);"""),
    ],
    "Regions/OldHavenBurrowsRegion.cs": [
        ("""    /// cellar hatch in its back room (ClusterFRootdeepSeeder.Hole), so the Entrance moves there.""",
         """    /// cellar hatch in its main hall (ClusterFRootdeepSeeder.Hole), so the Entrance moves there."""),
        ("""    public static readonly Point3D HoleEntrance = new(3621, 2611, 0);""",
         """    public static readonly Point3D HoleEntrance = new(3618, 2620, 0);"""),
    ],
}

for name, reps in REPS.items():
    p = CODE + name
    s = open(p, encoding="utf-8").read()
    for a, b in reps:
        assert s.count(a) == 1, (name, a[:60])
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)

p = "D:/UO/golems/Iron/shard-migration/notes/cc-P678-tools/crosscheck.py"
s = open(p).read()
a = 'HATCH, LANDING, ANNEX_DOOR = (3621, 2611), (3618, 2612), (3616, 2614)'
assert a in s
s = s.replace(a, 'HATCH, LANDING = (3618, 2620), (3621, 2620)')
s = s.replace('path = w.path(ANNEX_DOOR, HATCH) or []', 'path = w.path(START, HATCH) or []')
s = s.replace('print("blocking props %d; tiles reached %d; door to hatch %d steps"', 'print("blocking props %d; tiles reached %d; start to hatch %d steps"')
s = s.replace("  3. nothing stands on the hatch, the landing, or the walk from the bank's annex door (3616,2614) to the hatch.",
              "  3. nothing stands on or beside the hatch or the landing, or on the walk from the start to the hatch.")
open(p, "w").write(s)
print("ok")
