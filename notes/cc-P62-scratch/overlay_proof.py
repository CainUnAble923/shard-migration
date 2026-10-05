# P62 Part C: overlay proof from the ENCODED output, not the input PNGs.
# Reads vendor\shattered-legacy-art\sl-anim7.bin/-idx.bin the way the client does (people slot 400, action 0,
# direction 1) and decodes with P59's decode_runs (written for EA's anim.mul, independent of
# scripts\build-equip-anims.py), then: compares every frame with its PNG, and composites it over body 401's walk
# frames from the client's anim.mul into a strip.
import os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cc-P59-scratch'))
import p59anim as A
from PIL import Image

V = r'D:\ShatteredLegacy\player-package\vendor\shattered-legacy-art'
SRC = os.path.join(V, 'anim-src', '4783')
OUT = os.path.dirname(os.path.abspath(__file__))
SLOT, ACT, DIR = 400, 0, 1
TABLE = [0x00, 0x08, 0x10, 0x18, 0x20, 0x29, 0x31, 0x39, 0x41, 0x4A, 0x52, 0x5A, 0x62, 0x6A, 0x73, 0x7B, 0x83, 0x8B,
         0x94, 0x9C, 0xA4, 0xAC, 0xB4, 0xBD, 0xC5, 0xCD, 0xD5, 0xDE, 0xE6, 0xEE, 0xF6, 0xFF]   # HuesHelper.cs:10-14
t24 = lambda c: (TABLE[(c >> 10) & 31], TABLE[(c >> 5) & 31], TABLE[c & 31])

mul = open(os.path.join(V, 'sl-anim7.bin'), 'rb').read()
idx = open(os.path.join(V, 'sl-anim7-idx.bin'), 'rb').read()
entry = 35000 + (SLOT - 400) * 175 + ACT * 5 + DIR          # CalculatePeopleGroupOffset
pos, size, _ = struct.unpack_from('<iii', idx, entry * 12)
blk = mul[pos:pos + size]
pal = struct.unpack_from('<256H', blk, 0)
n = struct.unpack_from('<i', blk, 512)[0]
offs = struct.unpack_from('<%di' % n, blk, 516)
ours = [A.decode_runs(blk, 512 + o + 8, pal) for o in offs]
nonempty = sum(1 for k in range(len(idx) // 12) if struct.unpack_from('<i', idx, k * 12)[0] != -1)
print('idx entry %d -> %d bytes at %d; %d frames; %d non-empty index entries in all' % (entry, size, pos, n, nonempty))

body = A.frames(401, 0, 1)
worst, bad = 0, 0
tiles = []
for i in range(n):
    png = Image.open(os.path.join(SRC, 'a00_d1_f%02d.png' % i)).convert('RGBA')
    want = {(x - 67, y - 98): png.getpixel((x, y))[:3] for y in range(128) for x in range(130) if png.getpixel((x, y))[3]}
    got = {(x, y): t24(c) for x, y, c in ours[i]}
    same_pos = set(got) == set(want)
    d = max(max(abs(a - b) for a, b in zip(got[p], want[p])) for p in want) if same_pos else None
    bad += not same_pos
    worst = max(worst, d or 0)
    print('f%02d: %3d px, positions %s, largest colour difference %s' % (i, len(got), 'identical' if same_pos else 'DIFFER', d))
    # body (grey, as the client draws hue 0) then ours on top, in run coordinates, as MobileView draws them.
    im = Image.new('RGBA', (130, 128), (40, 90, 40, 255))
    for x, y, c in body[i]:
        im.putpixel((x + 67, y + 98), t24(c) + (255,))
    for (x, y), c in got.items():
        im.putpixel((x + 67, y + 98), c + (255,))
    tiles.append(im)

strip = Image.new('RGBA', (130 * n, 128))
for i, t in enumerate(tiles):
    strip.paste(t, (130 * i, 0))
strip.resize((strip.width * 3, strip.height * 3), Image.NEAREST).save(os.path.join(OUT, 'overlay-proof-3x.png'))
# the same strip, mirrored, as the client draws direction 1 for a mobile facing East (Animation.cs GetAnimDirection)
mstrip = Image.new('RGBA', (130 * n, 128))
for i, t in enumerate(tiles):
    mstrip.paste(t.transpose(Image.FLIP_LEFT_RIGHT), (130 * i, 0))
mstrip.resize((strip.width * 3, strip.height * 3), Image.NEAREST).save(
    os.path.join(OUT, 'overlay-proof-mirrored-3x.png'))
print('frames with different positions: %d; largest colour difference over all: %d' % (bad, worst))
sys.exit(1 if bad else 0)
