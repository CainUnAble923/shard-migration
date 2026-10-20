"""Minimal read-only UO map/statics/tiledata/cliloc reader for the P151 survey."""
import struct, os, functools

CLIENT = r"D:/ShatteredLegacy/client-data/classic-client"
# facet -> (width, height) in tiles
SIZES = {0: (7168, 4096), 1: (7168, 4096), 2: (2304, 1600), 3: (2560, 2048), 4: (1448, 1448), 5: (1280, 4096)}

F_BACKGROUND = 0x1
F_WEAPON = 0x2
F_WALL = 0x10
F_DAMAGING = 0x20
F_IMPASSABLE = 0x40
F_WET = 0x80
F_SURFACE = 0x200
F_BRIDGE = 0x400
F_FOLIAGE = 0x20000
F_ROOF = 0x10000000
F_DOOR = 0x20000000


def _hashlittle2(s: bytes):
    length = len(s)
    a = b = c = (0xDEADBEEF + length) & 0xFFFFFFFF
    k = 0
    M = 0xFFFFFFFF

    def rot(x, n):
        return ((x << n) | (x >> (32 - n))) & M

    while length > 12:
        a = (a + (s[k] | s[k+1] << 8 | s[k+2] << 16 | s[k+3] << 24)) & M
        b = (b + (s[k+4] | s[k+5] << 8 | s[k+6] << 16 | s[k+7] << 24)) & M
        c = (c + (s[k+8] | s[k+9] << 8 | s[k+10] << 16 | s[k+11] << 24)) & M
        a = (a - c) & M; a ^= rot(c, 4); c = (c + b) & M
        b = (b - a) & M; b ^= rot(a, 6); a = (a + c) & M
        c = (c - b) & M; c ^= rot(b, 8); b = (b + a) & M
        a = (a - c) & M; a ^= rot(c, 16); c = (c + b) & M
        b = (b - a) & M; b ^= rot(a, 19); a = (a + c) & M
        c = (c - b) & M; c ^= rot(b, 4); b = (b + a) & M
        length -= 12
        k += 12
    if length == 0:
        return (b << 32) | c
    rem = s[k:k+length]
    a = (a + sum(rem[i] << (8*i) for i in range(0, min(4, length)))) & M
    b = (b + sum(rem[i] << (8*(i-4)) for i in range(4, min(8, length)))) & M
    c = (c + sum(rem[i] << (8*(i-8)) for i in range(8, length))) & M
    c ^= b; c = (c - rot(b, 14)) & M
    a ^= c; a = (a - rot(c, 11)) & M
    b ^= a; b = (b - rot(a, 25)) & M
    c ^= b; c = (c - rot(b, 16)) & M
    a ^= c; a = (a - rot(c, 4)) & M
    b ^= a; b = (b - rot(a, 14)) & M
    c ^= b; c = (c - rot(b, 24)) & M
    return (b << 32) | c


@functools.lru_cache(None)
def tiledata():
    data = open(os.path.join(CLIENT, "tiledata.mul"), "rb").read()
    land = []
    off = 0
    for g in range(512):
        off += 4
        for i in range(32):
            flags, tex = struct.unpack_from("<QH", data, off)
            name = data[off+10:off+30].split(b"\0")[0].decode("latin1")
            land.append((flags, name))
            off += 30
    stat = []
    while off + 4 + 32*41 <= len(data):
        off += 4
        for i in range(32):
            flags = struct.unpack_from("<Q", data, off)[0]
            height = data[off+20]
            name = data[off+21:off+41].split(b"\0")[0].decode("latin1")
            stat.append((flags, height, name))
            off += 41
    return land, stat


class Facet:
    def __init__(self, n):
        self.n = n
        self.w, self.h = SIZES[n]
        self.bh = self.h // 8
        path = os.path.join(CLIENT, f"map{n}LegacyMUL.uop")
        self._map = self._read_uop(path, f"build/map{n}legacymul/{{:08d}}.dat")
        self._idx = open(os.path.join(CLIENT, f"staidx{n}.mul"), "rb").read()
        self._sta = open(os.path.join(CLIENT, f"statics{n}.mul"), "rb").read()
        self._land_cache = {}
        self._stat_cache = {}

    @staticmethod
    def _read_uop(path, pattern):
        f = open(path, "rb")
        raw = f.read()
        magic, ver, sig, nxt, blocksize, count = struct.unpack_from("<IIIQII", raw, 0)
        entries = {}
        while nxt:
            files, nxt2 = struct.unpack_from("<IQ", raw, nxt)
            p = nxt + 12
            for i in range(files):
                off, hl, cl, dl, h, adl, fl = struct.unpack_from("<QIIIQIH", raw, p)
                p += 34
                if off:
                    entries[h] = (off + hl, dl)
            nxt = nxt2
        out = bytearray()
        i = 0
        while True:
            h = _hashlittle2(pattern.format(i).encode())
            if h not in entries:
                break
            o, l = entries[h]
            out += raw[o:o+l]
            i += 1
        return bytes(out)

    def land(self, x, y):
        b = (x >> 3) * self.bh + (y >> 3)
        off = b * 196 + 4 + ((y & 7) * 8 + (x & 7)) * 3
        tid, z = struct.unpack_from("<Hb", self._map, off)
        return tid, z

    def statics_block(self, bx, by):
        key = (bx, by)
        if key in self._stat_cache:
            return self._stat_cache[key]
        b = bx * self.bh + by
        look, length, _ = struct.unpack_from("<iii", self._idx, b * 12)
        res = {}
        if look >= 0 and length > 0:
            for i in range(length // 7):
                tid, sx, sy, z, hue = struct.unpack_from("<HBBbH", self._sta, look + i*7)
                res.setdefault((bx*8+sx, by*8+sy), []).append((tid, z))
        self._stat_cache[key] = res
        return res

    def statics(self, x, y):
        return self.statics_block(x >> 3, y >> 3).get((x, y), [])


@functools.lru_cache(None)
def cliloc():
    data = open(os.path.join(CLIENT, "Cliloc.enu"), "rb").read()
    out = {}
    p = 6
    while p + 7 <= len(data):
        num, flag, ln = struct.unpack_from("<iBH", data, p)
        p += 7
        out[num] = data[p:p+ln].decode("utf8", "replace")
        p += ln
    return out
