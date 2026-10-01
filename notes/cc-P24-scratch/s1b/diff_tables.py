# tiledata / hues / radarcol / multi.mul / MultiCollection.uop: 114 vs 117
import os, struct, zlib, hashlib
from collections import Counter
from uodata import *

lo, io = read_tiledata(OLD)
ln, inn = read_tiledata(NEW)
print("== tiledata land")
for i in range(0x4000):
    if lo[i] != ln[i]:
        print(f"  land {i:#06x}: {lo[i]} -> {ln[i]}  flags {flagstr(lo[i][0])} -> {flagstr(ln[i][0])}")
print("== tiledata items")
newent = []; changed = []
for i in range(0x10000):
    a, b = io[i], inn[i]
    if a == b: continue
    empty_a = a["flags"] == 0 and a["name"] == "" and a["height"] == 0 and a["weight"] == 0 and a["anim"] == 0
    if empty_a:
        newent.append(i)
    else:
        changed.append(i)
print("  new (empty in 114, filled in 117):", len(newent))
if newent:
    rngs = []; s = p = newent[0]
    for i in newent[1:]:
        if i == p + 1: p = i
        else: rngs.append((s, p)); s = p = i
    rngs.append((s, p))
    print("  ranges:", [(hex(a), hex(b)) for a, b in rngs])
    for i in newent:
        b = inn[i]
        print(f"    {i:#06x} '{b['name']}' h{b['height']} flags {flagstr(b['flags'])}")
print("  changed existing entries:", len(changed))
for i in changed:
    a, b = io[i], inn[i]
    diffs = {k: (a[k], b[k]) for k in a if a[k] != b[k]}
    fs = ""
    if "flags" in diffs:
        fa, fb = a["flags"], b["flags"]
        add = fb & ~fa; rem = fa & ~fb
        fs = f" +[{flagstr(add) if add else ''}] -[{flagstr(rem) if rem else ''}]"
        diffs.pop("flags")
    print(f"    {i:#06x} '{a['name']}' -> '{b['name']}' {diffs}{fs}")

print("== hues.mul")
def hues(folder):
    d = open(os.path.join(folder, "hues.mul"), "rb").read()
    out = []; p = 0
    while p + 708 <= len(d):
        p += 4
        for k in range(8):
            cols = d[p:p + 68]; nm = d[p + 68:p + 88].split(b"\0")[0].decode("ascii", "replace")
            out.append((cols, nm)); p += 88
    return out, len(d)
ho, lho = hues(OLD); hn, lhn = hues(NEW)
print("  sizes", lho, lhn, "hues", len(ho), len(hn))
hd = [i for i in range(min(len(ho), len(hn))) if ho[i] != hn[i]]
print("  differing hues:", len(hd))
for i in hd[:60]:
    print(f"    hue {i+1} (index {i}): name '{ho[i][1]}' -> '{hn[i][1]}' colours_equal={ho[i][0]==hn[i][0]}")
# raw header diffs
do = open(os.path.join(OLD, "hues.mul"), "rb").read(); dn = open(os.path.join(NEW, "hues.mul"), "rb").read()
hdr = [g for g in range(len(do) // 708) if do[g*708:g*708+4] != dn[g*708:g*708+4]]
print("  group headers differing:", len(hdr))

print("== radarcol.mul")
ro = open(os.path.join(OLD, "radarcol.mul"), "rb").read(); rn = open(os.path.join(NEW, "radarcol.mul"), "rb").read()
co = struct.unpack(f"<{len(ro)//2}H", ro); cn = struct.unpack(f"<{len(rn)//2}H", rn)
rd = [i for i in range(len(co)) if co[i] != cn[i]]
print("  entries", len(co), "differing", len(rd), "land", sum(1 for i in rd if i < 0x4000), "items", sum(1 for i in rd if i >= 0x4000))
print("  item ids:", [hex(i - 0x4000) for i in rd if i >= 0x4000][:80])

print("== multi.mul / multi.idx")
for f in ("multi.mul", "multi.idx"):
    print(" ", f, "identical" if open(os.path.join(OLD, f), "rb").read() == open(os.path.join(NEW, f), "rb").read() else "DIFFER")

print("== MultiCollection.uop")
def mc(folder):
    ver, ents, data, allents = uop_by_name(os.path.join(folder, "MultiCollection.uop"), "multicollection", ".bin", 0x10000, 6)
    out = {}
    for i, e in ents.items():
        raw = data[e["off"] + e["hl"]: e["off"] + e["hl"] + e["cl"]]
        if e["flag"] == 1:
            try: raw = zlib.decompress(raw)
            except Exception: raw = zlib.decompress(raw, -15)
        out[i] = raw
    hh = hashlittle2("build/multicollection/housing.bin")
    hous = [e for e in allents if e["hash"] == hh]
    return ver, out, len(allents), hous
vo, mo, no, ho_ = mc(OLD); vn, mn, nn, hn_ = mc(NEW)
print("  version", vo, vn, "entries(all)", no, nn, "multis", len(mo), len(mn))
added = sorted(set(mn) - set(mo)); removed = sorted(set(mo) - set(mn))
chg = sorted(i for i in set(mo) & set(mn) if mo[i] != mn[i])
print("  added multi ids:", [hex(i) for i in added])
print("  removed multi ids:", [hex(i) for i in removed])
print("  changed multi ids:", [hex(i) for i in chg])
print("  housing.bin entry:", [(e['dl'], e['adler']) for e in ho_], [(e['dl'], e['adler']) for e in hn_])
