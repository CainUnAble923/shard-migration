"""cc-P720: OSI house multis as templates. Lists bounds, piece counts and Z range of each house multi, or dumps one.

    python -P multis.py list
    python -P multis.py dump <id hex>
"""
import os, struct, sys, zlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
from mapbuild import uofiles  # noqa: E402

_cache = {}


def multi(mid):
    """[(x, y, z, tid, flags)] for one multi (pinned MultiData.LoadUOP's record layout)."""
    if 'u' not in _cache:
        _cache['u'] = uofiles.uop_by_name(os.path.join(uofiles.CLIENT, 'MultiCollection.uop'), 'multicollection', '.bin', 0x2000, 6)
    ver, ents, data, allents = _cache['u']
    if mid not in ents:
        return None
    e = ents[mid]
    d = data[e['off'] + e['hl']:e['off'] + e['hl'] + e['cl']]
    if e['flag'] == 1:
        d = zlib.decompress(d)
    count = struct.unpack_from('<I', d, 4)[0]
    p = 8
    out = []
    for i in range(count):
        tid, x, y, z, fl = struct.unpack_from('<HhhhH', d, p)
        p += 10
        n = struct.unpack_from('<I', d, p)[0]
        p += 4 + 4 * n
        out.append((x, y, z, tid, fl))
    return out


if __name__ == '__main__':
    td = uofiles.read_tiledata(uofiles.CLIENT)[1]
    if sys.argv[1] == 'list':
        for mid in list(range(0x64, 0xA4)) + list(range(0xBB, 0xCA)):
            m = multi(mid)
            if not m:
                continue
            xs = [s[0] for s in m]; ys = [s[1] for s in m]; zs = [s[2] for s in m]
            print('0x%04X  x %d..%d  y %d..%d  z %d..%d  pieces %d  flag0 %d  e.g. %s' % (
                mid, min(xs), max(xs), min(ys), max(ys), min(zs), max(zs), len(m), sum(1 for s in m if s[4] == 0),
                td[m[1][3]]['name'] if len(m) > 1 else ''))
    else:
        for s in sorted(multi(int(sys.argv[2], 16)), key=lambda s: (s[2], s[1], s[0])):
            print('%3d %3d %3d 0x%04X fl%d %s' % (s[0], s[1], s[2], s[3], s[4], td[s[3]]['name']))
