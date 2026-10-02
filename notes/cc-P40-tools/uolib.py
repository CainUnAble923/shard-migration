"""Readers for UO map (UOP), statics (MUL) files. Scratch research tool for cc-P40."""
import struct, os

def hashlittle2(s: bytes) -> int:
    length = len(s)
    a = b = c = (0xDEADBEEF + length) & 0xFFFFFFFF
    k = 0
    M = 0xFFFFFFFF
    def rot(x, n): return ((x << n) | (x >> (32 - n))) & M
    while length > 12:
        a = (a + (s[k] | s[k+1] << 8 | s[k+2] << 16 | s[k+3] << 24)) & M
        b = (b + (s[k+4] | s[k+5] << 8 | s[k+6] << 16 | s[k+7] << 24)) & M
        c = (c + (s[k+8] | s[k+9] << 8 | s[k+10] << 16 | s[k+11] << 24)) & M
        a = (a - c) & M; a ^= rot(c, 4);  c = (c + b) & M
        b = (b - a) & M; b ^= rot(a, 6);  a = (a + c) & M
        c = (c - b) & M; c ^= rot(b, 8);  b = (b + a) & M
        a = (a - c) & M; a ^= rot(c, 16); c = (c + b) & M
        b = (b - a) & M; b ^= rot(a, 19); a = (a + c) & M
        c = (c - b) & M; c ^= rot(b, 4);  b = (b + a) & M
        length -= 12; k += 12
    if length == 0:
        return (b << 32) | c
    tail = s[k:] + b'\0' * 12
    if length >= 12: c = (c + (tail[11] << 24)) & M
    if length >= 11: c = (c + (tail[10] << 16)) & M
    if length >= 10: c = (c + (tail[9] << 8)) & M
    if length >= 9:  c = (c + tail[8]) & M
    if length >= 8:  b = (b + (tail[7] << 24)) & M
    if length >= 7:  b = (b + (tail[6] << 16)) & M
    if length >= 6:  b = (b + (tail[5] << 8)) & M
    if length >= 5:  b = (b + tail[4]) & M
    if length >= 4:  a = (a + (tail[3] << 24)) & M
    if length >= 3:  a = (a + (tail[2] << 16)) & M
    if length >= 2:  a = (a + (tail[1] << 8)) & M
    if length >= 1:  a = (a + tail[0]) & M
    c ^= b; c = (c - rot(b, 14)) & M
    a ^= c; a = (a - rot(c, 11)) & M
    b ^= a; b = (b - rot(a, 25)) & M
    c ^= b; c = (c - rot(b, 16)) & M
    a ^= c; a = (a - rot(c, 4)) & M
    b ^= a; b = (b - rot(a, 14)) & M
    c ^= b; c = (c - rot(b, 24)) & M
    return (b << 32) | c

def uop_entries(path):
    """hash -> (data offset, comp len, decomp len, flag, entry-table position)"""
    out = {}
    with open(path, 'rb') as f:
        hdr = f.read(28)
        assert hdr[:4] == b'MYP\0', path
        nxt, = struct.unpack_from('<q', hdr, 12)
        while nxt:
            f.seek(nxt)
            cnt, nxt2 = struct.unpack('<iq', f.read(12))
            for i in range(cnt):
                pos = f.tell()
                off, hl, cl, dl, h, adler, flag = struct.unpack('<qiiiQIh', f.read(34))
                if off:
                    out[h] = (off + hl, cl, dl, flag, pos)
            nxt = nxt2
    return out

MAPS = {0: (7168, 4096), 1: (7168, 4096), 2: (2304, 1600), 3: (2560, 2048), 4: (1448, 1448), 5: (1280, 4096)}
BLOCK = 196  # 4-byte header + 64 x (u16 tile, s8 z)

def map_block_offsets(path, facet):
    """block index -> absolute file offset of its 196-byte record, for a LegacyMUL.uop map."""
    ents = uop_entries(path)
    w, h = MAPS[facet]
    nblocks = (w >> 3) * (h >> 3)
    per = 0xC4000 // BLOCK  # 4096 blocks per entry
    offs = {}
    for e in range((nblocks + per - 1) // per):
        name = f'build/map{facet}legacymul/{e:08d}.dat'.encode()
        off, cl, dl, flag, _ = ents[hashlittle2(name)]
        assert flag == 0 and cl == dl, 'compressed map entry'
        offs[e] = off
    return lambda b: offs[b // per] + (b % per) * BLOCK, nblocks

def read_statics(idx_path, sta_path, block):
    with open(idx_path, 'rb') as fi:
        fi.seek(block * 12); lookup, length, extra = struct.unpack('<iii', fi.read(12))
    if lookup < 0 or length <= 0: return []
    with open(sta_path, 'rb') as fs:
        fs.seek(lookup); raw = fs.read(length)
    return [struct.unpack_from('<HBBbH', raw, i * 7) for i in range(length // 7)]
