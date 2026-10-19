# decode classic art (static and land) from the scratch art.mul/artidx.mul to PIL images; make labelled sheets.
import struct, sys, os
from PIL import Image, ImageDraw
FOLDER = r'D:\UO\cc-p167-work\scratch-client'
idx = open(FOLDER + r'\artidx.mul', 'rb').read()
mul = open(FOLDER + r'\art.mul', 'rb').read()

def rgb(px):
    return ((px >> 10 & 31) * 255 // 31, (px >> 5 & 31) * 255 // 31, (px & 31) * 255 // 31, 255)

def static_img(tid):
    look, ln, extra = struct.unpack_from('<iii', idx, (0x4000 + tid) * 12)
    if look < 0 or ln <= 0: return None
    d = mul[look:look + ln]
    flag, w, h = struct.unpack_from('<IHH', d, 0)
    lut = struct.unpack_from('<%dH' % h, d, 8)
    base = 8 + 2 * h
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); pix = im.load()
    for y in range(h):
        p = base + lut[y] * 2; x = 0
        while True:
            xo, rl = struct.unpack_from('<HH', d, p); p += 4
            if xo == 0 and rl == 0: break
            x += xo
            for i in range(rl):
                px = struct.unpack_from('<H', d, p)[0]; p += 2
                if px and x + i < w: pix[x + i, y] = rgb(px)
            x += rl
    return im

def land_img(tid):
    look, ln, extra = struct.unpack_from('<iii', idx, tid * 12)
    if look < 0 or ln <= 0: return None
    d = mul[look:look + ln]
    im = Image.new('RGBA', (44, 44), (0, 0, 0, 0)); pix = im.load(); p = 0
    for y in range(44):
        n = (y + 1) * 2 if y < 22 else (44 - y) * 2
        x0 = 22 - n // 2
        for i in range(n):
            px = struct.unpack_from('<H', d, p)[0]; p += 2
            pix[x0 + i, y] = rgb(px | 0x8000) if True else rgb(px)
    return im

def sheet(ids, kind, out, cols=8, scale=1):
    cell_w, cell_h = (60, 150) if kind == 'static' else (60, 70)
    rows = (len(ids) + cols - 1) // cols
    im = Image.new('RGB', (cols * cell_w, rows * cell_h), (40, 40, 40)); dr = ImageDraw.Draw(im)
    for i, tid in enumerate(ids):
        cx, cy = (i % cols) * cell_w, (i // cols) * cell_h
        art = static_img(tid) if kind == 'static' else land_img(tid)
        dr.text((cx + 2, cy + 2), '%04X' % tid, fill=(255, 255, 0))
        if art is not None:
            im.paste(art, (cx + (cell_w - art.width) // 2, cy + cell_h - art.height - 2), art)
    if scale != 1: im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(out)
    return out

if __name__ == '__main__':
    kind, out = sys.argv[1], sys.argv[2]
    ids = []
    for a in sys.argv[3:]:
        lo, _, hi = a.partition('-')
        ids += list(range(int(lo, 16), int(hi or lo, 16) + 1))
    print(sheet(ids, kind, out))
