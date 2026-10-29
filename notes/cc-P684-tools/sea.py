r"""cc-P684 (SoS swap S11): the SoS map's water, read the way pinned's boat and SOS code read it, and the land the way
the treasure map's ValidateLocation reads it.

    import sea; S = sea.load()

  S.ids, S.z         land tile id and Z for every tile (P481's copy of the SoS Trammel files; Felucca reads the same
                     file, P675)
  S.deep             SOS.cs ValidateDeepWater: the land id is 0x00A8-0x00AB or 0x0136-0x0137 (statics not read)
  S.boat             BaseBoat.CanFit, one tile at Z -5: water land at Z -5 (ids 168-171, 310-311) or a water static
                     (0x1796-0x17B2) at Z -5, and no other static at Z -5 or above
  S.ocean            the largest 4-connected component of S.boat: the open sea a boat sails, so any tile in it is reached
                     from any other and back
  S.seas             every component of S.boat of SEA tiles or more (the open sea and the Lost Lands' sea)
  S.statics_at(x, y) the statics on a tile, as (z, id)
"""
import os
import sys

import numpy as np

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\UltimaOnlineVanilla")
HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
DOCS = os.path.dirname(NOTES)
sys.path.insert(0, os.path.join(NOTES, "cc-P681-tools"))
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
sys.path.insert(0, os.path.join(DOCS, "scripts"))
import islands  # noqa: E402
from mapbuild import uofiles  # noqa: E402

SHARD = os.environ.get("SL_SHARD", os.path.join(os.path.dirname(DOCS), "ShatteredLegacy"))
W, H = 7168, 4096
BOAT_Z = -5
SEA = 100000      # a body of boat water this big is a sea (the open sea; the Lost Lands' own, which Papua's docks serve)
CACHE = os.environ.get("P684_CACHE", r"C:\Users\ckfle\AppData\Local\Temp\p684-sea.npz")


def components(mask):
    """4-connected component labels of a W x H bool mask (0 = not in the mask), by runs per column and union-find."""
    parent = []

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    runs = []          # per column: (starts, ends, ids)
    for x in range(W):
        col = mask[x]
        d = np.diff(np.concatenate(([0], col.view(np.int8), [0])))
        st, en = np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]
        ids = list(range(len(parent), len(parent) + len(st)))
        parent.extend(ids)
        if x and runs[-1][0].size and st.size:
            ps, pe, pid = runs[-1]
            i = j = 0
            while i < len(st) and j < len(ps):
                if st[i] < pe[j] and ps[j] < en[i]:
                    a, b = find(ids[i]), find(pid[j])
                    if a != b:
                        parent[a] = b
                if en[i] < pe[j]:
                    i += 1
                else:
                    j += 1
        runs.append((st, en, ids))
    lab = np.zeros((W, H), dtype=np.int32)
    for x, (st, en, ids) in enumerate(runs):
        for s, e, i in zip(st, en, ids):
            lab[x, s:e] = find(i) + 1
    return lab


class Sea:
    def __init__(self):
        self.ids, z = islands.load_land("sos")
        self.z = z.astype(np.int16)
        sx, sy, sz, sid = islands.load_statics("sos")
        key = sx.astype(np.int64) * H + sy.astype(np.int64)
        o = np.argsort(key, kind="stable")
        self._key, self._sz, self._sid = key[o], sz[o].astype(np.int32), sid[o].astype(np.int32)
        if os.path.exists(CACHE):
            d = np.load(CACHE)
            self.deep, self.boat, self.ocean, self.seas = d["deep"], d["boat"], d["ocean"], d["seas"]
            return
        ids = self.ids
        self.deep = ((ids >= 0xA8) & (ids <= 0xAB)) | ((ids >= 0x136) & (ids <= 0x137))
        water_land = (((ids >= 168) & (ids <= 171)) | ((ids >= 310) & (ids <= 311))) & (self.z == BOAT_Z)
        wst = (sid >= 0x1796) & (sid <= 0x17B2)
        flat = sx.astype(np.int64) * H + sy.astype(np.int64)
        water_static = np.zeros(W * H, dtype=bool)
        water_static[flat[wst & (sz == BOAT_Z)]] = True
        block = np.zeros(W * H, dtype=bool)
        block[flat[~wst & (sz >= BOAT_Z)]] = True
        self.boat = (water_land | water_static.reshape(W, H)) & ~block.reshape(W, H)
        lab = components(self.boat)
        counts = np.bincount(lab.ravel())
        counts[0] = 0
        self.ocean = lab == int(np.argmax(counts))
        self.seas = np.isin(lab, np.nonzero(counts >= SEA)[0])
        np.savez_compressed(CACHE, deep=self.deep, boat=self.boat, ocean=self.ocean, seas=self.seas)

    def statics_at(self, x, y):
        k = x * H + y
        a, b = np.searchsorted(self._key, k), np.searchsorted(self._key, k, side="right")
        return [(int(self._sz[i]), int(self._sid[i])) for i in range(a, b)]


_S = None


def load():
    global _S
    if _S is None:
        _S = Sea()
    return _S


def tiledata():
    return uofiles.read_tiledata(uofiles.CLIENT)


if __name__ == "__main__":
    s = load()
    print("deep (SOS)", int(s.deep.sum()), "boat", int(s.boat.sum()), "ocean", int(s.ocean.sum()))
