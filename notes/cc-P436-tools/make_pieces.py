"""cc-P436 step 2: write look B's nine frame pieces as our gumps 23200-23208.

The cut is previews.py's basalt_frame(), the one Chase picked from (10-25): Erachiro's Basalt status gump, its braided
bronze border (corner, top and left edges; the others mirrored) and plain basalt for the inside. AddBackground draws
id+0 to id+8 as top-left, top, top-right, left, centre, right, bottom-left, bottom, bottom-right, the order
basalt_frame() returns. Fully opaque RGBA PNGs (TazUO's ExternalImageLoader keeps PNG alpha and keys no colour).
    python -P make_pieces.py            writes the PNGs into the player package's art folder
    python -P make_pieces.py --check    only compares what is there with a fresh cut
"""
import hashlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -P leaves the script's folder off the path
import previews  # noqa: E402

FIRST = 23200
OUT = r"D:\UO\golems\Iron\ShatteredLegacy\player-package\vendor\shattered-legacy-art\gumps"
NAMES = ["top-left corner", "top edge", "top-right corner", "left edge", "centre", "right edge",
         "bottom-left corner", "bottom edge", "bottom-right corner"]


def png_bytes(img):
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def main():
    check = "--check" in sys.argv
    pieces, _ = previews.basalt_frame()
    assert len(pieces) == 9
    bad = 0
    for i, img in enumerate(pieces):
        img = img.convert("RGBA")
        assert all(a == 255 for a in img.getchannel("A").getdata()), "piece %d is not opaque" % i
        data = png_bytes(img)
        path = os.path.join(OUT, "%d.png" % (FIRST + i))
        if check:
            same = os.path.exists(path) and open(path, "rb").read() == data
            bad += not same
            print("%d %-20s %dx%d %s" % (FIRST + i, NAMES[i], img.width, img.height, "ok" if same else "DIFFERS"))
        else:
            open(path, "wb").write(data)
            print("%d %-20s %dx%d sha1 %s" % (FIRST + i, NAMES[i], img.width, img.height,
                                              hashlib.sha1(data).hexdigest()[:12]))
    sys.exit(1 if bad else 0)


main()
