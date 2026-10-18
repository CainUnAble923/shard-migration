"""cc-P147: the placeholder Achievements paperdoll button (normal, pressed, hover) from the Help button's frame.

The frame and the dark field are the shipped Help button's (Fiddle-Me-This 2031 to 2033, as the client shows it), the
label is drawn in a plain narrow face, and the label colours are sampled from the Help button's own states. Writes
22456.png (normal), 22457.png (pressed), 22458.png (hover) to the folder given."""
import os
import sys
from collections import Counter

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdlib  # noqa: E402

OUT = sys.argv[1]
LABEL = "Achievements"
FONT = os.environ.get("P147_FONT", r"C:/Windows/Fonts/ARIALNB.TTF")


def field_box(im):
    """The dark field inside the frame: rows and columns whose pixels are mostly dark."""
    w, h = im.size
    px = im.load()
    dark = lambda p: p[3] and sum(p[:3]) < 160  # noqa: E731
    rows = [y for y in range(h) if sum(dark(px[x, y]) for x in range(w)) > w * 0.6]
    cols = [x for x in range(w) if sum(dark(px[x, y]) for y in range(h)) > h * 0.5]
    return min(cols), min(rows), max(cols), max(rows)


def text_colour(im, box):
    """The commonest bright colour inside the field: the label's."""
    x0, y0, x1, y1 = box
    px = im.load()
    c = Counter(px[x, y][:3] for x in range(x0, x1 + 1) for y in range(y0, y1 + 1) if sum(px[x, y][:3]) > 300)
    return c.most_common(1)[0][0]


def blank(im, box):
    """The field with its label removed: every bright pixel takes the dark pixel to its left."""
    out = im.copy()
    x0, y0, x1, y1 = box
    px = out.load()
    for y in range(y0 + 1, y1 + 1):
        for x in range(x0 + 1, x1):
            px[x, y] = px[x0 + 1 + (x - x0) % 3, y]
    return out


def best_font(width, height):
    for size in range(14, 6, -1):
        f = ImageFont.truetype(FONT, size)
        l, t, r, b = f.getbbox(LABEL)
        if r - l <= width and b - t <= height:
            return f
    return ImageFont.truetype(FONT, 7)


def make(base_id, shift):
    im, _ = pdlib.gump(base_id)
    box = field_box(im)
    colour = text_colour(im, box)
    out = blank(im, box)
    x0, y0, x1, y1 = box
    font = best_font(x1 - x0 - 4, y1 - y0 - 2)
    l, t, r, b = font.getbbox(LABEL)
    tx = x0 + (x1 - x0 - (r - l)) // 2 - l + shift
    ty = y0 + (y1 - y0 - (b - t)) // 2 - t + shift
    d = ImageDraw.Draw(out)
    d.text((tx + 1, ty + 1), LABEL, font=font, fill=(0, 0, 0, 255))
    d.text((tx, ty), LABEL, font=font, fill=colour + (255,))
    return out, box, colour, font.size


os.makedirs(OUT, exist_ok=True)
for gid, base, shift in ((22456, 2031, 0), (22457, 2032, 1), (22458, 2033, 0)):
    im, box, colour, size = make(base, shift)
    im.save(os.path.join(OUT, "%d.png" % gid), optimize=True)
    print(gid, "from", base, im.size, "field", box, "label", colour, "size", size)
