import sys
sys.path.insert(0, r"D:\UO\shard-migration\scripts")
from mapbuild import isorender as iso, uofiles as U
OUT=sys.argv[1]; C=U.CLIENT
td=U.read_tiledata(C); land_td=td[0]
L=U.load_land(C,1); ids,zs=L[0],L[1]
def nm(t): return land_td[int(t)][2]
def road(x,y):
    n=nm(ids[x,y]); return n in('dirt','cobblestones') or (n=='noname')
def grass(x,y): return nm(ids[x,y])=='grass'
sta={}
for x,y,z,i in U.statics_in(C,1,3440,2555,3545,2640): sta.setdefault((x,y),[]).append((z,i))
def imp(i): 
    try: return U.impassable_item(i,C)
    except Exception as e: return False
def cands(cx,cy,r,label):
    out=[]
    for x in range(cx-r,cx+r+1):
        for y in range(cy-r,cy+r+1):
            if not grass(x,y) : continue
            if any(imp(i) for z,i in sta.get((x,y),[])): continue
            s=[road(x,y+k) for k in (1,2,3)]; n=[road(x,y-k) for k in (1,2,3)]; side=road(x-1,y) or road(x+1,y)
            if any(s) and not any(n):
                out.append((abs(x-cx)+abs(y-cy),x,y,int(zs[x,y]),'side-road' if side else 'clear',len(sta.get((x,y),[]))))
    print(label,sorted(out)[:10])
cands(3477,2617,10,'mine')
cands(3521,2573,9,'stables')
cands(3464,2596,10,'housing1')
print('sign tiles', [(p,nm(ids[p]),int(zs[p]),sta.get(p)) for p in [(3477,2617),(3521,2573),(3464,2596),(3474,2601),(3521,2572),(3520,2573)]])
art=iso.Art()
def scene(x1,y1,x2,y2,extra,name):
    s=iso.Scene.from_map(C,1,x1,y1,x2,y2); s.statics=list(s.statics)+extra
    iso.render(s,x1,y1,x2,y2,art=art).convert('RGB').save(OUT+'/'+name)
scene(3497,2525,3508,2536,[(3502,2530,22,0x0B2C),(3503,2530,22,0x0B2C)],'bench-as-built.png')
scene(3497,2525,3508,2536,[(3502,2530,22,0x0B2D),(3503,2530,22,0x0B2D)],'bench-0B2D.png')
