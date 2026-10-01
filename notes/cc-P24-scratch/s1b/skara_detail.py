# Detail of the Skara Brae-north change: per-tile statics 114 vs 117 at stock skara.cfg decoration points, and summary.
import json, re, os
from collections import Counter
from uodata import *
here=os.path.dirname(os.path.abspath(__file__))
land_td, items = read_tiledata(NEW)
cfg=r"D:\UO\ModernUO-pinned\Distribution\Data\Decoration\Britannia\skara.cfg"
lines=open(cfg,errors="replace").read().splitlines()
# find header (type line) for each coord line
deco=[]; cur=None
for i,l in enumerate(lines,1):
    m=re.match(r"\s*(\d+)\s+(\d+)\s+(-?\d+)",l)
    if m: deco.append((i,cur,int(m[1]),int(m[2]),int(m[3])))
    elif l.strip() and not l.startswith("#"): cur=l.strip()
for fi in (0,1):
    st=set(json.load(open(os.path.join(here,"changed_statics.json")))[str(fi)]["blocks"])
    ld=set(json.load(open(os.path.join(here,"changed_land.json")))[str(fi)]["blocks"])
    bh=512
    io,so=load_statics_index(OLD,fi); inn,sn=load_statics_index(NEW,fi)
    lo=load_land(OLD,fi); ln_=load_land(NEW,fi)
    def tile(idx,sta,x,y):
        return [(hex(t),items[t]["name"],z,"Imp" if items[t]["flags"]&0x40 else "", "Surf" if items[t]["flags"]&0x200 else "") for (t,sx,sy,z,h) in block_statics(idx,sta,(x>>3)*bh+(y>>3)) if sx==(x&7) and sy==(y&7)]
    print("== facet",fi)
    n=0
    for (ln,typ,x,y,z) in deco:
        b=(x>>3)*bh+(y>>3)
        if b in st or b in ld:
            o=tile(io,so,x,y); nn=tile(inn,sn,x,y)
            lchg=(lo["ids"][x,y],lo["z"][x,y])!=(ln_["ids"][x,y],ln_["z"][x,y])
            if o!=nn or lchg:
                n+=1
                print(f"skara.cfg:{ln} {typ[:50]} @({x},{y},{z}) land {land_td[lo['ids'][x,y]][2]}/{lo['z'][x,y]} -> {land_td[ln_['ids'][x,y]][2]}/{ln_['z'][x,y]}\n   114:{o}\n   117:{nn}")
    print("deco points in changed blocks with changed tile:",n, "of", sum(1 for d in deco if ((d[2]>>3)*bh+(d[3]>>3)) in (st|ld)), "in changed blocks; total cfg points", len(deco))
