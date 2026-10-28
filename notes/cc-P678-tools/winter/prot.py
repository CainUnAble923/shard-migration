r"""cc-P678 read only: the protected tiles in a box and why.  python -P prot.py x1 y1 x2 y2"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import protected as PR
x1, y1, x2, y2 = [int(v) for v in sys.argv[1:5]]
for (x, y), v in sorted(PR.P.items(), key=lambda k: (k[0][1], k[0][0])):
    if x1 <= x <= x2 and y1 <= y <= y2:
        print(x, y, ' | '.join(sorted(set(v)))[:200])
