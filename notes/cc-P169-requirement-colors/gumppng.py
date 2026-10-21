"""Decode gumpartLegacyMUL.uop entries to PNG (pure stdlib). Usage: gumppng.py OUTDIR ID [ID ...]"""
import importlib.util, os, struct, sys, zlib

import types
_src = open(r'D:\ShatteredLegacy\scripts\find-free-art.py', encoding='utf-8').read()
_src = _src[_src.index('M32 = '):_src.index('# --- art')]
_ns = {'struct': struct, 'zlib': zlib}
exec(_src, _ns)
ffa = types.SimpleNamespace(Uop=_ns['Uop'])

UOP = r'D:\ShatteredLegacy\client-data\classic-client-7.0.117.0\gumpartLegacyMUL.uop'


def bwt(buf):
    # Port of Shard-Console.ps1's Bwt/BwtInternal (from ClassicUO BwtDecompress.cs).
    table = list(range(65536))
    lst = bytearray(len(buf) - 4)
    i = 0
    first = buf[4]
    pos = 5
    while pos < len(buf):
        c = first
        val = table[c]
        table[1:c + 1] = table[0:c]
        table[0] = val
        lst[i] = val & 0xFF
        i += 1
        first = buf[pos]
        pos += 1
    inp = bytes(lst)
    sym = list(range(256))
    part = [0] * 768
    for k in range(256):
        part[k] = struct.unpack_from('<i', inp, k * 4)[0]
    total = sum(part[:256])
    out = bytearray(total)
    tmp = part[:256]
    freq = [0] * 256
    for k in range(256):
        value = index = 0
        for j in range(256):
            if tmp[j] > value:
                index, value = j, tmp[j]
        if value == 0:
            break
        freq[k] = index
        tmp[index] = 0
    nz = sum(1 for k in range(256) if part[k] != 0)
    m = 0
    for k in range(nz):
        f = freq[k]
        sym[inp[m + 1024]] = f
        part[f + 256] = m + 1
        m += part[f]
        part[f + 512] = m
    val = sym[0]
    for count in range(total):
        out[count] = val
        if part[val + 256] >= part[val + 512]:
            if nz > 0:
                nz -= 1
                sym[0:nz] = sym[1:nz + 1]
                val = sym[0]
        else:
            idx = inp[part[val + 256] + 1024]
            part[val + 256] += 1
            if idx != 0:
                sym[0:idx] = sym[1:idx + 1]
                sym[idx] = val
                val = sym[0]
    return bytes(out)


def load(u, g):
    v = u.e.get(_ns['uop_hash']('build/gumpartlegacymul/%08d.tga' % g))
    if not v:
        return None
    u.f.seek(v[0])
    d = u.f.read(v[1])
    if v[3] in (1, 3):
        d = zlib.decompress(d)
    if v[3] == 3:
        d = bwt(d)
    return d


def decode(d):
    w, h = struct.unpack_from('<ii', d, 0)
    body = d[8:]
    table = struct.unpack_from('<%dI' % h, body, 0)
    px = [[(0, 0, 0, 0)] * w for _ in range(h)]
    for y in range(h):
        start = table[y] * 4
        end = table[y + 1] * 4 if y + 1 < h else len(body)
        x = 0
        for o in range(start, end, 4):
            c, run = struct.unpack_from('<HH', body, o)
            if c:
                r, g, b = ((c >> 10) & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, (c & 31) * 255 // 31
                for k in range(run):
                    if x + k < w:
                        px[y][x + k] = (r, g, b, 255)
            x += run
    return w, h, px


def png(path, w, h, px, scale=3):
    raw = b''.join(b'\0' + b''.join(bytes(px[y // scale][x // scale]) for x in range(w * scale)) for y in range(h * scale))
    def chunk(t, data):
        return struct.pack('>I', len(data)) + t + data + struct.pack('>I', zlib.crc32(t + data) & 0xFFFFFFFF)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w * scale, h * scale, 8, 6, 0, 0, 0))
                + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))


u = ffa.Uop(UOP)
out = sys.argv[1]
for g in (map(int, sys.argv[2:]) if __name__ == '__main__' else []):
    d = load(u, g)
    if not d:
        print(g, 'missing')
        continue
    w, h, px = decode(d)
    png(os.path.join(out, 'g%d.png' % g), w, h, px)
    print(g, w, h)
