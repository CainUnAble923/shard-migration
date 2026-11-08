"""cc-P242: a preview of the nine flying-loot animations as shipped (art 15536-15589), each frame at 2x beside an
outline the size of OSI's metal chest 0xE40 as drawn (36 x 45, measured from the client's art; no EA pixel is copied).
Writes notes/art/flying-loot/preview.png. Run: python -P preview.py <ShatteredLegacy>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ANIMS = ["longsword", "longbow", "staff", "steel armor", "shield", "ring", "gem", "potion", "clothes"]
FIRST, FRAMES, SCALE = 15536, 6, 2


def main(repo):
    art = os.path.join(repo, "player-package", "vendor", "shattered-legacy-art", "art")
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art", "flying-loot")
    os.makedirs(out_dir, exist_ok=True)
    cell_w, cell_h, label_w = 60 * SCALE, 130 * SCALE, 100
    sheet = Image.new("RGB", (label_w + (FRAMES + 1) * cell_w, 20 + len(ANIMS) * cell_h), (64, 72, 56))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    d.text((label_w + 4, 4), "frames 1-6 as shipped (2x), then an outline of OSI's metal chest 0xE40, 36 x 45 (2x)", fill=(230, 230, 230), font=font)
    for r, name in enumerate(ANIMS):
        y0 = 20 + r * cell_h
        d.text((6, y0 + cell_h // 2), f"{FIRST + r * FRAMES} {name}", fill=(255, 255, 255), font=font)
        for n in range(FRAMES):
            im = Image.open(os.path.join(art, f"{FIRST + r * FRAMES + n}.png")).convert("RGBA")
            im = im.resize((im.width * SCALE, im.height * SCALE), Image.NEAREST)
            x = label_w + n * cell_w + (cell_w - im.width) // 2
            sheet.paste(im, (x, y0 + cell_h - 6 - im.height), im)
        cw, ch = 36 * SCALE, 45 * SCALE
        cx = label_w + FRAMES * cell_w + (cell_w - cw) // 2
        d.rectangle([cx, y0 + cell_h - 6 - ch, cx + cw - 1, y0 + cell_h - 7], outline=(200, 170, 90))
        d.line([(0, y0 + cell_h - 1), (sheet.width, y0 + cell_h - 1)], fill=(90, 98, 80))
    path = os.path.join(out_dir, "preview.png")
    sheet.save(path, optimize=True)
    print(os.path.normpath(path), sheet.size)


if __name__ == "__main__":
    main(sys.argv[1])
