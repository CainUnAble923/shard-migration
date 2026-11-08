"""cc-P837 (from P818's lodge_view818.py): the isle's bank and League lodge on the MERGED map (main's P817/P823 bank and
eave fixes plus P818's lodge door), with the server items the seed places drawn in: the bank door, the lodge door and
the lesson and name signs at their merged spots. --cut leaves out statics above Z 19 (the roofs).

    python -P view837.py <map folder> <out.png> [--cut]
Run with PYTHONPATH=<shard-migration>/scripts, MAPBUILD_CLIENT and MAPBUILD_ART set (guide section 8)."""
import sys

from mapbuild import isorender

X1, Y1, X2, Y2 = 6752, 3966, 6797, 4008
SERVER = [
    (6762, 3980, 0, 0x06A9),  # bank door, WestCCW (TutorialWorld.BankDoor)
    (6757, 3982, 0, 0xA854),  # core.banking sign, cc-P817's spot
    (6787, 4000, 0, 0x06B3),  # lodge door, NorthCW in the east wall (cc-P818)
    (6788, 3984, 0, 0xA854),  # lodge name sign (cc-P818)
    (6789, 3984, 0, 0xA854),  # core.league sign (cc-P818)
]

folder, out = sys.argv[1], sys.argv[2]
sc = isorender.Scene.from_map(folder, 1, X1, Y1, X2, Y2)
if '--cut' in sys.argv:
    sc.statics = [s for s in sc.statics if s[2] <= 19]
sc.statics = list(sc.statics) + SERVER
print(out, isorender.save(isorender.render(sc, X1, Y1, X2, Y2), out))
