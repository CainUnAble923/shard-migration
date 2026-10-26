r"""cc-P481: an in-client style (isometric) view of a patch of any surveyed map, stock or downloaded, through
scripts\mapbuild\isorender.py (the classic client's tile layout) fed from islands.py's readers.
    MAPBUILD_CLIENT=D:/UO/UltimaOnlineVanilla python -P iso.py <map> x1 y1 x2 y2 out.png [maxwidth]
Stock art only: a static whose art the stock client lacks would draw nothing (none did in the patches shown).
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))
import islands  # noqa: E402
from mapbuild import isorender  # noqa: E402


def scene(name, x1, y1, x2, y2, pad=1):
    ids, zs = islands.load_land(name)
    land = {}
    for x in range(x1 - pad, x2 + pad + 1):
        for y in range(y1 - pad, y2 + pad + 1):
            land[(x, y)] = (int(ids[x, y]), int(zs[x, y]))
    sx, sy, sz, sid = islands.load_statics(name)
    m = (sx >= x1) & (sx <= x2) & (sy >= y1) & (sy <= y2)
    statics = list(zip(sx[m].tolist(), sy[m].tolist(), sz[m].tolist(), sid[m].tolist()))
    return isorender.Scene(land, statics)


if __name__ == "__main__":
    name = sys.argv[1]
    x1, y1, x2, y2 = (int(v) for v in sys.argv[2:6])
    out = sys.argv[6]
    maxw = int(sys.argv[7]) if len(sys.argv) > 7 else 1400
    im = isorender.render(scene(name, x1, y1, x2, y2), x1, y1, x2, y2)
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    im.convert("RGB").save(out, optimize=True)
    print(out, im.size, os.path.getsize(out))
