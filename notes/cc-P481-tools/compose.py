r"""cc-P481: the island candidates side by side for Chase (island-candidates\candidates.png), and where each sits
(island-candidates\where-trammel.png, where-sos.png). Built from islands.py's and iso.py's scratch renders.
    python -P compose.py
"""
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, "scratch")
OUT = os.path.join(HERE, "island-candidates")
os.makedirs(OUT, exist_ok=True)

import sys
sys.path.insert(0, HERE)  # -P leaves the script folder off the path
import islands  # noqa: E402

CARDS = [
    ("1. Isle of Colossus (Siege of Sosaria map, #51)", "248 x 196, woods, ponds, rocky hills; copied into void C",
     "cand-sos51.png", "iso-sos51.png"),
    ("2. Forest isle SE of Britain (Trammel #16)", "204 x 152, forest and grass, sandy cove; used as it is",
     "cand-tram16.png", "iso-tram16.png"),
    ("3. A new island painted in void C (P481 plan)", "about 200 x 90 on the diagonal; all new map work",
     "../fold-isle.png", "../fold-isle-iso.png"),
]
W = 460


def fit(path, w, h):
    im = Image.open(os.path.join(S, path)).convert("RGB")
    im.thumbnail((w, h), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), (12, 12, 16))
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return canvas


def main():
    f, small = islands.font(20), islands.font(15)
    sheet = Image.new("RGB", (W * len(CARDS) + 20 * (len(CARDS) + 1), 60 + 360 + 20 + 400 + 30), (24, 24, 30))
    d = ImageDraw.Draw(sheet)
    for i, (title, sub, top, iso) in enumerate(CARDS):
        x = 20 + i * (W + 20)
        d.text((x, 10), title, fill=(240, 220, 160), font=f)
        d.text((x, 36), sub, fill=(200, 200, 200), font=small)
        sheet.paste(fit(top, W, 360), (x, 60))
        sheet.paste(fit(iso, W, 400), (x, 440))
    d.text((20, sheet.height - 24), "Top row: from above (radar colours). Bottom row: a patch as the classic client lays it out "
           "(stock art, no hues). Numbers match notes section 10.", fill=(170, 170, 170), font=small)
    sheet.save(os.path.join(OUT, "candidates.png"), optimize=True)
    for name, src, box in (("where-trammel.png", "trammel-overview.png", None), ("where-sos.png", "sos-overview.png", None)):
        im = Image.open(os.path.join(S, src)).convert("RGB")
        im.thumbnail((1200, 1200), Image.LANCZOS)
        im.quantize(colors=128).save(os.path.join(OUT, name), optimize=True)
    for n in os.listdir(OUT):
        print(n, os.path.getsize(os.path.join(OUT, n)))


main()
