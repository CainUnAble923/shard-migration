import struct, sys, json, importlib.util
spec = importlib.util.spec_from_file_location("u", sys.argv[3]); 
src = open(sys.argv[3]).read()
ns = {}; exec(src.split("d = sys.argv[1]")[0], ns)   # reuse hashlittle2 from the P781 script
h2 = ns["hashlittle2"]
cd = sys.argv[1]
uop = open(cd + "/artLegacyMUL.uop", "rb").read()
magic, ver, sig, table, tsize, count = struct.unpack_from("<4sIIqII", uop, 0)
entries = {}
while table:
    n, nxt = struct.unpack_from("<iq", uop, table); p = table + 12
    for i in range(n):
        off, hl, cl, dl, h, adl, flag = struct.unpack_from("<qiiiQIh", uop, p); p += 34
        if off: entries[h] = (off + hl, cl, dl, flag)
    table = nxt
td = open(cd + "/tiledata.mul", "rb").read()
LAND = 512 * (4 + 32 * 30)
def tdname(item):
    g, k = divmod(item, 32)
    o = LAND + g * (4 + 32 * 41) + 4 + k * 41
    if o + 41 > len(td): return None
    return td[o + 21:o + 41].split(b"\0")[0].decode("latin-1")
def art(item):
    h = h2("build/artlegacymul/%08d.tga" % (item + 0x4000))
    if h not in entries: return None
    off, cl, dl, flag = entries[h]
    if flag != 0: return ("compressed", cl)
    w, ht = struct.unpack_from("<HH", uop, off + 4)
    return (w, ht)
pieces = json.load(open(sys.argv[2]))
missing = []; rows = []
for pc in pieces:
    ids = pc.get("unlit", []) + pc.get("lit", []) + pc.get("flip", [])
    for i in ids:
        a = art(i); n = tdname(i)
        rows.append((pc["cls"], i, hex(i), a, n))
        if a is None or a == (0, 0): missing.append((pc["cls"], hex(i)))
print("ids checked:", len(rows), "missing art:", len(missing), missing[:10])
print("tiledata items in file:", (len(td) - LAND) // (4 + 32 * 41) * 32)
for r in rows[:6] + rows[60:64] + rows[-6:]: print(r)
json.dump(rows, open(sys.argv[4], "w"))
