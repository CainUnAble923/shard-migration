# cc-P789: renders a sample line in UO's Unicode fonts 0-2 (unifont.mul, unifont1.mul, unifont2.mul), the three a
# server gump's HTML can reach in TazUO (BASEFONT SIZE: 0 or 4 -> font 1, 1-3 -> font 2, 5+ -> font 0). A unifont file
# starts with 0x10000 int32 offsets; at each glyph: sbyte x offset, sbyte y offset, byte width, byte height, then height
# rows of ((width - 1) / 8 + 1) bytes, one bit a pixel, high bit first.
#   python -P unifont-sample.py <client data dir> <out.png>
import struct, sys
from PIL import Image

TEXT = "Every new player starts here. 1. Log in and make a new character (about 6638, 3993)."


def glyphs(path):
    data = open(path, "rb").read()
    offs = struct.unpack_from("<65536i", data, 0)
    return data, offs


def draw(img, y, data, offs, text, color):
    x = 8
    for ch in text:
        o = offs[ord(ch)]
        if ch == " " or o <= 0 or o >= len(data):
            x += 6 if ch == " " else 0
            continue
        xo, yo, w, h = struct.unpack_from("<bbBB", data, o)
        stride = (w - 1) // 8 + 1 if w else 0
        p = o + 4
        for row in range(h):
            for col in range(w):
                if data[p + row * stride + col // 8] & (0x80 >> (col % 8)):
                    img.putpixel((x + xo + col, y + yo + row), color)
        x += xo + w + 1


def main():
    src, out = sys.argv[1], sys.argv[2]
    img = Image.new("RGB", (760, 120), (10, 10, 10))
    names = ["unifont.mul", "unifont1.mul", "unifont2.mul"]
    for i, n in enumerate(names):
        data, offs = glyphs(src + "/" + n)
        draw(img, 10 + i * 36, data, offs, "font %d: %s" % (i, TEXT), (244, 244, 244))
    img = img.resize((img.width * 2, img.height * 2), Image.NEAREST)
    img.save(out)


if __name__ == "__main__":
    main()
