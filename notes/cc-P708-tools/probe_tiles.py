"""cc-P708: per tile on the SoS land (the P708 hall tools' walk model): the standable heights, which of them are under a
roof, and the doors in the box.
    python -P probe_tiles.py x1 y1 x2 y2 [z]   -> a grid: '.' standable at z (+-3) and open sky, ',' standable at z under a
                                                 roof, 'D' a door tile, '~' water/none, '#' nothing standable near z
Read only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'p281sos'))
from walk import Walk  # noqa: E402

x1, y1, x2, y2 = (int(v) for v in sys.argv[1:5])
z = int(sys.argv[5]) if len(sys.argv) > 5 else None
W = Walk(1, (x1, y1, x2, y2), pad=2)
doors = set(W.door_tiles())
print('      ' + ''.join(str(x % 10) for x in range(x1, x2 + 1)))
for y in range(y1, y2 + 1):
    row = []
    for x in range(x1, x2 + 1):
        hs = W.heights(x, y)
        if (x, y) in doors:
            row.append('D')
            continue
        near = [h for h in hs if z is None or abs(h - z) <= 3]
        if not near:
            row.append('#' if hs else '~')
        elif any(W.F.roof_over(x, y, h) for h in near):
            row.append(',')
        else:
            row.append('.')
    print('%5d ' % y + ''.join(row))
