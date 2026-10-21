# cc-P236: each shipped icon in each class's in-game hue, the way the client tints it (PartialHue: only exact grays
# take the hue). Reads hues.mul from the given client folder; writes one PNG.
#   python -P preview_in_game_hues.py <shattered-legacy-art\art> <client hues.mul> <out.png>
import struct, sys
from PIL import Image, ImageDraw

art, hues_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
hm = open(hues_path, 'rb').read()


def colours(h):
    i = h - 1; off = (i // 8) * 708 + 4 + (i % 8) * 88
    return [(((c >> 10) & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, (c & 31) * 255 // 31)
            for c in struct.unpack_from('<32H', hm, off)]


def tint(im, h):
    if not h:
        return im.copy()
    cs = colours(h); o = im.copy(); src = im.load(); dst = o.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = src[x, y]
            if a and r == g == b:
                dst[x, y] = cs[r >> 3] + (a,)
    return o


# (art ID, class, hue): the hues the classes set (CompactOreSatchel tiers wear their metal's, cc-P55).
rows = [
    (13184, [('T1 Compact (Iron)', 0), ('T2 Reinforced (Gold)', 0x8A5), ('T3 Surveyor (Verite)', 0x89F),
             ('T4 Deepdelver (Valorite)', 0x8AB), ('T5 Master (Platinum)', 0x481)]),
    (13185, [('T1 Forester', 0x84C), ('T2 Seasoned', 0x60), ('T3 Arborist', 0x26C)]),
    (13186, [('Hunter', 0x5B5), ('Seasoned', 0x5B2), ('Warden', 0x4B5)]),
    (13187, [('Artificer 0xDC', 0xDC), ('(old 0x497)', 0x497)]),
    (13188, [('Gemologist 1177', 1177)]),
    (13189, [('Smith salvage 1154', 1154)]),
]
S = 3; cw = 44 * S + 30; rh = 40 * S + 34
img = Image.new('RGB', (cw * 5 + 70, rh * len(rows)), (58, 58, 58)); d = ImageDraw.Draw(img)
for ri, (aid, cls) in enumerate(rows):
    icon = Image.open(f'{art}/{aid}.png').convert('RGBA')
    y = ri * rh; d.text((4, y + 50), str(aid), fill=(255, 255, 255))
    for ci, (label, h) in enumerate(cls):
        t = tint(icon, h).resize((44 * S, 40 * S), Image.NEAREST)
        x = 70 + ci * cw; img.paste(t, (x, y + 4), t)
        d.text((x, y + 40 * S + 8), label, fill=(255, 255, 255))
img.save(out)
print('wrote', out)
