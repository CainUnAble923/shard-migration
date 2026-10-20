"""Port of pinned ModernUO Projects/Server/Client/BwtDecompress.cs (read-only use: decode Cliloc.enu)."""
import struct, sys, pickle, os

def decompress(raw):
    # raw: file bytes after the 4-byte header
    first = raw[0]
    table = []
    fb, sb = first, 0
    for i in range(65536):
        table.append((fb + (sb << 8)) & 0xFFFF)
        fb = (fb + 1) & 0xFF
        if fb == 0:
            sb += 1
    table.sort()
    t = table[:256]  # only the first 256 entries are ever touched
    out = bytearray(len(raw))
    i = 0
    for p in range(1, len(raw) + 1):
        cv = first
        v = t[cv]
        if cv > 0:
            t[1:cv + 1] = t[0:cv]
        t[0] = v
        out[i] = v & 0xFF
        i += 1
        first = raw[p] if p < len(raw) else 0xFF
    return internal(out)

def internal(inp):
    sym = bytearray(range(256))
    part = list(struct.unpack_from("<256i", inp, 0)) + [0] * 512
    total = sum(part[:256])
    nonzero = 256 - part[:256].count(0)
    tmp = part[:256]
    freq = bytearray(256)
    for i in range(256):
        value, index = 0, 0
        for j in range(256):
            if tmp[j] > value:
                index, value = j, tmp[j]
        if value == 0:
            break
        freq[i] = index
        tmp[index] = 0
    m = 0
    for i in range(nonzero):
        f = freq[i]
        sym[inp[m + 1024]] = f
        part[f + 256] = m + 1
        m += part[f]
        part[f + 512] = m
    val = sym[0]
    out = bytearray(total)
    count = 0
    while count < total:
        out[count] = val
        fv = part[val + 256]
        if fv >= part[val + 512]:
            if nonzero > 0:
                nonzero -= 1
                sym[0:nonzero] = sym[1:nonzero + 1]
                val = sym[0]
        else:
            idx = inp[fv + 1024]
            part[val + 256] = fv + 1
            if idx != 0:
                sym[0:idx] = sym[1:idx + 1]
                sym[idx] = val
                val = sym[0]
        count += 1
    return bytes(out)

if __name__ == "__main__":
    data = open(sys.argv[1], "rb").read()
    dec = decompress(data[4:])
    h2, h1 = struct.unpack_from("<ih", dec, 0)
    print("headers", h2, h1)
    p = 6; d = {}
    while p + 7 <= len(dec):
        n, fl, ln = struct.unpack_from("<iBH", dec, p); p += 7
        d[n] = dec[p:p + ln].decode("utf8", "replace"); p += ln
    print(len(d), d.get(1016093), d.get(1012004))
    pickle.dump(d, open(sys.argv[2], "wb"))
