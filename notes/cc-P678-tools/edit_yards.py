r"""cc-P678: the tutorial's training yard, trades yard and the housing tour's porch move into SoS Haven (yards.py).
    python -P edit_yards.py
"""
CODE = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/"

TRAINING = "the training yard, behind the Little Shop of Magic"
TRADES = "the trades yard, west of the training yard"

REPS = {
    "TutorialWingTrials.cs": [
        ("""        /// <summary>The training yard: open ground east of the farm gate (checked standable from the map files, notes cc-P290).</summary>
        public static readonly Point2D Yard = new(3411, 2617);""",
         """        /// <summary>
        /// The training yard: cc-P678, the grass behind the Little Shop of Magic in SoS Haven, 25 tiles from the start; its
        /// 7 x 5 is open, flat (one Z), uncovered and reachable on foot (notes/cc-P678-tools/yards.py). Was east of the
        /// west farm's gate (3411,2617, cc-P290), which is forest on SoS.
        /// </summary>
        public static readonly Point2D Yard = new(3633, 2562);"""),
    ],
    "TutorialTradeTrials.cs": [
        ("""// Places: the trades yard (TradesYard, open ground south-east of P290's training yard, checked standable from the map
// files)""", """// Places: the trades yard (TradesYard, open ground west of P290's training yard, cc-P678's yards.py on the SoS files)"""),
        ("""        public static readonly Point2D TradesYard = new(3426, 2626);""",
         """        public static readonly Point2D TradesYard = new(3617, 2554); // cc-P678: was 3426,2626, forest on SoS"""),
        ("""        private const string AtYard = "the trades yard, southeast of the training yard";""",
         """        private const string AtYard = "%s";""" % TRADES),
        ("""                    (() => Ground(3383, 2612), "the farmhouse porch",""",
         """                    (() => Ground(3708, 2593), "the farmhouse porch", // cc-P678: the stables farmhouse's south porch"""),
        ("""            ? "Follow the arrow to the training yard, east of the farm gate. Your lesson begins when you arrive.\"""",
         """            ? "Follow the arrow to %s. Your lesson begins when you arrive.\"""" % TRAINING),
    ],
    "TutorialStations.cs": [
        ('"the training yard, east of the farm gate"', '"%s"' % TRAINING),
        ('"the trades yard, southeast of the training yard"', '"%s"' % TRADES),
    ],
}

for name, reps in REPS.items():
    p = CODE + name
    s = open(p, encoding="utf-8").read()
    for a, b in reps:
        n = s.count(a)
        assert n >= 1, (name, a[:70])
        s = s.replace(a, b)
        print(name, n, "x", a[:50].strip())
    open(p, "w", encoding="utf-8", newline="").write(s)
