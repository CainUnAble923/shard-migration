r"""cc-P678 read only: a character map of SoS Haven for placing the winter rows.
    python -P view.py x1 y1 x2 y2 [x,y ...]
'#' an impassable static (a wall), '~' water, ' ' void, 'D' a door or its swing, 'P' another protected tile,
'=' a walkway (road, plaza, floor: P34's walkway rule) in the open, 'f' a walkway under a roof (a floor),
'.' open ground, ',' open ground under a roof, 'T' a table top (a Surface static above the floor), digits the given
points. The z of a tile that is not the land's 0 shows in the legend of given points only.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sosbase as B, protected as PR
F = B.facet()


def ch(x, y):
    lid, lz = F.land(x, y)
    s = F.top_surface(x, y, lz + 6 if not any(B.iflags(i) & B.SURF and z <= lz + 2 for i, z in F.statics(x, y)) else 127)
    floor = s if s is not None else lz
    floors = [z + B.calch(i) for i, z in F.statics(x, y) if B.iflags(i) & B.SURF and z + B.calch(i) <= lz + 4]
    if floors: floor = max(floors)
    if F.blocked(x, y, floor):
        tabs = [z + B.calch(i) for i, z in F.statics(x, y) if B.iflags(i) & B.SURF and B.iflags(i) & B.IMP]
        return 'T' if tabs else '#'
    if lid in (0x244, 0x2, 0x1DB) and not floors: return ' '
    if 0xA8 <= lid <= 0xAB or 0x136 <= lid <= 0x137:
        if not floors: return '~'
    pr = PR.P.get((x, y), ())
    if any(p.startswith(('door', 'swing', 'doorgen')) for p in pr): return 'D'
    if pr: return 'P'
    roof = F.roof_over(x, y, floor)
    if B.walkway(F, x, y, floor): return 'f' if roof else '='
    return ',' if roof else '.'


if __name__ == '__main__':
    a = [int(v) for v in sys.argv[1:5]]
    pts = [tuple(int(v) for v in p.split(',')[:2]) for p in sys.argv[5:]]
    print('     ' + ''.join(str((x // 10) % 10) if x % 10 == 0 else ' ' for x in range(a[0], a[2] + 1)))
    for y in range(a[1], a[3] + 1):
        row = ''.join(str(pts.index((x, y)) % 10) if (x, y) in pts else ch(x, y) for x in range(a[0], a[2] + 1))
        print('%4d ' % y + row)
    for i, (x, y) in enumerate(pts):
        print(i % 10, x, y, 'land', F.land(x, y), 'surf', F.top_surface(x, y), F.describe(x, y), PR.P.get((x, y), ''))
