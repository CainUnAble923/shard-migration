# cc-P281: list a multi's components from MultiCollection.uop (as isorender.from_multi reads it), flags included.
# Read only.   python -P multidump.py <multi id hex> [flag0 | all | z<n>]
import os
import struct
import sys
import zlib

sys.path.insert(0, 'D:/UO/golems/Iron/shard-migration/scripts')
from mapbuild import uofiles  # noqa: E402

CLIENT = 'D:/UO/tool-trials/client-data-copy'


def components(mid):
    ver, ents, data, allents = uofiles.uop_by_name(os.path.join(CLIENT, 'MultiCollection.uop'), 'multicollection', '.bin', 0x2000, 6)
    e = ents[mid]
    d = data[e['off'] + e['hl']:e['off'] + e['hl'] + e['cl']]
    if e['flag'] == 1:
        d = zlib.decompress(d)
    count = struct.unpack_from('<I', d, 4)[0]
    p = 8
    rows = []
    for _ in range(count):
        tid, x, y, z, fl = struct.unpack_from('<HhhhH', d, p)
        p += 10
        n = struct.unpack_from('<I', d, p)[0]
        p += 4 + 4 * n
        rows.append((x, y, z, tid, fl))
    return rows


if __name__ == '__main__':
    rows = components(int(sys.argv[1], 16))
    mode = sys.argv[2] if len(sys.argv) > 2 else 'flag0'
    print('components', len(rows), 'x', min(r[0] for r in rows), max(r[0] for r in rows),
          'y', min(r[1] for r in rows), max(r[1] for r in rows), 'z', min(r[2] for r in rows), max(r[2] for r in rows))
    for r in rows:
        if mode == 'all' or (mode == 'flag0' and r[4] == 0) or (mode.startswith('z') and r[2] == int(mode[1:])):
            print(r[0], r[1], r[2], hex(r[3]), r[4])
