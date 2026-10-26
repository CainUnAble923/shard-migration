r"""cc-P669: client-style renders of the notable places, stock Trammel beside Siege of Sosaria 3.0.

Read only; stock art (all 8,683 SoS item ids and its land ids have stock 7.0.117 art, measured). Uses
scripts\mapbuild\isorender.py (the classic client's layout) through P481's readers; maps loaded once.
    MAPBUILD_CLIENT=D:/UO/UltimaOnlineVanilla MAPBUILD_ART=D:/UO/cc-p167-work/scratch-client python -P render.py
    -> notes\art\sos-survey\<n>-<slug>.jpg (stock left, SoS right) and top-<slug>.png (radar colours, both)
"""
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cc-P481-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))
import islands  # noqa: E402
import sosdiff  # noqa: E402
from mapbuild import isorender  # noqa: E402

# name, centre x, y, half size (tiles)
ISO = [
    ("New Haven plaza (our tutorial start)", 3500, 2585, 22),
    ("Old Haven, our Rootdeep way in (3608,2616)", 3625, 2620, 22),
    ("Haven town centre in SoS (Uzeraan's Mansion)", 3640, 2600, 24),
    ("Britain moongate", 1336, 1997, 14),
    ("Moonglow moongate", 4467, 1283, 14),
    ("Valunstead, walled town and moated keep", 479, 388, 26),
    ("Fort Whitestone", 890, 1055, 22),
    ("Castle Dunbain", 1333, 1377, 22),
    ("Fort Stormhammer", 1490, 1323, 22),
    ("Hammerhill", 1530, 1010, 26),
    ("Kameron Kove", 1310, 2465, 24),
    ("Tigerclaw Fortress", 2595, 1085, 22),
    ("Khalahandra Keep entrance", 2505, 1707, 20),
    ("Pyramid, Compassion Desert", 2104, 611, 22),
    ("Nujelm Desert, south", 3813, 1277, 22),
    ("Skypoint Islands, ship", 4357, 2349, 20),
    ("Glimmerwood west", 2123, 3330, 22),
    ("Dragonstorm Island moongate", 3186, 3884, 20),
    ("Isle of the Avatar, south", 4764, 3819, 22),
    ("New Magincia", 3700, 2160, 26),
    ("Fold void C in SoS (the isle's beach 6214,2001)", 6230, 2000, 26),
    ("Blackthorn dungeon area in SoS (Hammerhill Sewers level 1)", 6394, 2771, 22),
]
TOP = [
    ("Nujelm Desert, the new landmass", 3500, 1000, 5100, 2150, 3),
    ("Fold void C (x 6160-6639, y 1832-2279)", 6140, 1812, 6660, 2300, 1),
    ("The Haven peninsula: New Haven, Old Haven, Rootdeep's way in", 3380, 2440, 3760, 2720, 1),
    ("Britannia mainland west, Britain to Yew", 300, 300, 2000, 2400, 4),
]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]


class Maps:
    def __init__(self):
        self.d = {}
        for n in ("trammel", "sos"):
            ids, zs = islands.load_land(n)
            sx, sy, sz, sid = islands.load_statics(n)
            self.d[n] = (ids, zs, sx, sy, sz, sid)

    def scene(self, n, x1, y1, x2, y2, pad=1):
        ids, zs, sx, sy, sz, sid = self.d[n]
        land = {(x, y): (int(ids[x, y]), int(zs[x, y])) for x in range(x1 - pad, x2 + pad + 1) for y in range(y1 - pad, y2 + pad + 1)}
        m = (sx >= x1) & (sx <= x2) & (sy >= y1) & (sy <= y2)
        return isorender.Scene(land, list(zip(sx[m].tolist(), sy[m].tolist(), sz[m].tolist(), sid[m].tolist())))


def label(im, text):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, im.width, 18], fill=(0, 0, 0))
    d.text((6, 3), text, fill=(255, 255, 255))
    return im


def main():
    out = sosdiff.ART
    maps = Maps()
    for i, (name, cx, cy, r) in enumerate(ISO, 1):
        x1, y1, x2, y2 = cx - r, cy - r, cx + r, cy + r
        pics = []
        for n, title in (("trammel", "stock Trammel"), ("sos", "Siege of Sosaria 3.0")):
            im = isorender.render(maps.scene(n, x1, y1, x2, y2), x1, y1, x2, y2).convert("RGB")
            w = 760
            im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
            pics.append(label(im, "%s  %d,%d-%d,%d" % (title, x1, y1, x2, y2)))
        h = max(p.height for p in pics)
        sheet = Image.new("RGB", (pics[0].width + pics[1].width + 8, h + 24), (20, 20, 20))
        sheet.paste(pics[0], (0, 24))
        sheet.paste(pics[1], (pics[0].width + 8, 24))
        ImageDraw.Draw(sheet).text((6, 5), "%d. %s (centre %d,%d)" % (i, name, cx, cy), fill=(255, 230, 120))
        p = os.path.join(out, "%02d-%s.jpg" % (i, slug(name)))
        sheet.save(p, quality=82, optimize=True)
        print(p, sheet.size, os.path.getsize(p), flush=True)
    for name, x1, y1, x2, y2, step in TOP:
        pics = []
        for n, title in (("trammel", "stock"), ("sos", "SoS 3.0")):
            col, _, _, _, _, _ = islands.build(n)
            sub = col[x1:x2:step, y1:y2:step].transpose(1, 0, 2).copy()
            pics.append(label(Image.fromarray(sub), "%s  %d,%d-%d,%d  1 px = %d tile(s)" % (title, x1, y1, x2, y2, step)))
        sheet = Image.new("RGB", (pics[0].width * 2 + 8, pics[0].height), (20, 20, 20))
        sheet.paste(pics[0], (0, 0))
        sheet.paste(pics[1], (pics[0].width + 8, 0))
        p = os.path.join(out, "top-%s.png" % slug(name))
        sheet.save(p, optimize=True)
        print(p, sheet.size, os.path.getsize(p), flush=True)


if __name__ == "__main__":
    main()
