r"""cc-P682 (SoS swap S10): shared loaders for the town survey, the spawn builder and the facts.
The map is P481's copy of the SoS Trammel files (notes\cc-P481-tools\scratch\sos), read through P681's sosgrid (the
playbook's walk rules, vectorized). Tiledata is the vanilla client's (D:\UO\UltimaOnlineVanilla), which SoS ships no
replacement for.
"""
import json
import os
import sys

os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\UltimaOnlineVanilla")

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
DOCS = os.path.dirname(NOTES)
sys.path.insert(0, os.path.join(NOTES, "cc-P681-tools"))
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
sys.path.insert(0, os.path.join(DOCS, "scripts"))

import numpy as np  # noqa: E402

import sosgrid  # noqa: E402
import islands  # noqa: E402
from mapbuild import uofiles  # noqa: E402

# the code copy beside this docs copy (a Golem's D:\UO\golems\<name>\ShatteredLegacy), or SL_SHARD
SHARD = os.environ.get("SL_SHARD", os.path.join(os.path.dirname(DOCS), "ShatteredLegacy"))
PINNED = r"D:\UO\ModernUO-pinned\Distribution\Data"
OUT = os.path.join(HERE, "out")
NONE = sosgrid.NONE
W, H = sosgrid.W, sosgrid.H

TOWNS = ["Valunstead", "Hammerhill", "Kameron Kove", "Elmhaven", "Kettleburg", "Fort Yondall"]

# P673 S14's closure boxes (inclusive), copied by P698: nothing of S10's stands in them before S19 / S14 opens them.
CLOSURES = {
    "Rooster island": (2840, 1324, 3039, 1523),
    "Northeast snow isles": (4224, 256, 4479, 767),
    "Bare land east of Haven": (3072, 2304, 3199, 2559),
    "Echoback/Darkfathom edge cells": (4096, 2560, 4223, 2815),
    "Glimmerwood seam cells": (2688, 2688, 2943, 3071),
}


def in_closure(x, y):
    return any(x1 <= x <= x2 and y1 <= y <= y2 for x1, y1, x2, y2 in CLOSURES.values())


def regions():
    """The shard's Trammel regions on SoS (P676's regions-trammel.json): name -> list of (x1, y1, x2, y2) exclusive."""
    out = {}
    for r in json.load(open(os.path.join(SHARD, "server", "data", "regions-trammel.json"), encoding="utf-8")):
        if r.get("Name"):
            out.setdefault(r["Name"], []).extend((a["x1"], a["y1"], a["x2"], a["y2"]) for a in r.get("Area", []))
    return out


def region_records():
    return json.load(open(os.path.join(SHARD, "server", "data", "regions-trammel.json"), encoding="utf-8"))


def in_rects(x, y, rects):
    return any(x1 <= x < x2 and y1 <= y < y2 for x1, y1, x2, y2 in rects)


def rect_mask(rects):
    m = np.zeros((W, H), dtype=bool)
    for x1, y1, x2, y2 in rects:
        m[max(0, x1):min(W, x2), max(0, y1):min(H, y2)] = True
    return m


_items = None


def item_names():
    global _items
    if _items is None:
        _items = [it["name"].lower() for it in uofiles.read_tiledata(uofiles.CLIENT)[1]]
    return _items


_statics = None


def statics():
    """(x, y, z, id) arrays of every SoS static, sorted by x * H + y, and the sort keys."""
    global _statics
    if _statics is None:
        sx, sy, sz, sid = islands.load_statics("sos")
        key = sx.astype(np.int64) * H + sy.astype(np.int64)
        o = np.argsort(key, kind="stable")
        _statics = (sx[o].astype(np.int32), sy[o].astype(np.int32), sz[o].astype(np.int32), sid[o].astype(np.int32), key[o])
    return _statics


def statics_in_box(x1, y1, x2, y2):
    """Statics with x1 <= x < x2 and y1 <= y < y2."""
    sx, sy, sz, sid, key = statics()
    a, b = np.searchsorted(key, x1 * H), np.searchsorted(key, x2 * H)
    sel = np.arange(a, b)
    m = (sy[sel] >= y1) & (sy[sel] < y2)
    sel = sel[m]
    return sx[sel], sy[sel], sz[sel], sid[sel]


_grid = None


def grid():
    global _grid
    if _grid is None:
        _grid = sosgrid.load()
    return _grid


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")
