# cc-P237 read only: overview renders of New Haven (here, git-ignored), grid every 10 tiles.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nhbase as B
F = B.Facet(1)
x0, y0, x1, y1, sc, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
print(B.render(F, x0, y0, x1, y1, grid=int(sys.argv[7]) if len(sys.argv) > 7 else 10, out=out, scale=sc, hide_roofs_above=int(sys.argv[8]) if len(sys.argv) > 8 else None))
