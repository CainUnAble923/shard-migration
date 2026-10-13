# Port of pinned Map.CanFit (Projects/Server/Maps/Map.cs:925-1010) and GetAverageZ (:243-285) over the client
# map (map1LegacyMUL.uop, statics1.mul, tiledata.mul) plus pinned's New Haven decoration items. Height 16.
import re, glob
exec(open('nhmap.py').read().split("if __name__")[0])
IMP,SURF,BRIDGE,WALL=0x40,0x200,0x400,0x10
def landz(x,y): return M.land(x,y)[1]
def avgz(x,y):
    t,l,r,b=landz(x,y),landz(x,y+1),landz(x+1,y),landz(x+1,y+1)
    low=min(t,l,r,b)
    avg=(l+r)//2 if abs(t-b)>abs(l-r) else (t+b)//2
    return low,avg
def ignored(i): return i==2 or i==0x1DB or 0x1AE<=i<=0x1B5
def calch(sid):
    h=T.sheight[sid]; return h//2 if T.sflags[sid]&BRIDGE else h
DECO={}
for f in glob.glob(r'D:/UO/ModernUO-pinned/Distribution/Data/Decoration/Trammel/*haven*.cfg'):
    cur=None
    for line in open(f,errors='replace'):
        line=line.split('#')[0].strip()
        if not line: cur=None; continue
        m=re.match(r'^[A-Za-z]\w*\s+(0x[0-9A-Fa-f]+)',line)
        if m: cur=int(m.group(1),16); continue
        m=re.match(r'^(-?\d+)\s+(-?\d+)\s+(-?\d+)$',line)
        if m and cur is not None:
            DECO.setdefault((int(m.group(1)),int(m.group(2))),[]).append((cur,int(m.group(3))))
def canfit(x,y,z,h=16,why=False):
    has=False; lid,_=M.land(x,y); low,avg=avgz(x,y); lf=T.lflags.get(lid&0x3FFF,0)
    if lf&IMP and avg>z and z+h>low: return (False,'impassable land') if why else False
    if not lf&IMP and z==avg and not ignored(lid): has=True
    tiles=[(sid,sz,'static') for (sid,sx,sy,sz,hue) in M.statics(x>>3,y>>3) if (x&7,y&7)==(sx,sy)]
    tiles+=[(sid,sz,'deco') for (sid,sz) in DECO.get((x,y),[])]
    for sid,sz,src in tiles:
        f=T.sflags[sid]; s=bool(f&SURF); i=bool(f&IMP)
        if (s or i) and sz+calch(sid)>z and z+h>sz: return (False,f'{src} 0x{sid:X} {T.sname[sid]} z{sz}') if why else False
        if s and not i and z==sz+calch(sid): has=True
    return (has,'ok' if has else 'no surface') if why else has
def surfaces(x,y):
    out=set(); lid,_=M.land(x,y); low,avg=avgz(x,y)
    if not T.lflags.get(lid&0x3FFF,0)&IMP and not ignored(lid): out.add(avg)
    for (sid,sx,sy,sz,hue) in M.statics(x>>3,y>>3):
        if (x&7,y&7)==(sx,sy) and T.sflags[sid]&SURF and not T.sflags[sid]&IMP: out.add(sz+calch(sid))
    for (sid,sz) in DECO.get((x,y),[]):
        if T.sflags[sid]&SURF and not T.sflags[sid]&IMP: out.add(sz+calch(sid))
    return sorted(z for z in out if canfit(x,y,z))
