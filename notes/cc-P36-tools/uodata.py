# Read-only helpers for UO client data (P24 s1b). ASCII only.
import struct, os, zlib
import numpy as np

OLD = r"D:\ShatteredLegacy\client-data\classic-client"
NEW = r"D:\ShatteredLegacy\client-data\classic-client-7.0.117.0"  # cc-P36: the copy, not the EA install

# map-definitions.json (pinned Distribution/Data/map-definitions.json)
FACETS = {0: ("Felucca", 7168, 4096), 1: ("Trammel", 7168, 4096), 2: ("Ilshenar", 2304, 1600),
          3: ("Malas", 2560, 2048), 4: ("Tokuno", 1448, 1448), 5: ("TerMur", 1280, 4096)}


def hashlittle2(s):
    # port of pinned Projects/Server/Client/UOPFiles.cs HashLittle2
    M = 0xFFFFFFFF
    length = len(s)
    a = b = c = (0xDEADBEEF + length) & M
    k = 0
    o = [ord(ch) for ch in s]

    def rot(x, n):
        return ((x << n) | (x >> (32 - n))) & M
    while length > 12:
        a = (a + o[k] + (o[k+1] << 8) + (o[k+2] << 16) + (o[k+3] << 24)) & M
        b = (b + o[k+4] + (o[k+5] << 8) + (o[k+6] << 16) + (o[k+7] << 24)) & M
        c = (c + o[k+8] + (o[k+9] << 8) + (o[k+10] << 16) + (o[k+11] << 24)) & M
        a = (a - c) & M; a ^= rot(c, 4); c = (c + b) & M
        b = (b - a) & M; b ^= rot(a, 6); a = (a + c) & M
        c = (c - b) & M; c ^= rot(b, 8); b = (b + a) & M
        a = (a - c) & M; a ^= rot(c, 16); c = (c + b) & M
        b = (b - a) & M; b ^= rot(a, 19); a = (a + c) & M
        c = (c - b) & M; c ^= rot(b, 4); b = (b + a) & M
        length -= 12
        k += 12
    if length != 0:
        if length >= 12: c = (c + (o[k+11] << 24)) & M
        if length >= 11: c = (c + (o[k+10] << 16)) & M
        if length >= 10: c = (c + (o[k+9] << 8)) & M
        if length >= 9: c = (c + o[k+8]) & M
        if length >= 8: b = (b + (o[k+7] << 24)) & M
        if length >= 7: b = (b + (o[k+6] << 16)) & M
        if length >= 6: b = (b + (o[k+5] << 8)) & M
        if length >= 5: b = (b + o[k+4]) & M
        if length >= 4: a = (a + (o[k+3] << 24)) & M
        if length >= 3: a = (a + (o[k+2] << 16)) & M
        if length >= 2: a = (a + (o[k+1] << 8)) & M
        if length >= 1: a = (a + o[k]) & M
        c ^= b; c = (c - rot(b, 14)) & M
        a ^= c; a = (a - rot(c, 11)) & M
        b ^= a; b = (b - rot(a, 25)) & M
        c ^= b; c = (c - rot(b, 16)) & M
        a ^= c; a = (a - rot(c, 4)) & M
        b ^= a; b = (b - rot(a, 14)) & M
        c ^= b; c = (c - rot(b, 24)) & M
    return (b << 32) | c


def read_uop(path):
    """Return (version, list of entries dict) in table order."""
    with open(path, "rb") as f:
        data = f.read()
    magic, ver, sig, nxt = struct.unpack_from("<IiIq", data, 0)
    assert magic == 0x50594D, path
    entries = []
    while nxt:
        cnt, nxt2 = struct.unpack_from("<iq", data, nxt)
        p = nxt + 12
        for i in range(cnt):
            off, hl, cl, dl, h, adler, flag = struct.unpack_from("<qiiiQIh", data, p)
            p += 34
            if off:
                entries.append(dict(off=off, hl=hl, cl=cl, dl=dl, hash=h, adler=adler, flag=flag))
        nxt = nxt2
    return ver, entries, data


def uop_by_name(path, root, ext, count, prec):
    ver, entries, data = read_uop(path)
    byhash = {e["hash"]: e for e in entries}
    out = {}
    for i in range(count):
        name = f"build/{root}/{i:0{prec}d}{ext}"
        e = byhash.get(hashlittle2(name))
        if e:
            out[i] = e
    return ver, out, data, entries


def load_land(folder, fi):
    """Return land as numpy arrays id[x,y], z[x,y] for facet fi from map{fi}LegacyMUL.uop."""
    name, w, h = FACETS[fi]
    path = os.path.join(folder, f"map{fi}LegacyMUL.uop")
    ver, ents, data, allents = uop_by_name(path, f"map{fi}legacymul", ".dat", 0x14000, 8)
    raw = bytearray()
    for i in sorted(ents):
        e = ents[i]
        assert e["flag"] == 0, "compressed map chunk"
        s = e["off"] + e["hl"]
        raw += data[s:s + e["dl"]]
    bw, bh = w >> 3, h >> 3
    nblocks = bw * bh
    need = nblocks * 196
    raw = bytes(raw[:need])
    arr = np.frombuffer(raw, dtype=np.uint8).reshape(nblocks, 196)
    hdr = arr[:, :4].copy().view("<u4").reshape(nblocks)
    cells = arr[:, 4:].reshape(nblocks, 64, 3)
    ids = (cells[:, :, 0].astype(np.uint16) | (cells[:, :, 1].astype(np.uint16) << 8))
    zs = cells[:, :, 2].view(np.int8)
    # block index = bx*bh + by ; cell index = cy*8 + cx
    # cc-P181: cell index is cy * 8 + cx, so the 8 x 8 block reshapes to [bx][by][cy][cx]; the old transpose
    # (0, 2, 1, 3) swapped x and y inside every block (checked against vseUOAware inspect_map_region at 5144-5155,
    # 1159-1162 and against TileMatrix's reader). (0, 3, 1, 2) puts cx with bx and cy with by.
    ids = ids.reshape(bw, bh, 8, 8).transpose(0, 3, 1, 2).reshape(w, h)
    zs = zs.reshape(bw, bh, 8, 8).transpose(0, 3, 1, 2).reshape(w, h)
    return dict(ver=ver, nent=len(ents), nall=len(allents), hdr=hdr, ids=ids, z=zs, rawlen=len(raw))


def load_statics_index(folder, fi):
    with open(os.path.join(folder, f"staidx{fi}.mul"), "rb") as f:
        idx = np.frombuffer(f.read(), dtype="<i4").reshape(-1, 3)
    with open(os.path.join(folder, f"statics{fi}.mul"), "rb") as f:
        sta = f.read()
    return idx, sta


def block_statics(idx, sta, b):
    if b >= len(idx):
        return []
    look, ln, _ = idx[b]
    if look < 0 or ln <= 0:
        return []
    out = []
    for p in range(look, look + (ln // 7) * 7, 7):
        tid, x, y, z, hue = struct.unpack_from("<HBBbh", sta, p)
        out.append((tid, x, y, z, hue))
    return out


def read_tiledata(folder):
    with open(os.path.join(folder, "tiledata.mul"), "rb") as f:
        d = f.read()
    assert len(d) >= 3188736
    land, items = [], []
    p = 0
    for g in range(0x4000 // 32):
        p += 4
        for i in range(32):
            flags, tex = struct.unpack_from("<QH", d, p)
            nm = d[p + 10:p + 30].split(b"\0")[0].decode("ascii", "replace")
            land.append((flags, tex, nm))
            p += 30
    for g in range(0x10000 // 32):
        p += 4
        for i in range(32):
            flags, wt, qual, anim, u1, qty, u2, u3, val, ht = struct.unpack_from("<QBBHBBiBBB", d, p)
            nm = d[p + 21:p + 41].split(b"\0")[0].decode("ascii", "replace")
            items.append(dict(flags=flags, weight=wt, quality=qual, anim=anim, u1=u1, qty=qty, u2=u2, u3=u3,
                              value=val, height=ht, name=nm))
            p += 41
    assert p == len(d), (p, len(d))
    return land, items


FLAGNAMES = ["Background", "Weapon", "Transparent", "Translucent", "Wall", "Damaging", "Impassable", "Wet",
             "Unknown1", "Surface", "Bridge", "Generic", "Window", "NoShoot", "ArticleA", "ArticleAn", "Internal",
             "Foliage", "PartialHue", "Unknown2", "Map", "Container", "Wearable", "LightSource", "Animation",
             "NoDiagonal", "Unknown3", "Armor", "Roof", "Door", "StairBack", "StairRight"]


def flagstr(v):
    s = [FLAGNAMES[i] for i in range(32) if v >> i & 1]
    s += [f"HS{i+1}" for i in range(32, 64) if v >> i & 1]
    return "|".join(s) if s else "None"
