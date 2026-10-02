"""Base (EA) vs edited -> our map patch: one line per changed land cell and per added/removed static.
Contains only what we changed; EA's untouched content is never copied in. Also prints the gate result."""
import sys, os, struct, hashlib, json
sys.path.insert(0, os.path.dirname(__file__))
from uolib import *
from collections import Counter
EA, ED, FACET = sys.argv[1], sys.argv[2], 1
offB, n = map_block_offsets(f'{EA}/map1LegacyMUL.uop', FACET)
offE, _ = map_block_offsets(f'{ED}/map1LegacyMUL.uop', FACET)
fb, fe = open(f'{EA}/map1LegacyMUL.uop', 'rb'), open(f'{ED}/map1LegacyMUL.uop', 'rb')
ib, sb = open(f'{EA}/staidx1.mul', 'rb').read(), open(f'{EA}/statics1.mul', 'rb').read()
ie, se = open(f'{ED}/staidx1.mul', 'rb').read(), open(f'{ED}/statics1.mul', 'rb').read()
def statics(idx, sta, b):
    lk, ln, _ = struct.unpack_from('<iii', idx, b * 12)
    if lk < 0 or ln <= 0: return []
    return [struct.unpack_from('<HBBbH', sta, lk + i * 7) for i in range(ln // 7)]
lines, touched = [], {}
for b in range(n):
    fb.seek(offB(b)); fe.seek(offE(b)); rb, re_ = fb.read(196), fe.read(196)
    bx, by = divmod(b, 512)
    if rb[4:] != re_[4:]:
        touched.setdefault(b, set()).add('land')
        for i in range(64):
            if rb[4 + i*3:7 + i*3] != re_[4 + i*3:7 + i*3]:
                t, z = struct.unpack_from('<Hb', re_, 4 + i*3)
                lines.append(f'L {bx*8 + i % 8} {by*8 + i // 8} {t} {z}')
    sB, sE = statics(ib, sb, b), statics(ie, se, b)
    if sB != sE:
        touched.setdefault(b, set()).add('statics')
        cB, cE = Counter(sB), Counter(sE)
        for s, k in (cB - cE).items():
            lines += [f'S- {bx*8 + s[1]} {by*8 + s[2]} {s[3]} {s[0]} {s[4]}'] * k
        for s, k in (cE - cB).items():
            lines += [f'S+ {bx*8 + s[1]} {by*8 + s[2]} {s[3]} {s[0]} {s[4]}'] * k
# base fingerprint of each touched block: a hash, not EA's bytes. Lets the applier see EA change our area.
fp = {}
for b, kinds in sorted(touched.items()):
    fb.seek(offB(b)); h = hashlib.sha256(fb.read(196)[4:] + b''.join(struct.pack('<HBBbH', *s) for s in statics(ib, sb, b))).hexdigest()[:16]
    fp[b] = h
hdr = ['# Shattered Legacy map patch, facet 1 (Trammel). Ours only: every line is a change we made.',
       '# L x y tile z  |  S+ x y z id hue (add)  |  S- x y z id hue (remove one EA static)',
       f'F 1 {len(fp)}'] + [f'B {b} {h}' for b, h in fp.items()]
open('trammel.mapops', 'w', newline='\n').write('\n'.join(hdr + sorted(lines, key=lambda l: (l[0], l))) + '\n')
c = Counter(l.split()[0] for l in lines)
print('ops', dict(c), 'blocks touched', len(touched))
