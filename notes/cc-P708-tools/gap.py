"""cc-P708: where two places that should be joined on foot come closest: floods from each (P281's walk on the SoS land,
the P708 copy) and prints the nearest pairs of reached tiles, with what stands between.
    python -P gap.py ax ay az bx by bz [pad]
Read only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'p281sos'))
import hallbase as H  # noqa: E402
from walk import Walk  # noqa: E402

a = tuple(int(v) for v in sys.argv[1:4])
b = tuple(int(v) for v in sys.argv[4:7])
pad = int(sys.argv[7]) if len(sys.argv) > 7 else 40
W = Walk(1, (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])), pad=pad)
ra, rb = W.flood(a), W.flood(b)
print('reached from a:', len(ra), ' from b:', len(rb), ' joined:', bool(ra & rb))
xa = {}
for x, y, z in ra:
    xa.setdefault((x, y), z)
best = []
for x, y, z in rb:
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if (x + dx, y + dy) in xa:
                best.append((max(abs(dx), abs(dy)), (x + dx, y + dy, xa[(x + dx, y + dy)]), (x, y, z)))
best.sort()
for d, p, q in best[:12]:
    mid = ((p[0] + q[0]) // 2, (p[1] + q[1]) // 2)
    print('a %s  b %s  apart %d  between %s: heights %s, statics %s' % (
        p, q, d, mid, W.heights(*mid), ['0x%04X %s z%d' % (i, H.iname(i), z) for i, z in W.F.statics(*mid)][:4]))
