"""cc-P687 part 3: the seam tiles the dressing pass works on, as arrays (shared by dress.py and the facts).

  new     a seam on SoS (P669's: dry, no static, a 20+ land Z jump to a 4-neighbour) that is not the same seam on stock
          Trammel (identical land id and Z there, and a seam there too): the author's cliffs, not OSI's
  soft    its land is grass, dirt, sand, forest, jungle or snow (sosgrid's terrain classes): a cliff face drawn with a
          stretched ground texture. Mountain rock ('rock', 'cave') draws as OSI's own mountains do and is left
  near    within seams.NEAR of a town rect, a road tile or a public moongate (seams.py), outside S14's closure boxes
"""
import os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
sys.path.insert(0, os.path.join(NOTES, "cc-P681-tools"))
import islands  # noqa: E402
import seams  # noqa: E402
import sosgrid  # noqa: E402

SOFT = ("grass", "dirt", "sand", "forest", "jungle", "snow")


def build(code):
    S = seams.SURFACE
    _, lclass, _, _ = sosgrid.tables()
    ids, zs = islands.load_land("sos")
    _, k, c, _, _, _ = islands.build("sos")
    ti, tz = islands.load_land("trammel")
    _, tk, tc, _, _, _ = islands.build("trammel")
    ids, zs = ids[:S], zs[:S]
    j = seams.jump(zs)
    sos = (j >= 20) & (k[:S] == 0) & (c[:S] == 0)
    stock = (seams.jump(tz[:S]) >= 20) & (tk[:S] == 0) & (tc[:S] == 0)
    new = sos & ~(stock & (ids == ti[:S]) & (zs == tz[:S]))
    soft = np.isin(lclass[ids], [sosgrid.CLASS_NAMES.index(n) for n in SOFT])
    closed = np.zeros(sos.shape, bool)
    for x1, y1, x2, y2 in seams.CLOSURES:
        closed[x1:x2 + 1, y1:y2 + 1] = True
    town = np.zeros(sos.shape, bool)
    for _, (x1, y1, x2, y2) in seams.towns(code):
        town[max(0, x1):min(S, x2), y1:y2] = True
    road = np.zeros(sos.shape, bool)
    for a, b in seams.ROADS:
        road |= (ids >= a) & (ids <= b)
    gate = np.zeros(sos.shape, bool)
    for x, y in seams.MOONGATES:
        gate[x, y] = True
    near = (seams.grow(town, seams.NEAR) | seams.grow(road, seams.NEAR) | seams.grow(gate, seams.NEAR)) & ~closed
    return dict(ids=ids, zs=zs, jump=j, sos=sos, new=new, soft=soft, near=near, road=road, closed=closed,
                target=new & soft & near & ~road)
