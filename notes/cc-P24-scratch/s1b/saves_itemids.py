# Count save items (any parent) whose ItemID is a tile whose tiledata flags changed 114->117.
import struct, os
from collections import Counter
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves_scan.py")).read().replace("\nmain()\n", "\n")
ns = {"__file__": __file__}; exec(compile(src, "saves_scan", "exec"), ns)
ids = set([0xa90e, 0xa90f] + list(range(0xb272, 0xb278)) + list(range(0xb3d2, 0xb3d6)) + list(range(0xb406, 0xb40a)) + [0xb41b, 0xb41c])
for SAVE in (r"D:\ShatteredLegacy\server\lib\uo\modernuo\Saves-test", r"D:\ShatteredLegacy\server\lib\uo\modernuo\Saves"):
    db = ns["types"](os.path.join(SAVE, "SerializedTypes.db")); ver, ents = ns["entries"](SAVE, "Items")
    b_ = open(os.path.join(SAVE, "Items", "Items.bin"), "rb").read(); enc = ns["enc"]
    hits = Counter(); ok = 0
    for h, serial, pos, ln in ents:
        b = b_[pos:pos + ln]
        try:
            flags, = struct.unpack_from("<I", b, 4); m, p = enc(b, 8)
            if flags & 1: p += 1
            if flags & 2: continue
            if flags & 4: p += 1
            if flags & 8:
                _, p = enc(b, p); _, p = enc(b, p); _, p = enc(b, p)
            else:
                if flags & 0x80000: p += 2
                elif flags & 0x40000: p += 4
                if flags & 0x20000: p += 1
            if flags & 0x10:
                iid, p = enc(b, p); ok += 1
                if iid in ids: hits[(db.get(h), hex(iid))] += 1
        except Exception: pass
    print(SAVE, "items", len(ents), "ItemID decoded", ok, "hits", dict(hits))
