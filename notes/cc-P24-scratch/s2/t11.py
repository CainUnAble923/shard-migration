from render import *
import collections
land_n, items = load_tiledata_names(D+'/tiledata.mul')
st=area_statics(idx,mul,3380,2420,3800,2780)
print('statics in area', len(st))
c=collections.Counter()
for x,y,t,z,h in st: c[items[t][1]]+=1
print([k for k in c.most_common(80)])
for kw in ('ruin','rubble','broken','debris','crumbl','damaged'):
    hits=[(x,y,t) for x,y,t,z,h in st if kw in items[t][1].lower()]
    print(kw, len(hits), collections.Counter(items[t][1] for _,_,t in hits).most_common(10))
render(3380,2420,3800,2780,'newhaven_overview.png',scale=3,grid=20)
