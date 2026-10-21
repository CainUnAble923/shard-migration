"""cc-P188: unpack the classic art from artLegacyMUL.uop into art.mul and artidx.mul, which isorender.py and
vseUOAware's render_map_region read. P167 did this with a tool that lived in the scratch folder on the game PC and was
lost with it; this one lives in the module so any PC with the client data can make the renders.

    python -P uop2art.py [<client folder>] [<out folder>]

Defaults: the shard's client-data copy (uofiles.CLIENT) and D:/UO/cc-p167-work/scratch-client. The UOP names its
entries build/artlegacymul/<id, 8 digits>.tga for ids 0 to 0x13FFF (0x4000 land, 0x10000 items), some zlib
compressed (flag 1); each is written as is into art.mul with a 12-byte artidx.mul row (lookup, length, extra 0), the
same layout the client's ArtLoader reads for a .mul install. Entries the UOP lacks get lookup -1.
"""
import os, struct, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from mapbuild import uofiles  # noqa: E402

COUNT = 0x14000


def unpack(client, out):
    src = os.path.join(client, 'artLegacyMUL.uop')
    ver, byid, data, entries = uofiles.uop_by_name(src, 'artlegacymul', '.tga', COUNT, 8)
    idx = bytearray()
    mul = bytearray()
    found = 0
    for i in range(COUNT):
        e = byid.get(i)
        if not e:
            idx += struct.pack('<iii', -1, 0, 0)
            continue
        raw = data[e['off'] + e['hl']:e['off'] + e['hl'] + e['cl']]
        if e['flag'] == 1:
            raw = zlib.decompress(raw)
        assert len(raw) == e['dl'], (i, len(raw), e['dl'])
        idx += struct.pack('<iii', len(mul), len(raw), 0)
        mul += raw
        found += 1
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'art.mul'), 'wb') as f:
        f.write(mul)
    with open(os.path.join(out, 'artidx.mul'), 'wb') as f:
        f.write(idx)
    print('art entries', found, 'of', COUNT, '; art.mul', len(mul), 'bytes; artidx.mul', len(idx), 'bytes')
    return found


if __name__ == '__main__':
    client = sys.argv[1] if len(sys.argv) > 1 else uofiles.CLIENT
    out = sys.argv[2] if len(sys.argv) > 2 else 'D:/UO/cc-p167-work/scratch-client'
    unpack(client, out)
