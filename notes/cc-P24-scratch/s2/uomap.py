# Read-only loader for UO map1 (UOP) + statics1/staidx1 + tiledata + radarcol.
import struct, numpy as np, os

W, H = 7168, 4096
BW, BH = W // 8, H // 8

def uop_hash(s):
    s = s.encode('ascii')
    length = len(s)
    eax = ecx = edx = ebx = esi = edi = 0
    ebx = edi = esi = (length + 0xDEADBEEF) & 0xFFFFFFFF
    i = 0
    M = 0xFFFFFFFF
    def rot(x, k): return ((x << k) | (x >> (32 - k))) & M
    while i + 12 < length:
        edi = (edi + (s[i+7] << 24 | s[i+6] << 16 | s[i+5] << 8 | s[i+4])) & M
        esi = (esi + (s[i+11] << 24 | s[i+10] << 16 | s[i+9] << 8 | s[i+8])) & M
        edx = ((s[i+3] << 24 | s[i+2] << 16 | s[i+1] << 8 | s[i]) - esi) & M
        edx = ((edx + ebx) ^ (esi >> 28) ^ (esi << 4)) & M
        esi = (esi + edi) & M
        edi = ((edi - edx) ^ (edx >> 26) ^ (edx << 6)) & M
        edx = (edx + esi) & M
        esi = ((esi - edi) ^ (edi >> 24) ^ (edi << 8)) & M
        edi = (edi + edx) & M
        ebx = ((edx - esi) ^ (esi >> 16) ^ (esi << 16)) & M
        esi = (esi + edi) & M
        edi = ((edi - ebx) ^ (ebx >> 13) ^ (ebx << 19)) & M
        ebx = (ebx + esi) & M
        esi = ((esi - edi) ^ (edi >> 28) ^ (edi << 4)) & M
        edi = (edi + ebx) & M
        i += 12
    if length - i > 0:
        r = length - i
        b = lambda k: s[i+k] if k < r else 0
        if r >= 9 or True:
            pass
        # fallthrough switch
        if r >= 12: esi = (esi + (b(11) << 24)) & M
        if r >= 11: esi = (esi + (b(10) << 16)) & M
        if r >= 10: esi = (esi + (b(9) << 8)) & M
        if r >= 9: esi = (esi + b(8)) & M
        if r >= 8: edi = (edi + (b(7) << 24)) & M
        if r >= 7: edi = (edi + (b(6) << 16)) & M
        if r >= 6: edi = (edi + (b(5) << 8)) & M
        if r >= 5: edi = (edi + b(4)) & M
        if r >= 4: ebx = (ebx + (b(3) << 24)) & M
        if r >= 3: ebx = (ebx + (b(2) << 16)) & M
        if r >= 2: ebx = (ebx + (b(1) << 8)) & M
        if r >= 1: ebx = (ebx + b(0)) & M
        esi = ((esi ^ edi) - ((edi >> 18) ^ (edi << 14))) & M
        ecx = ((esi ^ ebx) - ((esi >> 21) ^ (esi << 11))) & M
        edi = ((edi ^ ecx) - ((ecx >> 7) ^ (ecx << 25))) & M
        esi = ((esi ^ edi) - ((edi >> 16) ^ (edi << 16))) & M
        edx = ((esi ^ ecx) - ((esi >> 28) ^ (esi << 4))) & M
        edi = ((edi ^ edx) - ((edx >> 18) ^ (edx << 14))) & M
        eax = ((esi ^ edi) - ((edi >> 8) ^ (edi << 24))) & M
        return (edi << 32) | eax
    return (esi << 32) | eax

def load_land(path, mapname='map1legacymul'):
    data = open(path, 'rb').read()
    assert data[:4] == b'MYP\0'
    nxt = struct.unpack_from('<q', data, 12)[0]
    entries = {}
    while nxt:
        cnt, nxt2 = struct.unpack_from('<iq', data, nxt)
        p = nxt + 12
        for _ in range(cnt):
            off, hl, cl, dl, h, ad, fl = struct.unpack_from('<qiiiQIh', data, p)
            p += 34
            if off:
                entries[h] = (off + hl, dl)
        nxt = nxt2
    out = bytearray()
    i = 0
    while True:
        h = uop_hash('build/%s/%08d.dat' % (mapname, i))
        if h not in entries: break
        off, ln = entries[h]
        out += data[off:off+ln]
        i += 1
    raw = np.frombuffer(bytes(out), dtype=np.uint8)
    nblk = len(raw) // 196
    assert nblk >= BW * BH, (nblk, i)
    print('uop files', i, 'bytes', len(raw), 'extra', len(raw) - BW*BH*196)
    blk = raw[:BW*BH*196].reshape(BW * BH, 196)[:, 4:].reshape(BW * BH, 64, 3)
    tid = blk[:, :, 0].astype(np.uint16) | (blk[:, :, 1].astype(np.uint16) << 8)
    z = blk[:, :, 2].view(np.int8)
    # block index = bx*BH + by ; cell = y*8+x
    tid = tid.reshape(BW, BH, 8, 8).transpose(1, 2, 0, 3).reshape(H, W)
    z = z.reshape(BW, BH, 8, 8).transpose(1, 2, 0, 3).reshape(H, W)
    return tid, z

def load_statics(idxpath, mulpath):
    idx = np.frombuffer(open(idxpath, 'rb').read(), dtype=np.int32).reshape(-1, 3)
    mul = open(mulpath, 'rb').read()
    return idx, mul

def statics_count_grid(idx):
    # per-block static count
    lk = idx[:, 0]; ln = idx[:, 1]
    cnt = np.where((lk >= 0) & (ln > 0), ln // 7, 0)
    return cnt.reshape(BW, BH).T  # [by, bx]

def block_statics(idx, mul, bx, by):
    lk, ln, _ = idx[bx * BH + by]
    res = []
    if lk < 0 or ln <= 0: return res
    for k in range(ln // 7):
        t, x, y, z, hue = struct.unpack_from('<HBBbH', mul, lk + k * 7)
        res.append((bx * 8 + x, by * 8 + y, t, z, hue))
    return res

def area_statics(idx, mul, x0, y0, x1, y1):
    out = []
    for bx in range(x0 // 8, (x1 - 1) // 8 + 1):
        for by in range(y0 // 8, (y1 - 1) // 8 + 1):
            for s in block_statics(idx, mul, bx, by):
                if x0 <= s[0] < x1 and y0 <= s[1] < y1: out.append(s)
    return out

def load_radar(path):
    a = np.frombuffer(open(path, 'rb').read(), dtype=np.uint16)
    r = ((a >> 10) & 31) * 255 // 31
    g = ((a >> 5) & 31) * 255 // 31
    b = (a & 31) * 255 // 31
    return np.stack([r, g, b], 1).astype(np.uint8)

def load_tiledata_names(path):
    d = open(path, 'rb').read()
    # new format (HS+): land 0x4000 entries in groups of 32: 4 hdr + 32*(8 flags+2 tex+20 name)=964
    land = {}
    p = 0
    for g in range(0x4000 // 32):
        p += 4
        for i in range(32):
            fl, tex = struct.unpack_from('<QH', d, p)
            nm = d[p + 10:p + 30].split(b'\0')[0].decode('latin1')
            land[g * 32 + i] = (fl, nm)
            p += 30
    items = {}
    gi = 0
    while p + 4 <= len(d):
        p += 4
        for i in range(32):
            if p + 41 > len(d): break
            fl, wt, q, mi, u2, qty, an, u3, hue, so, val, hgt = struct.unpack_from('<QBBHBBHBBBBB', d, p)
            nm = d[p + 21:p + 41].split(b'\0')[0].decode('latin1')
            items[gi * 32 + i] = (fl, nm, hgt)
            p += 41
        gi += 1
    return land, items
