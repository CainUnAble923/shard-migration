import struct, sys
from PIL import Image, ImageDraw
icon_path, hues_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
hm = open(hues_path, 'rb').read()
def hue(h):
    i = h - 1; blk = i // 8; ent = i % 8; off = blk * 708 + 4 + ent * 88
    cs = struct.unpack_from('<32H', hm, off)
    name = hm[off + 68:off + 88].split(b'\0')[0].decode('ascii', 'replace')
    return [(((c >> 10) & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, (c & 31) * 255 // 31) for c in cs], name
def apply(im, h):
    if not h: return im.copy()
    cs, _ = hue(h); px = im.load(); o = im.copy(); po = o.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and r == g == b:  # PartialHue: only exact grays take the hue
                po[x, y] = cs[r >> 3] + (a,)
    return o
icon = Image.open(icon_path).convert('RGBA')
rows = [('in code now', [(0x84C, 'T1 Forester'), (0x60, 'T2 Seasoned'), (0x26C, 'T3 Arborist')]),
        ('ore ladder', [(0x8A5, 'Gold'), (0x89F, 'Verite'), (0x8AB, 'Valorite'), (0x979, 'Agapite'), (0x972, 'Bronze')]),
        ('greens', [(0x7D6, ''), (0x59B, ''), (0x48F, ''), (0x483, ''), (0x557, '')])]
S = 3; cw = 44 * S + 20
img = Image.new('RGB', (cw * 5 + 110, (40 * S + 40) * len(rows)), (60, 60, 60)); d = ImageDraw.Draw(img)
for ri, (label, hs) in enumerate(rows):
    y = ri * (40 * S + 40); d.text((4, y + 50), label, fill=(255, 255, 255))
    for ci, (h, nm) in enumerate(hs):
        t = apply(icon, h).resize((44 * S, 40 * S), Image.NEAREST)
        x = 110 + ci * cw; img.paste(t, (x, y + 4), t)
        cs, hn = hue(h); mid = cs[18]
        print(f'0x{h:X} {nm or hn!r:24} hues.mul name {hn!r:20} mid colour {mid}')
        d.text((x, y + 40 * S + 6), f'0x{h:X} {nm or hn}'[:24], fill=(255, 255, 255))
img.save(out)
