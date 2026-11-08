"""cc-P743: the shortest walk (P281's walker, P708's SoS copy) between two spots, printed every few steps.

    python -u -P -W ignore notes/cc-P743-tools/route.py x y z x y z [every]
"""
import os
import sys
from collections import deque

DOCS = os.path.abspath('D:/UO/golems/Iron/shard-migration')
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P708-tools', 'p281sos'))
import hallbase as H
H.CLIENT = H.uofiles.CLIENT = "D:/UO/tool-trials/client-data-copy"
import walk as Wk  # noqa: E402

a = tuple(int(v) for v in sys.argv[1:4])
b = tuple(int(v) for v in sys.argv[4:7])
every = int(sys.argv[7]) if len(sys.argv) > 7 else 8
box = (3380, 2440, 3800, 2820)  # the Haven island part the flood used
W = Wk.Walk(1, box, pad=0)


def near(p):
    hs = W.heights(p[0], p[1])
    return (p[0], p[1], min(hs, key=lambda h: abs(h - p[2]))) if hs else None


s, t = near(a), near(b)
prev = {s: None}
q = deque([s])
x1, y1, x2, y2 = W.box
while q:
    c = q.popleft()
    if c == t:
        break
    x, y, z = c
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            nx, ny = x + dx, y + dy
            if (dx or dy) and x1 <= nx <= x2 and y1 <= ny <= y2:
                for nz in W.heights(nx, ny):
                    step = Wk.STEP_BRIDGE if (z in W.bridge_heights(x, y) or nz in W.bridge_heights(nx, ny)) else Wk.STEP
                    n = (nx, ny, nz)
                    if n not in prev and (abs(nz - z) <= step or W.land_step(x, y, z, nx, ny, nz)):
                        prev[n] = c
                        q.append(n)
if t not in prev:
    print('no path')
    sys.exit(1)
path = []
c = t
while c:
    path.append(c)
    c = prev[c]
path.reverse()
print('steps', len(path) - 1)
for i, p in enumerate(path):
    if i % every == 0 or i == len(path) - 1:
        print(i, p, H.lname(W.F.land(p[0], p[1])[0]))
