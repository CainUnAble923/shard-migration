# cc-P678 read only: where a community-art row of one mode would pass art_validate.check, as characters.
#     python -P art_map.py mode x1 y1 x2 y2 [x,y ...]
# '+' passes; otherwise '#' no stand (wall, tree, water), 'p' protected, '=' a walkway, 'c' a spawner's box (camp),
# 'R' covered, '.' any other failure; digits mark the given points. z is the tile's top surface (ground modes) or the
# soswalk stand (indoor and wall modes).
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art_validate as V
B, F, PR = V.B, V.F, V.PR
ART = {'ground': 0x3C88, 'camp': 0x3C96, 'edge': 0x3C8F, 'indoor': 0x3C8F, 'wall': 0x3CA0}


def verdict(mode, x, y):
    st = V.WALK.stand.get((x, y))
    if mode in ('ground', 'camp', 'edge'):
        z = F.top_surface(x, y, F.avgz(x, y) + 2)
    else:
        z = st
    if z is None: return '#', []
    r = dict(key='k', x=x, y=y, z=z, itemId=ART[mode], mode=mode, art='ptg-x' if mode == 'wall' else 'x')
    errs = V.check(r, set(), {})
    if not errs: return '+', errs
    if st is None: return '#', errs
    if (x, y) in PR.P: return 'p', errs
    e = ' '.join(errs)
    if 'walkway' in e: return '=', errs
    if 'inside spawner' in e: return 'c', errs
    if any(sz > z + 8 for s, sz in F.statics(x, y)): return 'R', errs
    return '.', errs


if __name__ == '__main__':
    mode = sys.argv[1]
    a = [int(v) for v in sys.argv[2:6]]
    pts = [tuple(int(v) for v in p.split(',')[:2]) for p in sys.argv[6:]]
    print('     ' + ''.join(str((x // 10) % 10) if x % 10 == 0 else ' ' for x in range(a[0], a[2] + 1)))
    for y in range(a[1], a[3] + 1):
        row = ''
        for x in range(a[0], a[2] + 1):
            row += str(pts.index((x, y)) % 10) if (x, y) in pts else verdict(mode, x, y)[0]
        print('%4d %s' % (y, row))
    for i, p in enumerate(pts):
        print(i, p, verdict(mode, *p)[1] or 'ok')
