import sys
sys.path.insert(0, r"D:\UO\shard-migration\scripts")
from mapbuild import uofiles as U
C=U.CLIENT
td=U.read_tiledata(C); land_td=td[0]
L=U.load_land(C,1); ids,zs=L[0],L[1]
def nm(t): return land_td[int(t)][2]
def road(x,y):
    n=nm(ids[x,y]); return n in('dirt','cobblestones') or n=='noname' or n=='NoName'
sta={}
for x,y,z,i in U.statics_in(C,1,3455,2580,3485,2600): sta.setdefault((x,y),[]).append((z,hex(i),U.impassable_item(i,C)))
for y in range(2585,2593):
    print(y,' '.join(f"{'R' if road(x,y) else nm(ids[x,y])[0]}{int(zs[x,y]):>3}{'*' if (x,y) in sta else ' '}" for x in range(3462,3478)))
print('statics:')
for (x,y),v in sorted(sta.items()):
    if 3462<=x<=3478 and 2586<=y<=2592: print((x,y),v)
out=[]
for x in range(3458,3482):
    for y in range(2583,2600):
        if road(x,y): continue
        if any(t[2] for t in sta.get((x,y),[])): continue
        s=[road(x,y+k) for k in (1,2,3)]; n=[road(x,y-k) for k in (1,2,3)]
        if any(s) and not any(n) and not(road(x-1,y) or road(x+1,y)):
            out.append((x,y,nm(ids[x,y]),int(zs[x,y]),sta.get((x,y))))
print('rule tiles',out)
