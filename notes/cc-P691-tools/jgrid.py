import sys
sys.path.insert(0, r"D:/UO/golems/Iron/shard-migration/scripts")
from mapbuild import uofiles
STOCK = r"D:/UO/UltimaOnlineVanilla"
ids, zs = uofiles.load_land(STOCK, 1)
x1,x2,y1,y2=[int(a) for a in sys.argv[1:5]]
st = uofiles.statics_in(STOCK, 1, x1,y1,x2,y2)
from collections import defaultdict
d=defaultdict(list)
for s in st: d[(s[0],s[1])].append(s)
for y in range(y1,y2+1):
    cells=[]
    for x in range(x1,x2+1):
        s=d.get((x,y),[])
        cells.append("%03x/%+d%s" % (ids[x,y], zs[x,y], ("*%d" % len(s)) if s else "  "))
    print(y, " ".join(cells))
print([ (s[0],s[1],hex(s[3]) if len(s)>3 else s) for s in st][:80])
