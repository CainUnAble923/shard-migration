r"""cc-P670: contact sheets of redrawn statics beside stock, both drawn on the same tile anchor as the client does
(image centre over the tile's centre, image bottom on the tile's bottom corner), with the tile's diamond outlined in red.
    python -P sheet.py <verdict> [<png folder>] [per sheet] -> out\sheet-<verdict>-<n>.jpg
"""
import csv
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))
from mapbuild import isorender  # noqa: E402
import fit  # noqa: E402

CELL_W, CELL_H = 200, 230


def anchored(im, cw, ch):
    """Place im in a cw x ch cell as the client would on a tile whose diamond's bottom corner is at (cw/2, ch-10)."""
    cell = Image.new("RGBA", (cw, ch), (40, 40, 40, 255))
    d = ImageDraw.Draw(cell)
    bx, by = cw // 2, ch - 10
    d.polygon([(bx, by), (bx + 22, by - 22), (bx, by - 44), (bx - 22, by - 22)], outline=(220, 40, 40))
    if im is not None:
        x = bx - 22 + 22 - (im.width >> 1)   # tile x - (w >> 1) + 22, with the tile's left corner at bx - 22
        y = by - im.height
        cell.alpha_composite(im, (max(-im.width, x), max(-im.height, y)))
    return cell


def main():
    verdict = sys.argv[1]
    folder = sys.argv[2] if len(sys.argv) > 2 else fit.VENDOR
    per = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    art = isorender.Art()
    rows = [r for r in csv.DictReader(open(os.path.join(fit.OUT, "fit.csv"))) if r["verdict"] == verdict]
    cols = 6
    for n in range(0, len(rows), per):
        chunk = rows[n:n + per]
        nrows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (CELL_W * 2 + 12), nrows * (CELL_H + 16)), (16, 16, 16))
        d = ImageDraw.Draw(sheet)
        for i, r in enumerate(chunk):
            tid = int(r["id"])
            s = art.static(tid)
            p = Image.open(os.path.join(folder, "%d.png" % tid)).convert("RGBA")
            a = np.array(p)
            a[a[:, :, 3] < 16] = 0
            p = Image.fromarray(a, "RGBA")
            x0, y0 = (i % cols) * (CELL_W * 2 + 12), (i // cols) * (CELL_H + 16)
            sheet.paste(anchored(s.convert("RGBA") if s else None, CELL_W, CELL_H).convert("RGB"), (x0, y0 + 14))
            sheet.paste(anchored(p, CELL_W, CELL_H).convert("RGB"), (x0 + CELL_W, y0 + 14))
            d.text((x0 + 2, y0), "%d %s  dB %s dC %s" % (tid, (r["name"] or "")[:16], r["dBottom"], r["dCentre"]), fill=(255, 230, 120))
        out = os.path.join(fit.OUT, "sheet-%s-%d.jpg" % (verdict.replace(" ", "-"), n // per + 1))
        sheet.save(out, quality=80)
        print(out, sheet.size)


if __name__ == "__main__":
    main()
