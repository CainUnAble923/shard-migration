"""cc-P707 run 4: is there a path from the standing stones to the dock moongate, on P480's grid and on islegrid's?"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv += []
import isle  # noqa: sets the paths
import playthrough as base
RECT = isle.RECT
mapdir, tiledir = sys.argv[1], sys.argv[2]
start, gate = (6792, 3984), (6832, 3991)
g = base.Grid(mapdir, tiledir, RECT)
goals = {(gate[0] + dx, gate[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
p = g.path(start, goals, set())
print("P480 grid:", "path of %d" % len(p) if p else "no path")
import islegrid  # noqa: patches base.Grid._tile
g2 = base.Grid(mapdir, tiledir, RECT)
p2 = g2.path(start, goals, set())
print("islegrid:", "path of %d" % len(p2) if p2 else "no path")
