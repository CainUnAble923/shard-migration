# Count differing statics blocks per facet, 114 (OLD) vs 117 (NEW). Writes changed_statics.json
import json, hashlib, os
from uodata import *

res = {}
for fi, (name, w, h) in FACETS.items():
    bw, bh = w >> 3, h >> 3
    n = bw * bh
    io, so = load_statics_index(OLD, fi)
    inn, sn = load_statics_index(NEW, fi)
    changed = []
    changed_unordered = 0
    for b in range(n):
        lo, llo, _ = io[b] if b < len(io) else (-1, 0, 0)
        ln, lln, _ = inn[b] if b < len(inn) else (-1, 0, 0)
        a = so[lo:lo + llo] if lo >= 0 and llo > 0 else b""
        c = sn[ln:ln + lln] if ln >= 0 and lln > 0 else b""
        if a != c:
            sa = block_statics(io, so, b)
            sc = block_statics(inn, sn, b)
            if sorted(sa) != sorted(sc):
                changed.append(b)
            else:
                changed_unordered += 1
    xs = [b // bh for b in changed]
    ys = [b % bh for b in changed]
    info = dict(name=name, blocks=n, idx_entries_old=len(io), idx_entries_new=len(inn), changed=len(changed),
                reorder_only=changed_unordered)
    if changed:
        info["bbox_tiles"] = [min(xs) * 8, min(ys) * 8, max(xs) * 8 + 7, max(ys) * 8 + 7]
    res[fi] = dict(info=info, blocks=changed)
    print(fi, info)
json.dump(res, open(os.path.join(os.path.dirname(__file__), "changed_statics.json"), "w"))
