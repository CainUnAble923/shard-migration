"""cc-P734: where OSI house multis put the roof relative to the walls. For each multi with a roof: the wall box of the
first storey (pieces 19+ high), the lowest roof course's Z and box, and the offset between them; also where the floor
tiles lie relative to the wall box (under which wall rows) and the stair pieces per multi.
Usage (PYTHONPATH=scripts): python -P notes/cc-P734-tools/roof_survey.py"""
import collections
import sys

sys.path.insert(0, __file__.rsplit('notes', 1)[0] + 'notes/cc-P734-tools')
import stair_survey as S  # noqa: E402

offs = collections.Counter()
floor_rows = collections.Counter()
for mid in range(0x60, 0xA0):
    try:
        cs = S.comps(mid)
    except Exception:
        continue
    if not cs:
        continue
    walls = [c for c in cs if S.items[c[3]]['height'] >= 19 and any(k in S.name(c[3]) for k in ('wall', 'post', 'window', 'door'))]
    roofs = [c for c in cs if 'roof' in S.name(c[3])]
    floors = [c for c in cs if S.items[c[3]]['height'] == 0 and any(k in S.name(c[3]) for k in ('board', 'floor', 'tile', 'paver', 'flagstone', 'carpet'))]
    if not walls or not roofs:
        continue
    z0 = min(w[2] for w in walls)
    base = [w for w in walls if w[2] == z0]
    wx = (min(b[0] for b in base), max(b[0] for b in base))
    wy = (min(b[1] for b in base), max(b[1] for b in base))
    rz = min(r[2] for r in roofs)
    low = [r for r in roofs if r[2] == rz]
    rx = (min(r[0] for r in low), max(r[0] for r in low))
    ry = (min(r[1] for r in low), max(r[1] for r in low))
    key = 'roof z = wall z + %d; roof box x %+d..%+d, y %+d..%+d of the wall box' % (rz - z0, rx[0] - wx[0], rx[1] - wx[1], ry[0] - wy[0], ry[1] - wy[1])
    offs[key] += 1
    fl = [f for f in floors if f[2] == z0]
    if fl:
        under = []
        if any(f[1] == wy[0] for f in fl):
            under.append('north row')
        if any(f[1] == wy[1] for f in fl):
            under.append('south row')
        if any(f[0] == wx[0] for f in fl):
            under.append('west column')
        if any(f[0] == wx[1] for f in fl):
            under.append('east column')
        floor_rows['floor at wall Z under: ' + (', '.join(under) or 'inside only')] += 1
    print('0x%04X walls x%d..%d y%d..%d z%d | lowest roof z%d x%d..%d y%d..%d' % (mid, wx[0], wx[1], wy[0], wy[1], z0, rz, rx[0], rx[1], ry[0], ry[1]))
print('\nRoof offsets (count of multis):')
for k, v in offs.most_common():
    print('  %3d  %s' % (v, k))
print('\nFloor tiles (count of multis):')
for k, v in floor_rows.most_common():
    print('  %3d  %s' % (v, k))
