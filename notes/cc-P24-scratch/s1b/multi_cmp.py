import os, struct, zlib
from uodata import *
def comps(folder):
    ver, ents, data, allents = uop_by_name(os.path.join(folder, "MultiCollection.uop"), "multicollection", ".bin", 0x10000, 6)
    out = {}; heads = {}
    for i, e in ents.items():
        raw = data[e["off"] + e["hl"]: e["off"] + e["hl"] + e["cl"]]
        if e["flag"] == 1: raw = zlib.decompress(raw)
        heads[i] = raw[:4]
        cnt, = struct.unpack_from("<I", raw, 4); p = 8; L = []
        for t in range(cnt):
            tid, x, y, z, fl, nc = struct.unpack_from("<HhhhHI", raw, p); p += 14 + 4 * nc
            L.append((tid, x, y, z, fl))
        out[i] = L
    return out, heads
a, ha = comps(OLD); b, hb = comps(NEW)
ch = [i for i in a if i in b and a[i] != b[i]]
print("multis with different components:", len(ch), [hex(i) for i in ch])
print("multis whose first 4 bytes differ:", sum(1 for i in a if i in b and ha[i] != hb[i]))
print("example header", ha[0], hb[0])
for i in set(b) - set(a): print("new multi", hex(i), "components", len(b[i]), "bounds x", min(c[1] for c in b[i]), max(c[1] for c in b[i]), "y", min(c[2] for c in b[i]), max(c[2] for c in b[i]))
