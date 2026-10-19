# measure where each wall piece's art sits inside its 44 px tile cell: static art from the scratch art.mul/artidx.mul
# (unpacked by P167). The client draws static art centred on the tile (posX = sx - w/2 + 22) and bottom-aligned
# (posY = sy - h + 44), so column 22 of a 44-wide base is the tile's centre line; the diamond's top corner is at
# (22, 0), right corner (44, 22), bottom corner (22, 44), left corner (0, 22) in cell coordinates.
import struct, sys
FOLDER = r'D:\UO\cc-p167-work\scratch-client'
idx = open(FOLDER + r'\artidx.mul', 'rb').read()
mul = open(FOLDER + r'\art.mul', 'rb').read()

def static_art(tid):
    look, ln, extra = struct.unpack_from('<iii', idx, (0x4000 + tid) * 12)
    if look < 0 or ln <= 0:
        return None
    d = mul[look:look + ln]
    flag, w, h = struct.unpack_from('<IHH', d, 0)
    lut = struct.unpack_from('<%dH' % h, d, 8)
    base = 8 + 2 * h
    rows = []
    for y in range(h):
        p = base + lut[y] * 2
        x = 0
        row = set()
        while True:
            xo, rl = struct.unpack_from('<HH', d, p); p += 4
            if xo == 0 and rl == 0:
                break
            x += xo
            for i in range(rl):
                px = struct.unpack_from('<H', d, p)[0]; p += 2
                if px:
                    row.add(x + i)
            x += rl
        rows.append(row)
    return w, h, rows

for a in sys.argv[1:]:
    tid = int(a, 16)
    r = static_art(tid)
    if r is None:
        print('0x%04X no art' % tid); continue
    w, h, rows = r
    cx = w // 2  # tile centre column (the client centres the art)
    # per row (from the bottom): leftmost and rightmost pixel relative to the centre column
    print('0x%04X art %dx%d; bottom rows (row from bottom: left..right relative to the tile centre, centre=0):' % (tid, w, h))
    out = []
    for k in range(0, min(h, 48), 4):
        row = rows[h - 1 - k]
        if row:
            out.append('%2d:%+d..%+d' % (k, min(row) - cx, max(row) - cx))
        else:
            out.append('%2d:--' % k)
    print('   ' + '  '.join(out))
    # where is the lowest pixel?
    for k in range(h):
        row = rows[h - 1 - k]
        if row:
            print('   lowest pixel row %d from bottom at x %+d..%+d; ' % (k, min(row) - cx, max(row) - cx), end='')
            break
    left = sum(1 for row in rows for x in row if x < cx); right = sum(1 for row in rows for x in row if x >= cx)
    print('pixels left of centre %d, right %d' % (left, right))
