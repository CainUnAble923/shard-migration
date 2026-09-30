# Read-only: list mobiles standing in New Haven's box on Trammel in a copied test save.
import struct, sys, collections
def types():
    b=open('SerializedTypes.db','rb').read(); p=0
    ver,cnt=struct.unpack_from('<ii',b,p); p=8; t={}
    for _ in range(cnt):
        h,=struct.unpack_from('<Q',b,p); p+=8
        n=0; sh=0
        while True:
            x=b[p]; p+=1; n|=(x&0x7f)<<sh; sh+=7
            if x<0x80: break
        t[h]=b[p:p+n].decode(); p+=n
    return t
T=types()
def idx(name):
    b=open(name+'.idx','rb').read(); ver,cnt=struct.unpack_from('<ii',b,0); p=8; out=[]
    for _ in range(cnt):
        flag=b[p]; p+=1; h,=struct.unpack_from('<Q',b,p); p+=8
        s,c,pos,ln=struct.unpack_from('<IqqI',b,p); p+=24
        out.append((T.get(h,hex(h)),s,pos,ln))
    return out
def enc(b,p):
    v=0; sh=0
    while True:
        x=b[p]; p+=1; v|=(x&0x7f)<<sh; sh+=7
        if x<0x80: return v,p
def rstr(b,p):
    f=b[p]; p+=1
    if f==0: return None,p
    n,p=enc(b,p); return b[p:p+n].decode('utf8','replace'),p+n
mb=open('Mobiles.bin','rb').read()
X0,X1,Y0,Y1 = (int(a) for a in sys.argv[1:5]) if len(sys.argv)>4 else (3400,3560,2400,2760)
rows=[]; bad=0
for tname,s,pos,ln in idx('Mobiles'):
    blob=mb[pos:pos+ln]; hit=None
    # Location (3 ints) then Body (int) then Name (string) ... then Map byte after fixed fields.
    for q in range(0, min(len(blob)-20, 400)):
        x,y,z=struct.unpack_from('<iii',blob,q)
        if not (X0<=x<=X1 and Y0<=y<=Y1 and -128<=z<=127): continue
        try:
            body,=struct.unpack_from('<i',blob,q+12)
            name,r=rstr(blob,q+16)
            gt,r=rstr(blob,r); r+=1+4+16   # criminal, kills, 4 hues
            lang,r=rstr(blob,r); r+=3+1+4+24 # female,warmode,hidden, dir, hue, 6 stats
            mp=blob[r]
            if 0<body<0x10000 and mp<=5: hit=(x,y,z,mp,name); break
        except Exception: pass
    if hit: rows.append((tname.split('.')[-1],)+hit+(hex(s),))
for r in sorted(rows, key=lambda r:(r[4],r[0])):
    if r[4]==1: print(f'{r[0]:<34} {r[1]},{r[2]},{r[3]:<4} map{r[4]} {r[5]!s:<28} {r[6]}')
print('trammel rows', sum(1 for r in rows if r[4]==1), 'other maps', collections.Counter(r[4] for r in rows))
