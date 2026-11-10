"""cc-P855: every art ID in the ShardDecorAddon data files exists in the player package's client art (artidx.mul), with
its tiledata name. The art index and tiledata reading follow P852's survey.py.

  python -P artcheck.py <Addons folder> [client data folder]   (default D:/UO/tool-trials/client-data-copy)
"""
import glob
import os
import re
import struct
import sys

folder = sys.argv[1]
CD = sys.argv[2] if len(sys.argv) > 2 else "D:/UO/tool-trials/client-data-copy"
idx = open(CD + "/artidx.mul", "rb").read()
nidx = len(idx) // 12
td = open(CD + "/tiledata.mul", "rb").read()
LAND = 512 * (4 + 32 * 30)
ITEMREC = 41
GROUP = 4 + 32 * ITEMREC
nitems = (len(td) - LAND) // GROUP * 32


def art_exists(i):
    e = 0x4000 + i
    if e >= nidx:
        return False
    off, ln, _ = struct.unpack_from("<iii", idx, e * 12)
    return off != -1 and ln > 0


def td_name(i):
    if i >= nitems:
        return "?"
    g, r = divmod(i, 32)
    o = LAND + g * GROUP + 4 + r * ITEMREC
    return td[o + 21:o + 41].split(b"\0")[0].decode("latin-1")


bad = 0
ids = {}
for path in sorted(glob.glob(os.path.join(folder, "*.cfg"))):
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^Static 0x([0-9A-Fa-f]+)", line)
        if m:
            ids.setdefault(int(m.group(1), 16), set()).add(os.path.basename(path)[:-4])
for i in sorted(ids):
    ok = art_exists(i)
    bad += not ok
    print(f"0x{i:04X} {'ok     ' if ok else 'MISSING'} {td_name(i):20} {', '.join(sorted(ids[i]))}")
print(f"{len(ids)} distinct art IDs, {bad} missing from {CD}")
sys.exit(1 if bad else 0)
