"""cc-P818: the League lodge and its approach as a player sees it: the map (an overlay folder) plus the server items the
seed places there (the door, the lodge's name sign and the League lesson sign), drawn in. --cut leaves out statics above
Z 19 (the roof), for the inside.

    python -P lodge_view818.py <map folder> <out.png> before|after [--cut]
Run with PYTHONPATH=<shard-migration>/scripts, MAPBUILD_CLIENT and MAPBUILD_ART set (guide section 8)."""
import sys

from mapbuild import isorender

X1, Y1, X2, Y2 = 6772, 3980, 6797, 4008
SERVER = {
    'before': [(6782, 3995, 0, 0x06A9), (6781, 3989, 0, 0xA854), (6782, 3989, 0, 0xA854)],
    'after': [(6787, 4000, 0, 0x06B3), (6788, 3984, 0, 0xA854), (6789, 3984, 0, 0xA854)],
}

folder, out, which = sys.argv[1], sys.argv[2], sys.argv[3]
sc = isorender.Scene.from_map(folder, 1, X1, Y1, X2, Y2)
if '--cut' in sys.argv:
    sc.statics = [s for s in sc.statics if s[2] <= 19]
sc.statics = list(sc.statics) + SERVER[which]
print(out, isorender.save(isorender.render(sc, X1, Y1, X2, Y2), out))
