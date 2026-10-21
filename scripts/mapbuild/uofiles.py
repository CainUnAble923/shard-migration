"""Client map files, read and written the way pinned ModernUO reads them (cc-P181; readers from P24/P36's uodata.py
with the load_land in-block transpose fixed).

Facts this module rests on, each checked against D:/UO/ModernUO-pinned:
  - map{N}LegacyMUL.uop holds 196-byte blocks of 8 x 8 land cells (4-byte header, then id:u16, z:s8 per cell);
    block index = bx * (height / 8) + by, cell index = (y & 7) * 8 + (x & 7)
    (Projects/Server/TileMatrix/TileMatrix.cs:345  tiles[((y & 0x7) << 3) + (x & 0x7)]).
  - staidx{N}.mul: 12 bytes per block (lookup:i32, length:i32, extra:i32); statics{N}.mul rows are 7 bytes
    (id:u16, x:u8, y:u8, z:s8, hue:u16).
  - tiledata.mul: 0x4000 land records (flags:u64, texture:u16, name[20]) in groups of 32 with a 4-byte group header,
    then 0x10000 item records of 41 bytes the same way (the 7.0.9+ layout, 3,188,736 bytes).
"""
import collections, hashlib, os, shutil, struct
import numpy as np

CLIENT = r"D:\ShatteredLegacy\client-data\classic-client-7.0.117.0"   # read only: the shard's copy of the client files
FACETS = {0: ("Felucca", 7168, 4096), 1: ("Trammel", 7168, 4096), 2: ("Ilshenar", 2304, 1600),
          3: ("Malas", 2560, 2048), 4: ("Tokuno", 1448, 1448), 5: ("TerMur", 1280, 4096)}
VOID = 0x0244

# tiledata flag bits (TileData.cs TileFlag)
BACKGROUND, WEAPON, TRANSPARENT, TRANSLUCENT, WALL, DAMAGING, IMPASSABLE, WET = [1 << i for i in range(8)]
SURFACE, BRIDGE, GENERIC, WINDOW, NOSHOOT = 1 << 9, 1 << 10, 1 << 11, 1 << 12, 1 << 13
CONTAINER, LIGHTSOURCE, ROOF, DOOR = 1 << 21, 1 << 23, 1 << 28, 1 << 29
FLAGNAMES = ["Background", "Weapon", "Transparent", "Translucent", "Wall", "Damaging", "Impassable", "Wet",
             "Unknown1", "Surface", "Bridge", "Generic", "Window", "NoShoot", "ArticleA", "ArticleAn", "Internal",
             "Foliage", "PartialHue", "Unknown2", "Map", "Container", "Wearable", "LightSource", "Animation",
             "NoDiagonal", "Unknown3", "Armor", "Roof", "Door", "StairBack", "StairRight"]


def flagstr(v):
    s = [FLAGNAMES[i] for i in range(32) if v >> i & 1]
    s += ["HS%d" % (i + 1) for i in range(32, 64) if v >> i & 1]
    return "|".join(s) if s else "None"


# ------------------------------------------------------------------------------------------------ uop

def hashlittle2(s):
    """Port of pinned Projects/Server/Client/UOPFiles.cs HashLittle2 (the uop entry hash of a file name)."""
    M = 0xFFFFFFFF
    length = len(s)
    a = b = c = (0xDEADBEEF + length) & M
    k = 0
    o = [ord(ch) for ch in s]

    def rot(x, n):
        return ((x << n) | (x >> (32 - n))) & M
    while length > 12:
        a = (a + o[k] + (o[k + 1] << 8) + (o[k + 2] << 16) + (o[k + 3] << 24)) & M
        b = (b + o[k + 4] + (o[k + 5] << 8) + (o[k + 6] << 16) + (o[k + 7] << 24)) & M
        c = (c + o[k + 8] + (o[k + 9] << 8) + (o[k + 10] << 16) + (o[k + 11] << 24)) & M
        a = (a - c) & M; a ^= rot(c, 4); c = (c + b) & M
        b = (b - a) & M; b ^= rot(a, 6); a = (a + c) & M
        c = (c - b) & M; c ^= rot(b, 8); b = (b + a) & M
        a = (a - c) & M; a ^= rot(c, 16); c = (c + b) & M
        b = (b - a) & M; b ^= rot(a, 19); a = (a + c) & M
        c = (c - b) & M; c ^= rot(b, 4); b = (b + a) & M
        length -= 12
        k += 12
    if length != 0:
        if length >= 12: c = (c + (o[k + 11] << 24)) & M
        if length >= 11: c = (c + (o[k + 10] << 16)) & M
        if length >= 10: c = (c + (o[k + 9] << 8)) & M
        if length >= 9: c = (c + o[k + 8]) & M
        if length >= 8: b = (b + (o[k + 7] << 24)) & M
        if length >= 7: b = (b + (o[k + 6] << 16)) & M
        if length >= 6: b = (b + (o[k + 5] << 8)) & M
        if length >= 5: b = (b + o[k + 4]) & M
        if length >= 4: a = (a + (o[k + 3] << 24)) & M
        if length >= 3: a = (a + (o[k + 2] << 16)) & M
        if length >= 2: a = (a + (o[k + 1] << 8)) & M
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
    """(version, entries in table order, the whole file as bytes)."""
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
    """Entries keyed by their chunk number, for files named build/<root>/<n>.<ext>."""
    ver, entries, data = read_uop(path)
    byhash = {e["hash"]: e for e in entries}
    out = {}
    for i in range(count):
        name = "build/%s/%0*d%s" % (root, prec, i, ext)
        e = byhash.get(hashlittle2(name))
        if e:
            out[i] = e
    return ver, out, data, entries


# ------------------------------------------------------------------------------------------------ land

class MapFile:
    """One facet's land file, with the chunk table resolved so a block's file offset is a lookup."""

    def __init__(self, folder, fi):
        self.name, self.w, self.h = FACETS[fi]
        self.bh = self.h >> 3
        self.path = os.path.join(folder, "map%dLegacyMUL.uop" % fi)
        ver, ents, data, allents = uop_by_name(self.path, "map%dlegacymul" % fi, ".dat", 0x14000, 8)
        self.data = data
        self.starts = []
        pos = 0
        for i in sorted(ents):
            e = ents[i]
            assert e["flag"] == 0, "compressed map chunk"
            self.starts.append((pos, pos + e["dl"], e["off"] + e["hl"]))
            pos += e["dl"]

    def block_offset(self, b):
        off = b * 196
        for s, e, fo in self.starts:
            if s <= off < e:
                return fo + (off - s)
        raise ValueError(b)

    def cell_offset(self, x, y):
        return self.block_offset((x >> 3) * self.bh + (y >> 3)) + 4 + ((y & 7) * 8 + (x & 7)) * 3

    def get(self, x, y):
        return struct.unpack_from("<Hb", self.data, self.cell_offset(x, y))

    def region(self, x1, y1, x2, y2):
        """{(x, y): (id, z)} for the rect, clipped to the facet."""
        out = {}
        for x in range(max(0, x1), min(self.w - 1, x2) + 1):
            for y in range(max(0, y1), min(self.h - 1, y2) + 1):
                out[(x, y)] = self.get(x, y)
        return out


def load_land(folder, fi):
    """Whole-facet numpy arrays ids[x, y], z[x, y]. The block reshapes to [bx][by][cy][cx], so cx pairs with bx and
    cy with by: transpose (0, 3, 1, 2). (P36's uodata.load_land had (0, 2, 1, 3), which swapped x and y inside
    every 8 x 8 block; found by cc-P181 against vseUOAware inspect_map_region.)"""
    name, w, h = FACETS[fi]
    mf = MapFile(folder, fi)
    raw = bytearray()
    for s, e, fo in mf.starts:
        raw += mf.data[fo:fo + (e - s)]
    bw, bh = w >> 3, h >> 3
    nblocks = bw * bh
    arr = np.frombuffer(bytes(raw[:nblocks * 196]), dtype=np.uint8).reshape(nblocks, 196)
    cells = arr[:, 4:].reshape(nblocks, 64, 3)
    ids = (cells[:, :, 0].astype(np.uint16) | (cells[:, :, 1].astype(np.uint16) << 8))
    zs = cells[:, :, 2].view(np.int8)
    ids = ids.reshape(bw, bh, 8, 8).transpose(0, 3, 1, 2).reshape(w, h)
    zs = zs.reshape(bw, bh, 8, 8).transpose(0, 3, 1, 2).reshape(w, h)
    return ids, zs


def write_land(folder, fi, land):
    """Write {(x, y): (id, z)} into the facet's uop in place. Returns {(x, y): (old id, old z)}."""
    mf = MapFile(folder, fi)
    data = bytearray(mf.data)
    changed = {}
    for (x, y), (tid, z) in land.items():
        o = mf.cell_offset(x, y)
        changed[(x, y)] = struct.unpack_from("<Hb", data, o)
        struct.pack_into("<Hb", data, o, tid, z)
    with open(mf.path, "wb") as f:
        f.write(data)
    return changed


# ------------------------------------------------------------------------------------------------ statics

def load_statics_index(folder, fi):
    with open(os.path.join(folder, "staidx%d.mul" % fi), "rb") as f:
        idx = np.frombuffer(f.read(), dtype="<i4").reshape(-1, 3)
    with open(os.path.join(folder, "statics%d.mul" % fi), "rb") as f:
        sta = f.read()
    return idx, sta


def block_statics(idx, sta, b):
    """[(id, cx, cy, z, hue)] of block b."""
    if b >= len(idx):
        return []
    look, ln, _ = idx[b]
    if look < 0 or ln <= 0:
        return []
    out = []
    for p in range(look, look + (ln // 7) * 7, 7):
        out.append(struct.unpack_from("<HBBbh", sta, p))
    return out


def statics_in(folder, fi, x1, y1, x2, y2):
    """[(x, y, z, id)] inside the rect."""
    name, w, h = FACETS[fi]
    bh = h >> 3
    idx, sta = load_statics_index(folder, fi)
    out = []
    for bx in range(max(0, x1) >> 3, (min(w - 1, x2) >> 3) + 1):
        for by in range(max(0, y1) >> 3, (min(h - 1, y2) >> 3) + 1):
            for (tid, cx, cy, z, hue) in block_statics(idx, sta, bx * bh + by):
                x, y = bx * 8 + cx, by * 8 + cy
                if x1 <= x <= x2 and y1 <= y <= y2:
                    out.append((x, y, z, tid))
    return out


def write_statics(folder, fi, statics):
    """Append [(x, y, z, id, ...)] to the facet's statics: each touched block is rewritten at the end of
    statics{N}.mul with its existing rows first, and the index repointed. Returns (blocks written,
    [(block, rows it already held)])."""
    name, w, h = FACETS[fi]
    bh = h >> 3
    idx_path, sta_path = os.path.join(folder, "staidx%d.mul" % fi), os.path.join(folder, "statics%d.mul" % fi)
    idx = bytearray(open(idx_path, "rb").read())
    sta = bytearray(open(sta_path, "rb").read())
    by_block = collections.defaultdict(list)
    for s in statics:
        x, y, z, tid = s[0], s[1], s[2], s[3]
        by_block[(x >> 3) * bh + (y >> 3)].append((tid, x & 7, y & 7, z, 0))
    kept = []
    for b, rows in sorted(by_block.items()):
        look, ln, extra = struct.unpack_from("<iii", idx, b * 12)
        existing = []
        if look >= 0 and ln > 0:
            for p in range(look, look + (ln // 7) * 7, 7):
                existing.append(struct.unpack_from("<HBBbh", sta, p))
        rows = existing + rows
        newlook = len(sta)
        for r in rows:
            sta += struct.pack("<HBBbh", *r)
        struct.pack_into("<iii", idx, b * 12, newlook, len(rows) * 7, extra)
        if existing:
            kept.append((b, len(existing)))
    with open(idx_path, "wb") as f:
        f.write(idx)
    with open(sta_path, "wb") as f:
        f.write(sta)
    return len(by_block), kept


def remove_statics(folder, fi, statics):
    """Remove [(x, y, z, id, ...)] from the facet's statics: each touched block is rewritten at the end of
    statics{N}.mul without one matching row per entry (id, cell, z; hue ignored), and the index repointed.
    Returns (rows removed, [(x, y, z, id) not found]). cc-P188: the way in through Old Haven's ruined bank."""
    name, w, h = FACETS[fi]
    bh = h >> 3
    idx_path, sta_path = os.path.join(folder, "staidx%d.mul" % fi), os.path.join(folder, "statics%d.mul" % fi)
    idx = bytearray(open(idx_path, "rb").read())
    sta = bytearray(open(sta_path, "rb").read())
    by_block = collections.defaultdict(list)
    for s in statics:
        x, y, z, tid = s[0], s[1], s[2], s[3]
        by_block[(x >> 3) * bh + (y >> 3)].append((tid, x & 7, y & 7, z))
    removed, missing = 0, []
    for b, wanted in sorted(by_block.items()):
        look, ln, extra = struct.unpack_from("<iii", idx, b * 12)
        rows = []
        if look >= 0 and ln > 0:
            for p in range(look, look + (ln // 7) * 7, 7):
                rows.append(struct.unpack_from("<HBBbh", sta, p))
        for (tid, cx, cy, z) in wanted:
            hit = next((i for i, r in enumerate(rows) if r[0] == tid and r[1] == cx and r[2] == cy and r[3] == z), None)
            if hit is None:
                bx, by = divmod(b, bh)
                missing.append((bx * 8 + cx, by * 8 + cy, z, tid))
                continue
            del rows[hit]
            removed += 1
        if rows:
            newlook = len(sta)
            for r in rows:
                sta += struct.pack("<HBBbh", *r)
            struct.pack_into("<iii", idx, b * 12, newlook, len(rows) * 7, extra)
        else:
            struct.pack_into("<iii", idx, b * 12, -1, -1, extra)
    with open(idx_path, "wb") as f:
        f.write(idx)
    with open(sta_path, "wb") as f:
        f.write(sta)
    return removed, missing


def verify(folder, fi, land, statics):
    """Re-read the files and compare every planned tile. Returns (land mismatches, statics match, statics read)."""
    mf = MapFile(folder, fi)
    bad = sum(1 for (x, y), (tid, z) in land.items() if mf.get(x, y) != (tid, z))
    idx, sta = load_statics_index(folder, fi)
    want = collections.Counter((s[0], s[1], s[2], s[3]) for s in statics)
    have = collections.Counter()
    bh = mf.bh
    for b in {(s[0] >> 3) * bh + (s[1] >> 3) for s in statics}:
        bx, by = divmod(b, bh)
        for (tid, cx, cy, z, hue) in block_statics(idx, sta, b):
            have[(bx * 8 + cx, by * 8 + cy, z, tid)] += 1
    return bad, want == have, sum(have.values())


def restore_scratch(folder, fi, source=CLIENT, hashes="ORIGINAL-SHA256.txt"):
    """Copy the facet's three files from the read-only source over the scratch copies, after proving the source
    files hash as the ORIGINAL-SHA256.txt beside the scratch copies (so a rebuild never stacks on an old build)."""
    want = {}
    for line in open(os.path.join(folder, hashes)):
        h, _, name = line.strip().partition(" *")
        name = name.split("/")[-1]
        if name:
            want[name] = h
    for name in ("map%dLegacyMUL.uop" % fi, "statics%d.mul" % fi, "staidx%d.mul" % fi):
        src = os.path.join(source, name)
        h = hashlib.sha256(open(src, "rb").read()).hexdigest()
        assert h == want[name], (name, h, want[name])
        shutil.copyfile(src, os.path.join(folder, name))
        print("restored", name, h[:12])


# ------------------------------------------------------------------------------------------------ tiledata

_TD = {}


def read_tiledata(folder=CLIENT):
    """(land, items): land[i] = (flags, texture, name); items[i] = dict(flags, height, name, ...). Cached."""
    if folder in _TD:
        return _TD[folder]
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
    _TD[folder] = (land, items)
    return land, items


def impassable_item(tid, folder=CLIENT):
    return bool(read_tiledata(folder)[1][tid]["flags"] & IMPASSABLE)


def impassable_land(tid, folder=CLIENT):
    return bool(read_tiledata(folder)[0][tid][0] & IMPASSABLE)


# ------------------------------------------------------------------------------------------------ the walkable gate

def same_cells(prev, floor, opening, walls):
    """The walkable-floor gate: True when the floor, opening and wall tile sets equal the previous build's record
    ({"floor": [[x, y], ...], "opening": [...], "walls": [...]})."""
    return (sorted(map(tuple, prev["floor"])) == sorted(floor) and sorted(map(tuple, prev["opening"])) == sorted(opening)
            and sorted(map(tuple, prev["walls"])) == sorted(walls))
