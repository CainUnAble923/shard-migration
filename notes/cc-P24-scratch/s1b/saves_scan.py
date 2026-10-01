# Read-only scan of a ModernUO save: top-level item locations from Items.idx/.bin (base Item header only).
# Layout: pinned Projects/Server/Serialization/GenericEntityPersistence.cs:100-122 (idx v3) and
# Projects/Server/Items/Item.cs:816-1000 (Item.Serialize: version, flags, minutes, [dir], [bounce], [loottype], location).
import struct, sys, os, json
from collections import Counter

SAVE = sys.argv[1] if len(sys.argv) > 1 else r"D:\ShatteredLegacy\server\lib\uo\modernuo\Saves-test"
here = os.path.dirname(os.path.abspath(__file__))

def enc(b, p):
    v = 0; s = 0
    while True:
        c = b[p]; p += 1
        v |= (c & 0x7F) << s; s += 7
        if not c & 0x80: return v, p

def types(path):
    d = open(path, "rb").read()
    ver, cnt = struct.unpack_from("<ii", d, 0); p = 8; db = {}
    for _ in range(cnt):
        h, = struct.unpack_from("<Q", d, p); p += 8
        ln, p = enc(d, p)
        db[h] = d[p:p + ln].decode("utf-8", "replace"); p += ln
    return db

def entries(save, name):
    idx = open(os.path.join(save, name, name + ".idx"), "rb").read()
    ver, cnt = struct.unpack_from("<ii", idx, 0); p = 8
    out = []
    for _ in range(cnt):
        flag, h, serial, created, pos, ln = struct.unpack_from("<BQIqqi", idx, p); p += 33
        assert flag == 2
        out.append((h, serial, pos, ln))
    return ver, out

AREAS = {"skara": (736, 2120, 791, 2167), "east": (6448, 3040, 6959, 3623)}
PAD = 32  # a house multi extends up to ~16 tiles from its centre; pad generously

def main():
    db = types(os.path.join(SAVE, "SerializedTypes.db"))
    ver, ents = entries(SAVE, "Items")
    binf = open(os.path.join(SAVE, "Items", "Items.bin"), "rb").read()
    mapc = Counter(); tot = Counter(); located = 0; bounce = 0; near = []
    houses = Counter(); spawners = Counter()
    for h, serial, pos, ln in ents:
        t = db.get(h, f"?{h:x}")
        tot[t] += 1
        b = binf[pos:pos + ln]
        try:
            v, = struct.unpack_from("<i", b, 0)
            flags, = struct.unpack_from("<I", b, 4)
            m, p = enc(b, 8)
            if flags & 0x200:  # Parent: not on the ground
                continue
            if flags & 0x1: p += 1
            if flags & 0x2: bounce += 1; continue
            if flags & 0x4: p += 1
            x = y = z = 0
            if flags & 0x8:
                x, p = enc(b, p); y, p = enc(b, p); z, p = enc(b, p)
            else:
                if flags & 0x80000: x, y = b[p], b[p + 1]; p += 2
                elif flags & 0x40000: x, y = struct.unpack_from("<hh", b, p); p += 4
                if flags & 0x20000: z = struct.unpack_from("<b", b, p)[0]; p += 1
            hasmap = bool(flags & 0x1000)
            mapi = 0
            if hasmap:
                if flags & 0x10: _, p = enc(b, p)
                if flags & 0x20: _, p = enc(b, p)
                if flags & 0x40: _, p = enc(b, p)
                if flags & 0x80: p += 1
                if flags & 0x100:
                    if b[p]:
                        p += 1; l, p = enc(b, p); p += l
                    else:
                        p += 1
                if flags & 0x400:
                    cnt, = struct.unpack_from("<i", b, p); p += 4 + 4 * cnt
                if flags & 0x1000000: _, p = enc(b, p)
                elif flags & 0x800: p += 8
                mapi = b[p]
                mapc[mapi] += 1
        except Exception as e:
            continue
        located += 1
        tl = t.lower()
        if not hasmap: continue
        if "house" in tl or "multis." in tl or "tent" in tl or "castle" in tl or "keep" in tl or "tower" in tl:
            houses[t] += 1
        if "spawner" in tl:
            spawners[t] += 1
        for an, (ax0, ay0, ax1, ay1) in AREAS.items():
            if hasmap and ax0 - PAD <= x <= ax1 + PAD and ay0 - PAD <= y <= ay1 + PAD:
                near.append(dict(area=an, type=t, serial=hex(serial), x=x, y=y, z=z, map=mapi))
    print("save", SAVE, "idx version", ver, "items", len(ents), "top-level located", located, "bounce-skipped", bounce)
    print("map index distribution of top-level items:", dict(mapc))
    print("house-like types (top-level):", sum(houses.values()), houses.most_common(30))
    print("spawner types (top-level):", sum(spawners.values()), spawners.most_common(10))
    print("top-level items within", PAD, "tiles of a changed area (any map):", len(near))
    c = Counter((n["area"], n["type"]) for n in near)
    for k, v in c.most_common(60): print("  ", k, v)
    json.dump(near, open(os.path.join(here, "saves_near_" + os.path.basename(SAVE.rstrip("\\/")) + ".json"), "w"), indent=0)

main()
