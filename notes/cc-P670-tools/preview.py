r"""cc-P670: a patch of the real map drawn as the classic client lays it out (scripts\mapbuild\isorender.py), three ways:
stock art, every redrawn PNG, and only the PNGs fit.py passed. The client's anchor rule is isorender's, so a redraw
that stands off its tile shows here as it would in game.

    python -P preview.py <name> <facet> x1 y1 x2 y2 [<png folder>]   -> out\preview-<name>.jpg
facet 1 Trammel; reads the vanilla client (MAPBUILD_CLIENT) and art (MAPBUILD_ART).
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


class Redrawn(isorender.Art):
    """Stock art, except the IDs given, which come from their PNG."""

    def __init__(self, pngs):
        super().__init__()
        self.pngs = pngs

    def static(self, tid):
        p = self.pngs.get(tid)
        if p is None:
            return super().static(tid)
        key = ("r", tid)
        if key not in self.cache:
            a = np.array(Image.open(p).convert("RGBA"))
            a[a[:, :, 3] < 16] = 0
            self.cache[key] = Image.fromarray(a, "RGBA")
        return self.cache[key]


def main():
    name, facet = sys.argv[1], int(sys.argv[2])
    x1, y1, x2, y2 = (int(v) for v in sys.argv[3:7])
    folder = sys.argv[7] if len(sys.argv) > 7 else fit.VENDOR
    pngs = {int(f[:-4]): os.path.join(folder, f) for f in os.listdir(folder) if re.fullmatch(r"\d+\.png", f)}
    ok = {int(r["id"]) for r in csv.DictReader(open(os.path.join(fit.OUT, "fit.csv"))) if r["verdict"] == "ok"}
    scene = isorender.Scene.from_map(isorender.CLIENT, facet, x1, y1, x2, y2)
    used = {s[3] for s in scene.statics} if hasattr(scene, "statics") else set()
    pics = []
    for title, art in (("stock", isorender.Art()), ("every redraw", Redrawn(pngs)), ("only those that fit", Redrawn({k: v for k, v in pngs.items() if k in ok}))):
        im = isorender.render(scene, x1, y1, x2, y2, art=art).convert("RGB")
        w = 720
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        ImageDraw.Draw(im).text((6, 4), title, fill=(255, 255, 0))
        pics.append(im)
    sheet = Image.new("RGB", (sum(p.width for p in pics) + 16, max(p.height for p in pics) + 20), (16, 16, 16))
    x = 0
    for p in pics:
        sheet.paste(p, (x, 20))
        x += p.width + 8
    hit = len([t for t in used if t in pngs])
    ImageDraw.Draw(sheet).text((6, 4), "%s  facet %d  %d,%d-%d,%d  (statics here with a redraw: %d ids)" % (name, facet, x1, y1, x2, y2, hit), fill=(255, 255, 255))
    out = os.path.join(fit.OUT, "preview-%s.jpg" % name)
    sheet.save(out, quality=85)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
