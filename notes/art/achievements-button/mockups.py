"""cc-P147: the classic paperdoll with an Achievements button, three placements, from the art the package ships.

The background (2000) and the eight stock buttons are what our client shows (Fiddle-Me-This, else EA's), the bodies
are the Siege of Sosaria SFW set (vendor\\paperdoll-sos), placed at TazUO's avatar position (8, 19), and the button
positions are TazUO's PaperDollGump.Settings (x 185, y 44 + 27 n). A mockup, not a client screenshot: no hues, no
equipment, no title text."""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdlib  # noqa: E402

OUT = sys.argv[1]
BTN = sys.argv[2]           # folder with 22456.png
os.makedirs(OUT, exist_ok=True)
ACH = Image.open(os.path.join(BTN, "22456.png")).convert("RGBA")
ACH_HOVER = Image.open(os.path.join(BTN, "22458.png")).convert("RGBA")
STOCK = [("Help", 0x07EF), ("Options", 2006), ("Log Out", 2009), ("Quests", 22453), ("Skills", 2015),
         ("Guild", 22450), ("Peace", 0x07E5), ("Status", 2027)]
FONT = ImageFont.truetype(r"C:/Windows/Fonts/segoeui.ttf", 13)


def base(body):
    bg, _ = pdlib.gump(2000)
    im = bg.copy()
    b, _ = pdlib.gump(body)
    if b is not None:
        im.alpha_composite(b, (8, 19))
    v, _ = pdlib.gump(0x0071)        # the virtue gem
    if v is not None:
        im.alpha_composite(v, (80, 4))
    return im


def column(im, rows, step=27, top=44):
    for n, item in enumerate(rows):
        g = item if isinstance(item, Image.Image) else pdlib.gump(item)[0]
        if g is not None:
            im.alpha_composite(g, (185, top + step * n))


def small_icon():
    """Option C's stand-in: a 21x21 frame cut from the button art, with a star."""
    frame = ACH.crop((0, 0, 21, 21)).copy()
    frame.paste(ACH.crop((43, 0, 64, 21)).crop((11, 0, 21, 21)), (11, 0))
    d = ImageDraw.Draw(frame)
    d.rectangle((5, 4, 15, 16), fill=(24, 22, 20, 255))
    d.polygon([(10, 5), (12, 9), (16, 9), (13, 12), (14, 16), (10, 13), (6, 16), (7, 12), (4, 9), (8, 9)], fill=(255, 164, 0, 255))
    return frame


def option(key, body):
    im = base(body)
    ids = [g for _, g in STOCK]
    if key == "A":                       # Achievements in Help's place (Help stays in the top bar's More + menu)
        column(im, [ACH] + ids[1:])
    elif key == "B":                     # a ninth button: the column closes up to 24 px a row
        column(im, ids + [ACH], step=24, top=42)
    elif key == "C":                     # a small icon button on the frame, left of the title strip
        column(im, ids)
        im.alpha_composite(small_icon(), (8, 258))
    return im


def label(im, text, scale=2):
    big = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    out = Image.new("RGBA", (big.width + 20, big.height + 44), (24, 24, 24, 255))
    out.alpha_composite(big, (10, 10))
    ImageDraw.Draw(out).text((10, big.height + 16), text, font=FONT, fill=(230, 230, 230, 255))
    return out


TEXT = {"A": "A (built): Achievements replaces Help", "B": "B: a ninth button, rows 24 px apart",
        "C": "C: a small icon button by the title strip"}
sheet = []
for key in "ABC":
    im = label(option(key, 12), TEXT[key])
    im.convert("RGB").save(os.path.join(OUT, "option-%s.png" % key), optimize=True)
    sheet.append(im)
w = sum(i.width for i in sheet)
s = Image.new("RGBA", (w, sheet[0].height), (24, 24, 24, 255))
x = 0
for i in sheet:
    s.alpha_composite(i, (x, 0))
    x += i.width
s.convert("RGB").save(os.path.join(OUT, "options-ABC.png"), optimize=True)

# Option A on every Siege of Sosaria body, and the hover state.
bodies = [(12, "human male"), (13, "human female"), (14, "elf male"), (15, "elf female"), (665, "gargoyle male"),
          (666, "gargoyle female")]
cells = []
for body, name in bodies:
    im = option("A", body)
    cells.append(label(im, name, scale=1))
hover = base(12)
column(hover, [ACH_HOVER] + [g for _, g in STOCK][1:])
cells.append(label(hover, "hover", scale=1))
s = Image.new("RGBA", (sum(c.width for c in cells), cells[0].height), (24, 24, 24, 255))
x = 0
for c in cells:
    s.alpha_composite(c, (x, 0))
    x += c.width
s.convert("RGB").save(os.path.join(OUT, "option-A-every-body.png"), optimize=True)
print("written", sorted(os.listdir(OUT)))
