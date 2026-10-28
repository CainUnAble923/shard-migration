r"""cc-P678 read only: walkway tiles (P34's rule) of SoS Haven at half resolution. python -P roads.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sosbase as B
F = B.facet()
x0, y0, x1, y1 = 3540, 2440, 3790, 2730
print('     ' + ''.join(str((x // 10) % 10) if x % 20 == 0 else ' ' for x in range(x0, x1, 2)))
for y in range(y0, y1, 2):
    r = ''
    for x in range(x0, x1, 2):
        n = 0
        for dx in (0, 1):
            for dy in (0, 1):
                lz = F.landz(x + dx, y + dy)
                fl = [z + B.calch(i) for i, z in F.statics(x + dx, y + dy) if B.iflags(i) & B.SURF and z + B.calch(i) <= lz + 4]
                fz = max(fl) if fl else F.avgz(x + dx, y + dy)
                n += bool(B.walkway(F, x + dx, y + dy, fz))
        r += '=' if n >= 2 else ('#' if F.blocked(x, y, F.avgz(x, y)) else '.')
    print('%4d ' % y + r)
