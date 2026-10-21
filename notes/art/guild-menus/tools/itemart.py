"""Static item art from artLegacyMUL.uop, and tiledata names (pure stdlib, for the P177 renders)."""
import os, runpy, struct
G = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gumppng.py'), run_name='lib')
DATA = r'D:\ShatteredLegacy\client-data\classic-client-7.0.117.0'
U = G['ffa'].Uop(os.path.join(DATA, 'artLegacyMUL.uop'))
_cache = {}

def item(i):
    if i in _cache:
        return _cache[i]
    d = U.get('build/artlegacymul/%08d.tga' % (0x4000 + i))
    r = (0, 0, [])
    if d and len(d) >= 8:
        w, h = struct.unpack_from('<HH', d, 4)
        look = struct.unpack_from('<%dH' % h, d, 8)
        base = 8 + h * 2
        px = [[(0, 0, 0, 0)] * w for _ in range(h)]
        for y in range(h):
            o = base + look[y] * 2
            x = 0
            while True:
                xo, rl = struct.unpack_from('<HH', d, o)
                o += 4
                if xo + rl == 0:
                    break
                x += xo
                for k in range(rl):
                    c = struct.unpack_from('<H', d, o + k * 2)[0]
                    if x + k < w:
                        px[y][x + k] = (((c >> 10) & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, (c & 31) * 255 // 31, 255)
                o += rl * 2
                x += rl
        r = (w, h, px)
    _cache[i] = r
    return r

def names():
    d = open(os.path.join(DATA, 'tiledata.mul'), 'rb').read()
    land = 512 * (4 + 32 * 30)
    grp = 4 + 32 * 41
    n = (len(d) - land) // grp * 32
    out = []
    for i in range(n):
        o = land + (i // 32) * grp + 4 + (i % 32) * 41
        out.append(d[o + 21:o + 41].split(b'\0')[0].decode('latin1'))
    return out
