"""cc-P241: the contact sheet of the achievement category icons, the pick and two alternates per category.

Reads Praxiiz's 44 x 44 BMPs (D:\\UO\\third-party\\spell-icons-1000\\bmp), makes pure black transparent (the only change
the package makes) and lays them out over the gump's panel tile colour, each at 1x and 2x (nearest) so the pixels show.
Writes contact-sheet.png beside this script. Run: python -P make_sheet.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

SRC = r"D:\UO\third-party\spell-icons-1000\bmp"
HERE = os.path.dirname(os.path.abspath(__file__))

# (category, [(icon, author), pick first, then the two alternates])
PICKS = [
    ("Combat", [("crossed-swords", "Lorc"), ("sword-clash", "Lorc"), ("broadsword", "Lorc")]),
    ("Skills", [("open-book", "Lorc"), ("level-four-advanced", "Sbed"), ("brain", "Lorc")]),
    ("Exploration", [("compass", "Lorc"), ("spyglass", "Lorc"), ("boot-prints", "Lorc")]),
    ("Mining", [("mining", "Lorc"), ("mine-wagon", "Delapouite"), ("mineral-heart", "Lorc")]),
    ("Crafting", [("anvil", "Lorc"), ("hammer-nails", "Lorc"), ("sewing-needle", "Lorc")]),
    ("Legacy", [("scroll-unfurled", "Lorc"), ("stone-tablet", "Lorc"), ("tattered-banner", "Lorc")]),
    ("Discovery", [("magnifying-glass", "Lorc"), ("treasure-map", "Lorc"), ("third-eye", "Lorc")]),
    ("Collection", [("swap-bag", "Lorc"), ("locked-chest", "Lorc"), ("gems", "Lorc")]),
    ("League", [("laurel-crown", "Lorc"), ("wax-seal", "Lorc"), ("medal", "Lorc")]),
    ("Mischief", [("imp-laugh", "Lorc"), ("drama-masks", "Lorc"), ("domino-mask", "Lorc")]),
]

BG = (40, 32, 24)  # near the dark panel the gump draws under its rows


def load(name):
    im = Image.open(os.path.join(SRC, name + ".bmp")).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, _ = px[x, y]
            if (r, g, b) == (0, 0, 0):
                px[x, y] = (0, 0, 0, 0)
    return im


def main():
    font = ImageFont.load_default()
    cell_w, cell_h, label_w = 190, 120, 110
    sheet = Image.new("RGB", (label_w + 3 * cell_w, 30 + len(PICKS) * cell_h), BG)
    d = ImageDraw.Draw(sheet)
    for i, head in enumerate(("PICK (shipped)", "alternate 1", "alternate 2")):
        d.text((label_w + i * cell_w + 6, 8), head, fill=(255, 215, 0) if i == 0 else (200, 200, 200), font=font)
    for r, (cat, icons) in enumerate(PICKS):
        y = 30 + r * cell_h
        d.text((8, y + 40), cat, fill=(255, 255, 255), font=font)
        for c, (name, author) in enumerate(icons):
            x = label_w + c * cell_w
            im = load(name)
            sheet.paste(im, (x + 6, y + 6), im)
            big = im.resize((88, 88), Image.NEAREST)
            sheet.paste(big, (x + 56, y + 6), big)
            d.text((x + 6, y + 98), f"{name} ({author})", fill=(255, 215, 0) if c == 0 else (190, 190, 190), font=font)
        d.line([(0, y + cell_h - 1), (sheet.width, y + cell_h - 1)], fill=(80, 70, 60))
    out = os.path.join(HERE, "contact-sheet.png")
    sheet.save(out, optimize=True)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
