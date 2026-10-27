r"""cc-P673: check the two best void sites with a block-aligned shift (a multiple of 8, so every static keeps its
place inside its 8 x 8 block and P481's plan moves by plain addition).

For each: the box and a buffer hold only empty void on the SoS file; how far the nearest content is; which stock,
ServUO or our own points (P669's geo-points.csv, every category) fall in the box or near it; the Fold's later zones
(P481 3.2: vision chamber, League spaces, events, custom dungeons) and whether they still fit beside the isle.
    python -P sitecheck.py -> out\sitecheck.json, ..\art\sos-isle-site\pick-*.png
"""
import csv
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(NOTES, "cc-P481-tools"))
import islands  # noqa: E402
import sitefind as sf  # noqa: E402

PICKS = {
    # tag: shift from the old box (6170, 1913)
    "A": (424, 1992),   # the south strip, middle of its room
    "C": (704, 0),      # east of void C, same rows: every P481 y stays as it is
}
NEAR = 64


def main():
    colour, kind, count, _, _, _ = islands.build("sos")
    empty = kind == 2
    s = sf.integral(~empty)
    pts = []
    with open(os.path.join(NOTES, "cc-P669-tools", "out", "geo-points.csv"), newline="") as f:
        for r in csv.DictReader(f):
            pts.append((r["category"], r["source"], r["name"], int(r["x"]), int(r["y"])))
    res = {}
    for tag, (dx, dy) in PICKS.items():
        x1, y1 = sf.OLD[0] + dx, sf.OLD[1] + dy
        x2, y2 = x1 + sf.BW - 1, y1 + sf.BH - 1
        clear = 0
        for b in range(0, 400):
            if sf.box_sum(s, x1 - b, y1 - b, x2 + b, y2 + b) != 0:
                break
            clear = b
        # Room: grow each side alone while it stays empty.
        room = []
        for side in range(4):
            n = 0
            while True:
                bx = [x1, y1, x2, y2]
                bx[side] += (-1 if side < 2 else 1) * (n + 1)
                if bx[0] < 0 or bx[1] < 0 or bx[2] >= sf.W or bx[3] >= sf.H or sf.box_sum(s, *bx) != 0:
                    break
                n += 1
            room.append(n)
        inside = [p for p in pts if x1 - NEAR <= p[3] <= x2 + NEAR and y1 - NEAR <= p[4] <= y2 + NEAR]
        walk = (x1 + sf.WALK[0], y1 + sf.WALK[1], x1 + sf.WALK[2], y1 + sf.WALK[3])
        res[tag] = dict(shift=(dx, dy), box=(x1, y1, x2, y2), walkable=walk, beach=(6214 + dx, 2001 + dy),
                        dock=(6407 + dx, 1999 + dy), clear_all_round=clear,
                        free_tiles_west_north_east_south=room,
                        points_within_64=[list(p) for p in inside], block_aligned=(dx % 8 == 0 and dy % 8 == 0),
                        stock_trammel_also_void=None)
    # Stock Trammel at the same boxes, for the record (if the swap ever slipped, would the site still work?).
    _, kt, ct, _, _, _ = islands.build("trammel")
    st = sf.integral(~(kt == 2))
    for tag, r in res.items():
        r["stock_trammel_also_void"] = bool(sf.box_sum(st, *r["box"]) == 0)
    json.dump(res, open(os.path.join(sf.OUT, "sitecheck.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))
    img = colour.copy()
    img[kind == 2] = (0, 0, 0)
    for tag, r in res.items():
        x1, y1, x2, y2 = r["box"]
        pad = 200
        a, b = max(x1 - pad, 0), max(y1 - pad, 0)
        c, d = min(x2 + pad, sf.W - 1), min(y2 + pad, sf.H - 1)
        im = Image.fromarray(np.ascontiguousarray(img[a:c + 1, b:d + 1].transpose(1, 0, 2)))
        dr = ImageDraw.Draw(im)
        dr.rectangle([x1 - a, y1 - b, x2 - a, y2 - b], outline=(255, 230, 0), width=2)
        w = r["walkable"]
        dr.rectangle([w[0] - a, w[1] - b, w[2] - a, w[3] - b], outline=(80, 220, 80), width=1)
        for p in r["points_within_64"]:
            dr.ellipse([p[3] - a - 2, p[4] - b - 2, p[3] - a + 2, p[4] - b + 2], fill=(255, 60, 60))
        dr.rectangle([0, 0, im.width, 30], fill=(0, 0, 0))
        dr.text((4, 2), "Pick %s: isle box x %d-%d, y %d-%d (yellow), walkable land (green); shift (%+d, %+d) from void C"
                % (tag, x1, x2, y1, y2, r["shift"][0], r["shift"][1]), fill=(255, 255, 255))
        dr.text((4, 16), "SoS Trammel, 1 tile a pixel, 200 tiles round; black = empty void; empty all round for %d tiles"
                % r["clear_all_round"], fill=(255, 255, 255))
        im.save(os.path.join(sf.ART, "pick-%s.png" % tag))


if __name__ == "__main__":
    main()
