r"""cc-P673: where the Wakening Isle can go on the Siege of Sosaria Trammel map.

The isle's drawn area (P481 section 11.2) is 272 x 145 tiles, west to east, with its 24-tile sea margin inside it.
A site is a top-left corner where that box, plus a buffer of b tiles all round, holds only empty void (void land
0x0244 / 0x0002 with no static, P481's kind 2). The buffer keeps the author's caves out of sight of our sea, and our
sea out of sight of his players on Trammel and Felucca (both read this file after the swap). Open sea is scanned the
same way for comparison (kind 1, no static); a sea site is reachable by boat, so it is listed, not recommended.

Read only, from P481's copies in notes\cc-P481-tools\scratch\sos\. Nothing is written to any map file.
    python -P sitefind.py -> out\sites.csv, out\sites.json, ..\art\sos-isle-site\*.png
"""
import csv
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
import islands  # noqa: E402

OUT = os.path.join(HERE, "out")
ART = os.path.join(NOTES, "art", "sos-isle-site")
os.makedirs(OUT, exist_ok=True)
os.makedirs(ART, exist_ok=True)

W, H = 7168, 4096
BW, BH = 272, 145            # the isle's drawn area, P481 11.2 (x 6170-6441, y 1913-2057)
OLD = (6170, 1913)           # its old top-left in void C
WALK = (32, 25, 239, 113)    # walkable land and dock inside the box (x 6202-6409, y 1938-2026), relative
BUFFERS = (0, 16, 24, 32, 48, 64, 96, 128)
STEP = 4


def integral(bad):
    s = np.zeros((W + 1, H + 1), dtype=np.int64)
    s[1:, 1:] = bad.astype(np.int64).cumsum(0).cumsum(1)
    return s


def box_sum(s, x1, y1, x2, y2):
    """Sum of bad tiles in [x1, x2] x [y1, y2], clipped to the map (off-map counts as empty)."""
    x1, y1 = np.maximum(x1, 0), np.maximum(y1, 0)
    x2, y2 = np.minimum(x2, W - 1), np.minimum(y2, H - 1)
    return s[x2 + 1, y2 + 1] - s[x1, y2 + 1] - s[x2 + 1, y1] + s[x1, y1]


def feasible(s, b):
    xs = np.arange(0, W - BW + 1, STEP)
    ys = np.arange(0, H - BH + 1, STEP)
    gx, gy = np.meshgrid(xs, ys, indexing="ij")
    ok = box_sum(s, gx - b, gy - b, gx + BW - 1 + b, gy + BH - 1 + b) == 0
    return xs, ys, ok


def components(ok):
    lab = np.zeros(ok.shape, dtype=np.int32)
    n = 0
    for i, j in zip(*np.nonzero(ok)):
        if lab[i, j]:
            continue
        n += 1
        st = [(i, j)]
        lab[i, j] = n
        while st:
            a, c = st.pop()
            for da, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p, q = a + da, c + dc
                if 0 <= p < ok.shape[0] and 0 <= q < ok.shape[1] and ok[p, q] and not lab[p, q]:
                    lab[p, q] = n
                    st.append((p, q))
    return lab, n


def nearest(bad_xy, x1, y1, x2, y2):
    """Chebyshev distance from the box to the nearest bad tile, and that tile."""
    bx, by = bad_xy
    dx = np.maximum(np.maximum(x1 - bx, bx - x2), 0)
    dy = np.maximum(np.maximum(y1 - by, by - y2), 0)
    d = np.maximum(dx, dy)
    k = int(np.argmin(d))
    return int(d[k]), (int(bx[k]), int(by[k]))


def main():
    colour, kind, count, _, _, _ = islands.build("sos")
    spots = []
    with open(os.path.join(NOTES, "cc-P669-tools", "out", "spots.csv"), newline="") as f:
        for r in csv.DictReader(f):
            spots.append((r["group"], r["name"], int(r["x"]), int(r["y"])))
    rows, picks = [], []
    for what, empty in (("void", kind == 2), ("sea", (kind == 1) & (count == 0))):
        s = integral(~empty)
        bad = np.nonzero(~empty[5120:, :] if what == "void" else ~empty)
        bad_xy = (bad[0] + (5120 if what == "void" else 0), bad[1])
        if what == "sea":
            # Only tiles near sea matter for the distance; subsample land far inland to keep it quick.
            keep = np.arange(len(bad_xy[0])) % 7 == 0
            bad_xy = (bad_xy[0][keep], bad_xy[1][keep])
        counts = {}
        for b in BUFFERS:
            xs, ys, ok = feasible(s, b)
            counts[b] = int(ok.sum())
        print(what, "corners feasible by buffer:", counts)
        # Clusters at buffer 24 (the isle's own view margin again, outside the box).
        xs, ys, ok = feasible(s, 24)
        lab, n = components(ok)
        for c in range(1, n + 1):
            ii, jj = np.nonzero(lab == c)
            # The corner in this cluster with the largest buffer, ties to the cluster's middle.
            best = None
            for b in BUFFERS[::-1]:
                _, _, okb = feasible(s, b)
                sel = okb[ii, jj]
                if sel.any():
                    ci, cj = ii[sel], jj[sel]
                    mi, mj = np.median(ci), np.median(cj)
                    k = int(np.argmin((ci - mi) ** 2 + (cj - mj) ** 2))
                    best = (b, int(xs[ci[k]]), int(ys[cj[k]]))
                    break
            b, x, y = best
            d, at = nearest(bad_xy, x, y, x + BW - 1, y + BH - 1)
            sd = min(((max(abs(sx - (x + BW // 2)) - BW // 2, abs(sy - (y + BH // 2)) - BH // 2, 0), g, nm, sx, sy)
                      for g, nm, sx, sy in spots), key=lambda t: t[0])
            area = (int(xs[ii.min()]), int(ys[jj.min()]), int(xs[ii.max()]) + BW - 1, int(ys[jj.max()]) + BH - 1)
            row = dict(kind=what, cluster=c, corners=int(len(ii)), x1=x, y1=y, x2=x + BW - 1, y2=y + BH - 1,
                       buffer=b, clear_to=d, nearest_content=at, nearest_spot=sd[2], nearest_spot_group=sd[1],
                       nearest_spot_at=(sd[3], sd[4]), nearest_spot_dist=int(sd[0]), room=area,
                       shift=(x - OLD[0], y - OLD[1]))
            rows.append(row)
    rows.sort(key=lambda r: (r["kind"] != "void", -r["clear_to"]))
    with open(os.path.join(OUT, "sites.csv"), "w", newline="") as f:
        w = csv.writer(f)
        keys = list(rows[0].keys())
        w.writerow(keys)
        for r in rows:
            w.writerow([r[k] for k in keys])
    json.dump(rows, open(os.path.join(OUT, "sites.json"), "w"), indent=1)
    for r in rows:
        print(r)
    draw(colour, kind, rows)


def draw(colour, kind, rows):
    img = colour.copy()
    img[kind == 2] = (0, 0, 0)
    # Overview of the dungeon strip, 2 tiles a pixel.
    x0 = 5120
    strip = img[x0:, :].transpose(1, 0, 2)[::2, ::2]
    im = Image.fromarray(np.ascontiguousarray(strip))
    d = ImageDraw.Draw(im)
    d.rectangle([(OLD[0] - x0) // 2, OLD[1] // 2, (OLD[0] + BW - 1 - x0) // 2, (OLD[1] + BH - 1) // 2], outline=(255, 60, 60), width=2)
    d.text(((OLD[0] - x0) // 2 + 2, OLD[1] // 2 - 12), "old site (void C, now a cave)", fill=(255, 90, 90))
    tag = "ABCDEFGHIJ"
    vs = [r for r in rows if r["kind"] == "void"]
    for i, r in enumerate(vs):
        r["tag"] = tag[i]
        rx1, ry1, rx2, ry2 = r["room"]
        d.rectangle([(rx1 - x0) // 2, ry1 // 2, (rx2 - x0) // 2, ry2 // 2], outline=(90, 90, 255), width=1)
        d.rectangle([(r["x1"] - x0) // 2, r["y1"] // 2, (r["x2"] - x0) // 2, r["y2"] // 2], outline=(255, 230, 0), width=2)
        d.text(((r["x1"] - x0) // 2 + 4, r["y1"] // 2 + 4), "%s (%d,%d)" % (tag[i], r["x1"], r["y1"]), fill=(255, 230, 0))
    d.rectangle([0, 0, im.width, 16], fill=(0, 0, 0))
    d.text((4, 2), "SoS Trammel x 5120-7167, 2 tiles/px. Yellow: isle box (272x145) per site; blue: room it can slide in; black: empty void", fill=(255, 255, 255))
    im.save(os.path.join(ART, "overview-dungeon-strip.png"))
    # Each void site at 1 tile a pixel, with the plan's walkable box and 64 tiles round it.
    for r in vs:
        pad = 64
        x1, y1 = max(r["x1"] - pad, 0), max(r["y1"] - pad, 0)
        x2, y2 = min(r["x2"] + pad, W - 1), min(r["y2"] + pad, H - 1)
        sub = img[x1:x2 + 1, y1:y2 + 1].transpose(1, 0, 2)
        im = Image.fromarray(np.ascontiguousarray(sub)).resize(((x2 - x1 + 1) * 2, (y2 - y1 + 1) * 2), Image.NEAREST)
        d = ImageDraw.Draw(im)
        ox, oy = (r["x1"] - x1) * 2, (r["y1"] - y1) * 2
        d.rectangle([ox, oy, ox + BW * 2 - 1, oy + BH * 2 - 1], outline=(255, 230, 0), width=2)
        d.rectangle([ox + WALK[0] * 2, oy + WALK[1] * 2, ox + WALK[2] * 2, oy + WALK[3] * 2], outline=(80, 220, 80), width=2)
        d.rectangle([0, 0, im.width, 16], fill=(0, 0, 0))
        d.text((4, 2), "Site %s: box x %d-%d, y %d-%d (yellow; green = walkable land); clear %d tiles to the nearest content at %s"
               % (r["tag"], r["x1"], r["x2"], r["y1"], r["y2"], r["clear_to"], r["nearest_content"]), fill=(255, 255, 255))
        im.save(os.path.join(ART, "site-%s.png" % r["tag"]))
    json.dump(rows, open(os.path.join(OUT, "sites.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
