# cc-P11: decode ClusterFAccountPersistence's bytes with offsets. Usage: python extract.py blob.bin; python this.py blob.bin
# extract.py: reads Saves/Items/Items.idx (v3: flag byte, u64 type hash, u32 serial, i64 created, i64 pos, i32 len) READ-ONLY.
# --- extract.py (fix: each idx entry is 1+8+4+8+8+4 = 33 bytes) ---
# import struct, sys
# d = r'D:\ShatteredLegacy\server\lib\uo\modernuo\Saves\Items'
# idx = open(d + r'\Items.idx','rb').read()
# ver, cnt = struct.unpack_from('<ii', idx, 0); p = 8
# print('idx version', ver, 'count', cnt)
# target = 0x40128E03; hits=[]
# from collections import Counter
# for i in range(cnt):
#     flag = idx[p]; p+=1
#     h, = struct.unpack_from('<Q', idx, p); p+=8
#     serial, created, pos, length = struct.unpack_from('<IqqI', idx, p); p += 4+8+8+4
#     if serial == target: hits.append((h, serial, created, pos, length))
# print(hits)
# h, serial, created, pos, length = hits[0]
# bin_ = open(d + r'\Items.bin','rb').read()
# blob = bin_[pos:pos+length]
# open(sys.argv[1],'wb').write(blob)
# print('blob', len(blob))
# # other objects of same type
# same=[]; p=8
# for i in range(cnt):
#     p+=1; hh,=struct.unpack_from('<Q',idx,p); p+=8
#     s,c,po,l=struct.unpack_from('<IqqI',idx,p); p+=28
#     if hh==h: same.append(hex(s))
# print('same-type objects', same)
# --- decoder (wood entries: v0 flat, v1 with locations) ---
import struct, sys, datetime
b = open(sys.argv[1],'rb').read()
MAXT = 3155378975999999999
class R:
    def __init__(s,p): s.p=p
    def i(s): v,=struct.unpack_from('<i',b,s.p); s.p+=4; return v
    def u(s): v,=struct.unpack_from('<I',b,s.p); s.p+=4; return v
    def q(s): v,=struct.unpack_from('<q',b,s.p); s.p+=8; return v
    def bo(s): v=b[s.p]; s.p+=1; return v
    def enc(s):
        v=0; sh=0
        while True:
            x=b[s.p]; s.p+=1; v|=(x&0x7f)<<sh; sh+=7
            if x<0x80: return v
    def st(s):
        f=s.bo()
        if f==0: return None
        if f!=1: raise Exception(f'bad string prefix {f} at {s.p-1}')
        n=s.enc(); v=b[s.p:s.p+n].decode('utf8','replace'); s.p+=n; return v
    def dt(s):
        at=s.p; t=s.q()
        if not (0<=t<=MAXT): raise Exception(f'IMPOSSIBLE TICKS {t} (0x{t&0xffffffffffffffff:016x}) at offset {at}')
        return datetime.datetime(1,1,1)+datetime.timedelta(microseconds=t//10)
    def bits(s):
        n=s.enc(); s.p+=(n+7)//8; return n

# find start: [0][count][01 len name][13]
cands=[]
for p in range(0, 400):
    try:
        r=R(p); v=r.i(); c=r.i()
        if v!=0 or not (0<c<10000): continue
        name=r.st()
        if name and name.isprintable() and 0<len(name)<40 and r.i()==13: cands.append((p,c,name))
    except Exception: pass
print('candidates', cands)
start,count,_=cands[0]
r=R(start+8)
log=lambda *a: print(f'{r.p:>8}', *a)
for acct in range(count):
    name=r.st(); a0=r.p; ver=r.i()
    try:
        ren,ap,bul=r.i(),r.i(),r.i()
        rep=r.i(); [ (r.st(),r.i()) for _ in range(rep)]
        cur=r.i(); [ (r.st(),r.i()) for _ in range(cur)]
        reg=r.i()
        for _ in range(reg):
            r.i(); r.st(); r.st(); r.dt(); r.i(); r.bo()
            if r.bo(): r.dt()
        jg=r.i(); [r.st() for _ in range(jg)]
        fl=r.i(); [r.st() for _ in range(fl)]
        fv=r.i(); [(r.st(),r.st()) for _ in range(fv)]
        wo=[]
        for lst in ('active','completed'):
            n=r.i(); wo.append(n)
            for _ in range(n):
                wv=r.i(); r.st(); r.st(); r.dt()
                if r.bo(): r.dt()
                if wv>=1:
                    for _ in range(r.i()): r.st(); r.i()
        od=r.i()
        for _ in range(od):
            ov=r.i(); r.st(); r.i(); r.i()
            for _ in range(r.i()):
                r.st(); r.st(); r.i();r.i();r.i(); r.dt(); r.i()
                if ov>=2: r.bo()
        sc=r.i()
        for _ in range(sc):
            r.i(); r.st(); r.st(); r.i(); r.bo(); r.st(); r.st(); r.i(); r.i(); r.dt()
        sl=r.i()
        for _ in range(sl):
            r.i(); r.st(); r.st(); r.i(); r.bo(); r.st(); r.st(); r.i(); r.i(); r.dt()
            for _ in range(r.i()): r.st()
        chunksAt=r.p; ch=r.i(); nb=0
        for _ in range(ch):
            r.u()
            for f in range(6):
                if r.bo(): nb+=1; r.bits()
        ecAt=r.p; ec=r.i(); ecn=[r.st() for _ in range(ec)]
        wdAt=r.p; wd=r.i(); wds=[]
        for _ in range(wd):
            e0=r.p; wv=r.i(); k=r.st(); tc=r.i(); stt=r.i()
            if wv==0: ff=r.dt(); locs=1
            else:
                locs=r.i()
                for _ in range(locs): r.st(); r.st(); r.i();r.i();r.i(); ff=r.dt(); r.i()
            wds.append((wv,k,tc,stt,locs))
        idc=r.i(); [(r.st(),r.i()) for _ in range(idc)]
        ak=r.st(); asr=r.u()
        print(f'OK acct#{acct} {name!r} v{ver} at {a0}-{r.p}: rep{rep} cur{cur} reg{reg} jg{jg} fl{fl} fv{fv} wo{wo} ore{od} sc{sc} sl{sl} chunks{ch}@{chunksAt} bitarrays{nb} ec{ec}@{ecAt} wood{wd}@{wdAt} {wds} imb{idc} art={ak!r},{asr}')
    except Exception as e:
        print(f'FAIL acct#{acct} {name!r} v{ver} starting {a0}: {e}  (reader at {r.p})')
        print('bytes around:', b[r.p-40:r.p+24].hex(' '))
        break
print('end', r.p, 'blob length', len(b))
