# cc-P786 (P785's): is an item's art in our client? Reads artLegacyMUL.uop (entry hash: Bob Jenkins' hashlittle2 of
# "build/artlegacymul/%08d.tga" % (item + 0x4000)) and tiledata.mul (the item's name), as P783's check did.
#   python artcheck.py <client data dir> 0x260F 4013 ...
import struct, sys

def rot(x, k):
    return ((x << k) | (x >> (32 - k))) & 0xFFFFFFFF

def hashlittle2(s):
    data = s.encode("ascii")
    length = len(data)
    a = b = c = (0xDEADBEEF + length) & 0xFFFFFFFF
    i = 0
    while length > 12:
        a = (a + struct.unpack_from("<I", data, i)[0]) & 0xFFFFFFFF
        b = (b + struct.unpack_from("<I", data, i + 4)[0]) & 0xFFFFFFFF
        c = (c + struct.unpack_from("<I", data, i + 8)[0]) & 0xFFFFFFFF
        a = (a - c) & 0xFFFFFFFF; a ^= rot(c, 4);  c = (c + b) & 0xFFFFFFFF
        b = (b - a) & 0xFFFFFFFF; b ^= rot(a, 6);  a = (a + c) & 0xFFFFFFFF
        c = (c - b) & 0xFFFFFFFF; c ^= rot(b, 8);  b = (b + a) & 0xFFFFFFFF
        a = (a - c) & 0xFFFFFFFF; a ^= rot(c, 16); c = (c + b) & 0xFFFFFFFF
        b = (b - a) & 0xFFFFFFFF; b ^= rot(a, 19); a = (a + c) & 0xFFFFFFFF
        c = (c - b) & 0xFFFFFFFF; c ^= rot(b, 4);  b = (b + a) & 0xFFFFFFFF
        length -= 12
        i += 12
    if length == 0:
        return (b << 32) | c
    tail = data[i:] + b"\0" * (12 - length)
    a = (a + struct.unpack_from("<I", tail, 0)[0]) & 0xFFFFFFFF
    b = (b + struct.unpack_from("<I", tail, 4)[0]) & 0xFFFFFFFF
    c = (c + struct.unpack_from("<I", tail, 8)[0]) & 0xFFFFFFFF
    c ^= b; c = (c - rot(b, 14)) & 0xFFFFFFFF
    a ^= c; a = (a - rot(c, 11)) & 0xFFFFFFFF
    b ^= a; b = (b - rot(a, 25)) & 0xFFFFFFFF
    c ^= b; c = (c - rot(b, 16)) & 0xFFFFFFFF
    a ^= c; a = (a - rot(c, 4)) & 0xFFFFFFFF
    b ^= a; b = (b - rot(a, 14)) & 0xFFFFFFFF
    c ^= b; c = (c - rot(b, 24)) & 0xFFFFFFFF
    return (b << 32) | c

cd = sys.argv[1]
uop = open(cd + "/artLegacyMUL.uop", "rb").read()
magic, ver, sig, table, tsize, count = struct.unpack_from("<4sIIqII", uop, 0)
entries = {}
while table:
    n, nxt = struct.unpack_from("<iq", uop, table)
    p = table + 12
    for _ in range(n):
        off, hl, cl, dl, h, adl, flag = struct.unpack_from("<qiiiQIh", uop, p)
        p += 34
        if off:
            entries[h] = (off + hl, cl, dl, flag)
    table = nxt

td = open(cd + "/tiledata.mul", "rb").read()
LAND = 512 * (4 + 32 * 30)

def tdname(item):
    g, k = divmod(item, 32)
    o = LAND + g * (4 + 32 * 41) + 4 + k * 41
    if o + 41 > len(td):
        return None
    return td[o + 21:o + 41].split(b"\0")[0].decode("latin-1")

def art(item):
    h = hashlittle2("build/artlegacymul/%08d.tga" % (item + 0x4000))
    if h not in entries:
        return None
    off, cl, dl, flag = entries[h]
    if flag != 0:
        return ("compressed", cl)
    w, ht = struct.unpack_from("<HH", uop, off + 4)
    return (w, ht)

print("uop entries:", len(entries))
for a in sys.argv[2:]:
    i = int(a, 0)
    r = art(i)
    print(f"{a:>8} {i:6d} {hex(i):>7}  art={r}  tiledata={tdname(i)!r}  {'PRESENT' if r and r != (0, 0) else 'MISSING'}")
