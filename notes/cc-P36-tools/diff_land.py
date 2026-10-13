# Compare land cells per facet between 114 and 117 map{n}LegacyMUL.uop. Also report container-level differences.
import json, os, hashlib
import numpy as np
from uodata import *

here = os.path.dirname(os.path.abspath(__file__))
res = {}
for fi, (name, w, h) in FACETS.items():
    a = load_land(OLD, fi)
    b = load_land(NEW, fi)
    # container comparison
    vo, eo, do = read_uop(os.path.join(OLD, f"map{fi}LegacyMUL.uop"))
    vn, en, dn = read_uop(os.path.join(NEW, f"map{fi}LegacyMUL.uop"))
    so = sorted((e["hash"], e["dl"], e["adler"], e["flag"]) for e in eo)
    sn = sorted((e["hash"], e["dl"], e["adler"], e["flag"]) for e in en)
    ent_diff = sum(1 for x, y in zip(so, sn) if x != y) + abs(len(so) - len(sn))
    # payload comparison per chunk by hash
    po = {e["hash"]: do[e["off"] + e["hl"]: e["off"] + e["hl"] + e["dl"]] for e in eo}
    pn = {e["hash"]: dn[e["off"] + e["hl"]: e["off"] + e["hl"] + e["dl"]] for e in en}
    payload_diff = [hh for hh in po if po[hh] != pn.get(hh)]
    hdr_old = do[:40]; hdr_new = dn[:40]
    did = a["ids"] != b["ids"]
    dz = a["z"] != b["z"]
    dcell = did | dz
    hdrdiff = int(np.count_nonzero(a["hdr"] != b["hdr"]))
    info = dict(name=name, uop_version=(vo, vn), entries=(len(eo), len(en)), mapped_entries=(a["nent"], b["nent"]),
                entry_meta_diff=ent_diff, payload_chunks_diff=len(payload_diff), size=(len(do), len(dn)),
                file_header_equal=hdr_old == hdr_new,
                cells_id_diff=int(did.sum()), cells_z_diff=int(dz.sum()), cells_any_diff=int(dcell.sum()),
                block_header_diff=hdrdiff)
    if dcell.any():
        xs, ys = np.nonzero(dcell)
        info["bbox"] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        blocks = sorted(set((int(x) >> 3) * (h >> 3) + (int(y) >> 3) for x, y in zip(xs, ys)))
        info["blocks_diff"] = len(blocks)
        res[fi] = dict(info=info, blocks=blocks)
        np.save(os.path.join(here, f"landdiff{fi}.npy"), np.stack([xs, ys]))
    else:
        res[fi] = dict(info=info, blocks=[])
    # where do the raw byte differences lie, if no cell differs?
    if payload_diff and not dcell.any():
        info["note"] = "payload differs but cells equal"
    print(fi, info)
json.dump(res, open(os.path.join(here, "changed_land.json"), "w"))
