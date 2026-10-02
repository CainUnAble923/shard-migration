# cc-P29 Part D: every static in and around the Fountain of Fortune's pool (Ter Mur 1121,957), with its tiledata
# flags and height in the server's data and in EA's current data; then land differences between the two map5s.
import sys
sys.path.insert(0, r'D:/UO/shard-migration/notes/cc-P29-tools')
from uodata import *
S, E = load(SERVER), load(EA)
MS, ME = S['Map'](5), E['Map'](5)
TS, TE = S['Tiles'](), E['Tiles']()
X0, X1, Y0, Y1 = 1111, 1131, 949, 967
print('statics in the box, server data:')
seen = set()
for y in range(Y0, Y1 + 1):
    for x in range(X0, X1 + 1):
        lid, lz = MS.land(x, y)
        lw = TS.lflags[lid & 0x3FFF] & IMP
        for (sid, sx, sy, sz, hue) in MS.statics(x >> 3, y >> 3):
            if (x & 7, y & 7) != (sx, sy):
                continue
            seen.add(sid)
            print(f'  {x},{y} land 0x{lid:X} z{lz}{" (water)" if lw else ""}: static 0x{sid:04X} "{TS.sname[sid]}" z{sz} '
                  f'h{TS.sheight[sid]} [{flagnames(TS.sflags[sid])}]')
print()
print('the same IDs in both tiledata files:')
for sid in sorted(seen):
    a = (TS.sname[sid], TS.sheight[sid], TS.sflags[sid]); b = (TE.sname[sid], TE.sheight[sid], TE.sflags[sid])
    mark = '' if a == b else '   <-- DIFFERS'
    print(f'  0x{sid:04X} server "{a[0]}" h{a[1]} [{flagnames(a[2])}] | EA "{b[0]}" h{b[1]} [{flagnames(b[2])}]{mark}')
print()
print('land tiles that differ between server and EA map5 in the box:')
n = 0
for y in range(Y0, Y1 + 1):
    for x in range(X0, X1 + 1):
        a, b = MS.land(x, y), ME.land(x, y)
        if a != b:
            n += 1; print(f'  {x},{y} server 0x{a[0]:X} z{a[1]} | EA 0x{b[0]:X} z{b[1]}')
print(f'  {n} differ')
print('land flags of the pool water ids:', {hex(i): (flagnames(TS.lflags[i]), flagnames(TE.lflags[i])) for i in (0xA8,0xA9,0xAA,0xAB)})
