# cc-P237 read only: free tiles near a point (surface at the ground or given floor, nothing impassable in the way, not
# protected; walkway tiles listed separately).   python pick.py x y r [floor z]
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nhbase as B, protected as PR
F = B.Facet(1)
def free(x, y, fz=None):
    g = F.avgz(x, y) if fz is None else fz
    s = F.top_surface(x, y, g + 2)
    if s is None: return None, 'no surface'
    if abs(s - g) > 2: return None, 'surface %d' % s
    if F.blocked(x, y, s): return None, 'blocked ' + F.blocked(x, y, s)
    if (x, y) in PR.P: return None, 'protected'
    return s, B.walkway(F, x, y, s)
if __name__ == '__main__':
    cx, cy, r = map(int, sys.argv[1:4]); fz = int(sys.argv[4]) if len(sys.argv) > 4 else None
    off, on = [], []
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            s, w = free(x, y, fz)
            if s is None: continue
            (on if w else off).append(((x - cx) ** 2 + (y - cy) ** 2, x, y, s, w))
    print('off-road:', ['%d,%d z%d' % (x, y, s) for d, x, y, s, w in sorted(off)][:14])
    print('road:', ['%d,%d z%d %s' % (x, y, s, w) for d, x, y, s, w in sorted(on)][:10])
