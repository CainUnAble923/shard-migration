# For save items near changed areas: is the item's own tile in a changed block, and did that tile change (statics or land)?
import json, os, sys
from collections import Counter
from uodata import *
here=os.path.dirname(os.path.abspath(__file__))
name=sys.argv[1]
near=json.load(open(os.path.join(here,f"saves_near_{name}.json")))
land_td, items = read_tiledata(NEW)
for fi in (0,1):
    st=set(json.load(open(os.path.join(here,"changed_statics.json")))[str(fi)]["blocks"])
    ld=set(json.load(open(os.path.join(here,"changed_land.json")))[str(fi)]["blocks"])
    io,so=load_statics_index(OLD,fi); inn,sn=load_statics_index(NEW,fi)
    lo=load_land(OLD,fi); ln_=load_land(NEW,fi)
    def tile(idx,sta,x,y): return sorted((t,z) for (t,sx,sy,z,h) in block_statics(idx,sta,(x>>3)*512+(y>>3)) if sx==(x&7) and sy==(y&7))
    inblk=[n for n in near if n.get("map")==fi and ((n["x"]>>3)*512+(n["y"]>>3)) in (st|ld)]
    chg=[]
    for n in inblk:
        x,y=n["x"],n["y"]
        a=tile(io,so,x,y); b=tile(inn,sn,x,y)
        la=(int(lo["ids"][x,y]),int(lo["z"][x,y])); lb=(int(ln_["ids"][x,y]),int(ln_["z"][x,y]))
        if a!=b or la!=lb:
            chg.append((n,a,b,la,lb))
    print(f"facet {fi}: near={len(near)} in changed blocks={len(inblk)} tile itself changed={len(chg)}")
    print("   types in changed blocks:", Counter(n["type"].split(".")[-1] for n in inblk).most_common(20))
    for n,a,b,la,lb in chg:
        fa=lambda L: [(hex(t),items[t]['name'],z) for t,z in L]
        print("  ", n["type"].split(".")[-1], n["serial"], (n["x"],n["y"],n["z"]), "land", land_td[la[0]][2], la[1], "->", land_td[lb[0]][2], lb[1], "| 114", fa(a), "| 117", fa(b))
