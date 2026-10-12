# cc-P34: shared loader for the read-only map checks. Loads the client map1 / statics / tiledata the server
# reads through design/registrar-office/uorender.py, as notes/cc-P31-tools/office_z.py does. Read only.
src = open(r'D:/ShatteredLegacy/design/registrar-office/uorender.py').read()
src = src.replace("os.path.expanduser('~/mnt/ShatteredLegacy/client-data/classic-client')",
                  "r'D:/ShatteredLegacy/client-data/classic-client'")
src = src.replace("'/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'", "'C:/Windows/Fonts/arialbd.ttf'")
RNS = {}
exec(compile(src, 'uor', 'exec'), RNS)
M = RNS['Map'](1); T = RNS['Tiles']()
IMP, WET, SURF, BRIDGE, WALL, DOOR = 0x40, 0x80, 0x200, 0x400, 0x10, 0x20000000
def statics(x, y):
    return [(sid, sz) for (sid, sx, sy, sz, hue) in M.statics(x >> 3, y >> 3) if (x & 7, y & 7) == (sx, sy)]
def name(sid): return T.sname[sid].strip()
def flags(f):
    out = []
    for n, b in (('imp', IMP), ('wall', WALL), ('wet', WET), ('surf', SURF), ('bridge', BRIDGE), ('door', DOOR)):
        if f & b: out.append(n)
    return '|'.join(out) or '-'
def describe(x, y):
    return ' '.join(f"0x{s:04X}@{sz}+{T.sheight[s]}[{flags(T.sflags[s])}]({name(s)})" for s, sz in statics(x, y)) or 'none'
# Land names (tiledata land entry: flags 8, texture 2, name 20), which uorender.Tiles does not keep.
import struct as _st
_d = open(r'D:/ShatteredLegacy/client-data/classic-client/tiledata.mul', 'rb').read(); _o = 0; T.lname = {}
for _g in range(512):
    _o += 4
    for _k in range(32):
        T.lname[_g * 32 + _k] = _d[_o + 10:_o + 30].split(b'\0')[0].decode('latin1'); _o += 30
