"""cc-P687 (SoS swap S14) part 3: the seam-dressing pass, as trammel.mapops S+ lines.

Which seams: seamgrid.build's target (the author's new seams on grass, dirt, sand, forest, jungle or snow, within 40 of a
town, road or moongate, outside S14's closure boxes, not on a road tile).

How a seam is drawn: the client lays a tile's land between its four corners, so where a tile H stands 20 or more above
its neighbour to the south or east (the faces the camera, looking from the south-east, sees), H's land is stretched down
to that neighbour's Z: a smeared cliff face of grass or dirt texture. OSI has no dressing of its own for this to copy
(cavewall_survey.py, rock_palette.py: its cave walls on the surface stand buried 30 under the land at cave mouths, and
under 1 in 500 of its rocks stand on a cliff). So the pass lays OSI's own tall grey boulders (stock art, 0x1357-0x135C,
45 x 58 to 85 px) on H at the low neighbour's Z: drawn from the foot of the cliff up over the face, one more every 20 Z
for a taller face. Each stays at least CLEAR under H's walking Z (sosgrid's stand: pinned's GetAverageZ, the walk rule),
so no tile's walkability changes: not H's (the piece is under it), not the low tile's (nothing is on it).

    python -P dress.py <code copy> <current trammel.mapops> <SoS base folder> <out trammel.mapops> [--window x1 y1 x2 y2]

Writes the patch with the dressing merged, in mapops.diff's own order (B lines by block, then L, S-, S+ by x, y, rest),
the F count updated, and out/dress.csv (one row per piece). --window limits the pass to a box (for trying it out).
"""
import csv, hashlib, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
REPO = os.path.dirname(NOTES)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "scripts"))
import seamgrid  # noqa: E402
import sosgrid  # noqa: E402
from mapbuild import mapops, uofiles  # noqa: E402

STEP = 20
CLEAR = 2
TALL = [0x1358, 0x135A]                      # 81 and 85 px: the foot of every face
MORE = [0x1358, 0x135A, 0x135B, 0x135C, 0x1357]   # 58 to 85 px: each 20 Z above
HEIGHT = 5                                   # tiledata height of every piece above
LOWS = ((0, 1), (1, 0), (1, 1))              # south, east, south-east: the faces the camera sees


def pick(ids, x, y, k):
    h = hashlib.sha256(b"%d,%d,%d" % (x, y, k)).digest()
    return ids[h[0] % len(ids)]


def pieces(g, stand, window=None):
    zs = g["zs"].astype(np.int32)
    xs, ys = np.nonzero(g["target"])
    out = []
    W, H = zs.shape
    for x, y in zip(xs.tolist(), ys.tolist()):
        if window and not (window[0] <= x <= window[2] and window[1] <= y <= window[3]):
            continue
        zh = int(zs[x, y])
        lows = [int(zs[x + dx, y + dy]) for dx, dy in LOWS if x + dx < W and y + dy < H and zh - zs[x + dx, y + dy] >= STEP]
        if not lows:
            continue
        zl = min(lows)
        top = int(stand[x, y]) if stand[x, y] != sosgrid.NONE else zh   # H's walking Z (or its land, if unwalkable)
        k = 0
        while zl + STEP * k + HEIGHT <= top - CLEAR and zl + STEP * k <= 127:
            out.append((x, y, zl + STEP * k, pick(TALL if k == 0 else MORE, x, y, k), zh - zl))
            k += 1
    return out


def merge(text, adds, base):
    """The patch text with S+ lines for adds and B lines for the blocks they touch, as mapops.diff orders them."""
    mf = uofiles.MapFile(base, 1)
    idx, sta = mapops._read(base, 1)
    bh = mf.bh
    bl, lines = {}, []
    for ln in text.splitlines():
        if not ln or ln.startswith("#") or ln.startswith("F "):
            continue
        p = ln.split()
        if p[0] == "B":
            bl[int(p[1])] = p[2]
        else:
            lines.append((p[0],) + tuple(int(v) for v in p[1:]))
    for x, y, z, tid in adds:
        b = (x >> 3) * bh + (y >> 3)
        if b not in bl:
            ob = mf.block_offset(b)
            bl[b] = mapops.fingerprint(mf.data[ob + 4:ob + mapops.BLOCK_BYTES], mapops._block_rows(idx, sta, b))
        lines.append(("S+", x, y, z, tid, 0))
    order = {"L": 0, "S-": 1, "S+": 2}
    lines.sort(key=lambda l: (order[l[0]], l[1], l[2], l[3:]))
    out = ["# Shattered Legacy map patch, facet 1. Ours only: every line is a change we made (scripts/mapbuild/mapops.py).",
           "# L x y tile z  |  S+ x y z id hue (add)  |  S- x y z id hue (remove one EA static)  |  B block fingerprint",
           "F 1 %d" % len(bl)]
    out += ["B %d %s" % (b, bl[b]) for b in sorted(bl)]
    out += [" ".join(str(v) for v in l) for l in lines]
    return "\n".join(out) + "\n"


def main():
    code, cur, base, dst = sys.argv[1:5]
    window = tuple(int(v) for v in sys.argv[sys.argv.index("--window") + 1:][:4]) if "--window" in sys.argv else None
    g = seamgrid.build(code)
    stand = sosgrid.load()["stand"]
    ps = pieces(g, stand, window)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "dress.csv" if not window else "dress-window.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "z", "id", "faceZ"])
        w.writerows([(x, y, z, "0x%04X" % t, fz) for x, y, z, t, fz in ps])
    text = open(cur, encoding="ascii").read()
    new = merge(text, [(x, y, z, t) for x, y, z, t, _ in ps], base)
    open(dst, "w", encoding="ascii", newline="\n").write(new)
    print("seam tiles", int(g["target"].sum()), "faces dressed", len({(p[0], p[1]) for p in ps}), "pieces", len(ps))
    print("patch", len(text.encode()), "->", len(new.encode()), "bytes")


if __name__ == "__main__":
    main()
