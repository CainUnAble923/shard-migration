# Read-only: decode one body's legacy animation frames from AnimationFrame*.uop and save PNG strips to scratchpad.
import struct, sys, os, zlib
from PIL import Image

def rot(x, k): return ((x << k) | (x >> (32 - k))) & 0xFFFFFFFF

def hashlittle2(s):
    s = s.encode('ascii'); length = len(s)
    a = b = c = (0xDEADBEEF + length) & 0xFFFFFFFF
    k = 0
    while length > 12:
        a = (a + (s[k] | s[k+1] << 8 | s[k+2] << 16 | s[k+3] << 24)) & 0xFFFFFFFF
        b = (b + (s[k+4] | s[k+5] << 8 | s[k+6] << 16 | s[k+7] << 24)) & 0xFFFFFFFF
        c = (c + (s[k+8] | s[k+9] << 8 | s[k+10] << 16 | s[k+11] << 24)) & 0xFFFFFFFF
        a = (a - c) & 0xFFFFFFFF; a ^= rot(c, 4); c = (c + b) & 0xFFFFFFFF
        b = (b - a) & 0xFFFFFFFF; b ^= rot(a, 6); a = (a + c) & 0xFFFFFFFF
        c = (c - b) & 0xFFFFFFFF; c ^= rot(b, 8); b = (b + a) & 0xFFFFFFFF
        a = (a - c) & 0xFFFFFFFF; a ^= rot(c, 16); c = (c + b) & 0xFFFFFFFF
        b = (b - a) & 0xFFFFFFFF; b ^= rot(a, 19); a = (a + c) & 0xFFFFFFFF
        c = (c - b) & 0xFFFFFFFF; c ^= rot(b, 4); b = (b + a) & 0xFFFFFFFF
        length -= 12; k += 12
    if length == 0:
        return (b << 32) | c
    tail = s[k:] + b'\0' * (12 - length)
    if length >= 12: c = (c + (tail[11] << 24)) & 0xFFFFFFFF
    if length >= 11: c = (c + (tail[10] << 16)) & 0xFFFFFFFF
    if length >= 10: c = (c + (tail[9] << 8)) & 0xFFFFFFFF
    if length >= 9: c = (c + tail[8]) & 0xFFFFFFFF
    if length >= 8: b = (b + (tail[7] << 24)) & 0xFFFFFFFF
    if length >= 7: b = (b + (tail[6] << 16)) & 0xFFFFFFFF
    if length >= 6: b = (b + (tail[5] << 8)) & 0xFFFFFFFF
    if length >= 5: b = (b + tail[4]) & 0xFFFFFFFF
    if length >= 4: a = (a + (tail[3] << 24)) & 0xFFFFFFFF
    if length >= 3: a = (a + (tail[2] << 16)) & 0xFFFFFFFF
    if length >= 2: a = (a + (tail[1] << 8)) & 0xFFFFFFFF
    a = (a + tail[0]) & 0xFFFFFFFF
    c ^= b; c = (c - rot(b, 14)) & 0xFFFFFFFF
    a ^= c; a = (a - rot(c, 11)) & 0xFFFFFFFF
    b ^= a; b = (b - rot(a, 25)) & 0xFFFFFFFF
    c ^= b; c = (c - rot(b, 16)) & 0xFFFFFFFF
    a ^= c; a = (a - rot(c, 4)) & 0xFFFFFFFF
    b ^= a; b = (b - rot(a, 14)) & 0xFFFFFFFF
    c ^= b; c = (c - rot(b, 24)) & 0xFFFFFFFF
    return (b << 32) | c

def read_uop_index(path):
    idx = {}
    with open(path, 'rb') as f:
        magic, ver, sig, nxt = struct.unpack('<IIIQ', f.read(20))
        while nxt:
            f.seek(nxt)
            cnt, nxt2 = struct.unpack('<iQ', f.read(12))
            for _ in range(cnt):
                off, hl, cl, dl, h, adl, flag = struct.unpack('<qiiiQIh', f.read(34))
                if off: idx[h] = (off + hl, cl, dl, flag)
            nxt = nxt2
    return idx

def decode(data):
    # AMOU header
    pos = 0
    hdr = data[:40]
    fmt, ver, dcs, anim_id = struct.unpack_from('<IIIi', data, 0)
    frame_count, data_start = struct.unpack_from('<ii', data, 32)
    frames = []
    p = data_start
    for i in range(frame_count):
        group, frame_id = struct.unpack_from('<Hh', data, p)
        pix_off, = struct.unpack_from('<I', data, p + 12)
        frames.append((group, frame_id, p + pix_off))
        p += 16
    out = []
    for group, frame_id, fp in frames:
        pal = struct.unpack_from('<256H', data, fp)
        q = fp + 512
        cx, cy, w, h = struct.unpack_from('<hhHH', data, q); q += 8
        px = []
        while True:
            header, = struct.unpack_from('<I', data, q); q += 4
            if header == 0x7FFF7FFF: break
            run = header & 0xFFF
            x = (header >> 22) & 0x3FF
            if x & 0x200: x -= 0x400
            y = (header >> 12) & 0x3FF
            if y & 0x200: y -= 0x400
            for j in range(run):
                c = pal[data[q + j]]
                px.append((x + j, y, c))
            q += run
        out.append((group, frame_id, w, h, px))
    return anim_id, out

def to_img(px):
    xs = [p[0] for p in px]; ys = [p[1] for p in px]
    mx, my = min(xs), min(ys)
    W, H = max(xs) - mx + 1, max(ys) - my + 1
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for x, y, c in px:
        r = ((c >> 10) & 31) * 255 // 31; g = ((c >> 5) & 31) * 255 // 31; b = (c & 31) * 255 // 31
        im.putpixel((x - mx, y - my), (r, g, b, 255))
    return im

if __name__ == '__main__':
    client = sys.argv[1]; body = int(sys.argv[2]); out = sys.argv[3]
    files = [os.path.join(client, f'AnimationFrame{i}.uop') for i in range(1, 7)]
    idxs = [(f, read_uop_index(f)) for f in files if os.path.exists(f)]
    for action in range(0, 40):
        key = hashlittle2(f'build/animationlegacyframe/{body:06d}/{action:02d}.bin')
        for f, idx in idxs:
            if key in idx:
                off, cl, dl, flag = idx[key]
                with open(f, 'rb') as fh:
                    fh.seek(off); raw = fh.read(cl)
                if flag in (1, 3): raw = zlib.decompress(raw)
                anim_id, frames = decode(raw)
                print(f'action {action:02d} in {os.path.basename(f)} animId={anim_id} frames={len(frames)} groups={sorted(set(g for g,_,_,_,_ in frames))}')
                if action in (0, 1, 2, 4, 5, 6, 12):
                    imgs = [to_img(fr[4]) for fr in frames[:min(len(frames), 12)] if fr[4]]
                    if imgs:
                        W = sum(i.width for i in imgs) + 4 * len(imgs); H = max(i.height for i in imgs)
                        strip = Image.new('RGBA', (W, H), (255, 255, 255, 255)); x = 0
                        for i in imgs:
                            strip.paste(i, (x, H - i.height), i); x += i.width + 4
                        strip = strip.resize((W * 2, H * 2), Image.NEAREST)
                        strip.save(os.path.join(out, f'body{body}_a{action:02d}.png'))
                break
