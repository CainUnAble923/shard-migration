import sys, re, importlib.util
src=open(r'D:/ShatteredLegacy/design/mine-camp-tents/uorender.py').read().replace("os.path.expanduser('~/mnt/ShatteredLegacy/client-data/classic-client')","r'D:/ShatteredLegacy/client-data/classic-client'")
src=src.replace("'/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'","'C:/Windows/Fonts/arialbd.ttf'")
RNS={}; exec(compile(src,'uor','exec'),RNS)
exec(open('fit.py').read())
def npcs(x0,y0,x1,y1):
    out=[]
    for line in open('nh_mobiles.txt'):
        m=re.match(r'^(\w+)\s+(\d+),(\d+),(-?\d+)\s+map1',line)
        if m:
            t,x,y,z=m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4))
            if x0<=x<=x1 and y0<=y<=y1 and t not in('Bird','Zombie','Skeleton','Bogling'): out.append((t[:10],x,y,z,(255,80,80,255)))
    return out
def go(name,x0,y0,x1,y1,cands=(),hide=None):
    marks=npcs(x0,y0,x1,y1)+[(l,x,y,z,(80,255,80,255)) for (l,x,y,z) in cands]
    deco=[(sid,x,y,z) for (x,y),v in DECO.items() for (sid,z) in v if x0<=x<=x1 and y0<=y<=y1]
    print(name, RNS['render'](1,x0,y0,x1,y1,extra=deco,marks=marks,grid=5,out=name+'.png',hide=hide))
_orig=RNS['Map'].statics
ZMAX=[127]
def _cut(self,bx,by): return [s for s in _orig(self,bx,by) if s[3] < ZMAX[0]]
RNS['Map'].statics=_cut
def go2(name,x0,y0,x1,y1,zmax,cands=()):
    ZMAX[0]=zmax
    marks=npcs(x0,y0,x1,y1)+[(l,x,y,z,(80,255,80,255)) for (l,x,y,z) in cands]
    deco=[(sid,x,y,z) for (x,y),v in DECO.items() for (sid,z) in v if x0<=x<=x1 and y0<=y<=y1 and z<zmax]
    print(name, RNS['render'](1,x0,y0,x1,y1,extra=deco,marks=marks,grid=5,out=name+'.png'))
