"""Simulate an editor's output: scratch copies of EA's Trammel map/statics with a dungeon carved
into region A and a small edit at the B1 entrance. The statics file is rewritten compacted, the way
an editor saves. Output: edited/ (scratch only, never shipped)."""
import os, shutil, struct, random, sys
sys.path.insert(0, os.path.dirname(__file__))
from uolib import *
EA = 'D:/UO/UltimaOnlineVanilla'
OUT = 'edited'; os.makedirs(OUT, exist_ok=True)
random.seed(40)
shutil.copyfile(f'{EA}/map1LegacyMUL.uop', f'{OUT}/map1LegacyMUL.uop')
off, nblocks = map_block_offsets(f'{OUT}/map1LegacyMUL.uop', 1)
X0, X1, Y0, Y1 = 5136, 5247, 1128, 1263
# rooms and corridors: a grid of rooms joined by 3-wide corridors
floor = set()
rooms = []
for rx in range(X0 + 4, X1 - 14, 22):
    for ry in range(Y0 + 4, Y1 - 14, 24):
        w, h = random.randint(9, 16), random.randint(9, 16)
        rooms.append((rx, ry, w, h))
        for x in range(rx, rx + w):
            for y in range(ry, ry + h): floor.add((x, y))
for (ax, ay, aw, ah), (bx, by, bw, bh) in zip(rooms, rooms[1:]):
    cx0, cy0, cx1, cy1 = ax + aw // 2, ay + ah // 2, bx + bw // 2, by + bh // 2
    for x in range(min(cx0, cx1), max(cx0, cx1) + 1):
        for d in range(3): floor.add((x, cy0 + d))
    for y in range(min(cy0, cy1), max(cy0, cy1) + 1):
        for d in range(3): floor.add((cx1 + d, y))
FLOOR_IDS = [0x0245, 0x0246, 0x0247, 0x0248]
with open(f'{OUT}/map1LegacyMUL.uop', 'r+b') as f:
    for (x, y) in floor:
        b = (x >> 3) * 512 + (y >> 3)
        f.seek(off(b) + 4 + ((y & 7) * 8 + (x & 7)) * 3)
        f.write(struct.pack('<Hb', random.choice(FLOOR_IDS), random.choice([0, 0, 0, 1, -1])))
# statics: walls on every floor cell that touches void, plus decor
new_statics = {}
def add(x, y, z, gid, hue=0):
    new_statics.setdefault((x >> 3) * 512 + (y >> 3), []).append((gid, x & 7, y & 7, z, hue))
for (x, y) in floor:
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if (x + dx, y + dy) not in floor and X0 <= x + dx <= X1 and Y0 <= y + dy <= Y1:
            add(x + dx, y + dy, 0, random.choice([0x01F5, 0x01F6, 0x01F7, 0x01F8]))
for (x, y) in random.sample(sorted(floor), 300):
    add(x, y, 0, random.choice([0x1363, 0x1364, 0x1365, 0x0ED4, 0x1B10]))
# B1 entrance: remove three statics, add a hole and three decor pieces
ENT = (3619 >> 3) * 512 + (2620 >> 3)
base_ent = read_statics(f'{EA}/staidx1.mul', f'{EA}/statics1.mul', ENT)
ent = base_ent[3:] + [(0x1BF5, 3619 & 7, 2620 & 7, 0, 0), (0x0F6C, 3619 & 7, 2620 & 7, 1, 1150),
                      (0x1363, 2, 2, 0, 0), (0x1365, 4, 3, 0, 0)]
# rewrite statics compacted, block order
with open(f'{EA}/staidx1.mul', 'rb') as fi: idx = bytearray(fi.read())
with open(f'{EA}/statics1.mul', 'rb') as fs: sta = fs.read()
out_s = bytearray(); out_i = bytearray(len(idx))
for b in range(nblocks):
    lookup, length, extra = struct.unpack_from('<iii', idx, b * 12)
    recs = sta[lookup:lookup + length] if lookup >= 0 and length > 0 else b''
    if b == ENT:
        recs = b''.join(struct.pack('<HBBbH', *s) for s in ent)
    if b in new_statics:
        recs = recs + b''.join(struct.pack('<HBBbH', *s) for s in new_statics[b])
    if recs:
        struct.pack_into('<iii', out_i, b * 12, len(out_s), len(recs), extra)
        out_s += recs
    else:
        struct.pack_into('<iii', out_i, b * 12, -1, -1, extra)
open(f'{OUT}/statics1.mul', 'wb').write(out_s); open(f'{OUT}/staidx1.mul', 'wb').write(out_i)
print('floor cells', len(floor), 'new statics', sum(map(len, new_statics.values())), 'blocks with statics', len(new_statics))
print('statics sizes base', len(sta), 'edited', len(out_s))
