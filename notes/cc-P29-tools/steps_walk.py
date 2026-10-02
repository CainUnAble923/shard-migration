# cc-P29 Part D: the same walk as fountain_walk.py with the stepping stones placed as ClusterFFountainStepsSeeder
# places them (PaverStones Natural, 0x47DC-0x47E0 and 0x47E5, height 1, Surface; z -41 over each rock), in both
# data sets. Prints whether the end tile is reached and the path to it.
import sys
sys.path.insert(0, r'D:/UO/shard-migration/notes/cc-P29-tools')
from walk import *
from fountain_walk import near, report

# Must match ClusterFFountainStepsSeeder.Steps, in order.
STEPS = [(1122, 965), (1121, 965), (1123, 965), (1122, 964), (1123, 964), (1123, 963), (1123, 962), (1123, 961),
         (1122, 961), (1122, 960), (1121, 960), (1121, 959)]
ART = [0x47DC, 0x47DD, 0x47DE, 0x47DF, 0x47E0, 0x47E5]
Z = -41

if __name__ == '__main__':
    entries, srcs = teleporters()
    starts = sorted(set(e[2] for e in entries))
    extra = {xy: [(ART[i % len(ART)], Z)] for i, xy in enumerate(STEPS)}
    for label, cd in (('server 7.0.114.40', SERVER), ('EA 7.0.117.0', EA)):
        w = World(cd, extra=extra)
        for a in ART:
            print(f'  {label} 0x{a:X}: "{w.T.sname[a]}" h{w.T.sheight[a]} [{flagnames(w.iflags(a))}]')
        seen, inrange = report(label + ' with steps', w, starts, srcs)
        for xy in STEPS:
            print(f'    step {xy}: reached={xy in seen} z={seen.get(xy, (None,))[0]} distance={near(*xy)}')
        end = STEPS[-1]
        if end in seen:
            print('  path to the end tile:', path(seen, *end)[-16:])
