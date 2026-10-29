"""cc-P679 (SoS swap S4): the land the server reads, with the statics index cached.

The overlay (docker/uo/Build-MapOverlay.ps1's output: the SoS base with our trammel.mapops) is the folder; tiledata comes
from MAPBUILD_CLIENT. Trammel and Felucca both read these three files (server/customizations/Maps/SosMaps.cs).
P677's spots.Land gives the standing rule; this only caches the statics so a few thousand look-ups stay quick.
"""
import functools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(DOCS, 'scripts'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P677-tools'))
from mapbuild import uofiles  # noqa: E402

uofiles.load_statics_index = functools.lru_cache(maxsize=4)(uofiles.load_statics_index)
import spots  # noqa: E402


def land(folder):
    return spots.Land(folder)


def all_statics(folder, fi=1):
    """Every static: yields (x, y, z, id)."""
    name, w, h = uofiles.FACETS[fi]
    bh = h >> 3
    idx, sta = uofiles.load_statics_index(folder, fi)
    for b in range(len(idx)):
        bx, by = divmod(b, bh)
        for (tid, cx, cy, z, hue) in uofiles.block_statics(idx, sta, b):
            yield bx * 8 + cx, by * 8 + cy, z, tid
