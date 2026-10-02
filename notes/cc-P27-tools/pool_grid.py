# cc-P27: land and statics around the Fountain of Fortune's point, Ter Mur 1121,957 (map 5). Read only.
# Run from notes/cc-P15-tools. W = impassable land (water), w = water with a static, s = static on land,
# . = open land, * = the fountain's centre. Then the standable z's (fit.py's surfaces) for the same box.
exec(open('fit.py').read())
M=ns['Map'](5)
import struct
d=open(r'D:/ShatteredLegacy/client-data/classic-client/tiledata.mul','rb').read()
def lname(i):
    g,k=divmod(i,32); o=g*(4+32*30)+4+k*30
    return d[o+10:o+30].split(b'\0')[0].decode('latin1')
for i in (0xA8,0xA9,0xAA,0xAB):
    print(hex(i),lname(i),hex(T.lflags[i]))
X,Y=1121,957
for y in range(Y-8,Y+9):
    row=[]
    for x in range(X-10,X+11):
        lid,z=M.land(x,y); st=[s for (s,sx,sy,sz,h) in M.statics(x>>3,y>>3) if (x&7,y&7)==(sx,sy)]
        c='W' if T.lflags[lid&0x3FFF]&IMP else '.'
        if st: c=c.lower() if c=='W' else 's'
        if (x,y)==(X,Y): c='*'
        row.append(c)
    print(y,''.join(row))
print('surfaces, row by row, x 1111..1131:')
for y in range(Y-8,Y+9):
    print(y,' '.join(('/'.join(str(z) for z in surfaces(x,y)) or '-') for x in range(X-10,X+11)))
